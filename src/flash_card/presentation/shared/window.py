"""Window set-up shared by the screens.

@file window.py
@brief Gives the root window its title, padding and background.
"""

import tkinter as tk

from flash_card.constants import BACKGROUND_COLOR, WINDOW_PADDING, WINDOW_TITLE


def configure_window(root: tk.Tk) -> None:
    """Set the title, padding and background of the window.

    @param root The Tk root window.
    @return Nothing.
    """
    root.title(WINDOW_TITLE)
    root.config(padx=WINDOW_PADDING, pady=WINDOW_PADDING, bg=BACKGROUND_COLOR)
