"""View of the flash card screen.

@file flash_card_view.py
@brief Builds the window of the wireframe: card canvas and two buttons.
"""

import tkinter as tk

from flash_card.constants import (
    ASSETS_DIR,
    BACKGROUND_COLOR,
    CARD_CENTER_X,
    CARD_FRONT_IMAGE_NAME,
    CARD_HEIGHT,
    CARD_WIDTH,
    FRONT_TEXT_COLOR,
    LANGUAGE_FONT,
    LANGUAGE_TEXT_Y,
    RIGHT_IMAGE_NAME,
    WINDOW_PADDING,
    WINDOW_TITLE,
    WORD_FONT,
    WORD_TEXT_Y,
    WRONG_IMAGE_NAME,
)
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)


class FlashCardView:
    """The flash card window: a card and the wrong and right buttons."""

    def __init__(self, root: tk.Tk, view_model: FlashCardViewModel) -> None:
        """Build the window on a root.

        @param root The Tk root window.
        @param view_model The data to show.
        """
        ## @brief The Tk root window.
        self._root = root
        ## @brief The data source of the texts.
        self._view_model = view_model
        root.title(WINDOW_TITLE)
        root.config(padx=WINDOW_PADDING, pady=WINDOW_PADDING, bg=BACKGROUND_COLOR)

        # Kept as attributes: Tkinter drops an image nothing refers to.
        ## @brief Card front image, kept so Tk does not drop it.
        self._card_front_image = tk.PhotoImage(file=ASSETS_DIR / CARD_FRONT_IMAGE_NAME)
        ## @brief Wrong button image, kept so Tk does not drop it.
        self._wrong_image = tk.PhotoImage(file=ASSETS_DIR / WRONG_IMAGE_NAME)
        ## @brief Right button image, kept so Tk does not drop it.
        self._right_image = tk.PhotoImage(file=ASSETS_DIR / RIGHT_IMAGE_NAME)

        ## @brief Canvas that draws the card.
        self.canvas = tk.Canvas(
            root,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        ## @brief Canvas item id of the card image.
        self.image_id = self.canvas.create_image(
            CARD_CENTER_X, CARD_HEIGHT / 2, image=self._card_front_image
        )
        ## @brief Canvas item id of the language name text.
        self.language_text_id = self.canvas.create_text(
            CARD_CENTER_X,
            LANGUAGE_TEXT_Y,
            text=view_model.language_name,
            font=LANGUAGE_FONT,
            fill=FRONT_TEXT_COLOR,
        )
        ## @brief Canvas item id of the word text.
        self.word_text_id = self.canvas.create_text(
            CARD_CENTER_X,
            WORD_TEXT_Y,
            text=view_model.text,
            font=WORD_FONT,
            fill=FRONT_TEXT_COLOR,
        )
        self.canvas.grid(row=0, column=0, columnspan=2)

        ## @brief Button for a word the user does not know.
        self.wrong_button = tk.Button(
            root,
            image=self._wrong_image,
            highlightthickness=0,
            bd=0,
            command=self.next_card,
        )
        self.wrong_button.grid(row=1, column=0)
        ## @brief Button for a word the user knows.
        self.right_button = tk.Button(
            root,
            image=self._right_image,
            highlightthickness=0,
            bd=0,
            command=self.next_card,
        )
        self.right_button.grid(row=1, column=1)

    def next_card(self) -> None:
        """Show the next card.

        @return Nothing.
        """
        self._view_model.next_card()
        self.canvas.itemconfig(
            self.language_text_id, text=self._view_model.language_name
        )
        self.canvas.itemconfig(self.word_text_id, text=self._view_model.text)
