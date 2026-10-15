"""Integration tests: every word list keeps its progress in a file of its own."""

from collections.abc import Sequence
from pathlib import Path

from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.domain.entities.card import Card
from flash_card.domain.value_objects.level import Level
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.persistence.progress_file_name import (
    progress_file_name,
)
from flash_card.infrastructure.speech.null_speech import NullSpeech

MS_DA = "ms;da\naku;mig\nkau;du\nini;denne\n"
ANIMALS = "ms;da\nkucing;kat\nanjing;hund\n"


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


def _lists(folder: Path) -> tuple[Path, Path]:
    default = folder / "ms-da.csv"
    other = folder / "animals.csv"
    default.write_bytes(MS_DA.encode("utf-8"))
    other.write_bytes(ANIMALS.encode("utf-8"))
    return default, other


def _progress(folder: Path, list_path: Path) -> CsvProgressRepository:
    return CsvProgressRepository(folder / progress_file_name(list_path))


def _know_first_word(folder: Path, list_path: Path) -> str:
    session = open_study_session(
        CsvVocabularyRepository(list_path),
        _progress(folder, list_path),
        NullSpeech(),
        _first,
        Level(None),
    )
    card = session.next_card()
    assert card is not None
    session.mark_known()
    return card.front_text


def _remaining(folder: Path, list_path: Path) -> list[str]:
    deck = _progress(folder, list_path).load()
    assert deck is not None
    return [card.front for card in deck.cards]


def test_known_words_of_one_list_never_appear_in_the_other(tmp_path: Path) -> None:
    default, other = _lists(tmp_path)

    assert _know_first_word(tmp_path, default) == "aku"
    assert _know_first_word(tmp_path, other) == "kucing"

    assert _remaining(tmp_path, default) == ["kau", "ini"]
    assert _remaining(tmp_path, other) == ["anjing"]
    assert (tmp_path / "words_to_learn.csv").is_file()
    assert (tmp_path / "words_to_learn_animals.csv").is_file()


def test_reset_of_one_list_deletes_only_its_progress_file(tmp_path: Path) -> None:
    default, other = _lists(tmp_path)
    _know_first_word(tmp_path, default)
    _know_first_word(tmp_path, other)

    _progress(tmp_path, other).reset()

    assert not (tmp_path / "words_to_learn_animals.csv").exists()
    assert _remaining(tmp_path, default) == ["kau", "ini"]


def test_reset_leaves_the_word_list_file_byte_identical(tmp_path: Path) -> None:
    default, other = _lists(tmp_path)
    _know_first_word(tmp_path, other)

    _progress(tmp_path, other).reset()

    assert other.read_bytes() == ANIMALS.encode("utf-8")
    assert default.read_bytes() == MS_DA.encode("utf-8")


def test_delivered_list_keeps_words_to_learn_file_name(tmp_path: Path) -> None:
    default, _other = _lists(tmp_path)
    assert progress_file_name(default) == "words_to_learn.csv"
