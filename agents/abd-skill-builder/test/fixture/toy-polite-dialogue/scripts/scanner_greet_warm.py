#!/usr/bin/env python3
"""Enforce rules/greet-warm-brief.md: greet phase acknowledges user and stays brief."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "rules" / "greet-warm-brief.md"
AGENTS = ROOT / "AGENTS.md"


def main() -> int:
    if not RULE.is_file():
        print(f"FAIL: missing rule file {RULE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    rule_text = RULE.read_text(encoding="utf-8")
    if "acknowledge" not in rule_text.lower():
        print("FAIL: rule greet-warm-brief.md should mention acknowledge", file=sys.stderr)
        return 1

    if not AGENTS.is_file():
        print("FAIL: run scripts/base/build.py first (AGENTS.md missing)", file=sys.stderr)
        return 1
    agents = AGENTS.read_text(encoding="utf-8")
    # Greet section must exist and mention acknowledgment / warm framing
    m = re.search(r"## Phase: greet\b.*?(?=## Phase:|\Z)", agents, re.DOTALL | re.IGNORECASE)
    if not m:
        print("FAIL: AGENTS.md missing ## Phase: greet section", file=sys.stderr)
        return 1
    block = m.group(0).lower()
    if "acknowledge" not in block:
        print("FAIL: Greet phase must acknowledge user per rule greet-warm-brief", file=sys.stderr)
        return 1
    if len(block) > 2500:
        print("FAIL: Greet phase content unexpectedly long (keep brief)", file=sys.stderr)
        return 1

    print("OK: scanner_greet_warm (rule greet-warm-brief.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
