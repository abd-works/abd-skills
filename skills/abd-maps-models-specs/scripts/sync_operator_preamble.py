#!/usr/bin/env python3
"""
Prepend content/parts/operator-role.md to the top of every file in content/parts/phases/.

Source of truth: content/parts/operator-role.md
Run after editing that file:  python scripts/sync_operator_preamble.py
Then refresh AGENTS.md:       python scripts/build.py

If a phase file already contains <!-- operator-role:start --> ... <!-- operator-role:end -->,
the block is replaced. Otherwise the preamble is inserted before the first line that starts
with # (the phase title).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"
ROLE_PATH = PARTS / "operator-role.md"
PHASES_DIR = PARTS / "phases"

PHASE_FILES = [
    "context-readiness.md",
    "canonical-context.md",
    "terms-mechanisms.md",
    "story-map.md",
    "domain-types.md",
    "variant-classification.md",
    "deepen.md",
    "integrate.md",
    "validate-render.md",
]

MARKER_START = "<!-- operator-role:start -->\n"
MARKER_END = "\n<!-- operator-role:end -->\n"


def _strip_existing_preamble(text: str) -> str:
    if "<!-- operator-role:start -->" not in text:
        return text
    m = re.search(
        r"<!-- operator-role:start -->.*?<!-- operator-role:end -->\s*",
        text,
        flags=re.DOTALL,
    )
    if not m:
        return text
    return text[m.end() :].lstrip("\n")


def _insert_before_first_heading(text: str, preamble: str) -> str:
    """Insert preamble before the first # heading line."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("#"):
            return preamble + "\n" + "".join(lines[i:])
    return preamble + "\n" + text


def sync_file(phase_path: Path, role_text: str) -> None:
    raw = phase_path.read_text(encoding="utf-8")
    body = _strip_existing_preamble(raw)
    block = MARKER_START + role_text.rstrip() + MARKER_END
    if body.lstrip().startswith("#"):
        new = _insert_before_first_heading(body, block)
    else:
        new = block + "\n" + body
    phase_path.write_text(new, encoding="utf-8")


def main() -> None:
    if not ROLE_PATH.is_file():
        raise SystemExit(f"Missing {ROLE_PATH}")
    role_text = ROLE_PATH.read_text(encoding="utf-8").strip() + "\n"
    for fname in PHASE_FILES:
        p = PHASES_DIR / fname
        if not p.is_file():
            raise SystemExit(f"Missing phase file: {p}")
        sync_file(p, role_text)
        print(f"Updated {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
