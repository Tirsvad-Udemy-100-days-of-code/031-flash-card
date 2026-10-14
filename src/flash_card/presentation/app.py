"""Entry point and composition root of the flash card program.

@file app.py
@brief Creates the window, its view model and view, and runs the main loop.
"""

import argparse
import logging
import random
import tkinter as tk
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn

from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.constants import DEFAULT_DATA_DIR, VOCABULARY_FILE_NAME
from flash_card.domain.errors.vocabulary_errors import VocabularyError
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.presentation.features.flash_card.flash_card_view import FlashCardView
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)

## @brief Logger of the entry point.
_logger = logging.getLogger(__name__)


def create_application(
    data_dir: Path | None = None,
) -> tuple[tk.Tk, FlashCardView]:
    """Create the root window and the flash card view.

    @param data_dir Folder of the data files, or None for the default folder.
    @return The root window and the view built on it.
    @throws VocabularyError When the word list cannot be loaded.
    """
    folder = DEFAULT_DATA_DIR if data_dir is None else data_dir
    repository = CsvVocabularyRepository(folder / VOCABULARY_FILE_NAME)
    session = open_study_session(repository, random.choice)
    view_model = FlashCardViewModel(session)
    root = tk.Tk()
    view = FlashCardView(root, view_model)
    return root, view


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
    args = parser.parse_args(argv)
    try:
        root, _view = create_application(args.data_dir)
    except VocabularyError as error:
        _logger.error("%s", error)
        return 1
    root.mainloop()
    return 0


def run() -> NoReturn:
    """Run the program and exit the interpreter with its exit code.

    @return Never returns; the function always raises SystemExit.
    @throws SystemExit Always, with the exit code of main.
    """
    raise SystemExit(main())
