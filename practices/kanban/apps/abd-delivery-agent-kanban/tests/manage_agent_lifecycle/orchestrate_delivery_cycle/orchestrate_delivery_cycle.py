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
from pathlib import Path

import pytest

_APP_ROOT = Path(__file__).resolve().parents[3]  # → abd-delivery-agent-kanban/
_SKILL_SCRIPTS = _APP_ROOT.parent.parent / "skills" / "abd-kanban" / "scripts"
for _p in (_APP_ROOT, _SKILL_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

E2E_SEED_STUBS = Path(__file__).resolve().parents[2] / "e2e" / "_seed" / "pawplace-stubs"

from domain.action_state import ActionIntent, append_action_intent, load_action_intents
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
from mechanism_registry import load_registry, register_mechanisms


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
                SkillDef(skill="abd-story-acceptance-criteria", role="product-owner"),
                SkillDef(skill="abd-ux-mockup", role="ux-designer", optional=True),
                SkillDef(skill="abd-architecture-specification", role="engineer"),
            ],
        )
        ticket = given_ticket("1-inc-1-operator-signon", "exploration", "increment",
                              skill_progress={
                                  "abd-domain-language": given_skill_done("abd-domain-language", "business-expert"),
                                  "abd-story-acceptance-criteria": given_skill_done("abd-story-acceptance-criteria", "product-owner"),
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

    def test_project_all_scatters_to_modules_from_partition(self, workspace):
        """Scenario 5: Project-all scatters to partition modules, then increments from thin-slicing."""
        import shutil
        seed = E2E_SEED_STUBS
        partition = seed / "skill-fixtures" / "abd-domain-partition.md"
        thin = seed / "skill-fixtures" / "abd-thin-slicing.md"
        (workspace / "docs/end-to-end/shaping").mkdir(parents=True, exist_ok=True)
        (workspace / "docs/end-to-end/discovery/stories").mkdir(parents=True, exist_ok=True)
        shutil.copy2(partition, workspace / "docs/end-to-end/shaping/module-partition.md")
        shutil.copy2(thin, workspace / "docs/end-to-end/discovery/stories/thin-slicing.md")

        lead = KanbanLead(workspace)
        modules = lead._modules_from_module_partition(
            workspace / "docs/end-to-end/shaping/module-partition.md"
        )
        assert [m["id"] for m in modules] == [
            "1-product-catalog",
            "2-store-operations",
            "3-checkout-and-fulfillment",
        ]

        partition_ticket = given_ticket("1-product-catalog", "discovery", "partition")
        increments = lead._children_spec_for_ticket(partition_ticket)
        assert len(increments) == 2
        assert increments[0]["id"].startswith("1-product-catalog-inc-1-")
        assert increments[1]["id"].startswith("1-product-catalog-inc-2-")


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
                    {"skill": "abd-story-specification", "role": "product-owner"},
                    {"skill": "abd-architecture-specification", "role": "engineer"},
                    {"skill": "abd-story-acceptance-test", "role": "engineer"},
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
                    {"skill": "abd-story-specification", "role": "product-owner"},
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


# ============================================================================
# STORY: Spawn Team Member for Dead Slot
# (covers orphan-claim prevention and executor spawn epoch)
# ============================================================================

class TestAgentOrphanClaimPrevention:
    """Agent must not leave in_progress claims while heartbeat is ready."""

    def test_signal_ready_releases_own_in_progress_claims(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-ux-mockup", "role": "ux-designer", "optional": True},
                ],
            }],
        })
        ticket = given_ticket("1-inc-a", "exploration", "increment", skill_progress={
            "abd-ux-mockup": given_skill_in_progress("abd-ux-mockup", "ux-designer"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        result = Agent(workspace, "ux-designer").signal_ready("no_eligible_skill_on_active_tickets")

        assert result["action"] == "ready"
        assert len(result["released_claims"]) == 1
        board = load_board(workspace)
        sp = board["active"][0].get("skill_progress", {})
        assert "abd-ux-mockup" not in sp

    def test_pull_resumes_after_lead_dispatch_reserve(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-story-acceptance-criteria", "role": "product-owner"},
                    {"skill": "abd-ux-mockup", "role": "ux-designer", "optional": True},
                ],
            }],
        })
        ticket = given_ticket("1-inc-a", "exploration", "increment", skill_progress={
            "abd-story-acceptance-criteria": given_skill_done("abd-story-acceptance-criteria", "product-owner"),
            "abd-ux-mockup": given_skill_in_progress("abd-ux-mockup", "ux-designer"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        result = when_agent_pulls(workspace, "ux-designer")

        assert result["action"] in ("resume", "already_claimed")
        assert result["skill"] == "abd-ux-mockup"


class TestExecutorSpawnEpoch:
    """Ghost ready heartbeats must not block executor spawns."""

    def test_ghost_ready_heartbeat_does_not_count_as_live(self, workspace):
        wr = war_room_dir(workspace)
        wr.mkdir(parents=True, exist_ok=True)
        write_heartbeat(wr, "product-owner", "ready", "no_eligible_skill_on_active_tickets")

        assert count_live_agents(wr, "product-owner") == 0

    def test_registered_spawn_epoch_counts_as_live(self, workspace):
        wr = war_room_dir(workspace)
        wr.mkdir(parents=True, exist_ok=True)
        epoch = register_executor_spawn(wr, "product-owner", 1)
        write_heartbeat(wr, "product-owner", "working", "in_progress skill", spawn_epoch=epoch)

        assert count_live_agents(wr, "product-owner") == 1

    def test_manual_scan_spawns_despite_ghost_ready_heartbeat(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-story-mapping", "role": "product-owner"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all", skill_progress={
            "abd-story-mapping": given_skill_in_progress("abd-story-mapping", "product-owner"),
        })
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"product-owner": 1},
            "active": [ticket.to_dict()],
        })
        wr = war_room_dir(workspace)
        write_heartbeat(wr, "product-owner", "ready", "no_eligible_skill_on_active_tickets")

        report = KanbanLead(workspace).run_scan_with_mode()

        assert report["roles"]["product-owner"]["spawn_needed"] == 1
        assert any(s["role"] == "product-owner" for s in report["spawns"])


