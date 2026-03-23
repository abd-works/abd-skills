#!/usr/bin/env python3
"""Structural scanner: abd-skill-builder ships standards (library) + scaffold script."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Canonical authoring layout: `parts/library/`. (Some checkouts mirror under `content/parts/library/`.)
_LIBRARY = ROOT / "parts" / "library"
REQUIRED = [
    _LIBRARY / "skill-repo-standards.md",
    _LIBRARY / "builder-vs-operator.md",
    _LIBRARY / "skill-standards-section-3.md",
    _LIBRARY / "rules-and-automated-checks.md",
    ROOT / "content" / "built" / "README.md",
    ROOT / "conf" / "README.md",
    ROOT / "conf" / "abd-config.json",
    ROOT / "scripts" / "scaffold_skill.py",
]


def main() -> int:
    missing = [str(p) for p in REQUIRED if not p.is_file()]
    if missing:
        print("FAIL: abd-skill-builder layout incomplete:", file=sys.stderr)
        for m in missing:
            print(" ", m, file=sys.stderr)
        return 1
    print("OK: abd-skill-builder standards + scaffold present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
