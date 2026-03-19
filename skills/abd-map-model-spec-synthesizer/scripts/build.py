#!/usr/bin/env python3
"""Build AGENTS.md from parts. Thin entry point — delegates to mms_build_agents."""
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_dir / "scripts"))

from mms_build_agents import build_agents

if __name__ == "__main__":
    out = build_agents()
    print(f"Wrote {out}")