# ============================================================================
# STORY: Operate Board in Manual Mode — manual pull / dispatch / drop-intent
# ============================================================================

class TestManualModeBlocksSelfPull:
    def test_pull_does_not_claim_new_skill_on_manual_board(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-domain-partition", "role": "business-expert"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all")
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"business-expert": 1},
            "active": [ticket.to_dict()],
        })

        result = when_agent_pulls(workspace, "business-expert")

        assert result["action"] == "none"
        assert result["reason"] == "manual_mode_await_operator_drop"
        board = load_board(workspace)
        assert board["active"][0].get("skill_progress", {}) == {}

    def test_pull_resumes_manual_delegation_on_manual_board(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-domain-partition", "role": "business-expert"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all", skill_progress={
            "abd-domain-partition": given_skill_in_progress("abd-domain-partition", "business-expert"),
        })
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"business-expert": 1},
            "active": [ticket.to_dict()],
        })

        result = when_agent_pulls(workspace, "business-expert")

        assert result["action"] in ("resume", "already_claimed")
        assert result["skill"] == "abd-domain-partition"

    def test_manual_scan_does_not_dispatch_pull(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-domain-partition", "role": "business-expert"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all")
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"business-expert": 1},
            "active": [ticket.to_dict()],
        })
        wr = war_room_dir(workspace)
        write_heartbeat(wr, "business-expert", "ready", "idle")

        report = KanbanLead(workspace).run_scan_with_mode()

        assert "dispatch_" not in " ".join(report.get("actions", []))
        board = load_board(workspace)
        assert board["active"][0].get("skill_progress", {}) == {}


