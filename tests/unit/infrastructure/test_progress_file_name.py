"""Tests of the name of the words to learn file of a word list."""

from pathlib import Path

import pytest

from flash_card.infrastructure.persistence.progress_file_name import (
    progress_file_name,
)


def test_progress_file_name_is_default_for_the_delivered_list() -> None:
    assert progress_file_name(Path("data") / "ms-da.csv") == "words_to_learn.csv"


def test_progress_file_name_uses_the_stem_for_another_list() -> None:
    assert progress_file_name(Path("x") / "animals.csv") == "words_to_learn_animals.csv"


def test_progress_file_name_keeps_hyphen_and_underscore() -> None:
    name = progress_file_name(Path("my_list-2.csv"))
    assert name == "words_to_learn_my_list-2.csv"


@pytest.mark.parametrize(
    ("file_name", "expected"),
    [
        ("my list.csv", "words_to_learn_my_list.csv"),
        ("a.b;c.csv", "words_to_learn_a_b_c.csv"),
        ("ord (1).csv", "words_to_learn_ord__1_.csv"),
    ],
)
def test_progress_file_name_replaces_other_characters(
    file_name: str, expected: str
) -> None:
    assert progress_file_name(Path(file_name)) == expected
