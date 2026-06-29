"""Filter operations on ux-graph JSON dicts."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Set


def _filter_screens(screens: List[Any], screen_names: Set[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for screen in screens:
        if isinstance(screen, dict) and screen.get("name") in screen_names:
            out.append(dict(screen))
    return out


def filter_ux_graph_to_flow_names(graph: Dict[str, Any], flow_names: Set[str]) -> Dict[str, Any]:
    data = deepcopy(graph)
    data["flows"] = [
        dict(f)
        for f in data.get("flows") or []
        if isinstance(f, dict) and f.get("name") in flow_names
    ]
    return data


def filter_ux_graph_to_screen_names(graph: Dict[str, Any], screen_names: Set[str]) -> Dict[str, Any]:
    data = deepcopy(graph)
    flows_out: List[Dict[str, Any]] = []
    for flow in data.get("flows") or []:
        if not isinstance(flow, dict):
            continue
        screens = _filter_screens(flow.get("screens") or [], screen_names)
        if screens:
            fo = dict(flow)
            fo["screens"] = screens
            flows_out.append(fo)
    data["flows"] = flows_out
    if isinstance(data.get("connections"), list):
        data["connections"] = [
            c for c in data["connections"]
            if isinstance(c, dict)
            and c.get("from") in screen_names
            and c.get("to") in screen_names
        ]
    return data
