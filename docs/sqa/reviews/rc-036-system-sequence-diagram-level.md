# RC-036: Review of SSD-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-036 |
| CrossReference | [SSD-001], [QC-SSD-001], [QC-LANG-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [0b983b7] |

---

## Artifact Under Review

- Instance reviewed: [SSD-001]
- Checklist used: [QC-SSD-001], and [QC-LANG-001] (language and domain)
- Scope: full review
- Language and domain: en / it
- Language reviewer: none (the stand-in for S01 reads the language and knows the domain)
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Input/output messages match the corresponding Use Case's main success scenario step-for-step | Pass | System Operations table maps each message to steps of the main success scenario (1 to 9); the timer step is the one stated deviation. |
| 2 | Actor and System are treated strictly as black boxes (system shown as `:System`) | Pass | The system is `:System`; no internal object appears. |
| 3 | Object creation/destruction of the System instance handled explicitly where relevant | Pass | Lifecycle Notes state that the system lives for one run. |
| 4 | Return values are shown for operations that produce one, using dashed return arrows | Pass | Dashed return arrows are drawn for `startStudySession`, `chooseLevel`, the turn-over, `markKnown` and `markUnknown`. |
| 5 | Alternate/exceptional flows are represented separately (or explicitly out of scope noted) | Pass | The Alternate Flows section names extensions 3a, 4a, 5a, 7b and 9a, states that they add no operation, and says they are out of scope. |
| 6 | Message names are verb phrases consistent with the use case's system responsibilities | Pass | `startStudySession`, `markKnown` and `markUnknown` are verb phrases. |
| 7 | Diagram references the specific Use Case (name and ID) it depicts | Pass | Source Use Case section names UC-001 and the scenario. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | Metadata of SSD-001 has `Language | en` and `Domain | it`; neither is a placeholder. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is a BCP 47 code and `it` is a value of the registry's domain list. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | Prose and table cells are English; Malay and Danish words and file names appear only as quoted data. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | The registry gives `IT Professional English` for this type; the text is written for that reader. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | The PO terms of DICT-001 (flash card, word list, words to learn, study session) are used and no synonym replaces them. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, headings, IDs and statuses are English. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | No translated twin exists beside the document (checked in `docs/`). |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | First version; no change of language or domain since an earlier accepted version. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The reviewer is the stand-in for S01, the Product Owner, who reads English and knows the IT domain; no second language reviewer is needed (review-checklist-process step 2). Open to challenge by S01 in the end-of-run summary. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Fail | CSV, MVVM, UI, PO and similar abbreviations are not all spelled out at first use; Optional, deferred. |

## Overall Verdict

Go — every Mandatory criterion passes; the failed Optional criteria are deferred with an action item. Reviewed by AI as stand-in for S01; not independent of the author.

Full review (not a delta) after the level choice was added for MIL-008.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Criterion LANG 10 (Optional) failed: Abbreviations are spelled out on first use, in the stated language; fix or accept the deferral | S01 | 2026-10-21 |

---

[SSD-001]: ../../../docs/uc-001/ssd.md
[QC-SSD-001]: ../../../framework/qc/artifacts/qc-ssd.md
[QC-LANG-001]: ../../../framework/qc/artifacts/qc-language-domain.md
[0b983b7]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0b983b7fdadf6958717c1d0227d0f2ebe037f7b1
