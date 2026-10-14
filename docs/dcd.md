# Design Class Diagram: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | DCD-001 |
| CrossReference | [DM-001], [SD-001], [DICT-001], [ADR-0002] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose and Scope

The design classes of the program in `src/flash_card/`, in four layers (domain, application, infrastructure, presentation) with the presentation pattern MVVM ([ADR-0002]). The classes refine the concepts of [DM-001]; names are the IT terms of [DICT-001]. Methods trace to the operation contracts of [OC-001] and the sequence diagrams of [SD-001] (the SSD messages are in [SSD-001]).

## Diagram

```plantuml
@startuml
package domain {
  class Card <<frozen>> {
    +front : str
    +back : str
  }
  class LanguagePair <<frozen>> {
    +front_code : str
    +back_code : str
  }
  class Vocabulary <<frozen>> {
    +language_pair : LanguagePair
    +cards : tuple[Card, ...]
  }
  class Deck {
    +language_pair : LanguagePair
    -_cards : list[Card]
    +from_vocabulary(vocabulary : Vocabulary) : Deck
    +cards : tuple[Card, ...]
    +is_empty : bool
    +draw(choose, exclude : Card | None) : Card
    +remove(card : Card) : None
  }
  interface VocabularyRepository {
    +load() : Vocabulary
  }
  interface ProgressRepository {
    +load() : Deck | None
    +save(deck : Deck) : None
  }
  class VocabularyError
  class VocabularyFormatError
  class VocabularyNotFoundError
  class EmptyDeckError
}
package application {
  class CardDto <<frozen>> {
    +front_text : str
    +back_text : str
    +front_language : str
    +back_language : str
  }
  interface SpeechPort {
    +speak(text : str, language_code : str) : None
  }
  class StudySession {
    -_deck : Deck
    -_progress : ProgressRepository
    -_speech : SpeechPort
    +current_card : CardDto | None
    +remaining : int
    +next_card() : CardDto | None
    +mark_known() : None
  }
  class open_study_session <<function>>
}
package infrastructure {
  class CsvVocabularyRepository {
    -_path : Path
    +load() : Vocabulary
  }
  class CsvProgressRepository {
    -_path : Path
    +load() : Deck | None
    +save(deck : Deck) : None
  }
  class GttsSpeech {
    +speak(text : str, language_code : str) : None
  }
  class NullSpeech {
    +speak(text : str, language_code : str) : None
  }
}
package presentation {
  class FlashCardViewModel {
    -_session : StudySession
    +side : Side
    +language_name : str
    +text : str
    +next_card() : None
    +flip_card() : None
    +is_known() : None
  }
  class FlashCardView {
    +flip_timer : str | None
    +next_card() : None
    +flip_card() : None
    +is_known() : None
  }
  class "app.main" as Main <<function>>
}
Vocabulary "1" *-- "1..*" Card
Vocabulary "1" --> "1" LanguagePair
Deck "1" o-- "0..*" Card
Deck ..> Vocabulary : built from
Deck ..> EmptyDeckError : raises
VocabularyFormatError --|> VocabularyError
VocabularyNotFoundError --|> VocabularyError
EmptyDeckError --|> VocabularyError
StudySession "1" --> "1" Deck
StudySession "1" --> "1" ProgressRepository
StudySession "1" --> "1" SpeechPort
StudySession ..> CardDto : returns
open_study_session ..> VocabularyRepository
open_study_session ..> ProgressRepository
open_study_session ..> StudySession : creates
CsvVocabularyRepository ..|> VocabularyRepository
CsvProgressRepository ..|> ProgressRepository
GttsSpeech ..|> SpeechPort
NullSpeech ..|> SpeechPort
FlashCardViewModel "1" --> "1" StudySession
FlashCardView "1" --> "1" FlashCardViewModel
Main ..> CsvVocabularyRepository : composes
Main ..> CsvProgressRepository : composes
Main ..> GttsSpeech : composes
Main ..> FlashCardView : composes
@enduml
```

## Class Table

