"""End-to-end tests of the level screen and the flow to the first card.

@file test_level_window.py
@brief Builds the real level screen with Tk and checks it against the wireframe.
"""

import shutil
import tkinter as tk
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path

import pytest

from flash_card.constants import (
    BACKGROUND_COLOR,
    CARD_WIDTH,
    DEFAULT_DATA_DIR,
    FINISHED_MESSAGE,
    LEVEL_BUTTON_COLOR,
    LEVEL_BUTTON_FONT,
    LEVEL_SCREEN_HEIGHT,
    LEVEL_TITLE,
    LEVEL_TITLE_FONT,
    VOCABULARY_FILE_NAME,
    WINDOW_PADDING,
    WINDOW_TITLE,
)
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.repositories.progress_repository import ProgressRepository
from flash_card.domain.repositories.vocabulary_repository import VocabularyRepository
from flash_card.domain.value_objects.level import Level
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.persistence.progress_file_name import (
    progress_file_name,
)
from flash_card.infrastructure.speech.null_speech import NullSpeech
from flash_card.presentation import app
from flash_card.presentation.features.flash_card.flash_card_view import FlashCardView
from flash_card.presentation.features.level.level_view import LevelView
from flash_card.presentation.features.level.level_view_model import LevelViewModel


def _last(cards: Sequence[Card]) -> Card:
    return cards[-1]


def _label(button: tk.Button) -> str:
    return str(button.cget("text"))


def _word(view: FlashCardView) -> str:
    return str(view.canvas.itemcget(view.word_text_id, "text"))


def _clear(root: tk.Tk, view: object) -> None:
    """Destroy the widgets of whichever screen is shown, and pending timers."""
    if isinstance(view, FlashCardView):
        view.close()
    elif isinstance(view, LevelView):
        view.destroy()


def repositories_for(
    folder: Path,
) -> Callable[[Path], tuple[VocabularyRepository, ProgressRepository]]:
    """Build the CSV repositories of a list, its progress file in folder."""

    def build(list_path: Path) -> tuple[VocabularyRepository, ProgressRepository]:
        return (
            CsvVocabularyRepository(list_path),
            CsvProgressRepository(folder / progress_file_name(list_path)),
        )

    return build


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    shutil.copy(DEFAULT_DATA_DIR / VOCABULARY_FILE_NAME, tmp_path)
    return tmp_path


@pytest.fixture
def application(tk_root: tk.Tk, data_dir: Path) -> Iterator[app.Application]:
    instance = app.Application(
        tk_root,
        NullSpeech(),
        _last,
        repositories_for(data_dir),
        data_dir / VOCABULARY_FILE_NAME,
    )
    yield instance
    _clear(tk_root, instance.view)


@pytest.fixture
def level_view(tk_root: tk.Tk) -> Iterator[LevelView]:
    chosen: list[Level] = []
    view = LevelView(tk_root, LevelViewModel(), chosen.append)
    tk_root.update_idletasks()
    yield view
    view.destroy()


def test_level_screen_shows_title_with_font_on_window_background(
    level_view: LevelView,
) -> None:
    label = level_view.title_label
    assert label.cget("text") == LEVEL_TITLE == "Choose your level"
    assert label.cget("bg") == BACKGROUND_COLOR
    family, size, style = LEVEL_TITLE_FONT
    assert str(label.cget("font")).split() == [family, str(size), style]
    assert level_view.frame.cget("bg") == BACKGROUND_COLOR


def test_level_screen_sets_window_title_background_and_padding(
    tk_root: tk.Tk,
) -> None:
    tk_root.title("tk")
    tk_root.config(padx=0, pady=0, bg="white")

    view = LevelView(tk_root, LevelViewModel(), lambda level: None)
    try:
        assert tk_root.title() == WINDOW_TITLE
        assert tk_root.cget("bg") == BACKGROUND_COLOR
        assert int(str(tk_root.cget("padx"))) == WINDOW_PADDING
        assert int(str(tk_root.cget("pady"))) == WINDOW_PADDING
    finally:
        view.destroy()


def test_level_screen_frame_has_the_card_window_size(level_view: LevelView) -> None:
    assert level_view.frame.winfo_width() == CARD_WIDTH
    assert level_view.frame.winfo_height() == LEVEL_SCREEN_HEIGHT


