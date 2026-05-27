"""Put track_task scripts on sys.path for in-process imports."""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if _SCRIPTS.is_dir() and str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
