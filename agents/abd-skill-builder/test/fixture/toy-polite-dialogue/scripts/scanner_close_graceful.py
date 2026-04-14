#!/usr/bin/env python3
"""Enforce rules/close-graceful.md: close phase invites follow-up."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "rules" / "close-graceful.md"
AGENTS = ROOT / "AGENTS.md"


def main() -> int:
    if not RULE.is_file():
        print(f"FAIL: missing rule file {RULE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    rule_lower = RULE.read_text(encoding="utf-8").lower()
    if "follow" not in rule_lower and "invit" not in rule_lower:
        print("FAIL: close-graceful rule should mention follow-up or invite", file=sys.stderr)
        return 1

    if not AGENTS.is_file():
        print("FAIL: run scripts/base/build.py first (AGENTS.md missing)", file=sys.stderr)
        return 1
    agents = AGENTS.read_text(encoding="utf-8")
    m = re.search(r"## Phase: close\b.*?(?=## |\Z)", agents, re.DOTALL | re.IGNORECASE)
    if not m:
        print("FAIL: AGENTS.md missing ## Phase: close section", file=sys.stderr)
        return 1
    block = m.group(0).lower()
    if not any(w in block for w in ("follow", "invite", "another question", "continue")):
        print(
            "FAIL: Close phase must invite follow-up per rule close-graceful.md",
            file=sys.stderr,
        )
        return 1

    print("OK: scanner_close_graceful (rule close-graceful.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
