# UC-001: Study Flash Cards

## Metadata
| Key | Value |
| --- | --- |
| ID | UC-001 |
| CrossReference | [UCD-001], [US-001], [SA-001], [DM-001], [SSD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

**Format:** Fully Dressed

## Fully Dressed

- **Scope:** Flash Card program
- **Level:** user-goal
- **Primary Actor:** Learner
- **Stakeholders and Interests:**
  - S01 — learns the Malay words and wants only unknown words to come up
  - S02 — wants to see the assignment's behaviour step by step
- **Preconditions:**
  - A word list exists.
  - A display is available.
- **Postconditions (success guarantee):**
  - The words the Learner marked as known are no longer in the words to learn.
  - The words to learn are kept, so that the next session starts from them.

### Main Success Scenario

1. The Learner starts the program.
2. The system loads the words to learn: from the kept progress when it exists, otherwise from the word list.
3. The system shows a random card with the word in Malay.
4. After three seconds the system turns the card over and shows the translation in Danish.
5. The Learner states that the word is known.
6. The system removes the word from the words to learn and keeps the words to learn.
7. The system shows a new random card, and the Learner repeats from step 4 until no word is left.

### Extensions (Alternative / Exception Flows)

- 3a. Spoken words are available on the Learner's machine:
  1. The system speaks the Malay word. If speaking fails, the system logs it and goes on.
- 5a. The Learner states that the word is not known:
  1. The system keeps the word in the words to learn and shows a new random card; the Learner goes on at step 4.
- 5b. The Learner answers before three seconds have passed:
  1. The system cancels the turn-over of the card being shown and starts a new one for the next card.
- 7a. No word is left:
  1. The system tells the Learner that there is nothing left to learn, and further answers change nothing.
- 2a. The kept progress or the word list is unreadable:
  1. The system reports the problem to the Learner and ends; it does not overwrite the kept progress.

### Special Requirements / Business Rules

| Step | Rule |
| --- | --- |
| 3, 7 | The next card is chosen at random from the words to learn |
| 4 | The turn-over comes three seconds after the card appears |
| 6 | A word is identified by its Malay and Danish text; the first equal word is removed |
| 2 | The word list names its two languages and holds one word and one translation per card |

### Open Issues

- Starting again (resetting the kept progress) is not offered in the program; deleting the kept progress does it.

---

[UCD-001]: ../use-case-diagram.md
[US-001]: ../user-stories.md
[SA-001]: ../stakeholder-analysis.md
[DM-001]: ../domain-model.md
[SSD-001]: ./ssd.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
