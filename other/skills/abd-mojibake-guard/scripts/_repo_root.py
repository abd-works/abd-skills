"""Resolve abd-skills repo root from this skill's scripts folder."""
from __future__ import annotations

from pathlib import Path


def abd_skills_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here.parent, *here.parents):
        if (candidate / "scripts" / "scan_encoding.py").is_file():
            return candidate
    raise FileNotFoundError(
        "abd-skills repo root not found (expected scripts/scan_encoding.py in an ancestor directory)"
    )
