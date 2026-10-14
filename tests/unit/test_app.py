"""Tests of the entry point.

@file test_app.py
@brief Checks main of flash_card.presentation.app without opening a window.
"""

import pytest

from flash_card.presentation import app


class _FakeRoot:
    def __init__(self) -> None:
        self.mainloop_calls = 0

    def mainloop(self) -> None:
        self.mainloop_calls += 1


def test_main_runs_main_loop_and_returns_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = _FakeRoot()
    monkeypatch.setattr(app, "create_application", lambda: (root, object()))

    assert app.main([]) == 0
    assert root.mainloop_calls == 1
