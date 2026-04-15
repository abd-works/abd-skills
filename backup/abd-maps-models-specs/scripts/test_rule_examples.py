#!/usr/bin/env python3
"""
Fail if any governance rule under rules/*.md is missing the canonical DO/DON'T structure.

Rules follow the same shape as abd-maps-models-specs-old: guidance, then **DO** (with examples),
then **DON'T** or **DO NOT** (with examples). Examples are usually fenced ``` blocks or concrete bullets.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"

# Line-start markers (old rules use these as section headers).
RE_DO = re.compile(r"^\*\*DO\*\*\s*$", re.MULTILINE)
RE_DONT = re.compile(r"^\*\*DON'T\*\*\s*$", re.MULTILINE)
RE_DO_NOT = re.compile(r"^\*\*DO NOT\*\*\s*$", re.MULTILINE)


def main() -> None:
    missing: list[str] = []
    for p in sorted(RULES.glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        text = p.read_text(encoding="utf-8")
        if not RE_DO.search(text):
            missing.append(f"{p.name} (missing **DO** section header)")
            continue
        if not (RE_DONT.search(text) or RE_DO_NOT.search(text)):
            missing.append(f"{p.name} (missing **DON'T** or **DO NOT** section header)")

    if missing:
        print(
            "test_rule_examples.py: each rule must have line-start **DO** and **DON'T** or **DO NOT** "
            "(see rules/README.md — match legacy rule format).\n"
            "Problems:\n  - " + "\n  - ".join(missing),
            file=sys.stderr,
        )
        sys.exit(1)
    print(
        "test_rule_examples.py: OK (all rules have **DO** and **DON'T** / **DO NOT**)",
        flush=True,
    )


if __name__ == "__main__":
    main()
