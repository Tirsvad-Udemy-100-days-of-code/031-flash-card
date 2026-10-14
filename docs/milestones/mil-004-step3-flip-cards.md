# MIL-004: Step 3 - Flip the cards

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001], [US-001], [UC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose

Decide whether assignment step 3 works: three seconds after a card appears, it turns over and shows the Danish translation.

## Deliverable

After 3000 ms the card shows `card_back.png`, the language name "Danish", the translation, and white text. A button press shows the front of a new card with black text and restarts the timer; a press before the 3000 ms have passed cancels the earlier timer.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `FlashCardViewModel.flip_card` changes the side to the back, the language name to the back language and the text to the translation | Unit test passes | Any other state |
| 2 | `next_card` returns the side to the front | Unit test passes | Side stays on the back |
| 3 | The view schedules `flip_card` with `after(3000, ...)` and cancels the earlier timer with `after_cancel` before scheduling a new one | e2e test with a recording scheduler, or a unit test of the view with a fake root | Timer leaks or fires twice |
| 4 | The back uses `card_back.png` and white text; the front uses `card_front.png` and black text | e2e test reads the canvas item configuration | Any difference |
| 5 | `PhotoImage` objects are created once, outside the callbacks | Code review | An image is created in a function |
| 6 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest` exits with 0 | `RC-*` verdict Go and exit code 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | Cards with a front and a back to turn |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 1, step 3 | [BC-001] |
| US-001.03 See the translation | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-17 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add the card side to the view model | `Side` enum (front, back) and `flip_card` on the view model, so the language name and text change with the side without Tkinter. | Yes | US-001.03 |
| 2 | Flip the card after 3000 ms in the view | `FlashCardView.flip_card` swaps image, text colour, title and word with `itemconfig`; `flip_timer` holds the `after` id and is cancelled with `after_cancel` on every button press, as the assignment's hints say. | Yes | US-001.03 |
| 3 | Test the flip | View model unit tests for both sides, and an e2e test with the real timer replaced by a recording `after`/`after_cancel` pair. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
