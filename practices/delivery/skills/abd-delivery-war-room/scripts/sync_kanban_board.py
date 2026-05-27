#!/usr/bin/env python3
"""Sync delivery-war-room/board.json from on-disk delivery state.

**Read-only for planning.** This script does NOT create or modify:
  - agile-delivery-plan.md
  - run-catalog.json, system-of-work.json, run-state.json
  - slot-NN-start.md, manifest.md, or checklist content

Planning and slot materialization are owned by **delivery-lead** + **abd-delivery-planning**
+ **abd-delivery-war-room** (see `generate_run_slots.py` when a run opens).

**Inputs (read):** slot files, run-log.jsonl, run-catalog.json, run-state.json,
delivery-plan-checklist.md, existing board.json (preserve wip_policy / active_agents).

**Output (write):** board.json only.

Kanban model: delivery/content/kanban.md
Rule: delivery/skills/abd-delivery-war-room/rules/kanban-ticket-columns.md

Usage (from agilebydesign-skills repo root or with absolute paths):

    python delivery/skills/abd-delivery-war-room/scripts/sync_kanban_board.py --workspace C:\\dev\\my-engagement
    python delivery/skills/abd-delivery-war-room/scripts/sync_kanban_board.py --workspace C:\\dev\\my-engagement --dry-run

Exit: 0 on success, 1 if war room directory is missing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import (  # noqa: E402
    load_run_catalog,
    parent_discovery_from_catalog,
    resolve_runs,
)
from slot_paths import iter_slot_files  # noqa: E402

STAGE_ORDER = ["shaping", "discovery", "exploration", "specification", "engineering"]
SLOT_START_RE = re.compile(r"^slot-(\d+)-start\.md$")
SLOT_FINISHED_RE = re.compile(r"^slot-(\d+)(?:-[\w-]+)?-finished\.md$")
SLOT_CLAIM_RE = re.compile(r"^slot-(\d+)-claim\.md$")
SLOT_BLOCKED_RE = re.compile(r"^slot-(\d+)-blocked\.md$")
YAML_RUN_RE = re.compile(r'^run:\s*["\']?Run\s*(\d+)', re.M)
YAML_STAGE_RE = re.compile(r"^stage:\s*(\w+)", re.M)
YAML_ROLE_RE = re.compile(r"^team-role:\s*([\w-]+)", re.M)
YAML_SLOT_TYPE_RE = re.compile(r"^slot_type:\s*(\w+)", re.M)
DEPENDS_RE = re.compile(r'^\s*-\s*"(\d+)"', re.M)
PARENT_DISCOVERY_DONE_RE = re.compile(
    r"- \[x\] \*\*discovery\*\* — done \(completed by parent discovery run\)"
)


@dataclass
class SlotMeta:
    slot_id: int
    run: int | None = None
    stage: str | None = None
    team_role: str | None = None
    slot_type: str | None = None
    depends_on: list[int] = field(default_factory=list)


@dataclass
class RunMeta:
    run: int
    title: str
    first_slot: int | None = None
    last_slot: int | None = None


def _parse_slot_start(path: Path) -> SlotMeta | None:
    m = SLOT_START_RE.match(path.name)
    if not m:
        return None
    slot_id = int(m.group(1))
    text = path.read_text(encoding="utf-8")
    run_m = YAML_RUN_RE.search(text)
    run_num = int(run_m.group(1)) if run_m else None
    stage_m = YAML_STAGE_RE.search(text)
    role_m = YAML_ROLE_RE.search(text)
    type_m = YAML_SLOT_TYPE_RE.search(text)
    in_dep = False
    deps: list[int] = []
    for line in text.splitlines():
        if line.strip().startswith("depends_on:"):
            in_dep = True
            continue
        if in_dep:
            if line.strip().startswith("- "):
                dm = re.match(r'^\s*-\s*"(\d+)"', line)
                if dm:
                    deps.append(int(dm.group(1)))
            elif not line.startswith(" ") and line.strip() and not line.strip().startswith("#"):
                in_dep = False
    return SlotMeta(
        slot_id=slot_id,
        run=run_num,
        stage=stage_m.group(1) if stage_m else None,
        team_role=role_m.group(1) if role_m else None,
        slot_type=type_m.group(1) if type_m else None,
        depends_on=deps,
    )


def _parse_parent_discovery_done_runs(checklist_path: Path) -> set[int]:
    """Runs whose discovery stage was completed by a parent discovery run (increments)."""
    if not checklist_path.is_file():
        return set()
    text = checklist_path.read_text(encoding="utf-8")
    done: set[int] = set()
    sections = re.split(r"(?=^### Run \d+)", text, flags=re.M)
    for section in sections:
        m = re.match(r"^### Run (\d+)", section)
        if not m:
            continue
        if PARENT_DISCOVERY_DONE_RE.search(section):
            done.add(int(m.group(1)))
    return done


def _slot_run_map(
    slots: dict[int, SlotMeta],
    runs: dict[int, RunMeta],
) -> dict[int, int]:
    mapping: dict[int, int] = {}
    for sid, meta in slots.items():
        if meta.run is not None:
            mapping[sid] = meta.run
    for run in runs.values():
        if not run.slots_generated or run.first_slot is None or run.last_slot is None:
            continue
        for sid in range(run.first_slot, run.last_slot + 1):
            mapping.setdefault(sid, run.run)
    return mapping


def _parse_run_log(path: Path) -> tuple[set[int], dict[tuple[int, str], bool]]:
    completed_runs: set[int] = set()
    stage_gates: dict[tuple[int, str], bool] = {}
    if not path.is_file():
        return completed_runs, stage_gates
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = ev.get("event")
        if kind == "run_complete":
            r = ev.get("run")
            if r is not None:
                completed_runs.add(int(r))
        elif kind == "stage_exit_gate":
            stage = str(ev.get("stage", "")).lower()
            r = ev.get("run")
            if r is not None and stage:
                stage_gates[(int(r), stage)] = True
    return completed_runs, stage_gates


def _deps_met(slot: SlotMeta, finished: set[int]) -> bool:
    return all(d in finished for d in slot.depends_on)


def _stage_slots(slots: dict[int, SlotMeta], run_id: int, stage: str, slot_run: dict[int, int]) -> list[int]:
    out = [
        sid
        for sid, meta in slots.items()
        if slot_run.get(sid) == run_id and meta.stage == stage
    ]
    return sorted(out)


def _stage_complete(
    run_id: int,
    stage: str,
    slots: dict[int, SlotMeta],
    finished: set[int],
    slot_run: dict[int, int],
    stage_gates: dict[tuple[int, str], bool],
) -> bool:
    if stage_gates.get((run_id, stage)):
        return True
    stage_ids = _stage_slots(slots, run_id, stage, slot_run)
    if not stage_ids:
        return False
    return all(sid in finished for sid in stage_ids)


def _next_stage(stage: str) -> str | None:
    if stage not in STAGE_ORDER:
        return None
    idx = STAGE_ORDER.index(stage)
    if idx + 1 >= len(STAGE_ORDER):
        return None
    return STAGE_ORDER[idx + 1]


def _first_claimable_slot(
    slots: dict[int, SlotMeta],
    finished: set[int],
    slot_run: dict[int, int],
    run_id: int,
    stage: str,
    slot_type: str | None = None,
) -> int | None:
    for sid in sorted(slots):
        meta = slots[sid]
        if slot_run.get(sid) != run_id or meta.stage != stage:
            continue
        if slot_type and meta.slot_type != slot_type:
            continue
        if sid in finished:
            continue
        if not _deps_met(meta, finished):
            continue
        claim_path = None  # caller checks claims separately
        return sid
    return None


def _parse_claim_time(text: str) -> datetime | None:
    for line in text.splitlines():
        if line.startswith("claimed_at:"):
            raw = line.split(":", 1)[1].strip()
            try:
                return datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError:
                return None
    return None


def _infer_ticket_column(
    run_id: int,
    run: RunMeta,
    slots: dict[int, SlotMeta],
    finished: set[int],
    claims: dict[int, Path],
    blocked: set[int],
    slot_run: dict[int, int],
    stage_gates: dict[tuple[int, str], bool],
    stall_minutes: int,
    now: datetime,
    parent_discovery_done: set[int] | None = None,
) -> dict:
    run_slots = [s for s, r in slot_run.items() if r == run_id]
    started = any(s in finished or s in claims for s in run_slots)

    # Increment runs: discovery done by parent — stay at discovery/done until exploration
    # actually starts (claim or finish on an exploration slot for this run).
    if parent_discovery_done and run_id in parent_discovery_done:
        exploration_ids = [
            sid
            for sid, meta in slots.items()
            if meta.run == run_id and meta.stage == "exploration"
        ]
        exploration_active = any(s in finished or s in claims for s in exploration_ids)
        if not exploration_ids or not exploration_active:
            return {
                "run": run_id,
                "title": run.title,
                "stage": "discovery",
                "column": "done",
                "active_slot": None,
                "active_role": None,
                "note": "discovery_precompleted_by_parent",
            }

    if blocked & set(run_slots):
        bs = min(blocked & set(run_slots))
        meta = slots.get(bs)
        return {
            "run": run_id,
            "title": run.title,
            "stage": meta.stage if meta else None,
            "column": "blocked",
            "active_slot": str(bs),
            "blocked_slot": str(bs),
        }

    for sid, claim_path in sorted(claims.items()):
        if slot_run.get(sid) != run_id:
            continue
        meta = slots.get(sid)
        if not meta:
            continue
        claimed_at = _parse_claim_time(claim_path.read_text(encoding="utf-8"))
        if claimed_at and stall_minutes > 0:
            age = (now - claimed_at).total_seconds() / 60.0
            if age > stall_minutes:
                return {
                    "run": run_id,
                    "title": run.title,
                    "stage": meta.stage,
                    "column": "stalled",
                    "active_slot": str(sid),
                    "active_role": meta.team_role,
                    "slot_type": meta.slot_type,
                    "stall_since": claimed_at.isoformat(),
                }
        col = "review" if meta.slot_type == "reviewer" else "in_progress"
        return {
            "run": run_id,
            "title": run.title,
            "stage": meta.stage,
            "column": col,
            "active_slot": str(sid),
            "active_role": meta.team_role,
            "slot_type": meta.slot_type,
        }

    if not started:
        first = run.first_slot
        if first is None:
            return {"run": run_id, "title": run.title, "column": "backlog", "stage": None, "active_slot": None}
        meta = slots.get(first)
        if meta and _deps_met(meta, finished):
            return {
                "run": run_id,
                "title": run.title,
                "stage": meta.stage,
                "column": "backlog",
                "active_slot": str(first),
                "note": "pull_from_backlog_when_first_slot_claimable",
            }
        return {"run": run_id, "title": run.title, "column": "backlog", "stage": None, "active_slot": None}

    active_stage: str | None = None
    for stage in STAGE_ORDER:
        ids = _stage_slots(slots, run_id, stage, slot_run)
        if not ids:
            continue
        if not _stage_complete(run_id, stage, slots, finished, slot_run, stage_gates):
            active_stage = stage
            break

    if active_stage is None:
        if not started:
            return {"run": run_id, "title": run.title, "column": "backlog", "stage": None, "active_slot": None}
        # All authored stages are complete but next-stage slots not written yet.
        # Stay on the board at column: done — never regress to backlog.
        last_completed_stage: str | None = None
        for stage in STAGE_ORDER:
            ids = _stage_slots(slots, run_id, stage, slot_run)
            if ids and all(sid in finished for sid in ids):
                last_completed_stage = stage
        return {
            "run": run_id,
            "title": run.title,
            "stage": last_completed_stage,
            "column": "done",
            "active_slot": None,
            "note": "awaiting_next_stage_slots",
        }

    if _stage_complete(run_id, active_stage, slots, finished, slot_run, stage_gates):
        nxt = _next_stage(active_stage)
        if nxt and _stage_slots(slots, run_id, nxt, slot_run):
            if not _stage_complete(run_id, nxt, slots, finished, slot_run, stage_gates):
                first_nxt = _first_claimable_slot(slots, finished, slot_run, run_id, nxt)
                if first_nxt is None:
                    return {
                        "run": run_id,
                        "title": run.title,
                        "stage": active_stage,
                        "column": "done",
                        "active_slot": None,
                        "waiting_for_stage": nxt,
                    }
        return {
            "run": run_id,
            "title": run.title,
            "stage": active_stage,
            "column": "done",
            "active_slot": None,
        }

    ex = _first_claimable_slot(slots, finished, slot_run, run_id, active_stage, "executor")
    if ex is not None:
        em = slots[ex]
        return {
            "run": run_id,
            "title": run.title,
            "stage": active_stage,
            "column": "in_progress",
            "active_slot": str(ex),
            "active_role": em.team_role,
            "slot_type": "executor",
        }
    rev = _first_claimable_slot(slots, finished, slot_run, run_id, active_stage, "reviewer")
    if rev is not None:
        rm = slots[rev]
        return {
            "run": run_id,
            "title": run.title,
            "stage": active_stage,
            "column": "review",
            "active_slot": str(rev),
            "active_role": rm.team_role,
            "slot_type": "reviewer",
        }

    return {
        "run": run_id,
        "title": run.title,
        "stage": active_stage,
        "column": "done",
        "active_slot": None,
    }


def sync_board(workspace: Path, dry_run: bool = False) -> dict:
    war_room = workspace / "docs" / "planning" / "delivery-war-room"
    if not war_room.is_dir():
        raise FileNotFoundError(f"War room missing: {war_room}")

    runs = resolve_runs(workspace)
    slots: dict[int, SlotMeta] = {}
    for path in iter_slot_files(war_room, "slot-*-start.md"):
        meta = _parse_slot_start(path)
        if meta:
            slots[meta.slot_id] = meta

    finished: set[int] = set()
    for path in iter_slot_files(war_room, "slot-*-finished.md"):
        m = SLOT_FINISHED_RE.match(path.name)
        if m:
            finished.add(int(m.group(1)))

    claims: dict[int, Path] = {}
    for path in iter_slot_files(war_room, "slot-*-claim.md"):
        m = SLOT_CLAIM_RE.match(path.name)
        if m:
            claims[int(m.group(1))] = path

    blocked: set[int] = set()
    for path in iter_slot_files(war_room, "slot-*-blocked.md"):
        m = SLOT_BLOCKED_RE.match(path.name)
        if m:
            blocked.add(int(m.group(1)))

    slot_run = _slot_run_map(slots, runs)
    completed_runs, stage_gates = _parse_run_log(war_room / "run-log.jsonl")

    checklist_path = war_room / "delivery-plan-checklist.md"
    parent_discovery_done = _parse_parent_discovery_done_runs(checklist_path)
    parent_discovery_done |= parent_discovery_from_catalog(load_run_catalog(workspace))

    # Read existing board as baseline — preserve column: done tickets that have
    # no new activity (claims, blocks) so the script never regresses a ticket
    # that was manually or externally advanced.
    existing_board: dict = {}
    board_path = war_room / "board.json"
    if board_path.is_file():
        try:
            existing_board = json.loads(board_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    existing_tickets: dict[str, dict] = existing_board.get("tickets", {})

    stall_minutes = 20
    manifest = war_room / "manifest.md"
    if manifest.is_file():
        mm = re.search(r"stall_timeout_minutes:\s*(\d+)", manifest.read_text(encoding="utf-8"))
        if mm:
            stall_minutes = int(mm.group(1))

    now = datetime.now(timezone.utc)
    tickets: dict[str, dict] = {}
    backlog: list[dict] = []

    for run in sorted(runs.values(), key=lambda r: r.run):
        if run.run in completed_runs:
            continue
        ticket = _infer_ticket_column(
            run.run, run, slots, finished, claims, blocked, slot_run, stage_gates, stall_minutes, now,
            parent_discovery_done=parent_discovery_done,
        )
        # If the inferred result is backlog but the existing board already has this
        # run as a ticket at column: done (and no active claims or blocks), preserve it.
        # This prevents the script from regressing discovery-done or stage-done tickets
        # that have no slot-start files authored for the next stage yet.
        if ticket.get("column") == "backlog":
            run_key = str(run.run)
            existing = existing_tickets.get(run_key)
            run_slots = set(s for s, r in slot_run.items() if r == run.run)
            has_active_claim = bool(run_slots & set(claims.keys()))
            has_block = bool(run_slots & blocked)
            if existing and existing.get("column") == "done" and not has_active_claim and not has_block:
                tickets[run_key] = existing
                continue
            backlog.append(
                {
                    "run": run.run,
                    "title": run.title,
                    "priority": run.run,
                    "first_slot": str(run.first_slot) if run.first_slot else None,
                    "pull_when": ticket.get("note") or "plan_entry_or_cross_run_dep",
                }
            )
        else:
            tickets[str(run.run)] = ticket

    board = {
        "schema": "abd-delivery-war-room-kanban/v1",
        "synced_at": now.isoformat(),
        "columns": ["backlog", "in_progress", "review", "done", "blocked", "stalled"],
        "stage_flow": ["in_progress", "review", "done"],
        "backlog": sorted(backlog, key=lambda x: x["priority"]),
        "tickets": tickets,
        "completed_runs": [
            {"run": r, "title": runs[r].title if r in runs else f"Run {r}"}
            for r in sorted(completed_runs)
        ],
        "notes": (
            "Generated by sync_kanban_board.py — board snapshot only. "
            "Planning artifacts are written by delivery-lead + abd-delivery-planning + "
            "abd-delivery-war-room (generate_run_slots.py at run open)."
        ),
    }
    # Preserve delivery-lead-managed fields not derived from slot files.
    for key in ("active_agents", "wip_policy", "watching_runs"):
        if key in existing_board:
            board[key] = existing_board[key]

    out_path = war_room / "board.json"
    if not dry_run:
        out_path.write_text(json.dumps(board, indent=2) + "\n", encoding="utf-8")
    return board


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync war-room Kanban board.json")
    parser.add_argument("--workspace", required=True, type=Path, help="Engagement workspace root")
    parser.add_argument("--dry-run", action="store_true", help="Print board JSON, do not write")
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
        print(f"Wrote {workspace / 'docs/planning/delivery-war-room/board.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
