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
import os
import random
import shutil
import sys
import tempfile
import time
import tkinter as tk
from collections.abc import Sequence
from pathlib import Path

from PIL import Image, ImageGrab

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
## @brief Height in pixels of the menu bar above the client area on X11.
MENU_BAR_HEIGHT_X11 = 28
## @brief Platform kind of Windows.
KIND_WINDOWS = "windows"
## @brief Platform kind of every other platform (an X11 display).
KIND_X11 = "x11"


def platform_kind(platform: str) -> str:
    """Choose how to grab the screen.

    @param platform A `sys.platform` value.
    @return "windows" for win32, otherwise "x11".
    """
    return KIND_WINDOWS if platform == "win32" else KIND_X11


def window_box(
    kind: str, rootx: int, rooty: int, width: int, height: int, menu_height: int
) -> tuple[int, int, int, int]:
    """Return the screen box to grab for a window.

    @param kind The platform kind from `platform_kind`.
    @param rootx Left edge of the client area.
    @param rooty Top edge of the client area.
    @param width Width of the client area.
    @param height Height of the client area.
    @param menu_height Height of the menu bar above the client area; it is
        added on X11 only, as on Windows the frame box is read from the system.
    @return Left, top, right and bottom in screen pixels.
    """
    top = rooty - menu_height if kind == KIND_X11 else rooty
    return rootx, top, rootx + width, rooty + height


def _grab(box: tuple[int, int, int, int]) -> Image.Image:
    """Grab a screen box on the current platform."""
    if platform_kind(sys.platform) == KIND_X11:
        return ImageGrab.grab(bbox=box, xdisplay=os.environ.get("DISPLAY"))
    return ImageGrab.grab(bbox=box)


def _make_dpi_aware() -> None:
    """Make Windows report real pixel coordinates (no effect elsewhere)."""
    if sys.platform == "win32":
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # type: ignore[attr-defined,unused-ignore]


def _frame_box(root: tk.Tk) -> tuple[int, int, int, int]:
    """Return the screen box of the whole window, with title bar and menu bar.

    @param root The Tk root window.
    @return Left, top, right and bottom in screen pixels.
    """
    import ctypes.wintypes  # Windows only, so it is imported here

    handle = ctypes.windll.user32.GetParent(root.winfo_id())  # type: ignore[attr-defined,unused-ignore]
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(handle, ctypes.byref(rect))  # type: ignore[attr-defined,unused-ignore]
    # Windows 11 adds an invisible resize border of about 7 pixels at the left,
    # the right and the bottom; cut it so no other window is in the picture.
    border = 7
    return rect.left + border, rect.top, rect.right - border, rect.bottom - border


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
        `screenshot-front.png`, `screenshot-back.png` and `screenshot-menu.png`
        (the whole window with its menu bar) into.
    @return The four files written: level, front, back, menu.
    """
    _make_dpi_aware()
    output_dir.mkdir(parents=True, exist_ok=True)
    random.seed(SCREENSHOT_SEED)
    level = output_dir / "screenshot-level.png"
    menu = output_dir / "screenshot-menu.png"
    front = output_dir / "screenshot-front.png"
    back = output_dir / "screenshot-back.png"
    with tempfile.TemporaryDirectory() as data_dir:
        shutil.copy(DEFAULT_DATA_DIR / VOCABULARY_FILE_NAME, data_dir)
        application = create_application(Path(data_dir), speech_enabled=False)
        root = application.root
        root.lift()
        root.attributes("-topmost", True)
        _pump(root, SETTLE_SECONDS)
        kind = platform_kind(sys.platform)
        client = (
            root.winfo_rootx(),
            root.winfo_rooty(),
            root.winfo_width(),
            root.winfo_height(),
        )
        _grab(window_box(kind, *client, 0)).save(level)
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
        _grab(box).save(front)
        if kind == KIND_WINDOWS:
            menu_box = _frame_box(root)
        else:
            menu_box = window_box(kind, *client, MENU_BAR_HEIGHT_X11)
        _grab(menu_box).save(menu)
        _pump(root, FLIP_DELAY_MS / 1000 + SETTLE_SECONDS)
        _grab(box).save(back)
        root.destroy()
    return [level, front, back, menu]


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
