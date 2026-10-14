"""Tests of the GttsSpeech adapter with fake synthesizer and player."""

import threading
from pathlib import Path

import pytest

from flash_card.infrastructure.speech import gtts_speech
from flash_card.infrastructure.speech.gtts_speech import GttsSpeech


class _Recorder:
    def __init__(self) -> None:
        self.synthesized: list[tuple[str, str]] = []
        self.played: list[Path] = []
        self.existed_when_played = False

    def synthesize(self, text: str, language_code: str, path: Path) -> None:
        self.synthesized.append((text, language_code))
        path.write_bytes(b"mp3")

    def play(self, path: Path) -> None:
        self.played.append(path)
        self.existed_when_played = path.exists()


def test_speak_synthesizes_and_plays_then_removes_file() -> None:
    recorder = _Recorder()
    speech = GttsSpeech(recorder.synthesize, recorder.play)

    speech.speak("aku", "ms")
    speech.wait()

    assert recorder.synthesized == [("aku", "ms")]
    assert len(recorder.played) == 1
    assert recorder.existed_when_played
    assert not recorder.played[0].exists()


def test_speak_returns_before_player_has_finished() -> None:
    started = threading.Event()
    release = threading.Event()

    def blocked_play(path: Path) -> None:
        started.set()
        release.wait(timeout=5)

    speech = GttsSpeech(lambda text, code, path: None, blocked_play)

    speech.speak("aku", "ms")

    assert started.wait(timeout=5)
    assert speech._thread is not None
    assert speech._thread.is_alive()
    release.set()
    speech.wait()


def test_speak_logs_and_does_not_raise_when_synthesize_fails(
    caplog: pytest.LogCaptureFixture,
) -> None:
    played: list[Path] = []

    def failing(text: str, language_code: str, path: Path) -> None:
        raise OSError("no network")

    speech = GttsSpeech(failing, played.append)

    speech.speak("aku", "ms")
    speech.wait()

    assert played == []
    assert "Speech failed" in caplog.text
    assert "no network" in caplog.text


def test_speak_logs_and_does_not_raise_when_play_fails(
    caplog: pytest.LogCaptureFixture,
) -> None:
    def failing(path: Path) -> None:
        raise RuntimeError("no audio device")

    speech = GttsSpeech(lambda text, code, path: None, failing)

    speech.speak("aku", "ms")
    speech.wait()

    assert "no audio device" in caplog.text


def test_speak_logs_missing_package_when_default_synthesizer_raises_import_error(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def missing(name: str) -> object:
        raise ImportError(f"No module named {name!r}")

    monkeypatch.setattr(gtts_speech.importlib, "import_module", missing)
    speech = GttsSpeech()

    speech.speak("aku", "ms")
    speech.wait()

    assert "No module named 'gtts'" in caplog.text


def test_wait_returns_when_nothing_was_spoken() -> None:
    GttsSpeech().wait()
