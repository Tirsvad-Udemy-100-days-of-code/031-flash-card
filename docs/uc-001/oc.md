# Operation Contracts: Study Flash Cards

## Metadata
| Key | Value |
| --- | --- |
| ID | OC-001 |
| CrossReference | [SSD-001], [DM-001], [DICT-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

The turn-over of the card after 3000 ms is started by the system's own timer, not by a message from the Learner, so it has no contract; it is realized in [SD-001].

## Contract: startStudySession

| Item | Value |
| --- | --- |
| Operation | `startStudySession(): CardDto \| None` |
| Traces to | `startStudySession` in [SSD-001] |
| Domain Model concepts | Study Session, Words To Learn, Word List, Flash Card ([DM-001]); IT terms `StudySession`, `Deck`, `Vocabulary`, `Card` ([DICT-001]) |

**Preconditions**

- A `Vocabulary` exists in the word list file.

**Postconditions**

- A `StudySession` instance was created.
- A `Deck` instance was created and associated with the `StudySession`.
- The `Deck` holds the cards of the progress file when it exists, otherwise a copy of the cards of the `Vocabulary`.
- When the `Deck` is not empty, `StudySession.current_card` was set to a card of the `Deck` and a `CardDto` of it is returned; otherwise `current_card` is `None` and `None` is returned.

**Exceptions**

| Condition (failing precondition) | Outcome |
| --- | --- |
| The word list file does not exist | `VocabularyNotFoundError` is raised; no session is created |
| The word list or progress file has no header of two cells, or a row with other than two cells | `VocabularyFormatError` is raised; no session is created and no file is changed |

## Contract: markKnown

| Item | Value |
| --- | --- |
| Operation | `markKnown(): None` |
| Traces to | `markKnown` in [SSD-001] |
| Domain Model concepts | Study Session, Words To Learn, Flash Card ([DM-001]); IT terms `StudySession`, `Deck`, `Card` ([DICT-001]) |

**Preconditions**

- A `StudySession` exists and its `current_card` is not `None`.

**Postconditions**

- The `Card` of `current_card` was removed from the `Deck` (the association was destroyed).
- The `Deck` was stored in the progress file.
- `StudySession.current_card` was set to `None`.

**Exceptions**

| Condition (failing precondition) | Outcome |
| --- | --- |
| `current_card` is `None` (no card is shown) | Nothing is changed and nothing is stored |

## Contract: markUnknown

| Item | Value |
| --- | --- |
| Operation | `markUnknown(): CardDto \| None` |
| Traces to | `markUnknown` in [SSD-001] |
| Domain Model concepts | Study Session, Words To Learn, Flash Card ([DM-001]); IT terms `StudySession`, `Deck`, `Card` ([DICT-001]) |

**Preconditions**

- A `StudySession` exists.

**Postconditions**

- `StudySession.current_card` was set to a card of the `Deck` that differs from the previous `current_card` when the `Deck` holds two or more cards, and a `CardDto` of it is returned.
- When the `Deck` is empty, `current_card` is `None` and `None` is returned.
- The `Deck` and the progress file are unchanged.
- The Malay word of the new `current_card` was passed to the `SpeechPort`.

**Exceptions**

| Condition (failing precondition) | Outcome |
| --- | --- |
| The `Deck` is empty | `None` is returned; nothing is spoken |

---

[SSD-001]: ./ssd.md
[DM-001]: ../domain-model.md
[DICT-001]: ../dictionary.md
[SD-001]: ./sd.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
