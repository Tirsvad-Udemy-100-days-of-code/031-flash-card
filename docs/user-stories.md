# User Stories: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | US-001 |
| CrossReference | [UCD-001], [BC-001], [UC-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005], [MIL-006] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose and Scope

These stories cover the epic "Study Flash Cards": the four steps of the course assignment (the window, new cards, flipping the cards, saving progress) and the spoken Malay word. Each story is delivered by one milestone. The wireframe the stories follow is in `docs/uc-001/wireframe.md`.

## Story List

### US-001.01 — See a flash card

**As a** Learner, **I want** a window that shows one flash card with the language name, a word and two buttons (known and unknown), **so that** I can see what I am asked to learn.

**Acceptance Criteria**

- Given the program is started, when the window opens, then it shows a card with the language name above a word, a button for "I do not know it" under the left side and a button for "I know it" under the right side.
- Given the window is open, when I look at the card, then the language name is in italics and the word is in bold, both centred on the card.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-002], [UC-001] | fits one iteration | none |

### US-001.02 — Get a new card

**As a** Learner, **I want** a new random word every time I press a button, **so that** I do not meet the words in a fixed order.

**Acceptance Criteria**

- Given a card is shown, when I press the known button or the unknown button, then a different random word from the word list is shown.
- Given the word list has one word, when I press a button, then that word is shown again and the program does not fail.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-003], [UC-001] | fits one iteration | none |

### US-001.03 — See the translation

**As a** Learner, **I want** the card to turn over after three seconds and show the translation, **so that** I can check my answer without asking for it.

**Acceptance Criteria**

- Given a new card is shown, when 3000 ms have passed, then the card shows the back image, the language name of the translation, the translation, and the text is white.
- Given a card was shown less than 3000 ms ago, when I press a button, then the earlier timer is cancelled and only the new card is flipped after its own 3000 ms.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-004], [UC-001] | fits one iteration | none |

### US-001.04 — Keep my progress

**As a** Learner, **I want** the words I know to stop coming up, and the words still to learn to be kept when I close the program, **so that** I am only tested on what I do not know.

**Acceptance Criteria**

- Given a card is shown, when I press the known button, then that word is removed from the words to learn and the remaining words are saved in `words_to_learn.csv`.
- Given `words_to_learn.csv` exists, when the program starts, then the cards come from that file.
- Given `words_to_learn.csv` does not exist, when the program starts, then the cards come from the word list `ms-da.csv`.
- Given all words are known, when the last known button is pressed, then the program shows a message that there is nothing left to learn and does not fail.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-005], [UC-001] | fits one iteration | none |

### US-001.05 — Hear the Malay word

**As a** Learner, **I want** to hear the Malay word when its card is shown, **so that** I learn how it is pronounced.

**Acceptance Criteria**

- Given the speech extra is installed and a network is available, when a card shows a Malay word, then the word is spoken in Malay.
- Given the speech extra is not installed or no network is available, when a card is shown, then the program works as without speech and does not show an error to the Learner.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-006], [UC-001] | fits one iteration | none |

## INVEST Check

All five stories are Independent in delivery order (each builds on the one before but can be accepted alone), Negotiable in wording, Valuable to the Learner, Estimable, Small (one milestone each) and Testable (every criterion is Given/When/Then). Exception: US-001.02 to US-001.05 depend on the window of US-001.01, which is stated in their milestones' Dependencies.

---

[UCD-001]: ./use-case-diagram.md
[BC-001]: ./business-case.md
[UC-001]: ./uc-001/uc.md
[MIL-002]: ./milestones/mil-002-step1-user-interface.md
[MIL-003]: ./milestones/mil-003-step2-new-flash-cards.md
[MIL-004]: ./milestones/mil-004-step3-flip-cards.md
[MIL-005]: ./milestones/mil-005-step4-save-progress.md
[MIL-006]: ./milestones/mil-006-malay-speech.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
