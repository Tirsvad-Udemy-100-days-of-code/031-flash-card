# RC-081: The tag v0.2.0 is annotated

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-081 |
| CrossReference | [MIL-012], [RC-072] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-012], criterion 5 (the tag `v0.2.0` is an annotated tag on the commit that is built; `v0.1.0` is not moved), which [RC-072] marked Fail
- Checklist used: none exists; criterion 5 of MIL-012
- Scope: delta re-review of criterion 5 after the Product Owner asked for the tag to be annotated
- Language and domain: n/a (record of results)
- Language reviewer: none
- Mode: autonomous, not independent (reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 5 | The tag `v0.2.0` is an annotated tag on that commit; `v0.1.0` is not moved | Pass | At the Product Owner's request the lightweight tag on the host was replaced by the annotated tag object `a92bdd9` ("Flash Card 0.2.0: menu bar and progress per word list") with a forced update of that one tag; it dereferences to the same commit `d7ca24d`; `v0.1.0` is unchanged (`2c580cc`); the release `v0.2.0` still exists, is not a draft and points to the tag |

## Overall Verdict

Go — criterion 5 of MIL-012 is met. The remaining condition of RC-072 is the attachment of the executable to the release (upload limit of the git host). Reviewed by AI as stand-in for S01; not independent of the author.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Raise the upload limit of the git host, then attach `flash-card.exe` and its checksum to `v0.2.0` | S01 | 2026-10-21 |

---

[MIL-012]: ../milestones/mil-012-release-0-2-0.md
[RC-072]: ./rc-072-release-v0-2-0.md
