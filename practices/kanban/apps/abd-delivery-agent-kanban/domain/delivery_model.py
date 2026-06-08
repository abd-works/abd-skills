#!/usr/bin/env python3
"""Delivery Agent Kanban domain model (domain model: docs/domain/domain model.md).

Canonical home: practices/kanban/apps/abd-delivery-agent-kanban/domain/

Key abstractions:
  KanbanBoard, Ticket, BoardPosition, SkillProgress, Stage, StageWorkRequired,
  TeamMembership, Skill, Heartbeat (functions), ActionIntent (action_state.py)

Board state lives in board.json; stage configuration in kanban.json only.
Tickets carry skill_progress populated when agents start work.

War-room files under `<workspace>/docs/planning/kanban/`:
  kanban.json, board.json, metrics-log.jsonl, heartbeat-*.json, action-state.json
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ORDER = ["context", "shaping", "discovery", "exploration", "specification", "engineering"]
SCOPE_ORDER = ["project", "partition", "increment", "sprint"]
DEFAULT_BOARD_MODE = "automatic"


class ScatterNotAllowedError(Exception):
    """Raised when scatter is attempted but no finer-scope next stage exists."""


class DuplicateTicketIdError(Exception):
    """Raised when scatter would create a ticket ID that already exists on the board."""


# ---------------------------------------------------------------------------
# Stage Work Required (domain model: ordered skills, agent role per skill)
# ---------------------------------------------------------------------------

@dataclass
class Skill:
    """domain model Skill — skill name, required by stage, performed by agent role."""
    skill: str
    role: str
    optional: bool = False
    run_when: str | None = None

    @property
    def is_required(self) -> bool:
        return not self.optional

    @property
    def is_conditional(self) -> bool:
        return bool(self.run_when)


# Legacy alias used by orchestration scripts and tests
SkillDef = Skill


# ---------------------------------------------------------------------------
# Skill Progress (domain model: execution status, review status, agents, timestamps)
# ---------------------------------------------------------------------------

@dataclass
class SkillProgress:
    """Per-skill execution and review state on a ticket."""
    execution_status: str = "not_started"
    agent: str | None = None
    start: str | None = None
    end: str | None = None
    review_status: str | None = None
    reviewer: str | None = None
    review_start: str | None = None
    review_end: str | None = None
    notes: str | None = None

    # --- domain model responsibilities ---

    def is_done(self) -> bool:
        """Invariant: execution done AND review done."""
        return self.execution_status == "done" and self.review_status == "done"

    def review_can_start(self) -> bool:
        """Invariant: execution must be done before review leaves not_started."""
        return self.execution_status == "done"

    def is_claimable(self) -> bool:
        if self.execution_status in ("not_started", None):
            return True
        return self.execution_status not in ("in_progress", "done")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "execution_status": self.execution_status,
            "agent": self.agent,
            "start": self.start,
            "end": self.end,
            "review_status": self.review_status,
            "reviewer": self.reviewer,
            "review_start": self.review_start,
            "review_end": self.review_end,
        }
        if self.notes:
            d["notes"] = self.notes
        return d

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
            notes=d.get("notes"),
        )


# ---------------------------------------------------------------------------
# Stage (domain model: stage name, scope level, queue/ip/done of tickets)
# ---------------------------------------------------------------------------

@dataclass
class StageWorkRequired:
    """domain model Stage Work Required — ordered skills for a stage."""
    ordered_skills: list[Skill] = field(default_factory=list)

    def first_required_skill(self) -> str | None:
        for skill in self.ordered_skills:
            if skill.is_required:
                return skill.skill
        return None


@dataclass
class Stage:
    """domain model Stage — name, scope level, and stage work required."""
    name: str
    scope: str
    stage_work_required: list[Skill] = field(default_factory=list)

    @property
    def work_required(self) -> StageWorkRequired:
        return StageWorkRequired(ordered_skills=self.stage_work_required)

    def first_required_skill(self) -> str | None:
        for sd in self.stage_work_required:
            if sd.is_required:
                return sd.skill
        return None

    def priors_done(self, ticket: "Ticket", skill_name: str) -> bool:
        """All prior skills in the rail before ``skill_name`` are done (or optional+absent)."""
        for skill_def in self.stage_work_required:
            if skill_def.skill == skill_name:
                return True
            sp = ticket.skill_progress.get(skill_def.skill)
            if skill_def.optional and sp is None:
                continue
            if sp is None or not sp.is_done():
                return False
        return False


StageDef = Stage


# ---------------------------------------------------------------------------
# Board Position (domain model: derived sub-state and current stage — not persisted)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BoardPosition:
    """Value object: in-progress or done sub-state within the current stage."""
    sub_state: str
    current_stage_name: str

    @classmethod
    def derive(cls, ticket: "Ticket", stage_def: Stage | None = None) -> BoardPosition:
        if ticket.has_skill_in_progress():
            sub_state = "in_progress"
        elif stage_def is not None and ticket.is_stage_complete(stage_def):
            sub_state = "done"
        else:
            sub_state = "in_progress"
        return cls(sub_state=sub_state, current_stage_name=ticket.stage)


# ---------------------------------------------------------------------------
# Team Membership (domain model: role pair counts on the board)
# ---------------------------------------------------------------------------

@dataclass
class TeamMembership:
    """Maps delivery roles to agent pair counts (board team configuration)."""
    counts: dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_board(cls, board: dict[str, Any], kb_block: dict[str, Any] | None = None) -> TeamMembership:
        return cls(counts=load_team(board, kb_block))

    def count_for_role(self, role: str) -> int:
        return self.counts.get(role, 0)

    def increment_pair_count(self, role: str) -> None:
        self.counts[role] = self.counts.get(role, 0) + 1

    def decrement_pair_count(self, role: str) -> None:
        self.counts[role] = max(0, self.counts.get(role, 0) - 1)

    def to_dict(self) -> dict[str, int]:
        return dict(self.counts)


# ---------------------------------------------------------------------------
# Ticket (domain model: identifier, lineage, board position, scope level, priority,
#         skill progress, stage timestamps, wait/advance/scatter)
# ---------------------------------------------------------------------------

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

    # --- domain model responsibilities ---

    def is_stage_complete(self, stage_def: Stage) -> bool:
        """Invariant: a stage is complete only when every required skill has
        execution done and review done."""
        if not stage_def.stage_work_required:
            return False
        for skill_def in stage_def.stage_work_required:
            if not skill_def.is_required:
                continue
            sp = self.skill_progress.get(skill_def.skill)
            if sp is None or not sp.is_done():
                return False
        return True

    def is_active(self) -> bool:
        return any(
            sp.execution_status == "in_progress" or sp.review_status == "in_progress"
            for sp in self.skill_progress.values()
        )

    def has_skill_in_progress(self) -> bool:
        """True when any skill is actively executing or under review."""
        for sp in self.skill_progress.values():
            if sp.execution_status == "in_progress" or sp.review_status == "in_progress":
                return True
        return False

    def needs_scatter(self, kb: "KanbanBoard") -> bool:
        """Invariant: scatter only when the next stage's scope is finer than current."""
        stage_def = kb.get_stage(self.stage)
        if stage_def is None or not self.is_stage_complete(stage_def):
            return False
        nxt = kb.next_stage(self.stage)
        if nxt is None or nxt.scope == stage_def.scope:
            return False
        return True

    def board_position(self, stage_def: Stage | None = None) -> BoardPosition:
        return BoardPosition.derive(self, stage_def)

    def advance_to_next_stage(self, next_stage_def: Stage) -> None:
        """Move ticket to a new stage (same scope). Records history, clears skill_progress."""
        now = datetime.now(timezone.utc).isoformat()
        if self.stage and self.entered_stage:
            self.completed_stage = now
            self.stage_history.append({
                "stage": self.stage,
                "entered": self.entered_stage,
                "completed": now,
            })
        self.stage = next_stage_def.name
        self.skill_progress = {}
        self.entered_stage = now
        self.completed_stage = None

    def scatter_into_children(
        self,
        kb: "KanbanBoard",
        children_spec: list[dict],
        *,
        existing_ids: frozenset[str] | None = None,
    ) -> list["Ticket"]:
        """Scatter this ticket into child tickets at the next stage's finer scope.

        Invariant: scatter only occurs when the next stage's scope level is finer
        than the current.

        Archives self and returns the new child tickets (not yet persisted).
        Raises DuplicateTicketIdError if any child ID collides with existing_ids.
        """
        if existing_ids:
            collisions = [c["id"] for c in children_spec if c["id"] in existing_ids]
            if collisions:
                raise DuplicateTicketIdError(
                    f"Scatter from {self.ticket_id} would create duplicate IDs: {collisions}"
                )

        nxt = kb.next_stage(self.stage)
        if nxt is None:
            raise ScatterNotAllowedError(f"No next stage after '{self.stage}'")

        now = datetime.now(timezone.utc).isoformat()
        self.completed_stage = now
        self.archived = now
        self.scatter_to = [c["id"] for c in children_spec]
        if self.stage and self.entered_stage:
            self.stage_history.append({
                "stage": self.stage,
                "entered": self.entered_stage,
                "completed": now,
            })

        children: list[Ticket] = []
        for spec in children_spec:
            child = Ticket(
                ticket_id=spec["id"],
                lineage=self.lineage + [spec.get("name", spec["id"])],
                scope_level=nxt.scope,
                stage=nxt.name,
                priority=spec.get("priority", 1),
                created=now,
                scatter_from=self.ticket_id,
                entered_stage=now,
            )
            children.append(child)
        return children

    def next_eligible_skill(self, stage_def: Stage, role: str) -> str | None:
        """First claimable skill for ``role`` in rail order, with priors done.

        If a skill is already in_progress for this role (e.g. manual assignment),
        return it immediately — the priors gate doesn't apply to work already started.
        """
        for skill_def in stage_def.stage_work_required:
            if skill_def.role != role:
                continue
            sp = self.skill_progress.get(skill_def.skill)
            if sp is not None and sp.execution_status == "in_progress" and sp.agent == role:
                return skill_def.skill
            if not stage_def.priors_done(self, skill_def.skill):
                break
            if sp is not None and sp.is_done():
                continue
            if sp is not None and not sp.is_claimable():
                break
            return skill_def.skill
        return None

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


