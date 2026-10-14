"""Integration tests of saving and resuming progress over real CSV files."""

from collections.abc import Callable, Sequence
from pathlib import Path

from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.application.use_cases.study_session import StudySession
from flash_card.domain.entities.card import Card
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.speech.null_speech import NullSpeech

WORDS = "fr;en\nchaque;each\nparlé;speak\narrivé;come\n"

Choose = Callable[[Sequence[Card]], Card]


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def _choose_front(front: str) -> Choose:
    def choose(cards: Sequence[Card]) -> Card:
        return next(card for card in cards if card.front == front)

    return choose


def _open(folder: Path, choose: Choose = _first) -> StudySession:
    return open_study_session(
        CsvVocabularyRepository(folder / "words.csv"),
        CsvProgressRepository(folder / "words_to_learn.csv"),
        NullSpeech(),
        choose,
    )


def _setup(folder: Path) -> Path:
    (folder / "words.csv").write_text(WORDS, encoding="utf-8")
    return folder / "words_to_learn.csv"


def _text(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig")


def test_mark_known_writes_remaining_cards_in_order(tmp_path: Path) -> None:
    progress = _setup(tmp_path)
    session = _open(tmp_path, _choose_front("parlé"))
    session.next_card()
    session.mark_known()
    assert _text(progress) == "fr;en\nchaque;each\narrivé;come\n"


def test_restart_draws_only_from_progress_file(tmp_path: Path) -> None:
    _setup(tmp_path)
    first = _open(tmp_path, _choose_front("parlé"))
    first.next_card()
    first.mark_known()

    second = _open(tmp_path)
    fronts: set[str] = set()
    for _ in range(6):
        card = second.next_card()
        assert card is not None
        fronts.add(card.front_text)

    assert second.remaining == 2
    assert fronts == {"chaque", "arrivé"}


def test_progress_file_is_readable_as_vocabulary(tmp_path: Path) -> None:
    progress = _setup(tmp_path)
    session = _open(tmp_path, _choose_front("chaque"))
    session.next_card()
    session.mark_known()
    vocabulary = CsvVocabularyRepository(progress).load()
    assert vocabulary.cards == (Card("parlé", "speak"), Card("arrivé", "come"))


def test_header_only_progress_file_gives_finished_session(tmp_path: Path) -> None:
    progress = _setup(tmp_path)
    progress.write_text("fr;en\n", encoding="utf-8")
    session = _open(tmp_path)
    assert session.remaining == 0
    assert session.next_card() is None


def test_unknown_card_never_creates_progress_file(tmp_path: Path) -> None:
    progress = _setup(tmp_path)
    session = _open(tmp_path)
    session.next_card()
    session.next_card()
    assert not progress.exists()
