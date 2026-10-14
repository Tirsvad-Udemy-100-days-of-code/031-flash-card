"""Tests of the entry point.

@file test_app.py
@brief Checks main of flash_card.presentation.app.
"""

from flash_card.presentation.app import main


def test_main_returns_zero_without_arguments() -> None:
    assert main([]) == 0
