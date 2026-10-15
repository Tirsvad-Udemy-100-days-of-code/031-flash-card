# RC-078: Review of SH-MIL-013

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-078 |
| CrossReference | [SH-MIL-013], [QC-SH-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [SH-MIL-013]
- Checklist used: [QC-SH-001]
- Scope: full review
- Language and domain: n/a (technical type)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Starts with `#!/usr/bin/env bash` and `set -euo pipefail` (or a comment explains the exception) | Pass | Every executable script starts with `#!/usr/bin/env bash` and `set -euo pipefail`; `start-desktop.sh` is sourced, says so in its header and sets no shell options in the caller. |
| 2 | Every expansion is quoted; lists are arrays; tests use `[[ ]]` and `$(...)` | Pass | Expansions are quoted, tests use `[[ ]]`, command substitutions use `$(...)`; shellcheck reports nothing. |
| 3 | Names follow the conventions: `kebab-case.sh` files, `snake_case` functions and variables, `UPPER_SNAKE` constants and environment variables | Pass | File names are kebab-case; variables are snake_case, environment variables UPPER_SNAKE. |
| 4 | Passes `shellcheck` and `bash -n` with no unexplained `disable` comments | Pass | `shellcheck -x` and `bash -n` pass on all six scripts with no `disable` comment. |
| 5 | Errors go to standard error with an `error:` message and a non-zero exit code; bad or missing arguments print a usage line | Pass | Errors go to standard error with `error:`, a usage line is printed, and bad arguments exit with 2 (`selftest.sh` checks it). |
| 6 | Temporary files use `mktemp` with a `trap ... EXIT` cleanup; no fixed `/tmp` names | Pass | `start-desktop.sh` uses `mktemp -d` with a `trap ... EXIT`; no fixed `/tmp` names remain. |
| 7 | No secret is written in the script, echoed, or put on a command line; secrets come from the environment or a gitignored file | Pass | No secret is used or written. |
| 8 | A script that changes state outside its own directory defaults to a dry run or needs an explicit flag, and says so in its header | Pass | `in-container.sh` is the only script that deletes a folder; its header says so and it refuses the repository and `/` as work folder. |
| 9 | A header comment states purpose, usage, options, environment variables and exit codes | Pass | Each header gives purpose, usage, environment, tools and exit codes. |
| 10 | The script implements a task or design it cites; deviations are recorded | Pass | The scripts implement tasks 3, 4 and 6 of MIL-013 and ADR-0005; the fallback from GNOME Shell to mutter is recorded in the output. |
| 11 | Behaviour is tested for success, failure and any disabled or bypass path | Pass | `selftest.sh` tests the refusals and `bash -n`; the success paths are the container runs of `run-checks.sh`, `screenshots.sh` and `smoke-binary.sh` (recorded in RC-079). |
| 12 | Formatted with `shfmt` (or the project's formatter) | Fail | `shfmt` was not run; Optional, deferred. |
| 13 | Safe to re-run: a second run does not duplicate or corrupt what the first did | Pass | The second container run gave the same result as the first (272 passed, 5 of 5 smoke runs). |
| 14 | Bash version and external tools it needs are stated; GNU-only options are named | Pass | Bash and the external tools are listed under `Needs`; GNU `tar --exclude` is named by the tool list. |
| 15 | A command sequence, constant, path or message used more than once is defined once (a function, a variable or a sourced helper); a helper is shared between scripts only where it expresses the same knowledge | Pass | The desktop start is defined once in `start-desktop.sh` and sourced by the three scripts. |

## Overall Verdict

Go — every Mandatory criterion passes; the failed Optional criteria are deferred with an action item. Reviewed by AI as stand-in for S01; not independent of the author.

Container run of the self test: 11 cases ok.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Criterion 12 (Optional) failed: Formatted with `shfmt` (or the project's formatter); fix or accept the deferral | S01 | 2026-10-21 |

---

[SH-MIL-013]: ../../../tools/docker
[QC-SH-001]: ../../../framework/qc/code/qc-programming-shell.md
