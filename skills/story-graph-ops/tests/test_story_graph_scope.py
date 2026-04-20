"""Tests for ``story_graph_ops.story_graph_scope`` (vendored scope filters)."""

from pathlib import Path

import pytest

from story_graph_ops.story_graph_scope import (
    ScopeType,
    StoryGraphFilter,
    StoryGraphScope,
)


def test_story_graph_filter_increment_limits_epics_and_increments():
    graph = {
        'epics': [
            {
                'name': 'E1',
                'sub_epics': [
                    {
                        'name': 'SE1',
                        'story_groups': [{'name': None, 'stories': [{'name': 'S1'}]}],
                    }
                ],
            }
        ],
        'increments': [
            {'name': 'Lane A', 'priority': 1, 'stories': [{'name': 'S1'}]},
            {'name': 'Lane B', 'priority': 2, 'stories': [{'name': 'Other'}]},
        ],
    }
    flt = StoryGraphFilter(increments=['Lane A'])
    out = flt.filter_story_graph(graph)
    assert len(out['increments']) == 1
    assert out['increments'][0]['name'] == 'Lane A'
    assert out['epics'] and out['epics'][0]['sub_epics']


def test_story_graph_scope_filters_story_graph_dict(tmp_path: Path):
    sg = tmp_path / 'docs' / 'story' / 'story-graph.json'
    sg.parent.mkdir(parents=True)
    sg.write_text(
        '{"epics":[{"name":"Epic","sub_epics":[{"name":"Sub","story_groups":'
        '[{"name":null,"stories":[{"name":"KeepMe"}]}]}]}],"increments":[]}',
        encoding='utf-8',
    )
    scope = StoryGraphScope(tmp_path)
    scope.filter(ScopeType.STORY, ['KeepMe'])
    data = scope.filtered_story_graph
    assert data is not None
    assert data['epics'][0]['name'] == 'Epic'
