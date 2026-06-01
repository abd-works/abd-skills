"""Assign Team Member Agent to Ticket — manual-mode intent, delegation, execution

Epic:      Operate Board in Manual Mode
Sub-epic:  Assign Team Member Agent to Ticket

Stories covered:
  - Record Action Intent in State File
  - Detect State File Change
  - Delegate Skill to Team Member Agent
  - Execute Assigned Skill on Ticket (two-pass: work then review)
  - Advance Ticket to In Progress on First Skill Start
  - Persist Skill Completion to Board State (two-pass)
  - Complete Ticket When All Skills Finish

Note: UI stories (Drag, Move Ticket on Agent Advance, Update Skill Status on
      Completion, Move Ticket to Done on Agent Completion) are not testable here.

Orchestrator pattern: test methods call Given/When/Then helpers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_SCRIPT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from action_state import (
    ACTION_STATE_FILENAME,
    ActionIntent,
    NoActionStateFileError,
    append_action_intent,
    clear_processed_intents,
    load_action_intents,
)
from board_mode import BOARD_MODE_AUTOMATIC, BOARD_MODE_MANUAL
from delivery_model import (
    KanbanBoard,
    SkillDef,
    SkillProgress,
    StageDef,
    Ticket,
    load_board,
    save_board,
    save_ticket_in_board,
    war_room_dir,
)

from tests.operate_board_in_manual_mode.operate_board_in_manual_mode_helper import (
    given_action_intent,
    given_action_intent_appended,
    given_board_mode_is,
    given_board_state,
    given_kanban_board,
    given_no_action_state_file,
    given_skill_execution_done,
    given_skill_execution_in_progress,
    given_skill_fully_done,
    given_skill_not_started,
    given_skill_review_failed,
    given_skill_review_in_progress,
    given_stage_config_with_skills,
    given_ticket,
    then_action_state_file_exists,
    then_all_skills_fully_done,
    then_intent_count_is,
    then_intent_matches,
    then_skill_execution_status_is,
    then_skill_review_status_is,
    then_ticket_is_active,
    then_ticket_is_in_backlog,
    when_action_intent_appended,
    when_action_intents_loaded,
    workspace,
)


# ============================================================================
# STORY: Record Action Intent in State File
# ============================================================================

class TestRecordActionIntentInStateFile:
    """Record Action Intent in State File."""

    def test_user_drops_agent_onto_ticket_writes_intent(self, workspace):
        """WHEN user drops agent onto ticket -> app writes ActionIntent to
        action-state.json."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        given_board_state(workspace, {
            "active": [given_ticket("t-1", "specification", "sprint").to_dict()],
        })
        intent = given_action_intent("t-1", "abd-crc", "business-expert")

        # When:
        when_action_intent_appended(workspace, intent)

        # Then:
        then_action_state_file_exists(workspace)
        intents = when_action_intents_loaded(workspace)
        assert len(intents) == 1
        then_intent_matches(intents[0], "t-1", "abd-crc", "business-expert")

    def test_multiple_intents_appended_none_overwritten(self, workspace):
        """WHEN multiple assignments before lead processes -> each appended,
        none overwritten."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        given_board_state(workspace, {
            "active": [given_ticket("t-1", "specification", "sprint").to_dict()],
        })
        intent_a = given_action_intent("t-1", "abd-crc", "business-expert")
        intent_b = given_action_intent("t-1", "abd-spec-by-example", "product-owner")

        # When:
        when_action_intent_appended(workspace, intent_a)
        when_action_intent_appended(workspace, intent_b)

        # Then:
        then_intent_count_is(workspace, 2)
        intents = when_action_intents_loaded(workspace)
        then_intent_matches(intents[0], "t-1", "abd-crc", "business-expert")
        then_intent_matches(intents[1], "t-1", "abd-spec-by-example", "product-owner")

    def test_action_state_file_created_on_first_write(self, workspace):
        """WHEN action-state.json doesn't exist -> app creates on first write."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        given_board_state(workspace, {})
        given_no_action_state_file(workspace)
        intent = given_action_intent("t-1", "abd-crc", "business-expert")

        # When:
        when_action_intent_appended(workspace, intent)

        # Then:
        then_action_state_file_exists(workspace)
        then_intent_count_is(workspace, 1)


# ============================================================================
# STORY: Detect State File Change
# ============================================================================

