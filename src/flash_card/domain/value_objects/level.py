"""The level of a study session.

@file level.py
@brief The Level value object: how many of the first words a session uses.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from flash_card.domain.entities.card import Card


@dataclass(frozen=True, slots=True)
class Level:
    """A limit on the words of the list, counted from the most frequent."""

    ## @brief Number of first words used, or None for all words.
    limit: int | None

    def __post_init__(self) -> None:
        """Check the limit.

        @return Nothing.
        @throws ValueError When the limit is set and not above zero.
        """
        if self.limit is not None and self.limit <= 0:
            raise ValueError(f"level limit must be above zero, got {self.limit}")

    def first(self, cards: Sequence[Card]) -> tuple[Card, ...]:
        """Select the cards of this level.

        @param cards The word list in order from the most frequent word.
        @return The first limit cards, or all cards when there is no limit or
            the list is shorter.
        """
        if self.limit is None:
            return tuple(cards)
        return tuple(cards[: self.limit])
