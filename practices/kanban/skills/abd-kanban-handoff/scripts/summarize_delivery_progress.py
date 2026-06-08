#!/usr/bin/env python3
"""Summarize abd-kanban delivery progress from board + artifacts (no chat).

Usage:
  python summarize_delivery_progress.py --workspace <path> [--format text|json]
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGES = ("context", "shaping", "discovery", "exploration", "specification", "engineering")
STAGE_SCOPE = {
    "context": "all",
    "shaping": "all",
    "discovery": "increment",
    "exploration": "increment",
    "specification": "sprint",
    "engineering": "sprint",
}

SHAPING_SIGNALS = (
    "module-partition.md",
    "impact-map.md",
    "architecture-outline.md",
    "story-map.md",
    "story-graph.json",
)
DISCOVERY_SIGNALS = (
    "thin-slicing.md",
    "domain-terms.md",
    "information-architecture.md",
    "architecture-blueprint.md",
)
INCREMENT_STAGE_DIRS = ("exploration", "specification", "engineering")


def war_room_dir(workspace: Path) -> Path | None:
    p = workspace / "docs" / "kanban"
    return p if p.is_dir() else None


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return None


def skill_fully_done(sp: dict[str, Any]) -> bool:
    return sp.get("execution_status") == "done" and sp.get("review_status") == "done"


def summarize_ticket(t: dict[str, Any]) -> dict[str, Any]:
    progress = t.get("skill_progress") or {}
    in_progress: list[str] = []
    done: list[str] = []
    awaiting_review: list[str] = []
    for skill_id, sp in progress.items():
        if not isinstance(sp, dict):
            continue
        if sp.get("execution_status") == "in_progress":
            in_progress.append(skill_id)
        elif sp.get("execution_status") == "done" and sp.get("review_status") == "in_progress":
            awaiting_review.append(skill_id)
        elif skill_fully_done(sp):
            done.append(skill_id)
    return {
        "ticket_id": t.get("ticket_id"),
        "stage": t.get("stage"),
        "scope_level": t.get("scope_level"),
        "lineage": t.get("lineage"),
        "scatter_from": t.get("scatter_from"),
        "skills_in_progress": in_progress,
        "skills_awaiting_review": awaiting_review,
        "skills_done": done,
        "stage_history": t.get("stage_history") or [],
    }


def load_kanban_stages(wr: Path, config_name: str | None) -> list[dict[str, Any]]:
    raw = _read_json(wr / "kanban.json") or _read_json(wr / "system-of-work.json")
    if not raw or not config_name:
        return []
    block = (raw.get("definitions") or {}).get(config_name) or {}
    stages = []
    for s in block.get("stages") or []:
        skills = s.get("stage_work_required") or s.get("skills") or []
        stages.append({
            "name": s.get("name"),
            "scope": s.get("scope"),
            "skills": [x.get("skill") for x in skills if isinstance(x, dict)],
        })
    return stages


def folder_has_files(path: Path, min_count: int = 1) -> bool:
    if not path.is_dir():
        return False
    n = 0
    for p in path.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".md", ".json", ".drawio", ".txt"):
            n += 1
            if n >= min_count:
                return True
    return False


def infer_end_to_end(workspace: Path) -> dict[str, Any]:
    e2e = workspace / "docs" / "end-to-end"
    out: dict[str, Any] = {}
    for stage in STAGES:
        base = e2e / stage
        entry: dict[str, Any] = {"path": str(base), "present": base.is_dir(), "signals": []}
        if stage == "shaping" and base.is_dir():
            for name in SHAPING_SIGNALS:
                if (base / name).is_file():
                    entry["signals"].append(name)
        if stage == "discovery" and base.is_dir():
            for sub in ("stories", "domain", "ux", "architecture"):
                sub_path = base / sub
                if folder_has_files(sub_path):
                    entry["signals"].append(f"{sub}/")
            for name in DISCOVERY_SIGNALS:
                for hit in base.rglob(name):
                    if hit.is_file():
                        entry["signals"].append(name)
                        break
        if stage in ("exploration", "specification", "engineering") and base.is_dir():
            if folder_has_files(base):
                entry["signals"].append("has_content")
        out[stage] = entry
    return out


def infer_increments(workspace: Path) -> list[dict[str, Any]]:
    inc_root = workspace / "docs" / "increments"
    if not inc_root.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    pattern = re.compile(r"^(\d+)-(.+)$")
    for child in sorted(inc_root.iterdir()):
        if not child.is_dir():
            continue
        m = pattern.match(child.name)
        deepest = None
        for stage_dir in reversed(INCREMENT_STAGE_DIRS):
            if folder_has_files(child / stage_dir):
                deepest = stage_dir
                break
        rows.append({
            "folder": child.name,
            "path": str(child),
            "increment_number": int(m.group(1)) if m else None,
            "slug": m.group(2) if m else child.name,
            "deepest_stage_with_files": deepest,
        })
    return rows


def build_report(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    wr = war_room_dir(workspace)
    board = _read_json(wr / "board.json") if wr else None
    config = (board or {}).get("stage_configuration") or (board or {}).get("system_of_work")

    tickets_summary: dict[str, list[dict[str, Any]]] = {}
    if board:
        for bucket in ("active", "backlog", "done", "archived"):
            raw_list = board.get(bucket) or []
            tickets_summary[bucket] = [
                summarize_ticket(t) for t in raw_list if isinstance(t, dict)
            ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "war_room": str(wr) if wr else None,
        "has_board": board is not None,
        "board_mode": (board or {}).get("board_mode"),
        "stage_configuration": config,
        "kanban_stages": load_kanban_stages(wr, config) if wr else [],
        "tickets": tickets_summary,
        "end_to_end": infer_end_to_end(workspace),
        "increments": infer_increments(workspace),
        "stage_scope_reference": STAGE_SCOPE,
    }


def format_text(report: dict[str, Any]) -> str:
    lines = [
        "# Delivery progress summary (machine)",
        f"Workspace: {report['workspace']}",
        f"War room: {report['war_room'] or '(none)'}",
        f"Board present: {report['has_board']} · mode: {report.get('board_mode')}",
        f"Configuration: {report.get('stage_configuration')}",
        "",
        "## End-to-end artifact signals",
    ]
    for stage, info in report.get("end_to_end", {}).items():
        sig = ", ".join(info.get("signals") or []) or "(none)"
        lines.append(f"- **{stage}** ({STAGE_SCOPE.get(stage, '?')}): {sig}")

    lines.append("")
    lines.append("## Increments")
    incs = report.get("increments") or []
    if not incs:
        lines.append("- (no docs/increments folders)")
    else:
        for row in incs:
            lines.append(
                f"- `{row['folder']}` -> deepest: {row.get('deepest_stage_with_files') or 'empty'}"
            )

    lines.append("")
    lines.append("## Board tickets")
    for bucket, tickets in (report.get("tickets") or {}).items():
        if not tickets:
            continue
        lines.append(f"### {bucket} ({len(tickets)})")
        for t in tickets:
            ip = t.get("skills_in_progress") or []
            ar = t.get("skills_awaiting_review") or []
            done = t.get("skills_done") or []
            lines.append(
                f"- `{t.get('ticket_id')}` stage={t.get('stage')} scope={t.get('scope_level')} "
                f"in_progress={ip} review={ar} done={len(done)} skills"
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize abd-kanban delivery progress")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    report = build_report(args.workspace)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
