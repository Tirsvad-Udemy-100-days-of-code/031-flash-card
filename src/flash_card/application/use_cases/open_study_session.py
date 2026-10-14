"""Start a study session.

@file open_study_session.py
@brief The open_study_session use case.
"""

from collections.abc import Callable, Sequence

from flash_card.application.ports.speech_port import SpeechPort
from flash_card.application.use_cases.study_session import StudySession
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.repositories.progress_repository import ProgressRepository
from flash_card.domain.repositories.vocabulary_repository import VocabularyRepository


def open_study_session(
    vocabulary_repository: VocabularyRepository,
    progress_repository: ProgressRepository,
    speech: SpeechPort,
    choose: Callable[[Sequence[Card]], Card],
) -> StudySession:
    """Build a session over the saved words to learn, else the whole word list.

    @param vocabulary_repository Source of the delivered word list.
    @param progress_repository Store of the words still to learn.
    @param speech Speaks the front text of each drawn card.
    @param choose Picks one card from a non-empty sequence.
    @return The new session.
    @throws VocabularyError When the saved progress, or the word list when no
        progress exists, cannot be loaded.
    """
    deck = progress_repository.load()
    if deck is None:
        deck = Deck.from_vocabulary(vocabulary_repository.load())
    return StudySession(deck, choose, progress_repository, speech)
