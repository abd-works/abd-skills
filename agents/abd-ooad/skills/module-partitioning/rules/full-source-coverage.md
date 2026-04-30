---
scanner: full-source-coverage
---

# Rule: Full source coverage — every source file must appear in the partition

**Scanner:** `scanners/full-source-coverage-scanner.py` — **`FullSourceCoverageScanner`**

Every file in the workspace's source directories must be referenced by at least one `Source:` line across all module files (`abd-ooad/modules/*.md`) — allocated to a module, placed in `unallocated.md`, or explicitly placed in `rejected.md`. No source file may be silently dropped.

## DO

- Walk every file in the source directories (context/, corpus/, source/, data/) and confirm it appears in at least one `Source:` line across the module files.
- Place files that don't fit any module into `unallocated.md` with a `Reason:` line explaining the ambiguity.
- Place out-of-scope files into `rejected.md` with a `Reason:` line explaining why they are excluded.
- After the first pass, re-read the source directory listing and confirm full coverage.

## DON'T

- Silently skip source files because they "don't seem important" — every file gets an explicit allocation decision.
- Leave source files unreferenced on the assumption they'll be handled in a later pass — the partition is the single authoritative record of what's in, what's out, and what's pending.
- Assume a source file is covered because a nearby file from the same directory was included — each file must appear individually.
