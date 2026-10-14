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


class _RecordingProgress:
    def __init__(self) -> None:
        self.saved: list[tuple[Card, ...]] = []

    def load(self) -> Deck | None:
        return None

    def save(self, deck: Deck) -> None:
        self.saved.append(deck.cards)


class _RecordingSpeech:
    def __init__(self) -> None:
        self.spoken: list[tuple[str, str]] = []

    def speak(self, text: str, language_code: str) -> None:
        self.spoken.append((text, language_code))


def _session(
    *cards: Card,
    progress: _RecordingProgress | None = None,
    speech: _RecordingSpeech | None = None,
) -> StudySession:
    store = _RecordingProgress() if progress is None else progress
    voice = _RecordingSpeech() if speech is None else speech
    return StudySession(Deck(PAIR, cards), _first, store, voice)


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


def test_mark_known_removes_current_card_and_saves_remaining_once() -> None:
    progress = _RecordingProgress()
    session = _session(A, B, progress=progress)
    session.next_card()
    session.mark_known()
    assert session.remaining == 1
    assert session.current_card is None
    assert progress.saved == [(B,)]


def test_mark_known_saves_nothing_when_no_current_card() -> None:
    progress = _RecordingProgress()
    session = _session(A, progress=progress)
    session.mark_known()
    assert session.remaining == 1
    assert progress.saved == []


def test_mark_known_on_last_card_leaves_session_finished() -> None:
    progress = _RecordingProgress()
    session = _session(A, progress=progress)
    session.next_card()
    session.mark_known()
    assert progress.saved == [()]
    assert session.next_card() is None


def test_next_card_never_saves() -> None:
    progress = _RecordingProgress()
    session = _session(A, B, progress=progress)
    session.next_card()
    session.next_card()
    assert progress.saved == []


def test_next_card_speaks_front_text_once_in_front_language() -> None:
    speech = _RecordingSpeech()
    session = _session(A, B, speech=speech)
    session.next_card()
    assert speech.spoken == [("aku", "ms")]


def test_next_card_does_not_speak_when_deck_is_empty() -> None:
    speech = _RecordingSpeech()
    session = _session(speech=speech)
    session.next_card()
    assert speech.spoken == []


def test_next_card_speaks_again_on_every_draw() -> None:
    speech = _RecordingSpeech()
    session = _session(A, B, speech=speech)
    session.next_card()
    session.next_card()
    assert speech.spoken == [("aku", "ms"), ("kau", "ms")]


def test_mark_known_does_not_speak_but_following_draw_does() -> None:
    speech = _RecordingSpeech()
    session = _session(A, B, speech=speech)
    session.next_card()
    session.mark_known()
    assert speech.spoken == [("aku", "ms")]
    session.next_card()
    assert speech.spoken == [("aku", "ms"), ("kau", "ms")]
