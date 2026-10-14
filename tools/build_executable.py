"""Build the single file Windows executable with PyInstaller.

@file build_executable.py
@brief Runs PyInstaller with the arguments of the flash card program.
Uses the standard library; PyInstaller is imported only when a build runs.
"""

import argparse
import importlib
import os
import sys
from collections.abc import Sequence
from pathlib import Path

_SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from flash_card.constants import (  # noqa: E402
    EXECUTABLE_NAME,
    ICON_FILE_NAME,
    VOCABULARY_FILE_NAME,
)

_ASSETS_RELATIVE = Path("src") / "flash_card" / "presentation" / "assets"
_ASSETS_TARGET = "flash_card/presentation/assets"
_DATA_RELATIVE = Path("data")
_SPEECH_PACKAGES = ("gtts", "playsound")
_INSTALL_HINT = 'python -m pip install -e ".[build]"'
_EXIT_MISSING_PYINSTALLER = 2


def _add_data(source: Path, target: str) -> list[str]:
    """Return the --add-data option of one source and target.

    @param source File or folder to bundle.
    @param target Folder inside the bundle.
    @return The option and its value.
    """
    return ["--add-data", f"{source}{os.pathsep}{target}"]


def build_arguments(
    root: Path, *, speech: bool = True, clean: bool = False
) -> list[str]:
    """Return the PyInstaller argument list.

    @param root Project root folder.
    @param speech True to bundle the optional gtts and playsound packages.
    @param clean True to clear the PyInstaller cache first.
    @return The arguments, the entry script last.
    """
    arguments = [
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--name",
        EXECUTABLE_NAME,
        "--icon",
        str(root / _ASSETS_RELATIVE / ICON_FILE_NAME),
        "--paths",
        str(root / "src"),
        "--distpath",
        str(root / "dist"),
        "--workpath",
        str(root / "build"),
        "--specpath",
        str(root / "build"),
    ]
    arguments += _add_data(root / _ASSETS_RELATIVE, _ASSETS_TARGET)
    arguments += _add_data(root / _DATA_RELATIVE / VOCABULARY_FILE_NAME, "data")
    if speech:
        for package in _SPEECH_PACKAGES:
            arguments += ["--hidden-import", package, "--collect-all", package]
    if clean:
        arguments.append("--clean")
    arguments.append(str(root / "src" / "flash_card" / "__main__.py"))
    return arguments


def main(argv: Sequence[str] | None = None) -> int:
    """Build the executable from the command line.

    @param argv Command line arguments, or None for sys.argv.
    @return 0 on success, 2 when PyInstaller is not installed.
    """
    parser = argparse.ArgumentParser(description="Build the flash card executable.")
    parser.add_argument(
        "--no-speech", action="store_true", help="leave out gtts and playsound"
    )
    parser.add_argument("--clean", action="store_true", help="clear the cache first")
    args = parser.parse_args(argv)
    try:
        pyinstaller = importlib.import_module("PyInstaller.__main__")
    except ImportError:
        sys.stderr.write(
            f"PyInstaller is not installed; run {_INSTALL_HINT} and try again\n"
        )
        return _EXIT_MISSING_PYINSTALLER
    root = Path(__file__).resolve().parents[1]
    pyinstaller.run(build_arguments(root, speech=not args.no_speech, clean=args.clean))
    sys.stdout.write(f"built {root / 'dist' / (EXECUTABLE_NAME + '.exe')}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