# ---------------------------------------------------------------------------
# Kanban Board (domain model: ordered stages, active stage flow, team configuration,
#               tickets in flow, define stage order)
# ---------------------------------------------------------------------------

@dataclass
class KanbanBoard:
    name: str
    label: str = ""
    stages: list[Stage] = field(default_factory=list)
    saved_at: str | None = None

    # --- domain model responsibilities ---

    def record_save_timestamp(self) -> None:
        self.saved_at = now_iso()

    def get_stage(self, stage_name: str) -> Stage | None:
        for s in self.stages:
            if s.name == stage_name:
                return s
        return None

    def next_stage(self, current_stage: str) -> Stage | None:
        for i, s in enumerate(self.stages):
            if s.name == current_stage and i + 1 < len(self.stages):
                return self.stages[i + 1]
        return None

    def tickets_needing_scatter(self, board: dict) -> list[Ticket]:
        """Done tickets at a scope boundary awaiting scatter."""
        out: list[Ticket] = []
        for raw in board.get("done", []):
            ticket = Ticket.from_dict(raw)
            if ticket.archived or ticket.scatter_to:
                continue
            if ticket.needs_scatter(self):
                out.append(ticket)
        return out

    def pull_slots_for_stage(
        self,
        board: dict,
        stage_def: Stage,
        team: dict[str, int] | None = None,
    ) -> int:
        """How many backlog tickets to pull for a stage.  WIP from config or team size."""
        wip = wip_limit_for_scope(board, stage_def.scope, team, stage_def)
        first_skill = stage_def.first_required_skill()
        if first_skill is None:
            return max(0, wip - count_active_at_stage(board, stage_def.name))
        needing = 0
        for raw in board.get("active", []):
            ticket = Ticket.from_dict(raw)
            if ticket.stage != stage_def.name:
                continue
            sp = ticket.skill_progress.get(first_skill)
            if sp is None or not sp.is_done():
                needing += 1
        return max(0, wip - needing)

    def find_next_eligible(
        self,
        tickets: list[Ticket],
        role: str,
        *,
        skip_skills: frozenset[tuple[str, str]] | None = None,
    ) -> tuple[Ticket, str, Stage] | None:
        """Downstream-first pull: last stage first, lowest priority, first open skill."""
        skip = skip_skills or frozenset()
        for stage_def in reversed(self.stages):
            stage_tickets = sorted(
                [t for t in tickets if t.stage == stage_def.name],
                key=lambda t: t.priority,
            )
            for ticket in stage_tickets:
                skill = ticket.next_eligible_skill(stage_def, role)
                if skill is None:
                    continue
                key = (ticket.ticket_id, skill)
                if key in skip:
                    continue
                return ticket, skill, stage_def
        return None

    def list_eligible_pulls(
        self,
        tickets: list[Ticket],
        role: str,
    ) -> list[tuple[str, str]]:
        """All claimable (ticket_id, skill) pairs for a role — downstream-first, no skill-side gates."""
        skip: set[tuple[str, str]] = set()
        out: list[tuple[str, str]] = []
        for _ in range(max(1, len(tickets)) + 8):
            match = self.find_next_eligible(tickets, role, skip_skills=frozenset(skip))
            if match is None:
                break
            ticket, skill, _ = match
            key = (ticket.ticket_id, skill)
            out.append(key)
            skip.add(key)
        return out

    def count_eligible_claims(
        self,
        tickets: list[Ticket],
        role: str,
        *,
        skip_skills: frozenset[tuple[str, str]] | None = None,
    ) -> list[tuple[str, str]]:
        """One eligible skill per active ticket (parallel flight)."""
        out: list[tuple[str, str]] = []
        skip: set[tuple[str, str]] = set(skip_skills or ())
        for ticket in tickets:
            match = self.find_next_eligible([ticket], role, skip_skills=frozenset(skip))
            if match:
                key = (match[0].ticket_id, match[1])
                out.append(key)
                skip.add(key)
        return out

    def in_progress_claims_for_role(
        self,
        tickets: list[Ticket],
        role: str,
    ) -> list[tuple[Ticket, str]]:
        """Downstream-first in_progress skills owned by ``role`` on active tickets."""
        claims: list[tuple[Ticket, str]] = []
        for stage_def in reversed(self.stages):
            stage_tickets = sorted(
                [t for t in tickets if t.stage == stage_def.name],
                key=lambda t: t.priority,
            )
            for ticket in stage_tickets:
                for skill_id, sp in ticket.skill_progress.items():
                    owns_execution = sp.execution_status == "in_progress" and sp.agent == role
                    owns_review = sp.review_status == "in_progress" and (
                        sp.reviewer == role or sp.agent == role
                    )
                    if owns_execution or owns_review:
                        claims.append((ticket, skill_id))
        return claims


