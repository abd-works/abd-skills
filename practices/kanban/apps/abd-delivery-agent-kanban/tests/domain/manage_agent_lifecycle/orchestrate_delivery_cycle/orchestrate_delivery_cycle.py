"""Orchestrate Delivery Cycle — Kanban Lead, Agent, and Skill Orchestration

Epic:     Manage Agent Lifecycle
Sub-epic: Orchestrate Delivery Cycle

Stories covered:
  - Pull Backlog Tickets to Active per Stage WIP
  - Detect Stage Completion on a Ticket
  - Scatter Ticket at Scope Boundary
  - Advance Ticket to Next Stage (Same Scope)
  - Agent Claims Next Eligible Skill (Downstream-First Pull)

Orchestrator pattern: test methods call Given/When/Then helpers.
File named after the sub-epic; class named after each story;
method names match spec-by-example scenario titles verbatim.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

_SCRIPT_DIR = Path(__file__).resolve().parent.parent.parent  # → tests/
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

E2E_SEED_STUBS = Path(__file__).resolve().parents[2] / "e2e" / "_seed" / "pawplace-stubs"

from domain.agent import Agent
from domain.delivery_model import (
    KanbanBoard,
    ScatterNotAllowedError,
    Skill as SkillDef,
    SkillProgress,
    Stage as StageDef,
    Ticket,
    count_live_agents,
    load_board,
    register_executor_spawn,
    save_board,
    war_room_dir,
    write_heartbeat,
)
from domain.kanban_lead import KanbanLead


# ============================================================================
# SHARED HELPERS — Given / When / Then
# ============================================================================

def given_kanban_board(ws: Path, config: dict) -> KanbanLead:
    wr = ws / "docs" / "planning" / "kanban"
    wr.mkdir(parents=True, exist_ok=True)
    (wr / "kanban.json").write_text(
        json.dumps({"definitions": {"test": config}}),
        encoding="utf-8",
    )
    return KanbanLead(ws)


def given_board_state(ws: Path, board: dict) -> None:
    board.setdefault("schema", "abd-delivery-kanban/v2")
    board.setdefault("stage_configuration", "test")
    board.setdefault("backlog", [])
    board.setdefault("active", [])
    board.setdefault("done", [])
    board.setdefault("archived", [])
    save_board(ws, board)


def given_ticket(ticket_id: str, stage: str, scope_level: str, priority: int = 1, **kwargs) -> Ticket:
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


def given_skill_done(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="done",
        agent=role,
        review_status="done",
        reviewer=role,
    )


def given_skill_in_progress(skill: str, role: str) -> SkillProgress:
    return SkillProgress(
        execution_status="in_progress",
        agent=role,
        start="2026-01-01T00:00:00+00:00",
        review_status="not_started",
    )


def when_lead_pulls(lead: KanbanLead) -> list[str]:
    return lead.pull_backlog()


def when_lead_syncs(lead: KanbanLead) -> dict:
    return lead.sync_board()


def when_lead_scatters(lead: KanbanLead) -> list[str]:
    return lead.scatter_pending()


def when_agent_pulls(ws: Path, role: str) -> dict:
    ag = Agent(ws, role)
    return ag.pull_skill()


def then_ticket_is_active(ws: Path, ticket_id: str) -> None:
    board = load_board(ws)
    active_ids = {t["ticket_id"] for t in board.get("active", [])}
    assert ticket_id in active_ids, f"{ticket_id} not in active: {active_ids}"


def then_ticket_is_in_backlog(ws: Path, ticket_id: str) -> None:
    board = load_board(ws)
    backlog_ids = {t["ticket_id"] for t in board.get("backlog", [])}
    assert ticket_id in backlog_ids, f"{ticket_id} not in backlog: {backlog_ids}"


def then_ticket_not_in_active(ws: Path, ticket_id: str) -> None:
    board = load_board(ws)
    active_ids = {t["ticket_id"] for t in board.get("active", [])}
    assert ticket_id not in active_ids, f"{ticket_id} should not be in active"


def then_no_tickets_pulled(actions: list[str]) -> None:
    pulled = [a for a in actions if a.startswith("pulled:")]
    assert len(pulled) == 0, f"Expected no pulls but got: {pulled}"


def then_n_children_in_backlog(ws: Path, n: int, stage: str, scope: str) -> None:
    board = load_board(ws)
    children = [
        t for t in board.get("backlog", [])
        if t.get("stage") == stage and t.get("scope_level") == scope
    ]
    assert len(children) == n, f"Expected {n} children, got {len(children)}"


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    return tmp_path


# ============================================================================
# STORY: Pull Backlog Tickets to Active per Stage WIP
# ============================================================================

class TestPullBacklogTicketsToActivePerStageWip:
    """Pull Backlog Tickets to Active per Stage WIP."""

    def test_kanban_lead_pulls_partition_tickets_up_to_wip_limit(self, workspace):
        """Scenario 1: Kanban Lead pulls partition tickets up to WIP limit."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{"name": "discovery", "scope": "partition", "stage_work_required": []}],
        })
        given_board_state(workspace, {
            "partition_wip_limit": 1,
            "backlog": [
                given_ticket("1-external-protocol-integration", "discovery", "partition", priority=1).to_dict(),
                given_ticket("2-dual-persistence", "discovery", "partition", priority=2).to_dict(),
            ],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then
        then_ticket_is_active(workspace, "1-external-protocol-integration")
        then_ticket_is_in_backlog(workspace, "2-dual-persistence")
        assert any("pulled:1-external-protocol-integration" in a for a in actions)

    def test_kanban_lead_does_not_pull_when_wip_is_full(self, workspace):
        """Scenario 2: Kanban Lead does not pull when WIP is full."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{"name": "discovery", "scope": "partition", "stage_work_required": []}],
        })
        given_board_state(workspace, {
            "partition_wip_limit": 1,
            "active": [given_ticket("1-external-protocol-integration", "discovery", "partition").to_dict()],
            "backlog": [given_ticket("2-dual-persistence", "discovery", "partition", priority=2).to_dict()],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then
        then_no_tickets_pulled(actions)
        then_ticket_is_in_backlog(workspace, "2-dual-persistence")

    def test_kanban_lead_pulls_for_each_stage_independently(self, workspace):
        """Scenario 3: Kanban Lead pulls for each stage independently."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "discovery", "scope": "partition", "stage_work_required": []},
                {"name": "exploration", "scope": "increment", "stage_work_required": []},
            ],
        })
        given_board_state(workspace, {
            "backlog": [
                given_ticket("3-batch-eod", "discovery", "partition").to_dict(),
                given_ticket("1-inc-1-operator-signon", "exploration", "increment").to_dict(),
            ],
        })

        # When
        when_lead_pulls(lead)

        # Then
        then_ticket_is_active(workspace, "3-batch-eod")
        then_ticket_is_active(workspace, "1-inc-1-operator-signon")

    def test_wip_limit_derived_from_team_capacity_when_not_explicit(self, workspace):
        """Scenario 4: WIP limit derived from Team capacity when not explicit."""
        # Given
        lead = given_kanban_board(workspace, {
            "team": {"business-expert": 3},
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-domain-language", "role": "business-expert"},
                ],
            }],
        })
        given_board_state(workspace, {
            "team": {"business-expert": 3},
            "backlog": [
                given_ticket(f"inc-{i}", "exploration", "increment", priority=i).to_dict()
                for i in range(1, 5)
            ],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then — WIP is 3 derived from team capacity; 4th ticket stays in backlog
        pulled = [a for a in actions if a.startswith("pulled:")]
        assert len(pulled) == 3

    def test_rolling_pull_when_first_skill_is_done_on_active_tickets(self, workspace):
        """Scenario 5: Rolling pull when first skill is done on active tickets."""
        # Given
        lead = given_kanban_board(workspace, {
            "team": {"business-expert": 3},
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-domain-language", "role": "business-expert"},
                ],
            }],
        })
        ul_done = given_skill_done("abd-domain-language", "business-expert")
        given_board_state(workspace, {
            "team": {"business-expert": 3},
            "active": [
                given_ticket("inc-1", "exploration", "increment",
                            skill_progress={"abd-domain-language": ul_done}).to_dict(),
                given_ticket("inc-2", "exploration", "increment",
                            skill_progress={"abd-domain-language": ul_done}).to_dict(),
            ],
            "backlog": [
                given_ticket("1-inc-3-payment-processing", "exploration", "increment", priority=3).to_dict(),
            ],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then — 2 active with first skill done don't count against WIP; new ticket pulled
        then_ticket_is_active(workspace, "1-inc-3-payment-processing")


# ============================================================================
# STORY: Detect Stage Completion on a Ticket
# ============================================================================

class TestDetectStageCompletionOnATicket:
    """Detect Stage Completion on a Ticket."""

    def test_stage_complete_when_all_required_skills_are_done(self, workspace):
        """Scenario 1: Stage complete when all required skills are done."""
        # Given
        stage_def = StageDef(
            name="discovery",
            scope="partition",
            stage_work_required=[
                SkillDef(skill="abd-domain-terms", role="business-expert"),
                SkillDef(skill="abd-story-mapping", role="product-owner"),
                SkillDef(skill="abd-thin-slicing", role="product-owner"),
                SkillDef(skill="abd-architecture-blueprint", role="engineer"),
            ],
        )
        ticket = given_ticket("1-external-protocol-integration", "discovery", "partition",
                              skill_progress={
                                  "abd-domain-terms": given_skill_done("abd-domain-terms", "business-expert"),
                                  "abd-story-mapping": given_skill_done("abd-story-mapping", "product-owner"),
                                  "abd-thin-slicing": given_skill_done("abd-thin-slicing", "product-owner"),
                                  "abd-architecture-blueprint": given_skill_done("abd-architecture-blueprint", "engineer"),
                              })

        # When / Then
        assert ticket.is_stage_complete(stage_def) is True

    def test_stage_not_complete_when_a_required_skill_has_review_pending(self, workspace):
        """Scenario 2: Stage not complete when a required skill has review pending."""
        # Given
        stage_def = StageDef(
            name="discovery",
            scope="partition",
            stage_work_required=[
                SkillDef(skill="abd-domain-terms", role="business-expert"),
                SkillDef(skill="abd-story-mapping", role="product-owner"),
            ],
        )
        ticket = given_ticket("1-external-protocol-integration", "discovery", "partition",
                              skill_progress={
                                  "abd-domain-terms": given_skill_done("abd-domain-terms", "business-expert"),
                                  "abd-story-mapping": SkillProgress(
                                      execution_status="done",
                                      agent="product-owner",
                                      review_status="not_started",
                                  ),
                              })

        # When / Then — review_status "not_started" means not complete
        assert ticket.is_stage_complete(stage_def) is False

    def test_optional_skill_does_not_block_stage_completion(self, workspace):
        """Scenario 3: Optional skill does not block stage completion."""
        # Given
        stage_def = StageDef(
            name="exploration",
            scope="increment",
            stage_work_required=[
                SkillDef(skill="abd-domain-language", role="business-expert"),
                SkillDef(skill="abd-acceptance-criteria", role="product-owner"),
                SkillDef(skill="abd-ux-mockup", role="ux-designer", optional=True),
                SkillDef(skill="abd-architecture-specification", role="engineer"),
            ],
        )
        ticket = given_ticket("1-inc-1-operator-signon", "exploration", "increment",
                              skill_progress={
                                  "abd-domain-language": given_skill_done("abd-domain-language", "business-expert"),
                                  "abd-acceptance-criteria": given_skill_done("abd-acceptance-criteria", "product-owner"),
                                  "abd-architecture-specification": given_skill_done("abd-architecture-specification", "engineer"),
                                  # abd-ux-mockup has no entry — it is optional
                              })

        # When / Then — optional abd-ux-mockup absent; stage is still complete
        assert ticket.is_stage_complete(stage_def) is True


# ============================================================================
# STORY: Scatter Ticket at Scope Boundary
# ============================================================================

class TestScatterTicketAtScopeBoundary:
    """Scatter Ticket at Scope Boundary."""

    def test_completed_partition_scatters_into_increment_children(self, workspace):
        """Scenario 1: Completed partition scatters into increment children."""
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="discovery", scope="partition", stage_work_required=[]),
                StageDef(name="exploration", scope="increment", stage_work_required=[]),
            ],
        )
        parent = given_ticket("1-external-protocol-integration", "discovery", "partition",
                              entered_stage="2026-01-01T00:00:00+00:00")
        children_spec = [
            {"id": "1-external-protocol-integration-inc-1-operator-signon", "name": "Operator Signon", "priority": 1},
            {"id": "1-external-protocol-integration-inc-2-message-routing", "name": "Message Routing", "priority": 2},
            {"id": "1-external-protocol-integration-inc-3-session-mgmt", "name": "Session Management", "priority": 3},
            {"id": "1-external-protocol-integration-inc-4-error-handling", "name": "Error Handling", "priority": 4},
        ]

        # When
        children = parent.scatter_into_children(kb, children_spec)

        # Then
        assert len(children) == 4
        assert parent.archived is not None
        assert parent.scatter_to == [
            "1-external-protocol-integration-inc-1-operator-signon",
            "1-external-protocol-integration-inc-2-message-routing",
            "1-external-protocol-integration-inc-3-session-mgmt",
            "1-external-protocol-integration-inc-4-error-handling",
        ]
        for child in children:
            assert child.scope_level == "increment"
            assert child.stage == "exploration"
            assert child.scatter_from == "1-external-protocol-integration"

    def test_scatter_does_not_fire_when_next_stage_has_same_scope(self, workspace):
        """Scenario 2: Scatter does not fire when next stage has same scope."""
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="specification", scope="sprint", stage_work_required=[]),
                StageDef(name="engineering", scope="sprint", stage_work_required=[]),
            ],
        )
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint")

        # When / Then — scope stays "sprint"; needs_scatter is False
        assert ticket.needs_scatter(kb) is False

    def test_already_scattered_ticket_is_not_scattered_again(self, workspace):
        """Scenario 3: Already-scattered ticket is not scattered again."""
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="discovery", scope="partition", stage_work_required=[]),
                StageDef(name="exploration", scope="increment", stage_work_required=[]),
            ],
        )
        ticket = given_ticket(
            "1-external-protocol-integration", "discovery", "partition",
            scatter_to=["1-epi-inc-1", "1-epi-inc-2"],
        )
        given_kanban_board(workspace, {
            "stages": [
                {"name": "discovery", "scope": "partition", "stage_work_required": []},
                {"name": "exploration", "scope": "increment", "stage_work_required": []},
            ],
        })
        given_board_state(workspace, {"done": [ticket.to_dict()]})

        # When
        needing = kb.tickets_needing_scatter(load_board(workspace))

        # Then — scatter_to already populated; ticket excluded
        assert len(needing) == 0

    def test_child_ticket_ids_include_parent_context_to_prevent_collisions(self, workspace):
        """Scenario 4: Child ticket IDs include parent context to prevent collisions."""
        seed = E2E_SEED_STUBS
        partition = seed / "skill-fixtures" / "abd-domain-partition.md"
        thin = seed / "skill-fixtures" / "abd-thin-slicing.md"
        (workspace / "docs/end-to-end/shaping").mkdir(parents=True, exist_ok=True)
        (workspace / "docs/end-to-end/discovery/stories").mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(partition, workspace / "docs/end-to-end/shaping/module-partition.md")
        shutil.copy2(thin, workspace / "docs/end-to-end/discovery/stories/thin-slicing.md")

        lead = KanbanLead(workspace)
        partition_ticket = given_ticket("1-product-catalog", "discovery", "partition")
        increments = lead._children_spec_for_ticket(partition_ticket)

        # Then — each child ID is prefixed with its parent's ID
        assert all(c["id"].startswith("1-product-catalog-") for c in increments)
        ids = [c["id"] for c in increments]
        assert len(ids) == len(set(ids)), "Duplicate child IDs detected"


