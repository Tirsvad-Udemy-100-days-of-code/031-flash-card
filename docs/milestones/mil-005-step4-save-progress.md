# MIL-005: Step 4 - Save progress

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001], [US-001], [UC-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decide whether assignment step 4 works: a known word stops coming up, and the words still to learn are kept in `words_to_learn.csv` and used on the next start.

## Deliverable

Pressing the known button removes the current card from the words to learn and saves them to `data/words_to_learn.csv`. A start with that file uses it; a start without it uses `data/ms-da.csv`. When no word is left the card shows "Nothing left to learn".

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | With the 3 word example of the assignment, marking the second known leaves the other two in the saved file, in order, with the original header | Integration test passes | Any other content |
| 2 | A start with an existing progress file draws only from that file; a start without it draws from the word list | Integration test passes | Any other source |
| 3 | The unknown button never changes the file | Unit test passes | File changed |
| 4 | Marking the last card known results in a finished state and does not raise | Unit test passes | An exception |
| 5 | The program does not overwrite the progress file when it cannot be read; it reports a `VocabularyFormatError` | Unit test passes | File overwritten |
| 6 | The progress file has the same format as the word list, so that it can be used as a word list | Integration test round trip passes | Different format |
| 7 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest` exits with 0 | `RC-*` verdict Go and exit code 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-004 | The finished card and the full card cycle |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 1, step 4 | [BC-001] |
| US-001.04 Keep my progress | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-18 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add the progress port and its CSV adapter | `ProgressRepository` (`load` returns the deck or `None`, `save`) and `CsvProgressRepository` sharing the reading and writing code of the word list adapter, so the file format is defined once. | No | DCD-001 |
| 2 | Remove a known card and save | `Deck.remove`, `StudySession.mark_known` removing the current card and saving the deck; `open_study_session` prefers the progress file as the assignment says. | Yes | US-001.04 |
| 3 | Show the finished state | When the deck is empty the session returns no card, the view model shows "Nothing left to learn" and the buttons do nothing. | Yes | US-001.04 |
| 4 | Wire the known button | `is_known` on the view model and view calls `mark_known` and then `next_card`; the unknown button only calls `next_card`. | Yes | US-001.04 |
| 5 | Test progress | Unit tests for deck, session and finished state; integration tests of the three word example, the restart and the round trip, using `tmp_path`. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DCD-001]: ../dcd.md
