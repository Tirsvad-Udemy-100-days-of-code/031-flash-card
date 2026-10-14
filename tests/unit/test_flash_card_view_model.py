"""Tests of the flash card view model over a real session and in-memory deck."""

from collections.abc import Sequence

from flash_card.application.use_cases.study_session import StudySession
from flash_card.constants import FINISHED_MESSAGE
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)

A = Card("aku", "mig")
B = Card("kau", "du")


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def _session(code: str, *cards: Card) -> StudySession:
    return StudySession(Deck(LanguagePair(code, "da"), cards), _first)


def test_view_model_draws_first_card_on_construction() -> None:
    view_model = FlashCardViewModel(_session("ms", A, B))
    assert view_model.text == "aku"
    assert view_model.language_name == "Malay"
    assert not view_model.is_finished


def test_next_card_shows_next_card() -> None:
    view_model = FlashCardViewModel(_session("ms", A, B))
    view_model.next_card()
    assert view_model.text == "kau"


def test_language_name_shows_unknown_code_in_upper_case() -> None:
    view_model = FlashCardViewModel(_session("xx", A))
    assert view_model.language_name == "XX"


def test_language_name_uses_given_names() -> None:
    view_model = FlashCardViewModel(_session("ms", A), {"ms": "Melayu"})
    assert view_model.language_name == "Melayu"


def test_view_model_shows_finished_message_when_no_card_is_left() -> None:
    view_model = FlashCardViewModel(_session("ms"))
    assert view_model.is_finished
    assert view_model.language_name == ""
    assert view_model.text == FINISHED_MESSAGE
