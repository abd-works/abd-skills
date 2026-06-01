#!/usr/bin/env python3
"""One kanban-lead scan cycle — CLI entry point.

All orchestration logic lives on KanbanLead.run_scan().

Usage:
  python run_kanban_scan.py --workspace <path>
  python run_kanban_scan.py --workspace <path> --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from kanban_lead import KanbanLead  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one kanban-lead scan cycle")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--json", action="store_true", help="Print full report JSON")
    args = parser.parse_args()

    lead = KanbanLead(args.workspace.resolve())
    report = lead.run_scan()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Scan cycle {report['cycle']}: {len(report['spawns'])} spawn(s) recommended")
        for s in report["spawns"]:
            print(f"  spawn {s['role']} instance {s['instance']} ({s['reason']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
