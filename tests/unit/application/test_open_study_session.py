"""Tests of the open_study_session use case."""

from collections.abc import Sequence

import pytest

from flash_card.application.dto.card_dto import CardDto
from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.errors.vocabulary_errors import VocabularyNotFoundError
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.domain.value_objects.level import Level


class _FakeRepository:
    def __init__(self, vocabulary: Vocabulary) -> None:
        self._vocabulary = vocabulary

    def load(self) -> Vocabulary:
        return self._vocabulary


class _RecordingProgress:
    def __init__(self, stored: Deck | None = None) -> None:
        self.stored = stored
        self.saved: list[tuple[Card, ...]] = []

    def load(self) -> Deck | None:
        return self.stored

    def save(self, deck: Deck) -> None:
        self.saved.append(deck.cards)


class _SilentSpeech:
    def speak(self, text: str, language_code: str) -> None:
        return None


class _MissingRepository:
    def load(self) -> Vocabulary:
        raise VocabularyNotFoundError("missing")


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def test_open_study_session_builds_session_over_all_cards() -> None:
    cards = (Card("aku", "mig"), Card("kau", "du"))
    repository = _FakeRepository(Vocabulary(LanguagePair("ms", "da"), cards))

    session = open_study_session(
        repository, _RecordingProgress(), _SilentSpeech(), _first, Level(None)
    )

    assert session.remaining == 2
    assert session.next_card() == CardDto("aku", "mig", "ms", "da")


def test_open_study_session_propagates_repository_error() -> None:
    with pytest.raises(VocabularyNotFoundError):
        open_study_session(
            _MissingRepository(),
            _RecordingProgress(),
            _SilentSpeech(),
            _first,
            Level(None),
        )


def test_open_study_session_prefers_saved_progress() -> None:
    pair = LanguagePair("ms", "da")
    vocabulary = Vocabulary(pair, (Card("aku", "mig"), Card("kau", "du")))
    progress = _RecordingProgress(Deck(pair, [Card("kau", "du")]))

    session = open_study_session(
        _FakeRepository(vocabulary), progress, _SilentSpeech(), _first, Level(None)
    )

    assert session.remaining == 1
    assert session.next_card() == CardDto("kau", "du", "ms", "da")


PAIR = LanguagePair("ms", "da")
THREE = (Card("aku", "mig"), Card("kau", "du"), Card("ini", "denne"))


def _last(cards: Sequence[Card]) -> Card:
    return cards[-1]


def test_open_study_session_propagates_error_when_list_is_missing() -> None:
    progress = _RecordingProgress(Deck(PAIR, []))

    with pytest.raises(VocabularyNotFoundError):
        open_study_session(
            _MissingRepository(), progress, _SilentSpeech(), _first, Level(None)
        )


def test_open_study_session_limits_draws_to_first_cards_of_level() -> None:
    session = open_study_session(
        _FakeRepository(Vocabulary(PAIR, THREE)),
        _RecordingProgress(),
        _SilentSpeech(),
        _last,
        Level(2),
    )

    assert session.remaining == 3
    assert session.remaining_in_level == 2
    assert session.next_card() == CardDto("kau", "du", "ms", "da")


def test_open_study_session_uses_vocabulary_order_with_saved_progress() -> None:
    progress = _RecordingProgress(Deck(PAIR, [THREE[2], THREE[1]]))
    session = open_study_session(
        _FakeRepository(Vocabulary(PAIR, THREE)),
        progress,
        _SilentSpeech(),
        _first,
        Level(2),
    )

    assert session.remaining == 2
    assert session.remaining_in_level == 1
    assert session.next_card() == CardDto("kau", "du", "ms", "da")


def test_open_study_session_is_finished_when_level_has_nothing_left() -> None:
    progress = _RecordingProgress(Deck(PAIR, [THREE[1]]))
    session = open_study_session(
        _FakeRepository(Vocabulary(PAIR, THREE)),
        progress,
        _SilentSpeech(),
        _first,
        Level(1),
    )

    assert session.next_card() is None
    assert session.remaining == 1


def test_open_study_session_uses_all_cards_when_level_exceeds_list() -> None:
    session = open_study_session(
        _FakeRepository(Vocabulary(PAIR, THREE)),
        _RecordingProgress(),
        _SilentSpeech(),
        _first,
        Level(1000),
    )

    assert session.remaining_in_level == 3


def test_open_study_session_never_saves_on_start() -> None:
    vocabulary = Vocabulary(LanguagePair("ms", "da"), (Card("aku", "mig"),))
    progress = _RecordingProgress()

    session = open_study_session(
        _FakeRepository(vocabulary), progress, _SilentSpeech(), _first, Level(None)
    )
    session.next_card()

    assert progress.saved == []
