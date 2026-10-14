"""Tests of the vocabulary error hierarchy."""

import pytest

from flash_card.domain.errors.vocabulary_errors import (
    EmptyDeckError,
    VocabularyError,
    VocabularyFormatError,
    VocabularyNotFoundError,
)


@pytest.mark.parametrize(
    "error", [VocabularyFormatError, VocabularyNotFoundError, EmptyDeckError]
)
def test_error_is_a_vocabulary_error(error: type[VocabularyError]) -> None:
    assert issubclass(error, VocabularyError)


def test_vocabulary_error_is_an_exception() -> None:
    assert issubclass(VocabularyError, Exception)
