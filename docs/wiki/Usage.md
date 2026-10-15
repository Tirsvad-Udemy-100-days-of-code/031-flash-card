# Usage

🌐 **English** · [Dansk](Usage-da) · [Bahasa Malaysia](Usage-ms)

## Study the cards

1. Start the program with `python -m flash_card`.
2. Choose a level: **100 words**, **1000 words** or **All words**. The word list is ordered from the most to the least frequent word, so level 100 is the 100 most frequent words.
3. A card shows a Malay word. Try to remember its Danish translation.
4. After three seconds the card turns over and shows the translation.
5. Press the green tick when you knew the word, or the red cross when you did not.
6. A new random word of the level appears. Repeat.

A word you marked as known is removed and does not come up again. When no word of the level is left, the card says "Nothing left to learn"; restart the program and choose a higher level.

## The menu bar

![The window with the menu bar](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-menu.png)

| Menu | Command | What it does |
| --- | --- | --- |
| File | Open... | Opens another word list from a CSV file (header with two language codes, for example `en;da`). Progress is kept apart for each list |
| File | Change level... | Shows the level choice again without a restart; known words stay known |
| File | Reset word list... | After a confirmation removes the progress of the open list, so all its words are to learn again; the list file is not changed |
| File | Exit | Closes the program |
| About | Contact | The author, Jens Tirsvad Nielsen, Software engineer; opens the LinkedIn page in your browser |

The progress of the delivered `ms-da.csv` is `data/words_to_learn.csv`; another list gets `data/words_to_learn_<name>.csv`. The opened list is not remembered after a restart.

## Your progress

- The first time you press the green tick, the program writes `data/words_to_learn.csv` with the words you do not know yet.
- The next start uses that file. If it does not exist, the program uses the full word list `data/ms-da.csv`.
- To start again, delete `data/words_to_learn.csv`.
- The red cross never changes the file.
- Known words stay known at every level. The level only limits which of the words you do not know yet come up, and the file always keeps every word you do not know, also those outside the level.
- This list has 1000 words, so "1000 words" and "All words" give the same cards.

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
| `--level {100,1000,all}` | Start at that level and skip the level screen |
| `--no-speech` | Do not speak the Malay word, even when the speech extra is installed |

## Use another language pair

Put a file with the same format in the data folder and name it `ms-da.csv`, or change `VOCABULARY_FILE_NAME` and `LANGUAGE_NAMES` in `src/flash_card/constants.py`. The header codes are shown as language names from `LANGUAGE_NAMES`; unknown codes are shown in upper case.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `No module named tkinter` | Install Tkinter (`python3-tk` on Debian and Ubuntu) |
| No sound | Install the `speech` extra and check the network; the program logs a warning when speaking fails |
| The program stops with a message about the file | The CSV file is malformed; the message names the file and the line. The file is not overwritten |
