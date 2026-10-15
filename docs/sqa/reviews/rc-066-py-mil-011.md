# RC-066: Review of PY-MIL-011

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-066 |
| CrossReference | [PY-MIL-011], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-011]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds in the new modules (`menu_view.py`, `menu_view_model.py`, `progress_file_name.py`); ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose and are the DCD-001 IT terms (`MenuView`, `MenuViewModel`, `Application.open_word_list`, `reset`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 79 files with no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 49 source files and on the three tool scripts. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Refused files raise `VocabularyFormatError` with `from` (also for bytes that are not UTF-8), a failed reset is logged and shown, a failed browser start is logged; no bare `except`, nothing swallowed silently. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Reading uses `with`; the delete uses `unlink(missing_ok=True)`; the Tk root is destroyed through `exit_application`. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | New and changed members have Doxygen docstrings; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print`; failures use `logging`; the contact data is public author information given by S01. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | The new classes match the revised DCD-001 and OC-001/SD-001. Deviations: `MenuEntry` has a third field `underline`; `MenuViewModel` has `file_label` and `contact_menu_label`; `Application` has `word_list_folder` and takes a repository factory; `MenuView` depends on a small `MenuApplication` Protocol to avoid an import cycle. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 258 tests (5 consecutive full runs green): unit with fakes only, integration with two word lists, and e2e on the real menu bar with injected dialogs; none uses the network or a real browser. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty; `webbrowser`, `tkinter.filedialog` and `tkinter.messagebox` are standard library. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The progress file rule is one function (`progress_file_name`); labels, contact data and dialog texts are constants once. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; a grep finds no `tkinter`, `csv`, `random` or `webbrowser` import in `domain` or `application`; the menu view model imports no Tkinter. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The view model owns the entries and the view draws and asks dialogs; `Application` coordinates; the repositories own their files; dialogs and the browser are injected. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `presentation/features/menu/` and `infrastructure/persistence/` follow the folder structure; tests stay in `unit`, `integration`, `e2e`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-011 Go criteria: 1 the menu bar structure and order are read from the real `tk.Menu` (e2e); 2 open valid / invalid / cancelled covered (unit and e2e, including a Latin-1 file and invalid UTF-8 bytes); 3 two lists keep separate progress files, `ms-da.csv` keeps `words_to_learn.csv` (integration); 4 change level shows the level screen and keeps the known words (unit and e2e); 5 reset asks, deletes only the progress file of the open list, never the list file (unit, integration, e2e); 6 About, Contact opens `https://www.linkedin.com/in/tirsvad74` through an injected `webbrowser.open` (unit and e2e); 7 exit cancels the timer and destroys the window (e2e); 8 view model tested without Tkinter; 9 RC-056 to RC-065 `Go`, README and the Usage page of the wiki in three languages describe the menu; 10 this record, `pytest` 258 passed and linters clean. The executable was rebuilt with the menu and passes the smoke test (window, embedded list, list override, progress file). A real browser launch and the native file dialog were not exercised on this machine. Defect found by the reviewer and fixed in this milestone: a file that is not UTF-8 raised `UnicodeDecodeError` instead of a message. All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-011]: ../../../src/flash_card
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
