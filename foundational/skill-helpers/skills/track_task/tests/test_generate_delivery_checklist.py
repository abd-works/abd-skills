"""Tests for generate_delivery_checklist: plan parsing + checklist merge semantics."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from generate_delivery_checklist import (  # type: ignore
    parse_plan,
    render_checklist,
    _reapply_checks,
    _existing_checked_labels,
)


_SAMPLE_PLAN = """\
# Agile Delivery Plan — Sample

## Context Assessment
- Known: React.
- Risky: Acme SSO.

## Runs

| Run | Stages                     | Scope                | Checkpoint Policy | Rationale                |
| --- | -------------------------- | -------------------- | ----------------- | ------------------------ |
| 1   | Discovery → Prioritization | SSO stories          | Per-story         | Map integration surface  |
| 2   | Exploration → Engineering  | Thin slice 1         | Per-AC            | Prove end-to-end path    |
| 3a  | Exploration                | Second actor path    | Per-story         | Alternate auth flow      |
| 3b  | Specification → Engineering | Same slice | Per-story | Drain the slice |
"""


def test_parse_plan_extracts_all_runs():
    runs = parse_plan(_SAMPLE_PLAN)
    labels = [r.label for r in runs]
    assert labels == ["1", "2", "3a", "3b"]


def test_parse_plan_normalizes_stage_aliases():
    runs = parse_plan(_SAMPLE_PLAN)
    # "Story Definition" -> specification; ATDD is skill inside engineering
    assert runs[3].stages == ["specification", "engineering"]


def test_parse_plan_captures_checkpoint_and_rationale():
    runs = parse_plan(_SAMPLE_PLAN)
    assert "Per-story" in runs[0].checkpoint_policy
    assert "Map integration surface" in runs[0].rationale


def test_render_checklist_includes_reviewer_and_rework_steps(tmp_path):
    runs = parse_plan(_SAMPLE_PLAN)
    plan_path = tmp_path / "agile-delivery-plan.md"
    plan_path.write_text(_SAMPLE_PLAN, encoding="utf-8")
    rendered = render_checklist(runs, plan_path, "2026-04-22T00:00:00+00:00")

    assert "##### Reviewer" in rendered
    assert "scanners run" in rendered
    assert "exit-gate review complete" in rendered
    assert "##### Rework" in rendered
    assert "executor incorporated suggested fixes" in rendered
    assert "Per-stage tracking" in rendered
    assert "#### discovery" in rendered


def test_render_checklist_hierarchy_stage_role_skill(tmp_path):
    runs = parse_plan(_SAMPLE_PLAN)
    plan_path = tmp_path / "agile-delivery-plan.md"
    plan_path.write_text(_SAMPLE_PLAN, encoding="utf-8")
    war_room = tmp_path / "docs" / "planning" / "delivery-war-room"
    war_room.mkdir(parents=True)
    (war_room / "run-catalog.json").write_text(
        """{
  "runs": [{
    "run": 1,
    "stages": ["discovery"],
    "system_of_work": "test-sow"
  }]
}""",
        encoding="utf-8",
    )
    (war_room / "system-of-work.json").write_text(
        """{
  "definitions": {
    "test-sow": {
      "stages": {
        "discovery": [{"skill": "abd-story-mapping", "role": "product-owner", "label": "Map stories"}]
      }
    }
  }
}""",
        encoding="utf-8",
    )
    rendered = render_checklist(
        [runs[0]],
        plan_path,
        "2026-04-22T00:00:00+00:00",
        workspace=tmp_path,
    )
    assert "#### discovery" in rendered
    assert "##### Executor" in rendered
    assert "###### abd-story-mapping" in rendered
    assert "Map stories · product-owner" in rendered
    assert "##### Delivery lead" in rendered


def test_render_checklist_has_orchestration_section_and_run_rows(tmp_path):
    runs = parse_plan(_SAMPLE_PLAN)
    plan_path = tmp_path / "agile-delivery-plan.md"
    plan_path.write_text(_SAMPLE_PLAN, encoding="utf-8")
    rendered = render_checklist(runs, plan_path, "2026-04-22T00:00:00+00:00")

    assert "## Orchestration" in rendered
    assert "Step 1 — Establish workspace" in rendered
    assert "Step 8 — Plan complete" in rendered
    for r in runs:
        assert f"### Run {r.label}" in rendered
    # Stages appear for run 3b
    assert "#### specification" in rendered
    assert "#### engineering" in rendered


def test_reapply_checks_preserves_existing_state(tmp_path):
    """Simulate: generator runs → user checks Step 1 → generator runs again →
    the previously-checked line stays checked."""
    runs = parse_plan(_SAMPLE_PLAN)
    plan_path = tmp_path / "plan.md"
    plan_path.write_text(_SAMPLE_PLAN, encoding="utf-8")
    first = render_checklist(runs, plan_path, "2026-04-22T00:00:00+00:00")
    user_modified = first.replace(
        "- [ ] **Step 1 — Establish workspace**",
        "- [x] **Step 1 — Establish workspace**",
        1,
    )
    out_file = tmp_path / "checklist.md"
    out_file.write_text(user_modified, encoding="utf-8")
    previously_checked = _existing_checked_labels(out_file)
    second = render_checklist(runs, plan_path, "2026-04-23T00:00:00+00:00")
    merged = _reapply_checks(second, previously_checked)
    assert "- [x] **Step 1 — Establish workspace**" in merged
    assert "- [ ] **Step 2 — Build the plan**" in merged


def test_cli_dry_run_produces_checklist(tmp_path):
    plan = tmp_path / "agile-delivery-plan.md"
    plan.write_text(_SAMPLE_PLAN, encoding="utf-8")
    script = Path(__file__).resolve().parents[1] / "scripts" / "generate_delivery_checklist.py"
    result = subprocess.run(
        [sys.executable, str(script), "--plan", str(plan), "--dry-run"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Run 1" in result.stdout
    assert "Run 3b" in result.stdout
    assert "Orchestration" in result.stdout


def test_cli_no_runs_exits_2(tmp_path):
    plan = tmp_path / "agile-delivery-plan.md"
    plan.write_text("# Plan\n\nJust prose, no runs table.\n", encoding="utf-8")
    script = Path(__file__).resolve().parents[1] / "scripts" / "generate_delivery_checklist.py"
    result = subprocess.run(
        [sys.executable, str(script), "--plan", str(plan), "--dry-run"],
        capture_output=True, text=True,
    )
    assert result.returncode == 2
