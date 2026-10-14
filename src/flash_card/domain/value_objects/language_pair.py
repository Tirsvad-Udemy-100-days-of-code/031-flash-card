"""The two languages of a word list.

@file language_pair.py
@brief The LanguagePair value object.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LanguagePair:
    """The language codes of the front and the back of the cards."""

    ## @brief Language code of the card front.
    front_code: str
    ## @brief Language code of the card back.
    back_code: str
