#!/usr/bin/env python3
"""Bundle agents/abd-practice-skill-builder/rules/*.md into AGENTS.md.

Uses skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py with
--skill-md AGENTS.md. Edit normative prose in AGENTS.md and rules in rules/;
do not hand-edit the HTML-comment block between bundle markers.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = AGENT_ROOT.parents[1]
BUNDLE = REPO_ROOT / "skills" / "execute_using_rules" / "scripts" / "bundle_rules_into_skill_md.py"


def build() -> int:
    if not BUNDLE.is_file():
        print(f"  ERROR  missing {BUNDLE}", file=sys.stderr)
        return 1
    cmd = [
        sys.executable,
        str(BUNDLE),
        "--skill-root",
        str(AGENT_ROOT),
        "--skill-md",
        "AGENTS.md",
    ]
    r = subprocess.call(cmd)
    if r == 0:
        print(f"  BUNDLED rules into {AGENT_ROOT / 'AGENTS.md'}")
    return r


if __name__ == "__main__":
    sys.exit(build())
