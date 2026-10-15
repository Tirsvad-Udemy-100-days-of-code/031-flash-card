# Installation

🌐 [English](Install) · **Dansk** · [Bahasa Malaysia](Install-ms)

## Krav

- Python 3.13 eller nyere med Tkinter (på Debian eller Ubuntu: `sudo apt install python3-tk`).
- `git`.
- Valgfrit: en internetforbindelse og tilvalget `speech`, hvis du vil høre det malajiske ord.

## Hent koden

```bash
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card.git
cd 031-flash-card
```

## Opret og brug et lokalt virtuelt miljø

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux og macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

- `.[dev]` tilføjer `pytest`, `ruff`, `mypy` og `import-linter`. Brug `.`, hvis du kun vil køre programmet.
- Hvis PowerShell nægter at køre `Activate.ps1`, så kør `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` én gang.
- Forlad miljøet med `deactivate`; slet mappen `.venv` for at starte forfra.

## Udtalt malajisk ord (valgfrit)

```bash
python -m pip install -e ".[speech]"
```

Det installerer `gTTS` og `playsound==1.2.2`. Uden tilvalget virker programmet uden lyd.

## Kør og test

```bash
python -m flash_card
python -m pytest
```

Vinduestesten i `tests/e2e/` springes over, når der ikke er en skærm.

## Download programfilen (Windows)

Hent `flash-card.exe` og `flash-card.exe.sha256` fra [udgivelsessiden](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.1.0). Sammenlign filens SHA-256-hash med kontrolsumfilen (`certutil -hashfile flash-card.exe SHA256` i Windows). Filen er ikke signeret, så Windows kan vise en SmartScreen-advarsel.

## Byg en programfil (Windows)

```powershell
python -m pip install -e ".[build,speech]"
python tools/build_executable.py
```

Scriptet bruger PyInstaller og skriver `dist/flash-card.exe`: én fil uden konsolvindue, med billeder, ordliste og udtalen indeni. Dobbeltklik for at starte; Python er ikke nødvendigt for at køre den.

- Din fremgang gemmes i en `data/`-mappe ved siden af programfilen (`data/words_to_learn.csv`).
- En `data/ms-da.csv` ved siden af programfilen erstatter ordlisten indeni.
- `python tools/build_executable.py --no-speech` udelader talepakkerne; `--clean` bygger forfra.
- Programfilen er ikke i repositoryet. Byg den på det system, hvor den skal køre; Windows kan vise en SmartScreen-advarsel, fordi filen ikke er signeret.

## Dokumentation af kildekoden

```bash
doxygen Doxyfile
```

HTML-filerne skrives til `docs/doxygen/html/index.html`.
