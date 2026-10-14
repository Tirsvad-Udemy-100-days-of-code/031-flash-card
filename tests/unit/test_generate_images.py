"""Tests of the image generator tool.

@file test_generate_images.py
@brief Checks the PNG files written by tools/generate_images.py.
"""

import importlib.util
import struct
from pathlib import Path
from types import ModuleType

import pytest

from flash_card.constants import (
    CARD_BACK_IMAGE_NAME,
    CARD_FRONT_IMAGE_NAME,
    CARD_HEIGHT,
    CARD_WIDTH,
    RIGHT_IMAGE_NAME,
    WRONG_IMAGE_NAME,
)

_TOOL_PATH = Path(__file__).resolve().parents[2] / "tools" / "generate_images.py"
_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("generate_images", _TOOL_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def generated(tmp_path_factory: pytest.TempPathFactory) -> Path:
    output_dir = tmp_path_factory.mktemp("assets")
    assert _load_tool().main(["--output-dir", str(output_dir)]) == 0
    return output_dir


@pytest.mark.parametrize(
    ("name", "width", "height"),
    [
        (CARD_FRONT_IMAGE_NAME, CARD_WIDTH, CARD_HEIGHT),
        (CARD_BACK_IMAGE_NAME, CARD_WIDTH, CARD_HEIGHT),
        (RIGHT_IMAGE_NAME, 100, 100),
        (WRONG_IMAGE_NAME, 100, 100),
    ],
)
def test_generate_images_writes_png_with_expected_size(
    generated: Path, name: str, width: int, height: int
) -> None:
    data = (generated / name).read_bytes()
    assert data.startswith(_SIGNATURE)
    assert data[12:16] == b"IHDR"
    assert struct.unpack(">II", data[16:24]) == (width, height)
