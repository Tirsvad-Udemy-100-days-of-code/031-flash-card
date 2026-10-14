# Data

| File | Content | In git |
| --- | --- | --- |
| `ms-da.csv` | The word list: 1000 of the most frequent Malay words with a Danish translation | yes |
| `words_to_learn.csv` | The words you have not marked as known; created by the program | no (`.gitignore`) |

## Format

- UTF-8 text, one card per line, cells separated by a semicolon (`;`).
- The first line is a header with the two language codes: `ms;da` (Malay, Danish).
- Blank lines are ignored.
- `words_to_learn.csv` has the same format, so it can be used as a word list.

## Origin

The Malay words are a frequency list built from film and series subtitles (the *FrequencyWords* lists by the GitHub user `hermitdave`). The Danish column was filled with machine translation in a spreadsheet, as the course suggests. A word can therefore have a translation that does not fit its use; edit the file if you find one.

## Start again

Delete `words_to_learn.csv`. The next start uses `ms-da.csv`.
