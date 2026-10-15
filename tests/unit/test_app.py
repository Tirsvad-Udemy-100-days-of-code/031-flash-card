"""Tests of the entry point.

@file test_app.py
@brief Checks main and Application of flash_card.presentation.app without Tk.
"""

import tkinter as tk
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import cast

import pytest

from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.entities.vocabulary import Vocabulary
from flash_card.domain.errors.vocabulary_errors import VocabularyNotFoundError
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.domain.value_objects.level import Level
from flash_card.presentation import app
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)
from flash_card.presentation.features.level.level_view_model import LevelViewModel

PAIR = LanguagePair("ms", "da")
CARDS = (Card("aku", "mig"), Card("kau", "du"), Card("ini", "denne"))


class _FakeRoot:
    def __init__(self) -> None:
        self.mainloop_calls = 0
        self.destroyed = False

    def mainloop(self) -> None:
        self.mainloop_calls += 1

    def destroy(self) -> None:
        self.destroyed = True


class _FakeApplication:
    def __init__(self, root: _FakeRoot, exit_code: int = 0) -> None:
        self.root = root
        self.exit_code = exit_code


class _FakeLevelView:
    def __init__(
        self,
        root: object,
        view_model: LevelViewModel,
        on_choose: Callable[[Level], None],
    ) -> None:
        self.view_model = view_model
        self.on_choose = on_choose
        self.destroyed = False

    def destroy(self) -> None:
        self.destroyed = True


class _FakeFlashCardView:
    def __init__(self, root: object, view_model: FlashCardViewModel) -> None:
        self.view_model = view_model
        self.closed = False

    def close(self) -> None:
        self.closed = True


class _FakeMenuView:
    def __init__(self, root: object, view_model: object, application: object) -> None:
        self.application = application


class _Vocabulary:
    def __init__(self, error: bool = False) -> None:
        self._error = error

    def load(self) -> Vocabulary:
        if self._error:
            raise VocabularyNotFoundError("word list not found")
        return Vocabulary(PAIR, CARDS)


class _Progress:
    def __init__(self) -> None:
        self.resets = 0

    def load(self) -> Deck | None:
        return None

    def save(self, deck: Deck) -> None:
        return None

    def reset(self) -> None:
        self.resets += 1


class _Speech:
    def speak(self, text: str, language_code: str) -> None:
        return None


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


