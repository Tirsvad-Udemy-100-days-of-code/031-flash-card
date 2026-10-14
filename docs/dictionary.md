# Domain Dictionary: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | DICT-001 |
| CrossReference | [BC-001], [SA-001], [DM-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added the term Level | [0b983b7] |

---

## Purpose and Scope

Maps each Product Owner (PO) term to its professional IT term. PO language: English (`en`), domain: Software and IT (`it`), from the registry's `Languages` section. The PO terms are the words of a language learner; the IT terms are the class and function names of the code.

## Dictionary

| PO term | Language | IT term | Definition | Used as PO term in | Used as IT term in |
| --- | --- | --- | --- | --- | --- |
| Flash card | en | `Card` | A word in one language together with its translation in another language. | DM, UC, US | DCD |
| Word list | en | `Vocabulary` | The complete set of flash cards of one language pair, as delivered with the program. | DM, UC, US | DCD |
| Words to learn | en | `Deck` | The flash cards the learner does not yet know; it starts as the word list and only gets smaller. | DM, UC, US | DCD |
| Study session | en | `StudySession` | One run of the program in which the learner is shown cards one by one. | DM, UC, US | DCD |
| Level | en | `Level` | The number of the most frequent words of the word list that a study session uses: 100, 1000 or all. | DM, UC, US | DCD |
| Language pair | en | `LanguagePair` | The two languages of a word list, the language learned and the language of the translation. | DM, UC | DCD |
| Progress file | en | `ProgressRepository` | The file `words_to_learn.csv` that keeps the words to learn between runs. | UC, US | DCD |
| Spoken word | en | `SpeechPort` | The Malay word read aloud when its card is shown. | UC, US | DCD |

## Rules

- The Domain Model, use cases and user stories use the PO term; the Operation Contract, Sequence Diagram, Design Class Diagram and ERD use the IT term.
- One IT term per PO term and one PO term per IT term; no synonyms.
- "Card" alone means a flash card; "front" is its word in the language learned and "back" is its translation, and the card on screen shows one of them at a time.

---

[BC-001]: ./business-case.md
[SA-001]: ./stakeholder-analysis.md
[DM-001]: ./domain-model.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
[0b983b7]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/0b983b7fdadf6958717c1d0227d0f2ebe037f7b1
