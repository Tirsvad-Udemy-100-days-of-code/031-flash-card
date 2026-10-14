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


def test_within_returns_deck_cards_found_in_given_cards_in_deck_order() -> None:
    c = Card("ini", "denne")
    deck = Deck(PAIR, [A, B, c])
    assert deck.within([c, A]) == (A, c)


def test_within_respects_multiplicity() -> None:
    deck = Deck(PAIR, [A, A, B])
    assert deck.within([A, B]) == (A, B)
    assert deck.within([A, A, A]) == (A, A)


def test_within_returns_empty_when_no_card_matches() -> None:
    assert Deck(PAIR, [A]).within([B]) == ()


def test_within_does_not_change_the_deck() -> None:
    deck = Deck(PAIR, [A, B])
    deck.within([A])
    assert deck.cards == (A, B)


def test_draw_chooses_among_given_candidates_only() -> None:
    deck = Deck(PAIR, [A, B])
    assert deck.draw(_first, among=[B]) == B


def test_draw_among_avoids_excluded_when_another_candidate_exists() -> None:
    c = Card("ini", "denne")
    deck = Deck(PAIR, [A, B, c])
    assert deck.draw(_first, exclude=B, among=[B, c]) == c


def test_draw_among_returns_excluded_when_it_is_the_only_candidate() -> None:
    deck = Deck(PAIR, [A, B])
    assert deck.draw(_first, exclude=B, among=[B]) == B


def test_draw_among_empty_raises_empty_deck_error() -> None:
    deck = Deck(PAIR, [A, B])
    with pytest.raises(EmptyDeckError):
        deck.draw(_first, among=[])