@pytest.fixture(autouse=True)
def fake_tk_root(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep every test in this module away from a real Tk root."""
    monkeypatch.setattr(app.tk, "Tk", _FakeRoot)
    monkeypatch.setattr(app, "MenuView", _FakeMenuView)


@pytest.fixture
def fake_views(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(app, "LevelView", _FakeLevelView)
    monkeypatch.setattr(app, "FlashCardView", _FakeFlashCardView)


LIST_PATH = Path("lists") / "ms-da.csv"
OTHER_PATH = Path("lists") / "animals.csv"


class _Factory:
    """Repositories for a path, recorded; the paths in bad are unusable."""

    def __init__(self, error: bool = False, bad: tuple[Path, ...] = ()) -> None:
        self._error = error
        self._bad = bad
        self.progress: dict[Path, _Progress] = {}
        self.calls: list[Path] = []

    def __call__(self, path: Path) -> tuple[_Vocabulary, _Progress]:
        self.calls.append(path)
        progress = self.progress.setdefault(path, _Progress())
        return _Vocabulary(self._error or path in self._bad), progress


def _application(
    root: _FakeRoot, error: bool = False, factory: _Factory | None = None
) -> app.Application:
    repositories_for = _Factory(error) if factory is None else factory
    return app.Application(
        cast(tk.Tk, root), _Speech(), _first, repositories_for, LIST_PATH
    )


def _recording_create(
    seen: list[Level | None], exit_code: int = 0
) -> Callable[..., _FakeApplication]:
    def fake_create(
        data_dir: Path | None = None,
        speech_enabled: bool = True,
        level: Level | None = None,
    ) -> _FakeApplication:
        seen.append(level)
        return _FakeApplication(_FakeRoot(), exit_code)

    return fake_create


def test_main_runs_main_loop_and_returns_zero(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _FakeRoot()
    seen: list[tuple[Path | None, Level | None]] = []

    def fake_create(
        data_dir: Path | None = None,
        speech_enabled: bool = True,
        level: Level | None = None,
    ) -> _FakeApplication:
        seen.append((data_dir, level))
        return _FakeApplication(root)

    monkeypatch.setattr(app, "create_application", fake_create)

    assert app.main(["--data-dir", str(tmp_path)]) == 0
    assert root.mainloop_calls == 1
    assert seen == [(tmp_path, None)]


def test_main_returns_one_when_word_list_is_missing_with_level(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    code = app.main(["--data-dir", str(tmp_path / "nowhere"), "--level", "all"])
    assert code == 1
    assert "word list not found" in caplog.text


@pytest.mark.parametrize(
    ("value", "limit"), [("100", 100), ("1000", 1000), ("all", None)]
)
def test_main_passes_level_of_level_option(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, value: str, limit: int | None
) -> None:
    seen: list[Level | None] = []
    monkeypatch.setattr(app, "create_application", _recording_create(seen))

    assert app.main(["--data-dir", str(tmp_path), "--level", value]) == 0
    assert seen == [Level(limit)]


def test_main_refuses_unknown_level(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as raised:
        app.main(["--level", "50"])
    assert raised.value.code == 2
    assert "invalid level" in capsys.readouterr().err


def test_main_returns_exit_code_of_application(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    seen: list[Level | None] = []
    monkeypatch.setattr(app, "create_application", _recording_create(seen, 1))

    assert app.main(["--data-dir", str(tmp_path)]) == 1


def test_application_shows_no_view_before_a_screen_is_requested(
    fake_views: None,
) -> None:
    assert _application(_FakeRoot()).view is None


def test_show_level_screen_offers_the_three_levels(fake_views: None) -> None:
    application = _application(_FakeRoot())
    application.show_level_screen()
    view = application.view
    assert isinstance(view, _FakeLevelView)
    assert [c.level.limit for c in view.view_model.choices] == [100, 1000, None]


def test_choosing_a_level_replaces_level_screen_by_card_screen(
    fake_views: None,
) -> None:
    application = _application(_FakeRoot())
    application.show_level_screen()
    level_view = application.view
    assert isinstance(level_view, _FakeLevelView)

    level_view.on_choose(Level(100))

    assert level_view.destroyed
    assert isinstance(application.view, _FakeFlashCardView)
    assert application.exit_code == 0


def test_start_draws_the_first_card_of_the_level(fake_views: None) -> None:
    application = _application(_FakeRoot())
    application.start(Level(2))
    view = application.view
    assert isinstance(view, _FakeFlashCardView)
    assert view.view_model.text == "aku"


def test_start_without_level_screen_shows_card_screen_only(
    fake_views: None,
) -> None:
    application = _application(_FakeRoot())
    application.start(Level(None))
    assert isinstance(application.view, _FakeFlashCardView)


def test_choosing_a_level_closes_window_with_code_one_on_vocabulary_error(
    fake_views: None, caplog: pytest.LogCaptureFixture
) -> None:
    root = _FakeRoot()
    application = _application(root, error=True)
    application.show_level_screen()
    level_view = application.view
    assert isinstance(level_view, _FakeLevelView)

    level_view.on_choose(Level(100))

    assert root.destroyed
    assert application.exit_code == 1
    assert "word list not found" in caplog.text


def test_start_raises_vocabulary_error_for_the_caller(fake_views: None) -> None:
    application = _application(_FakeRoot(), error=True)
    with pytest.raises(VocabularyNotFoundError):
        application.start(Level(100))


def test_resolve_data_files_uses_bundled_list_when_default_folder_has_none(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    bundled = tmp_path / "bundle" / "ms-da.csv"
    monkeypatch.setattr(app, "DEFAULT_DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(app, "BUNDLED_VOCABULARY_PATH", bundled)
    vocabulary, progress = app.resolve_data_files(None)
    assert vocabulary == bundled
    assert progress == tmp_path / "data" / "words_to_learn.csv"


def test_resolve_data_files_prefers_the_default_folder_list(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "ms-da.csv").write_text("x", encoding="utf-8")
    monkeypatch.setattr(app, "DEFAULT_DATA_DIR", tmp_path)
    monkeypatch.setattr(app, "BUNDLED_VOCABULARY_PATH", tmp_path / "other.csv")
    vocabulary, _ = app.resolve_data_files(None)
    assert vocabulary == tmp_path / "ms-da.csv"


def test_resolve_data_files_uses_a_given_folder_alone(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(app, "BUNDLED_VOCABULARY_PATH", tmp_path / "other.csv")
    vocabulary, progress = app.resolve_data_files(tmp_path / "given")
    assert vocabulary == tmp_path / "given" / "ms-da.csv"
    assert progress == tmp_path / "given" / "words_to_learn.csv"


def test_create_application_draws_first_card_from_bundled_list(
    fake_views: None, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    bundled = tmp_path / "bundle" / "ms-da.csv"
    bundled.parent.mkdir()
    bundled.write_text("ms;da\nsaya;jeg\n", encoding="utf-8")
    data = tmp_path / "data"
    monkeypatch.setattr(app, "DEFAULT_DATA_DIR", data)
    monkeypatch.setattr(app, "BUNDLED_VOCABULARY_PATH", bundled)
    application = app.create_application(None, False, Level(None))
    view = cast(_FakeFlashCardView, application.view)
    assert view.view_model.text == "saya"
    view.view_model.is_known()
    assert (data / "words_to_learn.csv").is_file()


def test_word_list_name_and_folder_are_those_of_the_list_in_use() -> None:
    application = _application(_FakeRoot())
    assert application.word_list_name == "ms-da.csv"
    assert application.word_list_folder == Path("lists")


def test_open_word_list_replaces_repositories_and_shows_level_screen(
    fake_views: None,
) -> None:
    factory = _Factory()
    application = _application(_FakeRoot(), factory=factory)
    application.start(Level(None))
    card_view = application.view
    assert isinstance(card_view, _FakeFlashCardView)

    application.open_word_list(OTHER_PATH)

    assert card_view.closed
    assert isinstance(application.view, _FakeLevelView)
    assert application.word_list_name == "animals.csv"
    application.start(Level(None))
    application.reset_word_list()
    assert factory.progress[OTHER_PATH].resets == 1
    assert factory.progress[LIST_PATH].resets == 0


def test_open_word_list_raises_and_changes_nothing_when_list_is_invalid(
    fake_views: None,
) -> None:
    factory = _Factory(bad=(OTHER_PATH,))
    application = _application(_FakeRoot(), factory=factory)
    application.start(Level(None))
    card_view = application.view
    assert isinstance(card_view, _FakeFlashCardView)

    with pytest.raises(VocabularyNotFoundError):
        application.open_word_list(OTHER_PATH)

    assert application.view is card_view
    assert not card_view.closed
    assert application.word_list_name == "ms-da.csv"
    application.reset_word_list()
    assert factory.progress[LIST_PATH].resets == 1
    assert factory.progress[OTHER_PATH].resets == 0


def test_change_level_closes_the_card_screen_and_shows_the_level_screen(
    fake_views: None,
) -> None:
    application = _application(_FakeRoot())
    application.start(Level(None))
    card_view = application.view
    assert isinstance(card_view, _FakeFlashCardView)

    application.change_level()

    assert card_view.closed
    assert isinstance(application.view, _FakeLevelView)


def test_change_level_destroys_the_level_screen_it_replaces(
    fake_views: None,
) -> None:
    application = _application(_FakeRoot())
    application.show_level_screen()
    first = application.view
    assert isinstance(first, _FakeLevelView)

    application.change_level()

    assert first.destroyed
    assert application.view is not first


def test_reset_word_list_resets_progress_then_shows_the_level_screen(
    fake_views: None,
) -> None:
    factory = _Factory()
    application = _application(_FakeRoot(), factory=factory)
    application.start(Level(None))

    application.reset_word_list()

    assert factory.progress[LIST_PATH].resets == 1
    assert isinstance(application.view, _FakeLevelView)


def test_exit_application_closes_the_screen_and_destroys_the_root(
    fake_views: None,
) -> None:
    root = _FakeRoot()
    application = _application(root)
    application.start(Level(None))
    card_view = application.view
    assert isinstance(card_view, _FakeFlashCardView)

    application.exit_application()

    assert card_view.closed
    assert root.destroyed
    assert application.exit_code == 0
