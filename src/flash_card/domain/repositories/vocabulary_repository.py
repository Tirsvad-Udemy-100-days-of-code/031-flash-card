"""Port to the delivered word list.

@file vocabulary_repository.py
@brief The VocabularyRepository interface.
"""

from typing import Protocol

from flash_card.domain.entities.vocabulary import Vocabulary


class VocabularyRepository(Protocol):
    """Source of the delivered word list."""

    def load(self) -> Vocabulary:
        """Load the delivered word list.

        @return The vocabulary.
        @throws VocabularyError When the word list cannot be loaded.
        """
        ...
