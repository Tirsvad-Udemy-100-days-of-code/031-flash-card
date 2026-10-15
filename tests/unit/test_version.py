"""Keep the version declared in code, pyproject.toml and the Doxyfile in step.

@file test_version.py
@brief Unit tests that the three version declarations cannot drift.
"""

import re
import tomllib

import flash_card
from flash_card.constants import PROJECT_ROOT

_SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
_PROJECT_NUMBER_PATTERN = re.compile(r"^PROJECT_NUMBER\s*=\s*(\S+)\s*$", re.MULTILINE)


def _pyproject_version() -> str:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as file:
        version: str = tomllib.load(file)["project"]["version"]
    return version


def test_version_matches_package_version_when_read_from_pyproject() -> None:
    assert _pyproject_version() == flash_card.__version__


def test_version_has_major_minor_patch_form() -> None:
    assert _SEMVER_PATTERN.match(flash_card.__version__) is not None


def test_version_matches_doxyfile_project_number() -> None:
    text = (PROJECT_ROOT / "Doxyfile").read_text(encoding="utf-8")
    match = _PROJECT_NUMBER_PATTERN.search(text)
    assert match is not None
    assert match.group(1) == flash_card.__version__
