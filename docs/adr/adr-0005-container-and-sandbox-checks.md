# ADR-0005: Container and sandbox checks without the user's desktop

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0005 |
| CrossReference | [BC-001], [ADR-0004] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [f86bc91] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

Smoke tests of the program drive a real window. Run on the Product Owner's own Windows desktop they open windows, take the focus and move the mouse, which interrupts the Product Owner's work (RC-072). The checks must run somewhere else. Options:

1. A Windows hidden desktop (a second Win32 desktop of the same session): invisible, but still the host's session and a place where a mistake can reach the host.
2. A Debian Docker container with a virtual X screen and GNOME for the Linux checks, and Windows Sandbox for the Windows executable: both are isolated from the host's input and desktop; the Debian check is not a Windows check.
3. A Wine container for the Windows executable, or a real Windows virtual machine run in Docker with KVM: Wine is an emulation of the Windows interface; the Windows virtual machine needs a Microsoft evaluation image of tens of gigabytes and licence terms the Product Owner has not accepted.
4. macOS in Docker: not possible on a Windows host, and Apple's licence allows macOS only on Apple hardware.

## Decision

Run the Linux checks (linters, tests including the real window, screenshots, a Linux binary and its smoke test) in a Debian image based on `python:3.13-slim-bookworm` with Xvfb, GNOME's window manager and, if it runs in a container, the GNOME session. Run the Windows executable in Windows Sandbox of Windows 11 Pro through a `.wsb` configuration and a script that presses the known button inside the sandbox and writes the result to a mapped folder. Do not run macOS, and state that in the documents.

## Consequences

**Positive:**

- No check takes the focus or the mouse of the host any more.
- The container checks are repeatable on any machine with Docker and need no Python installation.
- The sandbox is a real Windows, thrown away after each run.

**Negative:**

- The Debian image is large (a desktop and a Python image) and the first build takes time.
- A full GNOME session may not run in a container; the fallback (GNOME's window manager) is a weaker statement, and the record says which one ran.
- Windows Sandbox needs Windows 11 Pro with the feature enabled and shows its own window on the host while it runs.
- macOS stays untested.

## Affected Artifacts

- [BC-001] — In Scope and Out of Scope lists
- [ADR-0004] — the executable that the sandbox runs

---

[BC-001]: ../business-case.md
[ADR-0004]: ./adr-0004-pyinstaller-executable.md
[f86bc91]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/f86bc9136e7719fbcd049a4f803959019b7d2df3
