# MIL-010: Release v0.1.0

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-010 |
| CrossReference | [BC-001], [US-001], [UC-001], [ADR-0004] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [9c8e294] |

---

## Purpose

Decide whether the project can be handed out as a release: the version 0.1.0 is tagged, and the executable built from exactly that commit is attached to a release page with its checksum and release notes.

## Deliverable

A tag `v0.1.0` on the head of `main`, and a release on the git host with the assets `flash-card.exe` and `flash-card.exe.sha256`, and release notes. `CHANGELOG.md` holds the same notes. The README and the wiki (English, Danish, Bahasa Malaysia) link to the release page.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The executable is rebuilt from the head of `main` that gets the tag, in a clean build folder, and passes the smoke test of MIL-009 (window, embedded list, progress file beside it, list override) | Smoke test output recorded in the review record | A failing case |
| 2 | The tag `v0.1.0` is an annotated tag on that commit and `pyproject.toml` and `flash_card.__version__` say `0.1.0` | `git show v0.1.0` and the two files agree | A different version or commit |
| 3 | The release has the assets `flash-card.exe` and `flash-card.exe.sha256` | Listed by the host API | An asset is missing |
| 4 | The SHA-256 of the file downloaded from the release equals the value in `flash-card.exe.sha256` and in the release notes | Hash compared after a download | A difference |
| 5 | The release notes say that the file is an unsigned Windows build, what the `data` folder next to it holds, the SHA-256, and how to build it | Notes read back from the API | A statement is missing |
| 6 | `CHANGELOG.md`, README and the Install page of the wiki in three languages link the release; `check-readme.sh` exit 0 | Exit code 0 | A link is missing |
| 7 | BC-001, US-001 and PP-001 are updated (the release upload leaves Out of Scope) and reviewed `Go` | Review records `Go` | A document is not updated |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-009 | The executable and its build script |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 4 (a repository others can use), extended by the new request of S01 | [BC-001] |
| US-001.08 Download the executable | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-16 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Update the documents for the release | Amend BC-001 (the upload of the executable to a release leaves Out of Scope and the release becomes In Scope; signing and an installer stay out), add US-001.08 and the gateway to PP-001; each changed document gets a Version History row and a review. | No | BC-001, US-001 |
| 2 | Write the release notes and CHANGELOG.md | `CHANGELOG.md` (Keep a Changelog layout) with the version 0.1.0: what the program does, the four assignment steps, the level choice, the executable, known limits (unsigned, Windows only, Python 3.13 or later to build); the notes are reused for the release body. | No | |
| 3 | Rebuild and smoke-test the executable from the tagged commit | Build `dist/flash-card.exe` from a clean tree of the head of `main`, run the smoke test of MIL-009, compute the SHA-256 and write `flash-card.exe.sha256` (not committed). | Yes | US-001.08 |
| 4 | Tag v0.1.0 | Create an annotated tag `v0.1.0` on the head of `main` and push it; a tag cannot be undone without deleting it on the host, so it is made only after the documents are merged. | No | |
| 5 | Create the release and attach the files | Create the release `v0.1.0` through the host API with the notes, attach `flash-card.exe` and `flash-card.exe.sha256`, download the asset again and compare the hash. The token is read from `.env` and is never printed or put on a command line. | Yes | US-001.08 |
| 6 | Link the release | README, the Install page of the wiki in English, Danish and Bahasa Malaysia and `CHANGELOG.md` link the release page; the wiki is republished. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[ADR-0004]: ../adr/adr-0004-pyinstaller-executable.md
[9c8e294]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/9c8e2940217e615f82eda2d48aca9b2fd58f3687
