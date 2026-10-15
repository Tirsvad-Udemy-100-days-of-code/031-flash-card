# MIL-011: Menu bar

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-011 |
| CrossReference | [BC-001], [US-001], [UC-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decide whether the program has the classic menu bar the Product Owner asked for: a File menu (open a word list, change the level, reset a word list, exit) and an About menu (contact), and whether the commands keep the progress of every word list safe.

## Deliverable

The window has a menu bar. File: Open (a CSV word list), Change level, Reset word list, Exit. About: Contact with the author's name and title and a link to the author's LinkedIn page. The progress of each word list is kept in its own file. README, the Usage page of the wiki in three languages and a screenshot show the menu.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The menu bar has File (Open, Change level, Reset word list, separator, Exit) and About (Contact, LinkedIn entry) with the labels of the wireframe | e2e test reads the menu entries and their order | A different structure |
| 2 | Opening a valid CSV word list switches the cards to it after the level choice; opening an invalid file shows a message and keeps the earlier list; cancelling changes nothing | Unit and e2e tests with a faked file dialog and message box | A wrong list in use or a crash |
| 3 | The progress of each word list is a file of its own: `words_to_learn.csv` for the delivered `ms-da.csv` and `words_to_learn_<name>.csv` for another list; known words of one list never appear in another | Integration test with two lists | Progress mixed or lost |
| 4 | Change level shows the level choice again without a restart and keeps the known words | Unit and e2e tests | Restart needed or progress lost |
| 5 | Reset word list asks to confirm; on yes only the progress file of the open list is deleted and the level choice is shown; on no nothing changes; the word list file is never changed | Unit, integration and e2e tests | Another file touched |
| 6 | About, Contact opens `https://www.linkedin.com/in/tirsvad74` through `webbrowser` and shows "Jens Tirsvad Nielsen, Software engineer" | Unit test with a faked `webbrowser.open` | Another address |
| 7 | Exit closes the window, cancels the pending timer and ends the program with exit code 0 | e2e test | A leftover timer or an error |
| 8 | The menu logic is in a view model without Tkinter; the commands are one use case or application call each | View model unit tests without a display | A rule in the view |
| 9 | The documents of the plan (BC-001, US-001, UC-001, SSD-001, OC-001, SD-001, DCD-001, DICT-001, wireframe, PP-001) and README and wiki in three languages describe the menu, each reviewed `Go` | Review records `Go`; `check-readme.sh` exit 0 | A document is missing |
| 10 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest`, `ruff`, `mypy --strict`, `lint-imports` and `doxygen` are clean | `RC-*` verdict Go and exit codes 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-009 | The program with the level screen, the executable and the data folder rules; MIL-010 (release) is independent and may be done before or after |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 1 and 2 (learning with word lists), extended by the new request of S01 | [BC-001] |
| US-001.09 to US-001.12 | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-17 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Update the documents for the menu bar | Amend BC-001 (In Scope: a menu bar with the commands), UC-001 (the menu commands as extensions at any card), SSD-001, OC-001 and SD-001 (`openWordList`, `changeLevel`, `resetWordList`, `exit`), DCD-001 (`ProgressRepository.reset`, the menu classes, `Application` commands), DICT-001 and the wireframe (menu bar and dialogs); each changed document gets a Version History row and a review. | No | UC-001, DCD-001 |
| 2 | Keep the progress of every word list apart | `progress_file_name(list_path)` in one place (`words_to_learn.csv` for `ms-da.csv`, `words_to_learn_<name>.csv` for another list) and `ProgressRepository.reset()` with its CSV adapter (deletes the file, no error when it is absent). | Yes | US-001.09, US-001.11 |
| 3 | Open another word list | The application loads a CSV chosen in the file dialog (starting in the data folder), validates it before it replaces the list in use, and shows the level choice for it; an invalid file gives a message and no change. | Yes | US-001.09 |
| 4 | Change level while learning | The application shows the level choice again on the same window and starts the session at the chosen level with the progress kept. | Yes | US-001.10 |
| 5 | Reset a word list | After a confirmation the application resets the progress of the open list and shows the level choice; the word list file is never changed. | Yes | US-001.11 |
| 6 | Add the menu bar and the About menu | `MenuViewModel` (entries, labels, order, no Tkinter) and `MenuView` (the Tk menu bar on the window, mnemonics, Exit that cancels the timer, About, Contact entry that opens the LinkedIn page); the contact data and labels are constants. | Yes | US-001.12 |
| 7 | Test the menu and the commands | Unit tests (progress file names, reset, view model, application commands with faked dialogs and `webbrowser`), integration tests with two word lists, e2e test of the real menu bar. | No | |
| 8 | Update README, wiki and screenshots | README and the Usage page of the wiki in English, Danish and Bahasa Malaysia, and a screenshot that includes the menu bar; the wiki is republished after the merge. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DCD-001]: ../dcd.md
