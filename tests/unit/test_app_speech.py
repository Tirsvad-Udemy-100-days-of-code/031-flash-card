"""Tests of the speech wiring in the entry point."""

import importlib.util
from importlib.machinery import ModuleSpec
from pathlib import Path

import pytest

from flash_card.infrastructure.speech.gtts_speech import GttsSpeech
from flash_card.infrastructure.speech.null_speech import NullSpeech
from flash_card.presentation import app


class _FakeRoot:
    def mainloop(self) -> None:
        return None


def _found(name: str) -> ModuleSpec:
    return ModuleSpec(name, None)


def test_build_speech_returns_null_speech_when_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", _found)
    assert isinstance(app.build_speech(False), NullSpeech)


def test_build_speech_returns_null_speech_when_packages_are_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda name: None)
    assert isinstance(app.build_speech(True), NullSpeech)


def test_build_speech_returns_null_speech_when_one_package_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        importlib.util,
        "find_spec",
        lambda name: None if name == "playsound" else _found(name),
    )
    assert isinstance(app.build_speech(True), NullSpeech)


def test_build_speech_returns_gtts_speech_when_both_packages_are_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", _found)
    assert isinstance(app.build_speech(True), GttsSpeech)


def test_main_passes_speech_disabled_with_no_speech_option(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    seen: list[bool] = []

    def fake_create(
        data_dir: Path | None = None, speech_enabled: bool = True
    ) -> tuple[_FakeRoot, object]:
        seen.append(speech_enabled)
        return _FakeRoot(), object()

    monkeypatch.setattr(app, "create_application", fake_create)

    assert app.main(["--data-dir", str(tmp_path), "--no-speech"]) == 0
    assert app.main(["--data-dir", str(tmp_path)]) == 0
    assert seen == [False, True]