def test_level_screen_shows_three_buttons_in_order(level_view: LevelView) -> None:
    labels = [_label(button) for button in level_view.buttons]
    assert labels == ["100 words", "1000 words", "All words"]
    rows = [int(button.grid_info()["row"]) for button in level_view.buttons]
    assert rows == [1, 2, 3]


def test_level_buttons_have_equal_width_font_and_colour(
    level_view: LevelView,
) -> None:
    widths = {int(str(button.cget("width"))) for button in level_view.buttons}
    assert len(widths) == 1
    family, size, style = LEVEL_BUTTON_FONT
    for button in level_view.buttons:
        assert str(button.cget("font")).split() == [family, str(size), style]
        assert button.cget("bg") == LEVEL_BUTTON_COLOR
    assert len({button.winfo_reqwidth() for button in level_view.buttons}) == 1


def test_clicking_a_button_forwards_its_level(tk_root: tk.Tk) -> None:
    chosen: list[Level] = []
    view = LevelView(tk_root, LevelViewModel(), chosen.append)
    for button in view.buttons:
        button.invoke()
    view.destroy()
    assert chosen == [Level(100), Level(1000), Level(None)]


def test_destroy_removes_the_level_frame(tk_root: tk.Tk) -> None:
    view = LevelView(tk_root, LevelViewModel(), lambda level: None)
    view.destroy()
    assert not view.frame.winfo_exists()


def test_clicking_100_words_replaces_screen_with_first_card_of_first_hundred(
    tk_root: tk.Tk, application: app.Application, data_dir: Path
) -> None:
    first_hundred = (
        CsvVocabularyRepository(data_dir / VOCABULARY_FILE_NAME).load().cards[:100]
    )
    application.show_level_screen()
    level_view = application.view
    assert isinstance(level_view, LevelView)

    level_view.buttons[0].invoke()

    card_view = application.view
    assert isinstance(card_view, FlashCardView)
    assert not level_view.frame.winfo_exists()
    assert _word(card_view) == first_hundred[-1].front
    assert tk_root.title() == WINDOW_TITLE
    assert int(str(tk_root.cget("padx"))) == WINDOW_PADDING


def test_level_whose_words_are_all_known_shows_the_finished_message(
    application: app.Application, data_dir: Path
) -> None:
    cards = CsvVocabularyRepository(data_dir / VOCABULARY_FILE_NAME).load().cards
    pair = CsvVocabularyRepository(data_dir / VOCABULARY_FILE_NAME).load().language_pair
    CsvProgressRepository(data_dir / "words_to_learn.csv").save(Deck(pair, cards[100:]))
    application.show_level_screen()
    level_view = application.view
    assert isinstance(level_view, LevelView)

    level_view.buttons[0].invoke()

    card_view = application.view
    assert isinstance(card_view, FlashCardView)
    assert _word(card_view) == FINISHED_MESSAGE


def test_create_application_with_level_skips_the_level_screen(
    tk_root: tk.Tk, data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tk, "Tk", lambda: tk_root)

    application = app.create_application(data_dir, False, Level(100))

    try:
        assert isinstance(application.view, FlashCardView)
        assert not [c for c in tk_root.winfo_children() if isinstance(c, tk.Frame)]
        assert str(tk_root.cget("menu"))
    finally:
        _clear(tk_root, application.view)
        tk_root.config(menu="")


def test_create_application_without_level_shows_the_level_screen(
    tk_root: tk.Tk, data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tk, "Tk", lambda: tk_root)

    application = app.create_application(data_dir, False)

    try:
        assert isinstance(application.view, LevelView)
        assert application.root is tk_root
        assert str(tk_root.cget("menu"))
    finally:
        _clear(tk_root, application.view)
        tk_root.config(menu="")


def test_create_application_with_word_list_keeps_progress_in_the_data_folder(
    tk_root: tk.Tk, data_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tk, "Tk", lambda: tk_root)
    other = tmp_path / "other" / "animals.csv"
    other.parent.mkdir()
    other.write_text("ms;da\nkucing;kat\n", encoding="utf-8")

    application = app.create_application(data_dir, False, Level(None), other)

    try:
        view = application.view
        assert isinstance(view, FlashCardView)
        assert application.word_list_name == "animals.csv"
        view.right_button.invoke()
        assert (data_dir / "words_to_learn_animals.csv").is_file()
    finally:
        _clear(tk_root, application.view)
        tk_root.config(menu="")
