# MIL-001: Project foundation

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001], [US-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

---

## Purpose

Decide whether the project can start building features: the repository has its configuration, layer skeleton, tooling and run instructions, so that every later milestone adds behaviour to a ready structure.

## Deliverable

A repository in which `pip install -e ".[dev]"` works in a fresh `.venv`, `pytest` runs (with the placeholder test passing), the four layer packages and the three test folders exist, and the README explains how to create the virtual environment, run the program and run the tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `pyproject.toml` declares Python `>=3.13`, an empty `dependencies` list, the extras `speech` and `dev`, and the pytest, ruff and mypy configuration | Present and `pip install -e ".[dev]"` succeeds in a fresh `.venv` | Missing or install fails |
| 2 | `.gitignore` is a Python ignore file and also ignores `.venv/`, `.env`, `data/words_to_learn.csv` and `docs/doxygen/` | `git check-ignore` reports each path | A path is not ignored |
| 3 | `src/flash_card/` has `domain`, `application`, `infrastructure` and `presentation` packages and `constants.py`; `tests/` has `unit`, `integration`, `e2e` | Every folder exists | A folder is missing |
| 4 | `doxygen Doxyfile` runs without error | Exit code 0 | Any error |
| 5 | README follows the framework template and gives the `.venv` and `python -m pip install --upgrade pip` commands | `check-readme.sh` reports no finding | Any finding |
| 6 | `pytest` exits with 0 | Exit code 0 | Any failure |

## Dependencies

| Depends on | Reason |
| --- | --- |
| BC-001, SA-001, PP-001 accepted | Required by the plan-first gate before a milestone |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 3 (no runtime dependencies) and objective 4 (repository others can use) | [BC-001] |
| Success criteria 3 and 4 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-14 — the first day of the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add pyproject.toml | Declare the project `flash-card` for Python 3.13 or later with no runtime dependencies, an optional `speech` extra (`gTTS`, `playsound==1.2.2`) and a `dev` extra (`pytest`, `ruff`, `mypy`), and configure pytest (`src` on the path, `tests` folder), ruff and mypy. Meets objective 3 of the Business Case and ADR-0001. | No | ADR-0001 |
| 2 | Add Python .gitignore | Ignore Python build and cache output, `.venv/`, the local `.env` with tokens that is never imported into the project, the generated `docs/doxygen/` and the learner's own `data/words_to_learn.csv`. | No | |
| 3 | Create the layer skeleton and constants.py | Create `src/flash_card/` with the packages `domain`, `application`, `infrastructure`, `presentation` and `constants.py` (background colour, fonts, delay 3000 ms, file names), and `tests/unit`, `tests/integration`, `tests/e2e`, as ADR-0002 and DCD-001 set out. | No | ADR-0002, DCD-001 |
| 4 | Add the Doxyfile | Add a `Doxyfile` for `src/` with Python optimisation, output in `docs/doxygen/`, so that the Doxygen comments written in every later milestone produce documentation. | No | |
| 5 | Write the first README with the .venv instructions | Create README.md from the framework template with overview, requirements, and the commands to create and activate `.venv`, upgrade pip with `python -m pip install --upgrade pip`, install, run and test, for Windows and Linux/macOS. | No | |
| 6 | Add the word list to the repository | Commit `data/ms-da.csv` (1000 Malay words with Danish translation, semicolon separated, header `ms;da`) and describe its origin and that it is machine translated, in `data/README.md`. | No | |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[DCD-001]: ../dcd.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
