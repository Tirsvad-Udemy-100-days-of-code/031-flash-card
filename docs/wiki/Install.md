# Install

🌐 **English** · [Dansk](Install-da) · [Bahasa Malaysia](Install-ms)

## Requirements

- Python 3.13 or later with Tkinter (on Debian or Ubuntu: `sudo apt install python3-tk`).
- `git`.
- Optional: an internet connection and the `speech` extra to hear the Malay word.

## Get the code

```bash
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card.git
cd 031-flash-card
```

## Create and use a local virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

- `.[dev]` adds `pytest`, `ruff`, `mypy` and `import-linter`. Use `.` if you only want to run the program.
- If PowerShell refuses to run `Activate.ps1`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.
- Leave the environment with `deactivate`; delete the `.venv` folder to start over.

## Spoken Malay word (optional)

```bash
python -m pip install -e ".[speech]"
```

This installs `gTTS` and `playsound==1.2.2`. Without it the program works silently.

## Run and test

```bash
python -m flash_card
python -m pytest
```

The window test in `tests/e2e/` is skipped when no display is available.

## Documentation of the source code

```bash
doxygen Doxyfile
```

The HTML is written to `docs/doxygen/html/index.html`.
