"""Tests of the runtime helpers.

@file test_runtime.py
@brief Checks where resources and the executable are, frozen or from source.
"""

from pathlib import Path

from flash_card import runtime

BUNDLE = Path("bundle")
EXECUTABLE = Path("apps") / "flash-card.exe"
ROOT = Path("project")


def test_pick_resource_root_returns_bundle_when_frozen() -> None:
    assert runtime.pick_resource_root(True, BUNDLE, ROOT) == BUNDLE


def test_pick_resource_root_returns_root_when_not_frozen() -> None:
    assert runtime.pick_resource_root(False, BUNDLE, ROOT) == ROOT


def test_pick_resource_root_returns_root_when_bundle_is_unknown() -> None:
    assert runtime.pick_resource_root(True, None, ROOT) == ROOT


def test_pick_executable_dir_returns_executable_folder_when_frozen() -> None:
    assert runtime.pick_executable_dir(True, EXECUTABLE, ROOT) == EXECUTABLE.parent


def test_pick_executable_dir_returns_root_when_not_frozen() -> None:
    assert runtime.pick_executable_dir(False, EXECUTABLE, ROOT) == ROOT


def test_is_frozen_is_false_in_a_test_run() -> None:
    assert runtime.is_frozen() is False


def test_resource_root_is_project_root_in_a_source_run() -> None:
    assert (runtime.resource_root() / "pyproject.toml").is_file()


def test_executable_dir_is_project_root_in_a_source_run() -> None:
    assert runtime.executable_dir() == runtime.source_root()
