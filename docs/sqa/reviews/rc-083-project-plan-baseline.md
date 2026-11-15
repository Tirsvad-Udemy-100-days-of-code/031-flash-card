# Review Record: PP-001 against QC-PP-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-083 |
| CrossReference | [PP-001], [QC-PP-001], [QC-LANG-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-16 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial review record; verdict Go-with-conditions (autonomous, not independent) | pending |

---

## Artifact Under Review

- Instance reviewed: [PP-001]
- Checklist used: [QC-PP-001] and [QC-LANG-001]
- Scope: full review
- Language and domain: en / education
- Language reviewer: none (the stand-in reads English and knows the education domain)
- Mode: autonomous, not independent (AI as stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The plan states its start date, end date and the constraint it must fit | Pass | Planning Assumptions give the start date 2026-10-14, the end date 2026-10-21 and the constraint of the Business Case, and the window 2026-11-16 to 2026-11-23 of MIL-014. |
| 2 | Every milestone or gateway is listed once with its document, decision date and owner | Pass | The Gateway Schedule lists MIL-001 to MIL-014 once each with document, decision date and owner; every document exists. |
| 3 | Every decision date lies inside the plan's window and is consistent with the dates in the linked `MIL-*` document | Pass | The decision dates of MIL-001 to MIL-013 equal the Target Dates of their milestone documents (read for this review); MIL-014 decides on 2026-11-23, which is its Target Date and the end of its own window. |
| 4 | Every in-scope item of the Business Case is delivered at a named gateway (scope coverage) | Pass | Scope Coverage maps every In Scope item of BC-001 to a gateway; the new baseline item maps to MIL-014. |
| 5 | Dependencies between gateways are stated, acyclic and consistent with the schedule order | Fail | MIL-009 depends on MIL-008 (2026-10-20) but is dated 2026-10-16, and MIL-010 to MIL-013 are dated before MIL-008 as well. The chain is acyclic, but the dates do not follow it. The dates are as accepted and agree with the milestone documents; recorded as an Open Issue for S01. |
| 6 | The plan states what happens to later gateways and to the end date when a gateway is No-Go | Pass | Dependencies state that a No-Go moves the later dates and that a No-Go on MIL-014 leaves the program and the earlier gateways as they are; S01 decides the new date. |
| 7 | Owners, reviewers and escalation roles use Stakeholder Analysis IDs and match the governance RACI | Pass | Owner S01 and reviewer S01 (stand-in for the baseline) are stakeholder IDs of SA-001; no governance document exists (ADR-0003), so there is no RACI to contradict. |
| 8 | Planning assumptions are listed with their source, and a changed baseline is recorded with its reason | Pass | Each planning assumption names its source or is a decision of S01 (stated in the plan); the later window of MIL-014 is recorded with its reason. |
| 9 | Plan risks are listed with impact and a mitigation, and trace to Business Case risks where they come from there | Pass | Plan Risks give impact and mitigation for each of the four risks; the display risk matches a risk of BC-001 and the CI risk of MIL-014 traces to success criterion 9 of BC-001. |
| 10 | Open issues are listed, and none contradicts a statement elsewhere in the plan | Pass | Open Issues lists four points (no governance document, the missing milestone-sync workflow, the domain of the unchanged documents and the date order); none contradicts another statement of the plan. |
| 11 | Each gateway's main deliverable is stated and matches the deliverable of its `MIL-*` document | Pass | The main deliverable of MIL-014 names the same items as its Deliverable section; the rows of MIL-001 to MIL-013 are unchanged since their acceptance. |
| 12 | Gateways that deliver user stories name them, and those that do not say why | Pass | The Stories column names the user stories of each gateway; gateways with `none` are explained in the Planning Assumptions. |
| 13 | The schedule view (table, Gantt) and the dependency view agree with each other | Pass | The Gantt bars use the dates of the schedule table and the dependency line is the same chain as the Dependencies section. |
| 14 | Each gateway is linked to its issue-tracker milestone, or marked as not yet synced | Pass | MIL-001 to MIL-013 link milestones 165 to 179 of the git host, which exist; the baseline gateway links its milestone after the sync. |
| 15 | The plan is a singleton: one Project Plan per project, changes recorded in Version History | Pass | PP-001 is the only Project Plan; its Version History records each change in its own row and only the latest row is Accepted. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | The Metadata table has `Language | en` and `Domain | education`; neither is a placeholder. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is a BCP 47 code and `education` is a row of the domain list of docs/artifact-registry.md. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | The prose and the table cells are English; only file names, commands and IDs are code. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | The registry gives the register `IT Executive English` for this type; the text is written for that reader. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | The dictionary DICT-001 exists; the text uses its terms (flash card, word list, words to learn, study session, level, progress file) in one meaning each, with no synonym found by reading. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, section headings, IDs and statuses are the framework's English ones. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | No file `<name>.<language>.md` exists beside the document. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | The `Domain` row changed from `it` to `education` in this version (the language `en` is unchanged). The Version History row records the change and this review covers it. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The stand-in reads English and knows the education domain and checked the terms; the check is autonomous and not independent. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Fail | Some abbreviations of the earlier text (SQA, QC, MVVM, CSV, GNOME and similar) are not all spelled out at first use; CI and the other abbreviations added in this change are. Optional, deferred. |

## Overall Verdict

Go-with-conditions — every Mandatory criterion of QC-PP-001 and QC-LANG-001 passes except criterion 5 (the dates of MIL-009 to MIL-013 precede the date of MIL-008, on which MIL-009 depends); the dates are as accepted and the issue is recorded in the Open Issues of the plan for S01. Review of the whole document after the edits of this change.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Criterion PP 5 (Mandatory) failed: dates of MIL-009 to MIL-013 precede the date of MIL-008; S01 decides whether to re-date them (Open Issue of PP-001) | S01 | 2026-11-23 |
| Criterion LANG 10 (Optional) failed: Abbreviations are spelled out on first use, in the stated language; fix or accept the deferral | S01 | 2026-11-23 |

---

[PP-001]: ../../project-plan.md
[QC-PP-001]: ../../../framework/qc/artifacts/qc-project-plan.md
[QC-LANG-001]: ../../../framework/qc/artifacts/qc-language-domain.md
