# RC-079: Review of the container checks

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-079 |
| CrossReference | [MIL-013] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [2f192b6] |

---

## Artifact Under Review

- Instance reviewed: [MIL-013] (the milestone's Go / No-Go criteria, checked against the container and sandbox checks)
- Checklist used: none exists for this result; the ten criteria of MIL-013 are the checklist
- Scope: full review
- Language and domain: n/a (record of results)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | `docker build` of the Debian image succeeds | Pass | Image `flash-card-debian` built from `docker/debian.Dockerfile` (base `python:3.13-slim-bookworm`, Python 3.13.16); size 1697 MB; `binutils` was missing at first and was added after the first smoke build failed |
| 2 | Linters and the whole test suite run on the virtual desktop and end with exit code 0, e2e tests not skipped | Pass | `run-checks.sh` twice: ruff, ruff format, mypy (49 files), lint-imports (1 kept) and 272 tests passed in 3.5 s; 33 s per run |
| 3 | The full GNOME session is tried and the result recorded; fallback to mutter stated | Pass | `gnome-shell --x11` starts and then fails with `Gio.IOErrorEnum: Could not connect` in `LoginManagerSystemd` (no login manager in a container); the checks ran on GNOME's window manager mutter 43.8, which the script prints (`desktop: mutter on :99`) |
| 4 | Nothing opens or moves on the host desktop during the runs | Pass | All runs of this record were `docker run` commands with no display; note: earlier unit runs of the test suite on the host by a helper agent opened Tk windows briefly before the Product Owner's instruction; from then on the suite ran only in the container |
| 5 | The screenshot script writes the four PNG files from the Debian image | Pass | `screenshot-level.png`, `-front.png`, `-back.png`, `-menu.png` (20 to 23 KB each) written to the mounted folder and read by eye: the level screen, the card with the menu bar (File, About) are right |
| 6 | The Linux binary is built and passes the smoke test 5 consecutive runs, and the source program too | Pass | `smoke-binary.sh 5` twice: the PyInstaller binary 5 of 5 (0.64 s per run) and `python -m flash_card` 5 of 5 (0.38 s); each run: window found, click at the known button (650, 659), progress file has header plus 2 cards |
| 7 | The Windows executable passes the smoke test inside Windows Sandbox, 5 consecutive runs | Fail | Not run. `tools/sandbox/` (`flash-card.wsb`, `smoke.ps1`, `run.ps1`) is written, the PowerShell parses without errors and the configuration is well-formed XML, but starting Windows Sandbox opens a window on the host, and the Product Owner asked that no app runs on the development machine while working. The run waits for the Product Owner's go |
| 8 | The lost-click symptom of RC-072 is investigated and the finding recorded | Pass | 10 of 10 presses of the known button registered in the container (binary and source). The symptom was seen only with the simulated Windows mouse (about 3 of 8 reruns) and is most likely a timing problem of that click automation (cursor move, focus, button down and up) and not a program defect; this is a finding for Linux only and it is not proven for Windows until criterion 7 is run |
| 9 | README and the wiki Install page in three languages describe the commands and the limits; `check-readme.sh` exit 0 | Pass | Sections added; `check-readme.sh` exit 0; macOS stated as not covered, the Debian check stated as not a Windows check, the sandbox requirements stated |
| 10 | BC-001, PP-001 and ADR-0005 are reviewed Go; code review has no failed Mandatory criterion | Pass | RC-073 to RC-076; RC-077 (Python) and RC-078 (shell) are Go |

## Overall Verdict

Go-with-conditions — everything that can run without the host desktop runs and passes: the Debian checks (272 tests, linters), the screenshots, and the smoke test of the Linux binary and the source program. Criterion 7 (the Windows executable in Windows Sandbox) is not run and keeps the issue "Run and record the checks" open. Reviewed by AI as stand-in for S01; not independent of the author.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Run `powershell -File tools\sandbox\run.ps1 -Runs 5` after `python tools/build_executable.py` at a time that suits the Product Owner (Windows Sandbox shows its own window), and record the result in a new review record | S01 | 2026-10-21 |
| Decide whether the GNOME Shell start in the container is worth a login-manager stub (it is not needed for the checks) | S01 | 2026-10-21 |

---

[MIL-013]: ../milestones/mil-013-container-checks.md
[2f192b6]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/2f192b6936a92f85c6c200de3cac3d6cf3572903
