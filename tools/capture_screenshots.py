"""Capture screenshots of the running flash card window.

@file capture_screenshots.py
@brief Starts the program, grabs the level screen, the front of a card and,
three seconds later, the back, and saves them as PNG files.

The tool needs Pillow (`python -m pip install -e ".[tools]"`), which is a tool
dependency only and not a dependency of the program. It grabs the screen area
of the window, so it needs a visible desktop.
"""

from __future__ import annotations

import argparse
import ctypes
import random
import shutil
import sys
import tempfile
import time
from collections.abc import Sequence
from pathlib import Path

from PIL import ImageGrab

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from flash_card.constants import (  # noqa: E402
    DEFAULT_DATA_DIR,
    FLIP_DELAY_MS,
    PROJECT_ROOT,
    VOCABULARY_FILE_NAME,
)
from flash_card.domain.value_objects.level import Level  # noqa: E402
from flash_card.presentation.app import create_application  # noqa: E402
from flash_card.presentation.features.flash_card.flash_card_view import (  # noqa: E402
    FlashCardView,
)

## @brief Default folder of the screenshots.
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "images"
## @brief Seed that makes the first card the same on every run.
SCREENSHOT_SEED = 7
## @brief Extra time in seconds to let the window settle before a grab.
SETTLE_SECONDS = 0.5


def _make_dpi_aware() -> None:
    """Make Windows report real pixel coordinates (no effect elsewhere)."""
    if sys.platform == "win32":
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # type: ignore[attr-defined,unused-ignore]


def _pump(root: object, seconds: float) -> None:
    """Run the Tk event loop for a while.

    @param root The Tk root window.
    @param seconds How long to run.
    """
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        root.update()  # type: ignore[attr-defined]
        time.sleep(0.01)


def capture(output_dir: Path) -> list[Path]:
    """Capture the level screen, then the front and the back of one card.

    @param output_dir Folder to write `screenshot-level.png`,
        `screenshot-front.png` and `screenshot-back.png` into.
    @return The three files written: level, front, back.
    """
    _make_dpi_aware()
    output_dir.mkdir(parents=True, exist_ok=True)
    random.seed(SCREENSHOT_SEED)
    level = output_dir / "screenshot-level.png"
    front = output_dir / "screenshot-front.png"
    back = output_dir / "screenshot-back.png"
    with tempfile.TemporaryDirectory() as data_dir:
        shutil.copy(DEFAULT_DATA_DIR / VOCABULARY_FILE_NAME, data_dir)
        application = create_application(Path(data_dir), speech_enabled=False)
        root = application.root
        root.lift()
        root.attributes("-topmost", True)
        _pump(root, SETTLE_SECONDS)
        window_box = (
            root.winfo_rootx(),
            root.winfo_rooty(),
            root.winfo_rootx() + root.winfo_width(),
            root.winfo_rooty() + root.winfo_height(),
        )
        ImageGrab.grab(bbox=window_box).save(level)
        application.start(Level(None))
        view = application.view
        if not isinstance(view, FlashCardView):
            raise RuntimeError("the card window did not open")
        _pump(root, SETTLE_SECONDS)
        box = (
            view.canvas.winfo_rootx() - 20,
            view.canvas.winfo_rooty() - 20,
            view.canvas.winfo_rootx() + view.canvas.winfo_width() + 20,
            view.canvas.winfo_rooty()
            + view.canvas.winfo_height()
            + view.right_button.winfo_height()
            + 20,
        )
        ImageGrab.grab(bbox=box).save(front)
        _pump(root, FLIP_DELAY_MS / 1000 + SETTLE_SECONDS)
        ImageGrab.grab(bbox=box).save(back)
        root.destroy()
    return [level, front, back]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the tool.

    @param argv Command line arguments, or None for `sys.argv`.
    @return The exit code, 0 on success.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    for path in capture(args.output_dir):
        sys.stdout.write(f"{path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
