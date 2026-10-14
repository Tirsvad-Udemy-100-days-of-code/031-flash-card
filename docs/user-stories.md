# User Stories: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | US-001 |
| CrossReference | [UCD-001], [BC-001], [UC-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005], [MIL-006], [MIL-008], [MIL-009] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |
| 2026-10-14 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added US-001.06 Choose my level | [0b983b7] |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added US-001.07 Start without Python | pending |

---

## Purpose and Scope

These stories cover the epic "Study Flash Cards": the four steps of the course assignment (the window, new cards, flipping the cards, saving progress), the spoken Malay word the choice of level and the start without an installed Python. Each story is delivered by one milestone. The wireframe the stories follow is in `docs/uc-001/wireframe.md`.

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

### US-001.06 — Choose my level

**As a** Learner, **I want** to choose a level of 100 words, 1000 words or all words before I start, **so that** I begin with the most frequent words and widen the list when I am ready.

**Acceptance Criteria**

- Given the program is started, when the window opens, then I see the choices 100 words, 1000 words and All words, and no card yet.
- Given I choose a level of N words, when the first card is shown, then every card comes from the first N words of the word list, which is ordered from the most to the least frequent word.
- Given I choose 1000 words or All words and the word list has fewer words than that, when the cards are drawn, then all words of the word list are used.
- Given I have marked words as known at one level, when I choose another level, then the known words stay known and only the words of the chosen level that I do not know yet come up.
- Given every word of the chosen level is known, when the level is chosen, then the program tells me that there is nothing left to learn at this level.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-008], [UC-001] | fits one iteration | none |

### US-001.07 — Start without Python

**As a** Learner, **I want** to start the program by opening one executable file, **so that** I can learn without installing Python or a virtual environment.

**Acceptance Criteria**

- Given the executable was built, when I open it on a Windows computer without Python, then the level screen appears and no console window opens.
- Given I mark a word as known in the executable, when I open it again, then the known word does not come up (my progress is kept in `data/words_to_learn.csv` next to the executable).
- Given a `data/ms-da.csv` exists next to the executable, when the program starts, then that word list is used; otherwise the word list inside the executable is used.
- Given the speech extra was included in the build and a network is available, when a card is shown, then the Malay word is spoken; without a network the program works silently.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-009], [UC-001] | fits one iteration | none |

## INVEST Check

All seven stories are Independent in delivery order (each builds on the one before but can be accepted alone), Negotiable in wording, Valuable to the Learner, Estimable, Small (one milestone each) and Testable (every criterion is Given/When/Then). Exception: US-001.02 to US-001.07 depend on the window of US-001.01, which is stated in their milestones' Dependencies.

---

[UCD-001]: ./use-case-diagram.md
[BC-001]: ./business-case.md
[UC-001]: ./uc-001/uc.md
[MIL-002]: ./milestones/mil-002-step1-user-interface.md
[MIL-003]: ./milestones/mil-003-step2-new-flash-cards.md
[MIL-004]: ./milestones/mil-004-step3-flip-cards.md
[MIL-005]: ./milestones/mil-005-step4-save-progress.md
[MIL-006]: ./milestones/mil-006-malay-speech.md
[MIL-008]: ./milestones/mil-008-choose-level.md
[MIL-009]: ./milestones/mil-009-executable.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
[0b983b7]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0b983b7fdadf6958717c1d0227d0f2ebe037f7b1
