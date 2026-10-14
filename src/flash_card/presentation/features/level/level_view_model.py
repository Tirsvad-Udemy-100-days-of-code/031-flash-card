"""View model of the level screen.

@file level_view_model.py
@brief Exposes the title and the level choices; free of any Tkinter import.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from flash_card.constants import LEVEL_CHOICES, LEVEL_TITLE
from flash_card.domain.value_objects.level import Level


@dataclass(frozen=True, slots=True)
class LevelChoice:
    """One choice on the level screen."""

    ## @brief Text of the choice.
    label: str
    ## @brief The level the choice stands for.
    level: Level


class LevelViewModel:
    """Data the level view shows."""

    def __init__(self, choices: Sequence[tuple[str, int | None]] | None = None) -> None:
        """Create the view model.

        @param choices Label and word limit of each choice, or None for the
            choices of the program.
        """
        source = LEVEL_CHOICES if choices is None else choices
        ## @brief The choices in display order.
        self._choices = tuple(
            LevelChoice(label, Level(limit)) for label, limit in source
        )

    @property
    def title(self) -> str:
        """Return the title of the screen.

        @return The title text.
        """
        return LEVEL_TITLE

    @property
    def choices(self) -> tuple[LevelChoice, ...]:
        """Return the choices.

        @return The choices in display order.
        """
        return self._choices