# ---------------------------------------------------------------------------
# Infrastructure: persistence, heartbeat, team loading
# ---------------------------------------------------------------------------

def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def war_room_dir(workspace: Path) -> Path:
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
                SkillDef(
                    skill=s["skill"],
                    role=s["role"],
                    optional=bool(s.get("optional")),
                    run_when=s.get("run_when"),
                )
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
            "board_mode": DEFAULT_BOARD_MODE,
            "backlog": [],
            "active": [],
            "done": [],
            "archived": [],
            "team": {},
        }
    board = _read_json(path)
    board.setdefault("board_mode", DEFAULT_BOARD_MODE)
    return board


def save_board(workspace: Path, board: dict[str, Any]) -> None:
    board["synced_at"] = datetime.now(timezone.utc).isoformat()
    board.setdefault("board_mode", DEFAULT_BOARD_MODE)
    _write_json(war_room_dir(workspace) / "board.json", board)


def append_metrics_log(workspace: Path, event: dict[str, Any]) -> None:
    path = war_room_dir(workspace) / "metrics-log.jsonl"
    event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_team(board: dict[str, Any], kb_block: dict[str, Any] | None = None) -> dict[str, int]:
    team = board.get("team") or board.get("wip_policy") or {}
    if not team and kb_block:
        team = kb_block.get("team") or {}
    return {k: int(v) for k, v in team.items()}


