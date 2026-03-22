"""Delivery graph runs end-to-end with real operator / expert on toy fixture."""

from pathlib import Path

from agentic_skill_builder.graph import compile_delivery_graph, default_interrupt_nodes
from agentic_skill_builder.state import initial_state
from langgraph.checkpoint.memory import MemorySaver

_REPO_ROOT = Path(__file__).resolve().parents[2]
_FIXTURE = _REPO_ROOT / "skills" / "abd-skill-builder" / "test" / "fixture" / "toy-polite-dialogue"


def test_delivery_graph_runs_with_toy_fixture():
    app = compile_delivery_graph(checkpointer=MemorySaver())
    out = app.invoke(
        initial_state("toy-polite-dialogue", str(_FIXTURE)),
        config={"configurable": {"thread_id": "test-1"}},
    )
    assert out["builder_manifest"] is not None
    assert out["builder_manifest"].get("stub") is True
    assert out.get("strategy_complete") is True
    assert (out.get("builder_manifest") or {}).get("strategy", {}).get("skill_purpose")
    assert out["operator_report"] is not None
    assert out["operator_report"].get("ok") is True
    assert out["expert_report"] is not None
    ex = out["expert_report"]
    assert ex.get("skipped") is True or ex.get("public")
    trace = out["trace"]
    assert any("ingest_request" in t for t in trace)
    assert any("strategize" in t for t in trace)
    assert any("builder" in t for t in trace)
    assert any("operator" in t for t in trace)
    assert any("expert" in t for t in trace)
    assert out["iteration"] == 1


def test_default_interrupt_nodes_lists_all_automated():
    names = default_interrupt_nodes()
    assert "ingest_request" in names
    assert "strategize" in names
    assert "builder" in names
    assert "operator" in names
    assert "expert_critique" in names
    assert "orchestrator_decide" in names
