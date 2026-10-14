"""End-to-end tests of the flash card window.

@file test_flash_card_window.py
@brief Builds the real window with Tk and checks it against the wireframe.
"""

import time
import tkinter as tk
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path

import pytest

from flash_card.application.use_cases.open_study_session import open_study_session
from flash_card.application.use_cases.study_session import StudySession
from flash_card.constants import (
    BACK_TEXT_COLOR,
    BACKGROUND_COLOR,
    CARD_HEIGHT,
    CARD_WIDTH,
    FINISHED_MESSAGE,
    FLIP_DELAY_MS,
    FRONT_TEXT_COLOR,
    LANGUAGE_FONT,
    WINDOW_PADDING,
    WINDOW_TITLE,
    WORD_FONT,
)
from flash_card.domain.entities.card import Card
from flash_card.domain.entities.deck import Deck
from flash_card.domain.value_objects.language_pair import LanguagePair
from flash_card.infrastructure.persistence.csv_progress_repository import (
    CsvProgressRepository,
)
from flash_card.infrastructure.persistence.csv_vocabulary_repository import (
    CsvVocabularyRepository,
)
from flash_card.infrastructure.speech.null_speech import NullSpeech
from flash_card.presentation.features.flash_card import flash_card_view
from flash_card.presentation.features.flash_card.flash_card_view import FlashCardView
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)

CARDS = (Card("aku", "mig"), Card("kau", "du"), Card("ini", "denne"))


def _first(cards: Sequence[Card]) -> Card:
    return cards[0]


class _MemoryProgress:
    """Progress store that keeps nothing: the shared window never deletes cards."""

    def load(self) -> Deck | None:
        return None

    def save(self, deck: Deck) -> None:
        return None


class _RecordingSpeech:
    """Speech port that records what would have been spoken."""

    def __init__(self) -> None:
        self.spoken: list[tuple[str, str]] = []

    def speak(self, text: str, language_code: str) -> None:
        self.spoken.append((text, language_code))


SPEECH = _RecordingSpeech()


def _build_view(root: tk.Tk) -> FlashCardView:
    deck = Deck(LanguagePair("ms", "da"), CARDS)
    session = StudySession(deck, _first, _MemoryProgress(), SPEECH)
    return FlashCardView(root, FlashCardViewModel(session))


def _shown(view: FlashCardView) -> tuple[str, str]:
    return (
        str(view.canvas.itemcget(view.language_text_id, "text")),
        str(view.canvas.itemcget(view.word_text_id, "text")),
    )


@pytest.fixture(scope="module")
def window() -> Iterator[tuple[tk.Tk, FlashCardView]]:
    # One Tk per module: a second interpreter right after destroying the
    # first fails to find init.tcl on some Windows Python installs.
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    view = _build_view(root)
    root.update_idletasks()
    yield root, view
    root.destroy()


