"""Tests of write_word_list and CsvProgressRepository."""

from pathlib import Path

import pytest

from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.errors.vocabulary_errors import VocabularyFormatError
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_word_list import (
    read_word_list,
    write_word_list,
)

PAIR = LanguagePair("ms", "da")
CARDS = (Card("aku", "mig"), Card("kau", "du"))


def test_write_word_list_round_trips_through_read_word_list(tmp_path: Path) -> None:
    path = tmp_path / "w.csv"
    write_word_list(path, PAIR, CARDS)
    assert read_word_list(path) == (PAIR, CARDS)


def test_write_word_list_writes_header_and_rows_with_semicolon(
    tmp_path: Path,
) -> None:
    path = tmp_path / "w.csv"
    write_word_list(path, PAIR, CARDS)
    raw = path.read_bytes()
    assert raw.decode("utf-8-sig") == "ms;da\naku;mig\nkau;du\n"
    assert b"\r" not in raw


def test_write_word_list_keeps_non_ascii_text(tmp_path: Path) -> None:
    path = tmp_path / "w.csv"
    cards = (Card("chaque", "each"), Card("parlé", "speak"))
    write_word_list(path, LanguagePair("fr", "en"), cards)
    assert read_word_list(path)[1] == cards


def test_write_word_list_writes_header_only_for_no_cards(tmp_path: Path) -> None:
    path = tmp_path / "w.csv"
    write_word_list(path, PAIR, ())
    assert read_word_list(path) == (PAIR, ())


def test_write_word_list_creates_parent_folder(tmp_path: Path) -> None:
    path = tmp_path / "data" / "deep" / "w.csv"
    write_word_list(path, PAIR, CARDS)
    assert path.is_file()


def test_write_word_list_replaces_file_and_leaves_no_temporary_file(
    tmp_path: Path,
) -> None:
    path = tmp_path / "w.csv"
    write_word_list(path, PAIR, CARDS)
    write_word_list(path, PAIR, CARDS[:1])
    assert read_word_list(path)[1] == CARDS[:1]
    assert [item.name for item in tmp_path.iterdir()] == ["w.csv"]


def test_write_word_list_keeps_old_file_and_no_temporary_when_write_fails(
    tmp_path: Path,
) -> None:
    path = tmp_path / "w.csv"
    write_word_list(path, PAIR, CARDS)
    unencodable = (Card("aku", "\ud800"),)
    with pytest.raises(UnicodeEncodeError):
        write_word_list(path, PAIR, unencodable)
    assert read_word_list(path)[1] == CARDS
    assert [item.name for item in tmp_path.iterdir()] == ["w.csv"]


def test_progress_load_returns_none_when_file_is_missing(tmp_path: Path) -> None:
    assert CsvProgressRepository(tmp_path / "p.csv").load() is None


def test_progress_load_returns_empty_deck_for_header_only_file(
    tmp_path: Path,
) -> None:
    path = tmp_path / "p.csv"
    path.write_text("ms;da\n", encoding="utf-8")
    deck = CsvProgressRepository(path).load()
    assert deck is not None
    assert deck.is_empty
    assert deck.language_pair == PAIR


def test_progress_load_raises_format_error_and_keeps_malformed_file(
    tmp_path: Path,
) -> None:
    path = tmp_path / "p.csv"
    content = b"ms;da\naku;mig;extra\n"
    path.write_bytes(content)
    with pytest.raises(VocabularyFormatError):
        CsvProgressRepository(path).load()
    assert path.read_bytes() == content


def test_progress_save_then_load_returns_same_cards(tmp_path: Path) -> None:
    repository = CsvProgressRepository(tmp_path / "p.csv")
    repository.save(Deck(PAIR, CARDS))
    deck = repository.load()
    assert deck is not None
    assert deck.cards == CARDS
    assert deck.language_pair == PAIR
