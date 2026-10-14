"""Fixtures shared by the end-to-end tests."""

import tkinter as tk
from collections.abc import Iterator

import pytest


@pytest.fixture(scope="session")
def tk_root() -> Iterator[tk.Tk]:
    """The one Tk root of the process, shared by every e2e module.

    A second interpreter right after destroying the first fails to find
    init.tcl on some Windows Python installs, so there is only one. Each test
    builds its views on it and destroys their widgets afterwards.
    """
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    yield root
    root.destroy()
