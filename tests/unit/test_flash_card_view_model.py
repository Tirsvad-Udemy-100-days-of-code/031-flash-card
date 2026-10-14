"""Tests of the flash card view model.

@file test_flash_card_view_model.py
@brief Checks the placeholder texts of FlashCardViewModel.
"""

from flash_card.constants import PLACEHOLDER_LANGUAGE_NAME, PLACEHOLDER_WORD
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)


def test_language_name_returns_placeholder() -> None:
    assert FlashCardViewModel().language_name == PLACEHOLDER_LANGUAGE_NAME


def test_text_returns_placeholder_word() -> None:
    assert FlashCardViewModel().text == PLACEHOLDER_WORD
