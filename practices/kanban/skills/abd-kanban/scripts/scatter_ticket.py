#!/usr/bin/env python3
"""Scatter a completed ticket into child tickets at finer scope.

When a ticket completes a stage whose next stage has finer scope (e.g. all→increment,
increment→sprint), this script decomposes it into child tickets.

Usage:
    python kanban/skills/abd-kanban/scripts/scatter_ticket.py \
        --workspace <path> --ticket <ticket_id> --children <child_spec_json>

child_spec_json is a JSON array of objects:
    [
        {"id": "inc-1", "name": "Increment 1", "priority": 1},
        {"id": "inc-2", "name": "Increment 2", "priority": 2}
    ]

The script:
1. Archives the parent ticket (moves from done to archived with timestamps)
2. Creates child tickets at the next stage's scope level
3. Populates children with skills from system of work for the next stage
4. Places children in backlog ordered by priority
5. Logs scatter event to metrics-log.jsonl
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
    SkillProgress,
    append_metrics_log,
    get_stage_def,
    load_board,
    load_system_of_work,
    next_stage,
    populate_skills_for_stage,
    save_board,
    war_room_dir,
)


def scatter(
    workspace: Path,
    ticket_id: str,
    children_spec: list[dict],
    dry_run: bool = False,
) -> list[Ticket]:
    """Scatter a parent ticket into children."""
    board = load_board(workspace)
    sow_name = board.get("system_of_work", "")
    sow_map = load_system_of_work(workspace)
    sow = sow_map.get(sow_name)
    if not sow:
        raise ValueError(f"System of work '{sow_name}' not found")

    done_list = [Ticket.from_dict(t) for t in board.get("done", [])]
    parent = None
    parent_idx = None
    for i, t in enumerate(done_list):
        if t.ticket_id == ticket_id:
            parent = t
            parent_idx = i
            break

    if parent is None:
        active_list = [Ticket.from_dict(t) for t in board.get("active", [])]
        for i, t in enumerate(active_list):
            if t.ticket_id == ticket_id:
                parent = t
                board["active"] = [
                    tt for j, tt in enumerate(board.get("active", []))
                    if j != i
                ]
                break

    if parent is None:
        raise ValueError(f"Ticket '{ticket_id}' not found in done or active")

    if parent_idx is not None:
        done_list.pop(parent_idx)
        board["done"] = [t.to_dict() for t in done_list]

    nxt = next_stage(sow, parent.stage)
    if nxt is None:
        raise ValueError(f"No next stage after '{parent.stage}' — cannot scatter")

    now = datetime.now(timezone.utc).isoformat()
    parent.completed_stage = now
    parent.scatter_to = [c["id"] for c in children_spec]

    archived = board.get("archived", [])
    archived.append(parent.to_dict())
    board["archived"] = archived

    children: list[Ticket] = []
    for spec in children_spec:
        child = Ticket(
            ticket_id=spec["id"],
            lineage=parent.lineage + [spec.get("name", spec["id"])],
            scope_level=nxt.scope,
            stage=nxt.name,
            priority=spec.get("priority", 1),
            scatter_from=parent.ticket_id,
        )
        populate_skills_for_stage(child, nxt)
        children.append(child)

    backlog = [Ticket.from_dict(t) for t in board.get("backlog", [])]
    backlog.extend(children)
    backlog.sort(key=lambda t: t.priority)
    board["backlog"] = [t.to_dict() for t in backlog]

    if not dry_run:
        save_board(workspace, board)
        append_metrics_log(workspace, {
            "event": "scatter",
            "parent_ticket": ticket_id,
            "parent_lineage": parent.lineage,
            "children": [c.ticket_id for c in children],
            "from_stage": parent.stage,
            "to_stage": nxt.name,
            "from_scope": parent.scope_level,
            "to_scope": nxt.scope,
        })

    return children


def main() -> int:
    parser = argparse.ArgumentParser(description="Scatter a ticket into children")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--ticket", required=True, help="Parent ticket ID to scatter")
    parser.add_argument("--children", required=True, help="JSON array of child specs")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    children_spec = json.loads(args.children)

    try:
        children = scatter(workspace, args.ticket, children_spec, dry_run=args.dry_run)
    except (FileNotFoundError, ValueError) as e:
        print(e, file=sys.stderr)
        return 1

    print(f"Scattered '{args.ticket}' into {len(children)} children:")
    for c in children:
        print(f"  - {c.ticket_id} ({c.scope_level}, stage: {c.stage}, priority: {c.priority})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
