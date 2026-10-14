# Domain Model: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | DM-001 |
| CrossReference | [UC-001], [UCD-001], [SSD-001], [DICT-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose and Scope

Covers: [UC-001] Study Flash Cards. The model holds the concepts a Learner talks about: the flash card, the word list, the words to learn and the study session. The project-level model is this document; no other use case exists.

## Diagram

Concepts, attributes and associations only — no operations.

```plantuml
@startuml
class "Flash Card" as FlashCard {
  word in the first language
  translation in the second language
}
class "Word List" as WordList {
  first language
  second language
}
class "Words To Learn" as WordsToLearn
class "Study Session" as StudySession {
  card shown
  side shown
}
WordList "1" o-- "1..*" FlashCard : holds
WordsToLearn "1" o-- "0..*" FlashCard : holds
WordsToLearn "1" --> "1" WordList : starts as a copy of
StudySession "1" --> "1" WordsToLearn : works through
StudySession "1" --> "0..1" FlashCard : shows
@enduml
```

## Concept Table

| Concept | Definition | Attributes | Source (use case / glossary) |
| --- | --- | --- | --- |
| Flash Card | A word in one language with its translation in another | word, translation | UC-001 steps 3 and 4 ("card", "translation") |
| Word List | The complete set of flash cards of a language pair, as delivered with the program | first language, second language | UC-001 step 2 ("word list") |
| Words To Learn | The flash cards the Learner does not yet know; starts as the word list and only gets smaller | none | UC-001 steps 2 and 6 ("words to learn") |
| Study Session | One run of the program in which the Learner is shown cards | card shown, side shown | UC-001 main scenario |

## Association Table

| From | Association (reading direction) | To | Multiplicity |
| --- | --- | --- | --- |
| Word List | holds | Flash Card | 1 to 1..* |
| Words To Learn | holds | Flash Card | 1 to 0..* |
| Words To Learn | starts as a copy of | Word List | 1 to 1 |
| Study Session | works through | Words To Learn | 1 to 1 |
| Study Session | shows | Flash Card | 1 to 0..1 |

## Generalizations

| General | Specializations | Is-a justification |
| --- | --- | --- |
| none | none | no generalization exists in this domain |

---

[UC-001]: ./uc-001/uc.md
[UCD-001]: ./use-case-diagram.md
[SSD-001]: ./uc-001/ssd.md
[DICT-001]: ./dictionary.md
