"""Integration tests of the word list reader on the delivered file."""

from pathlib import Path

from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.constants import (
    DEFAULT_DATA_DIR,
    PROGRESS_FILE_NAME,
    VOCABULARY_FILE_NAME,
)
from flash_card.domain.entities.card import Card
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.domain.value_objects.level import Level
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.persistence.csv_word_list import read_word_list
from flash_card.infrastructure.speech.null_speech import NullSpeech

PATH = DEFAULT_DATA_DIR / VOCABULARY_FILE_NAME


def test_read_word_list_reads_real_file() -> None:
    pair, cards = read_word_list(PATH)
    assert pair == LanguagePair("ms", "da")
    assert len(cards) == 1000
    assert cards[0] == Card("aku", "mig")


def test_open_study_session_yields_card_from_real_file(tmp_path: Path) -> None:
    repository = CsvVocabularyRepository(PATH)
    cards = repository.load().cards
    progress = CsvProgressRepository(tmp_path / PROGRESS_FILE_NAME)
    session = open_study_session(
        repository,
        progress,
        NullSpeech(),
        lambda candidates: candidates[0],
        Level(None),
    )

    card = session.next_card()

    assert card is not None
    assert Card(card.front_text, card.back_text) in cards
    assert (card.front_language, card.back_language) == ("ms", "da")
