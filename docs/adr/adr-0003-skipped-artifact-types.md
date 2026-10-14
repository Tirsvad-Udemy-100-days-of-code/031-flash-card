# ADR-0003: Artifact types skipped for this project

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0003 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The framework lists more artifact types than a one-week, single-person learning project needs. The journey of the `create-project` skill makes the baseline (`BC`, `SA`, `PP`, `MIL`) mandatory and every other type optional, but requires the reason for a skipped step to be recorded. Options: (1) create every type, which doubles the documents for one person and a 1000 word program; (2) create the baseline, the use case chain the code is traced to (`UCD`, `US`, `UC`, `DM`, `SSD`, `OC`, `SD`, `DCD`, `DICT`) and skip the types that add no information here.

## Decision

Option 2 is chosen. These types are not created in this project, for the reasons given:

| Type | Reason |
| --- | --- |
| `KPI`, `BMC`, `BPMN` | One owner, no revenue and no business process; the measurable success criteria are in the Business Case |
| `RA` | The idea is not a hunch: the assignment specifies the behaviour, so there is no belief to test before the Business Case |
| `GOV` | One person owns, builds and approves; the review workflow is the framework's own and the autonomous mode records stand-in reviews |
| `ERD` | The only persistence is two CSV files with the same two columns, described in the adapters of the Design Class Diagram |
| `TRN`, `TRR` | No reviewer training for a single-person project |

## Consequences

**Positive:**

- Less documentation to keep in step for a small program.
- Reviews concentrate on the documents that carry the decisions.

**Negative:**

- A later contributor finds no governance document; the review records show who stood in.
- If persistence grows beyond a CSV file, an `ERD` must be added in that change.

## Affected Artifacts

- [BC-001] — the success criterion on review coverage counts only created artifacts

---

[BC-001]: ../business-case.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