def find_ticket_in_board(board: dict[str, Any], ticket_id: str) -> tuple[str, int, Ticket] | None:
    for bucket in ("active", "backlog", "done"):
        for i, raw in enumerate(board.get(bucket, [])):
            if raw.get("ticket_id") == ticket_id:
                return bucket, i, Ticket.from_dict(raw)
    return None


def save_ticket_in_board(board: dict[str, Any], bucket: str, index: int, ticket: Ticket) -> None:
    board.setdefault(bucket, [])[index] = ticket.to_dict()


# ---------------------------------------------------------------------------
# Heartbeat (domain model: timestamp, age, determine liveness)
# ---------------------------------------------------------------------------

def heartbeat_path(wr: Path, role: str, instance: int = 1) -> Path:
    if instance <= 1:
        return wr / f"heartbeat-{role}.json"
    return wr / f"heartbeat-{role}-{instance}.json"


def list_heartbeat_files(wr: Path, role: str) -> list[Path]:
    primary = wr / f"heartbeat-{role}.json"
    numbered = sorted(wr.glob(f"heartbeat-{role}-*.json"))
    paths: list[Path] = []
    if primary.is_file():
        paths.append(primary)
    paths.extend(p for p in numbered if p not in paths)
    return paths


def read_heartbeat_age_seconds(path: Path) -> float | None:
    if not path.is_file():
        return None
    try:
        raw = _read_json(path)
        ts = raw.get("ts") or raw.get("timestamp")
        if not ts:
            return None
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - dt).total_seconds()
        if age < 0:
            return None
        return age
    except (json.JSONDecodeError, ValueError, TypeError):
        return None


