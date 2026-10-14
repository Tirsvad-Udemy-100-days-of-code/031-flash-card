"""The cards still to learn.

@file deck.py
@brief The Deck entity: holds cards, draws one and removes one.
"""

from collections import Counter
from collections.abc import Callable, Iterable, Sequence

from flash_card.domain.entities.card import Card
from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.errors.vocabulary_errors import EmptyDeckError
from flash_card.domain.value_objects.language_pair import LanguagePair


class Deck:
    """The cards still to learn, of one language pair."""

    def __init__(self, language_pair: LanguagePair, cards: Iterable[Card]) -> None:
        """Create a deck.

        @param language_pair The languages of the cards.
        @param cards The cards of the deck.
        """
        ## @brief The languages of the cards.
        self._language_pair = language_pair
        ## @brief The cards still in the deck.
        self._cards = list(cards)

    @classmethod
    def from_vocabulary(cls, vocabulary: Vocabulary) -> "Deck":
        """Create a deck holding every card of a vocabulary.

        @param vocabulary The delivered word list.
        @return A new deck.
        """
        return cls(vocabulary.language_pair, vocabulary.cards)

    @property
    def language_pair(self) -> LanguagePair:
        """Return the languages of the cards.

        @return The language pair.
        """
        return self._language_pair

    @property
    def cards(self) -> tuple[Card, ...]:
        """Return a copy of the cards.

        @return The cards in deck order.
        """
        return tuple(self._cards)

    @property
    def is_empty(self) -> bool:
        """Tell whether the deck has no card.

        @return True when no card is left.
        """
        return not self._cards

    def __len__(self) -> int:
        """Return the number of cards.

        @return The card count.
        """
        return len(self._cards)

    def within(self, cards: Sequence[Card]) -> tuple[Card, ...]:
        """Select the cards of the deck that also appear in the given cards.

        A card counts as often as it appears in both.

        @param cards The cards to match against, for example a level.
        @return The matching cards in deck order.
        """
        allowed = Counter(cards)
        selected: list[Card] = []
        for card in self._cards:
            if allowed[card] > 0:
                allowed[card] -= 1
                selected.append(card)
        return tuple(selected)

    def draw(
        self,
        choose: Callable[[Sequence[Card]], Card],
        exclude: Card | None = None,
        among: Sequence[Card] | None = None,
    ) -> Card:
        """Pick a card without removing it.

        The pick avoids the excluded card when another candidate exists.

        @param choose Picks one card from a non-empty sequence.
        @param exclude A card to avoid, usually the one shown now.
        @param among The candidates, or None for every card of the deck.
        @return The picked card.
        @throws EmptyDeckError When there is no candidate.
        """
        candidates = self._cards if among is None else list(among)
        if not candidates:
            raise EmptyDeckError("cannot draw from an empty deck")
        others = [card for card in candidates if card != exclude]
        return choose(others or candidates)

    def remove(self, card: Card) -> None:
        """Remove the first card equal to the given one.

        @param card The card to remove.
        @return Nothing.
        @throws ValueError When the deck holds no such card.
        """
        self._cards.remove(card)
