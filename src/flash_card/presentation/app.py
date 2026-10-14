"""Entry point and composition root of the flash card program.

@file app.py
@brief Creates the window, shows the level screen and then the card screen.
"""

import argparse
import importlib.util
import logging
import random
import tkinter as tk
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import NoReturn

from flash_card.application.ports.speech_port import SpeechPort
from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.constants import (
    DEFAULT_DATA_DIR,
    LEVEL_ARGUMENT_VALUES,
    PROGRESS_FILE_NAME,
    VOCABULARY_FILE_NAME,
)
from flash_card.domain.entities.card import Card
from flash_card.domain.errors.vocabulary_errors import VocabularyError
from flash_card.domain.repositories.progress_repository import ProgressRepository
from flash_card.domain.repositories.vocabulary_repository import VocabularyRepository
from flash_card.domain.value_objects.level import Level
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.speech.gtts_speech import GttsSpeech
from flash_card.infrastructure.speech.null_speech import NullSpeech
from flash_card.presentation.features.flash_card.flash_card_view import FlashCardView
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)
from flash_card.presentation.features.level.level_view import LevelView
from flash_card.presentation.features.level.level_view_model import LevelViewModel

## @brief Logger of the entry point.
_logger = logging.getLogger(__name__)

## @brief Optional packages the spoken words need.
_SPEECH_PACKAGES = ("gtts", "playsound")


def build_speech(enabled: bool) -> SpeechPort:
    """Choose the speech adapter.

    @param enabled False when the user switched speech off.
    @return GttsSpeech when enabled and gtts and playsound are installed,
        else NullSpeech.
    """
    if enabled and all(
        importlib.util.find_spec(name) is not None for name in _SPEECH_PACKAGES
    ):
        return GttsSpeech()
    return NullSpeech()


class Application:
    """The running program: one window that shows the level screen, then the card."""

    def __init__(
        self,
        root: tk.Tk,
        vocabulary_repository: VocabularyRepository,
        progress_repository: ProgressRepository,
        speech: SpeechPort,
        choose: Callable[[Sequence[Card]], Card] = random.choice,
    ) -> None:
        """Create the application on a window; no screen is shown yet.

        @param root The Tk root window.
        @param vocabulary_repository Source of the delivered word list.
        @param progress_repository Store of the words still to learn.
        @param speech Speaks the front text of each drawn card.
        @param choose Picks one card from a non-empty sequence.
        """
        ## @brief The Tk root window.
        self.root = root
        ## @brief Source of the delivered word list.
        self._vocabulary_repository = vocabulary_repository
        ## @brief Store of the words still to learn.
        self._progress_repository = progress_repository
        ## @brief Speaks the front text of each drawn card.
        self._speech = speech
        ## @brief Picks one card from a non-empty sequence.
        self._choose = choose
        ## @brief The screen shown now, or None before the first one.
        self._view: LevelView | FlashCardView | None = None
        ## @brief The exit code of the program.
        self._exit_code = 0

    @property
    def view(self) -> LevelView | FlashCardView | None:
        """Return the screen shown now.

        @return The level screen, the card screen, or None before the first.
        """
        return self._view

    @property
    def exit_code(self) -> int:
        """Return the exit code the program ends with.

        @return 0, or 1 when a session could not be started after a choice.
        """
        return self._exit_code

    def show_level_screen(self) -> None:
        """Show the level screen; a choice starts the session.

        @return Nothing.
        """
        self._view = LevelView(self.root, LevelViewModel(), self._choose_level)

    def start(self, level: Level) -> None:
        """Open the session of a level and show the card screen on the window.

        @param level The level the user chose.
        @return Nothing.
        @throws VocabularyError When the word list or saved progress is unusable.
        """
        session = open_study_session(
            self._vocabulary_repository,
            self._progress_repository,
            self._speech,
            self._choose,
            level,
        )
        if isinstance(self._view, LevelView):
            self._view.destroy()
        self._view = FlashCardView(self.root, FlashCardViewModel(session))

    def _choose_level(self, level: Level) -> None:
        """Start the session after a click; close the window when it fails.

        @param level The level the user chose.
        @return Nothing.
        """
        try:
            self.start(level)
        except VocabularyError as error:
            _logger.error("%s", error)
            self._exit_code = 1
            self.root.destroy()


def create_application(
    data_dir: Path | None = None,
    speech_enabled: bool = True,
    level: Level | None = None,
) -> Application:
    """Create the window and show the level screen, or start at the given level.

    @param data_dir Folder of the data files, or None for the default folder.
    @param speech_enabled False to run without spoken words.
    @param level The level to start at, or None to show the level screen.
    @return The application, its window in the root attribute.
    @throws VocabularyError When a level is given and the word list or saved
        progress is unusable.
    """
    folder = DEFAULT_DATA_DIR if data_dir is None else data_dir
    root = tk.Tk()
    application = Application(
        root,
        CsvVocabularyRepository(folder / VOCABULARY_FILE_NAME),
        CsvProgressRepository(folder / PROGRESS_FILE_NAME),
        build_speech(speech_enabled),
    )
    if level is None:
        application.show_level_screen()
        return application
    try:
        application.start(level)
    except VocabularyError:
        root.destroy()
        raise
    return application


def _level_argument(value: str) -> Level:
    """Convert a --level value to a level.

    @param value One of the keys of LEVEL_ARGUMENT_VALUES.
    @return The level.
    @throws argparse.ArgumentTypeError When the value is unknown.
    """
    if value not in LEVEL_ARGUMENT_VALUES:
        choices = ", ".join(LEVEL_ARGUMENT_VALUES)
        raise argparse.ArgumentTypeError(
            f"invalid level {value!r} (choose from {choices})"
        )
    return Level(LEVEL_ARGUMENT_VALUES[value])


def main(argv: Sequence[str] | None = None) -> int:
    """Run the program and return its exit code.

    @param argv Command line arguments, or None for those of the process.
    @return The exit code, 0 on success and 1 when the word list is unusable.
    """
    parser = argparse.ArgumentParser(description="Flash card program.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="folder of the data files",
    )
    parser.add_argument(
        "--no-speech",
        action="store_true",
        help="do not speak the words",
    )
    parser.add_argument(
        "--level",
        type=_level_argument,
        default=None,
        metavar="{" + ",".join(LEVEL_ARGUMENT_VALUES) + "}",
        help="start at a level (100, 1000 or all words) and skip the level screen",
    )
    args = parser.parse_args(argv)
    try:
        application = create_application(args.data_dir, not args.no_speech, args.level)
    except VocabularyError as error:
        _logger.error("%s", error)
        return 1
    application.root.mainloop()
    return application.exit_code


def run() -> NoReturn:
    """Run the program and exit the interpreter with its exit code.

    @return Never returns; the function always raises SystemExit.
    @throws SystemExit Always, with the exit code of main.
    """
    raise SystemExit(main())
