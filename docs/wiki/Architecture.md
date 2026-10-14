# Architecture

🌐 **English** · [Dansk](Architecture-da) · [Bahasa Malaysia](Architecture-ms)

The program is built in four layers under `src/flash_card/`. Imports point inward; `lint-imports` checks this.

| Layer | Holds | May import |
| --- | --- | --- |
| `domain` | `Card`, `LanguagePair`, `Vocabulary`, `Deck`, the errors and the repository interfaces | nothing |
| `application` | `StudySession`, `open_study_session`, `CardDto` and `SpeechPort` | `domain` |
| `infrastructure` | The CSV repositories and the speech adapters | `application`, `domain` |
| `presentation` | `FlashCardView`, `FlashCardViewModel` (MVVM) and the composition root `app.py` | all layers |

All constants are in `src/flash_card/constants.py`.

## Where is each assignment step?

| Assignment | Code |
| --- | --- |
| Step 1: window, canvas, image, texts, buttons | `FlashCardView.__init__` in `presentation/features/flash_card/flash_card_view.py`; images made by `tools/generate_images.py` |
| Step 2: read the CSV, random word on each press | `CsvVocabularyRepository` and `read_word_list` (replace `pandas`), `Deck.draw`, `StudySession.next_card`, `FlashCardView.next_card` |
| Step 3: flip after 3 seconds | `FlashCardView.flip_card`, `FlashCardView.flip_timer` (`after`, `after_cancel`), `FlashCardViewModel.flip_card` |
| Step 4: known words, `words_to_learn.csv` | `FlashCardView.is_known`, `StudySession.mark_known`, `CsvProgressRepository`, `open_study_session` |
| Extra: speech | `SpeechPort`, `GttsSpeech`, `NullSpeech`, `build_speech` in `presentation/app.py` |

## Why a layered program for a small assignment?

The rules (which card comes next, what a known word does) are tested without a window or a file system. The window, the CSV files and the speech service can be replaced without touching the rules. See ADR-0001 and ADR-0002 in `docs/adr/`.

## Tests

| Folder | What it tests |
| --- | --- |
| `tests/unit/` | Each layer alone, with fakes for the ports |
| `tests/integration/` | The real word list and the progress file in a temporary folder |
| `tests/e2e/` | The real Tkinter window (skipped when no display exists) |

## Project documents

The business case, plan, design and review records are in `docs/`. The work was done in seven milestones, one pull request each: see `docs/milestones/`.
