"""Interrupt + resume: ``invoke(None, config)`` and CLI ``resume`` subcommand."""

from pathlib import Path

from agentic_skill_builder.cli import main
from agentic_skill_builder.graph import build_checkpointer, compile_delivery_graph
from agentic_skill_builder.state import initial_state

_REPO_ROOT = Path(__file__).resolve().parents[2]
_FIXTURE = _REPO_ROOT / "skills" / "abd-skill-builder" / "test" / "fixture" / "toy-polite-dialogue"


def test_interrupt_before_then_invoke_none_completes():
    app = compile_delivery_graph(
        checkpointer=__import__("langgraph.checkpoint.memory", fromlist=["MemorySaver"]).MemorySaver(),
        interrupt_before=["ingest_request"],
    )
    cfg = {"configurable": {"thread_id": "t-resume"}}
    s0 = app.invoke(
        initial_state("x", str(_FIXTURE)),
        config=cfg,
    )
    assert s0.get("trace") == []

    s1 = app.invoke(None, config=cfg)
    assert s1.get("operator_report", {}).get("ok") is True
    assert any("ingest_request" in t for t in s1.get("trace", []))


def test_cli_resume_continues_sqlite_checkpoint(tmp_path):
    db = tmp_path / "cp.sqlite"
    code = main(
        [
            "run",
            "--skill-id",
            "toy",
            "--skill-path",
            str(_FIXTURE),
            "--sqlite",
            str(db),
            "--thread-id",
            "cli-resume-test",
            "--interrupt-before",
            "ingest_request",
            "--json",
        ]
    )
    assert code == 0

    code2 = main(
        [
            "resume",
            "--sqlite",
            str(db),
            "--thread-id",
            "cli-resume-test",
            "--interrupt-before",
            "ingest_request",
            "--json",
        ]
    )
    assert code2 == 0
