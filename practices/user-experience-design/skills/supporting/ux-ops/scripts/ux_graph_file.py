"""Validated load/save for ``ux-graph.json`` (abd-ux-graph/v1)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from ux_map import GRAPH_SCHEMA, VALID_LAYOUTS, VALID_REGION_TYPES, VALID_SLOTS


def _err(path: str, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def _validate_regions(path: str, regions: Any, *, required: bool) -> None:
    if regions is None:
        if required:
            _err(path, "regions is required (may be empty)")
        return
    if not isinstance(regions, list):
        _err(path, "regions must be an array")
    for idx, region in enumerate(regions):
        rp = f"{path}[{idx}]"
        if isinstance(region, str):
            continue
        if not isinstance(region, dict):
            _err(rp, "region must be an object or string")
        if not str(region.get("name", "")).strip():
            _err(rp, "region name must be non-empty")
        slot = region.get("slot")
        if slot not in VALID_SLOTS:
            _err(rp, f"slot must be one of {sorted(VALID_SLOTS)}")
        rtype = region.get("type")
        if rtype not in VALID_REGION_TYPES:
            _err(rp, f"type must be one of {sorted(VALID_REGION_TYPES)}")


def validate_ux_graph_dict(data: Dict[str, Any]) -> None:
    """Validate abd-ux-graph/v1."""
    if not isinstance(data, dict):
        raise TypeError("ux graph root must be a JSON object")
    schema = data.get("schema")
    if schema is not None and schema != GRAPH_SCHEMA:
        _err("schema", f"expected {GRAPH_SCHEMA!r}, got {schema!r}")
    if not str(data.get("product", "")).strip():
        _err("product", "product is required")
    if not str(data.get("scope", "")).strip():
        _err("scope", "scope is required")
    flows = data.get("flows")
    if not isinstance(flows, list):
        _err("flows", "flows must be an array")
    all_screen_names: Set[str] = set()
    for fidx, flow in enumerate(flows):
        fp = f"flows[{fidx}]"
        if not isinstance(flow, dict):
            _err(fp, "flow must be an object")
        if not str(flow.get("name", "")).strip():
            _err(fp, "flow name must be non-empty")
        screens = flow.get("screens")
        if not isinstance(screens, list):
            _err(f"{fp}.screens", "screens must be an array")
        for sidx, screen in enumerate(screens):
            sp = f"{fp}.screens[{sidx}]"
            if not isinstance(screen, dict):
                _err(sp, "screen must be an object")
            name = str(screen.get("name", "")).strip()
            if not name:
                _err(sp, "screen name must be non-empty")
            if name in all_screen_names:
                _err(sp, f"duplicate screen name '{name}'")
            all_screen_names.add(name)
            if not str(screen.get("slug", "")).strip():
                _err(sp, "slug is required")
            if screen.get("layout") not in VALID_LAYOUTS:
                _err(sp, f"layout must be one of {sorted(VALID_LAYOUTS)}")
            for coord in ("col", "row"):
                if coord not in screen:
                    _err(sp, f"{coord} is required")
            _validate_regions(f"{sp}.regions", screen.get("regions"), required=True)
    connections = data.get("connections")
    if connections is None:
        _err("connections", "connections is required (may be empty)")
    if not isinstance(connections, list):
        _err("connections", "connections must be an array")
    for idx, conn in enumerate(connections):
        cp = f"connections[{idx}]"
        if not isinstance(conn, dict):
            _err(cp, "connection must be an object")
        for key in ("from", "to", "label"):
            if not str(conn.get(key, "")).strip():
                _err(cp, f"connection requires {key}")
        src, dst = conn.get("from"), conn.get("to")
        if src not in all_screen_names:
            _err(cp, f"connection from '{src}' — no such screen")
        if dst not in all_screen_names:
            _err(cp, f"connection to '{dst}' — no such screen")


def load_ux_graph_dict(path: Path | str) -> Dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    data = json.loads(p.read_text(encoding="utf-8"))
    validate_ux_graph_dict(data)
    return data


def save_ux_graph_dict(path: Path | str, data: Dict[str, Any]) -> None:
    validate_ux_graph_dict(data)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
