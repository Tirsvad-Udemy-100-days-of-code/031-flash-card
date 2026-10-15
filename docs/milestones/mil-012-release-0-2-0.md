# MIL-012: Release v0.2.0

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-012 |
| CrossReference | [BC-001], [US-001], [UC-001], [ADR-0004] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decide whether the project can be handed out as version 0.2.0: the version is raised, the tag `v0.2.0` is made on the commit that is built, and the release page has notes and, when the git host accepts the upload, the executable with its checksum. Version 0.2.0 is the minor release that adds the menu bar and the progress per word list to 0.1.0.

## Deliverable

`pyproject.toml`, `flash_card.__version__` and the `Doxyfile` say `0.2.0`; `CHANGELOG.md` has the entry for 0.2.0; the annotated tag `v0.2.0` is on the head of `main`; the release `v0.2.0` exists with notes; `flash-card.exe` and `flash-card.exe.sha256` are attached if the upload limit of the git host allows it, otherwise the notes say how to build the executable and the open issue stays open.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The three version places say `0.2.0` and a test fails when `flash_card.__version__` and `pyproject.toml` differ | Test passes; grep shows the same version | A different version |
| 2 | `CHANGELOG.md` has a `[0.2.0]` entry listing the menu bar, the progress per word list and the message for a file that is not UTF-8, and `[0.1.0]` is unchanged | File read in the review record | A missing or changed entry |
| 3 | The upload limit of the git host is probed before the build with a draft release that is deleted afterwards, and the result is recorded | Result in the review record | No probe |
| 4 | The executable is built with `--clean` from the commit to be tagged and passes the smoke test of MIL-009 (window, embedded list, progress beside it, list override) | Smoke test output in the review record | A failing case |
| 5 | The tag `v0.2.0` is an annotated tag on that commit; `v0.1.0` is not moved | `git show v0.2.0` and `git rev-parse v0.1.0` | A moved or lightweight tag |
| 6 | The release `v0.2.0` is published with notes that state what is new, that the file is unsigned, the `data` folder rule and how to build | Notes read back from the API | A statement is missing |
| 7 | When the probe allowed it: the release has `flash-card.exe` and `flash-card.exe.sha256`, and the SHA-256 of the downloaded file equals the checksum; when the probe did not allow it: the notes say so and the issue "attach the files" stays open | Hash compared, or the statement is present | A wrong or unverifiable hash |
| 8 | README, CHANGELOG and the Install page of the wiki in three languages link `v0.2.0` and say whether the executable is attached; `check-readme.sh` exit 0 | Exit code 0 | A link is missing |
| 9 | `pytest`, `ruff`, `mypy --strict`, `lint-imports` and `doxygen` are clean after the version change; BC-001, US-001 and PP-001 are reviewed `Go` | `RC-*` verdict Go and exit codes 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-011 | The menu bar that makes this release |
| MIL-010 | The release procedure and its open issue about the upload limit |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 4 (a repository others can use) | [BC-001] |
| US-001.08 Download the executable | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-18 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Update the documents for the release | BC-001 (releases in plural), US-001.08 (the latest release instead of v0.1.0) and PP-001; each changed document gets a Version History row and a review. | No | BC-001, US-001 |
| 2 | Raise the version to 0.2.0 | `pyproject.toml`, `flash_card.__version__` in `src/flash_card/__init__.py` and `PROJECT_NUMBER` of the `Doxyfile`; one unit test compares the version of the package with `pyproject.toml`, so the places cannot drift. | No | |
| 3 | Write the CHANGELOG entry and the release notes | `[0.2.0]` with Added (menu bar: open another word list, change level, reset word list, exit, contact; progress kept apart for each word list), Fixed (a file that is not UTF-8 gives a message) and the known limits; the same text is the release body. | No | |
| 4 | Probe the upload limit of the git host | Create a draft release, try uploads of 1, 5, 10 and 30 MB random files one after another and stop at the first refusal, delete the draft and its tag; record the largest accepted size. The token is read inside the script. | No | |
| 5 | Build and smoke-test the executable from the tagged commit | `python tools/build_executable.py --clean` from a clean tree of the head of `main` after the version change, the smoke test, and the SHA-256. | Yes | US-001.08 |
| 6 | Tag v0.2.0 | Annotated tag `v0.2.0` on the head of `main` and push it; `v0.1.0` stays where it is. | No | |
| 7 | Create the release and attach the files | Create the release `v0.2.0` with the notes through the API; attach `flash-card.exe` and `flash-card.exe.sha256` when the probe allows it and compare the hash after a download; otherwise say so in the notes and leave the issue open. | Yes | US-001.08 |
| 8 | Link the release | README, CHANGELOG and the Install page of the wiki in English, Danish and Bahasa Malaysia link `v0.2.0`; the wiki is republished. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[ADR-0004]: ../adr/adr-0004-pyinstaller-executable.md
