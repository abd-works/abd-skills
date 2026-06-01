#!/usr/bin/env python3
"""Diagnose pull eligibility per role — shows why work is or is not claimable.

Usage:
  python pull_diagnostics.py --workspace <path>
  python pull_diagnostics.py --workspace <path> --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import (  # noqa: E402
    KanbanBoard,
    SkillDef,
    StageDef,
    Ticket,
    count_in_progress_for_role,
    count_live_agents,
    count_working_agents,
    load_board,
    load_kanban_board,
    load_team,
    war_room_dir,
)

ROLES = ("business-expert", "product-owner", "ux-designer", "engineer")


def _explain_ticket_role(ticket: Ticket, kb: KanbanBoard, role: str) -> dict:
    stage_def = next((s for s in kb.stages if s.name == ticket.stage), None)
    if stage_def is None:
        return {"ticket_id": ticket.ticket_id, "stage": ticket.stage, "next_for_role": None, "blockers": ["unknown_stage"]}

    blockers: list[str] = []
    next_skill: str | None = None
    for skill_def in stage_def.stage_work_required:
        if skill_def.role != role:
            continue
        sp = ticket.skill_progress.get(skill_def.skill)
        if not stage_def.priors_done(ticket, skill_def.skill):
            blockers.append(f"priors_incomplete_before:{skill_def.skill}")
            break
        if sp is not None and sp.is_done():
            continue
        if sp is None or sp.is_claimable():
            next_skill = skill_def.skill
            break
        blockers.append(f"in_progress:{skill_def.skill}")
        break

    return {
        "ticket_id": ticket.ticket_id,
        "stage": ticket.stage,
        "priority": ticket.priority,
        "scope_level": ticket.scope_level,
        "any_in_progress": ticket.has_skill_in_progress(),
        "next_for_role": next_skill,
        "blockers": blockers,
    }


def diagnose(workspace: Path) -> dict:
    wr = war_room_dir(workspace)
    board = load_board(workspace)
    config_name = board.get("stage_configuration") or board.get("system_of_work", "")
    kb_map = load_kanban_board(workspace)
    kb = kb_map.get(config_name)
    if kb is None:
        raise SystemExit(f"Unknown stage_configuration: {config_name}")

    raw_kb = json.loads((wr / "kanban.json").read_text(encoding="utf-8"))
    team = load_team(board, raw_kb.get("definitions", {}).get(config_name, {}))
    active = [Ticket.from_dict(t) for t in board.get("active", [])]
    backlog = board.get("backlog", [])

    report: dict = {
        "active_tickets": len(active),
        "backlog_tickets": len(backlog),
        "roles": {},
    }

    for role in ROLES:
        if role not in team:
            continue
        eligible = kb.list_eligible_pulls(active, role)
        in_prog = count_in_progress_for_role(active, role)
        working = count_working_agents(wr, role)
        live = count_live_agents(wr, role)
        ticket_detail = [_explain_ticket_role(t, kb, role) for t in active]

        dead_slots = max(0, team[role] - live)
        idle_live = max(0, live - working)

        report["roles"][role] = {
            "team": team[role],
            "live_agents": live,
            "working_agents": working,
            "in_progress": in_prog,
            "eligible_pulls": eligible,
            "dead_slots_need_spawn": dead_slots,
            "idle_agents_need_dispatch": idle_live,
            "active_tickets": ticket_detail,
        }

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Pull eligibility diagnostics")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = diagnose(args.workspace.resolve())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for role, data in report["roles"].items():
            print(f"\n=== {role} (team={data['team']} live={data['live_agents']} working={data['working_agents']}) ===")
            print(f"  eligible: {data['eligible_pulls']}")
            print(f"  dead slots (NEED SPAWN): {data['dead_slots_need_spawn']}")
            print(f"  idle live (dispatched by scan): {data['idle_agents_need_dispatch']}")
            for t in data["active_tickets"]:
                if t["next_for_role"] or t["blockers"]:
                    print(f"  {t['ticket_id']}: next={t['next_for_role']} blockers={t['blockers']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
