# Brug

🌐 [English](Usage) · **Dansk** · [Bahasa Malaysia](Usage-ms)

## Øv kortene

1. Start programmet med `python -m flash_card`.
2. Vælg et niveau: **100 words**, **1000 words** eller **All words**. Ordlisten er sorteret fra det hyppigste til det sjældneste ord, så niveau 100 er de 100 hyppigste ord.
3. Et kort viser et malajisk ord. Prøv at huske den danske oversættelse.
4. Efter tre sekunder vender kortet og viser oversættelsen.
5. Tryk på det grønne flueben, hvis du kendte ordet, eller på det røde kryds, hvis du ikke gjorde.
6. Et nyt tilfældigt ord fra niveauet vises. Gentag.

Et ord, du har markeret som kendt, fjernes og kommer ikke igen. Når der ikke er flere ord på niveauet, står der "Nothing left to learn" på kortet; start programmet igen og vælg et højere niveau.

## Din fremgang

- Første gang du trykker på det grønne flueben, skriver programmet `data/words_to_learn.csv` med de ord, du endnu ikke kan.
- Næste start bruger den fil. Findes den ikke, bruger programmet hele ordlisten `data/ms-da.csv`.
- For at starte forfra skal du slette `data/words_to_learn.csv`.
- Det røde kryds ændrer aldrig filen.
- Kendte ord forbliver kendte på alle niveauer. Niveauet begrænser kun, hvilke af de ord, du endnu ikke kender, der kommer frem, og filen beholder altid alle ord, du ikke kender, også dem uden for niveauet.
- Denne liste har 1000 ord, så "1000 words" og "All words" giver de samme kort.

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
| `--level {100,1000,all}` | Start på det niveau og spring niveauskærmen over |
| `--no-speech` | Udtal ikke det malajiske ord, selv om tilvalget til tale er installeret |

## Brug et andet sprogpar

Læg en fil med samme format i datamappen og kald den `ms-da.csv`, eller ret `VOCABULARY_FILE_NAME` og `LANGUAGE_NAMES` i `src/flash_card/constants.py`. Kodene i overskriften vises som sprognavne fra `LANGUAGE_NAMES`; ukendte koder vises med store bogstaver.

## Fejlfinding

| Problem | Hvad du skal gøre |
| --- | --- |
| `No module named tkinter` | Installer Tkinter (`python3-tk` på Debian og Ubuntu) |
| Ingen lyd | Installer tilvalget `speech` og tjek netværket; programmet logger en advarsel, når udtalen mislykkes |
| Programmet stopper med en meddelelse om filen | CSV-filen er forkert opbygget; meddelelsen nævner filen og linjen. Filen bliver ikke overskrevet |
