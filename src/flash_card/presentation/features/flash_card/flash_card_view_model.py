"""View model of the flash card screen.

@file flash_card_view_model.py
@brief Exposes the texts shown on the card; free of any Tkinter import.
"""

import enum
from collections.abc import Mapping

from flash_card.application.dto.card_dto import CardDto
from flash_card.application.use_cases.study_session import StudySession
from flash_card.constants import FINISHED_MESSAGE, LANGUAGE_NAMES


class Side(enum.Enum):
    """The side of a card that is shown."""

    ## @brief The front: the word to learn.
    FRONT = enum.auto()
    ## @brief The back: the translation.
    BACK = enum.auto()


class FlashCardViewModel:
    """Data the flash card view shows."""

    def __init__(
        self,
        session: StudySession,
        language_names: Mapping[str, str] = LANGUAGE_NAMES,
    ) -> None:
        """Create the view model and draw the first card.

        @param session The study session that supplies the cards.
        @param language_names Display names by language code.
        """
        ## @brief The study session that supplies the cards.
        self._session = session
        ## @brief Display names by language code.
        self._language_names = language_names
        ## @brief The card shown now, or None when none is left.
        self._card: CardDto | None = session.next_card()
        ## @brief The side of the card shown.
        self._side = Side.FRONT

    @property
    def is_finished(self) -> bool:
        """Tell whether no card is left to show.

        @return True when there is no card.
        """
        return self._card is None

    @property
    def side(self) -> Side:
        """Return the side of the card shown.

        @return FRONT or BACK; FRONT when no card is left.
        """
        return self._side

    @property
    def language_name(self) -> str:
        """Return the language name shown on the card.

        @return The display name of the language of the side shown, upper case
            code when unknown, or an empty string when no card is left.
        """
        if self._card is None:
            return ""
        if self._side is Side.BACK:
            code = self._card.back_language
        else:
            code = self._card.front_language
        return self._language_names.get(code, code.upper())

    @property
    def text(self) -> str:
        """Return the word shown on the card.

        @return The text of the side shown, or the finished message when no
            card is left.
        """
        if self._card is None:
            return FINISHED_MESSAGE
        if self._side is Side.BACK:
            return self._card.back_text
        return self._card.front_text

    def next_card(self) -> None:
        """Draw the next card and show its front; does nothing when finished.

        @return Nothing.
        """
        if self._card is None:
            return
        self._card = self._session.next_card()
        self._side = Side.FRONT

    def is_known(self) -> None:
        """Mark the card as known, save the progress and show the next card.

        Does nothing when finished.

        @return Nothing.
        """
        if self._card is None:
            return
        self._session.mark_known()
        self._card = self._session.next_card()
        self._side = Side.FRONT

    def flip_card(self) -> None:
        """Show the back of the card; does nothing when finished or flipped.

        @return Nothing.
        """
        if self._card is not None:
            self._side = Side.BACK
