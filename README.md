# 🚀 Flash Card

A flash card program for learning the most frequent Malay words with their Danish translations. It is the solution of day 31 of Udemy's *100 Days of Code: The Complete Python Pro Bootcamp*, written for course participants who want to compare solutions and for visitors who browse the repository for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

The program first asks for a level: the first 100 words, the first 1000 words or all words of the word list, which is ordered from the most to the least frequent word. Then it shows a Malay word on a card. After three seconds the card turns over and shows the Danish translation. You press the green tick when you know the word and the red cross when you do not. A known word is removed from the words to learn, and the words still to learn are saved, so the next start continues where you stopped.

| Part | What it is for |
| --- | --- |
| `src/flash_card/` | The program, in four layers: `domain`, `application`, `infrastructure`, `presentation` |
| `tests/` | `pytest` tests: `unit`, `integration`, `e2e` |
| `data/` | The word list `ms-da.csv` and, after the first known word, your own `words_to_learn.csv` |
| `docs/` | Project documents (business case, plan, design, review records), `docs/wiki/` and `docs/images/` |
| `tools/` | Helper scripts: `generate_images.py`, `capture_screenshots.py` and `build_executable.py` |
| `Doxyfile` | Doxygen configuration for the source code documentation |

The core program uses only the Python standard library. Spoken Malay words are an optional extra.

### Screenshots

| Choose your level | Front: the Malay word | Back: the Danish translation after 3 seconds |
| --- | --- | --- |
| ![The level screen][screenshot-level] | ![The front of a card][screenshot-front] | ![The back of a card][screenshot-back] |

### Where is each assignment step?

| Assignment step | Code |
| --- | --- |
| 1. User interface | `FlashCardView.__init__` in `src/flash_card/presentation/features/flash_card/flash_card_view.py`; images made by `tools/generate_images.py` |
| 2. New flash cards | `CsvVocabularyRepository` (the standard library `csv` instead of `pandas`), `Deck.draw`, `StudySession.next_card`, `FlashCardView.next_card` |
| 3. Flip the cards | `FlashCardView.flip_card` and `FlashCardView.flip_timer` (`after`, `after_cancel`), `FlashCardViewModel.flip_card` |
| 4. Save your progress | `FlashCardView.is_known`, `StudySession.mark_known`, `CsvProgressRepository` |
| Extra: level choice | `LevelView`, `LevelViewModel`, `Level`, `Deck.within`, `StudySession.next_card`, `open_study_session` |
| Extra: spoken word | `GttsSpeech`, `NullSpeech`, `build_speech` in `presentation/app.py` |

The wiki ([English][wiki-en], [Dansk][wiki-da], [Bahasa Malaysia][wiki-ms]) explains the same in three languages.

### Data

`data/ms-da.csv` holds 1000 frequent Malay words with a Danish machine translation; see [data/README.md][data-readme] for the format and origin.

## 📋 Requirements

| Need | Why |
| --- | --- |
| Python 3.13 or later, with Tkinter | The program and its window (Tkinter is part of the standard Python installers for Windows and macOS; on Debian or Ubuntu install `python3-tk`) |
| `git` | To clone the repository |
| Doxygen (optional) | To build the source code documentation |
| `pyinstaller` (optional, extra `build`) | To build a single executable file (see Run) |
| `gTTS` and `playsound==1.2.2` (optional, extra `speech`) | To hear the Malay word; needs a network connection |

## 🛠️ Setup

Create a virtual environment in `.venv`, activate it, upgrade pip and install the project. Run the commands in the repository folder.

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

- Use `python -m pip install -e .` if you only want to run the program; the `dev` extra adds `pytest`, `ruff`, `mypy` and `import-linter`.
- Add the spoken word with `python -m pip install -e ".[speech]"`.
- If PowerShell refuses to run `Activate.ps1`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use `.\.venv\Scripts\activate.bat` in `cmd`.
- Leave the environment with `deactivate`. Delete the `.venv` folder to start over.

## ▶️ Run

```bash
python -m flash_card
```

The program is run from the activated `.venv`. The window opens with the level screen: choose 100 words, 1000 words or All words. Then a card appears. Press the green tick for a word you know and the red cross for a word you do not. Options:

| Option | Meaning |
| --- | --- |
| `--data-dir <folder>` | Folder with `ms-da.csv` and `words_to_learn.csv` |
| `--level {100,1000,all}` | Start at that level and skip the level screen |
| `--no-speech` | Do not speak the Malay word |

Known words stay known at every level: the level only limits which of the words you do not know yet come up. To start again, delete `data/words_to_learn.csv`.

### Executable (Windows, no Python needed to run it)

The [release page][release-0-1-0] of v0.1.0 has the release notes. The executable is not attached there yet, because the server's upload limit rejects a file of this size (HTTP 413). Build it yourself:

```powershell
python -m pip install -e ".[build,speech]"
python tools/build_executable.py
```

The script builds `dist/flash-card.exe`: one file, no console window, with the images, the word list and the spoken word inside. Open it by double-clicking. It keeps your progress in a `data/` folder next to the executable (`data/words_to_learn.csv`); a `data/ms-da.csv` next to it replaces the word list inside. Add `--no-speech` to the build script to leave the speech packages out. The executable is a build output and is not committed; build it on the system you want to run it on (Windows, Linux or macOS).

## 🧪 Tests

```bash
python -m pytest
```

Quality checks used by the project:

```bash
python -m ruff check src tests
python -m mypy
lint-imports
```

The window test in `tests/e2e/` is skipped when no display is available.

Build the source code documentation (Doxygen comments) with `doxygen Doxyfile`; the HTML is written to `docs/doxygen/html/`. The screenshots are made with `python tools/capture_screenshots.py` after `python -m pip install -e ".[tools]"` (Pillow, tool only).

## 📄 License

GNU Affero General Public License v3.0 or later. See [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]
- [Releases][releases] (v0.1.0: release notes; the executable is built from source, see Run)

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [AGENTS.md][agents] | The rules AI agents follow in this repository |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Domain dictionary][DICT-001] | The PO terms and the IT terms |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[license]: ./LICENSE
[screenshot-level]: ./docs/images/screenshot-level.png
[screenshot-front]: ./docs/images/screenshot-front.png
[screenshot-back]: ./docs/images/screenshot-back.png
[wiki-en]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/wiki/Home
[wiki-da]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/wiki/Home-da
[wiki-ms]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/wiki/Home-ms
[data-readme]: ./data/README.md
[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/issues
[releases]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases
[release-0-1-0]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.1.0
[agents]: ./AGENTS.md
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[DICT-001]: ./docs/dictionary.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
