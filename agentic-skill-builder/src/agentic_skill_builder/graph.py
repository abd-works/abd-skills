"""LangGraph: ingest → strategize → builder → operator → expert → orchestrator (plan §5.2, P1)."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from agentic_skill_builder.expert import run_expert
from agentic_skill_builder.operator import run_operator
from agentic_skill_builder.pipeline_slack import (
    lines_for_expert_report,
    lines_for_operator_report,
    log_pipeline_stage,
)
from agentic_skill_builder.state import SkillDeliveryState
from agentic_skill_builder.strategize import load_build_strategy, strategy_filled_enough

try:
    from langgraph.checkpoint.sqlite import SqliteSaver
except ImportError:  # pragma: no cover
    SqliteSaver = None  # type: ignore[misc, assignment]


def _ingest_request(state: SkillDeliveryState) -> dict[str, Any]:
    sid = state["skill_id"]
    sp = state["skill_path"]
    trace = [f"ingest_request: skill_id={sid!r} skill_path={sp!r}"]
    trace.extend(
        log_pipeline_stage(
            "ingest",
            skill_id=sid,
            skill_path=sp,
            body_lines=[
                "Starting LangGraph delivery run (ingest → strategize → builder → operator → expert → orchestrator).",
                f"*Decision:* proceed using skill_path `{sp}` for all file operations.",
            ],
        )
    )
    return {"trace": trace}


def _strategize(state: SkillDeliveryState) -> dict[str, Any]:
    """Load ``conf/build-strategy.json`` or ``--strategy-file``; records how the skill should be built."""
    root = Path(state["skill_path"]).resolve()
    strat, extra, src = load_build_strategy(root, state.get("strategy_path"))
    trace = [f"strategize: source={src}"] + extra
    complete = strategy_filled_enough(strat)
    if not complete:
        trace.append(
            "strategize: note — add a non-empty skill_purpose when you are ready to lock intent.",
        )
    purpose = (strat.get("skill_purpose") or "").strip()
    trace.extend(
        log_pipeline_stage(
            "strategize",
            skill_id=state["skill_id"],
            skill_path=state["skill_path"],
            body_lines=[
                f"*Strategy source:* `{src}`",
                f"*strategy_complete:* `{complete}` (requires non-empty skill_purpose)",
                f"*skill_purpose (excerpt):* {purpose[:280]}{'…' if len(purpose) > 280 else ''}",
                f"*Phases (from JSON):* {', '.join(str(x) for x in (strat.get('pipeline_phases') or [])[:12])}",
                "*Decision:* use this strategy for builder manifest and operator expectations.",
            ],
        )
    )
    return {
        "strategy": strat,
        "strategy_complete": complete,
        "trace": trace,
    }


def _builder(state: SkillDeliveryState) -> dict[str, Any]:
    # Stub: real implementation will expand templates and write files (plan §4.1).
    manifest = {
        "stub": True,
        "version": 1,
        "skill_path": state["skill_path"],
        "strategy": state.get("strategy") or {},
        "strategy_complete": state.get("strategy_complete", False),
    }
    trace = ["builder: stub manifest emitted"]
    trace.extend(
        log_pipeline_stage(
            "builder",
            skill_id=state["skill_id"],
            skill_path=state["skill_path"],
            body_lines=[
                "*Manifest:* stub v1 (P1 — real templating later).",
                f"*iteration:* {state['iteration'] + 1}",
                f"*strategy_complete carried:* `{manifest.get('strategy_complete')}`",
                "*Decision:* hand off to operator for compileall / build.py / scanners.",
            ],
        )
    )
    return {
        "builder_manifest": manifest,
        "iteration": state["iteration"] + 1,
        "trace": trace,
    }


def _operator(state: SkillDeliveryState) -> dict[str, Any]:
    report = run_operator(state["skill_path"])
    status = "pass" if report.get("ok") else "fail"
    trace = [f"operator: structural {status}"]
    trace.extend(
        log_pipeline_stage(
            "operator",
            skill_id=state["skill_id"],
            skill_path=state["skill_path"],
            body_lines=lines_for_operator_report(report)
            + [
                "*Decision:* if pass, run expert critique; if fail, expert still runs but fix scanners/build.",
            ],
        )
    )
    return {"operator_report": report, "trace": trace}


def _expert_critique(state: SkillDeliveryState) -> dict[str, Any]:
    report = run_expert(
        skill_id=state["skill_id"],
        skill_path=state["skill_path"],
        operator_report=state.get("operator_report"),
    )
    tag = "skipped" if report.get("skipped") else "llm"
    trace = [f"expert_critique: {tag}"]
    trace.extend(
        log_pipeline_stage(
            "expert_critique",
            skill_id=state["skill_id"],
            skill_path=state["skill_path"],
            body_lines=lines_for_expert_report(report)
            + [
                "*Decision:* rubric scores inform human review; deploy stub does not run in P1.",
            ],
        )
    )
    return {"expert_report": report, "trace": trace}


def _orchestrator_decide(state: SkillDeliveryState) -> dict[str, Any]:
    prior = list(state.get("trace") or [])
    bullet = "\n".join(f"  {i + 1}. {t}" for i, t in enumerate(prior[-25:]))
    if len(prior) > 25:
        bullet = f"  … ({len(prior) - 25} earlier line(s) omitted)\n" + bullet
    trace = ["orchestrator_decide: run complete (no deploy in P1 stub)"]
    trace.extend(
        log_pipeline_stage(
            "trace / orchestrator",
            skill_id=state["skill_id"],
            skill_path=state["skill_path"],
            body_lines=[
                "*Final trace (last up to 25 lines):*",
                bullet or "  (empty)",
                "*Decision:* graph complete; HITL resume available if SQLite + interrupt_before used.",
            ],
        )
    )
    return {"trace": trace}


def _make_state_graph() -> StateGraph[SkillDeliveryState]:
    g: StateGraph[SkillDeliveryState] = StateGraph(SkillDeliveryState)
    g.add_node("ingest_request", _ingest_request)
    g.add_node("strategize", _strategize)
    g.add_node("builder", _builder)
    g.add_node("operator", _operator)
    g.add_node("expert_critique", _expert_critique)
    g.add_node("orchestrator_decide", _orchestrator_decide)

    g.add_edge(START, "ingest_request")
    g.add_edge("ingest_request", "strategize")
    g.add_edge("strategize", "builder")
    g.add_edge("builder", "operator")
    g.add_edge("operator", "expert_critique")
    g.add_edge("expert_critique", "orchestrator_decide")
    g.add_edge("orchestrator_decide", END)
    return g


def build_checkpointer(sqlite_path: Path | None) -> BaseCheckpointSaver:
    """Memory for tests / ephemeral runs; SQLite for durable resume (plan §2)."""
    if sqlite_path is None:
        return MemorySaver()
    if SqliteSaver is None:
        raise RuntimeError("Install langgraph-checkpoint-sqlite for SQLite checkpoints")
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(sqlite_path), check_same_thread=False)
    return SqliteSaver(conn)


def compile_delivery_graph(
    *,
    checkpointer: BaseCheckpointSaver | None = None,
    interrupt_before: list[str] | None = None,
) -> Any:
    """
    Compile the skill-delivery graph.

    If ``checkpointer`` is None, uses in-memory checkpoints (fine for tests and one-shot CLI).
    """
    g = _make_state_graph()
    kwargs: dict[str, Any] = {"interrupt_before": interrupt_before or []}
    if checkpointer is not None:
        kwargs["checkpointer"] = checkpointer
    return g.compile(**kwargs)


def default_interrupt_nodes() -> list[str]:
    """All automated nodes — use for bootstrap HITL until scaffold sign-off (§5.2)."""
    return [
        "ingest_request",
        "strategize",
        "builder",
        "operator",
        "expert_critique",
        "orchestrator_decide",
    ]
