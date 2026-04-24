"""Stubbed-team-member orchestration invariants.

Emulates an abd-delivery-lead walk through Steps 1-8 over a toy workspace by
calling the scripts the lead is expected to call, with a fake team-member
that writes canned artifacts between stages. Tests the *tool-call contract*
and the *filesystem invariants* the steps must maintain — not LLM reasoning.

What each step is emulated to do:

  Step 1: create workspace + checklist file (track_task)
  Step 2: write agile-delivery-plan.md + regenerate checklist (generator)
          + run plan-shape scanner
  Step 3: read stage definition (existence assertion)
  Step 4: bootstrap team-member (write story-graph.json via story_graph_cli)
  Step 5: exit-gate — validate graph via story_graph_cli read
  Step 6: handoff — graph still valid
  Step 7: revise plan + append changelog entry + regenerate checklist
  Step 8: close out — checklist entirely checked

Invariants checked after relevant steps:

  - plan file exists after Step 2
  - checklist exists after Step 1 and regenerated after Step 2
  - checklist run labels correspond to plan run labels
  - scanners pass against the good plan
  - story_graph.json is valid JSON with the expected shape
  - corrections log entries picked up at bootstrap are those tagged Affects
  - changelog entry recorded after Step 7
  - checked state survives checklist regeneration
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


_REPO = Path(__file__).resolve().parents[3]
_GENERATOR = _REPO / "skills" / "track_task" / "scripts" / "generate_delivery_checklist.py"
_SCANNER = _REPO / "skills" / "abd-delivery-planning" / "scanners" / "plan-shape-scanner.py"
_STORY_CLI = _REPO / "skills" / "story-graph-ops" / "scripts" / "story_graph_cli.py"
_CHANGELOG = _REPO / "skills" / "abd-delivery-planning" / "scripts" / "append_plan_revision.py"
_STAGES = _REPO / "agents" / "abd-delivery-lead" / "stages"


GOOD_PLAN = """\
---
version: 1
---
# Agile Delivery Plan — Toy Engagement

## Context inventory

**Provided:** brief, React repo.
**Missing (not yet provided):** Acme SSO docs.
**Implications:** Run 2 blocked until docs land or spike runs first.

## Risks

- **Integration risk** — Acme SSO.
- **AI-model risk** — proprietary internals.

## Strategy

Selected: `strategies/new-initiative-proprietary-technology-risk.md`

## Runs

