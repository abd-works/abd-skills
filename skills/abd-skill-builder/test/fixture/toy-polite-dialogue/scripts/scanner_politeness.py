#!/usr/bin/env python3
"""Structural check: SKILL.md and AGENTS.md mention politeness cues."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
    if "polite" not in skill_md:
        print("FAIL: SKILL.md should mention 'polite'", file=sys.stderr)
        return 1
    agents = ROOT / "AGENTS.md"
    if not agents.is_file():
        print("FAIL: run scripts/build.py first (AGENTS.md missing)", file=sys.stderr)
        return 1
    body = agents.read_text(encoding="utf-8").lower()
    for needle in ("please", "thank"):
        if needle not in body:
            print(f"FAIL: AGENTS.md should include polite vocabulary ({needle!r})", file=sys.stderr)
            return 1
    print("OK: politeness scanner passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
