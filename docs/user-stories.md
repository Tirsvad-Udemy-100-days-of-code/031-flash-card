# User Stories: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | US-001 |
| CrossReference | [UCD-001], [BC-001], [UC-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005], [MIL-006], [MIL-008], [MIL-009], [MIL-010], [MIL-011] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added US-001.09 to US-001.12 (menu bar) | [2211d0f] |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | US-001.08 names the latest release instead of v0.1.0 | [0264b60] |

---

## Purpose and Scope

These stories cover the epic "Study Flash Cards": the four steps of the course assignment (the window, new cards, flipping the cards, saving progress), the spoken Malay word the choice of level the start without an installed Python the download of the executable from a release and the menu bar. Each story is delivered by one milestone. The wireframe the stories follow is in `docs/uc-001/wireframe.md`.

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

### US-001.08 — Download the executable

**As a** Learner, **I want** to download the executable from a release page of the repository, **so that** I can use the program without building it.

**Acceptance Criteria**

- Given a release exists (for example `v0.2.0`), when I open the releases page of the repository, then I find release notes and, when the git host accepts the upload, `flash-card.exe` and a checksum file attached to it.
- Given I downloaded `flash-card.exe`, when I compute its SHA-256 hash, then it equals the value in the checksum file and in the release notes.
- Given I read the release notes, when I look for what the file is, then they say that it is an unsigned Windows build, what the `data` folder next to it holds, and how to build it myself.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-010], [UC-001] | fits one iteration | none |

### US-001.09 — Open another word list

**As a** Learner, **I want** to open another word list from a CSV file with the File menu, **so that** I can learn another language pair than the one delivered.

**Acceptance Criteria**

- Given the program is running, when I choose File, Open, then a file dialog lets me pick a CSV file that starts in the data folder.
- Given I picked a valid word list, when the dialog closes, then I choose a level and the cards come from that list, and my progress in it is kept apart from the progress in other lists.
- Given I picked a file that is not a word list (no header of two language codes, or a row that is not two cells), when the dialog closes, then a message names the problem and the earlier word list stays in use.
- Given I cancel the dialog, when it closes, then nothing changes.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-011], [UC-001] | fits one iteration | none |

### US-001.10 — Change the level while learning

**As a** Learner, **I want** to change the level from the File menu, **so that** I do not have to restart the program to make the word list easier or harder.

**Acceptance Criteria**

- Given a card is shown, when I choose File, Change level, then I see the level choices again.
- Given I choose a level, when the cards continue, then they come from that level and the words I know stay known.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-011], [UC-001] | fits one iteration | none |

### US-001.11 — Learn a word list from the start again

**As a** Learner, **I want** to reset the current word list from the File menu, **so that** all its words are to learn again.

**Acceptance Criteria**

- Given a word list is open, when I choose File, Reset word list, then I am asked to confirm and the message names the word list.
- Given I confirm, when the reset is done, then the progress of that word list is gone, all its words are to learn again and the level choice is shown; the progress of other word lists and the word list file itself are not changed.
- Given I do not confirm, when the question closes, then nothing changes.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-011], [UC-001] | fits one iteration | none |

### US-001.12 — Find the author and leave the program

**As a** Learner, **I want** an About menu with the author's contact and a File, Exit command, **so that** I can reach the author and close the program in the usual way.

**Acceptance Criteria**

- Given the program is running, when I choose About, Contact, then I see an entry with the author's name and title (Jens Tirsvad Nielsen, Software engineer) and, when I choose it, the author's LinkedIn page opens in my web browser.
- Given the program is running, when I choose File, Exit, then the window closes and the program ends.

| Traces to | Size | INVEST exceptions |
| --- | --- | --- |
| [MIL-011], [UC-001] | fits one iteration | none |

## INVEST Check

All twelve stories are Independent in delivery order (each builds on the one before but can be accepted alone), Negotiable in wording, Valuable to the Learner, Estimable, Small (one milestone each) and Testable (every criterion is Given/When/Then). Exception: US-001.02 to US-001.12 depend on the window of US-001.01, which is stated in their milestones' Dependencies.

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
[MIL-010]: ./milestones/mil-010-release.md
[MIL-011]: ./milestones/mil-011-menu-bar.md
[2211d0f]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/2211d0f4cbd8182314d18cbdefd939ae50c39e6d
[0264b60]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0264b6084f26bac5af716ea71596ce3be961fec8