| Run | Stages                     | Scope            | Checkpoint Policy | Rationale                                                  |
| --- | -------------------------- | ---------------- | ----------------- | ---------------------------------------------------------- |
| 1   | Discovery → Prioritization | SSO surface      | Per-story         | Map integration surface and capture unknowns               |
| 2   | Exploration → Engineering  | Thin slice 1     | Per-AC            | Prove spec → test → code against Acme SSO                  |
"""

EMPTY_GRAPH = {"epics": [], "increments": []}


def _load_module(path: Path, modname: str):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
    )


def _fake_team_member_discovery(workspace: Path) -> None:
    """Stub for Step 4 (Discovery stage). Writes a minimal story-graph.json."""
    graph = {
        "epics": [
            {
                "name": "User signs in via Acme SSO",
                "sequential_order": 1.0,
                "sub_epics": [
                    {
                        "name": "Authenticate user",
                        "sequential_order": 1.0,
                        "story_groups": [
                            {
                                "name": None,
                                "stories": [
                                    {"name": "User submits Acme SSO credentials", "sequential_order": 1.0}
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "increments": [],
    }
    graph_path = workspace / "story-graph.json"
    result = _run_script(
        _STORY_CLI, "write", "--file", str(graph_path), "--input", "-",
    )
    # Subprocess flavor: provide json via stdin through a second call using --input with a tmp file
    # Simpler: use subprocess directly with stdin=json text
    result = subprocess.run(
        [sys.executable, str(_STORY_CLI), "write", "--file", str(graph_path)],
        input=json.dumps(graph), capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


# --- tests ------------------------------------------------------------------

def test_stage_definitions_exist():
    """Step 3 precondition: all six stage files are readable."""
    expected = {
        "discovery", "prioritization", "exploration",
        "scenarios", "acceptance-tests", "engineering",
    }
    present = {p.stem for p in _STAGES.glob("*.md")}
    assert expected.issubset(present), f"missing stages: {expected - present}"


def test_step_2_writes_plan_and_regenerates_checklist(tmp_path):
    """Step 2: plan written, checklist generated, run labels match between files."""
    workspace = tmp_path
    plan_path = workspace / "agile-delivery-plan.md"
    plan_path.write_text(GOOD_PLAN, encoding="utf-8")

    checklist_path = workspace / "abd-delivery-lead" / "progress" / "delivery-plan-checklist.md"
    r = _run_script(_GENERATOR, "--plan", str(plan_path), "--out", str(checklist_path))
    assert r.returncode == 0, r.stderr
    assert checklist_path.is_file()

    text = checklist_path.read_text(encoding="utf-8")
    # Invariant: every run in the plan appears in the checklist
    for label in ("Run 1", "Run 2"):
        assert f"### {label}" in text, f"checklist missing {label}"

    # Invariant: orchestration steps 1-8 are present
    for step in ("Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "Step 7", "Step 8"):
        assert step in text


def test_step_2_scanner_passes_on_good_plan(tmp_path):
    """Step 2 scanner check: plan-shape scanner exits 0 on a well-formed plan."""
    workspace = tmp_path
    (workspace / "agile-delivery-plan.md").write_text(GOOD_PLAN, encoding="utf-8")
    r = _run_script(_SCANNER, "--workspace", str(workspace))
    assert r.returncode == 0, r.stderr


def test_step_4_stub_writes_valid_story_graph(tmp_path):
    """Step 4: bootstrapped team-member produces a graph that passes read-validation."""
    workspace = tmp_path
    _fake_team_member_discovery(workspace)
    graph_path = workspace / "story-graph.json"
    r = _run_script(_STORY_CLI, "read", "--file", str(graph_path))
    assert r.returncode == 0, r.stderr
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    assert data["epics"][0]["name"] == "User signs in via Acme SSO"


def test_step_5_graph_is_valid_after_stage(tmp_path):
    """Step 5 exit-gate: graph still passes structural read after stage completes."""
    workspace = tmp_path
    _fake_team_member_discovery(workspace)
    r = _run_script(_STORY_CLI, "read", "--file", str(workspace / "story-graph.json"))
    assert r.returncode == 0
    r = _run_script(_STORY_CLI, "names", "--file", str(workspace / "story-graph.json"))
    assert r.returncode == 0
    assert "User submits Acme SSO credentials" in r.stdout


def test_step_7_changelog_entry_appended(tmp_path):
    """Step 7: append_plan_revision records the revision with summary + sha."""
    workspace = tmp_path
    (workspace / "agile-delivery-plan.md").write_text(GOOD_PLAN, encoding="utf-8")
    r = _run_script(
        _CHANGELOG,
        "--workspace", str(workspace),
        "--summary", "Re-scoped Run 2 after spike",
        "--rationale", "SSO doc landed; narrower scope now viable",
    )
    assert r.returncode == 0, r.stderr
    changelog = workspace / "agile-delivery-plan.changelog.md"
    assert changelog.is_file()
    text = changelog.read_text(encoding="utf-8")
    assert "Re-scoped Run 2 after spike" in text
    assert "Plan sha" in text


def test_step_7_checklist_regeneration_preserves_checked_state(tmp_path):
    """Step 7: re-running the generator after a plan revision preserves `[x]` state."""
    workspace = tmp_path
    plan = workspace / "agile-delivery-plan.md"
    plan.write_text(GOOD_PLAN, encoding="utf-8")
    checklist = workspace / "abd-delivery-lead" / "progress" / "delivery-plan-checklist.md"
    assert _run_script(_GENERATOR, "--plan", str(plan), "--out", str(checklist)).returncode == 0

    # Simulate user checking Step 1 off.
    text = checklist.read_text(encoding="utf-8")
    text = text.replace(
        "- [ ] **Step 1 — Establish workspace**",
        "- [x] **Step 1 — Establish workspace**",
        1,
    )
    checklist.write_text(text, encoding="utf-8")

    # Revise the plan and re-generate.
    plan.write_text(GOOD_PLAN + "\n## Notes\n- revised\n", encoding="utf-8")
    assert _run_script(_GENERATOR, "--plan", str(plan), "--out", str(checklist)).returncode == 0

    new_text = checklist.read_text(encoding="utf-8")
    assert "- [x] **Step 1 — Establish workspace**" in new_text


def test_step_5_cross_stage_corrections_filter_by_affects(tmp_path):
    """Step 5 / Step 4 carry-forward: the lead filters corrections by `Affects` scope.

    The lead's contract is: for the next stage + role, only surface entries whose
    Affects intersects. This test emulates that filter in the lead's role so we
    prove the contract is mechanically expressible.
    """
    log = tmp_path / "docs" / "corrections-log.md"
    log.parent.mkdir(parents=True)
    log.write_text(
        """# Corrections log

