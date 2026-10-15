# Traceability Matrix: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |
| 2026-10-14 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added MIL-008 and the review records of the level choice (no checklist exists for this type) | [0b983b7] |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the rows and review records of the executable request (no checklist exists for this type) | [768ca34] |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the rows and review records of the executable request (no checklist exists for this type) | [061b4f4] |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the rows and review records of the executable request (no checklist exists for this type) | [9c8e294] |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the rows and review records of the executable request (no checklist exists for this type) | [2211d0f] |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the rows and review records of the executable request (no checklist exists for this type) | [0264b60] |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the rows and review records of the executable request (no checklist exists for this type) | [f86bc91] |

---

## Purpose

Tracks backward/forward links between artifact instances so that the Business Case's
cross-artifact traceability success criterion is measurable. A row is added or
updated whenever an artifact instance is created or reviewed.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| BC-001 | Business Case | en | it | - | SA-001, PP-001 | [RC-073] |
| SA-001 | Stakeholder Analysis | en | it | BC-001 | PP-001, DICT-001 | [RC-002] |
| PP-001 | Project Plan | en | it | BC-001, SA-001 | MIL-001 to MIL-008 | [RC-074] |
| UCD-001 | Use Case Diagram | en | it | SA-001, BC-001 | US-001, UC-001 | [RC-004] |
| US-001 | User Story | en | it | UCD-001, BC-001 | MIL-002 to MIL-006, MIL-008 | [RC-068] |
| UC-001 | Use Case | en | it | UCD-001, US-001 | DM-001, SSD-001 | [RC-058] |
| DM-001 | Domain Model | en | it | UC-001 | SSD-001, DICT-001, DCD-001 | [RC-034] |
| SSD-001 | System Sequence Diagram | en | it | UC-001, DM-001 | DCD-001 | [RC-059] |
| OC-001 | Operation Contract | - | - | SSD-001, DM-001 | SD-001 | [RC-060] |
| SD-001 | Sequence Diagram | - | - | OC-001 | DCD-001 | [RC-061] |
| DCD-001 | Design Class Diagram | - | - | DM-001, SD-001, DICT-001 | src/flash_card | [RC-062] |
| DICT-001 | Domain Dictionary | en | it | BC-001, SA-001, DM-001 | DCD-001 | [RC-063] |
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
| MIL-008 | Milestone / Gateway | en | it | BC-001, PP-001 | tasks of MIL-008 | [RC-040] |
| MIL-009 | Milestone / Gateway | en | it | BC-001 | - | [RC-050] |
| ADR-0004 | Architecture Decision Record | - | - | BC-001 | - | [RC-046] |
| MIL-010 | Milestone / Gateway | en | it | BC-001 | - | [RC-054], [RC-055] |
| MIL-011 | Milestone / Gateway | en | it | BC-001 | - | [RC-065] |
| MIL-012 | Milestone / Gateway | en | it | BC-001 | - | [RC-070], [RC-072] |
| MIL-013 | Milestone / Gateway | en | it | BC-001 | - | [RC-076], [RC-079], [RC-080] |
| ADR-0005 | Architecture Decision Record | - | - | BC-001 | - | [RC-075] |
| PY-MIL-001 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-023] |
| PY-MIL-002 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-024] |
| PY-MIL-003 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-025] |
| PY-MIL-004 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-026] |
| PY-MIL-005 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-027] |
| PY-MIL-006 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-028] |
| PY-MIL-007 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-029] |
| PY-MIL-008 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-041] |
| PY-MIL-009 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-048] |
| PY-MIL-011 | Python Source Code | - | - | DCD-001, ADR-0002 | - | [RC-066] |
| PY-FIX-001 | Python Source Code | - | - | PY-MIL-008 | - | [RC-049] |
| PY-MIL-012 | Python Source Code | - | - | MIL-012 | - | [RC-071] |
| PY-MIL-013 | Python Source Code | - | - | MIL-013 | - | [RC-077] |
| SH-MIL-013 | Shell Script | - | - | MIL-013 | - | [RC-078] |

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
[RC-024]: ./reviews/rc-024-py-mil-002.md
[PY-MIL-002]: ../../src/flash_card
[RC-025]: ./reviews/rc-025-py-mil-003.md
[PY-MIL-003]: ../../src/flash_card
[RC-026]: ./reviews/rc-026-py-mil-004.md
[PY-MIL-004]: ../../src/flash_card
[RC-027]: ./reviews/rc-027-py-mil-005.md
[PY-MIL-005]: ../../src/flash_card
[RC-028]: ./reviews/rc-028-py-mil-006.md
[PY-MIL-006]: ../../src/flash_card
[RC-029]: ./reviews/rc-029-py-mil-007.md
[PY-MIL-007]: ../../src/flash_card
[RC-030]: ./reviews/rc-030-business-case-level.md
[RC-031]: ./reviews/rc-031-user-stories-level.md
[RC-032]: ./reviews/rc-032-project-plan-level.md
[RC-033]: ./reviews/rc-033-use-case-level.md
[RC-034]: ./reviews/rc-034-domain-model-level.md
[RC-035]: ./reviews/rc-035-domain-dictionary-level.md
[RC-036]: ./reviews/rc-036-system-sequence-diagram-level.md
[RC-037]: ./reviews/rc-037-operation-contracts-level.md
[RC-038]: ./reviews/rc-038-sequence-diagrams-level.md
[RC-039]: ./reviews/rc-039-design-class-diagram-level.md
[RC-040]: ./reviews/rc-040-mil-008.md
[MIL-008]: ../milestones/mil-008-choose-level.md
[0b983b7]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0b983b7fdadf6958717c1d0227d0f2ebe037f7b1
[RC-041]: ./reviews/rc-041-py-mil-008.md
[PY-MIL-008]: ../../src/flash_card
[RC-042]: ./reviews/rc-042-business-case-exe.md
[RC-043]: ./reviews/rc-043-user-stories-exe.md
[RC-044]: ./reviews/rc-044-project-plan-exe.md
[RC-045]: ./reviews/rc-045-design-class-diagram-exe.md
[RC-046]: ./reviews/rc-046-adr-0004.md
[RC-047]: ./reviews/rc-047-mil-009.md
[MIL-009]: ../milestones/mil-009-executable.md
[ADR-0004]: ../adr/adr-0004-pyinstaller-executable.md
[768ca34]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/768ca344c95d4f21e565e37ac96661c2f8dc8f54
[RC-048]: ./reviews/rc-048-py-mil-009.md
[PY-MIL-009]: ../../src/flash_card
[RC-049]: ./reviews/rc-049-py-fix-001.md
[PY-FIX-001]: ../../tests/unit/test_app.py
[RC-050]: ./reviews/rc-050-mil-009-task9.md
[061b4f4]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/061b4f48b5d49e6800656c95d79df707e07ec0f3
[RC-051]: ./reviews/rc-051-business-case-release.md
[RC-052]: ./reviews/rc-052-user-stories-release.md
[RC-053]: ./reviews/rc-053-project-plan-release.md
[RC-054]: ./reviews/rc-054-mil-010.md
[MIL-010]: ../milestones/mil-010-release.md
[9c8e294]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/9c8e2940217e615f82eda2d48aca9b2fd58f3687
[RC-055]: ./reviews/rc-055-release-v0-1-0.md
[RC-056]: ./reviews/rc-056-business-case-menu.md
[RC-057]: ./reviews/rc-057-user-stories-menu.md
[RC-058]: ./reviews/rc-058-use-case-menu.md
[RC-059]: ./reviews/rc-059-system-sequence-diagram-menu.md
[RC-060]: ./reviews/rc-060-operation-contracts-menu.md
[RC-061]: ./reviews/rc-061-sequence-diagrams-menu.md
[RC-062]: ./reviews/rc-062-design-class-diagram-menu.md
[RC-063]: ./reviews/rc-063-domain-dictionary-menu.md
[RC-064]: ./reviews/rc-064-project-plan-menu.md
[RC-065]: ./reviews/rc-065-mil-011.md
[MIL-011]: ../milestones/mil-011-menu-bar.md
[2211d0f]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/2211d0f4cbd8182314d18cbdefd939ae50c39e6d
[RC-066]: ./reviews/rc-066-py-mil-011.md
[PY-MIL-011]: ../../src/flash_card
[RC-067]: ./reviews/rc-067-business-case-r020.md
[RC-068]: ./reviews/rc-068-user-stories-r020.md
[RC-069]: ./reviews/rc-069-project-plan-r020.md
[RC-070]: ./reviews/rc-070-mil-012.md
[MIL-012]: ../milestones/mil-012-release-0-2-0.md
[0264b60]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0264b6084f26bac5af716ea71596ce3be961fec8
[RC-071]: ./reviews/rc-071-py-mil-012.md
[PY-MIL-012]: ../../src/flash_card/__init__.py
[RC-072]: ./reviews/rc-072-release-v0-2-0.md
[RC-073]: ./reviews/rc-073-business-case-containers.md
[RC-074]: ./reviews/rc-074-project-plan-containers.md
[RC-075]: ./reviews/rc-075-adr-0005.md
[RC-076]: ./reviews/rc-076-mil-013.md
[MIL-013]: ../milestones/mil-013-container-checks.md
[ADR-0005]: ../adr/adr-0005-container-and-sandbox-checks.md
[f86bc91]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/f86bc9136e7719fbcd049a4f803959019b7d2df3
[RC-077]: ./reviews/rc-077-py-mil-013.md
[RC-078]: ./reviews/rc-078-sh-mil-013.md
[PY-MIL-013]: ../../tools
[SH-MIL-013]: ../../tools/docker
[RC-079]: ./reviews/rc-079-container-checks.md
[RC-080]: ./reviews/rc-080-sandbox-run.md
