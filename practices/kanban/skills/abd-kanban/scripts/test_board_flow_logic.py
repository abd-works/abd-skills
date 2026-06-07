"""
test_board_flow_logic.py

Board Flow Logic — Kanban Lead, Agent, and Skill Orchestration

Stories covered:
  - Pull Backlog Tickets to Active per Stage WIP
  - Detect Stage Completion on a Ticket
  - Scatter Ticket at Scope Boundary
  - Advance Ticket to Next Stage (Same Scope)
  - Agent Claims Next Eligible Skill (Downstream-First Pull)

Orchestrator pattern: test methods call Given/When/Then helpers.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from agent import Agent
from delivery_model import (
    KanbanBoard,
    ScatterNotAllowedError,
    SkillDef,
    SkillProgress,
    StageDef,
    Ticket,
    count_live_agents,
    load_board,
    register_executor_spawn,
    save_board,
    war_room_dir,
    write_heartbeat,
)
from kanban_lead import KanbanLead


# ============================================================================
# HELPER FUNCTIONS
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

class TestPullBacklogTicketsToActive:
    """Pull Backlog Tickets to Active per Stage WIP."""

    def test_kanban_lead_pulls_partition_tickets_up_to_wip_limit(self, workspace):
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{"name": "discovery", "scope": "partition", "stage_work_required": []}],
        })
        given_board_state(workspace, {
            "partition_wip_limit": 1,
            "backlog": [
                given_ticket("1-ext-proto", "discovery", "partition", priority=1).to_dict(),
                given_ticket("2-dual-persist", "discovery", "partition", priority=2).to_dict(),
            ],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then
        then_ticket_is_active(workspace, "1-ext-proto")
        then_ticket_is_in_backlog(workspace, "2-dual-persist")
        assert any("pulled:1-ext-proto" in a for a in actions)

    def test_kanban_lead_does_not_pull_when_wip_is_full(self, workspace):
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{"name": "discovery", "scope": "partition", "stage_work_required": []}],
        })
        given_board_state(workspace, {
            "partition_wip_limit": 1,
            "active": [given_ticket("1-ext-proto", "discovery", "partition").to_dict()],
            "backlog": [given_ticket("2-dual-persist", "discovery", "partition", priority=2).to_dict()],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then
        then_no_tickets_pulled(actions)
        then_ticket_is_in_backlog(workspace, "2-dual-persist")

    def test_kanban_lead_pulls_for_each_stage_independently(self, workspace):
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
                given_ticket("1-inc-1", "exploration", "increment").to_dict(),
            ],
        })

        # When
        when_lead_pulls(lead)

        # Then
        then_ticket_is_active(workspace, "3-batch-eod")
        then_ticket_is_active(workspace, "1-inc-1")

    def test_wip_limit_derived_from_team_capacity(self, workspace):
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

        # Then — WIP 3 from team capacity, all 3 pulled (4th stays)
        pulled = [a for a in actions if a.startswith("pulled:")]
        assert len(pulled) == 3

    def test_rolling_pull_when_first_skill_done(self, workspace):
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
                given_ticket("inc-1", "exploration", "increment", skill_progress={"abd-domain-language": ul_done}).to_dict(),
                given_ticket("inc-2", "exploration", "increment", skill_progress={"abd-domain-language": ul_done}).to_dict(),
            ],
            "backlog": [
                given_ticket("inc-3", "exploration", "increment", priority=3).to_dict(),
            ],
        })

        # When
        actions = when_lead_pulls(lead)

        # Then — 2 active with first skill done don't count against WIP
        then_ticket_is_active(workspace, "inc-3")


# ============================================================================
# STORY: Detect Stage Completion on a Ticket
# ============================================================================

class TestDetectStageCompletion:
    """Detect Stage Completion on a Ticket."""

    def test_stage_complete_when_all_required_skills_done(self, workspace):
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
        ticket = given_ticket("1-ext-proto", "discovery", "partition", skill_progress={
            "abd-domain-terms": given_skill_done("abd-domain-terms", "business-expert"),
            "abd-story-mapping": given_skill_done("abd-story-mapping", "product-owner"),
            "abd-thin-slicing": given_skill_done("abd-thin-slicing", "product-owner"),
            "abd-architecture-blueprint": given_skill_done("abd-architecture-blueprint", "engineer"),
        })

        # When / Then
        assert ticket.is_stage_complete(stage_def) is True

    def test_stage_not_complete_when_review_pending(self, workspace):
        # Given
        stage_def = StageDef(
            name="discovery",
            scope="partition",
            stage_work_required=[
                SkillDef(skill="abd-domain-terms", role="business-expert"),
                SkillDef(skill="abd-story-mapping", role="product-owner"),
            ],
        )
        ticket = given_ticket("1-ext-proto", "discovery", "partition", skill_progress={
            "abd-domain-terms": given_skill_done("abd-domain-terms", "business-expert"),
            "abd-story-mapping": SkillProgress(
                execution_status="done",
                agent="product-owner",
                review_status="not_started",
            ),
        })

        # When / Then
        assert ticket.is_stage_complete(stage_def) is False

    def test_optional_skill_does_not_block_completion(self, workspace):
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
        ticket = given_ticket("1-inc-1", "exploration", "increment", skill_progress={
            "abd-domain-language": given_skill_done("abd-domain-language", "business-expert"),
            "abd-acceptance-criteria": given_skill_done("abd-acceptance-criteria", "product-owner"),
            "abd-architecture-specification": given_skill_done("abd-architecture-specification", "engineer"),
        })

        # When / Then
        assert ticket.is_stage_complete(stage_def) is True



# ============================================================================
# STORY: Scatter Ticket at Scope Boundary
# ============================================================================

class TestScatterTicketAtScopeBoundary:
    """Scatter Ticket at Scope Boundary."""

    def test_completed_partition_scatters_into_increment_children(self, workspace):
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="discovery", scope="partition", stage_work_required=[]),
                StageDef(name="exploration", scope="increment", stage_work_required=[]),
            ],
        )
        parent = given_ticket("1-ext-proto", "discovery", "partition", entered_stage="2026-01-01T00:00:00+00:00")
        children_spec = [
            {"id": "1-ext-proto-inc-1-signon", "name": "Operator Signon", "priority": 1},
            {"id": "1-ext-proto-inc-2-routing", "name": "Message Routing", "priority": 2},
            {"id": "1-ext-proto-inc-3-session", "name": "Session Management", "priority": 3},
            {"id": "1-ext-proto-inc-4-error", "name": "Error Handling", "priority": 4},
        ]

        # When
        children = parent.scatter_into_children(kb, children_spec)

        # Then
        assert len(children) == 4
        assert parent.archived is not None
        assert parent.scatter_to == ["1-ext-proto-inc-1-signon", "1-ext-proto-inc-2-routing",
                                      "1-ext-proto-inc-3-session", "1-ext-proto-inc-4-error"]
        for child in children:
            assert child.scope_level == "increment"
            assert child.stage == "exploration"
            assert child.scatter_from == "1-ext-proto"
            assert "1-ext-proto" in child.lineage[0] or "Project" in child.lineage[0]

    def test_scatter_does_not_fire_when_same_scope(self, workspace):
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="specification", scope="sprint", stage_work_required=[]),
                StageDef(name="engineering", scope="sprint", stage_work_required=[]),
            ],
        )
        ticket = given_ticket("1-inc-1-sprint-a", "specification", "sprint")

        # When / Then — needs_scatter is false when scopes are same
        assert ticket.needs_scatter(kb) is False

    def test_already_scattered_ticket_not_scattered_again(self, workspace):
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="discovery", scope="partition", stage_work_required=[]),
                StageDef(name="exploration", scope="increment", stage_work_required=[]),
            ],
        )
        ticket = given_ticket(
            "1-ext-proto", "discovery", "partition",
            scatter_to=["1-ext-proto-inc-1", "1-ext-proto-inc-2"],
        )

        # When checking scatter eligibility on the board
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "discovery", "scope": "partition", "stage_work_required": []},
                {"name": "exploration", "scope": "increment", "stage_work_required": []},
            ],
        })
        given_board_state(workspace, {
            "done": [ticket.to_dict()],
        })
        needing = kb.tickets_needing_scatter(load_board(workspace))

        # Then
        assert len(needing) == 0

    def test_project_all_scatters_to_modules_from_partition(self, workspace):
        seed = (
            Path(__file__).resolve().parents[3]
            / "apps"
            / "abd-delivery-agent-kanban"
            / "tests"
            / "e2e"
            / "_seed"
            / "pawplace-stubs"
        )
        partition = seed / "skill-fixtures" / "abd-domain-partition.md"
        thin = seed / "skill-fixtures" / "abd-thin-slicing.md"
        (workspace / "docs/end-to-end/shaping").mkdir(parents=True, exist_ok=True)
        (workspace / "docs/end-to-end/discovery/stories").mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(partition, workspace / "docs/end-to-end/shaping/module-partition.md")
        shutil.copy2(thin, workspace / "docs/end-to-end/discovery/stories/thin-slicing.md")

        lead = KanbanLead(workspace)
        parent = given_ticket("project-all", "shaping", "all")
        modules = lead._modules_from_module_partition(workspace / "docs/end-to-end/shaping/module-partition.md")
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

class TestAdvanceTicketToNextStage:
    """Advance Ticket to Next Stage (Same Scope)."""

    def test_ticket_advances_when_stage_complete_and_same_scope(self, workspace):
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "specification", "scope": "sprint", "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ]},
                {"name": "engineering", "scope": "sprint", "stage_work_required": []},
            ],
        })
        ticket = given_ticket("1-sprint-a", "specification", "sprint", skill_progress={
            "abd-domain-model": given_skill_done("abd-domain-model", "business-expert"),
        })
        given_board_state(workspace, {
            "active": [ticket.to_dict()],
        })

        # When
        board = lead.sync_board()

        # Then
        active_stages = {t["ticket_id"]: t["stage"] for t in board["active"]}
        assert active_stages.get("1-sprint-a") == "engineering"

    def test_ticket_does_not_skip_a_stage(self, workspace):
        # Given
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(name="exploration", scope="increment", stage_work_required=[]),
                StageDef(name="specification", scope="sprint", stage_work_required=[]),
                StageDef(name="engineering", scope="sprint", stage_work_required=[]),
            ],
        )
        ticket = given_ticket("1-sprint-a", "exploration", "increment")

        # When / Then — next_stage from exploration is specification, not engineering
        nxt = kb.next_stage("exploration")
        assert nxt is not None
        assert nxt.name == "specification"


# ============================================================================
# STORY: Agent Claims Next Eligible Skill (Downstream-First Pull)
# ============================================================================

class TestAgentClaimsNextEligibleSkill:
    """Agent Claims Next Eligible Skill (Downstream-First Pull)."""

    def test_agent_claims_first_eligible_skill_in_rail_order(self, workspace):
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                    {"skill": "abd-spec-by-example", "role": "product-owner"},
                    {"skill": "abd-arch-template", "role": "engineer"},
                ],
            }],
        })
        ticket = given_ticket("1-sprint-a", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When
        result = when_agent_pulls(workspace, "business-expert")

        # Then
        assert result["action"] == "claimed"
        assert result["skill"] == "abd-domain-model"
        assert result["ticket_id"] == "1-sprint-a"

    def test_agent_skips_skills_with_incomplete_priors(self, workspace):
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [{
                "name": "specification",
                "scope": "sprint",
                "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                    {"skill": "abd-spec-by-example", "role": "product-owner"},
                ],
            }],
        })
        ticket = given_ticket("1-sprint-a", "specification", "sprint")
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When — product-owner tries to pull but abd-domain model (prior) is not done
        result = when_agent_pulls(workspace, "product-owner")

        # Then
        assert result["action"] == "none"

    def test_agent_pulls_from_rightmost_stage_first(self, workspace):
        # Given
        lead = given_kanban_board(workspace, {
            "stages": [
                {"name": "exploration", "scope": "increment", "stage_work_required": [
                    {"skill": "abd-ul", "role": "business-expert"},
                ]},
                {"name": "specification", "scope": "sprint", "stage_work_required": [
                    {"skill": "abd-domain-model", "role": "business-expert"},
                ]},
            ],
        })
        ticket_spec = given_ticket("1-sprint-a", "specification", "sprint")
        ticket_expl = given_ticket("1-inc-2", "exploration", "increment")
        given_board_state(workspace, {
            "active": [ticket_expl.to_dict(), ticket_spec.to_dict()],
        })

        # When
        result = when_agent_pulls(workspace, "business-expert")

        # Then — specification is downstream, claimed first
        assert result["action"] == "claimed"
        assert result["ticket_id"] == "1-sprint-a"
        assert result["skill"] == "abd-domain-model"

    def test_agent_does_not_claim_skill_already_in_progress(self, workspace):
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
        ticket = given_ticket("1-sprint-a", "specification", "sprint", skill_progress={
            "abd-domain-model": given_skill_in_progress("abd-domain-model", "business-expert"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        # When — agent pulls while own claim is still in_progress
        result = when_agent_pulls(workspace, "business-expert")

        # Then — must resume existing claim, not report idle
        assert result["action"] == "resume"
        assert result["ticket_id"] == "1-sprint-a"
        assert result["skill"] == "abd-domain-model"


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
                    {"skill": "abd-acceptance-criteria", "role": "product-owner"},
                    {"skill": "abd-ux-mockup", "role": "ux-designer", "optional": True},
                ],
            }],
        })
        ticket = given_ticket("1-inc-a", "exploration", "increment", skill_progress={
            "abd-acceptance-criteria": given_skill_done("abd-acceptance-criteria", "product-owner"),
            "abd-ux-mockup": given_skill_in_progress("abd-ux-mockup", "ux-designer"),
        })
        given_board_state(workspace, {"active": [ticket.to_dict()]})

        result = when_agent_pulls(workspace, "ux-designer")

        assert result["action"] == "resume"
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
