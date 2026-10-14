"""Tests of the Card, LanguagePair and Vocabulary value types."""

import dataclasses

import pytest

from flash_card.domain.entities.card import Card
from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.value_objects.language_pair import LanguagePair


def test_card_equals_card_with_same_texts() -> None:
    assert Card("aku", "mig") == Card("aku", "mig")


def test_card_is_frozen() -> None:
    card = Card("aku", "mig")
    with pytest.raises(dataclasses.FrozenInstanceError):
        card.front = "kau"  # type: ignore[misc]


def test_language_pair_holds_codes() -> None:
    pair = LanguagePair("ms", "da")
    assert (pair.front_code, pair.back_code) == ("ms", "da")


def test_language_pair_is_frozen() -> None:
    pair = LanguagePair("ms", "da")
    with pytest.raises(dataclasses.FrozenInstanceError):
        pair.front_code = "en"  # type: ignore[misc]


def test_vocabulary_holds_pair_and_cards() -> None:
    pair = LanguagePair("ms", "da")
    cards = (Card("aku", "mig"),)
    vocabulary = Vocabulary(pair, cards)
    assert vocabulary.language_pair == pair
    assert vocabulary.cards == cards
