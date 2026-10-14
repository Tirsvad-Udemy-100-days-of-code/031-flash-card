"""Tests of the entry point.

@file test_app.py
@brief Checks main of flash_card.presentation.app without opening a window.
"""

from pathlib import Path

import pytest

from flash_card.presentation import app


class _FakeRoot:
    def __init__(self) -> None:
        self.mainloop_calls = 0

    def mainloop(self) -> None:
        self.mainloop_calls += 1


def test_main_runs_main_loop_and_returns_zero(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _FakeRoot()
    seen: list[Path | None] = []

    def fake_create(
        data_dir: Path | None = None, speech_enabled: bool = True
    ) -> tuple[_FakeRoot, object]:
        seen.append(data_dir)
        return root, object()

    monkeypatch.setattr(app, "create_application", fake_create)

    assert app.main(["--data-dir", str(tmp_path)]) == 0
    assert root.mainloop_calls == 1
    assert seen == [tmp_path]


def test_main_returns_one_when_word_list_is_missing(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    assert app.main(["--data-dir", str(tmp_path / "nowhere")]) == 1
    assert "word list not found" in caplog.text
