"""Silent speech adapter.

@file null_speech.py
@brief NullSpeech, the SpeechPort used when speech is off or unavailable.
"""


class NullSpeech:
    """Speaks nothing."""

    def speak(self, text: str, language_code: str) -> None:
        """Do nothing.

        @param text The text, ignored.
        @param language_code The language, ignored.
        @return Nothing.
        """
        return None