# ============================================================================
# STORY: Advance Ticket to Next Stage (Same Scope)
# ============================================================================

class TestAdvanceTicketToNextStageSameScope:
    """Advance Ticket to Next Stage (Same Scope)."""

    def test_ticket_advances_when_stage_complete_and_next_stage_has_same_scope(self, workspace):
        """Scenario 1: Ticket advances when stage complete and next stage has same scope."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "specification", "scope": "sprint", "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ]},
                {"name": "engineering", "scope": "sprint", "stage_work_required": []},
            ],
        })
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint", skill_progress={
            "abd-domain-model": given_skill_done("abd-domain-model", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When
        board = lead.sync_board()

        # Then
        active_stages = {t["ticket_id"]: t["stage"] for t in board["active"]}
        assert active_stages.get("1-inc-1-sprint-a") == "engineering"

    def test_ticket_does_not_advance_automatically(self, workspace):
        """Scenario 2: Ticket does not advance automatically — actor must pick it up."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "specification", "scope": "sprint", "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ]},
                {"name": "engineering", "scope": "sprint", "stage_work_required": []},
            ],
        })
        # Ticket in active with ALL skills done but not yet synced by lead
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint", skill_progress={
            "abd-domain-model": given_skill_done("abd-domain-model", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # Then — before sync_board is called the ticket stays at specification
        board = load_board(workspace)
        raw = next(t for t in board["active"] if t["ticket_id"] == "1-inc-1-sprint-a")
        assert raw["stage"] == "specification"

    def test_ticket_cannot_skip_a_stage(self, workspace):
        """Scenario 3: Ticket cannot skip a stage."""
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="exploration", scope="increment", stage_work_required=[]),
                StageDef(name="specification", scope="sprint", stage_work_required=[]),
                StageDef(name="engineering", scope="sprint", stage_work_required=[]),
            ],
        )
        ticket = given_ticket("1-inc-1-sprint-a", "exploration", "increment")

        # When — next_stage after exploration is specification, not engineering
        nxt = kb.next_stage("exploration")

        # Then
        assert nxt is not None
        assert nxt.name == "specification", (
            f"Expected next stage 'specification' but got '{nxt.name}' — ticket skipped a stage"
        )


