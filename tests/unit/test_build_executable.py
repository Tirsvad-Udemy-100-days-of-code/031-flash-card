"""Tests of the executable build tool.

@file test_build_executable.py
@brief Checks the PyInstaller arguments and the missing PyInstaller message.
"""

import importlib
import importlib.util
import os
from pathlib import Path
from types import ModuleType

import pytest

from flash_card.constants import EXECUTABLE_NAME, ICON_FILE_NAME

_TOOL_PATH = Path(__file__).resolve().parents[2] / "tools" / "build_executable.py"
ROOT = Path("project")
ASSETS = ROOT / "src" / "flash_card" / "presentation" / "assets"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_executable", _TOOL_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _option(arguments: list[str], name: str) -> str:
    return arguments[arguments.index(name) + 1]


def test_build_arguments_start_with_the_packaging_flags() -> None:
    arguments = _load_tool().build_arguments(ROOT)
    assert arguments[:3] == ["--onefile", "--windowed", "--noconfirm"]


def test_build_arguments_name_icon_and_folders() -> None:
    arguments = _load_tool().build_arguments(ROOT)
    assert _option(arguments, "--name") == EXECUTABLE_NAME == "flash-card"
    assert _option(arguments, "--icon") == str(ASSETS / ICON_FILE_NAME)
    assert _option(arguments, "--paths") == str(ROOT / "src")
    assert _option(arguments, "--distpath") == str(ROOT / "dist")
    assert _option(arguments, "--workpath") == str(ROOT / "build")
    assert _option(arguments, "--specpath") == str(ROOT / "build")


def test_build_arguments_add_assets_and_word_list() -> None:
    arguments = _load_tool().build_arguments(ROOT)
    pairs = [
        arguments[i + 1] for i, value in enumerate(arguments) if value == "--add-data"
    ]
    assert pairs == [
        f"{ASSETS}{os.pathsep}flash_card/presentation/assets",
        f"{ROOT / 'data' / 'ms-da.csv'}{os.pathsep}data",
    ]


def test_build_arguments_end_with_the_entry_script() -> None:
    arguments = _load_tool().build_arguments(ROOT, clean=True)
    assert arguments[-1] == str(ROOT / "src" / "flash_card" / "__main__.py")


def test_build_arguments_include_speech_packages_by_default() -> None:
    arguments = _load_tool().build_arguments(ROOT)
    assert arguments.count("--collect-all") == 2
    assert "gtts" in arguments
    assert "playsound" in arguments


def test_build_arguments_leave_out_speech_packages_without_speech() -> None:
    arguments = _load_tool().build_arguments(ROOT, speech=False)
    assert "--collect-all" not in arguments
    assert "--hidden-import" not in arguments


def test_build_arguments_clean_only_when_asked() -> None:
    tool = _load_tool()
    assert "--clean" not in tool.build_arguments(ROOT)
    assert "--clean" in tool.build_arguments(ROOT, clean=True)


def test_main_returns_two_and_explains_when_pyinstaller_is_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refuse(name: str, package: str | None = None) -> ModuleType:
        raise ImportError(name)

    tool = _load_tool()
    monkeypatch.setattr(importlib, "import_module", refuse)
    assert tool.main([]) == 2
    assert 'pip install -e ".[build]"' in capsys.readouterr().err
