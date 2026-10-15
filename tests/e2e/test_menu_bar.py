"""End-to-end tests of the menu bar and its commands on a real Tk window.

@file test_menu_bar.py
@brief Builds the real menu bar with injected dialogs and checks the commands.
"""

import tkinter as tk
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path

import pytest

from flash_card.constants import CONTACT_URL, WINDOW_TITLE
from flash_card.domain.entities.card import Card
from flash_card.domain.repositories.progress_repository import ProgressRepository
from flash_card.domain.repositories.vocabulary_repository import VocabularyRepository
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
from flash_card.presentation.features.menu.menu_view import MenuView
from flash_card.presentation.features.menu.menu_view_model import MenuViewModel

DEFAULT_LIST = "ms;da\naku;mig\nkau;du\n"
OTHER_LIST = "ms;da\nkucing;kat\n"
CONTACT_LABEL = "Jens Tirsvad Nielsen, Software engineer"

FILE_INDEX = 0
ABOUT_INDEX = 1
OPEN, CHANGE_LEVEL, RESET, SEPARATOR, EXIT = range(5)


def _last(cards: Sequence[Card]) -> Card:
    return cards[-1]


class _Dialogs:
    """Records and answers the dialogs the menu view asks."""

    def __init__(self) -> None:
        self.file = ""
        self.answer = True
        self.asked_files: list[dict[str, object]] = []
        self.questions: list[str] = []
        self.errors: list[tuple[str, str]] = []
        self.urls: list[str] = []

    def ask_open_file(self, **options: object) -> str:
        self.asked_files.append(options)
        return self.file

    def confirm(self, title: str, message: str, **options: object) -> bool:
        self.questions.append(message)
        return self.answer

    def show_error(self, title: str, message: str, **options: object) -> str:
        self.errors.append((title, message))
        return "ok"

    def open_url(self, url: str) -> bool:
        self.urls.append(url)
        return True


class _Window:
    def __init__(
        self,
        root: tk.Tk,
        application: app.Application,
        menu: MenuView,
        dialogs: _Dialogs,
        folder: Path,
    ) -> None:
        self.root = root
        self.application = application
        self.menu = menu
        self.dialogs = dialogs
        self.folder = folder


def _repositories_for(
    folder: Path,
) -> Callable[[Path], tuple[VocabularyRepository, ProgressRepository]]:
    def build(list_path: Path) -> tuple[VocabularyRepository, ProgressRepository]:
        return (
            CsvVocabularyRepository(list_path),
            CsvProgressRepository(folder / progress_file_name(list_path)),
        )

    return build


def _close(window: _Window) -> None:
    view = window.application.view
    if isinstance(view, FlashCardView):
        view.close()
    elif isinstance(view, LevelView):
        view.destroy()
    window.root.config(menu="")
    window.menu.menubar.destroy()


@pytest.fixture
def window(tk_root: tk.Tk, tmp_path: Path) -> Iterator[_Window]:
    default = tmp_path / "ms-da.csv"
    default.write_bytes(DEFAULT_LIST.encode("utf-8"))
    application = app.Application(
        tk_root, NullSpeech(), _last, _repositories_for(tmp_path), default
    )
    dialogs = _Dialogs()
    menu = MenuView(
        tk_root,
        MenuViewModel(),
        application,
        ask_open_file=dialogs.ask_open_file,
        confirm=dialogs.confirm,
        show_error=dialogs.show_error,
        open_url=dialogs.open_url,
    )
    application.show_level_screen()
    instance = _Window(tk_root, application, menu, dialogs, tmp_path)
    yield instance
    _close(instance)


def _labels(menu: tk.Menu, last: int) -> list[str]:
    return [
        "-" if menu.type(i) == "separator" else str(menu.entrycget(i, "label"))
        for i in range(last + 1)
    ]


def _start_first_level(window: _Window) -> FlashCardView:
    level_view = window.application.view
    assert isinstance(level_view, LevelView)
    level_view.buttons[0].invoke()
    card_view = window.application.view
    assert isinstance(card_view, FlashCardView)
    return card_view


def _word(view: FlashCardView) -> str:
    return str(view.canvas.itemcget(view.word_text_id, "text"))


def test_menu_bar_has_file_and_about_in_order(window: _Window) -> None:
    menubar = window.menu.menubar
    assert str(window.root.cget("menu")) == str(menubar)
    assert menubar.index("end") == ABOUT_INDEX
    assert _labels(menubar, ABOUT_INDEX) == ["File", "About"]


def test_file_menu_has_four_entries_and_a_separator_before_exit(
    window: _Window,
) -> None:
    file_menu = window.menu.file_menu
    assert file_menu.index("end") == EXIT
    assert _labels(file_menu, EXIT) == [
        "Open...",
        "Change level...",
        "Reset word list...",
        "-",
        "Exit",
    ]
    assert file_menu.type(SEPARATOR) == "separator"


