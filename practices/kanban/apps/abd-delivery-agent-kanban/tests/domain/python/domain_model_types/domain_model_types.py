"""Domain Model Types — BoardPosition, TeamMembership, SkillProgress invariants

Epic:     (cross-cutting domain model)
Sub-epic: Domain Model Types

Stories covered:
  - BoardPosition derived from Ticket (sub_state, current_stage_name)
  - TeamMembership pair counts (increment/decrement)
  - SkillProgress review invariant (review blocked until execution done)
  - KanbanBoard records save timestamp

Orchestrator pattern: one class per story area, GWT helpers.
File named after the sub-epic; class named after each story area.
"""
from __future__ import annotations

import sys
from pathlib import Path

_APP_ROOT = Path(__file__).resolve().parents[4]  # → abd-delivery-agent-kanban/
_SKILL_SCRIPTS = _APP_ROOT.parent.parent / "skills" / "abd-kanban" / "scripts"
for _p in (_APP_ROOT, _SKILL_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from domain.delivery_model import (
    BoardPosition,
    KanbanBoard,
    Skill,
    SkillProgress,
    Stage,
    TeamMembership,
    Ticket,
)


# ============================================================================
# GIVEN HELPERS
# ============================================================================

def given_ticket_with_execution_done_only() -> Ticket:
    return Ticket(
        ticket_id="1-partition",
        stage="discovery",
        scope_level="partition",
        skill_progress={
            "abd-domain-terms": SkillProgress(
                execution_status="done",
                review_status="not_started",
            ),
        },
    )


def given_stage_with_one_skill() -> Stage:
    return Stage(
        name="discovery",
        scope="partition",
        stage_work_required=[Skill(skill="abd-domain-terms", role="business-expert")],
    )


# ============================================================================
# STORY: BoardPosition Derived from Ticket
# ============================================================================

class TestBoardPositionDerivedFromTicket:
    """BoardPosition invariants derived from Ticket state."""

    def test_ticket_in_progress_when_skill_executing(self) -> None:
        ticket = Ticket(
            ticket_id="1-partition",
            stage="discovery",
            skill_progress={
                "abd-domain-terms": SkillProgress(execution_status="in_progress"),
            },
        )
        position = BoardPosition.derive(ticket)
        assert position.sub_state == "in_progress"
        assert position.current_stage_name == "discovery"

    def test_ticket_done_sub_state_when_stage_skills_complete(self) -> None:
        ticket = given_ticket_with_execution_done_only()
        ticket.skill_progress["abd-domain-terms"].review_status = "done"
        stage = given_stage_with_one_skill()
        position = BoardPosition.derive(ticket, stage)
        assert position.sub_state == "done"


# ============================================================================
# STORY: TeamMembership Pair Counts
# ============================================================================

class TestTeamMembershipPairCounts:
    """TeamMembership invariants — increment and decrement pair counts per role."""

    def test_increment_and_decrement_pair_count_for_role(self) -> None:
        membership = TeamMembership(counts={"engineer": 1})
        membership.increment_pair_count("engineer")
        assert membership.count_for_role("engineer") == 2
        membership.decrement_pair_count("engineer")
        assert membership.count_for_role("engineer") == 1

    def test_team_membership_loads_from_board_dict(self) -> None:
        board = {"team": {"product-owner": 2, "engineer": 1}}
        membership = TeamMembership.from_board(board)
        assert membership.count_for_role("product-owner") == 2


# ============================================================================
# STORY: SkillProgress Review Invariant
# ============================================================================

class TestSkillProgressReviewInvariant:
    """SkillProgress invariant — review cannot start until execution is done."""

    def test_review_cannot_start_until_execution_done(self) -> None:
        progress = SkillProgress(execution_status="in_progress", review_status="not_started")
        assert progress.review_can_start() is False

    def test_review_can_start_when_execution_done(self) -> None:
        progress = SkillProgress(execution_status="done", review_status="not_started")
        assert progress.review_can_start() is True


# ============================================================================
# STORY: KanbanBoard Records Save Timestamp
# ============================================================================

class TestKanbanBoardRecordsSaveTimestamp:
    """KanbanBoard saves timestamp on record_save_timestamp()."""

    def test_record_save_timestamp_sets_saved_at(self) -> None:
        board = KanbanBoard(name="test", stages=[])
        assert board.saved_at is None
        board.record_save_timestamp()
        assert board.saved_at is not None