# ============================================================================
# STORY: Agent Claims Next Eligible Skill (Downstream-First Pull)
# ============================================================================

class TestAgentClaimsNextEligibleSkillDownstreamFirstPull:
    """Agent Claims Next Eligible Skill (Downstream-First Pull)."""

    def test_agent_claims_first_eligible_skill_in_rail_order(self, workspace):
        """Scenario 1: Agent claims first eligible skill in rail order."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                    {"skill": "abd-specification-by-example", "role": "product-owner"},
                    {"skill": "abd-architecture-specification", "role": "engineer"},
                    {"skill": "abd-acceptance-test-driven-development", "role": "engineer"},
                ],
            }],
        })
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When
        result = when_agent_pulls(workspace, "business-expert")

        # Then — first required skill matching business-expert is claimed
        assert result["action"] == "claimed"
        assert result["skill"] == "abd-domain-model"
        assert result["ticket_id"] == "1-inc-1-sprint-a"

    def test_agent_skips_skills_that_require_prior_skills_incomplete(self, workspace):
        """Scenario 2: Agent skips skills that require prior skills incomplete."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                    {"skill": "abd-specification-by-example", "role": "product-owner"},
                ],
            }],
        })
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When — product-owner tries to pull but prior domain model skill not done
        result = when_agent_pulls(workspace, "product-owner")

        # Then — no skill available because prior is incomplete
        assert result["action"] == "none"

    def test_agent_pulls_from_rightmost_stage_first_downstream_first(self, workspace):
        """Scenario 3: Agent pulls from rightmost stage first (downstream-first)."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "exploration", "scope": "increment", "stage_work_required": [
                    {"skill": "abd-domain-language", "role": "business-expert"},
                ]},
                {"name": "specification", "scope": "sprint", "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ]},
            ],
        })
        ticket_spec = given_ticket("1-inc-1-sprint-a", "specification", "sprint")
        ticket_expl = given_ticket("1-inc-2-sprint-b", "exploration", "increment")
        given_board_state(workspace, {
            "active": [ticket_expl.to_dict(), ticket_spec.to_dict()],
        })

        # When
        result = when_agent_pulls(workspace, "business-expert")

        # Then — specification is downstream; claimed before exploration
        assert result["action"] == "claimed"
        assert result["ticket_id"] == "1-inc-1-sprint-a"
        assert result["skill"] == "abd-domain-model"

    def test_agent_does_not_claim_skill_already_in_progress(self, workspace):
        """Scenario 4: Agent does not claim skill already in progress."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ],
            }],
        })
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint", skill_progress={
            "abd-domain-model": given_skill_in_progress(
                "abd-domain-model", "business-expert"
            ),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When — second business-expert pulls; skill already in_progress by first
        result = when_agent_pulls(workspace, "business-expert")

        # Then — must resume existing claim, not idle
        assert result["action"] in ("resume", "already_claimed")
        assert result["ticket_id"] == "1-inc-1-sprint-a"
        assert result["skill"] == "abd-domain-model"

    def test_agent_claims_review_after_execution_done(self, workspace):
        """Scenario 5: Agent claims review after execution done."""
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ],
            }],
        })
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint", skill_progress={
            "abd-domain-model": SkillProgress(
                execution_status="done",
                agent="business-expert",
                review_status="not_started",
            ),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When — business-expert looks for review work
        result = when_agent_pulls(workspace, "business-expert")

        # Then — execution is done; review can be claimed
        assert result["action"] in ("claimed", "resume")
        assert result["skill"] == "abd-domain-model"
