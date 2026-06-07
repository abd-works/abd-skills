"""Operate Board in Manual Mode — shared GWT helpers.

Reusable Given/When/Then helpers for both sub-epics:
  - Switch Board Mode
  - Assign Team Member Agent to Ticket
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from action_state import (
    ACTION_STATE_FILENAME,
    ActionIntent,
    append_action_intent,
    load_action_intents,
)
from board_mode import (
    BOARD_MODE_AUTOMATIC,
    BOARD_MODE_MANUAL,
    InvalidBoardModeError,
    is_manual_mode,
    read_board_mode,
    set_board_mode,
)
from delivery_model import (
    KanbanBoard,
    SkillDef,
    SkillProgress,
    StageDef,
    Ticket,
    load_board,
    save_board,
    war_room_dir,
)
from kanban_lead import KanbanLead


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    return tmp_path


# ============================================================================
# GIVEN helpers
# ============================================================================

def given_kanban_board(ws: Path, config: dict) -> KanbanLead:
    """Set up kanban.json with the supplied stage configuration."""
    wr = ws / "docs" / "planning" / "kanban"
    wr.mkdir(parents=True, exist_ok=True)
    (wr / "kanban.json").write_text(
        json.dumps({"definitions": {"test": config}}),
        encoding="utf-8",
    )
    return KanbanLead(ws)


def given_board_state(ws: Path, board: dict) -> None:
    """Write a board.json with sensible defaults merged with supplied data."""
    board.setdefault("schema", "abd-delivery-kanban/v2")
    board.setdefault("stage_configuration", "test")
    board.setdefault("backlog", [])
    board.setdefault("active", [])
    board.setdefault("done", [])
    board.setdefault("archived", [])
    save_board(ws, board)


def given_ticket(
    ticket_id: str, stage: str, scope_level: str, priority: int = 1, **kwargs
) -> Ticket:
    """Create a Ticket with domain defaults."""
    return Ticket(
        ticket_id=ticket_id,
        lineage=kwargs.get("lineage", ["Project", ticket_id]),
        scope_level=scope_level,
        stage=stage,
        priority=priority,
        skill_progress=kwargs.get("skill_progress", {}),
        entered_stage=kwargs.get("entered_stage"),
        scatter_from=kwargs.get("scatter_from"),
        scatter_to=kwargs.get("scatter_to", []),
    )


def given_board_mode_is(ws: Path, mode: str) -> None:
    """Set board_mode on an existing board.json."""
    board = load_board(ws)
    set_board_mode(board, mode)
    save_board(ws, board)


def given_action_intent(
    ticket_id: str, skill: str, agent_role: str
) -> ActionIntent:
    """Create an ActionIntent with the required fields."""
    return ActionIntent(
        ticket_id=ticket_id, skill=skill, agent_role=agent_role
    )


def given_action_intent_appended(
    ws: Path, ticket_id: str, skill: str, agent_role: str
) -> None:
    """Append an action intent to action-state.json."""
    wr = war_room_dir(ws)
    intent = given_action_intent(ticket_id, skill, agent_role)
    append_action_intent(wr, intent)


def given_no_action_state_file(ws: Path) -> None:
    """Ensure action-state.json does not exist."""
    wr = war_room_dir(ws)
    path = wr / ACTION_STATE_FILENAME
    if path.is_file():
        path.unlink()


def given_skill_not_started(skill: str, role: str) -> SkillProgress:
    return SkillProgress(execution_status="not_started", review_status="not_started")


def given_skill_execution_in_progress(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="in_progress",
        agent=role,
        start="2026-01-01T00:00:00+00:00",
        review_status="not_started",
    )


def given_skill_execution_done(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="done",
        agent=role,
        start="2026-01-01T00:00:00+00:00",
        end="2026-01-01T01:00:00+00:00",
        review_status="not_started",
    )


def given_skill_review_in_progress(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="done",
        agent=role,
        start="2026-01-01T00:00:00+00:00",
        end="2026-01-01T01:00:00+00:00",
        review_status="in_progress",
        reviewer=role,
        review_start="2026-01-01T01:00:00+00:00",
    )


def given_skill_fully_done(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="done",
        agent=role,
        start="2026-01-01T00:00:00+00:00",
        end="2026-01-01T01:00:00+00:00",
        review_status="done",
        reviewer=role,
        review_start="2026-01-01T01:00:00+00:00",
        review_end="2026-01-01T02:00:00+00:00",
    )


def given_skill_review_failed(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="not_started",
        agent=role,
        review_status="failed",
        reviewer=role,
    )


def given_stage_config_with_skills(skills: list[dict]) -> dict:
    """Build a single-stage configuration dict for kanban.json."""
    return {
        "stages": [
            {
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": skills,
            }
        ],
    }


# ============================================================================
# WHEN helpers
# ============================================================================

def when_board_mode_set(board: dict, mode: str) -> dict:
    """Set board mode on in-memory board dict. Returns updated board."""
    return set_board_mode(board, mode)


def when_board_mode_read(board: dict) -> str:
    """Read board mode from in-memory board dict."""
    return read_board_mode(board)


def when_board_mode_persisted(ws: Path, mode: str) -> None:
    """Set mode and persist to disk."""
    board = load_board(ws)
    set_board_mode(board, mode)
    save_board(ws, board)


def when_board_reloaded(ws: Path) -> dict:
    """Reload board from disk."""
    return load_board(ws)


def when_action_intent_appended(ws: Path, intent: ActionIntent) -> None:
    """Append intent to the action state file."""
    wr = war_room_dir(ws)
    append_action_intent(wr, intent)


def when_action_intents_loaded(ws: Path) -> list[ActionIntent]:
    """Load all unprocessed intents from the action state file."""
    wr = war_room_dir(ws)
    return load_action_intents(wr)


# ============================================================================
# THEN helpers
# ============================================================================

def then_board_mode_is(board: dict, expected_mode: str) -> None:
    """Assert board_mode equals expected value."""
    actual = read_board_mode(board)
    assert actual == expected_mode, f"Expected mode '{expected_mode}', got '{actual}'"


def then_board_is_manual(board: dict) -> None:
    assert is_manual_mode(board), "Expected manual mode but board is automatic"


def then_board_is_automatic(board: dict) -> None:
    assert not is_manual_mode(board), "Expected automatic mode but board is manual"


def then_persisted_mode_is(ws: Path, expected_mode: str) -> None:
    """Reload board from disk and assert mode."""
    board = load_board(ws)
    then_board_mode_is(board, expected_mode)


def then_other_fields_unchanged(board_before: dict, board_after: dict) -> None:
    """Assert no fields other than board_mode and synced_at changed."""
    ignore = {"board_mode", "synced_at"}
    for key in set(board_before.keys()) | set(board_after.keys()):
        if key in ignore:
            continue
        assert board_before.get(key) == board_after.get(key), (
            f"Field '{key}' changed: {board_before.get(key)} -> {board_after.get(key)}"
        )


def then_action_state_file_exists(ws: Path) -> None:
    wr = war_room_dir(ws)
    path = wr / ACTION_STATE_FILENAME
    assert path.is_file(), f"action-state.json not found at {path}"


def then_intent_count_is(ws: Path, expected: int) -> None:
    wr = war_room_dir(ws)
    intents = load_action_intents(wr)
    assert len(intents) == expected, f"Expected {expected} intents, got {len(intents)}"


def then_intent_matches(
    intent: ActionIntent, ticket_id: str, skill: str, agent_role: str
) -> None:
    assert intent.ticket_id == ticket_id, (
        f"Intent ticket_id: expected '{ticket_id}', got '{intent.ticket_id}'"
    )
    assert intent.skill == skill, (
        f"Intent skill: expected '{skill}', got '{intent.skill}'"
    )
    assert intent.agent_role == agent_role, (
        f"Intent agent_role: expected '{agent_role}', got '{intent.agent_role}'"
    )


def then_ticket_stage_is(ws: Path, ticket_id: str, expected_stage: str) -> None:
    """Assert a ticket is at the expected stage on disk."""
    board = load_board(ws)
    for bucket in ("active", "backlog", "done"):
        for raw in board.get(bucket, []):
            if raw.get("ticket_id") == ticket_id:
                assert raw["stage"] == expected_stage, (
                    f"Ticket '{ticket_id}' stage: expected '{expected_stage}', "
                    f"got '{raw['stage']}'"
                )
                return
    raise AssertionError(f"Ticket '{ticket_id}' not found on board")


def then_ticket_is_active(ws: Path, ticket_id: str) -> None:
    board = load_board(ws)
    active_ids = {t["ticket_id"] for t in board.get("active", [])}
    assert ticket_id in active_ids, f"{ticket_id} not in active: {active_ids}"


def then_ticket_is_in_backlog(ws: Path, ticket_id: str) -> None:
    board = load_board(ws)
    backlog_ids = {t["ticket_id"] for t in board.get("backlog", [])}
    assert ticket_id in backlog_ids, f"{ticket_id} not in backlog: {backlog_ids}"


def then_skill_execution_status_is(
    ws: Path, ticket_id: str, skill: str, expected_status: str
) -> None:
    board = load_board(ws)
    for bucket in ("active", "backlog", "done"):
        for raw in board.get(bucket, []):
            if raw.get("ticket_id") == ticket_id:
                sp = raw.get("skill_progress", {}).get(skill, {})
                actual = sp.get("execution_status", "not_started")
                assert actual == expected_status, (
                    f"Ticket '{ticket_id}' skill '{skill}' execution_status: "
                    f"expected '{expected_status}', got '{actual}'"
                )
                return
    raise AssertionError(f"Ticket '{ticket_id}' not found on board")


def then_skill_review_status_is(
    ws: Path, ticket_id: str, skill: str, expected_status: str
) -> None:
    board = load_board(ws)
    for bucket in ("active", "backlog", "done"):
        for raw in board.get(bucket, []):
            if raw.get("ticket_id") == ticket_id:
                sp = raw.get("skill_progress", {}).get(skill, {})
                actual = sp.get("review_status", "not_started")
                assert actual == expected_status, (
                    f"Ticket '{ticket_id}' skill '{skill}' review_status: "
                    f"expected '{expected_status}', got '{actual}'"
                )
                return
    raise AssertionError(f"Ticket '{ticket_id}' not found on board")


def then_all_skills_fully_done(ws: Path, ticket_id: str, skills: list[str]) -> None:
    board = load_board(ws)
    for bucket in ("active", "backlog", "done"):
        for raw in board.get(bucket, []):
            if raw.get("ticket_id") == ticket_id:
                sp_map = raw.get("skill_progress", {})
                for skill in skills:
                    sp = sp_map.get(skill, {})
                    assert sp.get("execution_status") == "done", (
                        f"Skill '{skill}' execution_status not done"
                    )
                    assert sp.get("review_status") == "done", (
                        f"Skill '{skill}' review_status not done"
                    )
                return
    raise AssertionError(f"Ticket '{ticket_id}' not found on board")
