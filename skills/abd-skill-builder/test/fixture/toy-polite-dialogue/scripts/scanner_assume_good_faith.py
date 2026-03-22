#!/usr/bin/env python3
"""Enforce rules/assume-good-faith.md: converse phase commits to good-faith, non-dismissive tone."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "rules" / "assume-good-faith.md"
AGENTS = ROOT / "AGENTS.md"


def main() -> int:
    if not RULE.is_file():
        print(f"FAIL: missing rule file {RULE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    rule_text = RULE.read_text(encoding="utf-8")
    if "good faith" not in rule_text.lower():
        print("FAIL: rule assume-good-faith.md should mention good faith", file=sys.stderr)
        return 1

    if not AGENTS.is_file():
        print("FAIL: run scripts/build.py first (AGENTS.md missing)", file=sys.stderr)
        return 1
    agents = AGENTS.read_text(encoding="utf-8")
    m = re.search(r"## Phase: converse\b.*?(?=## Phase:|\Z)", agents, re.DOTALL | re.IGNORECASE)
    if not m:
        print("FAIL: AGENTS.md missing ## Phase: converse section", file=sys.stderr)
        return 1
    block = m.group(0).lower()
    if "good faith" not in block:
        print(
            "FAIL: Converse phase must mention good faith per rule assume-good-faith",
            file=sys.stderr,
        )
        return 1
    if "dismiss" not in block and "belittling" not in block:
        print(
            "FAIL: Converse phase should address dismissive/belittling tone per rule",
            file=sys.stderr,
        )
        return 1

    print("OK: scanner_assume_good_faith (rule assume-good-faith.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
