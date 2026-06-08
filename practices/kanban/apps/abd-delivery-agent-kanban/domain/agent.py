"""
agent.py

Domain area   : Kanban Board — Agent, Team Member: Agent
Responsibilities: start work on skill, drive skill to done, write heartbeat
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from .action_state import (
    ActionIntent,
    NoActionStateFileError,
    find_first_intent_for_role,
    load_action_intents,
    remove_action_intent,
)
from .board_mode import is_manual_mode
from .delivery_model import (
    KanbanBoard,
    SkillProgress,
    Stage,
    Ticket,
    append_metrics_log,
    count_in_progress_for_role,
    find_ticket_in_board,
    is_fixture_mode,
    load_board,
    load_kanban_board,
    load_team,
    now_iso,
    save_board,
    save_ticket_in_board,
    war_room_dir,
    read_registered_spawn_epoch,
    write_heartbeat,
)


class SkillAlreadyInProgressError(Exception):
    """Raised when an agent attempts to claim a skill already executing."""


class SkillAlreadyDoneError(Exception):
    """Raised when an agent attempts to claim a skill already completed."""


class TicketNotFoundError(Exception):
    """Raised when a referenced ticket does not exist on the board."""


class Agent:
    """A delivery agent that claims and completes skills on tickets.

    domain model responsibilities:
      - start work on skill    → Skill, Ticket, SkillProgress
      - drive skill to done    → SkillProgress
      - write heartbeat        → Heartbeat
    """

    def __init__(self, workspace: Path, role: str, instance: int = 1) -> None:
        self._workspace = workspace
        self._role = role
        self._instance = instance
        self._wr = war_room_dir(workspace)
        self._spawn_epoch = read_registered_spawn_epoch(self._wr, role, instance)

    def _heartbeat(self, status: str, note: str = "") -> None:
        write_heartbeat(
            self._wr,
            self._role,
            status,
            note,
            self._instance,
            spawn_epoch=self._spawn_epoch,
        )

    @property
    def role(self) -> str:
        return self._role

    @property
    def instance(self) -> int:
        return self._instance

    # ------------------------------------------------------------------
    # Pull next eligible skill (find + claim in one operation)
    # ------------------------------------------------------------------

    def pull_skill(self, reserve: bool = False) -> dict:
        """Find and claim the next eligible skill for this agent's role."""
        board = load_board(self._workspace)
        kb = self._resolve_kb(board)
        active = [Ticket.from_dict(t) for t in board.get("active", [])]

        if is_manual_mode(board):
            resume = self._resume_existing_claim(kb, active)
            if resume is not None:
                return resume
            return {"action": "none", "reason": "manual_mode_await_operator_drop"}

        in_progress = count_in_progress_for_role(active, self._role)
        capacity = self._role_capacity(board, kb)
        if in_progress >= capacity:
            resume = self._resume_existing_claim(kb, active)
            if resume is not None:
                return resume
            return {"action": "none", "reason": "wip_cap_reached"}

        match = kb.find_next_eligible(active, self._role)
        if match is None:
            resume = self._resume_existing_claim(kb, active)
            if resume is not None:
                return resume
            return {"action": "none", "reason": "no_eligible_skill"}

        ticket, skill, _stage_def = match
        return self.claim_skill(ticket.ticket_id, skill, reserve=reserve)

    # ------------------------------------------------------------------
    # Claim a specific skill on a ticket
    # ------------------------------------------------------------------

    def claim_next_intent(self) -> dict:
        """Start work from the oldest operator drop for this role (manual mode only)."""
        board = load_board(self._workspace)
        if not is_manual_mode(board):
            return {"action": "none", "reason": "not_manual_mode"}

        kb = self._resolve_kb(board)
        active = [Ticket.from_dict(t) for t in board.get("active", [])]
        resume = self._resume_existing_claim(kb, active)
        if resume is not None:
            return resume

        wr = war_room_dir(self._workspace)
        intent = find_first_intent_for_role(wr, self._role)
        if intent is None:
            return {"action": "none", "reason": "no_pending_intent"}

        return self.claim_skill(intent.ticket_id, intent.skill)

    def _matching_intent(self, ticket_id: str, skill: str) -> ActionIntent | None:
        wr = war_room_dir(self._workspace)
        try:
            intents = load_action_intents(wr)
        except NoActionStateFileError:
            return None
        for intent in intents:
            if (
                intent.ticket_id == ticket_id
                and intent.skill == skill
                and intent.agent_role == self._role
            ):
                return intent
        return None

    def claim_skill(self, ticket_id: str, skill: str, reserve: bool = False) -> dict:
        """Claim a skill on a ticket, setting it to in_progress."""
        board = load_board(self._workspace)
        found = find_ticket_in_board(board, ticket_id)
        if found is None:
            raise TicketNotFoundError(f"Ticket not found: {ticket_id}")

        bucket, index, ticket = found
        # Manual mode operator drops can target backlog children. Promote to active
        # before claiming so fixture apply/claim resolution sees the in-progress work.
        if is_manual_mode(board) and bucket == "backlog":
            backlog = board.get("backlog", [])
            raw = backlog.pop(index)
            active = board.setdefault("active", [])
            active.append(raw)
            bucket = "active"
            index = len(active) - 1
            ticket = Ticket.from_dict(raw)
        sp = ticket.skill_progress.get(skill)

        if is_manual_mode(board):
            if (
                sp is not None
                and sp.execution_status == "in_progress"
                and sp.agent == self._role
            ):
                self._heartbeat("working", f"resume {skill} on {ticket_id}")
                return {
                    "action": "resume",
                    "ticket_id": ticket_id,
                    "skill": skill,
                    "stage": ticket.stage,
                    "role": self._role,
                    "instance": self._instance,
                }
            intent = self._matching_intent(ticket_id, skill)
            if intent is None:
                return {"action": "none", "reason": "manual_mode_await_operator_drop"}
            if sp is not None and sp.execution_status == "done":
                remove_action_intent(war_room_dir(self._workspace), intent)
                raise SkillAlreadyDoneError(f"Skill {skill} already done on {ticket_id}")
            if sp is not None and sp.execution_status == "in_progress":
                if sp.agent != self._role:
                    return {"action": "none", "reason": "skill_in_progress_by_other_role"}
                remove_action_intent(war_room_dir(self._workspace), intent)
                self._heartbeat("working", f"resume {skill} on {ticket_id}")
                return {
                    "action": "resume",
                    "ticket_id": ticket_id,
                    "skill": skill,
                    "stage": ticket.stage,
                    "role": self._role,
                    "instance": self._instance,
                }
            remove_action_intent(war_room_dir(self._workspace), intent)
        elif sp is not None and sp.execution_status == "in_progress":
            if sp.agent == self._role:
                self._heartbeat("working", f"resume {skill} on {ticket_id}")
                return {"action": "already_claimed", "ticket_id": ticket_id, "skill": skill}
            raise SkillAlreadyInProgressError(
                f"Skill {skill} already in_progress by {sp.agent}"
            )
        if sp is not None and sp.execution_status == "done":
            raise SkillAlreadyDoneError(f"Skill {skill} already done on {ticket_id}")

        now = now_iso()
        ticket.skill_progress[skill] = SkillProgress(
            execution_status="in_progress",
            agent=self._role,
            start=now,
            review_status="not_started",
        )
        save_ticket_in_board(board, bucket, index, ticket)
        save_board(self._workspace, board)

        hb_status = "reserved" if reserve else "working"
        self._heartbeat(hb_status, f"in_progress {skill} on {ticket_id}")
        append_metrics_log(self._workspace, {
            "event": "skill_claim",
            "agent_role": self._role,
            "instance": self._instance,
            "ticket_id": ticket_id,
            "skill": skill,
            "stage": ticket.stage,
        })

        return {
            "action": "claimed",
            "ticket_id": ticket_id,
            "skill": skill,
            "stage": ticket.stage,
            "role": self._role,
            "instance": self._instance,
        }

    # ------------------------------------------------------------------
    # Complete a skill (two-pass: work done → review in progress → review done)
    # ------------------------------------------------------------------

    def complete_skill(self, ticket_id: str, skill: str, notes: str | None = None) -> dict:
        """Advance skill completion by one pass (work or review).

        First call while execution is in_progress: execution done, review in_progress.
        Second call while review is in_progress: review done (skill fully complete).
        """
        board = load_board(self._workspace)
        found = find_ticket_in_board(board, ticket_id)
        if found is None:
            raise TicketNotFoundError(f"Ticket not found: {ticket_id}")

        bucket, index, ticket = found
        sp = ticket.skill_progress.get(skill)
        if sp is None:
            sp = SkillProgress()
            ticket.skill_progress[skill] = sp

        if sp.execution_status == "done" and sp.review_status == "done":
            raise SkillAlreadyDoneError(f"Skill {skill} already done on {ticket_id}")

        if sp.execution_status == "in_progress":
            return self._complete_work_pass(board, bucket, index, ticket, skill, sp, notes)
        if sp.execution_status == "done" and sp.review_status == "in_progress":
            return self._complete_review_pass(board, bucket, index, ticket, skill, sp, notes)

        if sp.execution_status == "done" and sp.review_status in (None, "not_started"):
            now = now_iso()
            sp.review_status = "in_progress"
            sp.reviewer = self._role
            sp.review_start = now
            save_ticket_in_board(board, bucket, index, ticket)
            save_board(self._workspace, board)
            self._heartbeat("working", f"review {skill} on {ticket_id}")
            return {
                "action": "review_started",
                "ticket_id": ticket_id,
                "skill": skill,
                "stage": ticket.stage,
            }

        raise SkillAlreadyDoneError(
            f"Cannot complete skill {skill} on {ticket_id}: "
            f"execution={sp.execution_status!r} review={sp.review_status!r}",
        )

    def _complete_work_pass(
        self,
        board: dict,
        bucket: str,
        index: int,
        ticket: Ticket,
        skill: str,
        sp: SkillProgress,
        notes: str | None,
    ) -> dict:
        now = now_iso()
        sp.execution_status = "done"
        sp.agent = self._role
        sp.end = now
        sp.review_status = "in_progress"
        sp.reviewer = self._role
        sp.review_start = now
        if notes:
            sp.notes = notes

        save_ticket_in_board(board, bucket, index, ticket)
        save_board(self._workspace, board)

        self._heartbeat("working", f"work done {skill} on {ticket.ticket_id}")
        append_metrics_log(self._workspace, {
            "event": "skill_work_done",
            "agent_role": self._role,
            "instance": self._instance,
            "ticket_id": ticket.ticket_id,
            "skill": skill,
            "stage": ticket.stage,
        })
        return {
            "action": "work_done",
            "ticket_id": ticket.ticket_id,
            "skill": skill,
            "stage": ticket.stage,
        }

    def _complete_review_pass(
        self,
        board: dict,
        bucket: str,
        index: int,
        ticket: Ticket,
        skill: str,
        sp: SkillProgress,
        notes: str | None,
    ) -> dict:
        now = now_iso()
        sp.review_status = "done"
        sp.reviewer = sp.reviewer or self._role
        sp.review_end = now
        if notes:
            sp.notes = notes

        save_ticket_in_board(board, bucket, index, ticket)
        save_board(self._workspace, board)

        self._heartbeat("working", f"done {skill} on {ticket.ticket_id}")
        append_metrics_log(self._workspace, {
            "event": "skill_done",
            "agent_role": self._role,
            "instance": self._instance,
            "ticket_id": ticket.ticket_id,
            "skill": skill,
            "stage": ticket.stage,
        })
        return {
            "action": "completed",
            "ticket_id": ticket.ticket_id,
            "skill": skill,
            "stage": ticket.stage,
        }

    # ------------------------------------------------------------------
    # Signal readiness (no eligible work)
    # ------------------------------------------------------------------

    def signal_ready(self, reason: str = "no_eligible_skill_on_active_tickets") -> dict:
        """Write ready heartbeat only after releasing any own in_progress claims."""
        released = self.release_own_in_progress_claims(reason)
        self._heartbeat("ready", reason)
        append_metrics_log(self._workspace, {
            "event": "agent_ready",
            "agent_role": self._role,
            "instance": self._instance,
            "reason": reason,
            "released_claims": released,
        })
        return {
            "action": "ready",
            "role": self._role,
            "instance": self._instance,
            "reason": reason,
            "released_claims": released,
        }

    def release_own_in_progress_claims(self, reason: str) -> list[dict[str, str]]:
        """Drop in_progress board claims owned by this role before going idle."""
        board = load_board(self._workspace)
        active = board.get("active", [])
        released: list[dict[str, str]] = []
        changed = False

        for index, raw in enumerate(active):
            ticket = Ticket.from_dict(raw)
            ticket_released: list[str] = []
            for skill_id, sp in list(ticket.skill_progress.items()):
                if sp.agent != self._role or sp.execution_status != "in_progress":
                    continue
                del ticket.skill_progress[skill_id]
                ticket_released.append(skill_id)
            if not ticket_released:
                continue
            for skill_id in ticket_released:
                entry = {
                    "ticket_id": ticket.ticket_id,
                    "skill": skill_id,
                    "stage": ticket.stage,
                }
                released.append(entry)
                append_metrics_log(self._workspace, {
                    "event": "claim_released_self",
                    "agent_role": self._role,
                    "instance": self._instance,
                    "reason": reason,
                    **entry,
                })
            save_ticket_in_board(board, "active", index, ticket)
            changed = True

        if changed:
            save_board(self._workspace, board)
        return released

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resume_existing_claim(self, kb: KanbanBoard, active: list[Ticket]) -> dict | None:
        claims = kb.in_progress_claims_for_role(active, self._role)
        if not claims:
            return None
        ticket, skill = claims[0]
        self._heartbeat("working", f"resume {skill} on {ticket.ticket_id}")
        append_metrics_log(self._workspace, {
            "event": "skill_resume",
            "agent_role": self._role,
            "instance": self._instance,
            "ticket_id": ticket.ticket_id,
            "skill": skill,
            "stage": ticket.stage,
        })
        return {
            "action": "resume",
            "ticket_id": ticket.ticket_id,
            "skill": skill,
            "stage": ticket.stage,
            "role": self._role,
            "instance": self._instance,
        }

    def _resolve_kb(self, board: dict) -> KanbanBoard:
        config_name = board.get("stage_configuration") or board.get("system_of_work", "")
        kb_map = load_kanban_board(self._workspace)
        kb = kb_map.get(config_name)
        if kb is None:
            raise SystemExit(f"Unknown stage_configuration: {config_name}")
        return kb

    def _role_capacity(self, board: dict, kb: KanbanBoard) -> int:
        """Return team capacity for this agent's role (WIP cap)."""
        team = board.get("team") or board.get("wip_policy") or {}
        if team:
            return int(team.get(self._role, 3))
        config_name = board.get("stage_configuration") or board.get("system_of_work", "")
        wr = war_room_dir(self._workspace)
        kanban_path = wr / "kanban.json"
        if kanban_path.is_file():
            import json as _json
            raw = _json.loads(kanban_path.read_text(encoding="utf-8"))
            kb_block = raw.get("definitions", {}).get(config_name, {})
            team = kb_block.get("team") or {}
        return int(team.get(self._role, 3)) if team else 3


