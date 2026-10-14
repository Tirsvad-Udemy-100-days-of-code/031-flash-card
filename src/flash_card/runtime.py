"""Locate resources and the executable folder, frozen or from source.

@file runtime.py
@brief Packaging support: tells where bundled files and the executable are.
Imports only the standard library; it is not one of the layers.
"""

import sys
from pathlib import Path

## @brief Number of folders from this file up to the project root.
_ROOT_LEVELS = 2


def is_frozen() -> bool:
    """Tell whether the program runs as a PyInstaller executable.

    @return True when frozen.
    """
    return bool(getattr(sys, "frozen", False))


def source_root() -> Path:
    """Return the project root of a source run.

    @return The folder that holds src.
    """
    return Path(__file__).resolve().parents[_ROOT_LEVELS]


def pick_resource_root(frozen: bool, bundle_dir: Path | None, root: Path) -> Path:
    """Choose the folder that holds the bundled resources.

    @param frozen True when running as an executable.
    @param bundle_dir The unpack folder of the executable, when frozen.
    @param root The project root of a source run.
    @return The bundle folder when frozen and known, else the project root.
    """
    if frozen and bundle_dir is not None:
        return bundle_dir
    return root


def pick_executable_dir(frozen: bool, executable: Path, root: Path) -> Path:
    """Choose the folder next to the executable.

    @param frozen True when running as an executable.
    @param executable Path of the running executable.
    @param root The project root of a source run.
    @return The folder of the executable when frozen, else the project root.
    """
    if frozen:
        return executable.parent
    return root


def resource_root() -> Path:
    """Return the folder that holds the bundled resources.

    @return The PyInstaller unpack folder when frozen, else the project root.
    """
    bundle = getattr(sys, "_MEIPASS", None)
    bundle_dir = Path(bundle) if bundle else None
    return pick_resource_root(is_frozen(), bundle_dir, source_root())


def executable_dir() -> Path:
    """Return the folder of the running executable.

    @return The folder of the executable when frozen, else the project root.
    """
    return pick_executable_dir(is_frozen(), Path(sys.executable), source_root())
