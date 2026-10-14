# RC-025: Review of PY-MIL-003

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-025 |
| CrossReference | [PY-MIL-003], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-003]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Packages, modules, classes and functions follow PEP 8 casing; ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose in the dictionary's IT terms (`Deck`, `Vocabulary`, `StudySession`, `CardDto`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 43 files with no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 31 source files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | `read_word_list` raises `VocabularyNotFoundError` with `from` to keep the cause; no bare or swallowed exception; `Deck.remove` raises `ValueError` (not in OC-001, a deviation recorded here). |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default arguments; no builtin shadowed (`Card`, `Deck` do not shadow). |
| 7 | Files, locks and connections are managed with context managers | Pass | The CSV file is opened with `with` in `read_word_list`. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public modules, classes and functions have Doxygen docstrings; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print`; `app.main` logs errors with `logging`; no personal data logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | Classes and operations are those of DCD-001 (`Card`, `LanguagePair`, `Vocabulary`, `Deck`, `StudySession`, `CardDto`, `CsvVocabularyRepository`, view and view model). Deviations: `Deck.remove` raises `ValueError` when the card is absent; `read_word_list` is a shared function behind both CSV repositories, as MIL-005 task 1 requires. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 66 tests (unit by layer, integration on the real `data/ms-da.csv`, e2e on the real window) named for behaviour; none uses the network or depends on order. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty; `csv`, `random` and `pathlib` are standard library (ADR-0001). |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The CSV format, encoding and delimiter are defined once in `constants.py` and `read_word_list`; the draw rule is only in `Deck.draw`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; a grep finds no `tkinter`, `csv` or `random` import in `domain` or `application`. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | One reason to change per class; the choice function is injected into `StudySession` and `Deck.draw`, and the repository is a Protocol that the use case receives. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Source is in `domain`, `application`, `infrastructure`, `presentation` with the sub-folders of the clean-architecture skill; tests in `unit`, `integration`, `e2e`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names are English snake_case, no space. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-003 Go criteria: 1 integration test reads 1000 cards, pair ms/da; 2 missing header, bad row and missing file raise `VocabularyFormatError`/`VocabularyNotFoundError` (unit tests); 3 a press shows a different card when two or more exist and the same when one (unit tests); 4 blank lines are ignored (unit test); 5 no `tkinter`, `csv` or `random` import in domain/application (grep, empty); 6 this record and `pytest` 66 passed. A manual smoke run on the real file showed a new word after a press. All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-003]: ../../../src/flash_card
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
