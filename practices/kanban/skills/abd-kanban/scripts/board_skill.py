#!/usr/bin/env python3
"""Board skill CLI — thin entry point for Agent class.

Usage:
  python board_skill.py pull --workspace <path> --role product-owner [--instance 2]
  python board_skill.py claim --workspace <path> --ticket <id> --skill <name> --role <role>
  python board_skill.py complete --workspace <path> --ticket <id> --skill <name> --role <role> [--notes "..."]
  python board_skill.py skip --workspace <path> --ticket <id> --skill <name> --role <role> [--notes "..."]
  python board_skill.py ready --workspace <path> --role <role> [--instance 2] [--reason "..."]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from agent import Agent, SkillAlreadyDoneError, SkillAlreadyInProgressError, TicketNotFoundError  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Board skill claim/complete CLI")
    parser.add_argument("--workspace", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)

    p_pull = sub.add_parser("pull", help="Find and claim next eligible skill")
    p_pull.add_argument("--role", required=True)
    p_pull.add_argument("--instance", type=int, default=1)
    p_pull.add_argument("--dry-run", action="store_true")
    p_pull.add_argument("--reserve", action="store_true")

    for name in ("claim", "complete", "skip"):
        p = sub.add_parser(name)
        p.add_argument("--ticket", required=True)
        p.add_argument("--skill", required=True)
        p.add_argument("--role", required=True)
        p.add_argument("--instance", type=int, default=1)
        p.add_argument("--notes", default="")
        if name == "claim":
            p.add_argument("--reserve", action="store_true")

    p_ready = sub.add_parser("ready")
    p_ready.add_argument("--role", required=True)
    p_ready.add_argument("--instance", type=int, default=1)
    p_ready.add_argument("--reason", default="no_eligible_skill_on_active_tickets")

    args = parser.parse_args()
    workspace = args.workspace.resolve()

    try:
        if args.command == "pull":
            ag = Agent(workspace, args.role, args.instance)
            result = ag.pull_skill(reserve=args.reserve)
            print(json.dumps(result))
            return 0

        if args.command == "claim":
            ag = Agent(workspace, args.role, args.instance)
            result = ag.claim_skill(args.ticket, args.skill, reserve=args.reserve)
            print(json.dumps(result))
            return 0

        if args.command == "complete":
            ag = Agent(workspace, args.role, args.instance)
            result = ag.complete_skill(args.ticket, args.skill, args.notes or None)
            print(json.dumps(result))
            return 0

        if args.command == "skip":
            ag = Agent(workspace, args.role, args.instance)
            notes = args.notes or "skipped per conditional gate"
            result = ag.complete_skill(args.ticket, args.skill, notes)
            print(json.dumps(result))
            return 0

        if args.command == "ready":
            ag = Agent(workspace, args.role, args.instance)
            result = ag.signal_ready(args.reason)
            print(json.dumps(result))
            return 0

    except (TicketNotFoundError, SkillAlreadyInProgressError, SkillAlreadyDoneError) as e:
        print(str(e), file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