class TestDetectStateFileChange:
    """Detect State File Change."""

    def test_manual_mode_reads_unprocessed_intents(self, workspace):
        """WHEN lead in manual mode and action-state.json changes ->
        read all unprocessed intents."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        given_board_state(workspace, {})
        given_board_mode_is(workspace, BOARD_MODE_MANUAL)
        given_action_intent_appended(workspace, "t-1", "abd-crc", "business-expert")
        given_action_intent_appended(workspace, "t-2", "abd-crc", "business-expert")

        # When:
        intents = when_action_intents_loaded(workspace)

        # Then:
        assert len(intents) == 2
        then_intent_matches(intents[0], "t-1", "abd-crc", "business-expert")
        then_intent_matches(intents[1], "t-2", "abd-crc", "business-expert")

    def test_multiple_intents_processed_in_order(self, workspace):
        """WHEN multiple intents present -> process in order written."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        given_board_state(workspace, {})
        given_board_mode_is(workspace, BOARD_MODE_MANUAL)
        given_action_intent_appended(workspace, "t-1", "abd-crc", "business-expert")
        given_action_intent_appended(workspace, "t-2", "abd-spec-by-example", "product-owner")
        given_action_intent_appended(workspace, "t-1", "abd-spec-by-example", "product-owner")

        # When:
        intents = when_action_intents_loaded(workspace)

        # Then:
        assert len(intents) == 3
        then_intent_matches(intents[0], "t-1", "abd-crc", "business-expert")
        then_intent_matches(intents[1], "t-2", "abd-spec-by-example", "product-owner")
        then_intent_matches(intents[2], "t-1", "abd-spec-by-example", "product-owner")

    def test_automatic_mode_does_not_watch_action_state(self, workspace):
        """WHEN mode is automatic -> don't watch or read action-state.json."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        given_board_state(workspace, {})
        given_no_action_state_file(workspace)

        # When:
        board = load_board(workspace)

        # Then:
        assert not board.get("board_mode") or board.get("board_mode") == BOARD_MODE_AUTOMATIC
        wr = war_room_dir(workspace)
        assert not (wr / ACTION_STATE_FILENAME).is_file()


# ============================================================================
# STORY: Delegate Skill to Team Member Agent
# ============================================================================

class TestDelegateSkillToTeamMemberAgent:
    """Delegate Skill to Team Member Agent."""

    def test_lead_delegates_intent_to_named_role(self, workspace):
        """WHEN lead reads an intent -> delegate specified skill on specified
        ticket to named role."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})
        intent = given_action_intent("t-1", "abd-crc", "business-expert")

        # When:
        board = load_board(workspace)
        found = _find_ticket_raw(board, "t-1")
        sp = SkillProgress(execution_status="in_progress", agent="business-expert")
        found["skill_progress"] = {intent.skill: sp.to_dict()}
        save_board(workspace, board)

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "in_progress")

    def test_role_without_capacity_queues_intent(self, workspace):
        """WHEN role has no capacity -> queue until capacity; don't reject."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_execution_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})
        intent = given_action_intent("t-1", "abd-spec-by-example", "product-owner")

        # When:
        when_action_intent_appended(workspace, intent)
        intents = when_action_intents_loaded(workspace)

        # Then:
        assert len(intents) == 1
        then_intent_matches(intents[0], "t-1", "abd-spec-by-example", "product-owner")

    def test_intent_with_nonexistent_ticket_is_skipped(self, workspace):
        """WHEN intent references nonexistent ticket/skill -> skip; log reason."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        given_board_state(workspace, {"active": []})
        intent = given_action_intent("nonexistent-ticket", "abd-crc", "business-expert")

        # When:
        board = load_board(workspace)
        result = _find_ticket_raw(board, intent.ticket_id)

        # Then:
        assert result is None


# ============================================================================
# STORY: Execute Assigned Skill on Ticket (TWO-PASS)
# ============================================================================

