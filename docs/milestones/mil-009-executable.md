# MIL-009: Executable with PyInstaller

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-009 |
| CrossReference | [BC-001], [US-001], [UC-001], [DCD-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [768ca34] |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added task 9 (fix a flaky unit test found after the merge) | [061b4f4] |

---

## Purpose

Decide whether the Learner can start the program from one executable file without a Python installation: the program is packaged with PyInstaller by a script of this repository, and behaves in the executable as it does from the source.

## Deliverable

`python tools/build_executable.py` builds `dist/flash-card.exe` (one file, no console window, an icon, the images and the word list inside, the speech extra included). The executable shows the level screen, keeps the progress in `data/words_to_learn.csv` next to it and prefers a `data/ms-da.csv` next to it over the word list inside. The executable itself is not committed to git; README and wiki (English, Danish, Bahasa Malaysia) explain how to build and use it.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `python tools/build_executable.py` ends with exit code 0 and produces `dist/flash-card.exe` | File exists and is larger than 1 MB | No file or a build error |
| 2 | The executable starts on this machine with the virtual environment not activated and shows the level screen without a console window | A window titled "Flashy" exists after 5 seconds and the process is a Windows GUI program | The process ends or shows a console |
| 3 | With a `data/ms-da.csv` copied next to the executable it uses that file; without it the word list inside the executable is used | Smoke test with a marked list of two words, then without | The wrong list is used |
| 4 | Marking a word known in the executable writes `data/words_to_learn.csv` next to it and the next start continues from it | Smoke test reads the file after the run | No file or progress lost |
| 5 | The four images and the icon are inside the executable and are found when frozen | Card and button images are visible in a captured screenshot of the executable | A missing image or an exception |
| 6 | Path resolution when frozen (`sys.frozen`, `sys._MEIPASS`) is tested without PyInstaller | Unit tests pass | Not covered |
| 7 | `dependencies` in `pyproject.toml` is still empty; PyInstaller is only in the extra `build` | File check | A runtime dependency was added |
| 8 | BC-001, DCD-001 and ADR-0004 are updated and reviewed `Go`; README and wiki in three languages describe the build | Review records `Go`; `check-readme.sh` exit 0 | A document is missing |
| 9 | Code review against QC-PY-001 has no failed Mandatory criterion; `pytest`, `ruff`, `mypy --strict`, `lint-imports` and `doxygen` are clean | `RC-*` verdict Go and exit codes 0 | Otherwise |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-008 | The finished program, with the level screen, that is packaged |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 4 (a repository others can use), extended by the new request of S01; success criterion 4 (time to run) | [BC-001] |
| US-001.07 Start without Python | [US-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-16 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Update the documents for the executable | Amend BC-001 (In Scope: an executable built with PyInstaller; Out of Scope: an installer and a signed release stay out), add ADR-0004 (PyInstaller one-file windowed build, word list inside and a `data` folder beside the executable for progress, Windows only), and add the runtime path resolution to DCD-001. Every changed document gets a Version History row and a review. | No | BC-001, DCD-001 |
| 2 | Resolve resource and data paths when frozen | The images are found under `sys._MEIPASS` and the default data folder is `data/` next to the executable when `sys.frozen` is set; the source run keeps its paths. The rule is one function used by `constants.py`, tested by simulating the frozen state. | Yes | US-001.07 |
| 3 | Prefer the word list next to the executable | When the data folder has no `ms-da.csv` the program uses the copy inside the executable; the progress file is always written to the data folder; `--data-dir` still overrides both. | Yes | US-001.07 |
| 4 | Add the build script and the build extra | `tools/build_executable.py` calls PyInstaller (one file, windowed, name `flash-card`, the assets and the word list as data, the icon, the speech packages as hidden imports); `pyproject.toml` gets the extra `build`; `build/`, `dist/` and `*.spec` are ignored. | No | ADR-0004 |
| 5 | Generate the application icon | `tools/generate_images.py` also writes `flash_card.ico` (the card with the tick) from the same drawing code, so no external asset is used. | No | |
| 6 | Build and smoke-test the executable | Build it, start it with the virtual environment not active, check the window, the images, the level choice, the progress file next to it, the word list override and the speech import; record the result in the review record. | Yes | US-001.07 |
| 7 | Test the path rules and the build arguments | Unit tests for the frozen and source path rules and for the argument list the build script gives PyInstaller (without running PyInstaller). | No | |
| 8 | Update README and wiki | README and the Install page of the wiki in English, Danish and Bahasa Malaysia: how to build, where the executable and the data folder are, that Python is not needed to run it. The wiki is republished after the merge. | No | |
| 9 | Fix a flaky unit test | After the merge a unit test of `app.main` failed in about 1 of 6 full runs because it created a real Tk root; it uses the module's fake root instead, so the unit tests never need a display. Found by running the suite repeatedly. | No | RC-049 |

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[UC-001]: ../uc-001/uc.md
[DCD-001]: ../dcd.md
[768ca34]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/768ca344c95d4f21e565e37ac96661c2f8dc8f54
[061b4f4]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/061b4f48b5d49e6800656c95d79df707e07ec0f3
