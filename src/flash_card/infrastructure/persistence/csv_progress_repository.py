"""CSV implementation of the progress port.

@file csv_progress_repository.py
@brief The CsvProgressRepository adapter.
"""

from pathlib import Path

from flash_card.domain.entities.deck import Deck
from flash_card.infrastructure.persistence.csv_word_list import (
    read_word_list,
    write_word_list,
)


class CsvProgressRepository:
    """Keeps the words still to learn in a CSV file."""

    def __init__(self, path: Path) -> None:
        """Create the repository.

        @param path The words to learn file.
        """
        ## @brief The words to learn file.
        self._path = path

    def load(self) -> Deck | None:
        """Load the saved words to learn.

        @return The deck, possibly empty, or None when the file does not exist.
        @throws VocabularyFormatError When the file is malformed; it is left as is.
        """
        if not self._path.exists():
            return None
        pair, cards = read_word_list(self._path)
        return Deck(pair, cards)

    def save(self, deck: Deck) -> None:
        """Save the words still to learn.

        @param deck The cards still to learn.
        @return Nothing.
        """
        write_word_list(self._path, deck.language_pair, deck.cards)
