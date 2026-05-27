"""Slot file paths under delivery-war-room/runs/run-NN/<stage>/."""
from __future__ import annotations

import re
from pathlib import Path

RUNS_DIR = "runs"
STAGES = frozenset({"shaping", "discovery", "exploration", "specification", "engineering"})

SLOT_ID_RE = re.compile(r"^slot-(\d+)", re.I)
SLOT_START_NAME_RE = re.compile(r"^slot-(\d+)(?:-[\w-]+)?-start\.md$", re.I)
SLOT_ARTIFACT_RE = re.compile(
    r"^slot-(\d+)(?:-[\w-]+)?-(?:start|finished|claim|blocked|stalled|answer)\.md$",
    re.I,
)


def run_stage_dir(war_room: Path, run_num: int, stage: str) -> Path:
    return war_room / RUNS_DIR / f"run-{run_num:02d}" / stage


def slot_id_from_name(name: str) -> int | None:
    m = SLOT_ID_RE.match(name)
    return int(m.group(1)) if m else None


def parse_slot_start_meta(text: str) -> tuple[int | None, str | None]:
    ticket = re.search(r"^ticket_run:\s*(\d+)", text, re.M)
    if ticket:
        run_num = int(ticket.group(1))
    else:
        run_line = re.search(r'^run:\s*["\']?Run\s*(\d+)', text, re.M)
        run_num = int(run_line.group(1)) if run_line else None
    stage_m = re.search(r"^stage:\s*(\w+)", text, re.M)
    stage = stage_m.group(1).lower() if stage_m else None
    if stage and stage not in STAGES:
        stage = None
    return run_num, stage


def find_slot_start(war_room: Path, slot_id: int) -> Path | None:
    """Locate a slot start file (including rework/re-review variants)."""
    for path in war_room.rglob("slot-*-start.md"):
        m = SLOT_START_NAME_RE.match(path.name)
        if m and int(m.group(1)) == slot_id:
            return path
    return None


def iter_slot_files(war_room: Path, glob_pattern: str) -> list[Path]:
    return sorted(war_room.rglob(glob_pattern))


def slot_path_for(
    war_room: Path,
    slot_id: int,
    filename: str,
    *,
    run_num: int,
    stage: str,
    mkdir: bool = True,
) -> Path:
    dest_dir = run_stage_dir(war_room, run_num, stage)
    if mkdir:
        dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir / filename


def run_for_slot_id(slot_id: int, run_state: dict) -> int | None:
    for run_key, rs in (run_state.get("runs") or {}).items():
        if not rs.get("slots_generated"):
            continue
        first, last = rs.get("first_slot"), rs.get("last_slot")
        if first is None or last is None:
            continue
        if int(first) <= slot_id <= int(last):
            return int(run_key)
    return None


def build_slot_location_index(
    war_room: Path,
    *,
    run_state: dict | None = None,
) -> dict[int, tuple[int, str]]:
    """Map slot id → (run_num, stage) from start files and run-state ranges."""
    index: dict[int, tuple[int, str]] = {}

    for path in iter_slot_files(war_room, "slot-*-start.md"):
        sid = slot_id_from_name(path.name)
        if sid is None:
            continue
        text = path.read_text(encoding="utf-8")
        run_num, stage = parse_slot_start_meta(text)
        if run_num is None and run_state:
            run_num = run_for_slot_id(sid, run_state)
        if run_num and stage:
            index[sid] = (run_num, stage)

    if run_state:
        for run_key, rs in (run_state.get("runs") or {}).items():
            if not rs.get("slots_generated"):
                continue
            first = rs.get("first_slot")
            last = rs.get("last_slot")
            if first is None or last is None:
                continue
            run_num = int(run_key)
            for sid in range(int(first), int(last) + 1):
                if sid in index:
                    continue
                start = find_slot_start(war_room, sid)
                stage = "exploration"
                if start:
                    _, parsed_stage = parse_slot_start_meta(start.read_text(encoding="utf-8"))
                    if parsed_stage:
                        stage = parsed_stage
                index[sid] = (run_num, stage)

    return index


def resolve_slot_artifact(
    war_room: Path,
    slot_id: int,
    *,
    suffix: str,
    index: dict[int, tuple[int, str]] | None = None,
) -> Path | None:
    """Find slot-NN-{suffix}.md anywhere under war_room (flat or nested)."""
    padded = f"{slot_id:03d}"
    plain = str(slot_id)
    names = {f"slot-{padded}-{suffix}.md", f"slot-{plain}-{suffix}.md"}
    if suffix == "start":
        names.update(
            {
                f"slot-{padded}-rework-start.md",
                f"slot-{padded}-rework-2-start.md",
                f"slot-{padded}-re-review-start.md",
                f"slot-{padded}-re-review-2-start.md",
                f"slot-{padded}-rework2-start.md",
                f"slot-{padded}-rework2-re-review-start.md",
            }
        )
    for path in war_room.rglob("slot-*.md"):
        if path.name in names:
            return path
        if suffix != "start" and path.name.startswith(f"slot-{padded}-") and path.name.endswith(
            f"-{suffix}.md"
        ):
            return path
        if suffix != "start" and path.name.startswith(f"slot-{plain}-") and path.name.endswith(
            f"-{suffix}.md"
        ):
            return path
    return None


def max_existing_slot_id(war_room: Path) -> int:
    best = 0
    for path in war_room.rglob("slot-*.md"):
        sid = slot_id_from_name(path.name)
        if sid is not None:
            best = max(best, sid)
    return best