## Entry: domain term unified
- **Status:** confirmed
- **Rule:** rules/domain-terms.md
- **Affects:**
  - stage: exploration
  - story: *
  - role: analyst

## Entry: clean-code helper extracted
- **Status:** confirmed
- **Rule:** rules/helper-extracted.md
- **Affects:**
  - stage: engineering
  - role: engineer
""",
        encoding="utf-8",
    )

    def corrections_for(stage: str, role: str) -> list[str]:
        text = log.read_text(encoding="utf-8")
        entries = [e for e in text.split("## Entry:")[1:]]
        hits: list[str] = []
        for entry in entries:
            # Extract the Affects block (naive line scan)
            in_affects = False
            affects_text_lines: list[str] = []
            for line in entry.splitlines():
                if line.strip().startswith("- **Affects:**"):
                    in_affects = True
                    continue
                if in_affects:
                    if line.startswith("- **") or not line.strip():
                        break
                    affects_text_lines.append(line)
            block = "\n".join(affects_text_lines).lower()
            if (f"stage: {stage}" in block or "stage: *" in block) and \
               (f"role: {role}" in block or "role: *" in block or "role:" not in block):
                title = entry.splitlines()[0].strip()
                hits.append(title)
        return hits

    # Analyst in exploration should see the first entry only.
    assert corrections_for("exploration", "analyst") == ["domain term unified"]
    # Engineer in engineering should see the second entry only.
    assert corrections_for("engineering", "engineer") == ["clean-code helper extracted"]
    # Product owner in discovery should see neither.
    assert corrections_for("discovery", "product-owner") == []


def test_step_8_all_steps_tickable(tmp_path):
    """Step 8 close-out: regenerating the checklist with every orchestration step checked
    produces a file where those `[x]` survive."""
    workspace = tmp_path
    plan = workspace / "agile-delivery-plan.md"
    plan.write_text(GOOD_PLAN, encoding="utf-8")
    checklist = workspace / "abd-delivery-lead" / "progress" / "delivery-plan-checklist.md"
    _run_script(_GENERATOR, "--plan", str(plan), "--out", str(checklist))
    text = checklist.read_text(encoding="utf-8")
    for step in (
        "Step 1 — Establish workspace",
        "Step 2 — Build the plan",
        "Step 3 — Open first stage of first run",
        "Step 4 — Bootstrap team member",
        "Step 5 — Validate stage exit",
        "Step 6 — Handoff to next stage",
        "Step 7 — Run complete, revise plan",
        "Step 8 — Plan complete",
    ):
        text = text.replace(f"- [ ] **{step}**", f"- [x] **{step}**", 1)
    checklist.write_text(text, encoding="utf-8")

    # Regenerate; all orchestration steps should stay checked.
    _run_script(_GENERATOR, "--plan", str(plan), "--out", str(checklist))
    final = checklist.read_text(encoding="utf-8")
    for step in ("Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "Step 7", "Step 8"):
        assert f"- [x] **{step}" in final, f"{step} lost its check on regeneration"


def test_concurrent_graph_write_is_refused(tmp_path):
    """Cross-stage write safety: two 'team members' try to write the graph
    without coordinating; the second refuses due to the advisory lock."""
    workspace = tmp_path
    _fake_team_member_discovery(workspace)
    graph = workspace / "story-graph.json"

    # Simulate a held lock from another writer.
    lock = graph.with_name(graph.name + ".lock")
    lock.write_text(json.dumps({"pid": 99999, "acquired_at": 1_700_000_000_000, "host": "other"}),
                    encoding="utf-8")
    # Note: timestamp in ms-era would be stale, so use a present value:
    import time
    lock.write_text(json.dumps({"pid": 99999, "acquired_at": time.time(), "host": "other"}),
                    encoding="utf-8")
    try:
        r = subprocess.run(
            [sys.executable, str(_STORY_CLI), "write", "--file", str(graph)],
            input='{"epics": [], "increments": []}',
            capture_output=True, text=True,
        )
        assert r.returncode == 4, r.stderr
        assert "concurrent write refused" in r.stderr
    finally:
        if lock.exists():
            lock.unlink()
