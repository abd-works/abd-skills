"""Tests for plan-shape-scanner: asserts each rule fires on its matching fixture.

The scanner file uses a hyphenated name; import it by file path.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_SCANNER_PATH = _SKILL_ROOT / "scanners" / "plan-shape-scanner.py"
_FIXTURES = _SKILL_ROOT / "scanners" / "tests"


def _load_scanner_module():
    spec = importlib.util.spec_from_file_location("plan_shape_scanner", _SCANNER_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def scanner():
    return _load_scanner_module()


def _rules_fired(scanner, fixture_name: str) -> set[str]:
    text = (_FIXTURES / fixture_name).read_text(encoding="utf-8")
    return {v.rule.name for v in scanner.run_checks(text)}


def test_good_plan_has_no_violations(scanner):
    assert _rules_fired(scanner, "good-plan.md") == set()


def test_missing_inventory_fires_context_inventory_rule(scanner):
    fired = _rules_fired(scanner, "bad-plan-missing-inventory.md")
    assert "plan-has-context-inventory" in fired
    # Should not also fire unrelated rules
    assert "plan-runs-have-concrete-outcome" not in fired


def test_risk_only_rationale_fires_concrete_outcome_rule(scanner):
    fired = _rules_fired(scanner, "bad-plan-risk-only-rationale.md")
    assert "plan-runs-have-concrete-outcome" in fired


def test_default_six_stage_fires_decomposition_and_checkpoint_rules(scanner):
    fired = _rules_fired(scanner, "bad-plan-default-six-stage.md")
    assert "plan-is-not-default-six-stage" in fired
    assert "plan-checkpoint-density-matches-risk" in fired


def test_loose_checkpoints_fires_checkpoint_density_rule(scanner):
    fired = _rules_fired(scanner, "bad-plan-loose-checkpoints.md")
    assert "plan-checkpoint-density-matches-risk" in fired


def test_routine_template_fires_system_of_work_rule(scanner):
    fired = _rules_fired(scanner, "bad-plan-routine-template.md")
    assert "plan-uses-system-of-work" in fired


def _canonical_plan(tmp_path: Path) -> Path:
    lead = tmp_path / "docs" / "planning" / "abd-kanban-lead"
    lead.mkdir(parents=True, exist_ok=True)
    return lead / "agile-delivery-plan.md"


def test_cli_exit_code_pass(tmp_path):
    plan = _canonical_plan(tmp_path)
    plan.write_text((_FIXTURES / "good-plan.md").read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(_SCANNER_PATH), "--workspace", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


def test_cli_exit_code_fail(tmp_path):
    plan = _canonical_plan(tmp_path)
    plan.write_text((_FIXTURES / "bad-plan-missing-inventory.md").read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(_SCANNER_PATH), "--workspace", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "plan-has-context-inventory" in result.stderr


def test_cli_no_plan_is_silent_pass(tmp_path):
    # No plan file in tmp_path — scanner should exit 0 silently.
    result = subprocess.run(
        [sys.executable, str(_SCANNER_PATH), "--workspace", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stderr.strip() == ""


def test_trivial_frontmatter_allows_single_run_six_stage(scanner):
    plan = (
        "---\n"
        "trivial: true\n"
        "---\n"
        "# Plan\n"
        "## Runs\n"
        "| Run | Stages | Scope | Checkpoint Policy | Rationale |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 1 | Shaping -> Discovery -> Exploration -> Specification -> Engineering | all | per-slice | "
        "ship internal tool end-to-end; no classified risk |\n"
    )
    violations = scanner.run_checks(plan)
    rules = {v.rule.name for v in violations}
    # Trivial flag suppresses the default-six-stage rule; risk classification
    # rule still fires because the plan has no risks and context inventory is also missing.
    assert "plan-is-not-default-six-stage" not in rules
