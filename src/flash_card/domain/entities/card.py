"""A flash card.

@file card.py
@brief The Card entity: a word and its translation.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Card:
    """A word and its translation."""

    ## @brief The word in the front language.
    front: str
    ## @brief The translation in the back language.
    back: str
