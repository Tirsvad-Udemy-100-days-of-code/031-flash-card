"""CSV implementation of the vocabulary port.

@file csv_vocabulary_repository.py
@brief The CsvVocabularyRepository adapter.
"""

from pathlib import Path

from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.errors.vocabulary_errors import VocabularyFormatError
from flash_card.infrastructure.persistence.csv_word_list import read_word_list


class CsvVocabularyRepository:
    """Loads the delivered word list from a CSV file."""

    def __init__(self, path: Path) -> None:
        """Create the repository.

        @param path The word list file.
        """
        ## @brief The word list file.
        self._path = path

    def load(self) -> Vocabulary:
        """Load the word list.

        @return The vocabulary.
        @throws VocabularyNotFoundError When the file does not exist.
        @throws VocabularyFormatError When the file is malformed or has no card.
        """
        pair, cards = read_word_list(self._path)
        if not cards:
            raise VocabularyFormatError(f"{self._path}: word list has no card")
        return Vocabulary(pair, cards)
