#!/usr/bin/env python3
"""Apply skill fixture harness — team member executors use this in fixture_mode workspaces.

Usage:
  python apply_skill_fixture.py apply --workspace <path> --ticket <id> --skill <name> --role <role>
  python apply_skill_fixture.py apply-claim --workspace <path> --role <role> [--instance N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from skill_fixture import (  # noqa: E402
    apply_skill_fixture,
    find_in_progress_claim,
    is_fixture_mode,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy skill fixtures and mark skill done (fixture_mode workspaces only)",
    )
    parser.add_argument("--workspace", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)

    p_apply = sub.add_parser("apply", help="Apply fixture for a specific ticket/skill")
    p_apply.add_argument("--ticket", required=True)
    p_apply.add_argument("--skill", required=True)
    p_apply.add_argument("--role", required=True)
    p_apply.add_argument("--instance", type=int, default=1)

    p_claim = sub.add_parser(
        "apply-claim",
        help="Apply fixture for this role's current in_progress claim (manual delegate or pull)",
    )
    p_claim.add_argument("--role", required=True)
    p_claim.add_argument("--instance", type=int, default=1)

    args = parser.parse_args()
    workspace = args.workspace.resolve()

    if not is_fixture_mode(workspace):
        print("fixture_mode is not active (CONTEXT.md missing fixture_mode: true)", file=sys.stderr)
        return 1

    try:
        if args.command == "apply":
            result = apply_skill_fixture(
                workspace, args.ticket, args.skill, args.role, args.instance,
            )
        else:
            claim = find_in_progress_claim(workspace, args.role)
            if claim is None:
                print(json.dumps({"action": "none", "reason": "no_in_progress_claim"}))
                return 0
            ticket_id, skill = claim
            result = apply_skill_fixture(
                workspace, ticket_id, skill, args.role, args.instance,
            )
            result["action"] = "applied_claim"
    except (KeyError, FileNotFoundError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
