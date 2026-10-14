"""Tests of the NullSpeech adapter."""

from flash_card.infrastructure.speech.null_speech import NullSpeech


def test_speak_does_nothing_and_returns_none() -> None:
    assert NullSpeech().speak("aku", "ms") is None
