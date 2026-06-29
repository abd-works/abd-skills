"""Prepend ``common/scripts`` to ``sys.path`` — import this before any shared graph-ops module."""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[6]
_COMMON_SCRIPTS = _REPO_ROOT / "common" / "scripts"
if _COMMON_SCRIPTS.is_dir() and str(_COMMON_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_COMMON_SCRIPTS))
