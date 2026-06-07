#!/usr/bin/env python3
"""Unified Kanban CLI — all board operations in one entry point.

Lead (KanbanLead):
  kanban_cli.py lead tick      --workspace <path>
  kanban_cli.py lead scan      --workspace <path>
  kanban_cli.py lead sync      --workspace <path> [--dry-run]
  kanban_cli.py lead wake      --workspace <path> [--apply-tick]
  kanban_cli.py lead diagnose  --workspace <path>
  kanban_cli.py lead metrics   --workspace <path>
  kanban_cli.py lead repair    --workspace <path> --parent <ticket-id>

Member (TeamMemberAgent):
  kanban_cli.py member pull     --workspace <path> --role <role> [--instance N] [--reserve]
  kanban_cli.py member claim    --workspace <path> --role <role> --ticket <id> --skill <name> [--reserve]
  kanban_cli.py member intent   --workspace <path> --role <role> [--instance N]
  kanban_cli.py member complete --workspace <path> --role <role> --ticket <id> --skill <name> [--notes "..."]
  kanban_cli.py member review   --workspace <path> --role <role> --ticket <id> --skill <name> [--notes "..."]
  kanban_cli.py member skip     --workspace <path> --role <role> --ticket <id> --skill <name> [--notes "..."]
  kanban_cli.py member ready    --workspace <path> --role <role> [--instance N] [--reason "..."]
  kanban_cli.py member fixture  --workspace <path> --role <role> [--ticket <id> --skill <name>]

Registry (architecture artifact, not Kanban domain):
  kanban_cli.py registry load     --workspace <path>
  kanban_cli.py registry register --workspace <path> --ticket <id> --skill <name> --mechanisms A B ...
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_APP_ROOT = _SCRIPTS_DIR.parents[2] / "apps" / "abd-delivery-agent-kanban"
for _p in (_SCRIPTS_DIR, _APP_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from domain.kanban_lead import KanbanLead  # noqa: E402
from domain.agent import (  # noqa: E402
    SkillAlreadyDoneError,
    SkillAlreadyInProgressError,
    TeamMemberAgent,
    TicketNotFoundError,
)
from domain.delivery_model import war_room_dir  # noqa: E402
from mechanism_registry import load_registry, register_mechanisms  # noqa: E402


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="kanban_cli.py",
        description="Unified Kanban board CLI",
    )
    root.add_argument("--json", action="store_true", help="Output raw JSON")
    groups = root.add_subparsers(dest="group", required=True)

    _add_lead_commands(groups)
    _add_member_commands(groups)
    _add_registry_commands(groups)

    return root


def _ws(p: argparse.ArgumentParser) -> None:
    p.add_argument("--workspace", required=True, type=Path)


def _add_lead_commands(groups: argparse._SubParsersAction) -> None:  # type: ignore[type-arg]
    lead = groups.add_parser("lead", help="KanbanLead operations")
    sub = lead.add_subparsers(dest="cmd", required=True)

    _ws(sub.add_parser("tick",     help="Scan + build spawn prompts"))
    _ws(sub.add_parser("scan",     help="Run one scan cycle"))
    p_sync = sub.add_parser("sync", help="Sync board.json")
    _ws(p_sync); p_sync.add_argument("--dry-run", action="store_true")
    p_wake = sub.add_parser("wake", help="Check if lead must wake")
    _ws(p_wake); p_wake.add_argument("--apply-tick", action="store_true")
    _ws(sub.add_parser("diagnose", help="Pull eligibility per role"))
    _ws(sub.add_parser("metrics",  help="Compute delivery metrics"))
    p_repair = sub.add_parser("repair", help="Repair partial scatter")
    _ws(p_repair); p_repair.add_argument("--parent", required=True, metavar="TICKET_ID")


def _add_member_commands(groups: argparse._SubParsersAction) -> None:  # type: ignore[type-arg]
    member = groups.add_parser("member", help="TeamMemberAgent operations")
    sub = member.add_subparsers(dest="cmd", required=True)

    def _role(p: argparse.ArgumentParser) -> None:
        _ws(p)
        p.add_argument("--role", required=True)
        p.add_argument("--instance", type=int, default=1)

    def _ticket_skill(p: argparse.ArgumentParser) -> None:
        p.add_argument("--ticket", required=True)
        p.add_argument("--skill",  required=True)

    p_pull = sub.add_parser("pull", help="Pull next eligible skill (downstream-first)")
    _role(p_pull); p_pull.add_argument("--reserve", action="store_true")

    p_claim = sub.add_parser("claim", help="Work on ticket with skill (executor)")
    _role(p_claim); _ticket_skill(p_claim); p_claim.add_argument("--reserve", action="store_true")

    p_intent = sub.add_parser("intent", help="Claim oldest operator drop (manual mode)")
    _role(p_intent)

    for name, help_text in (
        ("complete", "Mark execution work done (opens review)"),
        ("review",   "Review ticket work from skill (reviewer approves)"),
        ("skip",     "Skip skill via conditional gate"),
    ):
        p = sub.add_parser(name, help=help_text)
        _role(p); _ticket_skill(p)
        p.add_argument("--notes", default=("skipped per conditional gate" if name == "skip" else ""))

    p_ready = sub.add_parser("ready", help="Signal ready — write heartbeat")
    _role(p_ready)
    p_ready.add_argument("--reason", default="no_eligible_skill_on_active_tickets")

    p_fixture = sub.add_parser("fixture", help="Apply skill fixture (fixture_mode workspaces)")
    _role(p_fixture)
    p_fixture.add_argument("--ticket", default="")
    p_fixture.add_argument("--skill",  default="")


def _add_registry_commands(groups: argparse._SubParsersAction) -> None:  # type: ignore[type-arg]
    registry = groups.add_parser("registry", help="Mechanism registry (architecture artifact)")
    sub = registry.add_subparsers(dest="cmd", required=True)

    _ws(sub.add_parser("load", help="Print all registered mechanisms"))

    p_reg = sub.add_parser("register", help="Register mechanisms from a skill run")
    _ws(p_reg)
    p_reg.add_argument("--ticket",     required=True)
    p_reg.add_argument("--skill",      required=True)
    p_reg.add_argument("--mechanisms", nargs="+", required=True)
    p_reg.add_argument("--reference-path", default="")


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def _run_lead(args: argparse.Namespace) -> object:
    lead = KanbanLead(args.workspace.resolve())
    if args.cmd == "tick":
        return lead.run_tick()
    if args.cmd == "scan":
        return lead.run_scan_with_mode()
    if args.cmd == "sync":
        return lead.sync_board(dry_run=args.dry_run)
    if args.cmd == "wake":
        return lead.check_wake(apply_tick=args.apply_tick)
    if args.cmd == "diagnose":
        return lead.pull_diagnostics()
    if args.cmd == "metrics":
        return lead.compute_metrics()
    if args.cmd == "repair":
        added = lead.repair_partial_scatter(args.parent)
        return {"added": added, "count": len(added)}
    return None


def _run_member(args: argparse.Namespace) -> object:
    workspace = args.workspace.resolve()
    agent = TeamMemberAgent(workspace, args.role, instance=args.instance)

    if args.cmd == "pull":
        return agent.pull_skill(reserve=args.reserve)
    if args.cmd == "claim":
        return agent.work_on_ticket(args.ticket, args.skill, reserve=args.reserve)
    if args.cmd == "intent":
        return agent.claim_next_intent()
    if args.cmd == "complete":
        return agent.complete_skill(args.ticket, args.skill, args.notes or None)
    if args.cmd == "review":
        return agent.review_ticket_work(args.ticket, args.skill, args.notes or None)
    if args.cmd == "skip":
        return agent.complete_skill(args.ticket, args.skill, args.notes)
    if args.cmd == "ready":
        return agent.signal_ready(args.reason)
    if args.cmd == "fixture":
        if args.ticket and args.skill:
            return agent.apply_skill_fixture(args.ticket, args.skill)
        claim = agent.find_in_progress_claim()
        if claim is None:
            return {"action": "none", "reason": "no_in_progress_claim"}
        return agent.apply_skill_fixture(*claim)
    return None


def _run_registry(args: argparse.Namespace) -> object:
    workspace = args.workspace.resolve()
    if args.cmd == "load":
        return load_registry(workspace)
    if args.cmd == "register":
        register_mechanisms(workspace, args.ticket, args.skill, args.mechanisms, args.reference_path)
        return {"registered": args.mechanisms}
    return None


def main() -> int:
    args = _build_parser().parse_args()

    try:
        if args.group == "lead":
            result = _run_lead(args)
        elif args.group == "member":
            result = _run_member(args)
        elif args.group == "registry":
            result = _run_registry(args)
        else:
            return 1
    except (TicketNotFoundError, SkillAlreadyInProgressError, SkillAlreadyDoneError) as e:
        print(str(e), file=sys.stderr)
        return 1

    if result is not None:
        print(json.dumps(result, indent=2 if args.json else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
