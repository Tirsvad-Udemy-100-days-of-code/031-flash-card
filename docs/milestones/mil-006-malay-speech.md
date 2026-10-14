# MIL-006: Spoken Malay word

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-006 |
| CrossReference | [BC-001], [US-001], [UC-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose

Decide whether the Product Owner's extra works without harming the core program: the Malay word is spoken when its card is shown, and the program is unchanged when the speech extra is not installed.

## Deliverable

`pip install -e ".[speech]"` makes the program speak the Malay word on each new card. Without the extra, without a network, or with `--no-speech`, the program works silently and shows no error.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `StudySession.next_card` calls `SpeechPort.speak(text, "ms")` once per drawn card, and never for the finished state | Unit test with a fake port passes | Any other number of calls |
| 2 | `GttsSpeech` imports `gtts` and `playsound` only when it speaks, writes the audio to a temporary file and removes it | Unit test with injected fakes passes | Import at module level or a leftover file |
| 3 | A failure of the service or the player is logged and not raised | Unit test passes | Exception reaches the caller |
| 4 | Without the extra installed, `build_speech` returns `NullSpeech` and the program starts | Unit test with a blocked import passes | Start fails |
| 5 | `dependencies` in `pyproject.toml` is still empty and the extra pins `playsound==1.2.2` | File check in the review record | Any runtime dependency |
| 6 | Speaking does not block the Tkinter main loop | The adapter speaks in a daemon thread; unit test asserts `speak` returns before the player finishes | The window freezes while speaking |
| 7 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest` exits with 0 | `RC-*` verdict Go and exit code 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-005 | The complete card cycle the speech hooks into |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 2 (spoken Malay word), objective 3 (no runtime dependencies) | [BC-001] |
| US-001.05 Hear the Malay word | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-19 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add the speech port and the silent adapter | `SpeechPort` in the application layer and `NullSpeech` in infrastructure, so that `StudySession` always has a speaker and has no `if speech` checks. | No | ADR-0001, DCD-001 |
| 2 | Speak the Malay word on each new card | `StudySession.next_card` asks the port to speak the front text in the front language code. | Yes | US-001.05 |
| 3 | Add the gTTS adapter | `GttsSpeech` creates the audio with `gTTS`, plays it with `playsound` in a daemon thread, removes the temporary file and logs failures; third-party imports happen on first use. | Yes | US-001.05 |
| 4 | Choose the speaker in the composition root and add --no-speech | `build_speech` returns `GttsSpeech` when `gtts` and `playsound` can be imported and `NullSpeech` otherwise; the command line option `--no-speech` forces silence. | No | |
| 5 | Declare the extra and test the adapters | The `speech` extra in `pyproject.toml`; unit tests with fake `gtts`, player and port, none of which uses the network. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DCD-001]: ../dcd.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