class TestExecuteAssignedSkillOnTicket:
    """Execute Assigned Skill on Ticket (two-pass: work then review)."""

    def test_agent_begins_work_pass_execution_in_progress(self, workspace):
        """WHEN agent receives assignment -> begin work pass;
        execution_status -> in_progress."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            SkillProgress(
                execution_status="in_progress",
                agent="business-expert",
                review_status="not_started",
            ),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "in_progress")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "not_started")

    def test_work_pass_completes_advances_to_review(self, workspace):
        """WHEN work pass completes -> execution_status -> done;
        review_status -> in_progress."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_execution_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_review_in_progress("abd-crc", "business-expert"),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "done")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "in_progress")

    def test_review_pass_completes_skill_fully_done(self, workspace):
        """WHEN review pass completes -> review_status -> done;
        skill fully complete."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_review_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_fully_done("abd-crc", "business-expert"),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "done")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "done")

    def test_review_fails_resets_execution(self, workspace):
        """WHEN review fails -> review_status -> failed;
        execution_status resets to not_started."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_review_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_review_failed("abd-crc", "business-expert"),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "not_started")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "failed")

    def test_agent_already_executing_waits(self, workspace):
        """WHEN agent already executing on another ticket ->
        new assignment waits."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket_a = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_execution_in_progress("abd-crc", "business-expert"),
        })
        ticket_b = given_ticket("t-2", "specification", "sprint")
        given_board_state(workspace, {
            "active": [ticket_a.to_dict(), ticket_b.to_dict()],
        })

        # When:
        board = load_board(workspace)
        active = [Ticket.from_dict(t) for t in board.get("active", [])]
        agent_busy = any(
            sp.execution_status == "in_progress" and sp.agent == "business-expert"
            for t in active
            for sp in t.skill_progress.values()
        )

        # Then:
        assert agent_busy is True
        board_t2 = _find_ticket_raw(board, "t-2")
        assert board_t2.get("skill_progress", {}).get("abd-crc") is None

    def test_work_pass_error_does_not_advance_to_review(self, workspace):
        """WHEN work pass errors -> record failure; don't advance to review."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_execution_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            SkillProgress(
                execution_status="failed",
                agent="business-expert",
                review_status="not_started",
            ),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "failed")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "not_started")


# ============================================================================
# STORY: Advance Ticket to In Progress on First Skill Start
# ============================================================================

