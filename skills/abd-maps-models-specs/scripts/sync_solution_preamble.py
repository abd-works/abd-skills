#!/usr/bin/env python3
"""
Remove legacy `<!-- solution-analyst-role:start -->` … `<!-- solution-analyst-role:end -->` blocks from
source files under `content/parts/phases/` (not `phases/built/`).

**Canonical role text** lives in `content/parts/solution-analyst-role.md`. It is **not** duplicated in
source phase files. **`python scripts/build.py`** (merge) assembles **built** phase bundles
(`content/parts/phases/built/<slug>.md`, etc.) and injects the role there via `MapsInstructions`.

Run after a one-time cleanup or if a phase file still contains old markers:

    python scripts/sync_solution_preamble.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_support import phase_fnames_from_skill_config

PARTS = ROOT / "content" / "parts"
PHASES_DIR = PARTS / "phases"

_LEGACY_BLOCK = re.compile(
    r"<!-- (?:solution-analyst-role|solution-role|operator-role):start -->.*?<!-- (?:solution-analyst-role|solution-role|operator-role):end -->\s*",
    flags=re.DOTALL,
)


def _strip_existing_preamble(text: str) -> str:
    if not any(
        m in text
        for m in (
            "<!-- solution-analyst-role:start -->",
            "<!-- solution-role:start -->",
            "<!-- operator-role:start -->",
        )
    ):
        return text
    m = _LEGACY_BLOCK.search(text)
    if not m:
        return text
    return text[m.end() :].lstrip("\n")


def strip_file(phase_path: Path) -> bool:
    raw = phase_path.read_text(encoding="utf-8")
    stripped = _strip_existing_preamble(raw)
    if stripped == raw:
        return False
    phase_path.write_text(stripped.lstrip("\n"), encoding="utf-8")
    return True


def main() -> None:
    cfg_path = ROOT / "skill-config.json"
    if not cfg_path.is_file():
        raise SystemExit(f"Missing {cfg_path}")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    phase_files = phase_fnames_from_skill_config(cfg)
    if not phase_files:
        raise SystemExit("skill-config.json has no phase_files")
    updated = 0
    for fname in phase_files:
        p = PHASES_DIR / fname
        if not p.is_file():
            raise SystemExit(f"Missing phase file: {p}")
        if strip_file(p):
            print(f"Stripped legacy preamble from {p.relative_to(ROOT)}", flush=True)
            updated += 1
    # Optional: other *.md in phases/ root (not in skill-config), e.g. stray copies
    for p in sorted(PHASES_DIR.glob("*.md")):
        if p.name in phase_files or p.parent != PHASES_DIR:
            continue
        if strip_file(p):
            print(f"Stripped legacy preamble from {p.relative_to(ROOT)}", flush=True)
            updated += 1
    if updated == 0:
        print("sync_solution_preamble: no legacy preamble blocks found in source phase files.", flush=True)
    else:
        print(f"sync_solution_preamble: updated {updated} file(s). Run python scripts/build.py --merge-only", flush=True)


if __name__ == "__main__":
    main()
