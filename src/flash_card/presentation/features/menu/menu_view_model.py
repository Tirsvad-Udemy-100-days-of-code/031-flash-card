"""View model of the menu bar.

@file menu_view_model.py
@brief Exposes the labels, the order and the contact data; free of Tkinter.
"""

from dataclasses import dataclass

from flash_card.constants import (
    CONTACT_LABEL_TEMPLATE,
    CONTACT_NAME,
    CONTACT_TITLE,
    CONTACT_URL,
    MENU_ABOUT_LABEL,
    MENU_CHANGE_LEVEL_LABEL,
    MENU_CHANGE_LEVEL_UNDERLINE,
    MENU_COMMAND_CHANGE_LEVEL,
    MENU_COMMAND_EXIT,
    MENU_COMMAND_OPEN,
    MENU_COMMAND_RESET,
    MENU_CONTACT_LABEL,
    MENU_EXIT_LABEL,
    MENU_EXIT_UNDERLINE,
    MENU_FILE_LABEL,
    MENU_OPEN_LABEL,
    MENU_OPEN_UNDERLINE,
    MENU_RESET_LABEL,
    MENU_RESET_UNDERLINE,
)


@dataclass(frozen=True, slots=True)
class MenuEntry:
    """One entry of the File menu."""

    ## @brief Text of the entry.
    label: str
    ## @brief Name of the command of the menu view the entry runs.
    command: str
    ## @brief Index of the mnemonic letter in the label.
    underline: int


class MenuViewModel:
    """Data the menu view shows."""

    @property
    def file_label(self) -> str:
        """Return the label of the File menu.

        @return The label.
        """
        return MENU_FILE_LABEL

    @property
    def file_entries(self) -> tuple[MenuEntry, ...]:
        """Return the entries of the File menu.

        @return Open, Change level, Reset word list and Exit, in this order.
        """
        return (
            MenuEntry(MENU_OPEN_LABEL, MENU_COMMAND_OPEN, MENU_OPEN_UNDERLINE),
            MenuEntry(
                MENU_CHANGE_LEVEL_LABEL,
                MENU_COMMAND_CHANGE_LEVEL,
                MENU_CHANGE_LEVEL_UNDERLINE,
            ),
            MenuEntry(MENU_RESET_LABEL, MENU_COMMAND_RESET, MENU_RESET_UNDERLINE),
            MenuEntry(MENU_EXIT_LABEL, MENU_COMMAND_EXIT, MENU_EXIT_UNDERLINE),
        )

    @property
    def about_label(self) -> str:
        """Return the label of the About menu.

        @return The label.
        """
        return MENU_ABOUT_LABEL

    @property
    def contact_menu_label(self) -> str:
        """Return the label of the Contact submenu.

        @return The label.
        """
        return MENU_CONTACT_LABEL

    @property
    def contact_label(self) -> str:
        """Return the text of the contact entry.

        @return The name and the title of the author.
        """
        return CONTACT_LABEL_TEMPLATE.format(name=CONTACT_NAME, title=CONTACT_TITLE)

    @property
    def contact_url(self) -> str:
        """Return the address the contact entry opens.

        @return The LinkedIn page of the author.
        """
        return CONTACT_URL
