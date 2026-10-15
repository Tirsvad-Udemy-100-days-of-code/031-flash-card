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

## Release and executable (Windows)

The release pages of [v0.2.0](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.2.0) and [v0.1.0](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.1.0) have the release notes. The executable is not attached there yet, because the server's upload limit rejects a file of this size (HTTP 413); build it as described below. The file is not signed, so Windows may show a SmartScreen warning.

## Build an executable (Windows)

```powershell
python -m pip install -e ".[build,speech]"
python tools/build_executable.py
```

The script uses PyInstaller and writes `dist/flash-card.exe`: one file, no console window, with the images, the word list and the spoken word inside. Double-click it to start; Python is not needed to run it.

- Your progress is kept in a `data/` folder next to the executable (`data/words_to_learn.csv`).
- A `data/ms-da.csv` next to the executable replaces the word list inside it.
- `python tools/build_executable.py --no-speech` leaves the speech packages out; `--clean` rebuilds from scratch.
- The executable is not committed to the repository. Build it on the system you want to run it on; Windows may show a SmartScreen warning because the file is not signed.

## Checks without a desktop (Docker)

The tests, the linters, the screenshots and a smoke test of a Linux binary run in a Debian container on a virtual screen, so no window opens on your own desktop.

```bash
docker build -f docker/debian.Dockerfile -t flash-card-debian .
# linters and the whole test suite, including the real window tests
docker run --rm -v "$PWD:/repo:ro" flash-card-debian bash /repo/tools/docker/in-container.sh run-checks.sh
# screenshots into ./build/container-out
docker run --rm -v "$PWD:/repo:ro" -v "$PWD/build/container-out:/out" flash-card-debian bash /repo/tools/docker/in-container.sh screenshots.sh /out
# build the Linux binary and press the known button 5 times (binary and source)
docker run --rm -v "$PWD:/repo:ro" flash-card-debian bash /repo/tools/docker/in-container.sh smoke-binary.sh 5
```

On Windows PowerShell write `${PWD}` for `$PWD`. The repository is mounted read-only and copied inside the container.

- The desktop is Xvfb with GNOME's window manager (mutter). GNOME Shell is tried first and does not start in a container (it needs a login manager), so the scripts fall back to mutter and print which one ran.
- The Windows executable is checked in **Windows Sandbox** (Windows 11 Pro, feature enabled): `powershell -File tools\sandbox\run.ps1 -Runs 5` after `python tools/build_executable.py`. The sandbox shows its own window while it runs; the click is made inside the sandbox.
- Not covered: macOS (it cannot be run in Docker on Windows or Linux and Apple's licence allows it only on Apple hardware), and Windows itself in the Debian container.

## Documentation of the source code

```bash
doxygen Doxyfile
```

The HTML is written to `docs/doxygen/html/index.html`.
