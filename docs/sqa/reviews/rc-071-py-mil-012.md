# RC-071: Review of PY-MIL-012

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-071 |
| CrossReference | [PY-MIL-012], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-012]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | The change is one assignment and a test module; names follow PEP 8. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | `test_version_of_the_package_equals_pyproject_version` and similar names state the behaviour. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass with no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Test functions are annotated `-> None`; `mypy --strict` passes on 49 source files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No exception handling in the change. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults. |
| 7 | Files, locks and connections are managed with context managers | Pass | `pyproject.toml` is read with `tomllib` through a `with open` context. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | The module docstring keeps `@file` and `@brief`; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print`, no logging in the change. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No class or operation changed; the version string is not part of the design. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 3 tests compare `__version__`, `pyproject.toml` and the `Doxyfile` `PROJECT_NUMBER` and the `MAJOR.MINOR.PATCH` form; 3 consecutive full runs (261 tests) green. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty; `tomllib` is standard library. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The version is stated once per file type; the test makes the three places agree. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | One test module with one reason to change. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | The test sits in `tests/unit`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-012 tasks 2, 3, 4 and 8 (this change set): 1 the three version places say 0.2.0 and a test fails if they differ; 2 CHANGELOG has `[0.2.0]` and `[0.1.0]` is unchanged; 3 the upload limit probe ran before the build: a draft release with a 1 MB random file was refused with `413 Request Entity Too Large`, so the largest accepted size is below 1 MB; the draft release and its tag were deleted afterwards (the tag list and the release list were checked); 8 README, CHANGELOG and the Install page of the wiki in three languages link v0.2.0 and say that the executable is not attached; `check-readme.sh` exit 0. The tag, the build and the release are criteria 4 to 7 and are recorded in a separate review record. Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-012]: ../../../src/flash_card/__init__.py
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
