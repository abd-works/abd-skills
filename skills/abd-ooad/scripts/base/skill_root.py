"""
skill_root.py — single source of truth for locating the skill root directory.

Every script in scripts/base/ lives two levels below the skill root:
    <skill_root>/scripts/base/<script>.py

Import and use:
    from skill_root import SKILL_ROOT
"""
from pathlib import Path

# base/ -> scripts/ -> skill root
SKILL_ROOT: Path = Path(__file__).resolve().parents[2]
