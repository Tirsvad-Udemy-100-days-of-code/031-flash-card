# MIL-008: Choose level

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-008 |
| CrossReference | [BC-001], [US-001], [UC-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [0b983b7] |

---

## Purpose

Decide whether the Learner can choose a level before learning: the program asks for 100 words, 1000 words or all words, and then uses the first N words of the word list, which is ordered from the most to the least frequent word.

## Deliverable

At start the window shows the choice "100 words", "1000 words" and "All words". After a choice the card window of the earlier milestones opens and every card comes from the first N words of the word list that the Learner does not yet know. Known words stay known across levels because there is still one progress file. The design documents, README, wiki (English, Danish, Bahasa Malaysia) and screenshots describe the choice.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Choosing 100 draws only cards that are among the first 100 rows of `data/ms-da.csv`, for every card of a full run through the deck | Integration test passes on the real word list | A card from row 101 or later appears |
| 2 | Choosing 1000 words or All words uses every word of the list; with a list of fewer than N words all are used | Unit and integration tests pass | Any word is missing |
| 3 | Marking words known at level 100 and then choosing All words leaves those words known, and `words_to_learn.csv` still holds every word that is not known (also those outside level 100) | Integration test passes | A word outside the level is lost from the file |
| 4 | When every word of the chosen level is known the card shows the message that nothing is left to learn, and the program does not fail | Unit and e2e tests pass | Exception or empty window |
| 5 | The level screen holds no rule: the labels and the choice come from the level view model, which imports no Tkinter | View model unit tests pass | A rule is in the view |
| 6 | `python -m flash_card --level 100` (also `1000`, `all`) skips the screen and starts at that level; an unknown value is refused by the argument parser | Unit tests pass | The screen appears or the program starts |
| 7 | The updated UC-001, DM-001, DICT-001, SSD-001, OC-001, SD-001, DCD-001, BC-001, wireframe, README and the wiki in three languages mention the level choice, and each changed document has a new Version History row and a `Go` review | Review records `Go`; `check-readme.sh` exit 0 | A document is not updated |
| 8 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest` exits with 0 and `ruff`, `mypy --strict`, `lint-imports` and `doxygen` are clean | `RC-*` verdict Go and exit codes 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-007 | The finished program, README, wiki and screenshots that this milestone extends |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 1 (learning with the word list) and success criterion 1, extended by the new request of S01 | [BC-001] |
| US-001.06 Choose my level | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-20 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Update the design documents for the level choice | Add the level to UC-001 (a first step before the cards, and the finished-level extension), to DM-001 and DICT-001 (concept Level), to SSD-001, OC-001 and SD-001 (operation chooseLevel and the level in startStudySession) and to DCD-001; draw the wireframe of the level screen in wireframe.md; add the level choice to the In Scope list of BC-001. Every changed document gets a Version History row and a new review. | No | UC-001, DCD-001 |
| 2 | Add the Level value object and the level choices | `Level` (limit as a number of words, or none for all words) in the domain and the three choices 100, 1000 and all words in constants.py with their labels, so that the choices are defined once. | No | DCD-001 |
| 3 | Draw cards from the chosen level | `StudySession` draws only from the first N words of the word list that are still to learn, and removes a known card from the whole words to learn and saves the whole deck, so that words of other levels are never lost. | Yes | US-001.06 |
| 4 | Open the session with a level | `open_study_session` gets the level, loads the word list for its order and the progress file for what is left, and builds the session; a level with nothing left gives a finished session. | Yes | US-001.06 |
| 5 | Add the level screen | `LevelViewModel` (the choices and their labels, no Tkinter) and `LevelView` in `presentation/features/level/` with the title "Choose your level" and three buttons on the window background. | Yes | US-001.06 |
| 6 | Show the level screen before the cards | The composition root shows the level screen first and builds the card view on the same window after the choice; the option `--level 100`, `--level 1000` or `--level all` skips the screen. | Yes | US-001.06 |
| 7 | Test the level choice | Unit tests of the level, the filter, the session and the view model; integration tests on the real word list and the progress file across levels; e2e test of the level screen and the flow to the first card. | No | |
| 8 | Update the README, the wiki and the screenshots | README, Usage and Home pages of the wiki in English, Danish and Bahasa Malaysia, and a new screenshot of the level screen made by tools/capture_screenshots.py; republish the wiki after the merge. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DCD-001]: ../dcd.md
[0b983b7]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0b983b7fdadf6958717c1d0227d0f2ebe037f7b1
