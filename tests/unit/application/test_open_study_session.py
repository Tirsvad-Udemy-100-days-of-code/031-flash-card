"""Tests of the open_study_session use case."""

from collections.abc import Sequence

import pytest

from flash_card.application.dto.card_dto import CardDto
from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.errors.vocabulary_errors import VocabularyNotFoundError
from flash_card.domain.value_objects.language_pair import LanguagePair


class _FakeRepository:
    def __init__(self, vocabulary: Vocabulary) -> None:
        self._vocabulary = vocabulary

    def load(self) -> Vocabulary:
        return self._vocabulary


class _MissingRepository:
    def load(self) -> Vocabulary:
        raise VocabularyNotFoundError("missing")


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def test_open_study_session_builds_session_over_all_cards() -> None:
    cards = (Card("aku", "mig"), Card("kau", "du"))
    repository = _FakeRepository(Vocabulary(LanguagePair("ms", "da"), cards))

    session = open_study_session(repository, _first)

    assert session.remaining == 2
    assert session.next_card() == CardDto("aku", "mig", "ms", "da")


def test_open_study_session_propagates_repository_error() -> None:
    with pytest.raises(VocabularyNotFoundError):
        open_study_session(_MissingRepository(), _first)
