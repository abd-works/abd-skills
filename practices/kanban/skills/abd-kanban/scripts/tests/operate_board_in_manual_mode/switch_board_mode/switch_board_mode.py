"""Switch Board Mode — Persist Board Mode Setting, Read Board Mode Setting

Epic:      Operate Board in Manual Mode
Sub-epic:  Switch Board Mode

Stories covered:
  - Persist Board Mode Setting
  - Read Board Mode Setting And Switches to Manual Mode

Note: "Toggle Manual Mode" is a UI story (User actor) — not testable here.

Orchestrator pattern: test methods call Given/When/Then helpers.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

_SCRIPT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from board_mode import (
    BOARD_MODE_AUTOMATIC,
    BOARD_MODE_MANUAL,
    InvalidBoardModeError,
    is_manual_mode,
    read_board_mode,
    set_board_mode,
)
from delivery_model import load_board, save_board

from tests.operate_board_in_manual_mode.operate_board_in_manual_mode_helper import (
    given_board_mode_is,
    given_board_state,
    given_kanban_board,
    then_board_is_automatic,
    then_board_is_manual,
    then_board_mode_is,
    then_other_fields_unchanged,
    then_persisted_mode_is,
    when_board_mode_persisted,
    when_board_mode_read,
    when_board_mode_set,
    when_board_reloaded,
    workspace,
)


# ============================================================================
# STORY: Persist Board Mode Setting
# ============================================================================

class TestPersistBoardModeSetting:
    """Persist Board Mode Setting."""

    def test_app_writes_new_mode_to_board_json(self, workspace):
        """WHEN user toggles Board Mode -> app writes new value to board.json;
        change available to any reader."""
        # Given:
        given_kanban_board(workspace, {
            "stages": [{"name": "specification", "scope": "sprint", "stage_work_required": []}],
        })
        given_board_state(workspace, {})

        # When:
        when_board_mode_persisted(workspace, BOARD_MODE_MANUAL)

        # Then:
        then_persisted_mode_is(workspace, BOARD_MODE_MANUAL)

    def test_persisted_mode_reflected_on_reload_without_side_effects(self, workspace):
        """WHEN board reloaded after change -> persisted mode reflected;
        no other fields modified."""
        # Given:
        given_kanban_board(workspace, {
            "stages": [{"name": "specification", "scope": "sprint", "stage_work_required": []}],
        })
        given_board_state(workspace, {
            "backlog": [{"ticket_id": "t-1", "stage": "specification",
                         "scope_level": "sprint", "priority": 1, "lineage": ["Project", "t-1"]}],
        })
        board_before = load_board(workspace)
        board_snapshot = copy.deepcopy(board_before)

        # When:
        when_board_mode_persisted(workspace, BOARD_MODE_MANUAL)
        board_after = when_board_reloaded(workspace)

        # Then:
        then_board_mode_is(board_after, BOARD_MODE_MANUAL)
        then_other_fields_unchanged(board_snapshot, board_after)

    def test_persist_fails_on_invalid_mode_and_board_reverts(self, workspace):
        """WHEN persist fails -> board reverts toggle; user sees error."""
        # Given:
        given_kanban_board(workspace, {
            "stages": [{"name": "specification", "scope": "sprint", "stage_work_required": []}],
        })
        given_board_state(workspace, {})
        given_board_mode_is(workspace, BOARD_MODE_AUTOMATIC)

        # When:
        board = load_board(workspace)
        with pytest.raises(InvalidBoardModeError):
            when_board_mode_set(board, "bogus")

        # Then:
        then_persisted_mode_is(workspace, BOARD_MODE_AUTOMATIC)


# ============================================================================
# STORY: Read Board Mode Setting And Switches to Manual Mode
# ============================================================================

class TestReadBoardModeSettingAndSwitchesToManualMode:
    """Read Board Mode Setting And Switches to Manual Mode."""

    def test_manual_mode_suppresses_auto_actions(self, workspace):
        """WHEN lead reads board and mode is manual -> suppress auto actions;
        begin watching action state file."""
        # Given:
        given_kanban_board(workspace, {
            "stages": [{"name": "specification", "scope": "sprint", "stage_work_required": []}],
        })
        given_board_state(workspace, {})
        given_board_mode_is(workspace, BOARD_MODE_MANUAL)

        # When:
        board = when_board_reloaded(workspace)
        mode = when_board_mode_read(board)

        # Then:
        then_board_is_manual(board)
        assert mode == BOARD_MODE_MANUAL

    def test_automatic_mode_continues_autonomous(self, workspace):
        """WHEN lead reads board and mode is automatic -> continue autonomous;
        don't watch action state file."""
        # Given:
        given_kanban_board(workspace, {
            "stages": [{"name": "specification", "scope": "sprint", "stage_work_required": []}],
        })
        given_board_state(workspace, {})

        # When:
        board = when_board_reloaded(workspace)
        mode = when_board_mode_read(board)

        # Then:
        then_board_is_automatic(board)
        assert mode == BOARD_MODE_AUTOMATIC

    def test_mode_change_detected_on_next_read(self, workspace):
        """WHEN mode changes auto->manual while lead running -> detect on next read;
        suppress from that point; in-flight work completes."""
        # Given:
        given_kanban_board(workspace, {
            "stages": [{"name": "specification", "scope": "sprint", "stage_work_required": []}],
        })
        given_board_state(workspace, {})
        board_first = when_board_reloaded(workspace)
        then_board_is_automatic(board_first)

        # When:
        when_board_mode_persisted(workspace, BOARD_MODE_MANUAL)
        board_second = when_board_reloaded(workspace)

        # Then:
        then_board_is_manual(board_second)