| Class | Refines (Domain Model concept) | Responsibility | Attributes | Operations |
| --- | --- | --- | --- | --- |
| `Card` | Flash Card | Holds a word and its translation | `front`, `back` | none |
| `LanguagePair` | Word List (first and second language) | Names the two languages of a word list by code | `front_code`, `back_code` | none |
| `Vocabulary` | Word List | Holds all cards of a language pair as delivered | `language_pair`, `cards` | none |
| `Deck` | Words To Learn | Holds the cards still to learn and picks and removes cards | `language_pair`, `_cards` | `from_vocabulary`, `draw`, `remove` |
| `VocabularyRepository` | Word List | Port: load the delivered word list | none | `load` |
| `ProgressRepository` | Words To Learn | Port: load and save the words to learn | none | `load`, `save` |
| `StudySession` | Study Session | Runs one session: draws cards, marks cards known, saves progress, asks for speech | `_deck`, `_progress`, `_speech`, `_current` | `next_card`, `mark_known` |
| `CardDto` | Flash Card | Plain data that crosses to the presentation layer | four text fields | none |
| `SpeechPort` | (none: external service) | Port: speak a text in a language | none | `speak` |
| `CsvVocabularyRepository`, `CsvProgressRepository` | Word List, Words To Learn | Adapters that read and write the semicolon separated CSV file | `_path` | `load`, `save` |
| `GttsSpeech`, `NullSpeech` | (none) | Adapters for speech: the gTTS service, and silence | none | `speak` |
| `FlashCardViewModel` | Study Session | Exposes the side, language name and text of the card shown, and the three commands | `_session`, `side`, `language_name`, `text` | `next_card`, `flip_card`, `is_known` |
| `FlashCardView` | (none: user interface) | Draws the window, forwards the buttons, owns the 3000 ms timer | `flip_timer`, widgets | `next_card`, `flip_card`, `is_known` |

## Method Traceability

| Method signature | Operation Contract / SD message |
| --- | --- |
| `open_study_session(vocabulary_repository, progress_repository, speech, choose) -> StudySession` | [OC-001] `startStudySession`, [SD-001] sequence startStudySession (loads the words to learn) |
| `StudySession.next_card() -> CardDto \| None` | [OC-001] `startStudySession` (first card), `markUnknown`; [SD-001] |
| `StudySession.mark_known() -> None` | [OC-001] `markKnown` (remove and save); [SD-001] |
| `FlashCardViewModel.next_card() -> None` | [OC-001] `markUnknown`; [SD-001] |
| `FlashCardViewModel.is_known() -> None` | [OC-001] `markKnown`; [SD-001] |
| `FlashCardViewModel.flip_card() -> None` | [SSD-001] timer turn-over (no contract: started by the system's timer) |
| `FlashCardView.next_card()`, `.is_known()`, `.flip_card()` | the same three operations, forwarded from buttons and the timer; names are the assignment's |

## Pattern Annotations

| Pattern | Classes | Rationale |
| --- | --- | --- |
| Repository | `VocabularyRepository`, `ProgressRepository`, CSV adapters | The domain does not know the CSV file |
| Ports and adapters | `SpeechPort`, `GttsSpeech`, `NullSpeech` | Speech is an optional extra; the core runs without it |
| Null Object | `NullSpeech` | No `if speech:` checks in the use case |
| MVVM | `FlashCardView`, `FlashCardViewModel` | Behaviour is tested without Tkinter ([ADR-0002]) |
| Composition root | `app.main` | The one place that names the adapters |

## Dependency Check

Imports point inward: `domain` imports nothing from the other packages; `application` imports `domain`; `infrastructure` imports `application` and `domain`; `presentation` imports `application` and `domain`, and `app.main` additionally imports `infrastructure`. There is no cycle. `constants.py` imports nothing from the packages.

---

[DM-001]: ./domain-model.md
[DICT-001]: ./dictionary.md
[SSD-001]: ./uc-001/ssd.md
[OC-001]: ./uc-001/oc.md
[SD-001]: ./uc-001/sd.md
[ADR-0002]: ./adr/adr-0002-clean-architecture-and-mvvm.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
