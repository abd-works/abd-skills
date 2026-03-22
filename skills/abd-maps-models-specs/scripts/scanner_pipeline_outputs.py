#!/usr/bin/env python3
"""Operator scanner: Phase 0 audit exists; Phase 2 artifacts exist."""

from __future__ import annotations

import sys
from pathlib import Path

from _config import PHASE0, PHASE2

REQUIRED = [
    PHASE0 / "phase0_audit_metrics.json",
    PHASE2 / "mm3_terms_layer.json",
    PHASE2 / "mm3_mechanisms.json",
    PHASE2 / "mm3_candidate_queue.json",
]


def main() -> int:
    missing = [str(p) for p in REQUIRED if not p.is_file()]
    if missing:
        print("FAIL: missing outputs — run: python scripts/build.py", file=sys.stderr)
        for m in missing:
            print(" ", m, file=sys.stderr)
        return 1
    print("OK: pipeline outputs present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
