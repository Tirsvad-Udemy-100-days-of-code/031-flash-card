"""Entry point of the flash card program.

@file app.py
@brief Starts the program; the window arrives in MIL-002.
"""

from collections.abc import Sequence
from typing import NoReturn


def main(argv: Sequence[str] | None = None) -> int:
    """Run the program and return its exit code.

    The window arrives in MIL-002; for now nothing happens.

    @param argv Command line arguments, or None for none.
    @return The exit code, 0 on success.
    """
    return 0


def run() -> NoReturn:
    """Run the program and exit the interpreter with its exit code.

    @return Never returns; the function always raises SystemExit.
    @throws SystemExit Always, with the exit code of main.
    """
    raise SystemExit(main())
