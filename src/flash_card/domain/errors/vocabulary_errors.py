"""Errors of the vocabulary and the deck.

@file vocabulary_errors.py
@brief The VocabularyError hierarchy.
"""


class VocabularyError(Exception):
    """Base of every error about the word list or the deck."""


class VocabularyFormatError(VocabularyError):
    """The word list is not in the expected format."""


class VocabularyNotFoundError(VocabularyError):
    """The word list does not exist."""


class EmptyDeckError(VocabularyError):
    """A card was drawn from a deck with no card."""
