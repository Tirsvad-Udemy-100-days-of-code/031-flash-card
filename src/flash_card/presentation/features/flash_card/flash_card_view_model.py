"""View model of the flash card screen.

@file flash_card_view_model.py
@brief Exposes the texts shown on the card; free of any Tkinter import.
"""

from flash_card.constants import PLACEHOLDER_LANGUAGE_NAME, PLACEHOLDER_WORD


class FlashCardViewModel:
    """Data the flash card view shows."""

    @property
    def language_name(self) -> str:
        """Return the language name shown on the card.

        @return The display name of the language.
        """
        return PLACEHOLDER_LANGUAGE_NAME

    @property
    def text(self) -> str:
        """Return the word shown on the card.

        @return The word text.
        """
        return PLACEHOLDER_WORD
