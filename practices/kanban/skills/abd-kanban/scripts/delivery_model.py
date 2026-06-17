#!/usr/bin/env python3
"""Shared delivery model for JIT Kanban with ticket scattering.

Ticket-based model: no slots, no run-catalog, no run-state.
Board state lives in board.json with tickets flowing through stages.
Skills are defined ONLY in system-of-work.json — tickets carry a `progress`
map that is lazily populated when agents claim work.

Machine files under `<workspace>/docs/planning/kanban/`:
  - `system-of-work.json` — stage definitions with scope levels and ordered skills
  - `board.json` — Kanban state (backlog, active, done, archived, wip_policy)
  - `metrics-log.jsonl` — timestamped events
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ORDER = ["context", "shaping", "discovery", "exploration", "specification", "engineering"]


@dataclass
class SkillDef:
    skill: str
    role: str


@dataclass
class StageDef:
    name: str
    scope: str
    skills: list[SkillDef] = field(default_factory=list)


@dataclass
class SystemOfWork:
    name: str
    label: str = ""
    stages: list[StageDef] = field(default_factory=list)


@dataclass
class SkillProgress:
    """Tracks execution state for one skill on a ticket. Lazily created when claimed."""
    status: str = "to_do"
    agent: str | None = None
    start: str | None = None
    end: str | None = None
    review_status: str | None = None
    reviewer: str | None = None
    review_start: str | None = None
    review_end: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "agent": self.agent,
            "start": self.start,
            "end": self.end,
            "review_status": self.review_status,
            "reviewer": self.reviewer,
            "review_start": self.review_start,
            "review_end": self.review_end,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SkillProgress":
        return cls(
            status=d.get("status", "to_do"),
            agent=d.get("agent"),
            start=d.get("start"),
            end=d.get("end"),
            review_status=d.get("review_status"),
            reviewer=d.get("reviewer"),
            review_start=d.get("review_start"),
            review_end=d.get("review_end"),
        )


@dataclass
class Ticket:
    ticket_id: str
    lineage: list[str] = field(default_factory=list)
    scope_level: str = "all"
    stage: str = "shaping"
    priority: int = 1
    progress: dict[str, SkillProgress] = field(default_factory=dict)
    entered_stage: str | None = None
    completed_stage: str | None = None
    scatter_from: str | None = None
    scatter_to: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "ticket_id": self.ticket_id,
            "lineage": self.lineage,
            "scope_level": self.scope_level,
            "stage": self.stage,
            "priority": self.priority,
            "entered_stage": self.entered_stage,
            "completed_stage": self.completed_stage,
            "scatter_from": self.scatter_from,
            "scatter_to": self.scatter_to,
            "notes": self.notes,
        }
        if self.progress:
            d["progress"] = {k: v.to_dict() for k, v in self.progress.items()}
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Ticket":
        progress = {}
        for k, v in (d.get("progress") or {}).items():
            progress[k] = SkillProgress.from_dict(v) if isinstance(v, dict) else SkillProgress()
        return cls(
            ticket_id=d["ticket_id"],
            lineage=d.get("lineage", []),
            scope_level=d.get("scope_level", "all"),
            stage=d.get("stage", "shaping"),
            priority=d.get("priority", 1),
            progress=progress,
            entered_stage=d.get("entered_stage"),
            completed_stage=d.get("completed_stage"),
            scatter_from=d.get("scatter_from"),
            scatter_to=d.get("scatter_to", []),
            notes=d.get("notes", ""),
        )

    def is_stage_complete(self, stage_def: StageDef) -> bool:
        """A stage is complete when ALL skills defined in the system of work
        for this stage have progress entries with status=done and review_status=done."""
        if not stage_def.skills:
            return False
        for skill_def in stage_def.skills:
            sp = self.progress.get(skill_def.skill)
            if sp is None or sp.status != "done" or sp.review_status != "done":
                return False
        return True

    def is_active(self) -> bool:
        return any(
            sp.status == "in_progress" or sp.review_status == "in_progress"
            for sp in self.progress.values()
        )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def war_room_dir(workspace: Path) -> Path:
    """Look for kanban/ first, fall back to delivery-war-room/ for compatibility."""
    kanban = workspace / "docs" / "planning" / "kanban"
    if kanban.is_dir():
        return kanban
    legacy = workspace / "docs" / "planning" / "delivery-war-room"
    if legacy.is_dir():
        return legacy
    return kanban


def load_system_of_work(workspace: Path) -> dict[str, SystemOfWork]:
    path = war_room_dir(workspace) / "system-of-work.json"
    if not path.is_file():
        return {}
    raw = _read_json(path)
    out: dict[str, SystemOfWork] = {}
    for name, block in raw.get("definitions", {}).items():
        stages: list[StageDef] = []
        for stage_raw in block.get("stages", []):
            skills = [
                SkillDef(skill=s["skill"], role=s["role"])
                for s in stage_raw.get("skills", [])
            ]
            stages.append(StageDef(
                name=stage_raw["name"],
                scope=stage_raw.get("scope", "all"),
                skills=skills,
            ))
        out[name] = SystemOfWork(
            name=name,
            label=block.get("label", name),
            stages=stages,
        )
    return out


def load_board(workspace: Path) -> dict[str, Any]:
    path = war_room_dir(workspace) / "board.json"
    if not path.is_file():
        return {
            "schema": "abd-delivery-kanban/v2",
            "synced_at": None,
            "system_of_work": None,
            "backlog": [],
            "active": [],
            "done": [],
            "archived": [],
            "wip_policy": {},
        }
    return _read_json(path)


def save_board(workspace: Path, board: dict[str, Any]) -> None:
    board["synced_at"] = datetime.now(timezone.utc).isoformat()
    _write_json(war_room_dir(workspace) / "board.json", board)


def get_stage_def(sow: SystemOfWork, stage_name: str) -> StageDef | None:
    for s in sow.stages:
        if s.name == stage_name:
            return s
    return None


def next_stage(sow: SystemOfWork, current_stage: str) -> StageDef | None:
    for i, s in enumerate(sow.stages):
        if s.name == current_stage and i + 1 < len(sow.stages):
            return sow.stages[i + 1]
    return None


def advance_ticket_to_stage(ticket: Ticket, stage_def: StageDef) -> None:
    """Move ticket to a new stage. Clears progress (agents will claim lazily)."""
    ticket.stage = stage_def.name
    ticket.progress = {}
    ticket.entered_stage = datetime.now(timezone.utc).isoformat()
    ticket.completed_stage = None


def append_metrics_log(workspace: Path, event: dict[str, Any]) -> None:
    path = war_room_dir(workspace) / "metrics-log.jsonl"
    event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