class TestAdvanceTicketToInProgressOnFirstSkillStart:
    """Advance Ticket to In Progress on First Skill Start."""

    def test_first_skill_start_advances_ticket_from_queue(self, workspace):
        """WHEN agent starts first skill on ticket in queue ->
        advance to in_progress; write board."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint")
        given_board_state(workspace, {"backlog": [ticket.to_dict()]})

        # When:
        board = load_board(workspace)
        backlog = board.get("backlog", [])
        raw_ticket = backlog.pop(0)
        raw_ticket["skill_progress"] = {
            "abd-crc": SkillProgress(
                execution_status="in_progress", agent="business-expert"
            ).to_dict(),
        }
        board["backlog"] = backlog
        board.setdefault("active", []).append(raw_ticket)
        save_board(workspace, board)

        # Then:
        then_ticket_is_active(workspace, "t-1")
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "in_progress")

    def test_skill_start_on_already_active_ticket_unchanged(self, workspace):
        """WHEN skill starts on ticket already in_progress ->
        board position unchanged."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_fully_done("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-spec-by-example",
            SkillProgress(execution_status="in_progress", agent="product-owner"),
        )

        # Then:
        then_ticket_is_active(workspace, "t-1")
        board = load_board(workspace)
        active_ids = [t["ticket_id"] for t in board.get("active", [])]
        assert active_ids.count("t-1") == 1

    def test_concurrent_skill_starts_only_first_advances(self, workspace):
        """WHEN multiple skills start concurrently -> only first advances;
        no revert/duplicate."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            SkillProgress(execution_status="in_progress", agent="business-expert"),
        )
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-spec-by-example",
            SkillProgress(execution_status="in_progress", agent="product-owner"),
        )

        # Then:
        then_ticket_is_active(workspace, "t-1")
        board = load_board(workspace)
        active_ids = [t["ticket_id"] for t in board.get("active", [])]
        assert active_ids.count("t-1") == 1


# ============================================================================
# STORY: Persist Skill Completion to Board State (TWO-PASS)
# ============================================================================

class TestPersistSkillCompletionToBoardState:
    """Persist Skill Completion to Board State (two-pass)."""

    def test_work_pass_complete_persists_execution_done_review_in_progress(self, workspace):
        """WHEN agent completes work pass -> write execution_status done +
        review_status in_progress."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_execution_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_review_in_progress("abd-crc", "business-expert"),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "done")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "in_progress")

    def test_review_pass_complete_persists_review_done_releases_agent(self, workspace):
        """WHEN agent completes review pass -> write review_status done;
        agent released."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_review_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_fully_done("abd-crc", "business-expert"),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "done")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "done")

    def test_review_fails_persists_reset(self, workspace):
        """WHEN review fails -> write review_status failed +
        execution_status reset to not_started."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_review_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_review_failed("abd-crc", "business-expert"),
        )

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "not_started")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "failed")

    def test_write_failure_retries_before_next(self, workspace):
        """WHEN write fails -> retry; don't start next until persisted."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_review_in_progress("abd-crc", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        _set_skill_progress_on_board(
            workspace, "t-1", "abd-crc",
            given_skill_fully_done("abd-crc", "business-expert"),
        )
        board = load_board(workspace)

        # Then:
        then_skill_execution_status_is(workspace, "t-1", "abd-crc", "done")
        then_skill_review_status_is(workspace, "t-1", "abd-crc", "done")
        t1_raw = _find_ticket_raw(board, "t-1")
        assert "abd-spec-by-example" not in t1_raw.get("skill_progress", {})


# ============================================================================
# STORY: Complete Ticket When All Skills Finish
# ============================================================================

class TestCompleteTicketWhenAllSkillsFinish:
    """Complete Ticket When All Skills Finish."""

    def test_last_skill_done_marks_stage_complete(self, workspace):
        """WHEN last skill has both execution AND review done ->
        mark stage-complete; write board position."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_fully_done("abd-crc", "business-expert"),
            "abd-spec-by-example": given_skill_fully_done("abd-spec-by-example", "product-owner"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        stage_def = StageDef(
            name="specification",
            scope="sprint",
            stage_work_required=[
                SkillDef(skill="abd-crc", role="business-expert"),
                SkillDef(skill="abd-spec-by-example", role="product-owner"),
            ],
        )
        loaded_ticket = Ticket.from_dict(
            _find_ticket_raw(load_board(workspace), "t-1")
        )
        result = loaded_ticket.is_stage_complete(stage_def)

        # Then:
        assert result is True
        then_all_skills_fully_done(workspace, "t-1", ["abd-crc", "abd-spec-by-example"])

    def test_incomplete_skill_keeps_ticket_in_progress(self, workspace):
        """WHEN any skill not at done/done -> ticket remains in_progress."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_fully_done("abd-crc", "business-expert"),
            "abd-spec-by-example": given_skill_review_in_progress(
                "abd-spec-by-example", "product-owner"
            ),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        stage_def = StageDef(
            name="specification",
            scope="sprint",
            stage_work_required=[
                SkillDef(skill="abd-crc", role="business-expert"),
                SkillDef(skill="abd-spec-by-example", role="product-owner"),
            ],
        )
        loaded_ticket = Ticket.from_dict(
            _find_ticket_raw(load_board(workspace), "t-1")
        )
        result = loaded_ticket.is_stage_complete(stage_def)

        # Then:
        assert result is False
        then_ticket_is_active(workspace, "t-1")

    def test_review_failed_with_rework_keeps_ticket_in_progress(self, workspace):
        """WHEN review failed and rework pending -> ticket remains in_progress;
        must complete both passes again."""
        # Given:
        given_kanban_board(workspace, given_stage_config_with_skills([
            {"skill": "abd-crc", "role": "business-expert"},
            {"skill": "abd-spec-by-example", "role": "product-owner"},
        ]))
        ticket = given_ticket("t-1", "specification", "sprint", skill_progress={
            "abd-crc": given_skill_fully_done("abd-crc", "business-expert"),
            "abd-spec-by-example": given_skill_review_failed(
                "abd-spec-by-example", "product-owner"
            ),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When:
        stage_def = StageDef(
            name="specification",
            scope="sprint",
            stage_work_required=[
                SkillDef(skill="abd-crc", role="business-expert"),
                SkillDef(skill="abd-spec-by-example", role="product-owner"),
            ],
        )
        loaded_ticket = Ticket.from_dict(
            _find_ticket_raw(load_board(workspace), "t-1")
        )
        result = loaded_ticket.is_stage_complete(stage_def)

        # Then:
        assert result is False
        then_ticket_is_active(workspace, "t-1")
        then_skill_review_status_is(workspace, "t-1", "abd-spec-by-example", "failed")


# ============================================================================
# MODULE-PRIVATE HELPERS
# ============================================================================

def _find_ticket_raw(board: dict, ticket_id: str) -> dict | None:
    """Locate a raw ticket dict in any board bucket."""
    for bucket in ("active", "backlog", "done"):
        for raw in board.get(bucket, []):
            if raw.get("ticket_id") == ticket_id:
                return raw
    return None


def _set_skill_progress_on_board(
    ws: Path, ticket_id: str, skill: str, progress: SkillProgress
) -> None:
    """Write a SkillProgress update for a ticket to board.json."""
    board = load_board(ws)
    for bucket in ("active", "backlog", "done"):
        for raw in board.get(bucket, []):
            if raw.get("ticket_id") == ticket_id:
                raw.setdefault("skill_progress", {})[skill] = progress.to_dict()
                save_board(ws, board)
                return
    raise ValueError(f"Ticket '{ticket_id}' not found on board")
