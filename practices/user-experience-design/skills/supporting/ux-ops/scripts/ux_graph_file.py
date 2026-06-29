"""Validated load/save for ``ux-graph.json`` (abd-ux-graph/v1)."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from graph_cli_commands import load_validated_graph, save_validated_graph
from graph_dict_utils import stripped_field

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from ux_map import GRAPH_SCHEMA, VALID_LAYOUTS, VALID_REGION_TYPES, VALID_SLOTS


def _err(path: str, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def _validate_region_dict(region_path: str, region: Dict[str, Any]) -> None:
    if not stripped_field(region, "name"):
        _err(region_path, "region name must be non-empty")
    slot = region["slot"] if "slot" in region else None
    if slot not in VALID_SLOTS:
        _err(region_path, f"slot must be one of {sorted(VALID_SLOTS)}")
    region_type = region["type"] if "type" in region else None
    if region_type not in VALID_REGION_TYPES:
        _err(region_path, f"type must be one of {sorted(VALID_REGION_TYPES)}")


def _validate_regions(path: str, regions: Any, *, required: bool) -> None:
    if regions is None:
        if required:
            _err(path, "regions is required (may be empty)")
        return
    if not isinstance(regions, list):
        _err(path, "regions must be an array")
    for idx, region in enumerate(regions):
        region_path = f"{path}[{idx}]"
        if isinstance(region, str):
            continue
        if not isinstance(region, dict):
            _err(region_path, "region must be an object or string")
        _validate_region_dict(region_path, region)


def _validate_screen(screen_path: str, screen: Dict[str, Any], all_screen_names: Set[str]) -> None:
    name = stripped_field(screen, "name")
    if not name:
        _err(screen_path, "screen name must be non-empty")
    if name in all_screen_names:
        _err(screen_path, f"duplicate screen name '{name}'")
    all_screen_names.add(name)
    if not stripped_field(screen, "slug"):
        _err(screen_path, "slug is required")
    layout = screen["layout"] if "layout" in screen else None
    if layout not in VALID_LAYOUTS:
        _err(screen_path, f"layout must be one of {sorted(VALID_LAYOUTS)}")
    for coord in ("col", "row"):
        if coord not in screen:
            _err(screen_path, f"{coord} is required")
    regions = screen["regions"] if "regions" in screen else None
    _validate_regions(f"{screen_path}.regions", regions, required=True)


def _validate_flow(flow_path: str, flow: Dict[str, Any], all_screen_names: Set[str]) -> None:
    if not stripped_field(flow, "name"):
        _err(flow_path, "flow name must be non-empty")
    screens = flow["screens"] if "screens" in flow else None
    if not isinstance(screens, list):
        _err(f"{flow_path}.screens", "screens must be an array")
    for screen_idx, screen in enumerate(screens):
        screen_path = f"{flow_path}.screens[{screen_idx}]"
        if not isinstance(screen, dict):
            _err(screen_path, "screen must be an object")
        _validate_screen(screen_path, screen, all_screen_names)


def _validate_connection(connection_path: str, connection: Dict[str, Any], all_screen_names: Set[str]) -> None:
    for key in ("from", "to", "label"):
        if not stripped_field(connection, key):
            _err(connection_path, f"connection requires {key}")
    source = stripped_field(connection, "from")
    destination = stripped_field(connection, "to")
    if source not in all_screen_names:
        _err(connection_path, f"connection from '{source}' — no such screen")
    if destination not in all_screen_names:
        _err(connection_path, f"connection to '{destination}' — no such screen")


def _validate_connections(path: str, connections: Any, all_screen_names: Set[str]) -> None:
    if connections is None:
        _err(path, "connections is required (may be empty)")
    if not isinstance(connections, list):
        _err(path, "connections must be an array")
    for idx, connection in enumerate(connections):
        connection_path = f"{path}[{idx}]"
        if not isinstance(connection, dict):
            _err(connection_path, "connection must be an object")
        _validate_connection(connection_path, connection, all_screen_names)


def _validate_flows(flows: List[Any]) -> Set[str]:
    all_screen_names: Set[str] = set()
    for flow_idx, flow in enumerate(flows):
        flow_path = f"flows[{flow_idx}]"
        if not isinstance(flow, dict):
            _err(flow_path, "flow must be an object")
        _validate_flow(flow_path, flow, all_screen_names)
    return all_screen_names


def validate_ux_graph_dict(ux_graph: Dict[str, Any]) -> None:
    if not isinstance(ux_graph, dict):
        raise TypeError("ux graph root must be a JSON object")
    schema = ux_graph["schema"] if "schema" in ux_graph else None
    if schema is not None and schema != GRAPH_SCHEMA:
        _err("schema", f"expected {GRAPH_SCHEMA!r}, got {schema!r}")
    if not stripped_field(ux_graph, "product"):
        _err("product", "product is required")
    if not stripped_field(ux_graph, "scope"):
        _err("scope", "scope is required")
    flows = ux_graph["flows"] if "flows" in ux_graph else None
    if not isinstance(flows, list):
        _err("flows", "flows must be an array")
    all_screen_names = _validate_flows(flows)
    connections = ux_graph["connections"] if "connections" in ux_graph else None
    _validate_connections("connections", connections, all_screen_names)


def load_ux_graph_dict(path: Path | str) -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    return load_validated_graph(file_path, validate_ux_graph_dict)


def save_ux_graph_dict(path: Path | str, ux_graph: Dict[str, Any]) -> None:
    save_validated_graph(Path(path), ux_graph, validate_ux_graph_dict)
