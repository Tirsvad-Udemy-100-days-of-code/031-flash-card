"""Smoke driver that clicks the known button of the running program.

@file smoke_driver.py
@brief Starts the program on the current X display, finds its window with
xdotool, clicks the tick button and checks that one card was saved as known.

Uses the standard library only, so it runs in a bare container. It needs
`xdotool` and a DISPLAY. Exit code 0 only when every run is ok.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

## @brief Title of the program window.
WINDOW_NAME = "Flashy"
## @brief X of the tick button, in window pixels.
KNOWN_BUTTON_X = 650
## @brief Distance of the tick button centre above the bottom window edge.
KNOWN_BUTTON_BOTTOM_OFFSET = 101
## @brief Seconds between two polls.
POLL_SECONDS = 0.25
## @brief Seconds to wait for the progress file after the click.
PROGRESS_TIMEOUT_SECONDS = 5.0
## @brief Name of the vocabulary file written for a run.
VOCABULARY_NAME = "ms-da.csv"
## @brief Name of the progress file the program writes.
PROGRESS_NAME = "words_to_learn.csv"


class Running(Protocol):
    """A started program that can be stopped."""

    def stop(self) -> None:
        """Stop the program and its children."""


## @brief Runs a command and returns its stdout ("" when it fails).
RunCommand = Callable[[Sequence[str]], str]
## @brief Starts the program and returns a handle to stop it.
StartProgram = Callable[[Sequence[str]], Running]
## @brief Waits for a number of seconds.
Sleep = Callable[[float], None]


def known_button_point(width: int, height: int) -> tuple[int, int]:
    """Return the click point of the known button inside the window.

    @param width Window width in pixels (the button x is fixed).
    @param height Window height in pixels.
    @return X and Y relative to the window.
    """
    return KNOWN_BUTTON_X, height - KNOWN_BUTTON_BOTTOM_OFFSET


def words_file_text(count: int) -> str:
    """Return the text of a vocabulary file with count cards.

    @param count Number of cards.
    @return A `ms;da` header and the lines `w1;t1`, `w2;t2`, ...
    """
    lines = ["ms;da", *(f"w{i};t{i}" for i in range(1, count + 1))]
    return "\n".join(lines) + "\n"


def parse_geometry(shell_output: str) -> tuple[int, int]:
    """Read the size from `xdotool getwindowgeometry --shell`.

    @param shell_output The KEY=VALUE lines.
    @return Width and height.
    @throws ValueError When WIDTH or HEIGHT is missing.
    """
    values: dict[str, int] = {}
    for line in shell_output.splitlines():
        key, _, value = line.partition("=")
        if key in ("WIDTH", "HEIGHT") and value.strip().isdigit():
            values[key] = int(value)
    if "WIDTH" not in values or "HEIGHT" not in values:
        raise ValueError("no WIDTH and HEIGHT in the geometry output")
    return values["WIDTH"], values["HEIGHT"]


def progress_ok(rows: int, words: int) -> bool:
    """Tell whether the progress file shows exactly one card known.

    @param rows Lines in the progress file, the header included.
    @param words Cards at the start.
    @return True when the file has the header and words - 1 cards.
    """
    return rows == words


class _Process:
    """A real subprocess, stopped as a whole process group."""

    def __init__(self, process: subprocess.Popen[bytes]) -> None:
        self._process = process

    def stop(self) -> None:
        """Terminate the process group, then kill it if it stays."""
        try:
            os.killpg(self._process.pid, signal.SIGTERM)  # type: ignore[attr-defined,unused-ignore]
            self._process.wait(timeout=3)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            self._process.kill()


def real_run(args: Sequence[str]) -> str:
    """Run a command and return stdout, or "" when it fails."""
    try:
        done = subprocess.run(args, capture_output=True, text=True, check=False)
    except OSError:
        return ""
    return done.stdout if done.returncode == 0 else ""


def real_start(command: Sequence[str]) -> Running:
    """Start the program in its own process group."""
    return _Process(subprocess.Popen(command, start_new_session=True))


@dataclass(frozen=True)
class RunResult:
    """The outcome of one run."""

    window: bool
    clicked: tuple[int, int] | None
    progress_rows: int
    ok: bool


def _count_rows(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8").splitlines())


def _wait_for_window(run: RunCommand, sleep: Sleep, timeout: float) -> str | None:
    waited = 0.0
    while True:
        found = run(["xdotool", "search", "--name", WINDOW_NAME]).split()
        if found:
            return found[0]
        if waited >= timeout:
            return None
        sleep(POLL_SECONDS)
        waited += POLL_SECONDS


def _wait_for_progress(path: Path, sleep: Sleep) -> int:
    waited = 0.0
    rows = _count_rows(path)
    while rows == 0 and waited < PROGRESS_TIMEOUT_SECONDS:
        sleep(POLL_SECONDS)
        waited += POLL_SECONDS
        rows = _count_rows(path)
    return rows


def run_once(
    command: Sequence[str],
    words: int,
    timeout: float,
    run: RunCommand,
    start: StartProgram,
    sleep: Sleep = time.sleep,
) -> RunResult:
    """Start the program, click the known button and check the progress file.

    @param command The program command.
    @param words Number of cards in the vocabulary.
    @param timeout Seconds to wait for the window.
    @param run Runs xdotool.
    @param start Starts the program.
    @param sleep Waits between polls.
    @return The result of the run.
    """
    folder = Path(tempfile.mkdtemp(prefix="flash-card-smoke-"))
    data = folder / "data"
    data.mkdir()
    (data / VOCABULARY_NAME).write_text(words_file_text(words), encoding="utf-8")
    argv = [*command, "--data-dir", str(data), "--level", "all", "--no-speech"]
    program = start(argv)
    try:
        window = _wait_for_window(run, sleep, timeout)
        if window is None:
            return RunResult(False, None, 0, False)
        width, height = parse_geometry(
            run(["xdotool", "getwindowgeometry", "--shell", window])
        )
        x, y = known_button_point(width, height)
        run(["xdotool", "mousemove", "--window", window, str(x), str(y), "click", "1"])
        rows = _wait_for_progress(data / PROGRESS_NAME, sleep)
        return RunResult(True, (x, y), rows, progress_ok(rows, words))
    finally:
        program.stop()
        shutil.rmtree(folder, ignore_errors=True)


def main(
    argv: Sequence[str] | None = None,
    run: RunCommand = real_run,
    start: StartProgram = real_start,
    sleep: Sleep = time.sleep,
) -> int:
    """Run the driver.

    @param argv Command line arguments, or None for `sys.argv`.
    @param run Runs xdotool.
    @param start Starts the program.
    @param sleep Waits between polls.
    @return 0 when every run is ok, otherwise 1.
    """
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--words", type=int, default=3)
    parser.add_argument("--command", nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args(argv)
    passed = 0
    for index in range(1, args.repeat + 1):
        began = time.monotonic()
        result = run_once(args.command, args.words, args.timeout, run, start, sleep)
        passed += result.ok
        line = {
            "run": index,
            "window": result.window,
            "clicked": list(result.clicked) if result.clicked else None,
            "progress_rows": result.progress_rows,
            "ok": result.ok,
            "seconds": round(time.monotonic() - began, 2),
        }
        sys.stdout.write(json.dumps(line) + "\n")
    summary = {"runs": args.repeat, "passed": passed}
    sys.stdout.write(json.dumps(summary) + "\n")
    return 0 if passed == args.repeat else 1


if __name__ == "__main__":
    raise SystemExit(main())
