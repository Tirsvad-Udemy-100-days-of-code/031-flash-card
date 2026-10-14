"""One study session.

@file study_session.py
@brief The StudySession use case: draws the cards the user studies.
"""

from collections.abc import Callable, Sequence

from flash_card.application.dto.card_dto import CardDto
from flash_card.application.ports.speech_port import SpeechPort
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.repositories.progress_repository import ProgressRepository


class StudySession:
    """Draws cards from a deck, one after another."""

    def __init__(
        self,
        deck: Deck,
        choose: Callable[[Sequence[Card]], Card],
        progress: ProgressRepository,
        speech: SpeechPort,
        level_cards: Sequence[Card] | None = None,
    ) -> None:
        """Create a session.

        @param deck The cards still to learn.
        @param choose Picks one card from a non-empty sequence.
        @param progress Store of the words still to learn.
        @param speech Speaks the front text of each drawn card.
        @param level_cards The cards of the chosen level, or None for no limit.
        """
        ## @brief The cards of the chosen level, or None for no limit.
        self._level_cards = None if level_cards is None else tuple(level_cards)
        ## @brief Speaks the front text of each drawn card.
        self._speech = speech
        ## @brief Store of the words still to learn.
        self._progress = progress
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
        """Return the number of cards still to learn, of every level.

        @return The card count.
        """
        return len(self._deck)

    @property
    def remaining_in_level(self) -> int:
        """Return the number of cards still to learn in the chosen level.

        @return The card count.
        """
        return len(self._candidates())

    def next_card(self) -> CardDto | None:
        """Draw the next card, different from the current one when possible.

        @return The new card, or None when no card of the level is left.
        """
        candidates = self._candidates()
        if not candidates:
            self._current = None
            return None
        card = self._deck.draw(self._choose, self._current, candidates)
        self._current = card
        self._speech.speak(card.front, self._deck.language_pair.front_code)
        return self._to_dto(card)

    def mark_known(self) -> None:
        """Remove the current card from the whole deck and save the whole deck.

        Does nothing and saves nothing when no card is shown.

        @return Nothing.
        """
        if self._current is None:
            return
        self._deck.remove(self._current)
        self._progress.save(self._deck)
        self._current = None

    def _candidates(self) -> tuple[Card, ...]:
        """Return the cards that may be drawn.

        @return The deck cards of the level, or all deck cards without a level.
        """
        if self._level_cards is None:
            return self._deck.cards
        return self._deck.within(self._level_cards)

    def _to_dto(self, card: Card | None) -> CardDto | None:
        """Map a card to its DTO.

        @param card The card, or None.
        @return The DTO, or None when there is no card.
        """
        if card is None:
            return None
        pair = self._deck.language_pair
        return CardDto(card.front, card.back, pair.front_code, pair.back_code)
