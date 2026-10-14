# RC-048: Review of PY-MIL-009

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-048 |
| CrossReference | [PY-MIL-009], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-009]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds in `runtime.py`, `build_executable.py` and the changed modules; ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`resource_root`, `executable_dir`, `build_arguments`, `resolve_data_files`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 71 files with no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 45 source files and on the three tool scripts. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | `main` of the build tool returns 2 with a message when PyInstaller is not installed; no bare `except`; no swallowed exception. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | No new file handling beyond the existing context managers; the ICO file is written with `Path.write_bytes`. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | New and changed members have Doxygen docstrings; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print` in `src`; the tools write results with `sys.stdout.write`; no secret. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | The program classes are unchanged (DCD-001); `runtime.py` and `tools/` are packaging support outside the design classes, as ADR-0004 and the Scope note of DCD-001 state; `resolve_data_files` is a function of the composition root. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 216 tests (3 consecutive runs green): pure runtime helpers for the frozen and source cases, the argument list of the build, the ICO file, the bundled word list fallback, and the level screen window title; none starts PyInstaller or uses the network. The real executable was built and smoke-tested separately (note below). |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; `sys._MEIPASS` is read with `getattr` and no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is still empty; PyInstaller is only in the extra `build` and Pillow only in `tools`. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The frozen rule is one definition (`runtime.py`) used by `constants.py`; file names and sizes stay in `constants.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; `runtime.py` imports only the standard library. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The build tool has one purpose and a pure `build_arguments` that is tested; the composition root chooses the word list file. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `tools/build_executable.py` and `runtime.py` sit outside the four layers as packaging support; layers and test folders are unchanged. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-009 Go criteria: 1 `python tools/build_executable.py` ended with exit code 0 and wrote `dist/flash-card.exe` (25.8 MB) with PyInstaller 6.22.3 on the Windows Store Python 3.13.14; 2 started from a temporary folder without the virtual environment, the executable showed a window titled `Flashy` after about 2 seconds and has no console (windowed bootloader); 3 with `data/ms-da.csv` beside it (3 words) one tick left 2 cards in the progress file, without it the embedded list was used (1000 words); 4 one tick wrote `data/words_to_learn.csv` next to the executable with 999 cards at level 100; 5 a captured screenshot of the executable shows the card and both button images; 6 unit tests of the frozen rule pass; 7 `dependencies` empty, extra `build`; 8 BC-001, DCD-001, ADR-0004, PP-001, US-001 and MIL-009 were reviewed Go (RC-042 to RC-047), README and the Install page of the wiki in three languages describe the build; 9 this record, `pytest` 216 passed, ruff, mypy, lint-imports and doxygen clean. Defects found by the smoke test and fixed in this milestone: the level screen window had the default title `tk` and no padding because `LevelView` did not call `configure_window`. Notes: the one-file build starts a second process (the bootloader), so a tool that watches a window must not match the first process id; the first start after a build took over 20 seconds on this machine (unpacking and a virus scan) and later starts about 2 seconds; the spoken word was not tested in the executable (the speech packages are collected into it, the network call was not exercised). All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-009]: ../../../src/flash_card
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