def test_window_has_title_background_and_padding(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    root, _view = window
    assert root.title() == WINDOW_TITLE
    assert root.cget("bg") == BACKGROUND_COLOR
    assert int(str(root.cget("padx"))) == WINDOW_PADDING
    assert int(str(root.cget("pady"))) == WINDOW_PADDING


def test_canvas_has_card_size_and_spans_two_columns(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    assert int(str(view.canvas.cget("width"))) == CARD_WIDTH
    assert int(str(view.canvas.cget("height"))) == CARD_HEIGHT
    info = view.canvas.grid_info()
    assert (int(info["row"]), int(info["column"])) == (0, 0)
    assert int(info["columnspan"]) == 2


def test_canvas_holds_one_image_and_two_texts(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    types = [view.canvas.type(item) for item in view.canvas.find_all()]
    assert types.count("image") == 1
    assert types.count("text") == 2
    assert len(types) == 3


def test_texts_show_first_card_with_font_and_colour(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    canvas = view.canvas
    expected = [
        (view.language_text_id, "Malay", LANGUAGE_FONT),
        (view.word_text_id, "aku", WORD_FONT),
    ]
    for item, text, font in expected:
        assert canvas.itemcget(item, "text") == text
        assert canvas.itemcget(item, "fill") == FRONT_TEXT_COLOR
        family, size, style = font
        assert canvas.itemcget(item, "font").split() == [family, str(size), style]


def test_buttons_sit_in_row_one_with_their_images(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    wrong = view.wrong_button.grid_info()
    right = view.right_button.grid_info()
    assert (int(wrong["row"]), int(wrong["column"])) == (1, 0)
    assert (int(right["row"]), int(right["column"])) == (1, 1)
    wrong_image = str(view.wrong_button.cget("image"))
    right_image = str(view.right_button.cget("image"))
    assert wrong_image
    assert right_image
    assert wrong_image != right_image
    assert str(view.wrong_button.cget("command"))
    assert str(view.right_button.cget("command"))


def test_buttons_sit_on_the_window_background(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    assert view.wrong_button.cget("bg") == BACKGROUND_COLOR
    assert view.right_button.cget("bg") == BACKGROUND_COLOR


def test_wrong_button_press_shows_next_card(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    assert _shown(view) == ("Malay", "aku")
    view.wrong_button.invoke()
    assert _shown(view) == ("Malay", "kau")
    view.wrong_button.invoke()
    assert _shown(view) == ("Malay", "aku")


def _word(view: FlashCardView) -> str:
    return _shown(view)[1]


def _image(view: FlashCardView) -> str:
    return str(view.canvas.itemcget(view.image_id, "image"))


def _fill(view: FlashCardView) -> tuple[str, str]:
    return (
        str(view.canvas.itemcget(view.language_text_id, "fill")),
        str(view.canvas.itemcget(view.word_text_id, "fill")),
    )


def _reset(root: tk.Tk, view: FlashCardView) -> None:
    """Show a fresh front with no pending timer."""
    view.next_card()
    if view.flip_timer is not None:
        root.after_cancel(view.flip_timer)
        view.flip_timer = None


def test_front_state_uses_front_image_black_text_and_front_language(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    root, view = window
    _reset(root, view)
    assert _image(view) == str(view.card_front_image)
    assert _fill(view) == (FRONT_TEXT_COLOR, FRONT_TEXT_COLOR)
    assert _shown(view)[0] == "Malay"
    assert _word(view) in {card.front for card in CARDS}


def test_flip_card_shows_back_image_white_text_and_translation(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    root, view = window
    _reset(root, view)
    front = _word(view)
    view.flip_card()
    translations = {card.front: card.back for card in CARDS}
    assert _image(view) == str(view.card_back_image)
    assert _image(view) != str(view.card_front_image)
    assert _fill(view) == (BACK_TEXT_COLOR, BACK_TEXT_COLOR)
    assert _shown(view) == ("Danish", translations[front])
    assert view.flip_timer is None


def test_next_card_after_flip_shows_front_again(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    root, view = window
    _reset(root, view)
    view.flip_card()
    view.wrong_button.invoke()
    assert _image(view) == str(view.card_front_image)
    assert _fill(view) == (FRONT_TEXT_COLOR, FRONT_TEXT_COLOR)
    assert _shown(view)[0] == "Malay"
    _reset(root, view)


def test_next_card_cancels_pending_timer_and_schedules_flip(
    window: tuple[tk.Tk, FlashCardView],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, view = window
    _reset(root, view)
    calls: list[tuple[str, object]] = []

    def fake_after(delay: int, callback: Callable[[], None]) -> str:
        calls.append(("after", (delay, callback)))
        return "timer-id"

    def fake_cancel(timer_id: str) -> None:
        calls.append(("cancel", timer_id))

    monkeypatch.setattr(root, "after", fake_after, raising=False)
    monkeypatch.setattr(root, "after_cancel", fake_cancel, raising=False)
    view.flip_timer = "old-id"
    view.next_card()
    assert calls == [
        ("cancel", "old-id"),
        ("after", (FLIP_DELAY_MS, view.flip_card)),
    ]
    assert view.flip_timer == "timer-id"
    view.flip_timer = None


def test_real_timer_flips_card_after_delay(
    window: tuple[tk.Tk, FlashCardView],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, view = window
    monkeypatch.setattr(flash_card_view, "FLIP_DELAY_MS", 50)
    view.next_card()
    assert _image(view) == str(view.card_front_image)
    deadline = time.monotonic() + 2
    while view.flip_timer is not None and time.monotonic() < deadline:
        root.update()
        time.sleep(0.005)
    assert view.flip_timer is None
    assert _image(view) == str(view.card_back_image)
    assert _shown(view)[0] == "Danish"
    _reset(root, view)


HEADER_ONLY = "ms;da\n"


@pytest.fixture
def files_view(
    window: tuple[tk.Tk, FlashCardView], tmp_path: Path
) -> Iterator[tuple[FlashCardView, Path]]:
    """A second view on the shared root, over real repositories in tmp_path."""
    root, _shared = window
    words = tmp_path / "words.csv"
    words.write_text("ms;da\naku;mig\nkau;du\nini;denne\n", encoding="utf-8")
    progress = tmp_path / "words_to_learn.csv"
    session = open_study_session(
        CsvVocabularyRepository(words),
        CsvProgressRepository(progress),
        NullSpeech(),
        _first,
    )
    view = FlashCardView(root, FlashCardViewModel(session))
    yield view, progress
    if view.flip_timer is not None:
        root.after_cancel(view.flip_timer)
    for widget in (view.canvas, view.wrong_button, view.right_button):
        widget.destroy()


def _saved(progress: Path) -> str:
    return progress.read_bytes().decode("utf-8-sig")


def test_right_button_removes_card_and_writes_progress_file(
    files_view: tuple[FlashCardView, Path],
) -> None:
    view, progress = files_view
    assert _shown(view) == ("Malay", "aku")
    view.right_button.invoke()
    assert _shown(view) == ("Malay", "kau")
    assert _saved(progress) == "ms;da\nkau;du\nini;denne\n"


def test_wrong_button_shows_next_card_and_leaves_progress_file_absent(
    files_view: tuple[FlashCardView, Path],
) -> None:
    view, progress = files_view
    view.wrong_button.invoke()
    assert _shown(view) == ("Malay", "kau")
    assert not progress.exists()


def test_buttons_do_nothing_visible_when_finished(
    files_view: tuple[FlashCardView, Path],
) -> None:
    view, progress = files_view
    for _ in range(3):
        view.right_button.invoke()
    assert _shown(view) == ("", FINISHED_MESSAGE)
    assert view.flip_timer is None
    assert _saved(progress) == HEADER_ONLY
    view.right_button.invoke()
    view.wrong_button.invoke()
    assert _shown(view) == ("", FINISHED_MESSAGE)
    assert view.flip_timer is None
    assert _saved(progress) == HEADER_ONLY


def test_button_press_speaks_the_malay_word_of_the_shown_card(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    root, view = window
    SPEECH.spoken.clear()
    view.wrong_button.invoke()
    assert SPEECH.spoken == [(_word(view), "ms")]
    _reset(root, view)
