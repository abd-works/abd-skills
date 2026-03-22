"""Operator structural checks on toy fixture."""

from pathlib import Path

from agentic_skill_builder.operator import run_operator

# Minimal valid skill lives under abd-skill-builder (not bundled in this package).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_FIXTURE = _REPO_ROOT / "skills" / "abd-skill-builder" / "test" / "fixture" / "toy-polite-dialogue"


def test_operator_toy_fixture_passes():
    r = run_operator(_FIXTURE)
    assert r["ok"] is True
    assert r["skill_path"] == str(_FIXTURE.resolve())
    steps = {c["step"] for c in r["checks"]}
    assert "compileall" in steps
    assert "build" in steps
    assert "scanner" in steps
    assert "rule_scanner_bindings" in steps
    binding = next(c for c in r["checks"] if c["step"] == "rule_scanner_bindings")
    assert binding["ok"] is True
    assert len(binding["bindings"]) == 3
    scanner_scripts = [c["script"] for c in r["checks"] if c["step"] == "scanner"]
    assert len(scanner_scripts) == 4
    assert "scripts/scanner_politeness.py" in scanner_scripts
    assert "scripts/scanner_greet_warm.py" in scanner_scripts
    assert "scripts/scanner_close_graceful.py" in scanner_scripts
    assert "scripts/scanner_assume_good_faith.py" in scanner_scripts


def test_operator_missing_skill_md_fails(tmp_path):
    r = run_operator(tmp_path)
    assert r["ok"] is False
    assert "missing" in (r.get("errors") or [""])[0].lower()
