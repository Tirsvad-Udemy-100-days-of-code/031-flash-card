"""View of the flash card screen.

@file flash_card_view.py
@brief Builds the window of the wireframe: card canvas and two buttons.
"""

import tkinter as tk

from flash_card.constants import (
    ASSETS_DIR,
    BACK_TEXT_COLOR,
    BACKGROUND_COLOR,
    CARD_BACK_IMAGE_NAME,
    CARD_CENTER_X,
    CARD_FRONT_IMAGE_NAME,
    CARD_HEIGHT,
    CARD_WIDTH,
    FLIP_DELAY_MS,
    FRONT_TEXT_COLOR,
    LANGUAGE_FONT,
    LANGUAGE_TEXT_Y,
    RIGHT_IMAGE_NAME,
    WORD_FONT,
    WORD_TEXT_Y,
    WRONG_IMAGE_NAME,
)
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
    Side,
)
from flash_card.presentation.shared.window import configure_window


def _load_image(root: tk.Tk, name: str) -> tk.PhotoImage:
    """Load an asset image.

    The bytes are read here and handed to Tk as data, so the image does not
    depend on Tcl opening the file: Tcl keeps the standard handles it saw at
    start, and a process that swaps them (pytest fd capture) makes the first
    Tcl file open fail with an empty error.

    @param root The Tk root window that owns the image.
    @param name The file name in the assets folder.
    @return The image; the caller must keep a reference.
    """
    return tk.PhotoImage(master=root, data=(ASSETS_DIR / name).read_bytes())


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
        configure_window(root)

        # Kept as attributes: Tkinter drops an image nothing refers to.
        ## @brief Card front image, kept so Tk does not drop it.
        self._card_front_image = _load_image(root, CARD_FRONT_IMAGE_NAME)
        ## @brief Card back image, kept so Tk does not drop it.
        self._card_back_image = _load_image(root, CARD_BACK_IMAGE_NAME)
        ## @brief Wrong button image, kept so Tk does not drop it.
        self._wrong_image = _load_image(root, WRONG_IMAGE_NAME)
        ## @brief Right button image, kept so Tk does not drop it.
        self._right_image = _load_image(root, RIGHT_IMAGE_NAME)

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
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            relief="flat",
            highlightthickness=0,
            bd=0,
            command=self.next_card,
        )
        self.wrong_button.grid(row=1, column=0)
        ## @brief Button for a word the user knows.
        self.right_button = tk.Button(
            root,
            image=self._right_image,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            relief="flat",
            highlightthickness=0,
            bd=0,
            command=self.is_known,
        )
        self.right_button.grid(row=1, column=1)

        ## @brief Id of the pending flip timer, or None when none is pending.
        self.flip_timer: str | None = None
        self._start_flip_timer()

    @property
    def card_front_image(self) -> tk.PhotoImage:
        """Return the card front image.

        @return The image shown while the front side is up.
        """
        return self._card_front_image

    @property
    def card_back_image(self) -> tk.PhotoImage:
        """Return the card back image.

        @return The image shown while the back side is up.
        """
        return self._card_back_image

    def close(self) -> None:
        """Cancel the flip timer and remove the widgets of the screen.

        @return Nothing.
        """
        self._cancel_flip_timer()
        for widget in (self.canvas, self.wrong_button, self.right_button):
            widget.destroy()

    def next_card(self) -> None:
        """Show the next card front and restart the flip timer.

        @return Nothing.
        """
        self._cancel_flip_timer()
        self._view_model.next_card()
        self._show_card()
        self._start_flip_timer()

    def is_known(self) -> None:
        """Mark the card as known, show the next card front, restart the timer.

        @return Nothing.
        """
        self._cancel_flip_timer()
        self._view_model.is_known()
        self._show_card()
        self._start_flip_timer()

    def flip_card(self) -> None:
        """Show the back of the current card.

        @return Nothing.
        """
        self._cancel_flip_timer()
        self._view_model.flip_card()
        self._show_card()

    def _cancel_flip_timer(self) -> None:
        """Cancel the pending flip timer, if any.

        @return Nothing.
        """
        if self.flip_timer is not None:
            self._root.after_cancel(self.flip_timer)
            self.flip_timer = None

    def _start_flip_timer(self) -> None:
        """Schedule the flip unless no card is left.

        @return Nothing.
        """
        if not self._view_model.is_finished:
            self.flip_timer = self._root.after(FLIP_DELAY_MS, self.flip_card)

    def _show_card(self) -> None:
        """Draw image and texts of the side the view model shows.

        @return Nothing.
        """
        if self._view_model.side is Side.BACK:
            image, color = self._card_back_image, BACK_TEXT_COLOR
        else:
            image, color = self._card_front_image, FRONT_TEXT_COLOR
        self.canvas.itemconfig(self.image_id, image=image)
        self.canvas.itemconfig(
            self.language_text_id, text=self._view_model.language_name, fill=color
        )
        self.canvas.itemconfig(
            self.word_text_id, text=self._view_model.text, fill=color
        )
