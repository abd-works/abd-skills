"""
build.py — assemble AGENTS.md from content/parts/

Usage:
    python scripts/base/build.py

Reads skill-config.json, walks content/parts/ in phase order,
merges library files, and writes AGENTS.md at the skill root.
Copy this file from abd-skill-builder's scripts/build.py and
adjust paths if needed.
"""
import sys
from pathlib import Path
from skill_root import SKILL_ROOT

sys.path.insert(0, str(SKILL_ROOT / "scripts" / "base"))

# Import assembler from abd-skill-builder if available,
# or copy assembler.py / instructions.py alongside this file.
try:
    from assembler import build  # type: ignore
except ImportError:
    raise ImportError(
        "assembler.py not found. Copy scripts/base/assembler.py and scripts/base/instructions.py "
        "from abd-skill-builder into this skill's scripts/base/ folder."
    )

if __name__ == "__main__":
    build(skill_root=SKILL_ROOT)
