"""Put ``scripts`` and **story-graph-ops** ``scripts`` on ``sys.path`` for optional in-process imports."""
from __future__ import annotations

import sys
from pathlib import Path

_skill_root = Path(__file__).resolve().parents[1]
_scripts = _skill_root / "scripts"
_ops = _skill_root.parent / "story-graph-ops" / "scripts"

for _p in (_scripts, _ops):
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
