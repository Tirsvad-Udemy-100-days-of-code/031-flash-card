"""Tests of read_word_list and CsvVocabularyRepository."""

from pathlib import Path

import pytest

from flash_card.domain.entities.card import Card
from flash_card.domain.errors.vocabulary_errors import (
    VocabularyFormatError,
    VocabularyNotFoundError,
)
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.persistence.csv_word_list import read_word_list


def _write(path: Path, content: str) -> Path:
    path.write_bytes(content.encode("utf-8"))
    return path


def test_read_word_list_returns_pair_and_cards(tmp_path: Path) -> None:
    path = _write(tmp_path / "w.csv", "ms;da\naku;mig\nkau;du\n")
    pair, cards = read_word_list(path)
    assert pair == LanguagePair("ms", "da")
    assert cards == (Card("aku", "mig"), Card("kau", "du"))


def test_read_word_list_drops_byte_order_mark(tmp_path: Path) -> None:
    path = _write(tmp_path / "w.csv", "﻿ms;da\r\naku;mig\r\n")
    pair, cards = read_word_list(path)
    assert pair == LanguagePair("ms", "da")
    assert cards == (Card("aku", "mig"),)


def test_read_word_list_skips_blank_lines(tmp_path: Path) -> None:
    path = _write(tmp_path / "w.csv", "\nms;da\n\naku;mig\n  \n;\nkau;du\n\n")
    _pair, cards = read_word_list(path)
    assert cards == (Card("aku", "mig"), Card("kau", "du"))


def test_read_word_list_strips_whitespace(tmp_path: Path) -> None:
    path = _write(tmp_path / "w.csv", " ms ; da \n aku ; mig \n")
    pair, cards = read_word_list(path)
    assert pair == LanguagePair("ms", "da")
    assert cards == (Card("aku", "mig"),)


def test_read_word_list_raises_not_found_when_file_is_missing(
    tmp_path: Path,
) -> None:
    with pytest.raises(VocabularyNotFoundError) as info:
        read_word_list(tmp_path / "missing.csv")
    assert isinstance(info.value.__cause__, FileNotFoundError)


def test_read_word_list_raises_format_error_when_file_is_empty(
    tmp_path: Path,
) -> None:
    path = _write(tmp_path / "w.csv", "\n\n")
    with pytest.raises(VocabularyFormatError, match="empty"):
        read_word_list(path)


@pytest.mark.parametrize("header", ["ms\n", "ms;da;en\n", "ms;\n"])
def test_read_word_list_raises_format_error_for_bad_header(
    tmp_path: Path, header: str
) -> None:
    path = _write(tmp_path / "w.csv", header + "aku;mig\n")
    with pytest.raises(VocabularyFormatError, match="line 1"):
        read_word_list(path)


def test_read_word_list_raises_format_error_with_line_number_for_bad_row(
    tmp_path: Path,
) -> None:
    path = _write(tmp_path / "w.csv", "ms;da\naku;mig\n\nkau;du;extra\n")
    with pytest.raises(VocabularyFormatError, match="line 4") as info:
        read_word_list(path)
    assert str(path) in str(info.value)


def test_repository_load_returns_vocabulary(tmp_path: Path) -> None:
    path = _write(tmp_path / "w.csv", "ms;da\naku;mig\n")
    vocabulary = CsvVocabularyRepository(path).load()
    assert vocabulary.language_pair == LanguagePair("ms", "da")
    assert vocabulary.cards == (Card("aku", "mig"),)


def test_repository_load_raises_format_error_when_no_card(tmp_path: Path) -> None:
    path = _write(tmp_path / "w.csv", "ms;da\n")
    with pytest.raises(VocabularyFormatError):
        CsvVocabularyRepository(path).load()


@pytest.mark.parametrize(
    "content",
    [b"ms;da\n\xff\xfe;x\n", "ms;da\nkøkken;x\n".encode("latin-1")],
    ids=["invalid-utf8", "latin-1"],
)
def test_read_word_list_raises_format_error_when_not_utf8(
    tmp_path: Path, content: bytes
) -> None:
    path = tmp_path / "w.csv"
    path.write_bytes(content)
    with pytest.raises(VocabularyFormatError, match=r"w\.csv.*not UTF-8") as info:
        read_word_list(path)
    assert isinstance(info.value.__cause__, UnicodeDecodeError)
