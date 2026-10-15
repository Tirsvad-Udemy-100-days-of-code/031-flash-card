# RC-055: Review of the release v0.1.0

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-055 |
| CrossReference | [MIL-010] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-010] (the milestone's Go / No-Go criteria, checked against the release v0.1.0)
- Checklist used: none exists for a release; the seven criteria of MIL-010 are the checklist
- Scope: full review
- Language and domain: n/a (record of results)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The executable is rebuilt from the head of `main` that gets the tag and passes the smoke test | Pass | Built with `--clean` from commit `2c580cc` after removing `build/` and `dist/`; four smoke cases passed (window "Flashy" after about 2 s, embedded list, progress file beside the exe with 999 cards, list override with a 2 word list) |
| 2 | The tag `v0.1.0` is an annotated tag on that commit and the version files say `0.1.0` | Pass | `git show v0.1.0` shows the annotated tag on `2c580cc`; `pyproject.toml` and `__version__` say `0.1.0` |
| 3 | The release has the assets `flash-card.exe` and `flash-card.exe.sha256` | Fail | The upload of `flash-card.exe` (25.8 MB) was rejected with `413 Request Entity Too Large` from the server's reverse proxy; a 1 MB test upload was reset as well; only an 82 byte file passed. The checksum asset alone was deleted again, because a checksum without its file is misleading |
| 4 | The SHA-256 of the file downloaded from the release equals the checksum | Fail | There is no downloadable file; the hash of the local build was `0ac22621ecb8ddad53c5f3d2a35278bebd34cefe458510971106ec52d5bdb47d`, which cannot be verified by others because PyInstaller builds are not bit-for-bit reproducible |
| 5 | The release notes say unsigned Windows build, the `data` folder and how to build, and give the SHA-256 | Fail | The notes say unsigned, the `data` folder and how to build, and state that the file is not attached; they give no SHA-256 because there is no file |
| 6 | CHANGELOG, README and the Install page of the wiki link the release; `check-readme.sh` exit 0 | Pass | Links present in all five files and corrected to say the file is not attached; `check-readme.sh` exit 0 |
| 7 | BC-001, US-001 and PP-001 are updated and reviewed `Go` | Pass | RC-051 to RC-053 |

## Overall Verdict

Go-with-conditions — the tag and the release page exist and the build was verified, but criteria 3, 4 and 5 fail because the server refuses the upload of the executable. The milestone MIL-010 stays open and issue "Create the release and attach the files" stays open until the executable is attached. Reviewed by AI as stand-in for S01; not independent of the author.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Raise the upload limit of the git host's reverse proxy (nginx `client_max_body_size`, and Gitea's attachment limit if set) to at least 50 MB, then ask for the attachment of `flash-card.exe` and its SHA-256 to v0.1.0 (or confirm another place to host the file) | S01 | 2026-10-21 |

---

[MIL-010]: ../milestones/mil-010-release.md
