"""Start a study session.

@file open_study_session.py
@brief The open_study_session use case.
"""

from collections.abc import Callable, Sequence

from flash_card.application.use_cases.study_session import StudySession
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.repositories.vocabulary_repository import VocabularyRepository


def open_study_session(
    vocabulary_repository: VocabularyRepository,
    choose: Callable[[Sequence[Card]], Card],
) -> StudySession:
    """Load the word list and build a session over all its cards.

    @param vocabulary_repository Source of the word list.
    @param choose Picks one card from a non-empty sequence.
    @return The new session.
    @throws VocabularyError When the word list cannot be loaded.
    """
    deck = Deck.from_vocabulary(vocabulary_repository.load())
    return StudySession(deck, choose)