class TeamMemberAgent(Agent):
    """domain model Team Member: Agent — delivery role, work role, active ticket, skill.

    Extends Agent with explicit role/work-role semantics from the domain model.
    """

    def __init__(
        self,
        workspace: Path,
        delivery_role: str,
        work_role: str = "executor",
        instance: int = 1,
    ) -> None:
        super().__init__(workspace, delivery_role, instance)
        self._work_role = work_role

    @property
    def delivery_role(self) -> str:
        return self._role

    @property
    def work_role(self) -> str:
        return self._work_role

    def work_on_ticket(self, ticket_id: str, skill: str, reserve: bool = False) -> dict:
        """domain model: work on ticket with skill — executor claims and starts work."""
        return self.claim_skill(ticket_id, skill, reserve=reserve)

    def review_ticket_work(self, ticket_id: str, skill: str, notes: str | None = None) -> dict:
        """domain model: review ticket work from skill."""
        return self.complete_skill(ticket_id, skill, notes)

    def write_heartbeat(self, status: str, note: str = "") -> None:
        """domain model: write heartbeat → Heartbeat."""
        self._heartbeat(status, note)

    # ------------------------------------------------------------------
    # Fixture mode — work on ticket in E2E / stub workspace
    # ------------------------------------------------------------------

    def is_fixture_mode(self) -> bool:
        """Return True when this workspace is running in fixture mode."""
        return is_fixture_mode(self._workspace)

    def find_in_progress_claim(self) -> tuple[str, str] | None:
        """Return (ticket_id, skill) if this role has an in_progress claim, else None."""
        board = load_board(self._workspace)
        config_name = board.get("stage_configuration") or board.get("system_of_work", "")
        kb_map = load_kanban_board(self._workspace)
        kb = kb_map.get(config_name)
        if kb is None:
            return None
        active = [Ticket.from_dict(t) for t in board.get("active", [])]
        claims = kb.in_progress_claims_for_role(active, self._role)
        if not claims:
            return None
        ticket, skill = claims[0]
        return ticket.ticket_id, skill

    def apply_skill_fixture(
        self,
        ticket_id: str,
        skill: str,
    ) -> dict:
        """Copy skill fixture files into workspace and mark skill done (fixture mode only)."""
        if not self.is_fixture_mode():
            raise RuntimeError(f"fixture_mode is not active for workspace {self._workspace}")

        board = load_board(self._workspace)
        match = find_ticket_in_board(board, ticket_id)
        if match is None:
            raise ValueError(f"Ticket not found: {ticket_id}")
        _, _, ticket = match
        ticket_obj = Ticket.from_dict(ticket) if isinstance(ticket, dict) else ticket

        fixtures = self._load_fixtures_index()
        entry = self._pick_fixture_entry(fixtures, skill, ticket_obj.scope_level)

        copied = self._copy_fixture_files(entry)
        post_copy_results: list[dict] = []
        if entry.get("post_copy"):
            post_copy_results = self._run_post_copy(entry["post_copy"])

        notes = "fixture_mode: copied from skill-fixtures"
        complete1 = self.complete_skill(ticket_id, skill, notes)
        complete2 = self.complete_skill(ticket_id, skill, notes)

        event = {
            "event": "skill_fixture_applied",
            "ts": now_iso(),
            "ticket_id": ticket_id,
            "skill": skill,
            "agent_role": self._role,
            "instance": self._instance,
            "scope_level": ticket_obj.scope_level,
            "copies": copied,
            "post_copy": post_copy_results,
            "complete": [complete1.get("action"), complete2.get("action")],
        }
        append_metrics_log(self._workspace, event)
        return event

    def _load_fixtures_index(self) -> dict:
        path = self._workspace / "skill-fixtures.json"
        if not path.is_file():
            raise FileNotFoundError(f"skill-fixtures.json not found at {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _pick_fixture_entry(fixtures: dict, skill: str, scope_level: str) -> dict:
        skill_entries = fixtures.get("fixtures", {}).get(skill)
        if not skill_entries:
            raise KeyError(f"No fixture entry for skill {skill!r}")
        scope_key = f"scope_{scope_level}"
        if scope_key in skill_entries:
            return skill_entries[scope_key]
        if "default" in skill_entries:
            return skill_entries["default"]
        for key, entry in skill_entries.items():
            if not key.startswith("scope_"):
                return entry
        raise KeyError(f"No fixture variant for skill {skill!r} scope {scope_level!r}")

    def _copy_fixture_files(self, entry: dict) -> list[dict]:
        copied: list[dict] = []
        for item in entry.get("copies", []):
            src = self._workspace / item["source"]
            dst = self._workspace / item["target"]
            if not src.is_file():
                raise FileNotFoundError(f"Fixture source missing: {src}")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append({"source": item["source"], "target": item["target"]})
        return copied

    def _run_post_copy(self, commands: list[str]) -> list[dict]:
        cwd = self._workspace if self._workspace.is_dir() else Path(__file__).resolve().parents[5]
        results: list[dict] = []
        for cmd in commands:
            proc = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
            results.append({
                "command": cmd,
                "returncode": proc.returncode,
                "stdout": proc.stdout[-500:] if proc.stdout else "",
                "stderr": proc.stderr[-500:] if proc.stderr else "",
            })
            if proc.returncode != 0:
                raise RuntimeError(f"post_copy failed ({proc.returncode}): {cmd}\n{proc.stderr}")
        return results
