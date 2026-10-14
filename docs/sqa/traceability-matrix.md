# Traceability Matrix: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose

Tracks backward/forward links between artifact instances so that the Business Case's
cross-artifact traceability success criterion is measurable. A row is added or
updated whenever an artifact instance is created or reviewed.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| BC-001 | Business Case | en | it | - | SA-001, PP-001 | [RC-001] |
| SA-001 | Stakeholder Analysis | en | it | BC-001 | PP-001, DICT-001 | [RC-002] |
| PP-001 | Project Plan | en | it | BC-001, SA-001 | MIL-001 to MIL-007 | [RC-003] |
| UCD-001 | Use Case Diagram | en | it | SA-001, BC-001 | US-001, UC-001 | [RC-004] |
| US-001 | User Story | en | it | UCD-001, BC-001 | MIL-002 to MIL-006 | [RC-005] |
| UC-001 | Use Case | en | it | UCD-001, US-001 | DM-001, SSD-001 | [RC-006] |
| DM-001 | Domain Model | en | it | UC-001 | SSD-001, DICT-001, DCD-001 | [RC-007] |
| SSD-001 | System Sequence Diagram | en | it | UC-001, DM-001 | DCD-001 | [RC-008] |
| OC-001 | Operation Contract | - | - | SSD-001, DM-001 | SD-001 | [RC-009] |
| SD-001 | Sequence Diagram | - | - | OC-001 | DCD-001 | [RC-010] |
| DCD-001 | Design Class Diagram | - | - | DM-001, SD-001, DICT-001 | src/flash_card | [RC-011] |
| DICT-001 | Domain Dictionary | en | it | BC-001, SA-001, DM-001 | DCD-001 | [RC-012] |
| ADR-0001 | Architecture Decision Record | - | - | BC-001 | MIL-001, MIL-003, MIL-006 | [RC-013] |
| ADR-0002 | Architecture Decision Record | - | - | BC-001 | DCD-001 | [RC-014] |
| ADR-0003 | Architecture Decision Record | - | - | BC-001 | - | [RC-015] |
| MIL-001 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-001 | [RC-016] |
| MIL-002 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-002 | [RC-017] |
| MIL-003 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-003 | [RC-018] |
| MIL-004 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-004 | [RC-019] |
| MIL-005 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-005 | [RC-020] |
| MIL-006 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-006 | [RC-021] |
| MIL-007 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-007 | [RC-022] |
| PY-MIL-001 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-023] |

## Coverage Notes

- `-` in Upstream means foundational; in Downstream it means nothing is built on it yet; in Last Reviewed it means no `RC-*` exists yet. Every row has a review record from the baseline review (autonomous mode, AI as stand-in for S01).
- Types not created for this project, and why: ADR-0003.
- Source code (`PY`) is added as `src/` is reviewed, one row per milestone.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[UCD-001]: ../use-case-diagram.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DM-001]: ../domain-model.md
[SSD-001]: ../uc-001/ssd.md
[OC-001]: ../uc-001/oc.md
[SD-001]: ../uc-001/sd.md
[DCD-001]: ../dcd.md
[DICT-001]: ../dictionary.md
[ADR-0001]: ../adr/adr-0001-standard-library-and-optional-speech.md
[ADR-0002]: ../adr/adr-0002-clean-architecture-and-mvvm.md
[ADR-0003]: ../adr/adr-0003-skipped-artifact-types.md
[MIL-001]: ../milestones/mil-001-foundation.md
[MIL-002]: ../milestones/mil-002-step1-user-interface.md
[MIL-003]: ../milestones/mil-003-step2-new-flash-cards.md
[MIL-004]: ../milestones/mil-004-step3-flip-cards.md
[MIL-005]: ../milestones/mil-005-step4-save-progress.md
[MIL-006]: ../milestones/mil-006-malay-speech.md
[MIL-007]: ../milestones/mil-007-documentation-and-publication.md
[PY-MIL-001]: ../../src/flash_card
[RC-001]: ./reviews/rc-001-business-case.md
[RC-002]: ./reviews/rc-002-stakeholder-analysis.md
[RC-003]: ./reviews/rc-003-project-plan.md
[RC-004]: ./reviews/rc-004-use-case-diagram.md
[RC-005]: ./reviews/rc-005-user-stories.md
[RC-006]: ./reviews/rc-006-use-case.md
[RC-007]: ./reviews/rc-007-domain-model.md
[RC-008]: ./reviews/rc-008-system-sequence-diagram.md
[RC-009]: ./reviews/rc-009-operation-contracts.md
[RC-010]: ./reviews/rc-010-sequence-diagrams.md
[RC-011]: ./reviews/rc-011-design-class-diagram.md
[RC-012]: ./reviews/rc-012-domain-dictionary.md
[RC-013]: ./reviews/rc-013-adr-0001.md
[RC-014]: ./reviews/rc-014-adr-0002.md
[RC-015]: ./reviews/rc-015-adr-0003.md
[RC-016]: ./reviews/rc-016-mil-001.md
[RC-017]: ./reviews/rc-017-mil-002.md
[RC-018]: ./reviews/rc-018-mil-003.md
[RC-019]: ./reviews/rc-019-mil-004.md
[RC-020]: ./reviews/rc-020-mil-005.md
[RC-021]: ./reviews/rc-021-mil-006.md
[RC-022]: ./reviews/rc-022-mil-007.md
[RC-023]: ./reviews/rc-023-py-mil-001.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
