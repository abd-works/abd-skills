"""LangGraph orchestration state for skill delivery (plan §5.1)."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class SkillDeliveryState(TypedDict):
    """Single reducible state for builder → operator → expert → deploy pipeline.

    strategy_path: optional JSON file path (overrides ``<skill>/conf/build-strategy.json``).
    strategy: human-authored build intent (purpose, scope, pipeline, operator expectations).
    strategy_complete: True when strategy has non-empty skill_purpose.
    """

    skill_id: str
    skill_path: str
    strategy_path: str | None
    strategy: dict
    strategy_complete: bool
    builder_manifest: dict | None
    operator_report: dict | None
    expert_report: dict | None
    deploy_result: dict | None
    iteration: int
    gates: dict[str, bool]
    trace: Annotated[list[str], operator.add]
    hitl_reason: str | None
    slack_notify_ts: str | None


def initial_state(
    skill_id: str,
    skill_path: str,
    *,
    strategy_path: str | None = None,
    strategy: dict | None = None,
) -> SkillDeliveryState:
    """Default state for a new run (thread)."""
    strat = dict(strategy) if strategy else {}
    return {
        "skill_id": skill_id,
        "skill_path": skill_path,
        "strategy_path": strategy_path,
        "strategy": strat,
        "strategy_complete": bool((strat.get("skill_purpose") or "").strip()),
        "builder_manifest": None,
        "operator_report": None,
        "expert_report": None,
        "deploy_result": None,
        "iteration": 0,
        "gates": {
            "builder_review": True,
            "expert_review": True,
            "deploy": True,
        },
        "trace": [],
        "hitl_reason": None,
        "slack_notify_ts": None,
    }
