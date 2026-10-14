"""Tests of the constants module.

@file test_constants.py
@brief Checks the key values of flash_card.constants.
"""

from flash_card import constants


def test_flip_delay_ms_is_three_seconds() -> None:
    assert constants.FLIP_DELAY_MS == 3000


def test_background_color_is_green() -> None:
    assert constants.BACKGROUND_COLOR == "#B1DDC6"


def test_default_data_dir_ends_with_data() -> None:
    assert constants.DEFAULT_DATA_DIR.name == "data"


def test_file_names_are_csv() -> None:
    assert constants.VOCABULARY_FILE_NAME.endswith(".csv")
    assert constants.PROGRESS_FILE_NAME.endswith(".csv")


def test_language_names_cover_ms_and_da() -> None:
    assert "ms" in constants.LANGUAGE_NAMES
    assert "da" in constants.LANGUAGE_NAMES


def test_project_root_contains_pyproject() -> None:
    assert (constants.PROJECT_ROOT / "pyproject.toml").is_file()


def test_csv_encoding_drops_byte_order_mark() -> None:
    assert constants.CSV_ENCODING == "utf-8-sig"
