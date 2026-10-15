# Changelog

All notable changes of the flash card program. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the version follows
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-15

First release. The solution of day 31 of Udemy's *100 Days of Code: The Complete
Python Pro Bootcamp*, for Malay words with Danish translations.

### Added

- The four assignment steps: the window with a card and two buttons, a random
  card on every press, the flip to the translation after 3 seconds, and the
  progress file `data/words_to_learn.csv`.
- A choice of level before learning: the first 100 words, the first 1000 words
  or all words of the frequency ordered word list; `--level 100|1000|all`.
- The spoken Malay word through the optional extra `speech` (gTTS and
  playsound); `--no-speech`.
- A single Windows executable built with PyInstaller (`python
  tools/build_executable.py`); the progress is kept in a `data/` folder next to
  it, and a `data/ms-da.csv` next to it replaces the word list inside it.
- README, a wiki in English, Danish and Bahasa Malaysia, and Doxygen comments.

### Known limits

- The executable is not signed; Windows SmartScreen may warn about it.
- The executable is not attached to the release: the upload limit of the server rejects a file of its size. Build it with `python tools/build_executable.py`.
- The executable is built for Windows (x64); on Linux and macOS run the program
  from source or build it on that system.
- The Danish column of the word list is machine translated.

[0.1.0]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.1.0
