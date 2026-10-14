# ADR-0004: Windows executable built with PyInstaller

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0004 |
| CrossReference | [BC-001], [US-001], [DCD-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [768ca34] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The Product Owner (S01) wants an executable file, so that the program can be started without a Python installation (US-001.07). The program has images, a word list, a progress file that must survive restarts, and an optional speech extra. Options:

1. A one-directory build (a folder with the executable and its libraries): starts faster and the data can sit beside the files, but it is a folder of hundreds of files to hand over.
2. A one-file build (a single `flash-card.exe` that unpacks itself to a temporary folder): one file to hand over, slower start; resources are in a temporary folder, so progress needs a place beside the executable.
3. Another packager (Nuitka, cx_Freeze) or an installer: more tooling and a larger change for the same result.

## Decision

Build a one-file, windowed (no console) Windows executable with PyInstaller by `tools/build_executable.py`. The images and the word list are inside the executable. The progress file and an optional word list are in a `data/` folder beside the executable (found with `sys.executable` when `sys.frozen` is set), and `--data-dir` still overrides it. PyInstaller is only in the optional extra `build`, so `dependencies` stays empty (ADR-0001). The executable is a build output and is not committed.

## Consequences

**Positive:**

- One file to hand over, and no Python, `.venv` or pip needed to run it.
- The source run is unchanged; only the path rule differs when frozen, and it is tested without PyInstaller.
- The word list stays editable beside the executable.

**Negative:**

- PyInstaller cannot cross-compile: the executable must be built on Windows (and on Linux or macOS for those systems).
- A one-file executable unpacks to a temporary folder at each start and is larger with the speech packages; unsigned executables can trigger Windows SmartScreen or antivirus warnings.
- The Windows Store Python can cause Tcl/Tk path problems with PyInstaller; a build with it must be checked by a real start.

## Affected Artifacts

- [BC-001] — scope: the executable is in scope; installer, signing and release upload are out
- [US-001] — US-001.07 Start without Python
- [DCD-001] — packaging support and the choice of the word list file in the composition root

---

[BC-001]: ../business-case.md
[US-001]: ../user-stories.md
[DCD-001]: ../dcd.md
[768ca34]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/768ca344c95d4f21e565e37ac96661c2f8dc8f54
