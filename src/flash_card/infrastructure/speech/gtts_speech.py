"""Speech adapter over the gTTS service.

@file gtts_speech.py
@brief GttsSpeech, the SpeechPort that synthesises with gTTS and plays the file.
The packages gtts and playsound are optional and imported only when used.
"""

import importlib
import logging
import tempfile
import threading
from collections.abc import Callable
from pathlib import Path

## @brief Logger of the speech adapter.
_logger = logging.getLogger(__name__)

## @brief File name of the synthesised speech inside the temporary folder.
_SPEECH_FILE_NAME = "speech.mp3"

## @brief Writes an mp3 of a text and language to a path.
Synthesize = Callable[[str, str, Path], None]
## @brief Plays an audio file.
Play = Callable[[Path], None]


def _default_synthesize(text: str, language_code: str, path: Path) -> None:
    """Write an mp3 of the text with gTTS.

    @param text The text to speak.
    @param language_code Language of the text.
    @param path File to write.
    @return Nothing.
    @throws ImportError When the gtts package is not installed.
    """
    # Imported by name so the program starts without the optional extra.
    module = importlib.import_module("gtts")
    module.gTTS(text=text, lang=language_code).save(str(path))


def _default_play(path: Path) -> None:
    """Play an audio file and wait until it has been played.

    @param path File to play.
    @return Nothing.
    @throws ImportError When the playsound package is not installed.
    """
    # Imported by name so the program starts without the optional extra.
    module = importlib.import_module("playsound")
    module.playsound(str(path))


class GttsSpeech:
    """Speaks a text in a background thread; never raises."""

    def __init__(
        self,
        synthesize: Synthesize | None = None,
        play: Play | None = None,
    ) -> None:
        """Create the adapter.

        @param synthesize Writes an mp3 of a text and language to a path, or
            None for gTTS.
        @param play Plays an audio file, or None for playsound.
        """
        ## @brief Writes the audio file.
        self._synthesize = _default_synthesize if synthesize is None else synthesize
        ## @brief Plays the audio file.
        self._play = _default_play if play is None else play
        ## @brief The thread of the latest speak call, or None.
        self._thread: threading.Thread | None = None

    def speak(self, text: str, language_code: str) -> None:
        """Start speaking and return at once.

        @param text The text to speak.
        @param language_code Language of the text.
        @return Nothing.
        """
        thread = threading.Thread(
            target=self._run, args=(text, language_code), daemon=True
        )
        self._thread = thread
        thread.start()

    def wait(self) -> None:
        """Block until the latest speech has ended.

        @return Nothing.
        """
        if self._thread is not None:
            self._thread.join()

    def _run(self, text: str, language_code: str) -> None:
        """Synthesise and play in a temporary folder, then remove the file.

        @param text The text to speak.
        @param language_code Language of the text.
        @return Nothing.
        """
        try:
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / _SPEECH_FILE_NAME
                self._synthesize(text, language_code, path)
                self._play(path)
        except Exception:  # thread boundary: speech must never crash the program
            _logger.warning("Speech failed for %r", text, exc_info=True)
