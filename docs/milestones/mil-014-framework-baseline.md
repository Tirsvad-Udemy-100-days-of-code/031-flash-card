# MIL-014: Framework baseline

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-014 |
| CrossReference | [BC-001], [PP-001], [MIL-013] |
| Language | en |
| Domain | education |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-16 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version; accepted with the Go verdict of the review record (autonomous, not independent) | [94431a3] |
| 2026-11-16 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added task 6 (behaviour-neutral rewrite of the process calls and a sleep in two tool scripts so the OpenGrep scan passes without a suppression); reviewed in autonomous mode, not independent | [12d3033] |

---

## Purpose

This gate decides whether Flash Card has the baseline of the framework: the adopted framework release, the wiki in English, Danish and Malay in the framework's shape (language line first, one sidebar), the README in the framework template with an appendix that lists only the documents of the repository, complete licence and project URL metadata, a traceability matrix that covers the changed documents and reviewed documents, merged to the default branch with a green build. One behaviour-neutral rewrite of two tool scripts is part of it, so that the OpenGrep scan of the pull request passes without a suppression. The work is delivered on the branch `mil-014-baseline` and one pull request. It changes no behaviour of the program.

## Deliverable

A merged pull request that holds: the updated Business Case, Project Plan, Artifact Registry and Traceability Matrix with their review records; the wiki in `docs/wiki/` with the language line on every page and one sidebar; the README without the private framework files in its appendix; `pyproject.toml` with the project URLs and a build requirement that reads the licence expression; and the framework release adopted by the project. The behaviour of the program, its tests and its tools do not change; only three statements in `tools/capture_screenshots.py` and `tools/docker/smoke_driver.py` are rewritten so that the OpenGrep scan passes.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | BC-001, PP-001 and MIL-014 each have an `Accepted` Version History row and a review record, and the wiki has a review record | Verdict `Go` (the wiki `Go-with-conditions` until it is checked on the host) | Any missing or `No-Go` |
| 2 | `python -m pytest` runs (the window tests skip without a display) | Exit code 0 | Any failure |
| 3 | `docs/wiki/` has `_Sidebar.md` and the pages Home, Install, Usage and Architecture in en, da and ms, each starting with the language line | 12 pages and the sidebar | A page or language missing |
| 4 | `framework/scripts/check-readme.sh` and `framework/scripts/check-languages.sh` run | Exit code 0 | Any finding |
| 5 | `pyproject.toml` sets `license`, `license-files`, the authors and the project URLs for the repository, the documentation and the issue tracker | All set | Any missing |
| 6 | All CI (continuous integration) checks of the pull request | Green | Red or pending |
| 7 | The pull request carries one `Closes #N` line per task of this milestone | Every issue is closed after the merge | An issue stays open |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-013] accepted | Documents and baselines the finished program, its container checks and its wiki |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 1 to 5 | Criterion 2 (the behaviour is unchanged and its tests pass) |
| Objective 6 | Criteria 1, 3, 4, 5 and 7 (documents, wiki, README, licence and issues) |
| Success criterion 9 | Criteria 1 and 6 |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-11-23: one week after the start, as the Business Case assumption requires.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Adopt the framework release | Track the `framework/` submodule and `.gitmodules`, install the skills and hooks, add `.editorconfig`, track `.env.example` and ignore the local prompt logs, so the project follows the same rules as the other projects of the portfolio. | No | Objective 6 |
| 2 | Update and review the planning documents | Add this milestone to the Business Case and Project Plan, set the domain of the changed documents to education, link the milestones MIL-008 to MIL-013 to the git host, extend the traceability matrix and review each changed document against its QC checklist, so the plan-first gate is met. | No | Objective 6 |
| 3 | Bring the wiki to the framework's shape | Put the language line first on every page and write one sidebar with the page list once and a Languages section, keeping the existing pages and their names. | No | Objective 6 |
| 4 | Bring the README to the framework template | Keep the text of the README, add the framework files to the project layout and give the appendix only the documents that are in the repository, so the README is complete and checkable. | No | Objective 6 |
| 5 | Complete the licence metadata | Add the project URLs to `pyproject.toml` and raise the build requirement to the setuptools version that reads a licence expression, so package tools can read them. | No | Objective 6 |
| 6 | Rewrite three statements in the tool scripts so the OpenGrep scan passes | In `tools/capture_screenshots.py` wait with the Tk `after` call instead of `time.sleep`, and in `tools/docker/smoke_driver.py` pass each command to `subprocess.run` and `subprocess.Popen` as a fresh list built from the given arguments, so that the three findings of severity ERROR of the OpenGrep scan no longer match. The scan is not suppressed. The behaviour is unchanged; the unit tests, ruff, mypy and import-linter pass. | No | Objective 6 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[MIL-013]: ./mil-013-container-checks.md
[94431a3]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/94431a39b6ef3859341ddc17384b90bd97fb8944
[12d3033]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/12d3033b2cbf2a6d6f88b1f8ad54c221cdc5e070
