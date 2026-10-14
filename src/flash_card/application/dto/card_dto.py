"""Card data for the presentation layer.

@file card_dto.py
@brief The CardDto: a card as plain text.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CardDto:
    """A card as plain data."""

    ## @brief Word on the card front.
    front_text: str
    ## @brief Translation on the card back.
    back_text: str
    ## @brief Language code of the front.
    front_language: str
    ## @brief Language code of the back.
    back_language: str
