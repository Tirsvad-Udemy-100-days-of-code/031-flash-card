# RC-063: Review of DICT-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-063 |
| CrossReference | [DICT-001], [QC-DICT-001], [QC-LANG-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [DICT-001]
- Checklist used: [QC-DICT-001], and [QC-LANG-001] (language and domain)
- Scope: full review
- Language and domain: en / it
- Language reviewer: none (the stand-in for S01 reads the language and knows the domain)
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Every row has a PO term, its language, an IT term and a definition | Pass | All 9 rows have PO term, language, IT term and definition. |
| 2 | Each PO term maps to exactly one IT term and the reverse (no synonyms) | Pass | One IT term per PO term; no synonym appears. |
| 3 | Every Domain Model concept has a row, and the Domain Model uses its PO term | Pass | The 5 concepts of DM-001 have a row and DM-001 uses the PO term; `Reset` was added. |
| 4 | The Operation Contracts, Sequence Diagrams, Design Class Diagrams and ERD use the IT term, not the PO term | Pass | DCD-001, OC-001 and SD-001 use `Card`, `Vocabulary`, `Deck`, `StudySession`. |
| 5 | Definitions are written in the PO language and are one sentence | Pass | Definitions are one English sentence each. |
| 6 | "Used as PO term in" and "Used as IT term in" name artifact types that exist in the project | Pass | Artifact types named in both columns exist in the project. |
| 7 | The dictionary's `Language` and `Domain` rows, and the language of every row, match the PO language and domain in the project registry | Pass | `Language | en` and `Domain | it` match the registry; every row says `en`. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | Metadata of DICT-001 has `Language | en` and `Domain | it`; neither is a placeholder. |
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

Full review (not a delta) after the change for MIL-011 (menu bar).

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Criterion LANG 10 (Optional) failed: Abbreviations are spelled out on first use, in the stated language; fix or accept the deferral | S01 | 2026-10-21 |

---

[DICT-001]: ../../../docs/dictionary.md
[QC-DICT-001]: ../../../framework/qc/artifacts/qc-dictionary.md
[QC-LANG-001]: ../../../framework/qc/artifacts/qc-language-domain.md
