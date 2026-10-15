"""View of the menu bar.

@file menu_view.py
@brief Builds the menu bar of the wireframe and asks the dialogs of its commands.
"""

import logging
import tkinter as tk
import webbrowser
from collections.abc import Callable
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Protocol

from flash_card.constants import (
    MENU_ABOUT_UNDERLINE,
    MENU_COMMAND_CHANGE_LEVEL,
    MENU_COMMAND_EXIT,
    MENU_COMMAND_OPEN,
    MENU_COMMAND_RESET,
    MENU_CONTACT_UNDERLINE,
    MENU_FILE_UNDERLINE,
    OPEN_DIALOG_TITLE,
    OPEN_ERROR_TEMPLATE,
    OPEN_ERROR_TITLE,
    OPEN_FILE_TYPES,
    RESET_CONFIRM_TEMPLATE,
    RESET_CONFIRM_TITLE,
    RESET_ERROR_TEMPLATE,
    RESET_ERROR_TITLE,
)
from flash_card.domain.errors.vocabulary_errors import VocabularyError
from flash_card.presentation.features.menu.menu_view_model import MenuViewModel

## @brief Logger of the menu view.
_logger = logging.getLogger(__name__)


class MenuApplication(Protocol):
    """What the menu view needs from the application."""

    @property
    def word_list_name(self) -> str:
        """Return the file name of the word list in use.

        @return The file name.
        """
        ...

    @property
    def word_list_folder(self) -> Path:
        """Return the folder of the word list in use.

        @return The folder.
        """
        ...

    def open_word_list(self, path: Path) -> None:
        """Switch to the word list in a file.

        @param path The CSV file.
        @return Nothing.
        """
        ...

    def change_level(self) -> None:
        """Show the level screen.

        @return Nothing.
        """
        ...

    def reset_word_list(self) -> None:
        """Forget the progress of the word list in use.

        @return Nothing.
        """
        ...

    def exit_application(self) -> None:
        """Close the window.

        @return Nothing.
        """
        ...


class MenuView:
    """The menu bar of the window: File and About."""

    def __init__(
        self,
        root: tk.Tk,
        view_model: MenuViewModel,
        application: MenuApplication,
        *,
        ask_open_file: Callable[..., str] = filedialog.askopenfilename,
        confirm: Callable[..., bool] = messagebox.askyesno,
        show_error: Callable[..., str] = messagebox.showerror,
        open_url: Callable[[str], bool] = webbrowser.open,
    ) -> None:
        """Build the menu bar on a root.

        @param root The Tk root window.
        @param view_model The labels and the contact data.
        @param application The commands the entries run.
        @param ask_open_file Shows the file dialog and returns the chosen path,
            or an empty value when cancelled.
        @param confirm Asks a yes or no question.
        @param show_error Shows an error message.
        @param open_url Opens an address in the web browser.
        """
        ## @brief The Tk root window.
        self._root = root
        ## @brief The labels and the contact data.
        self._view_model = view_model
        ## @brief The commands the entries run.
        self._application = application
        ## @brief Shows the file dialog.
        self._ask_open_file = ask_open_file
        ## @brief Asks a yes or no question.
        self._confirm = confirm
        ## @brief Shows an error message.
        self._show_error = show_error
        ## @brief Opens an address in the web browser.
        self._open_url = open_url
        ## @brief The menu bar of the window.
        self.menubar = tk.Menu(root, tearoff=False)
        ## @brief The File menu.
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        ## @brief The About menu.
        self.about_menu = tk.Menu(self.menubar, tearoff=False)
        ## @brief The Contact submenu of the About menu.
        self.contact_menu = tk.Menu(self.about_menu, tearoff=False)
        self._build()
        root.config(menu=self.menubar)

    def open_word_list(self) -> None:
        """Ask for a CSV file and switch to it; a refused file shows a message.

        @return Nothing.
        """
        chosen = self._ask_open_file(
            parent=self._root,
            title=OPEN_DIALOG_TITLE,
            initialdir=str(self._application.word_list_folder),
            filetypes=OPEN_FILE_TYPES,
        )
        if not chosen:
            return
        path = Path(chosen)
        try:
            self._application.open_word_list(path)
        except VocabularyError as error:
            _logger.error("%s", error)
            self._show_error(
                OPEN_ERROR_TITLE,
                OPEN_ERROR_TEMPLATE.format(name=path.name, reason=error),
                parent=self._root,
            )

    def change_level(self) -> None:
        """Show the level screen again.

        @return Nothing.
        """
        self._application.change_level()

    def reset_word_list(self) -> None:
        """Ask to confirm, then start the word list in use from the beginning.

        @return Nothing.
        """
        name = self._application.word_list_name
        question = RESET_CONFIRM_TEMPLATE.format(name=name)
        if not self._confirm(RESET_CONFIRM_TITLE, question, parent=self._root):
            return
        try:
            self._application.reset_word_list()
        except OSError as error:
            _logger.error("%s", error)
            self._show_error(
                RESET_ERROR_TITLE,
                RESET_ERROR_TEMPLATE.format(name=name, reason=error),
                parent=self._root,
            )

    def show_contact(self) -> None:
        """Open the LinkedIn page of the author in the web browser.

        @return Nothing.
        """
        try:
            self._open_url(self._view_model.contact_url)
        except (webbrowser.Error, OSError) as error:
            _logger.error("%s", error)

    def exit_program(self) -> None:
        """Close the window.

        @return Nothing.
        """
        self._application.exit_application()

    def _build(self) -> None:
        """Fill the menus and add them to the menu bar.

        @return Nothing.
        """
        commands = {
            MENU_COMMAND_OPEN: self.open_word_list,
            MENU_COMMAND_CHANGE_LEVEL: self.change_level,
            MENU_COMMAND_RESET: self.reset_word_list,
            MENU_COMMAND_EXIT: self.exit_program,
        }
        for entry in self._view_model.file_entries:
            if entry.command == MENU_COMMAND_EXIT:
                self.file_menu.add_separator()
            self.file_menu.add_command(
                label=entry.label,
                underline=entry.underline,
                command=commands[entry.command],
            )
        self.contact_menu.add_command(
            label=self._view_model.contact_label, command=self.show_contact
        )
        self.about_menu.add_cascade(
            label=self._view_model.contact_menu_label,
            underline=MENU_CONTACT_UNDERLINE,
            menu=self.contact_menu,
        )
        self.menubar.add_cascade(
            label=self._view_model.file_label,
            underline=MENU_FILE_UNDERLINE,
            menu=self.file_menu,
        )
        self.menubar.add_cascade(
            label=self._view_model.about_label,
            underline=MENU_ABOUT_UNDERLINE,
            menu=self.about_menu,
        )
