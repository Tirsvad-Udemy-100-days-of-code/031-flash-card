# ADR-0001: Standard library first, speech as an optional extra

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [SA-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c3fbcbc] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The assignment tells the participant to read the word list with `pandas`. The Product Owner (S01) also wants the Malay word spoken, which needs `gTTS` and `playsound`. GitHub viewers (S03) want no runtime dependencies, and fellow course participants (S02) want a program they can run at once. Options:

1. `pandas` for CSV and `gTTS` plus `playsound` as normal dependencies: matches the assignment text, but installs a large dependency tree for a 1000 row file, and a failing `playsound` build breaks the install.
2. Standard library `csv` for the data and `gTTS` plus `playsound` as an optional extra behind a port: no runtime dependency for the core program, speech available on request.
3. No speech at all: simplest, but does not meet the Product Owner's wish.

## Decision

The core program uses only the Python standard library (`csv`, `tkinter`, `random`, `pathlib`). Speech is an optional extra declared as `speech` in `pyproject.toml` (`pip install -e ".[speech]"`), used through a `SpeechPort`, and replaced by a silent adapter when the extra or the network is missing.

## Consequences

**Positive:**

- `dependencies` in `pyproject.toml` is empty, which meets success criterion 3 of [BC-001] and the concern of S03.
- The program and its tests run without a network.
- A broken audio player cannot stop the program from starting.

**Negative:**

- The code differs from the assignment text, which uses `pandas`; the wiki explains the mapping for S02.
- Two code paths exist for speech (real and silent) and both need tests.
- `playsound` is unmaintained and is pinned to 1.2.2.

## Affected Artifacts

- [BC-001] — success criterion 3 and the risk about `playsound`
- [SA-001] — the conflict between S01 and S03

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[c3fbcbc]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/commit/c3fbcbcfaf799e0ae34aed7e14d3bc8a62f03db3
