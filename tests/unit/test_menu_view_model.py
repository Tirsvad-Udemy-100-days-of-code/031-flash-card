"""Tests of the menu view model; no Tkinter is involved."""

import pytest

from flash_card.presentation.features.menu.menu_view_model import (
    MenuEntry,
    MenuViewModel,
)


def test_file_entries_are_open_change_level_reset_and_exit_in_order() -> None:
    labels = [entry.label for entry in MenuViewModel().file_entries]
    assert labels == ["Open...", "Change level...", "Reset word list...", "Exit"]


def test_file_entries_name_distinct_commands() -> None:
    commands = [entry.command for entry in MenuViewModel().file_entries]
    assert commands == [
        "open_word_list",
        "change_level",
        "reset_word_list",
        "exit_program",
    ]


def test_menu_labels_are_file_about_and_contact() -> None:
    model = MenuViewModel()
    assert model.file_label == "File"
    assert model.about_label == "About"
    assert model.contact_menu_label == "Contact"


def test_contact_shows_name_and_title() -> None:
    assert MenuViewModel().contact_label == "Jens Tirsvad Nielsen, Software engineer"


def test_contact_url_is_the_linkedin_page() -> None:
    assert MenuViewModel().contact_url == "https://www.linkedin.com/in/tirsvad74"


def test_menu_entry_is_immutable() -> None:
    entry = MenuEntry("Exit", "exit_program", 1)
    with pytest.raises(AttributeError):
        entry.label = "Quit"  # type: ignore[misc]