class TestManualDropIntentFlow:
    def test_lead_scan_queues_intent_without_in_progress(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-architecture-outline", "role": "engineer"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all")
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"engineer": 1},
            "active": [ticket.to_dict()],
        })
        wr = war_room_dir(workspace)
        append_action_intent(
            wr,
            ActionIntent("project-all", "abd-architecture-outline", "engineer"),
        )

        report = KanbanLead(workspace).run_scan_with_mode()

        assert any(a.startswith("queued:project-all:abd-architecture-outline:engineer") for a in report["actions"])
        board = load_board(workspace)
        assert board["active"][0].get("skill_progress", {}) == {}
        assert len(load_action_intents(wr)) == 1

    def test_claim_next_intent_starts_work_and_clears_intent(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-architecture-outline", "role": "engineer"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all")
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"engineer": 1},
            "active": [ticket.to_dict()],
        })
        wr = war_room_dir(workspace)
        append_action_intent(
            wr,
            ActionIntent("project-all", "abd-architecture-outline", "engineer"),
        )

        result = Agent(workspace, "engineer").claim_next_intent()

        assert result["action"] == "claimed"
        assert result["skill"] == "abd-architecture-outline"
        board = load_board(workspace)
        sp = board["active"][0]["skill_progress"]["abd-architecture-outline"]
        assert sp["execution_status"] == "in_progress"
        assert sp["agent"] == "engineer"
        assert load_action_intents(wr) == []

    def test_manual_scan_spawns_for_pending_intent_without_in_progress(self, workspace):
        given_kanban_board(workspace, {
            "stages": [{
                "name": "shaping",
                "scope": "all",
                "stage_work_required": [
                    {"skill": "abd-architecture-outline", "role": "engineer"},
                ],
            }],
        })
        ticket = given_ticket("project-all", "shaping", "all")
        given_board_state(workspace, {
            "board_mode": "manual",
            "team": {"engineer": 1},
            "active": [ticket.to_dict()],
        })
        wr = war_room_dir(workspace)
        append_action_intent(
            wr,
            ActionIntent("project-all", "abd-architecture-outline", "engineer"),
        )
        write_heartbeat(wr, "engineer", "ready", "idle")

        report = KanbanLead(workspace).run_scan_with_mode()

        assert report["roles"]["engineer"]["spawn_needed"] == 1
        assert any(s["role"] == "engineer" for s in report["spawns"])


# ============================================================================
# STORY: Pull Tickets from Backlog per WIP — mechanism registry
# ============================================================================

class TestMechanismRegistry:
    """Mechanism registry — register and retrieve architecture mechanisms."""

    def test_register_and_load(self, workspace) -> None:
        (workspace / "docs" / "planning" / "kanban").mkdir(parents=True, exist_ok=True)
        register_mechanisms(workspace, "1-inc-a", "abd-architecture-specification", ["Security"])
        reg = load_registry(workspace)
        assert "Security" in reg
        assert reg["Security"]["ticket_id"] == "1-inc-a"


class TestPullEligibility:
    """Pull eligibility rules — optional skills and downstream-first ordering."""

    def test_optional_skill_eligible_when_required_priors_done(self) -> None:
        kb = KanbanBoard(
            name="t",
            stages=[
                StageDef(
                    name="exploration",
                    scope="increment",
                    stage_work_required=[
                        SkillDef(skill="abd-domain-language", role="business-expert"),
                        SkillDef(skill="abd-story-acceptance-criteria", role="product-owner"),
                        SkillDef(skill="abd-ux-mockup", role="ux-designer", optional=True),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="1-inc",
            lineage=["P"],
            scope_level="increment",
            stage="exploration",
            skill_progress={
                "abd-domain-language": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-story-acceptance-criteria": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "ux-designer")
        assert match is not None
        assert match[1] == "abd-ux-mockup"

    def test_list_eligible_pulls_downstream_first(self) -> None:
        kb = KanbanBoard(
            name="t",
            stages=[
                StageDef(
                    name="discovery",
                    scope="partition",
                    stage_work_required=[
                        SkillDef(skill="abd-story-mapping", role="product-owner"),
                    ],
                ),
                StageDef(
                    name="exploration",
                    scope="increment",
                    stage_work_required=[
                        SkillDef(skill="abd-story-acceptance-criteria", role="product-owner"),
                    ],
                ),
            ],
        )
        tickets = [
            Ticket(ticket_id="disc-1", lineage=[], scope_level="partition", stage="discovery"),
            Ticket(ticket_id="exp-1", lineage=[], scope_level="increment", stage="exploration"),
        ]
        pulls = kb.list_eligible_pulls(tickets, "product-owner")
        assert pulls[0][0] == "exp-1"


# ============================================================================
# STORY: Pull Tickets from Backlog per WIP — KanbanLead integration
# ============================================================================

class TestLeadPullFillsEachStageIndependently:
    """Pull Tickets from Backlog per WIP — stage-independent pull (lead integration)."""

    def test_generic_pull_fills_each_stage_independently(self, workspace) -> None:
        """Both discovery (partition) and exploration (increment) pull when capacity exists."""
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "discovery", "scope": "partition", "stage_work_required": []},
                {"name": "exploration", "scope": "increment", "stage_work_required": []},
            ],
        })
        given_board_state(workspace, {
            "backlog": [
                given_ticket("1-inc-a", "exploration", "increment", priority=1).to_dict(),
                given_ticket("3-partition-b", "discovery", "partition", priority=3).to_dict(),
            ],
        })

        actions = lead.pull_backlog()

        assert len(actions) > 0
        then_ticket_is_active(workspace, "3-partition-b")
        then_ticket_is_active(workspace, "1-inc-a")
        board = load_board(workspace)
        assert len(board["backlog"]) == 0


class TestLeadRollingPull:
    """Pull Tickets from Backlog per WIP — rolling pull on first-skill-done (lead integration)."""

    def test_pulls_when_first_skill_done_on_active_increments(self, workspace) -> None:
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
            "backlog": [
                given_ticket("1-inc-next", "exploration", "increment", priority=4).to_dict(),
            ],
            "active": [
                given_ticket("1-inc-done", "exploration", "increment", priority=1,
                             skill_progress={"abd-domain-language": ul_done}).to_dict(),
            ],
        })

        actions = lead.pull_backlog()

        pulled_ids = [a.split(":")[1] for a in actions if a.startswith("pulled:")]
        assert "1-inc-next" in pulled_ids
        then_ticket_is_active(workspace, "1-inc-next")


