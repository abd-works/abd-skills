#!/usr/bin/env python3
"""Move flat slot-*.md files into runs/run-NN/<stage>/ layout.

Usage:
    python migrate_slot_layout.py --workspace C:\\dev\\abd-pet-store-demo
    python migrate_slot_layout.py --workspace C:\\dev\\abd-pet-store-demo --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from slot_paths import (  # noqa: E402
    RUNS_DIR,
    build_slot_location_index,
    parse_slot_start_meta,
    run_stage_dir,
    slot_id_from_name,
)


def _war_room(workspace: Path) -> Path:
    return workspace / "docs" / "planning" / "delivery-war-room"


def migrate(workspace: Path, *, dry_run: bool = False) -> int:
    war_room = _war_room(workspace)
    if not war_room.is_dir():
        raise FileNotFoundError(f"War room missing: {war_room}")

    state_path = war_room / "run-state.json"
    run_state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}
    index = build_slot_location_index(war_room, run_state=run_state)

    moves: list[tuple[Path, Path]] = []
    for path in sorted(war_room.glob("slot-*.md")):
        sid = slot_id_from_name(path.name)
        if sid is None:
            continue
        loc = index.get(sid)
        if loc is None:
            start_text = None
            for candidate in war_room.rglob(f"slot-{sid:03d}-start.md"):
                start_text = candidate.read_text(encoding="utf-8")
                break
            if start_text:
                loc = parse_slot_start_meta(start_text)
                if loc[0] and loc[1]:
                    index[sid] = loc
        if not loc or not loc[0] or not loc[1]:
            print(f"SKIP (no run/stage): {path.name}", file=sys.stderr)
            continue
        run_num, stage = loc
        dest = run_stage_dir(war_room, run_num, stage) / path.name
        if dest.resolve() == path.resolve():
            continue
        moves.append((path, dest))

    for src, dest in moves:
        if dest.exists() and dest.resolve() != src.resolve():
            print(f"SKIP (dest exists): {src.name} -> {dest.relative_to(war_room)}", file=sys.stderr)
            continue
        print(f"{'DRY ' if dry_run else ''}MOVE {src.name} -> {dest.relative_to(war_room)}")
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dest)

    if not dry_run and moves:
        print(f"Moved {len(moves)} files under {RUNS_DIR}/")

    return len(moves)


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate slot files to runs/run-NN/stage/ layout")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        count = migrate(args.workspace.resolve(), dry_run=args.dry_run)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1
    if count == 0:
        print("No flat slot files to migrate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
