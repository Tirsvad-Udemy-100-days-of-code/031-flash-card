"""The delivered word list.

@file vocabulary.py
@brief The Vocabulary entity: all cards of a language pair.
"""

from dataclasses import dataclass

from flash_card.domain.entities.card import Card
from flash_card.domain.value_objects.language_pair import LanguagePair


@dataclass(frozen=True, slots=True)
class Vocabulary:
    """All cards of a language pair as delivered."""

    ## @brief The languages of the cards.
    language_pair: LanguagePair
    ## @brief The cards in file order.
    cards: tuple[Card, ...]
