"""Filter operations on ux-graph JSON dicts."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
from copy import deepcopy
from typing import Any, Dict, List, Set

from graph_dict_utils import stripped_field


def _filter_screens(screens: List[Any], screen_names: Set[str]) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for screen_entry in screens:
        if isinstance(screen_entry, dict) and stripped_field(screen_entry, "name") in screen_names:
            filtered.append(dict(screen_entry))
    return filtered


def _filter_flow_screens(flow_entry: Dict[str, Any], screen_names: Set[str]) -> Dict[str, Any] | None:
    screens = _filter_screens(flow_entry["screens"] if "screens" in flow_entry else [], screen_names)
    if not screens:
        return None
    flow_copy = dict(flow_entry)
    flow_copy["screens"] = screens
    return flow_copy


def _filter_connections(connections: List[Any], screen_names: Set[str]) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for connection_entry in connections:
        if not isinstance(connection_entry, dict):
            continue
        source = stripped_field(connection_entry, "from")
        destination = stripped_field(connection_entry, "to")
        if source in screen_names and destination in screen_names:
            filtered.append(dict(connection_entry))
    return filtered


def filter_ux_graph_to_flow_names(ux_graph: Dict[str, Any], flow_names: Set[str]) -> Dict[str, Any]:
    result = deepcopy(ux_graph)
    result["flows"] = [
        dict(flow_entry)
        for flow_entry in result["flows"] or []
        if isinstance(flow_entry, dict) and stripped_field(flow_entry, "name") in flow_names
    ]
    return result


def filter_ux_graph_to_screen_names(ux_graph: Dict[str, Any], screen_names: Set[str]) -> Dict[str, Any]:
    result = deepcopy(ux_graph)
    flows_out: List[Dict[str, Any]] = []
    for flow_entry in result["flows"] or []:
        if not isinstance(flow_entry, dict):
            continue
        filtered_flow = _filter_flow_screens(flow_entry, screen_names)
        if filtered_flow:
            flows_out.append(filtered_flow)
    result["flows"] = flows_out
    if isinstance(result["connections"], list):
        result["connections"] = _filter_connections(result["connections"], screen_names)
    return result
