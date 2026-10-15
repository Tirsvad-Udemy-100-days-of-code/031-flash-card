# RC-072: Review of the release v0.2.0

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-072 |
| CrossReference | [MIL-012] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [5345fd7] |

---

## Artifact Under Review

- Instance reviewed: [MIL-012] (the milestone's Go / No-Go criteria, checked against the release v0.2.0)
- Checklist used: none exists for a release; the nine criteria of MIL-012 are the checklist
- Scope: full review
- Language and domain: n/a (record of results)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The three version places say `0.2.0` and a test fails when they differ | Pass | `pyproject.toml`, `flash_card.__version__` and `Doxyfile` say 0.2.0; `tests/unit/test_version.py` (3 tests) |
| 2 | `CHANGELOG.md` has a `[0.2.0]` entry (menu bar, progress per word list, UTF-8 message) and `[0.1.0]` is unchanged | Pass | Read in the pull request #94 |
| 3 | The upload limit of the git host is probed before the build with a draft release that is deleted afterwards, and the result is recorded | Pass | A draft release with a 1 MB random file was refused with `413 Request Entity Too Large`; the draft and its tag were deleted (release and tag lists checked) |
| 4 | The executable is built with `--clean` from the commit to be tagged and passes the smoke test of MIL-009 | Fail | Built with `--clean` from `d7ca24d` (25.8 MB). The first smoke run passed three cases (level screen window, embedded list, progress file with 999 cards at level 100); the list override case failed once because the simulated mouse click did not register, and in 3 of 8 reruns the same click was lost. The cause was not found: it may be the click automation (timing of the pointer and the focus) or a defect of the program. The checks were stopped at the Product Owner's request because they take over the desktop, and are to be repeated in a container or on an isolated desktop (MIL-013) |
| 5 | The tag `v0.2.0` is an annotated tag on that commit; `v0.1.0` is not moved | Fail | The tag points to `d7ca24d` and `v0.1.0` is unchanged (`2c580cc`), but the tag is lightweight: the push of my annotated tag failed on a connection error, and the release creation through the API then created a lightweight tag. Replacing it needs a force update of a tag, which is outside what an autonomous run may do without the Product Owner |
| 6 | The release `v0.2.0` is published with notes (new, unsigned, `data` folder rule, how to build) | Pass | Release page returns HTTP 200; notes say what is new, that the file is unsigned, the `data` folder and how to build |
| 7 | When the probe did not allow it: the notes say so and the issue "attach the files" stays open | Pass | The notes state that the executable is not attached and why; issue "Create the release and attach the files" stays open |
| 8 | README, CHANGELOG and the Install page of the wiki in three languages link `v0.2.0`; `check-readme.sh` exit 0 | Pass | Merged in #94; wiki republished |
| 9 | `pytest`, `ruff`, `mypy --strict`, `lint-imports` and `doxygen` are clean; BC-001, US-001 and PP-001 reviewed `Go` | Pass | 261 passed; RC-067 to RC-069 |

## Overall Verdict

Go-with-conditions — the version, the CHANGELOG, the tag (lightweight) and the release page are in place, and the executable is correctly stated as not attached. Criteria 4 and 5 fail or are incomplete: the smoke test of the executable is not complete, and the tag is not annotated. Reviewed by AI as stand-in for S01; not independent of the author.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Decide whether the lightweight tag `v0.2.0` may be replaced by an annotated tag on the same commit (a force update of the tag on the host); `v0.1.0` stays | S01 | 2026-10-18 |
| Repeat the smoke test of the executable on an isolated desktop or in a container and find the cause of the lost click (criterion 4), then close the issue "Build and smoke-test the executable" | S01 | 2026-10-21 |
| Attach `flash-card.exe` and its checksum when the git host's upload limit is raised (issue "Create the release and attach the files") | S01 | 2026-10-21 |

---

[MIL-012]: ../milestones/mil-012-release-0-2-0.md
[5345fd7]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/5345fd77d404b7a8b7c3722fa5ada2bf14f234a7
