# RC-029: Review of PY-MIL-007

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-029 |
| CrossReference | [PY-MIL-007], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [9289426] |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-007]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds in `tools/capture_screenshots.py` and the changed view; ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`capture`, `_make_dpi_aware`, `SCREENSHOT_SEED`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 56 files; the one `type: ignore` is for a Windows-only attribute and says which error it silences. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on `src` (38 files) and on both tool scripts. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No exception handling was added. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | The data copy uses `tempfile.TemporaryDirectory` as a context manager; the Tk root is destroyed. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Module, functions and constants have Doxygen comments; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | The tool writes the two output paths with `sys.stdout.write`; no `print`, no secret. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | The only source change is the button background in `FlashCardView`, which follows `wireframe.md`; the tool is outside the design classes and is not part of the program. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 125 tests, 2 consecutive full runs green; one e2e assertion was added for the button background; the tool is checked by running it and reading both images. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue on the touched files; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` stays empty; Pillow is the optional extra `tools` and is imported only by the tool. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The seed, output folder and delay come from one definition each; the delay is `FLIP_DELAY_MS`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; the tool imports the composition root only. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The tool has one purpose (capture); the view change adds no rule. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `tools/` holds helper scripts outside `src/`; the layers are unchanged. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule (`docs/images`, `docs/wiki` pages are exceptions for wiki names). |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-007 Go criteria: 1 `check-readme.sh` exit 0 and both screenshots linked from the README; 2 `docs/wiki/` holds Home, Install, Usage and Architecture as `<Page>.md`, `<Page>-da.md`, `<Page>-ms.md` (12 pages) and `_Sidebar.md` listing the three languages; 3 the screenshots are captured from the running program by `tools/capture_screenshots.py` and were inspected; 4 the README Setup and Run need 5 commands (create `.venv`, activate, upgrade pip, install, run); 5 the repository has a description and 10 topics (read back from the API); 6 `doxygen Doxyfile` 0 warnings; 7 `docs/sqa/traceability-matrix.md` has a row for every created artifact with its latest `RC-*`, and the plan links each milestone; 8 `check-languages.sh` exit 0 (`check-plan.sh` is a commit-message hook and was not run). The wiki is pushed to the host's wiki after this merge. The Danish and Malay wiki pages were written by the AI and have not been read by a native speaker; this is stated in the end-of-run summary. All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-007]: ../../../tools
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[9289426]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/92894268c51ec77d56cff48d968566e6265795a2
