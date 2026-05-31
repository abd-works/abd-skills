#!/usr/bin/env python3
"""Build script for abd-practice-skill-builder agent.

Bundling rules into SKILL.md/AGENTS.md has been removed. Rules live only in
rules/*.md and are read directly by agents at generate/validate time.
This script is retained as a placeholder for future build steps.
"""

import sys


def build() -> int:
    print("abd-practice-skill-builder: no build steps required (bundling removed).")
    return 0


if __name__ == "__main__":
    sys.exit(build())
