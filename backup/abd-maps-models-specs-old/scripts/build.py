#!/usr/bin/env python3
"""Build parts/steps/built/ then AGENTS.md. Same idea as solution modeler: phases → built, then assemble."""
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_dir / "scripts"))

from build_agents import build_agents
from build_steps import build_steps

if __name__ == "__main__":
    n = build_steps()
    print(f"Built {n} file(s) under parts/steps/built/")
    out = build_agents()
    print(f"Wrote {out}")
