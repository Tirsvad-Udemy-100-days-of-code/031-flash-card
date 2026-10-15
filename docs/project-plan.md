# Project Plan: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | PP-001 |
| CrossReference | [BC-001], [SA-001], [US-001], [MIL-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005], [MIL-006], [MIL-007], [MIL-008], [MIL-009], [MIL-010], [MIL-011] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added gateway MIL-010 Release v0.1.0 (new request of S01) | [9c8e294] |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added gateway MIL-011 Menu bar (new request of S01) | [2211d0f] |

---

## Purpose

This plan schedules the seven phases (gateways) that deliver the flash card program inside the delivery window of one week that the Business Case sets as a constraint (2026-10-14 to 2026-10-21). Each phase is one milestone and is delivered by one pull request, so the Product Owner (S01) can follow the work step by step.

## Planning Assumptions

- Week 1 starts 2026-10-14; the plan ends by 2026-10-21, per the Business Case constraint.
- One phase takes one day; the last phase (documentation and publication) has three days because the wiki exists in three languages and the screenshots need the finished program.
- The baseline documents (Business Case, Stakeholder Analysis, Project Plan, use case documents, ADRs) are accepted before MIL-001 starts, in a pull request of their own.
- Phases 2 to 5 follow the four steps of the course assignment in order; phase 6 is the Product Owner's extra.
- S01 is owner and approving reviewer of every phase; in autonomous mode the AI acts as stand-in and the review records say so.

## Gateway Schedule

| Gateway | Document | Window | Decision date | Owner | Stories | Main deliverable | Milestone |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Project foundation | [MIL-001] | 2026-10-14 | 2026-10-14 | S01 | none | pyproject, gitignore, skeleton, Doxyfile, first README, word list | [Milestone MIL-001][MS-001] |
| Step 1 - User interface | [MIL-002] | 2026-10-15 | 2026-10-15 | S01 | US-001.01 | The window with card and buttons | [Milestone MIL-002][MS-002] |
| Step 2 - New flash cards | [MIL-003] | 2026-10-16 | 2026-10-16 | S01 | US-001.02 | Random cards from the word list | [Milestone MIL-003][MS-003] |
| Step 3 - Flip the cards | [MIL-004] | 2026-10-17 | 2026-10-17 | S01 | US-001.03 | Flip after 3000 ms | [Milestone MIL-004][MS-004] |
| Step 4 - Save progress | [MIL-005] | 2026-10-18 | 2026-10-18 | S01 | US-001.04 | words_to_learn.csv | [Milestone MIL-005][MS-005] |
| Spoken Malay word | [MIL-006] | 2026-10-19 | 2026-10-19 | S01 | US-001.05 | Text to speech as optional extra | [Milestone MIL-006][MS-006] |
| Documentation and publication | [MIL-007] | 2026-10-19 to 2026-10-21 | 2026-10-21 | S01 | none | README, screenshots, wiki in 3 languages, description and topics | [Milestone MIL-007][MS-007] |
| Choose level | [MIL-008] | 2026-10-20 | 2026-10-20 | S01 | US-001.06 | A level choice (100, 1000, all words) before the cards; documents, wiki and screenshots updated | |
| Executable with PyInstaller | [MIL-009] | 2026-10-16 | 2026-10-16 | S01 | US-001.07 | One Windows executable that runs without Python, built by a script; documents, wiki and README updated | |
| Release v0.1.0 | [MIL-010] | 2026-10-16 | 2026-10-16 | S01 | US-001.08 | Tag v0.1.0 and a release with `flash-card.exe`, its checksum and release notes | |
| Menu bar | [MIL-011] | 2026-10-17 | 2026-10-17 | S01 | US-001.09 to US-001.12 | File menu (open word list, change level, reset word list, exit) and About menu (contact); documents, wiki and screenshots updated | |

