"""View model of the flash card screen.

@file flash_card_view_model.py
@brief Exposes the texts shown on the card; free of any Tkinter import.
"""

from collections.abc import Mapping

from flash_card.application.dto.card_dto import CardDto
from flash_card.application.use_cases.study_session import StudySession
from flash_card.constants import FINISHED_MESSAGE, LANGUAGE_NAMES


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

    @property
    def is_finished(self) -> bool:
        """Tell whether no card is left to show.

        @return True when there is no card.
        """
        return self._card is None

    @property
    def language_name(self) -> str:
        """Return the language name shown on the card.

        @return The display name of the front language, upper case code when
            unknown, or an empty string when no card is left.
        """
        if self._card is None:
            return ""
        code = self._card.front_language
        return self._language_names.get(code, code.upper())

    @property
    def text(self) -> str:
        """Return the word shown on the card.

        @return The front text, or the finished message when no card is left.
        """
        if self._card is None:
            return FINISHED_MESSAGE
        return self._card.front_text

    def next_card(self) -> None:
        """Draw the next card.

        @return Nothing.
        """
        self._card = self._session.next_card()
