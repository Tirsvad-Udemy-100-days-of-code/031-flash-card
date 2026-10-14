"""Tests of the Deck entity."""

from collections.abc import Sequence

import pytest

from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.errors.vocabulary_errors import EmptyDeckError
from flash_card.domain.value_objects.language_pair import LanguagePair

PAIR = LanguagePair("ms", "da")
A = Card("aku", "mig")
B = Card("kau", "du")


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def test_from_vocabulary_holds_all_cards() -> None:
    deck = Deck.from_vocabulary(Vocabulary(PAIR, (A, B)))
    assert deck.cards == (A, B)
    assert deck.language_pair == PAIR
    assert len(deck) == 2


def test_cards_returns_copy_when_deck_changes_later() -> None:
    deck = Deck(PAIR, [A])
    snapshot = deck.cards
    deck.remove(A)
    assert snapshot == (A,)
    assert deck.is_empty


def test_draw_returns_chosen_card() -> None:
    assert Deck(PAIR, [A, B]).draw(_first) == A


def test_draw_avoids_excluded_card_when_another_exists() -> None:
    assert Deck(PAIR, [A, B]).draw(_first, exclude=A) == B


def test_draw_returns_excluded_card_when_it_is_the_only_one() -> None:
    assert Deck(PAIR, [A]).draw(_first, exclude=A) == A


def test_draw_keeps_card_in_deck() -> None:
    deck = Deck(PAIR, [A, B])
    deck.draw(_first)
    assert len(deck) == 2


def test_draw_raises_when_deck_is_empty() -> None:
    with pytest.raises(EmptyDeckError):
        Deck(PAIR, []).draw(_first)


def test_remove_deletes_first_equal_card() -> None:
    deck = Deck(PAIR, [A, B, A])
    deck.remove(A)
    assert deck.cards == (B, A)


def test_remove_raises_when_card_is_absent() -> None:
    with pytest.raises(ValueError):
        Deck(PAIR, [A]).remove(B)


def test_is_empty_reflects_cards() -> None:
    assert Deck(PAIR, []).is_empty
    assert not Deck(PAIR, [A]).is_empty
