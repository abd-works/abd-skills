"""Round-trip and validation for :mod:`story_graph_file`."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from story_graph_file import load_story_graph_dict, save_story_graph_dict

_MINIMAL = {
    "epics": [
        {
            "name": "Epic A",
            "sub_epics": [
                {
                    "name": "Sub A",
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


def test_load_save_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "story-graph.json"
    save_story_graph_dict(p, _MINIMAL)
    back = load_story_graph_dict(p)
    assert back["epics"][0]["name"] == "Epic A"
    assert json.loads(p.read_text(encoding="utf-8")) == back


def test_load_rejects_empty_story_name(tmp_path: Path) -> None:
    bad = {
        "epics": [
            {
                "name": "E",
                "sub_epics": [
                    {
                        "name": "S",
                        "story_groups": [
                            {"name": None, "stories": [{"name": "", "sequential_order": 1.0}]}
                        ],
                    }
                ],
            }
        ],
    }
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="empty name"):
        load_story_graph_dict(p)
