# RC-041: Review of PY-MIL-008

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-041 |
| CrossReference | [PY-MIL-008], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-008]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds in all new modules (`level.py`, `level_view.py`, `window.py`); ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose and are the dictionary's IT terms (`Level`, `Deck.within`, `LevelViewModel`, `LevelChoice`, `Application.start`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 67 files with no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 44 source files and on `tools/capture_screenshots.py`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | `Level` raises `ValueError` for a limit below 1; a failed session start after a click is logged, closes the window with exit code 1 and never swallows silently; no bare `except`. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | No new file handling beyond the existing context managers. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | New and changed members have Doxygen docstrings; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print`; failures are logged with `logging`; no personal data is logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | `Level`, `Deck.within`, `Deck.draw(among)`, `StudySession(level_cards)`, `open_study_session(..., level)`, `LevelChoice`, `LevelViewModel`, `LevelView` and `Application` match the revised DCD-001, OC-001 `chooseLevel` and SD-001. Deviations: `Application` (root, repositories, speech) with `start`, `show_level_screen` and `exit_code` is the composition root detail that DCD-001 shows as `app.main`; `StudySession.remaining_in_level` and `LevelView.frame` are additions. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 191 tests (3 consecutive full runs green) cover `Level`, `Deck.within`, the level filter, the cross-level progress rules on the real word list, the view model, `--level` and the real level window flow; none uses the network. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty; no new package. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The level rule exists only in `Level.first` and `Deck.within`; the choices, labels and sizes exist once in `constants.py`; both views use `configure_window`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; a grep finds no `tkinter`, `csv` or `random` import in `domain` or `application`; the level view model imports no Tkinter. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The view model owns the choices and the view draws them; the composition root only wires; the session depends on protocols and receives its collaborators. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `presentation/features/level/` and `presentation/shared/` follow the clean-architecture folder structure; tests stay in `unit`, `integration`, `e2e` (with a session-scoped `tk_root` in `tests/e2e/conftest.py`). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-008 Go criteria: 1 level 100 draws exactly the first 100 rows over a full run of the real list (integration test); 2 levels 1000 and All use all 1000 words, and a shorter list is used whole (unit and integration tests); 3 words known at level 100 stay known at All and the progress file keeps every unknown word, also outside the level (integration test); 4 a level with nothing left gives the finished message and no failure (unit and e2e tests); 5 the level view model has no Tkinter import and its tests pass without a display; 6 `--level 100|1000|all` skips the screen and an unknown value exits with 2 (unit tests); 7 UC-001, DM-001, DICT-001, SSD-001, OC-001, SD-001, DCD-001, BC-001, US-001, PP-001 and MIL-008 were re-reviewed `Go` (RC-030 to RC-040), the wireframe has Screen 1, and the README and the wiki in en, da and ms describe the level; 8 this record, `pytest` 191 passed, ruff, mypy, lint-imports and doxygen clean. A real screenshot of the level screen was captured and inspected after fixing a too-small window. The Danish and Malay wiki additions were written by the AI and are not read by a native speaker. All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-008]: ../../../src/flash_card
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
