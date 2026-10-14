"""Port for spoken words.

@file speech_port.py
@brief The SpeechPort interface the study session uses to say a word aloud.
"""

from typing import Protocol


class SpeechPort(Protocol):
    """Speaks a text aloud in a language."""

    def speak(self, text: str, language_code: str) -> None:
        """Speak a text without blocking the caller for long.

        An implementation does not raise: a failure is logged and ignored.

        @param text The text to speak.
        @param language_code Language of the text, for example "ms".
        @return Nothing.
        """
        ...
