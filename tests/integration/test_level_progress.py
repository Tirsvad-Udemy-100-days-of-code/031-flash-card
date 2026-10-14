"""Integration tests of the levels over the real word list and a progress file."""

from collections.abc import Callable, Sequence
from pathlib import Path

from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.application.use_cases.study_session import StudySession
from flash_card.constants import (
    DEFAULT_DATA_DIR,
    PROGRESS_FILE_NAME,
    VOCABULARY_FILE_NAME,
)
from flash_card.domain.entities.card import Card
from flash_card.domain.value_objects.level import Level
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.speech.null_speech import NullSpeech

VOCABULARY = CsvVocabularyRepository(DEFAULT_DATA_DIR / VOCABULARY_FILE_NAME)
ALL_CARDS = VOCABULARY.load().cards
FIRST_HUNDRED = ALL_CARDS[:100]

Choose = Callable[[Sequence[Card]], Card]


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def _open(folder: Path, level: Level, choose: Choose = _first) -> StudySession:
    return open_study_session(
        VOCABULARY,
        CsvProgressRepository(folder / PROGRESS_FILE_NAME),
        NullSpeech(),
        choose,
        level,
    )


def _learn_to_the_end(session: StudySession) -> list[Card]:
    """Mark every drawn card known until the session is finished."""
    drawn: list[Card] = []
    while (card := session.next_card()) is not None:
        drawn.append(Card(card.front_text, card.back_text))
        session.mark_known()
    return drawn


def _saved(folder: Path) -> tuple[Card, ...]:
    loaded = CsvProgressRepository(folder / PROGRESS_FILE_NAME).load()
    assert loaded is not None
    return loaded.cards


def test_word_list_has_one_thousand_distinct_words() -> None:
    assert len(ALL_CARDS) == 1000
    assert len(set(ALL_CARDS)) == 1000


def test_level_100_draws_exactly_the_first_hundred_words(tmp_path: Path) -> None:
    drawn = _learn_to_the_end(_open(tmp_path, Level(100)))
    assert len(drawn) == 100
    assert len(set(drawn)) == 100
    assert set(drawn) == set(FIRST_HUNDRED)


def test_level_100_keeps_the_other_words_in_order_in_the_file(
    tmp_path: Path,
) -> None:
    _learn_to_the_end(_open(tmp_path, Level(100)))
    assert _saved(tmp_path) == ALL_CARDS[100:]
    assert len(_saved(tmp_path)) == 900


def test_level_all_after_level_100_draws_only_the_other_words(
    tmp_path: Path,
) -> None:
    _learn_to_the_end(_open(tmp_path, Level(100)))
    drawn = _learn_to_the_end(_open(tmp_path, Level(None)))
    assert len(drawn) == 900
    assert set(drawn) == set(ALL_CARDS[100:])
    assert not set(drawn) & set(FIRST_HUNDRED)


def test_level_1000_equals_all_words_for_this_list(tmp_path: Path) -> None:
    session_1000 = _open(tmp_path, Level(1000))
    session_all = _open(tmp_path, Level(None))
    assert session_1000.remaining_in_level == 1000
    assert session_all.remaining_in_level == 1000


def test_words_known_at_level_100_stay_known_at_level_1000(tmp_path: Path) -> None:
    first = _open(tmp_path, Level(100))
    shown = first.next_card()
    assert shown is not None
    first.mark_known()
    session = _open(tmp_path, Level(1000))
    assert session.remaining == 999
    assert session.remaining_in_level == 999


def test_marking_known_at_level_100_keeps_words_outside_the_level(
    tmp_path: Path,
) -> None:
    session = _open(tmp_path, Level(100))
    session.next_card()
    session.mark_known()
    saved = _saved(tmp_path)
    assert len(saved) == 999
    assert saved[-900:] == ALL_CARDS[100:]


def test_level_whose_words_are_all_known_is_finished_at_once(
    tmp_path: Path,
) -> None:
    _learn_to_the_end(_open(tmp_path, Level(100)))
    session = _open(tmp_path, Level(100))
    assert session.remaining_in_level == 0
    assert session.remaining == 900
    assert session.next_card() is None
