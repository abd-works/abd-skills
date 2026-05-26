#!/usr/bin/env python3
"""Generate slot-NN-start.md for a run from run-catalog + system-of-work.

Slots are materialized when a run **opens**, not when the plan is first approved.

Usage:

    python delivery/skills/abd-delivery-war-room/scripts/generate_run_slots.py \\
        --workspace C:\\dev\\abd-pet-store-demo --run 8

    python ... --run 8 --dry-run
    python ... --run 8 --force   # regenerate even if run-state says slots_generated
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import generate_run_slots  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize war-room slots for a run")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--run", required=True, type=int, help="Run number from run-catalog.json")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    try:
        paths = generate_run_slots(
            workspace, args.run, dry_run=args.dry_run, force=args.force
        )
    except (FileNotFoundError, ValueError) as e:
        print(e, file=sys.stderr)
        return 1
    verb = "Would write" if args.dry_run else "Wrote"
    for p in paths:
        print(f"{verb} {p}")
    print(f"{verb} {len(paths)} slot-start files for run {args.run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
