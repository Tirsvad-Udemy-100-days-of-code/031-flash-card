# RC-080: Windows Sandbox run of the executable

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-080 |
| CrossReference | [MIL-013], [RC-079] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-013], criterion 7 (the Windows executable in Windows Sandbox), which [RC-079] left open
- Checklist used: none exists; criterion 7 of MIL-013 and the open condition of RC-072 (smoke test of the executable)
- Scope: delta re-review of criterion 7 of MIL-013 after the Product Owner started the run
- Language and domain: n/a (record of results)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 7 | The Windows executable passes the smoke test inside Windows Sandbox (window titled Flashy, embedded list, list override, known button writes the progress file), 5 consecutive sandbox runs, with the results read from the mapped output folder | Pass | `tools/sandbox/run.ps1 -Runs 5` on Windows 11 Pro; the sandbox ran `Microsoft Windows 11 Enterprise`; `dist/flash-card.exe` (25.8 MB, built from the head of `main` before the container changes) mapped read-only; **5 of 5 runs passed**: window found, click made by the sandbox's own mouse at the known button, progress file with a header and 2 cards (3 rows), 4.5 to 5.2 s per run including the copy and the start; a screenshot of the sandbox desktop shows the card with the menu bar and both button images; the sandbox shut itself down and no sandbox process was left |
| RC-072 #4 | The executable passes the smoke test of MIL-009 | Pass | The list-override case (`ms-da.csv` next to the program, 3 words, one known word, 2 left) passed in all 5 runs; with the earlier 3 of 8 lost clicks on the host, the finding is that they came from the host click automation, not from the program |

## Overall Verdict

Go — criterion 7 of MIL-013 and the open condition of RC-072 on the smoke test of the executable are met. The issue "Run and record the checks" can be closed. The tag of v0.2.0 is still lightweight (RC-072 criterion 5) and the executable is still not attached to a release (upload limit of the host). Reviewed by AI as stand-in for S01; not independent of the author.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Decide whether the lightweight tag `v0.2.0` is replaced by an annotated tag (force update of the tag on the host) | S01 | 2026-10-21 |
| Raise the upload limit of the git host so that `flash-card.exe` and its checksum can be attached to a release | S01 | 2026-10-21 |

---

[MIL-013]: ../milestones/mil-013-container-checks.md
[RC-079]: ./rc-079-container-checks.md
