# MIL-013: Container checks

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-013 |
| CrossReference | [BC-001], [DCD-001], [ADR-0004] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [f86bc91] |

---

## Purpose

Decide whether the program can be built, tested and run without touching the Product Owner's own desktop: a Docker container gives a Debian desktop (GNOME) on a virtual screen, and Windows Sandbox (a disposable Windows virtual machine of Windows 11 Pro) runs the Windows executable on a desktop of its own. The checks that earlier took over the Windows desktop (mouse clicks, windows opening) move into the containers.

## Deliverable

- A Debian image (`python:3.13-slim-bookworm`) with GNOME's window manager and session, a virtual X screen, Tk and fonts, that runs the linters and the whole test suite (including the e2e tests of the real window), the headless run with screenshots, and a PyInstaller build of a Linux binary with its smoke test.
- A Windows Sandbox check of the Windows executable: a `.wsb` configuration and a PowerShell script (`tools/sandbox/`) that start a disposable Windows 11 virtual machine with the built `dist/` mapped read-only and an output folder mapped read-write, start the executable on the sandbox's own desktop, press the known button inside the sandbox, check the progress file, take screenshots, write the results to the output folder and shut the sandbox down. The mouse and the keyboard used are those of the sandbox, not of the host.
- macOS is not covered, and the documents say why (see ADR-0005).

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `docker build` of the Debian image succeeds on the Product Owner's Docker Desktop (Linux containers) | Exit code 0 | A build error |
| 2 | In the Debian image the linters and the whole test suite run on the virtual screen with the GNOME window manager and end with exit code 0, with the e2e tests counted as passed (not skipped) | Output and exit code | A skipped or failing test |
| 3 | The full GNOME session (`gnome-session` with its shell) is tried in the container; the result is recorded; when it cannot run in a container the checks use GNOME's window manager (mutter) and the record says so | Result in the review record | An unstated fallback |
| 4 | During the container runs nothing opens or moves on the host desktop; during a sandbox run the only host effect is the sandbox's own window, and the sandbox is closed by its script | Nothing else seen on the host | A host window other than the sandbox or any host click |
| 5 | The screenshot script writes the level screen, the card front, the card back and the window with the menu bar as PNG files to a mounted folder, from the Debian image | Four readable PNG files | A missing or blank file |
| 6 | A Linux binary is built in the container and its smoke test passes: the window appears, the level screen is shown, a known word is pressed through the virtual input of the screen and the progress file has one card less, the list override is used | Script output and exit code 0 for 5 consecutive runs | A failing run |
| 7 | The Windows executable passes the same smoke test inside Windows Sandbox (window titled Flashy, embedded list, list override, known button writes the progress file), 5 consecutive sandbox runs, with the results read from the mapped output folder | Result files of 5 runs | A failing run, or a run that needs the host mouse |
| 8 | The lost-click symptom of RC-072 is investigated with the container test (a repeated press of the known button on the same executable) and the finding is recorded: program defect or test harness | Finding in the review record | No finding |
| 9 | README and the wiki Install page in three languages describe the commands and state that macOS is not covered, that the sandbox needs Windows 11 Pro with Windows Sandbox enabled, and that the Debian check is not a Windows check; `check-readme.sh` exit 0 | Exit code 0 | A missing statement |
| 10 | BC-001 and PP-001 are updated and ADR-0005 records the decision and its limits (including why macOS is not run in Docker); each reviewed `Go`; code review against QC-PY-001 has no failed Mandatory criterion; the linters are clean | `RC-*` verdict Go | Otherwise |

## ## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-012 | The version 0.2.0 of the program, the built executable and the open condition (RC-072) about its smoke test |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 4 (a repository others can use) and success criterion 2 (tests run on a clean environment) | [BC-001] |
| The condition of RC-072 on the executable smoke test (Linux part) | [MIL-012] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in in autonomous mode) |

## Target Date

2026-10-19 — within the delivery window that ends 2026-10-21 ([BC-001] constraint).

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Update the documents for the container checks | BC-001 (In Scope: Docker images for tests and headless runs; Out of Scope: macOS, a signed or installed Windows setup), PP-001 and a new ADR-0005 (the Debian image with GNOME, Windows Sandbox for the Windows executable, what is covered and why macOS is not run in Docker: Apple's licence allows macOS only on Apple hardware); each changed document gets a Version History row and a review. | No | BC-001, ADR-0004 |
| 2 | Add the Debian image with GNOME | `docker/debian.Dockerfile` and `.dockerignore`: `python:3.13-slim-bookworm`, `xvfb`, `xauth`, `dbus-x11`, `mutter`, `gnome-session` and `gnome-shell`, `tk`, `fonts-liberation`, `x11-utils`, `xdotool`, a non-root user; the project installed with `[dev,speech,tools,build]`. | No | ADR-0005 |
| 3 | Start a GNOME session on the virtual screen | `tools/docker/start-desktop.sh` starts `dbus`, Xvfb and `gnome-session` (or, if the session cannot run in a container, mutter alone) and waits until the desktop is up; the choice is printed and recorded. | No | |
| 4 | Add the check scripts | `tools/docker/run-checks.sh`, `screenshots.sh` and `smoke-binary.sh`; each one purpose, `set -euo pipefail`, shellcheck clean, all run under the desktop of task 3. | No | |
| 5 | Make the screenshot tool work on Linux | `tools/capture_screenshots.py` chooses the platform: Windows as now, Linux grabs the X screen with Pillow and crops to the window; the pure parts are unit tested. | No | |
| 6 | Add the headless smoke driver | A script that starts the program or the binary, finds the window with `xdotool`, presses the known button with the virtual input of the screen, and checks the progress file, with a repeat count so the lost-click symptom of RC-072 can be measured; the sandbox script does the same with the sandbox's input. | No | |
| 7 | Add the Windows Sandbox check | `tools/sandbox/flash-card.wsb` (mapped folders: `dist` read-only, `out` read-write; logon command), `tools/sandbox/smoke.ps1` (runs inside the sandbox: copy the executable, start it, wait for the window, press the known button with the sandbox's own input, read the progress file, take screenshots, write a result file and shut the sandbox down) and `tools/sandbox/run.ps1` on the host (starts the sandbox with the generated configuration and waits for the result file). | No | ADR-0005 |
| 8 | Run and record the checks | Build the image, run the scripts and the smoke tests 5 times each in the container and 5 times in the sandbox, record counts, sizes, durations and the GNOME session result; record the finding on the lost click. | No | |
| 9 | Test the pure parts | Unit tests for the platform choice and the box calculation of the capture tool and for the argument handling of the smoke driver. | No | |
| 10 | Update README and wiki | README and the Install page of the wiki in English, Danish and Bahasa Malaysia: the commands, the output folders, the limits (the Debian check is not a Windows check, the sandbox needs Windows 11 Pro, macOS is not covered); the wiki is republished after the merge. | No | |

---

[BC-001]: ../business-case.md
[DCD-001]: ../dcd.md
[ADR-0004]: ../adr/adr-0004-pyinstaller-executable.md
[MIL-012]: ./mil-012-release-0-2-0.md
[f86bc91]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/f86bc9136e7719fbcd049a4f803959019b7d2df3
