# MIL-003: Step 2 - New flash cards

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001], [US-001], [UC-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decide whether assignment step 2 works: the word list is read from `data/ms-da.csv` and each press of a button shows a new random card.

## Deliverable

The program reads the word list and shows a random Malay word with the language name "Malay". Pressing the known or the unknown button shows another random word. The domain classes, the CSV reader and the use case that draws cards exist with tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `CsvVocabularyRepository` reads `data/ms-da.csv` into 1000 cards with the language pair `ms`, `da` | Integration test passes on the real file | Any other count or pair |
| 2 | A file with a missing header, a row with other than two cells, or no file raises a specific `VocabularyError` subclass | Unit tests pass | An unspecific exception or a silent skip |
| 3 | A button press shows a card different from the current one when the deck has two or more cards, and the same card when it has one | Unit tests pass | Any other behaviour |
| 4 | Blank lines in the CSV file are ignored | Unit test passes | A blank line becomes a card |
| 5 | The domain and application layers import no `tkinter`, `csv` or `random` module; randomness comes in through the injected `choose` function | `grep` check in the review record | An outward import |
| 6 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest` exits with 0 | `RC-*` verdict Go and exit code 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-002 | The window and view model this step feeds with data |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 1, step 2; objective 2 (Malay to Danish list) | [BC-001] |
| US-001.02 Get a new card | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-16 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add the domain classes | `Card`, `LanguagePair`, `Vocabulary` (frozen dataclasses), `Deck` (draw, remove) and the errors `VocabularyError`, `VocabularyFormatError`, `VocabularyNotFoundError`, `EmptyDeckError`, with the `VocabularyRepository` port. | No | DCD-001 |
| 2 | Read the word list from CSV | `CsvVocabularyRepository` reads a semicolon separated file with a two-code header using `csv`, `pathlib` and UTF-8, and ignores blank lines; this replaces `pandas` from the assignment (ADR-0001). | No | ADR-0001, DCD-001 |
| 3 | Draw a random card | `StudySession.next_card` returns a `CardDto` chosen at random from the deck and not equal to the current card when other cards exist; `open_study_session` builds the session from the repository. | Yes | US-001.02 |
| 4 | Show a new card on each button press | `FlashCardViewModel` and `FlashCardView` get `next_card`; both buttons call it so that the card changes, as in the assignment. | Yes | US-001.02 |
| 5 | Test the reader, the deck and the session | Unit tests for the domain and the session (with an injected `choose`), integration test of the reader on the real word list, and a view model test. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DCD-001]: ../dcd.md
