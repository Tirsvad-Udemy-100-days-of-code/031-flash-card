"""View of the level screen.

@file level_view.py
@brief Builds the level screen of the wireframe: a title and one button per level.
"""

import tkinter as tk
from collections.abc import Callable

from flash_card.constants import (
    BACKGROUND_COLOR,
    CARD_WIDTH,
    LEVEL_BUTTON_COLOR,
    LEVEL_BUTTON_FONT,
    LEVEL_BUTTON_WIDTH,
    LEVEL_SCREEN_HEIGHT,
    LEVEL_TITLE_FONT,
)
from flash_card.domain.value_objects.level import Level
from flash_card.presentation.features.level.level_view_model import (
    LevelChoice,
    LevelViewModel,
)
from flash_card.presentation.shared.window import configure_window


class LevelView:
    """The level screen: a title and a button for each level."""

    def __init__(
        self,
        root: tk.Tk,
        view_model: LevelViewModel,
        on_choose: Callable[[Level], None],
    ) -> None:
        """Build the screen on a root.

        @param root The Tk root window.
        @param view_model The data to show.
        @param on_choose Called with the level the user picked.
        """
        ## @brief Called with the level the user picked.
        self._on_choose = on_choose
        configure_window(root)
        ## @brief Frame that holds the whole screen.
        self.frame = tk.Frame(
            root, bg=BACKGROUND_COLOR, width=CARD_WIDTH, height=LEVEL_SCREEN_HEIGHT
        )
        self.frame.grid(row=0, column=0)
        self.frame.grid_propagate(False)
        self.frame.grid_columnconfigure(0, weight=1)
        for row in range(len(view_model.choices) + 1):
            self.frame.grid_rowconfigure(row, weight=1)
        ## @brief The title text.
        self.title_label = tk.Label(
            self.frame,
            text=view_model.title,
            font=LEVEL_TITLE_FONT,
            bg=BACKGROUND_COLOR,
        )
        self.title_label.grid(row=0, column=0)
        ## @brief One button per choice, in display order.
        self.buttons = tuple(
            self._build_button(row, choice)
            for row, choice in enumerate(view_model.choices, start=1)
        )

    def choose(self, level: Level) -> None:
        """Forward the chosen level.

        @param level The level the user picked.
        @return Nothing.
        """
        self._on_choose(level)

    def destroy(self) -> None:
        """Remove the screen from the window.

        @return Nothing.
        """
        self.frame.destroy()

    def _build_button(self, row: int, choice: LevelChoice) -> tk.Button:
        """Create the button of one choice.

        @param row Grid row of the button.
        @param choice The choice the button stands for.
        @return The button, placed in the frame.
        """
        button = tk.Button(
            self.frame,
            text=choice.label,
            font=LEVEL_BUTTON_FONT,
            width=LEVEL_BUTTON_WIDTH,
            bg=LEVEL_BUTTON_COLOR,
            command=lambda: self.choose(choice.level),
        )
        button.grid(row=row, column=0)
        return button
