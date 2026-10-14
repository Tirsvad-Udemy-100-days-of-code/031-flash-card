"""Tests of the StudySession use case."""

from collections.abc import Sequence

from flash_card.application.dto.card_dto import CardDto
from flash_card.application.use_cases.study_session import StudySession
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.value_objects.language_pair import LanguagePair

PAIR = LanguagePair("ms", "da")
A = Card("aku", "mig")
B = Card("kau", "du")


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def _session(*cards: Card) -> StudySession:
    return StudySession(Deck(PAIR, cards), _first)


def test_current_card_is_none_before_first_draw() -> None:
    assert _session(A).current_card is None


def test_next_card_returns_chosen_card_as_dto() -> None:
    assert _session(A, B).next_card() == CardDto("aku", "mig", "ms", "da")


def test_next_card_returns_different_card_when_two_or_more() -> None:
    session = _session(A, B)
    first = session.next_card()
    second = session.next_card()
    assert first != second
    assert second == CardDto("kau", "du", "ms", "da")


def test_next_card_returns_same_card_when_one() -> None:
    session = _session(A)
    assert session.next_card() == session.next_card()


def test_next_card_returns_none_when_deck_is_empty() -> None:
    session = _session()
    assert session.next_card() is None
    assert session.current_card is None


def test_current_card_follows_last_draw() -> None:
    session = _session(A, B)
    shown = session.next_card()
    assert session.current_card == shown


def test_remaining_counts_cards_in_deck() -> None:
    session = _session(A, B)
    session.next_card()
    assert session.remaining == 2
