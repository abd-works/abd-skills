"""
agent.py

Domain area   : Agent and Skills — Agent
Responsibilities: start work on skill, drive skill to done, write heartbeat
"""
from __future__ import annotations

import json
from pathlib import Path

from delivery_model import (
    KanbanBoard,
    SkillProgress,
    StageDef,
    Ticket,
    append_metrics_log,
    count_in_progress_for_role,
    find_ticket_in_board,
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

    def claim_skill(self, ticket_id: str, skill: str, reserve: bool = False) -> dict:
        """Claim a skill on a ticket, setting it to in_progress."""
        board = load_board(self._workspace)
        found = find_ticket_in_board(board, ticket_id)
        if found is None:
            raise TicketNotFoundError(f"Ticket not found: {ticket_id}")

        bucket, index, ticket = found
        sp = ticket.skill_progress.get(skill)

        if sp is not None and sp.execution_status == "in_progress":
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
