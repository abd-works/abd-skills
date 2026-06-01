#!/usr/bin/env python3
"""Detect when kanban-lead must wake (spawn obligations or stale lead).

Used by parent-chat watchdog loops — ticks on the lead subagent only work while
that session is listening. This script is read-only except it may run one tick
when --apply-tick is passed.

Usage:
  python check_lead_wake.py --workspace <engagement-root> [--json]
  python check_lead_wake.py --workspace <path> --json --apply-tick
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

from run_kanban_lead_tick import run_tick  # noqa: E402

LEAD_STALE_SECS = 90
EXECUTOR_STALE_SECS = 120


def _parse_ts(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _age_seconds(ts: datetime | None) -> float | None:
    if ts is None:
        return None
    return (datetime.now(timezone.utc) - ts).total_seconds()


def _read_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def check_wake(workspace: Path, *, apply_tick: bool) -> dict:
    wr = workspace / "docs" / "planning" / "kanban"
    board_path = wr / "board.json"
    action_path = wr / "action-state.json"
    lead_hb_path = wr / "heartbeat-kanban-lead.json"
    session_path = wr / "lead-cursor-session.json"

    reasons: list[str] = []
    intents = (_read_json(action_path) or {}) if action_path.is_file() else {}
    pending = intents.get("intents") or []
    if pending:
        reasons.append(f"action_intents:{len(pending)}")

    board = _read_json(board_path) or {}
    in_progress_roles: set[str] = set()
    for ticket in board.get("active") or []:
        for skill_id, prog in (ticket.get("skill_progress") or {}).items():
            if prog.get("execution_status") == "in_progress":
                role = prog.get("agent")
                if role:
                    in_progress_roles.add(role)
                    hb_path = wr / f"heartbeat-{role}.json"
                    hb_raw = _read_json(hb_path)
                    hb = hb_raw if isinstance(hb_raw, dict) else None
                    if hb is None:
                        reasons.append(f"no_heartbeat:{role}:{skill_id}")
                    else:
                        age = _age_seconds(_parse_ts(hb.get("ts")))
                        status = hb.get("status")
                        if age is None or age > EXECUTOR_STALE_SECS:
                            reasons.append(f"stale_executor:{role}")
                        elif status not in ("working", "reserved", "ready"):
                            reasons.append(f"executor_not_working:{role}:{status}")

    lead_hb = _read_json(lead_hb_path)
    lead_age = _age_seconds(_parse_ts(lead_hb.get("ts") if isinstance(lead_hb, dict) else None))
    lead_stale = lead_age is None or lead_age > LEAD_STALE_SECS

    tick_report: dict | None = None
    if apply_tick or pending or in_progress_roles:
        tick_report = run_tick(workspace)

    must_spawn = bool(tick_report and tick_report.get("must_spawn"))
    if must_spawn:
        for s in tick_report.get("spawns") or []:
            reasons.append(f"must_spawn:{s.get('role')}")

    wake_lead = bool(pending) or must_spawn or lead_stale or any(
        r.startswith("no_heartbeat:") or r.startswith("stale_executor:") for r in reasons
    )

    cursor_session = session_path.read_text(encoding="utf-8").strip() if session_path.is_file() else None
    if isinstance(_read_json(session_path), dict):
        cursor_session = (_read_json(session_path) or {}).get("cursor_agent_id")

    return {
        "wake_lead": wake_lead,
        "must_spawn": must_spawn,
        "lead_stale": lead_stale,
        "lead_age_seconds": lead_age,
        "reasons": reasons,
        "cursor_agent_id": cursor_session,
        "tick": tick_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check if kanban-lead must wake")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--apply-tick",
        action="store_true",
        help="Run one lead tick when checking (delegates + spawn obligations on disk)",
    )
    args = parser.parse_args()
    report = check_wake(args.workspace.resolve(), apply_tick=args.apply_tick)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("wake_lead" if report["wake_lead"] else "ok", report.get("reasons"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