def test_file_entries_have_mnemonics(window: _Window) -> None:
    file_menu = window.menu.file_menu
    assert int(str(file_menu.entrycget(OPEN, "underline"))) == 0
    assert int(str(file_menu.entrycget(EXIT, "underline"))) == 1
    assert int(str(window.menu.menubar.entrycget(FILE_INDEX, "underline"))) == 0


def test_about_menu_leads_to_the_contact_entry(window: _Window) -> None:
    about = window.menu.about_menu
    assert _labels(about, 0) == ["Contact"]
    assert about.type(0) == "cascade"
    contact = window.menu.contact_menu
    assert contact.index("end") == 0
    assert _labels(contact, 0) == [CONTACT_LABEL]


def test_open_starts_the_chosen_list_after_a_level_choice(window: _Window) -> None:
    other = window.folder / "animals.csv"
    other.write_bytes(OTHER_LIST.encode("utf-8"))
    window.dialogs.file = str(other)

    window.menu.file_menu.invoke(OPEN)

    assert isinstance(window.application.view, LevelView)
    assert window.application.word_list_name == "animals.csv"
    assert _word(_start_first_level(window)) == "kucing"
    asked = window.dialogs.asked_files[0]
    assert asked["initialdir"] == str(window.folder)
    assert ("CSV files", "*.csv") in asked["filetypes"]  # type: ignore[operator]
    assert window.root.title() == WINDOW_TITLE


@pytest.mark.parametrize(
    "content",
    [None, b"ms;da\n\xff\xfe;x\n", "ms;da\nkøkken;x\n".encode("latin-1")],
    ids=["missing", "invalid-utf8", "latin-1"],
)
def test_open_of_an_invalid_file_shows_a_message_and_keeps_the_list(
    window: _Window, content: bytes | None
) -> None:
    bad = window.folder / "bad.csv"
    if content is not None:
        bad.write_bytes(content)
    window.dialogs.file = str(bad)
    level_view = window.application.view

    window.menu.file_menu.invoke(OPEN)

    assert len(window.dialogs.errors) == 1
    assert "bad.csv" in window.dialogs.errors[0][1]
    assert window.application.view is level_view
    assert window.application.word_list_name == "ms-da.csv"
    assert _word(_start_first_level(window)) == "kau"


def test_open_cancelled_changes_nothing(window: _Window) -> None:
    window.dialogs.file = ""
    level_view = window.application.view

    window.menu.file_menu.invoke(OPEN)

    assert window.application.view is level_view
    assert window.application.word_list_name == "ms-da.csv"
    assert not window.dialogs.errors


def test_change_level_shows_the_level_screen_and_keeps_known_words(
    window: _Window,
) -> None:
    card_view = _start_first_level(window)
    card_view.right_button.invoke()
    progress = window.folder / "words_to_learn.csv"
    saved = progress.read_bytes()

    window.menu.file_menu.invoke(CHANGE_LEVEL)

    assert isinstance(window.application.view, LevelView)
    assert card_view.flip_timer is None
    assert progress.read_bytes() == saved


def test_reset_asks_and_on_yes_removes_progress_and_shows_level_screen(
    window: _Window,
) -> None:
    card_view = _start_first_level(window)
    card_view.right_button.invoke()
    progress = window.folder / "words_to_learn.csv"
    assert progress.is_file()

    window.menu.file_menu.invoke(RESET)

    assert window.dialogs.questions == [
        "Start ms-da.csv from the beginning? All words will be to learn again."
    ]
    assert not progress.exists()
    assert isinstance(window.application.view, LevelView)
    assert (window.folder / "ms-da.csv").read_bytes() == DEFAULT_LIST.encode("utf-8")


def test_reset_answered_no_changes_nothing(window: _Window) -> None:
    card_view = _start_first_level(window)
    card_view.right_button.invoke()
    progress = window.folder / "words_to_learn.csv"
    window.dialogs.answer = False

    window.menu.file_menu.invoke(RESET)

    assert progress.is_file()
    assert window.application.view is card_view


def test_contact_opens_the_linkedin_page(window: _Window) -> None:
    window.menu.contact_menu.invoke(0)
    assert window.dialogs.urls == [CONTACT_URL]
    assert CONTACT_URL == "https://www.linkedin.com/in/tirsvad74"


def test_exit_cancels_the_timer_and_destroys_the_window(
    window: _Window, monkeypatch: pytest.MonkeyPatch
) -> None:
    destroyed: list[bool] = []
    monkeypatch.setattr(window.root, "destroy", lambda: destroyed.append(True))
    card_view = _start_first_level(window)
    assert card_view.flip_timer is not None

    window.menu.file_menu.invoke(EXIT)

    assert destroyed == [True]
    assert card_view.flip_timer is None
    assert window.application.exit_code == 0
