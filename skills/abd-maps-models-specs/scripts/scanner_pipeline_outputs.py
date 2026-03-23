#!/usr/bin/env python3
"""Operator scanner: Phase 2 artifacts exist."""

from __future__ import annotations

import sys
from pathlib import Path

from _config import (
    CANDIDATE_QUEUE_JSON,
    MECHANISMS_JSON,
    PHASE2,
    TERMS_LAYER_JSON,
)

REQUIRED = [
    PHASE2 / TERMS_LAYER_JSON,
    PHASE2 / MECHANISMS_JSON,
    PHASE2 / CANDIDATE_QUEUE_JSON,
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
