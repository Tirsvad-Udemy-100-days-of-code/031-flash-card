# Arkitektur

🌐 [English](Architecture) · **Dansk** · [Bahasa Malaysia](Architecture-ms)

Programmet er bygget i fire lag under `src/flash_card/`. Importer peger indad; `lint-imports` kontrollerer det.

| Lag | Indeholder | Må importere |
| --- | --- | --- |
| `domain` | `Card`, `LanguagePair`, `Vocabulary`, `Deck`, fejlene og repository-grænsefladerne | ingenting |
| `application` | `StudySession`, `open_study_session`, `CardDto` og `SpeechPort` | `domain` |
| `infrastructure` | CSV-repositories og tale-adaptere | `application`, `domain` |
| `presentation` | `FlashCardView`, `FlashCardViewModel` (MVVM) og kompositionsroden `app.py` | alle lag |

Alle konstanter står i `src/flash_card/constants.py`.

## Hvor er hvert opgavetrin?

| Opgave | Kode |
| --- | --- |
| Trin 1: vindue, lærred, billede, tekster, knapper | `FlashCardView.__init__` i `presentation/features/flash_card/flash_card_view.py`; billederne laves af `tools/generate_images.py` |
| Trin 2: læs CSV, tilfældigt ord ved hvert tryk | `CsvVocabularyRepository` og `read_word_list` (erstatter `pandas`), `Deck.draw`, `StudySession.next_card`, `FlashCardView.next_card` |
| Trin 3: vend efter 3 sekunder | `FlashCardView.flip_card`, `FlashCardView.flip_timer` (`after`, `after_cancel`), `FlashCardViewModel.flip_card` |
| Trin 4: kendte ord, `words_to_learn.csv` | `FlashCardView.is_known`, `StudySession.mark_known`, `CsvProgressRepository`, `open_study_session` |
| Ekstra: tale | `SpeechPort`, `GttsSpeech`, `NullSpeech`, `build_speech` i `presentation/app.py` |

## Hvorfor en lagdelt løsning til en lille opgave?

Reglerne (hvilket kort der kommer næste gang, hvad et kendt ord gør) testes uden vindue og uden filsystem. Vinduet, CSV-filerne og taletjenesten kan udskiftes uden at røre reglerne. Se ADR-0001 og ADR-0002 i `docs/adr/`.

## Test

| Mappe | Hvad den tester |
| --- | --- |
| `tests/unit/` | Hvert lag for sig, med falske objekter til portene |
| `tests/integration/` | Den rigtige ordliste og fremgangsfilen i en midlertidig mappe |
| `tests/e2e/` | Det rigtige Tkinter-vindue (springes over uden skærm) |

## Projektdokumenter

Business case, plan, design og gennemgangsrapporter ligger i `docs/`. Arbejdet blev udført i syv milepæle, én pull request hver: se `docs/milestones/`.