# ============================================================================
# STORY: Dispatch Skill to Idle Team Member — dispatch_claims / release_stale
# ============================================================================

class TestLeadDispatchClaims:
    """Dispatch Skill to Idle Team Member — dispatch_claims does not reserve without executor."""

    def test_does_not_reserve_without_working_executor(self, workspace) -> None:
        given_kanban_board(workspace, {
            "team": {"product-owner": 2},
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-domain-language", "role": "business-expert"},
                    {"skill": "abd-story-acceptance-criteria", "role": "product-owner"},
                ],
            }],
        })
        given_board_state(workspace, {
            "team": {"product-owner": 2},
            "active": [{
                "ticket_id": "inc-1",
                "lineage": ["P", "Inc 1"],
                "scope_level": "increment",
                "stage": "exploration",
                "priority": 1,
                "skill_progress": {
                    "abd-domain-language": {
                        "execution_status": "done",
                        "agent": "business-expert",
                        "review_status": "done",
                        "reviewer": "business-expert",
                    },
                },
            }],
        })
        lead = KanbanLead(workspace)
        actions = lead.dispatch_claims(("product-owner",))
        assert actions == []
        board = load_board(workspace)
        sp = board["active"][0]["skill_progress"].get("abd-story-acceptance-criteria")
        assert sp is None


class TestLeadReleaseStaleReserved:
    """Dispatch Skill to Idle Team Member — release_stale_reserved clears orphaned in_progress."""

    def test_release_stale_reserved_claim(self, workspace) -> None:
        given_kanban_board(workspace, {
            "team": {"product-owner": 2},
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-domain-language", "role": "business-expert"},
                    {"skill": "abd-story-acceptance-criteria", "role": "product-owner"},
                ],
            }],
        })
        given_board_state(workspace, {
            "team": {"product-owner": 2},
            "active": [{
                "ticket_id": "inc-1",
                "lineage": ["P", "Inc 1"],
                "scope_level": "increment",
                "stage": "exploration",
                "priority": 1,
                "skill_progress": {
                    "abd-domain-language": {
                        "execution_status": "done",
                        "agent": "business-expert",
                        "review_status": "done",
                        "reviewer": "business-expert",
                    },
                },
            }],
        })
        wr = war_room_dir(workspace)
        board = load_board(workspace)
        ticket = Ticket.from_dict(board["active"][0])
        ticket.skill_progress["abd-story-acceptance-criteria"] = SkillProgress(
            execution_status="in_progress",
            agent="product-owner",
            start="2026-01-01T00:00:00+00:00",
        )
        board["active"][0] = ticket.to_dict()
        save_board(workspace, board)
        write_heartbeat(wr, "product-owner", "reserved", "orphan claim", 1)

        lead = KanbanLead(workspace)
        actions = lead.release_stale_reserved(("product-owner",), stale_seconds=0)
        assert actions
        board = load_board(workspace)
        assert "abd-story-acceptance-criteria" not in board["active"][0].get("skill_progress", {})


