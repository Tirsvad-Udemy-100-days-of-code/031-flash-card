# MIL-007: Documentation and publication

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-007 |
| CrossReference | [BC-001], [US-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose

Decide whether the project can be handed to its readers: S02 can run it and compare their solution, and S03 can understand what it is from the repository page.

## Deliverable

The final README with screenshots, the wiki in English, Danish and Bahasa Malaysia (same page set), the generated Doxygen documentation, the final traceability matrix, and the repository description and topics set on the git host.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `check-readme.sh` reports no finding and the README has the front and back screenshot | No finding; both files exist and are linked | Any finding |
| 2 | `docs/wiki/` holds the same pages in `<Page>.md`, `<Page>-da.md` and `<Page>-ms.md` and a `_Sidebar.md` that lists the three languages | File list compared | A page is missing in a language |
| 3 | The screenshots are taken from the running program, not drawn by hand | Capture script is in `tools/` and the images show the window of this program | Mock-up |
| 4 | The README gives the `.venv` and pip upgrade commands, and the run and test commands in five commands or fewer | Count in the review record | More than five |
| 5 | The repository has a description and at least 5 topics on the git host | Read back from the API | Any missing |
| 6 | `doxygen Doxyfile` builds without warnings about undocumented public items of `src/` | Output of the run | Warnings |
| 7 | The traceability matrix has a row for every created artifact and the last `RC-*` of each | Row count in the review record | A missing row |
| 8 | `check-languages.sh` and `check-plan.sh` report no finding | Exit code 0 | Any finding |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-006 | The documentation describes the finished program |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 4 (a repository others can use); success criteria 4, 5, 6, 7 | [BC-001] |
| All stories (the wiki maps each to a step) | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-21 — the end of the delivery window ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Capture screenshots of the running program | Write `tools/capture_screenshots.py` that starts the program, waits for the front, grabs the window, waits 3 s for the back and grabs it again; save `docs/images/screenshot-front.png` and `screenshot-back.png`. The tool needs Pillow, which is a tool-only dependency and not a project dependency. | No | |
| 2 | Finish the README | Complete the README from the framework template with the screenshots, the assignment-to-code map, the optional speech extra, the data attribution, and the commands to run the program and the tests. | No | |
| 3 | Write the wiki in English | Pages `Home`, `Install`, `Usage`, `Architecture` in `docs/wiki/` with the language line and a sidebar. | No | |
| 4 | Translate the wiki to Danish and Bahasa Malaysia | The same four pages as `<Page>-da.md` and `<Page>-ms.md`; commands, file names and IDs stay in English. | No | |
| 5 | Build the Doxygen documentation | Run `doxygen Doxyfile` and fix undocumented public items; the generated `docs/doxygen/` is ignored by git and described in the README. | No | |
| 6 | Set the repository description and topics | Update the description and topics of the repository on the git host through its API, using the token from `.env`, which is not read into the project. | No | |
| 7 | Publish the wiki pages | Push `docs/wiki/` to the repository's wiki over SSH after the merge, because the opt-in publish workflow needs a runner and a secret the project does not have. | No | |
| 8 | Close the traceability matrix | One row per artifact with its latest review record, and the end-of-run summary of the autonomous run. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
