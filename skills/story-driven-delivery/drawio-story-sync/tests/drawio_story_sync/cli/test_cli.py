"""Drawio Story Sync → CLI

Story Path: Drawio Story Sync → CLI (drawio_story_sync_cli subprocess contract).

Folder ``cli`` = lowest sub-epic (ATDD). File is ``test_cli.py`` so pytest discovers tests.

Behaviors: outline render; outline sync refreshes exploration and increments;
increments-diagram sync refreshes companions using outline stem; CLI stem helper.
"""
from __future__ import annotations

from pathlib import Path


from ..drawio_story_sync_helper import (
    requires_story_graph_ops,
    given_cli_pythonpath_env,
    given_minimal_story_graph_file,
    given_story_graph_file_with_one_increment,
    when_cli_runs_render_outline,
    when_cli_runs_render_increments,
    when_cli_runs_sync_outline,
    when_cli_runs_sync_with_diagram_type,
    when_cli_module_is_loaded,
    then_subprocess_succeeded,
    then_last_stdout_line_is_ok_json,
    then_drawio_file_exists_and_has_min_size,
    then_payload_refreshed_diagrams_include,
    then_story_graph_cli_read_succeeds,
)

pytestmark = requires_story_graph_ops


# =============================================================================
# STORY: Drawio Cli Renders Outline
# =============================================================================


class TestDrawioCliRendersOutline:
    """CLI renders a non-trivial outline DrawIO from a minimal story graph."""

    def test_outline_render_produces_drawio_and_ok_status(self, tmp_path: Path) -> None:
        env = given_cli_pythonpath_env()
        graph = given_minimal_story_graph_file(tmp_path)
        out = tmp_path / "smoke.drawio"
        proc = when_cli_runs_render_outline(graph, out, env)
        then_subprocess_succeeded(proc)
        then_drawio_file_exists_and_has_min_size(out)
        then_last_stdout_line_is_ok_json(proc)


# =============================================================================
# STORY: Drawio Cli Sync Refreshes Exploration And Increments
# =============================================================================


class TestDrawioCliSyncRefreshesExplorationAndIncrements:
    """Outline sync refreshes -exploration and -increments beside the outline stem."""

    def test_outline_sync_refreshes_companion_diagrams(self, tmp_path: Path) -> None:
        env = given_cli_pythonpath_env()
        graph = given_minimal_story_graph_file(tmp_path)
        outline = tmp_path / "story-map.drawio"
        exploration = tmp_path / "story-map-exploration.drawio"
        increments = tmp_path / "story-map-increments.drawio"
        proc_render = when_cli_runs_render_outline(graph, outline, env)
        then_subprocess_succeeded(proc_render)
        proc_sync = when_cli_runs_sync_outline(outline, graph, env)
        then_subprocess_succeeded(proc_sync)
        then_last_stdout_line_is_ok_json(proc_sync)
        then_payload_refreshed_diagrams_include(proc_sync, (exploration, increments))
        then_drawio_file_exists_and_has_min_size(exploration)
        then_drawio_file_exists_and_has_min_size(increments)
        then_story_graph_cli_read_succeeds(graph)


# =============================================================================
# STORY: Drawio Cli Sync From Increments Diagram Refreshes Outline Stem Companions
# =============================================================================


class TestDrawioCliSyncFromIncrementsDiagramRefreshesOutlineStemCompanions:
    """Sync with --diagram-type increments still writes exploration/increments under outline stem."""

    def test_increments_source_sync_refreshes_story_map_exploration_and_increments(
        self, tmp_path: Path
    ) -> None:
        env = given_cli_pythonpath_env()
        graph = given_story_graph_file_with_one_increment(tmp_path)
        outline = tmp_path / "story-map.drawio"
        inc_drawio = tmp_path / "story-map-increments.drawio"
        exploration = tmp_path / "story-map-exploration.drawio"
        increments = tmp_path / "story-map-increments.drawio"
        then_subprocess_succeeded(when_cli_runs_render_outline(graph, outline, env))
        then_subprocess_succeeded(when_cli_runs_render_increments(graph, inc_drawio, env))
        proc_sync = when_cli_runs_sync_with_diagram_type(
            inc_drawio, graph, "increments", env
        )
        then_subprocess_succeeded(proc_sync)
        then_payload_refreshed_diagrams_include(proc_sync, (exploration, increments))
        then_story_graph_cli_read_succeeds(graph)


# =============================================================================
# STORY: Drawio Story Sync Cli Companion Stem Resolution
# =============================================================================


class TestDrawioStorySyncCliCompanionStemResolution:
    """Pure helpers on drawio_story_sync_cli: companion stem for refresh paths."""

    def test_companion_stem_strips_increments_suffix(self) -> None:
        mod = when_cli_module_is_loaded()
        stem = mod._companion_stem(Path("x/y/story-map-increments.drawio"))
        assert stem == "story-map"

    def test_diagram_type_for_load_maps_exploration_to_acceptance_criteria(self) -> None:
        mod = when_cli_module_is_loaded()
        assert mod._diagram_type_for_load("exploration") == "acceptance_criteria"
        assert mod._diagram_type_for_load("increments") == "increments"