```plantuml
@startgantt
Project starts 2026-10-14
[Foundation] starts 2026-10-14 and ends 2026-10-14
[Step 1 UI] starts 2026-10-15 and ends 2026-10-15
[Step 2 Cards] starts 2026-10-16 and ends 2026-10-16
[Step 3 Flip] starts 2026-10-17 and ends 2026-10-17
[Step 4 Progress] starts 2026-10-18 and ends 2026-10-18
[Speech] starts 2026-10-19 and ends 2026-10-19
[Documentation] starts 2026-10-19 and ends 2026-10-21
[Foundation Go/No-Go] happens 2026-10-14
[Step 1 Go/No-Go] happens 2026-10-15
[Step 2 Go/No-Go] happens 2026-10-16
[Step 3 Go/No-Go] happens 2026-10-17
[Step 4 Go/No-Go] happens 2026-10-18
[Speech Go/No-Go] happens 2026-10-19
[Documentation Go/No-Go] happens 2026-10-21
[Choose level] starts 2026-10-20 and ends 2026-10-20
[Choose level Go/No-Go] happens 2026-10-20
[Executable] starts 2026-10-16 and ends 2026-10-16
[Executable Go/No-Go] happens 2026-10-16
[Release] starts 2026-10-16 and ends 2026-10-16
[Release Go/No-Go] happens 2026-10-16
[Menu bar] starts 2026-10-17 and ends 2026-10-17
[Menu bar Go/No-Go] happens 2026-10-17
@endgantt
```

## Scope Coverage

| Business Case scope item | Gateway |
| --- | --- |
| Tkinter program with the assignment's function names | MIL-002, MIL-003, MIL-004, MIL-005 |
| Reading `data/ms-da.csv` | MIL-003 |
| Saving and using `words_to_learn.csv` | MIL-005 |
| Optional spoken Malay word | MIL-006 |
| `pyproject.toml`, `.gitignore`, `Doxyfile`, `.venv` instructions, `pytest`, `constants.py` | MIL-001 |
| README, screenshots, wiki in three languages | MIL-007 |
| Repository description and topics | MIL-007 |
| Choice of level (new request after MIL-007) | MIL-008 |
| Executable built with PyInstaller (new request after MIL-008) | MIL-009 |
| Release with the executable attached (new request after MIL-009) | MIL-010 |
| Menu bar with File and About menus (new request after MIL-009) | MIL-011 |
| Framework documents of the baseline | Baseline pull request before MIL-001 |

## Dependencies

```
Baseline → MIL-001 → MIL-002 → MIL-003 → MIL-004 → MIL-005 → MIL-006 → MIL-007 → MIL-008 → MIL-009 → MIL-010 → MIL-011
```

A No-Go on a phase moves every later date by the days the rework takes; MIL-008 was added after MIL-007 and takes the unplanned day 2026-10-20, so no buffer is left inside the window; a No-Go moves the end date past 2026-10-21 and S01 decides whether to accept that.

## Plan Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| No display on the machine that runs the review, so the e2e tests skip | Window behaviour is checked by the view model tests only | The review record states whether the e2e tests ran; the screenshots in MIL-007 prove the window on a machine with a display |
| The git host's CI is not available | The publish workflows cannot run | Milestones are published with `sync-project.sh` and the wiki by SSH push (MIL-007) |
| The speech extra cannot be installed on the build machine | MIL-006 cannot be demonstrated end to end | The adapter is tested with fakes; the manual check is recorded as not done |

## Open Issues

- No Governance document (GOV): see ADR-0003. S01 is the only approver.
- The git host's `sync-milestones` workflow is not installed; whether to install it is S01's decision.

---

[BC-001]: ./business-case.md
[SA-001]: ./stakeholder-analysis.md
[US-001]: ./user-stories.md
[MIL-001]: ./milestones/mil-001-foundation.md
[MIL-002]: ./milestones/mil-002-step1-user-interface.md
[MIL-003]: ./milestones/mil-003-step2-new-flash-cards.md
[MIL-004]: ./milestones/mil-004-step3-flip-cards.md
[MIL-005]: ./milestones/mil-005-step4-save-progress.md
[MIL-006]: ./milestones/mil-006-malay-speech.md
[MIL-007]: ./milestones/mil-007-documentation-and-publication.md
[MIL-008]: ./milestones/mil-008-choose-level.md
[MIL-009]: ./milestones/mil-009-executable.md
[MIL-010]: ./milestones/mil-010-release.md
[MIL-011]: ./milestones/mil-011-menu-bar.md
[MS-001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/165
[MS-002]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/166
[MS-003]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/167
[MS-004]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/168
[MS-005]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/169
[MS-006]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/170
[MS-007]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/milestone/171
[9c8e294]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/9c8e2940217e615f82eda2d48aca9b2fd58f3687
[2211d0f]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/2211d0f4cbd8182314d18cbdefd939ae50c39e6d
