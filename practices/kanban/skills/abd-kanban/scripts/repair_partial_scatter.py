#!/usr/bin/env python3
"""Add missing increment tickets when a partial scatter left children out."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import Ticket, load_board, save_board  # noqa: E402
from lead_scatter import children_spec_for_ticket, increments_from_thin_slicing  # noqa: E402


def repair_partial_scatter(workspace: Path, parent_id: str) -> list[str]:
    board = load_board(workspace)
    parent = None
    for raw in board.get("archived", []):
        if raw.get("ticket_id") == parent_id:
            parent = Ticket.from_dict(raw)
            break
    if parent is None:
        raise SystemExit(f"Archived parent not found: {parent_id}")

    spec = children_spec_for_ticket(workspace, parent)
    existing = {t.get("ticket_id") for t in board.get("backlog", [])}
    existing |= {t.get("ticket_id") for t in board.get("active", [])}
    existing |= {t.get("ticket_id") for t in board.get("done", [])}

    now = datetime.now(timezone.utc).isoformat()
    added: list[str] = []
    backlog = board.get("backlog", [])

    for child in spec:
        cid = child["id"]
        if cid in existing:
            continue
        ticket = Ticket(
            ticket_id=cid,
            lineage=parent.lineage + [child.get("name", cid)],
            scope_level="increment",
            stage="exploration",
            priority=child.get("priority", 1),
            created=now,
            scatter_from=parent_id,
            entered_stage=now,
        )
        backlog.append(ticket.to_dict())
        added.append(cid)

    if added:
        backlog.sort(key=lambda t: t.get("priority", 99))
        board["backlog"] = backlog
        parent.scatter_to = [c["id"] for c in spec]
        for i, raw in enumerate(board["archived"]):
            if raw.get("ticket_id") == parent_id:
                board["archived"][i] = parent.to_dict()
                break
        save_board(workspace, board)

    return added


if __name__ == "__main__":
    ws = Path(sys.argv[1] if len(sys.argv) > 1 else "c:/dev/bess-replacement")
    parent = sys.argv[2] if len(sys.argv) > 2 else "1-terminal-requestor-screen-composition"
    added = repair_partial_scatter(ws, parent)
    print(json.dumps({"added": added, "count": len(added)}))