def executor_spawns_path(wr: Path) -> Path:
    return wr / "executor-spawns.json"


def load_executor_spawns(wr: Path) -> dict[str, Any]:
    path = executor_spawns_path(wr)
    if not path.is_file():
        return {}
    try:
        return _read_json(path)
    except (json.JSONDecodeError, OSError):
        return {}


def register_executor_spawn(wr: Path, role: str, instance: int = 1) -> int:
    """Bump spawn epoch when lead assigns a new executor session for role/instance."""
    spawns = load_executor_spawns(wr)
    role_block = spawns.setdefault(role, {})
    inst_key = str(instance)
    current = int(role_block.get(inst_key, {}).get("epoch", 0))
    epoch = current + 1
    role_block[inst_key] = {"epoch": epoch, "registered_at": now_iso()}
    _write_json(executor_spawns_path(wr), spawns)
    return epoch


def read_registered_spawn_epoch(wr: Path, role: str, instance: int = 1) -> int | None:
    block = load_executor_spawns(wr).get(role, {}).get(str(instance))
    if not block:
        return None
    epoch = int(block.get("epoch", 0))
    return epoch if epoch > 0 else None


def heartbeat_matches_registered_spawn(wr: Path, role: str, raw: dict[str, Any]) -> bool:
    """True only when heartbeat proves the current registered executor session."""
    instance = int(raw.get("instance") or 1)
    registered = read_registered_spawn_epoch(wr, role, instance)
    if registered is None:
        return False
    hb_epoch = raw.get("spawn_epoch")
    if hb_epoch is None:
        return False
    return int(hb_epoch) == registered


def purge_unregistered_heartbeats(wr: Path, role: str) -> int:
    """Remove heartbeats that cannot prove an active registered executor session."""
    removed = 0
    for path in list_heartbeat_files(wr, role):
        if path.name == "heartbeat-kanban-lead.json":
            continue
        try:
            raw = _read_json(path)
        except (json.JSONDecodeError, OSError):
            path.unlink(missing_ok=True)
            removed += 1
            continue
        if not heartbeat_matches_registered_spawn(wr, role, raw):
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def count_live_agents(wr: Path, role: str, stale_seconds: float = 120.0) -> int:
    live = 0
    for path in list_heartbeat_files(wr, role):
        age = read_heartbeat_age_seconds(path)
        if age is None or age > stale_seconds:
            continue
        try:
            raw = _read_json(path)
        except (json.JSONDecodeError, OSError):
            continue
        if heartbeat_matches_registered_spawn(wr, role, raw):
            live += 1
    return live


