"""Put all scripts the lead's orchestration test invokes on sys.path."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[3]  # agents/abd-delivery-lead/tests -> repo root

_PATHS = [
    _REPO_ROOT / "skills" / "execute_using_rules" / "scripts",
    _REPO_ROOT / "skills" / "track_task" / "scripts",
    _REPO_ROOT / "skills" / "abd-delivery-planning" / "scripts",
    _REPO_ROOT / "skills" / "abd-delivery-planning" / "scanners",
    _REPO_ROOT / "skills" / "story-graph-ops" / "scripts",
]
for _p in _PATHS:
    s = str(_p)
    if _p.is_dir() and s not in sys.path:
        sys.path.insert(0, s)
