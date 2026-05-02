"""Put scanner + generator scripts on sys.path for in-process imports."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_SKILL_ROOT = _HERE.parents[1]                 # .../skills/abd-delivery-planning
_SKILLS_DIR = _SKILL_ROOT.parent               # .../skills

_PATHS = [
    _SKILL_ROOT / "scanners",
    _SKILL_ROOT / "scripts",
    _SKILLS_DIR / "execute-skill-using-skills-rules" / "scripts",
    _SKILLS_DIR / "track_task" / "scripts",
]
for _p in _PATHS:
    s = str(_p)
    if _p.is_dir() and s not in sys.path:
        sys.path.insert(0, s)
