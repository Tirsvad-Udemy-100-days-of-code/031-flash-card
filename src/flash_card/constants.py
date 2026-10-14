"""All constants of the flash card program, defined once.

@file constants.py
@brief Window, card, font, language, file and asset constants.
Imports only the standard library.
"""

from collections.abc import Mapping
from pathlib import Path
from typing import Final

from flash_card.runtime import executable_dir, is_frozen, resource_root

## @brief Window background colour.
BACKGROUND_COLOR: Final[str] = "#B1DDC6"
## @brief Window title.
WINDOW_TITLE: Final[str] = "Flashy"
## @brief Padding around the card in pixels.
WINDOW_PADDING: Final[int] = 50

## @brief Card width in pixels.
CARD_WIDTH: Final[int] = 800
## @brief Card height in pixels.
CARD_HEIGHT: Final[int] = 526
## @brief Level screen height in pixels: card plus the card window button row.
LEVEL_SCREEN_HEIGHT: Final[int] = 526 + 100
## @brief Horizontal centre of the card in pixels.
CARD_CENTER_X: Final[int] = 400
## @brief Vertical position of the language text in pixels.
LANGUAGE_TEXT_Y: Final[int] = 150
## @brief Vertical position of the word text in pixels.
WORD_TEXT_Y: Final[int] = 263
## @brief Delay before the card flips, in milliseconds.
FLIP_DELAY_MS: Final[int] = 3000

## @brief Font of the language text: family, size, style.
LANGUAGE_FONT: Final[tuple[str, int, str]] = ("Arial", 40, "italic")
## @brief Font of the word text: family, size, style.
WORD_FONT: Final[tuple[str, int, str]] = ("Arial", 60, "bold")
## @brief Text colour on the card front.
FRONT_TEXT_COLOR: Final[str] = "black"
## @brief Text colour on the card back.
BACK_TEXT_COLOR: Final[str] = "white"

## @brief Display names by language code; the caller shows unknown codes in upper case.
LANGUAGE_NAMES: Final[Mapping[str, str]] = {"ms": "Malay", "da": "Danish"}
## @brief Message shown when no word is left to learn.
FINISHED_MESSAGE: Final[str] = "Nothing left to learn"

## @brief Title of the level screen.
LEVEL_TITLE: Final[str] = "Choose your level"
## @brief Level choices in display order: label and word limit (None = all words).
LEVEL_CHOICES: Final[tuple[tuple[str, int | None], ...]] = (
    ("100 words", 100),
    ("1000 words", 1000),
    ("All words", None),
)
## @brief Values of the --level option and the word limit each stands for.
LEVEL_ARGUMENT_VALUES: Final[Mapping[str, int | None]] = {
    "100": 100,
    "1000": 1000,
    "all": None,
}
## @brief Font of the level screen title: family, size, style.
LEVEL_TITLE_FONT: Final[tuple[str, int, str]] = ("Arial", 40, "italic")
## @brief Font of the level buttons: family, size, style.
LEVEL_BUTTON_FONT: Final[tuple[str, int, str]] = ("Arial", 24, "bold")
## @brief Width of every level button in characters.
LEVEL_BUTTON_WIDTH: Final[int] = 14
## @brief Background colour of the level buttons.
LEVEL_BUTTON_COLOR: Final[str] = "white"

## @brief Delimiter of the CSV files.
CSV_DELIMITER: Final[str] = ";"
## @brief Encoding of the CSV files; drops a leading byte order mark.
CSV_ENCODING: Final[str] = "utf-8-sig"
## @brief File name of the vocabulary.
VOCABULARY_FILE_NAME: Final[str] = "ms-da.csv"
## @brief File name of the words still to learn.
PROGRESS_FILE_NAME: Final[str] = "words_to_learn.csv"

## @brief Root folder of the project, for a source run.
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
## @brief Folder of the image assets, inside the bundle when frozen.
ASSETS_DIR: Final[Path] = (
    resource_root() / "flash_card" / "presentation" / "assets"
    if is_frozen()
    else Path(__file__).resolve().parent / "presentation" / "assets"
)
## @brief Folder of the word list delivered with the program.
BUNDLED_DATA_DIR: Final[Path] = resource_root() / "data"
## @brief The word list delivered with the program.
BUNDLED_VOCABULARY_PATH: Final[Path] = BUNDLED_DATA_DIR / VOCABULARY_FILE_NAME
## @brief Default folder of the data files, next to the executable when frozen.
DEFAULT_DATA_DIR: Final[Path] = executable_dir() / "data"
## @brief File name of the program icon.
ICON_FILE_NAME: Final[str] = "flash_card.ico"
## @brief Name of the executable without extension.
EXECUTABLE_NAME: Final[str] = "flash-card"
## @brief File name of the card front image.
CARD_FRONT_IMAGE_NAME: Final[str] = "card_front.png"
## @brief File name of the card back image.
CARD_BACK_IMAGE_NAME: Final[str] = "card_back.png"
## @brief File name of the right button image.
RIGHT_IMAGE_NAME: Final[str] = "right.png"
## @brief File name of the wrong button image.
WRONG_IMAGE_NAME: Final[str] = "wrong.png"
