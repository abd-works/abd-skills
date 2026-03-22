#!/usr/bin/env python3
"""Structural scanner: abd-skill-builder ships standards (library) + scaffold script."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "content" / "parts" / "library" / "skill-repo-standards.md",
    ROOT / "content" / "parts" / "library" / "builder-vs-operator.md",
    ROOT / "content" / "parts" / "library" / "skill-standards-section-3.md",
    ROOT / "content" / "built" / "README.md",
    ROOT / "docs" / "delivery.md",
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
