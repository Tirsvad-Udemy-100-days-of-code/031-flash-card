"""Name of the words to learn file of a word list.

@file progress_file_name.py
@brief Keeps the progress of every word list in a file of its own.
"""

import re
from pathlib import Path

from flash_card.constants import (
    PROGRESS_FILE_NAME,
    PROGRESS_FILE_NAME_TEMPLATE,
    PROGRESS_STEM_FORBIDDEN,
    PROGRESS_STEM_REPLACEMENT,
    VOCABULARY_FILE_NAME,
)


def progress_file_name(list_path: Path) -> str:
    """Name the words to learn file of a word list.

    @param list_path Path of the word list file.
    @return The default file name for the delivered list, else a name made of
        the list's file name stem with other characters than letters, digits,
        hyphen and underscore replaced by an underscore.
    """
    if list_path.name == VOCABULARY_FILE_NAME:
        return PROGRESS_FILE_NAME
    stem = re.sub(PROGRESS_STEM_FORBIDDEN, PROGRESS_STEM_REPLACEMENT, list_path.stem)
    return PROGRESS_FILE_NAME_TEMPLATE.format(stem=stem)
