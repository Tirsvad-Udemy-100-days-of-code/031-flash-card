# Brug

🌐 [English](Usage) · **Dansk** · [Bahasa Malaysia](Usage-ms)

## Øv kortene

1. Start programmet med `python -m flash_card`.
2. Et kort viser et malajisk ord. Prøv at huske den danske oversættelse.
3. Efter tre sekunder vender kortet og viser oversættelsen.
4. Tryk på det grønne flueben, hvis du kendte ordet, eller på det røde kryds, hvis du ikke gjorde.
5. Et nyt tilfældigt ord vises. Gentag.

Et ord, du har markeret som kendt, fjernes og kommer ikke igen. Når der ikke er flere ord, står der "Nothing left to learn" på kortet.

## Din fremgang

- Første gang du trykker på det grønne flueben, skriver programmet `data/words_to_learn.csv` med de ord, du endnu ikke kan.
- Næste start bruger den fil. Findes den ikke, bruger programmet hele ordlisten `data/ms-da.csv`.
- For at starte forfra skal du slette `data/words_to_learn.csv`.
- Det røde kryds ændrer aldrig filen.

## Filformat

Begge filer er UTF-8-tekst med ét kort pr. linje og cellerne adskilt af semikolon. Første linje har de to sprogkoder.

```text
ms;da
aku;mig
yang;hvilke
```

## Indstillinger

| Indstilling | Betydning |
| --- | --- |
| `--data-dir <mappe>` | Mappen med `ms-da.csv` og `words_to_learn.csv` (standard: `data/` i repositoryet) |
| `--no-speech` | Udtal ikke det malajiske ord, selv om tilvalget til tale er installeret |

## Brug et andet sprogpar

Læg en fil med samme format i datamappen og kald den `ms-da.csv`, eller ret `VOCABULARY_FILE_NAME` og `LANGUAGE_NAMES` i `src/flash_card/constants.py`. Kodene i overskriften vises som sprognavne fra `LANGUAGE_NAMES`; ukendte koder vises med store bogstaver.

## Fejlfinding

| Problem | Hvad du skal gøre |
| --- | --- |
| `No module named tkinter` | Installer Tkinter (`python3-tk` på Debian og Ubuntu) |
| Ingen lyd | Installer tilvalget `speech` og tjek netværket; programmet logger en advarsel, når udtalen mislykkes |
| Programmet stopper med en meddelelse om filen | CSV-filen er forkert opbygget; meddelelsen nævner filen og linjen. Filen bliver ikke overskrevet |