class TestLeadReleaseReadyOrphan:
    """Dispatch Skill to Idle Team Member — release_orphan_claims on ready heartbeat."""

    def _setup_with_ux_in_progress(self, workspace) -> Path:
        given_kanban_board(workspace, {
            "team": {"product-owner": 2},
            "stages": [{
                "name": "exploration",
                "scope": "increment",
                "stage_work_required": [
                    {"skill": "abd-domain-language", "role": "business-expert"},
                    {"skill": "abd-story-acceptance-criteria", "role": "product-owner"},
                ],
            }],
        })
        given_board_state(workspace, {
            "team": {"product-owner": 2},
            "active": [{
                "ticket_id": "inc-1",
                "lineage": ["P", "Inc 1"],
                "scope_level": "increment",
                "stage": "exploration",
                "priority": 1,
                "skill_progress": {
                    "abd-domain-language": {
                        "execution_status": "done",
                        "agent": "business-expert",
                        "review_status": "done",
                        "reviewer": "business-expert",
                    },
                },
            }],
        })
        wr = war_room_dir(workspace)
        board = load_board(workspace)
        ticket = Ticket.from_dict(board["active"][0])
        ticket.skill_progress["abd-ux-mockup"] = SkillProgress(
            execution_status="in_progress",
            agent="ux-designer",
            start="2026-01-01T00:00:00+00:00",
        )
        board["active"][0] = ticket.to_dict()
        save_board(workspace, board)
        return wr

    def test_release_in_progress_when_executor_is_ready(self, workspace) -> None:
        wr = self._setup_with_ux_in_progress(workspace)
        write_heartbeat(wr, "ux-designer", "ready", "no_eligible_skill_on_active_tickets", 1)

        lead = KanbanLead(workspace)
        actions = lead.release_orphan_claims(("ux-designer",), stale_seconds=120)
        assert any(a.startswith("release_orphan:") for a in actions)
        board = load_board(workspace)
        assert "abd-ux-mockup" not in board["active"][0].get("skill_progress", {})

    def test_release_ready_orphan_even_when_stale_working_heartbeat(self, workspace) -> None:
        """Ready heartbeat wins over stale working — must not skip orphan release."""
        wr = self._setup_with_ux_in_progress(workspace)
        write_heartbeat(wr, "ux-designer", "working", "stale in_progress abd-ux-mockup", 1)
        write_heartbeat(wr, "ux-designer", "ready", "no_eligible_skill_on_active_tickets", 1)

        lead = KanbanLead(workspace)
        actions = lead.release_orphan_claims(("ux-designer",), stale_seconds=120)
        assert any(a.startswith("release_orphan:") for a in actions)
        board = load_board(workspace)
        assert "abd-ux-mockup" not in board["active"][0].get("skill_progress", {})


# ============================================================================
# STORY: Agent Claims Next Eligible Skill — find_next_eligible advancing past done
# ============================================================================

class TestFindNextEligible:
    """Agent Claims Next Eligible Skill — advancing past already-done skills on same role."""

    def test_po_advances_from_done_story_mapping_to_thin_slicing(self) -> None:
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(
                    name="discovery",
                    scope="partition",
                    stage_work_required=[
                        SkillDef(skill="abd-domain-terms", role="business-expert"),
                        SkillDef(skill="abd-story-mapping", role="product-owner"),
                        SkillDef(skill="abd-thin-slicing", role="product-owner"),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="2-partition",
            lineage=["P"],
            scope_level="partition",
            stage="discovery",
            priority=1,
            skill_progress={
                "abd-domain-terms": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-story-mapping": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "product-owner")
        assert match is not None
        assert match[1] == "abd-thin-slicing"

    def test_engineer_arch_reference_after_exploration_priors(self) -> None:
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(
                    name="exploration",
                    scope="increment",
                    stage_work_required=[
                        SkillDef(skill="abd-domain-language", role="business-expert"),
                        SkillDef(skill="abd-story-acceptance-criteria", role="product-owner"),
                        SkillDef(skill="abd-architecture-specification", role="engineer"),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="1-inc",
            lineage=["P"],
            scope_level="increment",
            stage="exploration",
            priority=1,
            skill_progress={
                "abd-domain-language": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-story-acceptance-criteria": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "engineer")
        assert match is not None
        assert match[1] == "abd-architecture-specification"

    def test_engineer_arch_template_after_specification_priors(self) -> None:
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(
                    name="specification",
                    scope="sprint",
                    stage_work_required=[
                        SkillDef(skill="abd-domain-model", role="business-expert"),
                        SkillDef(skill="abd-story-specification", role="product-owner"),
                        SkillDef(skill="abd-architecture-specification", role="engineer"),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="1-sprint",
            lineage=["P"],
            scope_level="sprint",
            stage="specification",
            priority=1,
            skill_progress={
                "abd-domain-model": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-story-specification": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "engineer")
        assert match is not None
        assert match[1] == "abd-architecture-specification"
