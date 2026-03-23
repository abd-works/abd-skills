#!/usr/bin/env python3
"""Compatibility CLI — delegates to ``scanners/context_index_contract.py`` (Operator scanner)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from scanners.context_index_contract import main

if __name__ == "__main__":
    raise SystemExit(main())
