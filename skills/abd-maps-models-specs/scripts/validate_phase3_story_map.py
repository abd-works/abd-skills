#!/usr/bin/env python3
"""Compatibility CLI — delegates to ``scanners/phase3_story_map_evidence.py`` (Operator scanner)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from scanners.phase3_story_map_evidence import main

if __name__ == "__main__":
    raise SystemExit(main())
