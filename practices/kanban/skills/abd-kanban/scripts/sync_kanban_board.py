#!/usr/bin/env python3
"""Sync kanban board.json — CLI entry point.

All sync logic lives on KanbanLead.sync_board().

Usage:
    python sync_kanban_board.py --workspace <path>
    python sync_kanban_board.py --workspace <path> --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import war_room_dir  # noqa: E402
from kanban_lead import KanbanLead  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync JIT Kanban board.json")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.resolve()

    lead = KanbanLead(workspace)
    try:
        board = lead.sync_board(dry_run=args.dry_run)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    if args.dry_run:
        print(json.dumps(board, indent=2))
    else:
        wr = war_room_dir(workspace)
        print(f"Synced {wr / 'board.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
