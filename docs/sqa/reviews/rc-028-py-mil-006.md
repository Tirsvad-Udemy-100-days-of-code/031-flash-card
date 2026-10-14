# RC-028: Review of PY-MIL-006

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-028 |
| CrossReference | [PY-MIL-006], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [PY-MIL-006]
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | PEP 8 casing holds; ruff rule set N passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names are the DCD-001 IT terms (`SpeechPort`, `GttsSpeech`, `NullSpeech`, `build_speech`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass on 55 files with no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every signature is annotated; `mypy --strict` passes on 38 source files; third-party modules are imported with `importlib.import_module`, so no `type: ignore` is needed. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | The one broad `except Exception` in `GttsSpeech` is at the thread boundary, is commented, and logs with `exc_info`; it is not silent. No bare `except`. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults, no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Audio is written to a `tempfile.TemporaryDirectory` used as a context manager, so the file is always removed. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | New members have Doxygen docstrings; `doxygen Doxyfile` ends with 0 warnings. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | Failures are logged with `logging`, not printed; only the spoken text (a word) is in the log context, no personal data. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | `SpeechPort`, `GttsSpeech`, `NullSpeech`, `open_study_session(vocabulary_repository, progress_repository, speech, choose)` and `build_speech` match DCD-001 and SD-001 (the `speak` message of `startStudySession` and `markUnknown`). |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 124 tests (3 consecutive runs green) with fakes for the synthesiser and player; no test uses the network or plays a sound. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` reports no issue; no `Any`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is still empty; the extra `speech` pins `playsound==1.2.2` and `gTTS>=2.5`, and no module imports them outside `GttsSpeech`. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The speak rule is only in `StudySession.next_card`; the unused `SPEECH_LANGUAGE_CODE` constant was removed. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports `Layers point inward` kept; the port is in `application`, the adapters in `infrastructure`, the choice in the composition root. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `StudySession` depends on the `SpeechPort` Protocol and receives the adapter; `NullSpeech` honours the same contract (Null Object), so no `if speech` test exists. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `application/ports/` and `infrastructure/speech/` follow the folder structure of the clean-architecture skill. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names follow the rule. |

## Overall Verdict

Go — every Mandatory criterion passes. Reviewed by AI as stand-in for S01; not independent of the author.

Milestone MIL-006 Go criteria: 1 `speak(text, front_code)` once per drawn card and never when empty (unit tests); 2 `gtts` and `playsound` imported only when speaking, temporary file removed (unit tests with fakes); 3 service or player failure is logged and not raised (unit tests with caplog); 4 `build_speech` returns `NullSpeech` when the extra is missing or `--no-speech` is given (unit tests); 5 `dependencies` empty, extra pins `playsound==1.2.2` (pyproject.toml); 6 `speak` returns before a blocked player is released (unit test with an Event); 7 this record, `pytest` 124 passed. A manual check with the extra installed synthesised an mp3 of `kata` in Malay (7872 bytes) and `build_speech(True)` returned `GttsSpeech`; the audio was not played on this machine. All Go.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-MIL-006]: ../../../src/flash_card
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
