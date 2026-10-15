"""Tests of the smoke driver tool.

@file test_smoke_driver.py
@brief Checks the pure helpers and the run loop of tools/docker/smoke_driver.py
with a fake xdotool and a fake program.
"""

import importlib.util
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

import pytest

_TOOL_PATH = (
    Path(__file__).resolve().parents[2] / "tools" / "docker" / "smoke_driver.py"
)
_GEOMETRY = "WINDOW=7\nX=0\nY=0\nWIDTH=900\nHEIGHT=800\nSCREEN=0\n"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("smoke_driver", _TOOL_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # dataclasses looks the module up by name while the class is built
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class _FakeProgram:
    def __init__(self) -> None:
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


class _FakeSystem:
    """Fake xdotool and program; a click writes the progress file."""

    def __init__(self, has_window: bool, writes_progress: bool) -> None:
        self.has_window = has_window
        self.writes_progress = writes_progress
        self.program = _FakeProgram()
        self.data_dir: Path | None = None

    def start(self, command: Sequence[str]) -> _FakeProgram:
        self.data_dir = Path(command[command.index("--data-dir") + 1])
        return self.program

    def run(self, args: Sequence[str]) -> str:
        if args[1] == "search":
            return "7\n" if self.has_window else ""
        if args[1] == "getwindowgeometry":
            return _GEOMETRY
        if args[1] == "mousemove" and self.writes_progress:
            assert self.data_dir is not None
            progress = self.data_dir / "words_to_learn.csv"
            progress.write_text("ms;da\nw1;t1\nw2;t2\n", encoding="utf-8")
        return ""


def test_known_button_point_is_101_above_bottom() -> None:
    assert _load_tool().known_button_point(900, 800) == (650, 699)


def test_words_file_text_has_header_and_cards() -> None:
    assert _load_tool().words_file_text(2) == "ms;da\nw1;t1\nw2;t2\n"


def test_parse_geometry_reads_width_and_height() -> None:
    assert _load_tool().parse_geometry(_GEOMETRY) == (900, 800)


def test_parse_geometry_fails_without_size() -> None:
    with pytest.raises(ValueError):
        _load_tool().parse_geometry("X=0\n")


def test_progress_ok_needs_exactly_one_card_less() -> None:
    tool = _load_tool()
    assert tool.progress_ok(3, 3)
    assert not tool.progress_ok(4, 3)
    assert not tool.progress_ok(0, 3)


def test_main_returns_zero_when_click_saves_progress(
    capsys: pytest.CaptureFixture[str],
) -> None:
    system = _FakeSystem(has_window=True, writes_progress=True)
    code = _load_tool().main(
        ["--repeat", "2", "--words", "3", "--command", "prog", "-m", "x"],
        run=system.run,
        start=system.start,
        sleep=lambda _: None,
    )
    lines = [json.loads(x) for x in capsys.readouterr().out.splitlines()]
    assert code == 0
    assert lines[0]["ok"] is True
    assert lines[0]["clicked"] == [650, 699]
    assert lines[-1] == {"runs": 2, "passed": 2}
    assert system.program.stopped


def test_main_fails_when_no_window_appears(
    capsys: pytest.CaptureFixture[str],
) -> None:
    system = _FakeSystem(has_window=False, writes_progress=False)
    code = _load_tool().main(
        ["--repeat", "1", "--timeout", "1", "--command", "prog"],
        run=system.run,
        start=system.start,
        sleep=lambda _: None,
    )
    first = json.loads(capsys.readouterr().out.splitlines()[0])
    assert code == 1
    assert first["window"] is False
    assert system.program.stopped
