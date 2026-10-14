"""Tests of the level view model."""

import dataclasses

import pytest

from flash_card.constants import LEVEL_TITLE
from flash_card.domain.value_objects.level import Level
from flash_card.presentation.features.level import level_view_model
from flash_card.presentation.features.level.level_view_model import (
    LevelChoice,
    LevelViewModel,
)


def test_title_is_choose_your_level() -> None:
    assert LevelViewModel().title == LEVEL_TITLE == "Choose your level"


def test_choices_are_three_levels_in_order() -> None:
    choices = LevelViewModel().choices
    assert [choice.label for choice in choices] == [
        "100 words",
        "1000 words",
        "All words",
    ]
    assert [choice.level for choice in choices] == [
        Level(100),
        Level(1000),
        Level(None),
    ]


def test_choices_come_from_given_choices() -> None:
    model = LevelViewModel([("Ten", 10)])
    assert model.choices == (LevelChoice("Ten", Level(10)),)


def test_choice_is_frozen() -> None:
    choice = LevelChoice("Ten", Level(10))
    with pytest.raises(dataclasses.FrozenInstanceError):
        choice.label = "x"  # type: ignore[misc]


def test_view_model_module_does_not_import_tkinter() -> None:
    assert "tkinter" not in vars(level_view_model)
