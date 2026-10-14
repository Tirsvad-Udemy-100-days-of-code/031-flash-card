# Seni bina

🌐 [English](Architecture) · [Dansk](Architecture-da) · **Bahasa Malaysia**

Program dibina dalam empat lapisan di bawah `src/flash_card/`. Import menuju ke dalam; `lint-imports` memeriksanya.

| Lapisan | Mengandungi | Boleh mengimport |
| --- | --- | --- |
| `domain` | `Card`, `LanguagePair`, `Vocabulary`, `Deck`, ralat dan antara muka repositori | tiada |
| `application` | `StudySession`, `open_study_session`, `CardDto` dan `SpeechPort` | `domain` |
| `infrastructure` | Repositori CSV dan penyesuai suara | `application`, `domain` |
| `presentation` | `FlashCardView`, `FlashCardViewModel` (MVVM) dan akar komposisi `app.py` | semua lapisan |

Semua pemalar terdapat dalam `src/flash_card/constants.py`.

## Di manakah setiap langkah tugasan?

| Tugasan | Kod |
| --- | --- |
| Langkah 1: tetingkap, kanvas, imej, teks, butang | `FlashCardView.__init__` dalam `presentation/features/flash_card/flash_card_view.py`; imej dibuat oleh `tools/generate_images.py` |
| Langkah 2: baca CSV, perkataan rawak setiap tekanan | `CsvVocabularyRepository` dan `read_word_list` (menggantikan `pandas`), `Deck.draw`, `StudySession.next_card`, `FlashCardView.next_card` |
| Langkah 3: terbalik selepas 3 saat | `FlashCardView.flip_card`, `FlashCardView.flip_timer` (`after`, `after_cancel`), `FlashCardViewModel.flip_card` |
| Langkah 4: perkataan diketahui, `words_to_learn.csv` | `FlashCardView.is_known`, `StudySession.mark_known`, `CsvProgressRepository`, `open_study_session` |
| Tambahan: suara | `SpeechPort`, `GttsSpeech`, `NullSpeech`, `build_speech` dalam `presentation/app.py` |

## Mengapa program berlapis untuk tugasan kecil?

Peraturan (kad mana yang seterusnya, apa yang berlaku apabila perkataan diketahui) diuji tanpa tetingkap atau sistem fail. Tetingkap, fail CSV dan perkhidmatan suara boleh diganti tanpa menyentuh peraturan. Lihat ADR-0001 dan ADR-0002 dalam `docs/adr/`.

## Ujian

| Folder | Apa yang diuji |
| --- | --- |
| `tests/unit/` | Setiap lapisan sendiri, dengan objek palsu untuk port |
| `tests/integration/` | Senarai perkataan sebenar dan fail kemajuan dalam folder sementara |
| `tests/e2e/` | Tetingkap Tkinter sebenar (dilangkau tanpa paparan) |

## Dokumen projek

Kes perniagaan, pelan, reka bentuk dan rekod semakan terdapat dalam `docs/`. Kerja dilakukan dalam tujuh pencapaian, satu pull request setiap satu: lihat `docs/milestones/`.
