"""Validated load/save for ``story-graph.json`` (same shape as agile_bots graph files)."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
import sys
from pathlib import Path
from typing import Any, Dict

from graph_cli_commands import load_validated_graph, save_validated_graph

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


def _validate_graph_dict(story_graph: Dict[str, Any]) -> None:
    from story_map import Story, StoryMap

    story_map = StoryMap(story_graph)
    for epic in story_map.epics():
        for node in story_map.walk(epic):
            if isinstance(node, Story) and not node.name:
                raise ValueError("Story node with empty name under epic walk")


def load_story_graph_dict(path: Path | str) -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    return load_validated_graph(file_path, _validate_graph_dict)


def save_story_graph_dict(path: Path | str, story_graph: Dict[str, Any]) -> None:
    if not isinstance(story_graph, dict):
        raise TypeError("story graph root must be a dict")
    save_validated_graph(Path(path), story_graph, _validate_graph_dict)
