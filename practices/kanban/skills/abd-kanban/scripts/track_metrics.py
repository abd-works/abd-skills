#!/usr/bin/env python3
"""Compute delivery metrics from board.json and metrics-log.jsonl.

Reports:
- Cycle time per stage (avg, min, max)
- Cycle time per scope level (all, increment, sprint)
- Bottleneck detection (which stage/skill has most WIP)
- Throughput (tickets completed per time window)

Usage:
    python kanban/skills/abd-kanban/scripts/track_metrics.py --workspace <path>
    python kanban/skills/abd-kanban/scripts/track_metrics.py --workspace <path> --json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import (
    Ticket,
    load_board,
    load_system_of_work,
    get_stage_def,
    war_room_dir,
)


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def compute_metrics(workspace: Path) -> dict:
    board = load_board(workspace)
    sow_name = board.get("system_of_work", "")
    sow_map = load_system_of_work(workspace)
    sow = sow_map.get(sow_name)

    all_tickets = []
    for lst in ("active", "done", "archived"):
        for raw in board.get(lst, []):
            if isinstance(raw, dict) and "ticket_id" in raw:
                all_tickets.append(Ticket.from_dict(raw))

    stage_cycle_times: dict[str, list[float]] = defaultdict(list)
    skill_durations: dict[str, list[float]] = defaultdict(list)
    scope_cycle_times: dict[str, list[float]] = defaultdict(list)

    for ticket in all_tickets:
        entered = _parse_iso(ticket.entered_stage)
        completed = _parse_iso(ticket.completed_stage)
        if entered and completed:
            hours = (completed - entered).total_seconds() / 3600.0
            stage_cycle_times[ticket.stage].append(hours)
            scope_cycle_times[ticket.scope_level].append(hours)

        for skill_name, sp in ticket.progress.items():
            start = _parse_iso(sp.start)
            end = _parse_iso(sp.end)
            if start and end:
                hours = (end - start).total_seconds() / 3600.0
                skill_durations[skill_name].append(hours)

    bottlenecks = []
    active_tickets = [Ticket.from_dict(t) for t in board.get("active", [])]
    stage_wip: dict[str, int] = defaultdict(int)
    skill_wip: dict[str, int] = defaultdict(int)

    for ticket in active_tickets:
        stage_wip[ticket.stage] += 1
        if sow:
            stage_def = get_stage_def(sow, ticket.stage)
            if stage_def:
                for skill_def in stage_def.skills:
                    sp = ticket.progress.get(skill_def.skill)
                    if sp is None or sp.status == "to_do":
                        skill_wip[f"{ticket.stage}:{skill_def.skill}"] += 1

    if stage_wip:
        max_stage = max(stage_wip, key=stage_wip.get)
        if stage_wip[max_stage] > 1:
            bottlenecks.append({
                "type": "stage_wip",
                "stage": max_stage,
                "count": stage_wip[max_stage],
            })

    if skill_wip:
        max_skill = max(skill_wip, key=skill_wip.get)
        if skill_wip[max_skill] > 2:
            bottlenecks.append({
                "type": "skill_waiting",
                "skill": max_skill,
                "count": skill_wip[max_skill],
            })

    def _stats(values: list[float]) -> dict:
        if not values:
            return {"count": 0}
        return {
            "count": len(values),
            "avg_hours": round(sum(values) / len(values), 2),
            "min_hours": round(min(values), 2),
            "max_hours": round(max(values), 2),
        }

    return {
        "stage_cycle_times": {k: _stats(v) for k, v in stage_cycle_times.items()},
        "scope_cycle_times": {k: _stats(v) for k, v in scope_cycle_times.items()},
        "skill_durations": {k: _stats(v) for k, v in skill_durations.items()},
        "bottlenecks": bottlenecks,
        "active_tickets": len(active_tickets),
        "backlog_tickets": len(board.get("backlog", [])),
        "archived_tickets": len(board.get("archived", [])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute delivery metrics")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    workspace = args.workspace.resolve()

    wr = war_room_dir(workspace)
    if not wr.is_dir():
        print(f"War room missing: {wr}", file=sys.stderr)
        return 1

    metrics = compute_metrics(workspace)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print("=== Delivery Metrics ===\n")
        print(f"Active tickets: {metrics['active_tickets']}")
        print(f"Backlog tickets: {metrics['backlog_tickets']}")
        print(f"Archived tickets: {metrics['archived_tickets']}")

        if metrics["stage_cycle_times"]:
            print("\nStage cycle times (hours):")
            for stage, stats in metrics["stage_cycle_times"].items():
                if stats["count"] > 0:
                    print(f"  {stage}: avg={stats['avg_hours']}, min={stats['min_hours']}, max={stats['max_hours']} (n={stats['count']})")

        if metrics["bottlenecks"]:
            print("\nBottlenecks:")
            for b in metrics["bottlenecks"]:
                print(f"  - {b['type']}: {b.get('stage') or b.get('skill')} (count={b['count']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
