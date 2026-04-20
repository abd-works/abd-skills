"""Hierarchy diff and StoryMapUpdater.generate_report_from (no DrawIO)."""
from __future__ import annotations

import copy

from story_graph_ops.nodes import StoryMap
from story_graph_ops.story_graph_diff import diff_hierarchy_epics
from story_graph_ops.story_map_updater import StoryMapUpdater
from story_graph_ops.update_report import UpdateReport

_MINIMAL = {
    "epics": [
        {
            "name": "Epic A",
            "sequential_order": 1.0,
            "sub_epics": [
                {
                    "name": "Sub A",
                    "sequential_order": 1.0,
                    "story_groups": [
                        {
                            "name": None,
                            "stories": [{"name": "Story One", "sequential_order": 1.0}],
                        }
                    ],
                }
            ],
        }
    ],
    "increments": [],
}


def test_comparison_epics_matches_epics_list() -> None:
    m = StoryMap(copy.deepcopy(_MINIMAL))
    assert [e.name for e in m.comparison_epics()] == [e.name for e in m._epics_list]


def test_diff_identical_maps_counts_matches() -> None:
    a = StoryMap(copy.deepcopy(_MINIMAL))
    b = StoryMap(copy.deepcopy(_MINIMAL))
    report = UpdateReport()
    diff_hierarchy_epics(a, b, report)
    assert report.matched_count == 3  # epic, sub-epic, story
    assert not report.has_changes


def test_generate_report_from_detects_new_story() -> None:
    target = StoryMap(copy.deepcopy(_MINIMAL))
    source_graph = copy.deepcopy(_MINIMAL)
    source_graph["epics"][0]["sub_epics"][0]["story_groups"][0]["stories"].append(
        {"name": "Story Two", "sequential_order": 2.0}
    )
    source = StoryMap(source_graph)
    updater = StoryMapUpdater(target_map=target)
    report = updater.generate_report_from(source)
    names = {s.name for s in report.new_stories}
    assert "Story Two" in names


def test_generate_report_from_detects_removed_story() -> None:
    target_graph = copy.deepcopy(_MINIMAL)
    target_graph["epics"][0]["sub_epics"][0]["story_groups"][0]["stories"].append(
        {"name": "Story Two", "sequential_order": 2.0}
    )
    target = StoryMap(target_graph)
    source = StoryMap(copy.deepcopy(_MINIMAL))
    updater = StoryMapUpdater(target_map=target)
    report = updater.generate_report_from(source)
    names = {s.name for s in report.removed_stories}
    assert "Story Two" in names
