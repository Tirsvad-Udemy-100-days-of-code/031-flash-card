# Stakeholder Analysis: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose

This analysis names the people who influence the flash card project or are affected by it, so that owners, reviewers and readers can be cited by a stable ID in every other document. It follows the power and interest grid: each stakeholder is placed in one quadrant, and the quadrant sets how closely the project engages that stakeholder.

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen, course participant | Product Owner, developer and reviewer | Self (Tirsvad) | HIGH | HIGH | Manage Closely | Finish the assignment with a working, understood and documented solution |
| S02 | Udemy coursists | Fellow participants of the 100 Days of Code course | Udemy course community | LOW | HIGH | Keep Informed | Readable, runnable code that keeps the assignment's function names, and instructions to run it, so that solutions can be shared and compared |
| S03 | GitHub viewers | Visitors who browse the repository for ideas | Public | LOW | LOW | Monitor | A clear repository description, topics and README, and no runtime dependencies to install |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** S01 decides scope, writes the code and accepts the result, so both power and interest are high. S01 is the only stakeholder who can accept or reject a milestone.
- **Keep Informed (S02):** S02 cannot change the project, so power is low. They share code and compare solutions, so interest is high; the project informs them through a README that explains how to run the program and tests, and through function names they recognise from the assignment.
- **Monitor (S03):** S03 arrive occasionally and have no stake beyond finding the repository useful, so power and interest are both low. The project serves them with a repository description, topics and a README, and does not require them to install runtime dependencies.

S02 and S03 are classified by S01 as Product Owner; neither can be interviewed, so the classification is an assumption recorded in BC-001.

## Primary Concerns and FURPS+ Mapping

| ID | Concern | FURPS+ attribute |
| --- | --- | --- |
| S01 | The four assignment steps work and progress is saved | Functionality |
| S01 | Work is tracked step by step, each step reviewed | Supportability (+ Process) |
| S01 | Malay words are spoken, in Danish translation | Functionality |
| S02 | Code is readable and runnable with the assignment's function names | Usability, Supportability |
| S02 | Instructions to run the program and its tests | Usability |
| S03 | Repository description, topics and README are clear | Usability |
| S03 | No runtime dependencies to install | Supportability (+ Implementation) |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| S01 | Chat session and pull request review | Once per milestone | Pull request with the milestone's changes and review record | MIL-001 to MIL-007 |
| S02 | README and wiki | Once, at the documentation milestone, then on change | Run and test instructions, assignment function names | MIL-007 |
| S03 | Repository description, topics, README and wiki | Once, at the documentation milestone | Description, topics, README, screenshots | MIL-007 |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S01 wants spoken Malay words (needs `gTTS` and `playsound`), S03 wants no runtime dependencies | S01, S03 | Speech is an optional extra (`pip install .[speech]`) behind a port; the core program uses the standard library only |
| S01 wants clean architecture with layers, S02 wants code that is simple to read and compare with the assignment | S01, S02 | The assignment's function names (`next_card`, `flip_card`, `is_known`) are kept at the presentation layer, and the wiki maps each assignment step to the files that implement it |

## Traceability Analysis

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | Four assignment steps work, progress is saved | Objective 1 of [BC-001] |
| S01 | Spoken Malay word, Danish translation | Objective 2 of [BC-001] |
| S01 | Step-by-step tracking | Objective 5 of [BC-001] |
| S02 | Readable, runnable code with assignment function names | Objectives 1 and 4 of [BC-001] |
| S03 | Description, topics, README, no runtime dependencies | Objectives 3 and 4 of [BC-001] |

## Sign-Off

Proposed by the author. Accepted when `RC-*` for SA-001 has the verdict Go; in autonomous mode by the AI as stand-in for S01, and open to challenge by S01 in the end-of-run summary.

---

[BC-001]: ./business-case.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
