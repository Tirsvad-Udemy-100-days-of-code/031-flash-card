"""One study session.

@file study_session.py
@brief The StudySession use case: draws the cards the user studies.
"""

from collections.abc import Callable, Sequence

from flash_card.application.dto.card_dto import CardDto
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck


class StudySession:
    """Draws cards from a deck, one after another."""

    def __init__(self, deck: Deck, choose: Callable[[Sequence[Card]], Card]) -> None:
        """Create a session.

        @param deck The cards still to learn.
        @param choose Picks one card from a non-empty sequence.
        """
        ## @brief The cards still to learn.
        self._deck = deck
        ## @brief Picks one card from a non-empty sequence.
        self._choose = choose
        ## @brief The card shown now, or None.
        self._current: Card | None = None

    @property
    def current_card(self) -> CardDto | None:
        """Return the card shown now.

        @return The card, or None before the first draw or when none is left.
        """
        return self._to_dto(self._current)

    @property
    def remaining(self) -> int:
        """Return the number of cards still to learn.

        @return The card count.
        """
        return len(self._deck)

    def next_card(self) -> CardDto | None:
        """Draw the next card, different from the current one when possible.

        @return The new card, or None when the deck is empty.
        """
        if self._deck.is_empty:
            self._current = None
            return None
        self._current = self._deck.draw(self._choose, exclude=self._current)
        return self._to_dto(self._current)

    def _to_dto(self, card: Card | None) -> CardDto | None:
        """Map a card to its DTO.

        @param card The card, or None.
        @return The DTO, or None when there is no card.
        """
        if card is None:
            return None
        pair = self._deck.language_pair
        return CardDto(card.front, card.back, pair.front_code, pair.back_code)
