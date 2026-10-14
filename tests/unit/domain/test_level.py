"""Tests of the Level value object."""

import dataclasses

import pytest

from flash_card.domain.entities.card import Card
from flash_card.domain.value_objects.level import Level

CARDS = tuple(Card(f"w{i}", f"v{i}") for i in range(1000))


@pytest.mark.parametrize("limit", [0, -1, -100])
def test_level_refuses_limit_not_above_zero(limit: int) -> None:
    with pytest.raises(ValueError, match="above zero"):
        Level(limit)


def test_level_accepts_no_limit() -> None:
    assert Level(None).limit is None


def test_level_is_frozen() -> None:
    level = Level(100)
    with pytest.raises(dataclasses.FrozenInstanceError):
        level.limit = 5  # type: ignore[misc]


def test_first_returns_first_hundred_cards_when_limit_is_100() -> None:
    assert Level(100).first(CARDS) == CARDS[:100]


def test_first_returns_all_cards_when_there_is_no_limit() -> None:
    assert Level(None).first(CARDS) == CARDS


def test_first_returns_all_cards_when_limit_exceeds_the_list() -> None:
    assert Level(5000).first(CARDS) == CARDS


def test_first_returns_empty_when_list_is_empty() -> None:
    assert Level(100).first(()) == ()
