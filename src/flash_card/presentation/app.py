"""Entry point and composition root of the flash card program.

@file app.py
@brief Creates the window, its view model and view, and runs the main loop.
"""

import tkinter as tk
from collections.abc import Sequence
from typing import NoReturn

from flash_card.presentation.features.flash_card.flash_card_view import FlashCardView
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)


def create_application() -> tuple[tk.Tk, FlashCardView]:
    """Create the root window and the flash card view.

    @return The root window and the view built on it.
    """
    root = tk.Tk()
    view = FlashCardView(root, FlashCardViewModel())
    return root, view


def main(argv: Sequence[str] | None = None) -> int:
    """Run the program and return its exit code.

    @param argv Command line arguments, or None for none.
    @return The exit code, 0 on success.
    """
    root, _view = create_application()
    root.mainloop()
    return 0


def run() -> NoReturn:
    """Run the program and exit the interpreter with its exit code.

    @return Never returns; the function always raises SystemExit.
    @throws SystemExit Always, with the exit code of main.
    """
    raise SystemExit(main())
