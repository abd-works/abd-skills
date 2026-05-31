#!/usr/bin/env python3
"""Shared delivery model for JIT Kanban with ticket scattering.

Ticket-based model: no slots, no run-catalog, no run-state.
Board state lives in board.json with tickets flowing through stages.
Stage configuration is defined ONLY in kanban.json — tickets carry a
`skill_progress` map that is lazily populated when agents start work.

Machine files under `<workspace>/docs/planning/kanban/`:
  - `kanban.json` — kanban board stage configuration (stages, scope, stage work required)
  - `board.json` — Kanban state (backlog, active, done, archived, team)
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
    stage_work_required: list[SkillDef] = field(default_factory=list)


@dataclass
class KanbanBoard:
    name: str
    label: str = ""
    stages: list[StageDef] = field(default_factory=list)


@dataclass
class SkillProgress:
    """Tracks execution and review state for one skill on a ticket. Lazily created when an agent starts work."""
    execution_status: str = "not_started"
    agent: str | None = None
    start: str | None = None
    end: str | None = None
    review_status: str | None = None
    reviewer: str | None = None
    review_start: str | None = None
    review_end: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_status": self.execution_status,
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
            execution_status=d.get("execution_status", d.get("status", "not_started")),
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
    created: str | None = None
    skill_progress: dict[str, SkillProgress] = field(default_factory=dict)
    entered_stage: str | None = None
    completed_stage: str | None = None
    stage_history: list[dict[str, str | None]] = field(default_factory=list)
    archived: str | None = None
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
            "created": self.created,
            "entered_stage": self.entered_stage,
            "completed_stage": self.completed_stage,
            "stage_history": self.stage_history,
            "archived": self.archived,
            "scatter_from": self.scatter_from,
            "scatter_to": self.scatter_to,
            "notes": self.notes,
        }
        if self.skill_progress:
            d["skill_progress"] = {k: v.to_dict() for k, v in self.skill_progress.items()}
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Ticket":
        raw_progress = d.get("skill_progress") or d.get("progress") or {}
        skill_progress = {}
        for k, v in raw_progress.items():
            skill_progress[k] = SkillProgress.from_dict(v) if isinstance(v, dict) else SkillProgress()
        return cls(
            ticket_id=d["ticket_id"],
            lineage=d.get("lineage", []),
            scope_level=d.get("scope_level", "all"),
            stage=d.get("stage", "shaping"),
            priority=d.get("priority", 1),
            created=d.get("created"),
            skill_progress=skill_progress,
            entered_stage=d.get("entered_stage"),
            completed_stage=d.get("completed_stage"),
            stage_history=d.get("stage_history", []),
            archived=d.get("archived"),
            scatter_from=d.get("scatter_from"),
            scatter_to=d.get("scatter_to", []),
            notes=d.get("notes", ""),
        )

    def is_stage_complete(self, stage_def: StageDef) -> bool:
        """A stage is complete when ALL skills in the kanban board's stage work required
        have skill_progress entries with execution_status=done and review_status=done."""
        if not stage_def.stage_work_required:
            return False
        for skill_def in stage_def.stage_work_required:
            sp = self.skill_progress.get(skill_def.skill)
            if sp is None or sp.execution_status != "done" or sp.review_status != "done":
                return False
        return True

    def is_active(self) -> bool:
        return any(
            sp.execution_status == "in_progress" or sp.review_status == "in_progress"
            for sp in self.skill_progress.values()
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


def load_kanban_board(workspace: Path) -> dict[str, KanbanBoard]:
    wr = war_room_dir(workspace)
    path = wr / "kanban.json"
    if not path.is_file():
        legacy = wr / "system-of-work.json"
        if legacy.is_file():
            path = legacy
        else:
            return {}
    raw = _read_json(path)
    out: dict[str, KanbanBoard] = {}
    for name, block in raw.get("definitions", {}).items():
        stages: list[StageDef] = []
        for stage_raw in block.get("stages", []):
            skills_raw = stage_raw.get("stage_work_required") or stage_raw.get("skills", [])
            stage_work_required = [
                SkillDef(skill=s["skill"], role=s["role"])
                for s in skills_raw
            ]
            stages.append(StageDef(
                name=stage_raw["name"],
                scope=stage_raw.get("scope", "all"),
                stage_work_required=stage_work_required,
            ))
        out[name] = KanbanBoard(
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
            "stage_configuration": None,
            "backlog": [],
            "active": [],
            "done": [],
            "archived": [],
            "team": {},
        }
    return _read_json(path)


def save_board(workspace: Path, board: dict[str, Any]) -> None:
    board["synced_at"] = datetime.now(timezone.utc).isoformat()
    _write_json(war_room_dir(workspace) / "board.json", board)


def get_stage_def(kb: KanbanBoard, stage_name: str) -> StageDef | None:
    for s in kb.stages:
        if s.name == stage_name:
            return s
    return None


def next_stage(kb: KanbanBoard, current_stage: str) -> StageDef | None:
    for i, s in enumerate(kb.stages):
        if s.name == current_stage and i + 1 < len(kb.stages):
            return kb.stages[i + 1]
    return None


def advance_ticket_to_stage(ticket: Ticket, stage_def: StageDef) -> None:
    """Move ticket to a new stage. Records the completed stage in stage_history,
    then clears skill_progress (agents will start work lazily)."""
    now = datetime.now(timezone.utc).isoformat()
    if ticket.stage and ticket.entered_stage:
        ticket.completed_stage = now
        ticket.stage_history.append({
            "stage": ticket.stage,
            "entered": ticket.entered_stage,
            "completed": now,
        })
    ticket.stage = stage_def.name
    ticket.skill_progress = {}
    ticket.entered_stage = now
    ticket.completed_stage = None


def append_metrics_log(workspace: Path, event: dict[str, Any]) -> None:
    path = war_room_dir(workspace) / "metrics-log.jsonl"
    event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