def count_working_agents(wr: Path, role: str, stale_seconds: float = 120.0) -> int:
    working = 0
    for path in list_heartbeat_files(wr, role):
        age = read_heartbeat_age_seconds(path)
        if age is None or age > stale_seconds:
            continue
        try:
            raw = _read_json(path)
        except (json.JSONDecodeError, OSError):
            continue
        if raw.get("status") == "working" and heartbeat_matches_registered_spawn(wr, role, raw):
            working += 1
    return working


def read_heartbeat_instance(path: Path) -> int:
    try:
        raw = _read_json(path)
        return int(raw.get("instance") or 1)
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return 1


def write_heartbeat(
    wr: Path,
    role: str,
    status: str,
    note: str = "",
    instance: int = 1,
    spawn_epoch: int | None = None,
) -> None:
    path = heartbeat_path(wr, role, instance)
    payload = {
        "agent_role": role,
        "role": role,
        "instance": instance,
        "ts": now_iso(),
        "status": status,
    }
    if spawn_epoch is not None:
        payload["spawn_epoch"] = spawn_epoch
    if note:
        payload["note"] = note
    _write_json(path, payload)


# ---------------------------------------------------------------------------
# WIP and stage query helpers (used by KanbanBoard methods and lead_pull)
# ---------------------------------------------------------------------------

def wip_limit_for_scope(
    board: dict,
    scope: str,
    team: dict[str, int] | None = None,
    stage_def: StageDef | None = None,
) -> int:
    """WIP limit for any scope level.  Resolution:
    1. Explicit ``<scope>_wip_limit`` on board.json
    2. Team size of the first required skill's role
    3. Default 3 (1 for partition)
    """
    explicit = board.get(f"{scope}_wip_limit")
    if isinstance(explicit, int) and explicit > 0:
        return explicit
    if team and stage_def:
        for sd in stage_def.stage_work_required:
            if sd.is_required:
                role_cap = team.get(sd.role, 0)
                if role_cap > 0:
                    return role_cap
    if scope == "partition":
        return 1
    return 3


def count_active_at_stage(board: dict, stage_name: str) -> int:
    return sum(
        1 for raw in board.get("active", [])
        if Ticket.from_dict(raw).stage == stage_name
    )


def select_backlog_for_stage(board: dict, stage_name: str, limit: int) -> list[dict]:
    candidates = [
        raw for raw in board.get("backlog", [])
        if Ticket.from_dict(raw).stage == stage_name
    ]
    candidates.sort(key=lambda raw: Ticket.from_dict(raw).priority)
    return candidates[:limit]


def count_in_progress_for_role(tickets: list[Ticket], role: str) -> int:
    n = 0
    for ticket in tickets:
        for sp in ticket.skill_progress.values():
            if sp.agent == role and sp.execution_status == "in_progress":
                n += 1
    return n


def module_number_from_ticket_id(ticket_id: str) -> int:
    head = ticket_id.split("-", 1)[0]
    if not head.isdigit():
        raise ValueError(f"Cannot infer module number from ticket_id: {ticket_id}")
    return int(head)


def is_fixture_mode(workspace: Path) -> bool:
    """Return True when the workspace CONTEXT.md declares fixture_mode: true."""
    context = workspace / "CONTEXT.md"
    if not context.is_file():
        return False
    text = context.read_text(encoding="utf-8")
    if not re.search(r"fixture_mode", text, re.IGNORECASE):
        return False
    return bool(re.search(r"fixture_mode[^\n]*\btrue\b", text, re.IGNORECASE))


def backlog_sort_key(ticket: Ticket) -> tuple:
    scope_idx = SCOPE_ORDER.index(ticket.scope_level) if ticket.scope_level in SCOPE_ORDER else 99
    if ticket.scope_level == "increment":
        try:
            mod = module_number_from_ticket_id(ticket.ticket_id)
        except ValueError:
            mod = 99
        return (scope_idx, mod, ticket.priority)
    return (scope_idx, ticket.priority, 0)


