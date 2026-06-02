#!/usr/bin/env python3
"""One kanban-lead tick: scan + spawn obligations — CLI entry point.

Usage:
  python run_kanban_lead_tick.py --workspace <path>
  python run_kanban_lead_tick.py --workspace <path> --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from kanban_lead import KanbanLead  # noqa: E402
from skill_fixture import is_fixture_mode  # noqa: E402


def run_tick(workspace: Path) -> dict:
    lead = KanbanLead(workspace)
    report = lead.run_scan_with_mode()
    spawns = report.get("spawns", [])
    roles = report.get("roles", {})

    # Dispatch summary — idle agents that got work reserved by the scan
    dispatch_summary = {}
    for role, data in roles.items():
        dn = data.get("dispatch_needed", 0)
        if dn > 0:
            dispatch_summary[role] = dn

    report["must_spawn"] = len(spawns) > 0
    report["dispatch_summary"] = dispatch_summary
    report["spawn_prompts"] = [
        _spawn_prompt(workspace, s["role"], s["instance"], s.get("spawn_epoch")) for s in spawns
    ]
    report["orchestrator_rule"] = (
        "Dispatch already handled by scan (reserved skills for idle agents). "
        "If must_spawn is true, spawn every entry in spawn_prompts NOW "
        "(Task/subagent, run_in_background). Spawns are ONLY for dead/missing "
        "agent slots — live idle agents already got work dispatched."
    )
    return report


def _spawn_prompt(
    workspace: Path, role: str, instance: int, spawn_epoch: int | None = None,
) -> dict:
    inst_line = f"  instance: {instance}\n" if instance > 1 else ""
    fixture = is_fixture_mode(workspace)
    seed_path = workspace / "AGENT-SEED.md"
    first_read = (
        f"Read {seed_path} FIRST (fixture mode — team member executor).\n\n"
        if fixture and seed_path.is_file()
        else "Read practices/kanban/agents/reference/session-bootstrap.md FIRST.\n\n"
    )
    fixture_block = ""
    if fixture:
        fixture_block = (
            "\nFIXTURE MODE (mandatory): You are a team member executor — NOT kanban-lead. "
            "Do NOT read practice skill SKILL.md or run scanners.\n"
            "After board_skill.py pull (or resume manual assignment), run:\n"
            "  python practices/kanban/skills/abd-kanban/scripts/apply_skill_fixture.py apply "
            f"--workspace {workspace} --ticket <id> --skill <name> --role {role}\n"
            "Or if skill is already in_progress from manual drop:\n"
            "  python practices/kanban/skills/abd-kanban/scripts/apply_skill_fixture.py apply-claim "
            f"--workspace {workspace} --role {role}\n"
            "Then pull again. See agents/reference/skill-fixture-mode.md.\n"
        )
    epoch_line = ""
    if spawn_epoch is not None:
        epoch_line = (
            f"\nExecutor spawn_epoch: {spawn_epoch} "
            "(registered by kanban-lead — your heartbeats must carry this epoch).\n"
        )
    prompt = (
        f"{first_read}"
        f"Bootstrap:\n  workspace: {workspace}\n  delivery-role: {role}\n"
        f"{inst_line}{epoch_line}\n"
        f"Then read agents/{role}/AGENT.md, agents/reference/pull-model.md, "
        "agents/reference/work-queue.md, and reference/artifact-layout.md.\n"
        f"Arm AGENT_LOOP_TICK_{role} on turn 1. Pull via board_skill.py "
        "(never hand-edit board.json)."
        f"{fixture_block}"
        "\nNever exit after one skill."
    )
    if not fixture:
        prompt += " Execute and review per executor-workflow.md."
    return {"role": role, "instance": instance, "prompt": prompt}


def main() -> int:
    parser = argparse.ArgumentParser(description="Kanban lead tick — scan + spawn obligations")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = run_tick(args.workspace.resolve())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if report.get("dispatch_summary"):
            print(f"Cycle {report['cycle']}: DISPATCHED to idle agents: {report['dispatch_summary']}")
        if report["must_spawn"]:
            print(f"  MUST SPAWN {len(report['spawns'])} dead slot(s):")
            for s in report["spawns"]:
                print(f"    -> {s['role']} instance {s['instance']} ({s['reason']})")
        else:
            print(f"Cycle {report['cycle']}: All agent slots filled. No spawns needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
