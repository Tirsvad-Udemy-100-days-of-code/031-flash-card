# 🚀 Flash Card

A flash card program for learning the most frequent Malay words with their Danish translations. It is the solution of day 31 of Udemy's *100 Days of Code: The Complete Python Pro Bootcamp*, written for course participants who want to compare solutions and for visitors who browse the repository for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

The program shows a Malay word on a card. After three seconds the card turns over and shows the Danish translation. You press the green tick when you know the word and the red cross when you do not. A known word is removed from the words to learn, and the words still to learn are saved, so the next start continues where you stopped.

| Part | What it is for |
| --- | --- |
| `src/flash_card/` | The program, in four layers: `domain`, `application`, `infrastructure`, `presentation` |
| `tests/` | `pytest` tests: `unit`, `integration`, `e2e` |
| `data/` | The word list `ms-da.csv` and, after the first known word, your own `words_to_learn.csv` |
| `docs/` | Project documents (business case, plan, design, review records) |
| `Doxyfile` | Doxygen configuration for the source code documentation |

The core program uses only the Python standard library. Spoken Malay words are an optional extra.

## 📋 Requirements

| Need | Why |
| --- | --- |
| Python 3.13 or later, with Tkinter | The program and its window (Tkinter is part of the standard Python installers for Windows and macOS; on Debian or Ubuntu install `python3-tk`) |
| `git` | To clone the repository |
| Doxygen (optional) | To build the source code documentation |
| `gTTS` and `playsound==1.2.2` (optional, extra `speech`) | To hear the Malay word; needs a network connection |

## 🛠️ Setup

Create a virtual environment in `.venv`, activate it, upgrade pip and install the project. Run the commands in the repository folder.

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

- Use `python -m pip install -e .` if you only want to run the program; the `dev` extra adds `pytest`, `ruff`, `mypy` and `import-linter`.
- Add the spoken word with `python -m pip install -e ".[speech]"`.
- If PowerShell refuses to run `Activate.ps1`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use `.\.venv\Scripts\activate.bat` in `cmd`.
- Leave the environment with `deactivate`. Delete the `.venv` folder to start over.

## ▶️ Run

```bash
python -m flash_card
```

The program is run from the activated `.venv`. The window opens with the first card; the program is built step by step and the pull requests and milestones show each step.

## 🧪 Tests

```bash
python -m pytest
```

Quality checks used by the project:

```bash
python -m ruff check src tests
python -m mypy
lint-imports
```

The window test in `tests/e2e/` is skipped when no display is available.

## 📄 License

GNU Affero General Public License v3.0 or later. See [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [AGENTS.md][agents] | The rules AI agents follow in this repository |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Domain dictionary][DICT-001] | The PO terms and the IT terms |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[license]: ./LICENSE
[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/issues
[agents]: ./AGENTS.md
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[DICT-001]: ./docs/dictionary.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
