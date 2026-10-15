# RC-077: Review of PY-MIL-013

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-077 |
| CrossReference | [PY-MIL-013], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [f8ccfca] |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-013]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds in `smoke_driver.py`, `capture_screenshots.py` and the new tests; ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`known_button_point`, `parse_geometry`, `platform_kind`, `window_box`, `progress_ok`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 83 files; the one `type: ignore` for `os.killpg` names the errors it silences. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 49 source files and on the four tool scripts. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Process start and stop failures are turned into a failed run with its reason, not swallowed; no bare `except`. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Temporary folders are context-managed or removed in `finally`; processes are stopped as a group. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public modules, functions and constants have Doxygen docstrings; `doxygen Doxyfile` covers `src` and ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print` in `src`; the tools write results with `sys.stdout.write` as JSON lines. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No program class changed; the tools are packaging and check support outside the design classes (ADR-0005). |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 272 tests; the pure parts of the smoke driver and the capture tool are unit tested with fakes (no xdotool, no display); the whole suite passed twice in the Debian container including the real-window e2e tests. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty; the container image installs the extras `dev`, `speech`, `tools` and `build`. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The click point, the geometry parsing and the success rule are one function each in `smoke_driver.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; the tools import only the composition root. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | Pure functions with injected `run`, `start` and `sleep`; no function mixes the platform choice with drawing. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `tools/docker/` holds the container scripts and the driver; the layers and the test folders are unchanged. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Reviewed in the Debian container (python:3.13-slim-bookworm, Python 3.13.16).

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-013]: ../../../tools
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[f8ccfca]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/f8ccfca02ef3a518eae472e3acdcd2aef03b5950
