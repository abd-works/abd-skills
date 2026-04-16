#!/usr/bin/env python3
"""Shim: use :mod:`scanner_runner` in **execute_using_rules** (same call sequence for all scanners)."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILLS = _HERE.parent.parent
_ER = _SKILLS / "execute_using_rules" / "scripts"
if _ER.is_dir():
    er = str(_ER)
    if er not in sys.path:
        sys.path.insert(0, er)

from scanner_runner import (  # noqa: E402
    execute_scan,
    execute_scan_with_workspace,
    load_workspace_graph_json,
    main_with_scanner,
)

__all__ = [
    "execute_scan",
    "execute_scan_with_workspace",
    "load_workspace_graph_json",
    "main_with_scanner",
]
