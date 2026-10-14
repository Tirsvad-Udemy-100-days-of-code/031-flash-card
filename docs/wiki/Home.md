# Flash Card

🌐 **English** · [Dansk](Home-da) · [Bahasa Malaysia](Home-ms)

A flash card program for learning the most frequent Malay words with their Danish translations. It is the solution of day 31 of Udemy's *100 Days of Code: The Complete Python Pro Bootcamp*.

![The level screen: choose 100 words, 1000 words or all words](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-level.png)
![The front of a card: the Malay word](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-front.png)
![The back of the card after three seconds: the Danish translation](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-back.png)

| Page | Read it when you want to |
| --- | --- |
| [Install](Install) | Create the `.venv`, install the program and run the tests |
| [Usage](Usage) | Study the cards, understand the progress file, use the options |
| [Architecture](Architecture) | See the layers and find the code of each assignment step |

## The four assignment steps

| Step | What the program does | Milestone |
| --- | --- | --- |
| 1. User interface | A window with a card and two buttons | MIL-002 |
| 2. New flash cards | A random word from the word list on every button press | MIL-003 |
| 3. Flip the cards | After 3 seconds the card shows the Danish translation | MIL-004 |
| 4. Save your progress | Known words are removed and the rest is saved in `words_to_learn.csv` | MIL-005 |
| Extra | The Malay word is spoken (optional) | MIL-006 |
| Extra | You choose a level first: the first 100 words, the first 1000 words or all words | MIL-008 |

## For course participants

The function names of the assignment are kept: `next_card`, `flip_card`, `is_known`, and the attributes `flip_timer` and `current_card`. The data is read with the standard library `csv` module instead of `pandas`, so the core program has no runtime dependency.

Repository: <https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card>
