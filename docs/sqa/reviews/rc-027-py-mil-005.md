# RC-027: Review of PY-MIL-005

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-027 |
| CrossReference | [PY-MIL-005], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-005]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds; ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names are the dictionary's IT terms and the assignment's (`is_known`, `mark_known`, `ProgressRepository`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 47 files with no suppressions; `[tool.ruff.format] line-ending = "lf"` and `.gitattributes` fix the line endings. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 33 source files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | A malformed progress file raises `VocabularyFormatError` and is never overwritten; the temporary file is removed when a write fails (re-raise, no swallow); no bare `except`. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Reading uses `with`; the write goes through a temporary file that is replaced atomically. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | New and changed members have Doxygen docstrings; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print`; no secret or personal data is logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | `ProgressRepository`, `CsvProgressRepository`, `StudySession.mark_known` and `is_known` are in DCD-001 and OC-001 (`markKnown`); `open_study_session` takes no speech port until MIL-006, as DCD-001 shows for the final design. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 107 tests (6 consecutive full runs all green) include the assignment's 3 record example, restart, round trip, finished state and e2e on the real window over `tmp_path`; none uses the network. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Reader and writer share `CSV_DELIMITER`, `CSV_ENCODING` and the row width in `csv_word_list.py`; the removal rule is only in `Deck.remove`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; the `ProgressRepository` Protocol is in `domain`, its adapter in `infrastructure`. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The use case depends on the Protocol and receives the adapter; the view model sequences two session calls only. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | New files are in the layer folders of the clean-architecture skill; tests in `unit`, `integration`, `e2e`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-005 Go criteria: 1 the 3 record example leaves the other two cards in order with the header (integration test); 2 a start uses the progress file when it exists and the word list otherwise (integration test); 3 the wrong button never writes (unit and e2e); 4 the last card known gives a finished state (unit); 5 a malformed progress file raises `VocabularyFormatError` and stays untouched (unit); 6 round trip readable as a word list (integration); 7 this record, `pytest` 107 passed. A manual run on a copy of `ms-da.csv` removed the known word and wrote 999 cards. Defect found and fixed in this milestone: a flaky `TclError` caused by pytest's descriptor capture and Tcl file handles; the view now loads image bytes with `Path.read_bytes()` and `PhotoImage(data=...)`. All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-005]: ../../../src/flash_card
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
