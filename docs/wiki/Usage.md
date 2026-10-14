# Usage

🌐 **English** · [Dansk](Usage-da) · [Bahasa Malaysia](Usage-ms)

## Study the cards

1. Start the program with `python -m flash_card`.
2. A card shows a Malay word. Try to remember its Danish translation.
3. After three seconds the card turns over and shows the translation.
4. Press the green tick when you knew the word, or the red cross when you did not.
5. A new random word appears. Repeat.

A word you marked as known is removed and does not come up again. When no word is left, the card says "Nothing left to learn".

## Your progress

- The first time you press the green tick, the program writes `data/words_to_learn.csv` with the words you do not know yet.
- The next start uses that file. If it does not exist, the program uses the full word list `data/ms-da.csv`.
- To start again, delete `data/words_to_learn.csv`.
- The red cross never changes the file.

## File format

Both files are UTF-8 text with one card per line and the cells separated by a semicolon. The first line holds the two language codes.

```text
ms;da
aku;mig
yang;hvilke
```

## Options

| Option | Meaning |
| --- | --- |
| `--data-dir <folder>` | Folder that holds `ms-da.csv` and `words_to_learn.csv` (default: `data/` of the repository) |
| `--no-speech` | Do not speak the Malay word, even when the speech extra is installed |

## Use another language pair

Put a file with the same format in the data folder and name it `ms-da.csv`, or change `VOCABULARY_FILE_NAME` and `LANGUAGE_NAMES` in `src/flash_card/constants.py`. The header codes are shown as language names from `LANGUAGE_NAMES`; unknown codes are shown in upper case.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `No module named tkinter` | Install Tkinter (`python3-tk` on Debian and Ubuntu) |
| No sound | Install the `speech` extra and check the network; the program logs a warning when speaking fails |
| The program stops with a message about the file | The CSV file is malformed; the message names the file and the line. The file is not overwritten |
