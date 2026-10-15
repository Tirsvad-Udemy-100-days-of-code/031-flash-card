"""Port to the words still to learn.

@file progress_repository.py
@brief The ProgressRepository interface.
"""

from typing import Protocol

from flash_card.domain.entities.deck import Deck


class ProgressRepository(Protocol):
    """Store of the words still to learn."""

    def load(self) -> Deck | None:
        """Load the saved words to learn.

        @return The deck, or None when no progress was saved.
        @throws VocabularyError When the saved progress is unusable.
        """
        ...

    def save(self, deck: Deck) -> None:
        """Save the words still to learn.

        @param deck The cards still to learn.
        @return Nothing.
        """
        ...

    def reset(self) -> None:
        """Forget the saved words to learn, so every word is to learn again.

        @return Nothing.
        @throws OSError When the saved progress cannot be removed.
        """
        ...
