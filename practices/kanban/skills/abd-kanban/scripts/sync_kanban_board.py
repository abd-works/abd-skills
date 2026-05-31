#!/usr/bin/env python3
"""Sync kanban board.json — ticket-based JIT Kanban model.

Reads board.json, checks for stage completions (using kanban.json as the
skill authority), advances tickets or flags for scatter, updates metrics.

Usage:
    python kanban/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <path>
    python kanban/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <path> --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import (
    Ticket,
    advance_ticket_to_stage,
    append_metrics_log,
    get_stage_def,
    load_board,
    load_kanban_board,
    next_stage,
    save_board,
    war_room_dir,
)


def _advance_or_flag(
    ticket: Ticket,
    config_name: str,
    kb_map: dict,
    workspace: Path,
) -> str:
    """Check if ticket stage is complete; advance or flag for scatter. Returns action taken."""
    kb = kb_map.get(config_name)
    if not kb:
        return "no_change"

    current_def = get_stage_def(kb, ticket.stage)
    if not current_def:
        return "no_change"

    if not ticket.is_stage_complete(current_def):
        return "no_change"

    nxt = next_stage(kb, ticket.stage)
    if nxt is None:
        ticket.completed_stage = datetime.now(timezone.utc).isoformat()
        append_metrics_log(workspace, {
            "event": "ticket_complete",
            "ticket_id": ticket.ticket_id,
            "lineage": ticket.lineage,
            "stage": ticket.stage,
        })
        return "complete"

    if nxt.scope != current_def.scope:
        ticket.completed_stage = datetime.now(timezone.utc).isoformat()
        append_metrics_log(workspace, {
            "event": "scatter_needed",
            "ticket_id": ticket.ticket_id,
            "from_scope": current_def.scope,
            "to_scope": nxt.scope,
            "next_stage": nxt.name,
        })
        return "scatter_needed"

    old_stage = ticket.stage
    advance_ticket_to_stage(ticket, nxt)
    append_metrics_log(workspace, {
        "event": "stage_advance",
        "ticket_id": ticket.ticket_id,
        "lineage": ticket.lineage,
        "from_stage": old_stage,
        "to_stage": nxt.name,
    })
    return "advanced"


def sync_board(workspace: Path, dry_run: bool = False) -> dict:
    wr = war_room_dir(workspace)
    if not wr.is_dir():
        raise FileNotFoundError(f"War room missing: {wr}")

    board = load_board(workspace)
    config_name = board.get("stage_configuration") or board.get("system_of_work", "")
    kb_map = load_kanban_board(workspace)

    active_tickets = [Ticket.from_dict(t) for t in board.get("active", [])]
    done_tickets = [Ticket.from_dict(t) for t in board.get("done", [])]
    backlog_tickets = [Ticket.from_dict(t) for t in board.get("backlog", [])]
    archived = board.get("archived", [])

    new_active = []
    new_done = []

    for ticket in active_tickets:
        action = _advance_or_flag(ticket, config_name, kb_map, workspace)
        if action == "complete":
            archived.append(ticket.to_dict())
        elif action == "scatter_needed":
            new_done.append(ticket)
        elif action == "advanced":
            new_active.append(ticket)
        else:
            new_active.append(ticket)

    for ticket in done_tickets:
        new_done.append(ticket)

    team = board.get("team") or board.get("wip_policy", {})
    while backlog_tickets and len(new_active) < 10:
        ticket = backlog_tickets.pop(0)
        new_active.append(ticket)

    board["active"] = [t.to_dict() for t in new_active]
    board["done"] = [t.to_dict() for t in new_done]
    board["backlog"] = [t.to_dict() for t in backlog_tickets]
    board["archived"] = archived
    board["synced_at"] = datetime.now(timezone.utc).isoformat()

    if not dry_run:
        save_board(workspace, board)

    return board


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync JIT Kanban board.json")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    try:
        board = sync_board(workspace, dry_run=args.dry_run)
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
