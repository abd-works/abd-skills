"""
Scanner Runner Tests

Tests for load_workspace_graph_json and _violations_exit_code behaviors.
Stories: Load Story Graph, Report Violations.
"""
import json
import sys
from io import StringIO
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[4] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from scanner_runner import _violations_exit_code, load_workspace_graph_json

STANDARD_GRAPH = {
    "epics": [{"name": "Manage Orders", "sub_epics": []}],
    "increments": [],
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def given_graph_at(workspace: Path, *rel_parts: str) -> Path:
    graph_path = workspace.joinpath(*rel_parts)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(STANDARD_GRAPH), encoding="utf-8")
    return graph_path


def when_graph_is_loaded(workspace: Path, story_graph: Path | None = None) -> dict:
    return load_workspace_graph_json(workspace, story_graph)


def then_graph_matches_standard(result: dict) -> None:
    assert result == STANDARD_GRAPH


def then_graph_is_empty(result: dict) -> None:
    assert result == {"epics": [], "increments": []}


def when_violations_reported(violations: list, capsys) -> int:
    return _violations_exit_code(violations)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    return ws


# ============================================================================
# STORY: Load Story Graph
# ============================================================================


class TestLoadStoryGraph:
    """Load Story Graph — scanner runner resolves story-graph.json from workspace."""

    def test_loads_graph_from_explicit_path(self, workspace: Path) -> None:
        # Given: graph exists at an arbitrary nested location
        graph_path = given_graph_at(workspace, "docs", "stories", "story-graph.json")

        # When: loaded with explicit path
        result = when_graph_is_loaded(workspace, story_graph=graph_path)

        # Then: standard graph returned
        then_graph_matches_standard(result)

    def test_finds_graph_nested_deep_without_explicit_path(self, workspace: Path) -> None:
        # Given: graph buried several levels deep — no hardcoded location
        given_graph_at(workspace, "a", "b", "c", "story-graph.json")

        # When: loaded with workspace only (recursive fallback)
        result = when_graph_is_loaded(workspace)

        # Then: standard graph returned
        then_graph_matches_standard(result)

    def test_finds_graph_at_workspace_root(self, workspace: Path) -> None:
        # Given: graph sits at the workspace root
        given_graph_at(workspace, "story-graph.json")

        # When: loaded with workspace only
        result = when_graph_is_loaded(workspace)

        # Then: standard graph returned
        then_graph_matches_standard(result)

    def test_explicit_path_takes_precedence_over_workspace_search(self, workspace: Path) -> None:
        # Given: two graphs — one at workspace root, one elsewhere
        other_graph = workspace / "other" / "story-graph.json"
        other_graph.parent.mkdir(parents=True)
        other_graph.write_text(json.dumps({"epics": [], "increments": []}), encoding="utf-8")
        target = given_graph_at(workspace, "docs", "story-graph.json")

        # When: explicit path points to the target
        result = when_graph_is_loaded(workspace, story_graph=target)

        # Then: the explicit graph is used, not the workspace root one
        then_graph_matches_standard(result)

    def test_returns_empty_graph_when_none_found(self, workspace: Path) -> None:
        # Given: workspace has no story-graph.json

        # When
        result = when_graph_is_loaded(workspace)

        # Then: empty graph returned instead of crashing
        then_graph_is_empty(result)


# ============================================================================
# STORY: Report Violations
# ============================================================================


class TestReportViolations:
    """Report Violations — _violations_exit_code writes to stderr and signals failure."""

    def test_returns_exit_code_1_when_violations_present(self, capsys) -> None:
        # Given: a violation as a dict
        violations = [{"violation_message": "AC missing WHEN clause", "severity": "error"}]

        # When
        exit_code = _violations_exit_code(violations)

        # Then: non-zero exit signals failure
        assert exit_code == 1

    def test_returns_exit_code_0_when_no_violations(self, capsys) -> None:
        # Given: no violations

        # When
        exit_code = _violations_exit_code([])

        # Then: zero exit signals clean
        assert exit_code == 0

    def test_writes_violations_to_stderr_not_stdout(self, capsys) -> None:
        # Given: a violation
        violations = [{"violation_message": "Actor not alternating", "severity": "error"}]

        # When
        _violations_exit_code(violations)

        # Then: violation appears on stderr, stdout is clean
        captured = capsys.readouterr()
        assert "Actor not alternating" in captured.err
        assert captured.out == ""

    def test_each_violation_is_a_separate_stderr_line(self, capsys) -> None:
        # Given: two violations
        violations = [
            {"violation_message": "First violation", "severity": "error"},
            {"violation_message": "Second violation", "severity": "warning"},
        ]

        # When
        _violations_exit_code(violations)

        # Then: both appear on stderr
        captured = capsys.readouterr()
        assert "First violation" in captured.err
        assert "Second violation" in captured.err
