"""Tests of the pure parts of the screenshot tool.

@file test_capture_screenshots.py
@brief Checks platform_kind and window_box of tools/capture_screenshots.py.
"""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

pytest.importorskip("PIL")

_TOOL_PATH = Path(__file__).resolve().parents[2] / "tools" / "capture_screenshots.py"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("capture_screenshots", _TOOL_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_platform_kind_is_windows_for_win32() -> None:
    assert _load_tool().platform_kind("win32") == "windows"


def test_platform_kind_is_x11_for_linux() -> None:
    assert _load_tool().platform_kind("linux") == "x11"


def test_window_box_adds_menu_height_on_x11() -> None:
    assert _load_tool().window_box("x11", 10, 100, 900, 726, 28) == (10, 72, 910, 826)


def test_window_box_ignores_menu_height_on_windows() -> None:
    box = _load_tool().window_box("windows", 10, 100, 900, 726, 28)
    assert box == (10, 100, 910, 826)
