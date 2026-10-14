"""End-to-end tests of the flash card window.

@file test_flash_card_window.py
@brief Builds the real window with Tk and checks it against the wireframe.
"""

import tkinter as tk
from collections.abc import Iterator

import pytest

from flash_card.constants import (
    BACKGROUND_COLOR,
    CARD_HEIGHT,
    CARD_WIDTH,
    FRONT_TEXT_COLOR,
    LANGUAGE_FONT,
    PLACEHOLDER_LANGUAGE_NAME,
    PLACEHOLDER_WORD,
    WINDOW_PADDING,
    WINDOW_TITLE,
    WORD_FONT,
)
from flash_card.presentation.features.flash_card.flash_card_view import FlashCardView
from flash_card.presentation.features.flash_card.flash_card_view_model import (
    FlashCardViewModel,
)


@pytest.fixture(scope="module")
def window() -> Iterator[tuple[tk.Tk, FlashCardView]]:
    # One Tk per module: a second interpreter right after destroying the
    # first fails to find init.tcl on some Windows Python installs.
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    view = FlashCardView(root, FlashCardViewModel())
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


def test_texts_show_placeholders_with_font_and_colour(
    window: tuple[tk.Tk, FlashCardView],
) -> None:
    _root, view = window
    canvas = view.canvas
    expected = [
        (view.language_text_id, PLACEHOLDER_LANGUAGE_NAME, LANGUAGE_FONT),
        (view.word_text_id, PLACEHOLDER_WORD, WORD_FONT),
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
    assert not str(view.wrong_button.cget("command"))
    assert not str(view.right_button.cget("command"))
