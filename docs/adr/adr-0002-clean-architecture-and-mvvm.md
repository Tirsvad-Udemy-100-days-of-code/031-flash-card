# ADR-0002: Clean architecture with MVVM for the Tkinter program

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0002 |
| CrossReference | [BC-001], [DM-001], [DCD-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The assignment solution is a single script with global variables (`current_card`, `to_learn`, `flip_timer`). The project's coding standard (QC-PY-001, criteria 14 to 17) asks for layers that point inward, ports for external services and a presentation pattern. The program is small, so a full layering has a cost in files. Options:

1. One module with the assignment's globals: closest to the course, but behaviour cannot be tested without a display and rules are mixed with Tkinter.
2. The four layers (domain, application, infrastructure, presentation) with MVVM: behaviour is testable, the assignment's function names live on in the view and view model.
3. Layers without a view model: the view would hold the rules again.

## Decision

The program is built in four layers under `src/flash_card/` with MVVM in the presentation layer. The function names of the assignment (`next_card`, `flip_card`, `is_known`) are kept on the view and on the view model, and the names `current_card` and `flip_timer` are kept where the concept exists (`StudySession.current_card`, `FlashCardView.flip_timer`); the course's `to_learn` list is the `Deck`.

## Consequences

**Positive:**

- The rules (draw, remove, persist) are tested without Tkinter or a file system.
- Replacing the CSV file or the speech service touches one adapter.
- The wiki can map each assignment step to the file that implements it.

**Negative:**

- More files than the course solution; a beginner needs the wiki's map to find the assignment's code.
- Layer boundaries need discipline (DTO at the boundary, one composition root).

## Affected Artifacts

- [DM-001] — concepts refined by the domain layer
- [DCD-001] — the class design this ADR constrains
- [BC-001] — objective 5, step by step delivery

---

[BC-001]: ../business-case.md
[DM-001]: ../domain-model.md
[DCD-001]: ../dcd.md
