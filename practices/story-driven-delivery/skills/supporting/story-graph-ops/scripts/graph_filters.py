"""Filter and subset operations on raw story-graph JSON dicts."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
from copy import deepcopy
from typing import Any, Dict, Optional, Set

from graph_dict_utils import dict_object_list, stripped_field


def _filter_story_group_dict(
    story_group: Dict[str, Any],
    story_names: Set[str],
) -> Optional[Dict[str, Any]]:
    stories = [
        story_entry
        for story_entry in dict_object_list(story_group, "stories")
        if stripped_field(story_entry, "name") in story_names
    ]
    if not stories:
        return None
    filtered_group = dict(story_group)
    filtered_group["stories"] = stories
    return filtered_group


def _filter_sub_epic_dict(
    sub_epic: Dict[str, Any],
    story_names: Set[str],
) -> Optional[Dict[str, Any]]:
    nested_sub_epics = []
    for child in dict_object_list(sub_epic, "sub_epics"):
        filtered_child = _filter_sub_epic_dict(child, story_names)
        if filtered_child:
            nested_sub_epics.append(filtered_child)
    story_groups = []
    for story_group in dict_object_list(sub_epic, "story_groups"):
        filtered_group = _filter_story_group_dict(story_group, story_names)
        if filtered_group:
            story_groups.append(filtered_group)
    if nested_sub_epics or story_groups:
        filtered_sub_epic = dict(sub_epic)
        filtered_sub_epic["sub_epics"] = nested_sub_epics
        filtered_sub_epic["story_groups"] = story_groups
        return filtered_sub_epic
    return None


def _filter_epic_dict(epic: Dict[str, Any], story_names: Set[str]) -> Optional[Dict[str, Any]]:
    nested_sub_epics = []
    for sub_epic in dict_object_list(epic, "sub_epics"):
        filtered_sub_epic = _filter_sub_epic_dict(sub_epic, story_names)
        if filtered_sub_epic:
            nested_sub_epics.append(filtered_sub_epic)
    story_groups = []
    for story_group in dict_object_list(epic, "story_groups"):
        filtered_group = _filter_story_group_dict(story_group, story_names)
        if filtered_group:
            story_groups.append(filtered_group)
    if nested_sub_epics or story_groups:
        filtered_epic = dict(epic)
        filtered_epic["sub_epics"] = nested_sub_epics
        filtered_epic["story_groups"] = story_groups
        return filtered_epic
    return None


def filter_story_graph_to_story_names(
    story_graph: Dict[str, Any],
    story_names: Set[str],
) -> Dict[str, Any]:
    result = deepcopy(story_graph)
    filtered_epics = []
    for epic_entry in dict_object_list(result, "epics"):
        filtered_epic = _filter_epic_dict(epic_entry, story_names)
        if filtered_epic:
            filtered_epics.append(filtered_epic)
    result["epics"] = filtered_epics
    return result
