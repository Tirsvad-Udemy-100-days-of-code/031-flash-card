"""Reading and writing of the word list CSV file.

@file csv_word_list.py
@brief Reads and writes a semicolon separated word list with a language code
header; the format is defined once here.
"""

import csv
from collections.abc import Iterable
from pathlib import Path

from flash_card.constants import CSV_DELIMITER, CSV_ENCODING
from flash_card.domain.entities.card import Card
from flash_card.domain.errors.vocabulary_errors import (
    VocabularyFormatError,
    VocabularyNotFoundError,
)
from flash_card.domain.value_objects.language_pair import LanguagePair

## @brief Number of cells in the header and in every card row.
_CELLS_PER_ROW = 2


def _format_error(path: Path, line: int, reason: str) -> VocabularyFormatError:
    """Build a format error naming the file and line.

    @param path The file read.
    @param line The line number of the fault.
    @param reason What is wrong.
    @return The error to raise.
    """
    return VocabularyFormatError(f"{path}, line {line}: {reason}")


def _parse_header(path: Path, line: int, row: list[str]) -> LanguagePair:
    """Parse the header row.

    @param path The file read.
    @param line The line number of the row.
    @param row The cells of the row.
    @return The language pair.
    @throws VocabularyFormatError When the header is not two codes.
    """
    cells = [cell.strip() for cell in row]
    if len(cells) != _CELLS_PER_ROW or not all(cells):
        raise _format_error(path, line, "header must hold two language codes")
    return LanguagePair(cells[0], cells[1])


def _parse_card(path: Path, line: int, row: list[str]) -> Card:
    """Parse a card row.

    @param path The file read.
    @param line The line number of the row.
    @param row The cells of the row.
    @return The card.
    @throws VocabularyFormatError When the row is not two cells.
    """
    if len(row) != _CELLS_PER_ROW:
        raise _format_error(path, line, "row must hold exactly two cells")
    return Card(row[0].strip(), row[1].strip())


def read_word_list(path: Path) -> tuple[LanguagePair, tuple[Card, ...]]:
    """Read a word list file.

    @param path The CSV file: a header of two language codes, then one card a row.
    @return The language pair and the cards in file order.
    @throws VocabularyNotFoundError When the file does not exist.
    @throws VocabularyFormatError When the file is empty or a row is malformed.
    """
    pair: LanguagePair | None = None
    cards: list[Card] = []
    try:
        with path.open(encoding=CSV_ENCODING, newline="") as file:
            reader = csv.reader(file, delimiter=CSV_DELIMITER)
            for row in reader:
                if not any(cell.strip() for cell in row):
                    continue
                if pair is None:
                    pair = _parse_header(path, reader.line_num, row)
                else:
                    cards.append(_parse_card(path, reader.line_num, row))
    except FileNotFoundError as error:
        raise VocabularyNotFoundError(f"word list not found: {path}") from error
    if pair is None:
        raise _format_error(path, 1, "file is empty")
    return pair, tuple(cards)


def write_word_list(
    path: Path, language_pair: LanguagePair, cards: Iterable[Card]
) -> None:
    """Write a word list file atomically.

    The rows go to a temporary file in the same folder, which then replaces the
    target, so a crash never leaves a half written file.

    @param path The CSV file to create or replace.
    @param language_pair The languages, written as the header row.
    @param cards The cards, written one row each in the given order.
    @return Nothing.
    @throws OSError When the file cannot be written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    rows = [(language_pair.front_code, language_pair.back_code)]
    rows.extend((card.front, card.back) for card in cards)
    try:
        with temporary.open("w", encoding=CSV_ENCODING, newline="") as file:
            writer = csv.writer(file, delimiter=CSV_DELIMITER, lineterminator="\n")
            writer.writerows(rows)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
