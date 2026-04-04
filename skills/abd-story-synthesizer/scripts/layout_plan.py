# =============================================================================
# GENERATED FILE — DO NOT EDIT MANUALLY
# Canonical source: src/drawio/layout_plan.py
# Regenerate from repo root: python scripts/sync_drawio_vendor.py
# Generated at: 2026-04-02T14:30:24+00:00
# =============================================================================
"""
Logical layout plan for class diagrams — clusters and flow, no pixel coordinates.

Emitted JSON (e.g. ``class-diagram-layout-plan.json``) is optional; the emitter
turns it into x/y using fixed geometry constants.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

COL_WIDTH = 280
MIN_ROW_HEIGHT = 100
GAP_WITHIN = 20
GAP_CLUSTER = 80
START_X = 40
START_Y = 40
UNASSIGNED_TOP_GAP = 60
COLS_PER_ROW_UNASSIGNED = 5


def load_layout_plan(path: Path | None) -> dict[str, Any] | None:
    """Load JSON layout plan from path; return None if missing or unusable."""
    if path is None or not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        print(f"class-diagram layout plan: ignored ({path}): {e}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        print("class-diagram layout plan: root must be an object, ignoring", file=sys.stderr)
        return None
    ver = data.get("schema_version")
    if ver != 1:
        print(
            f"class-diagram layout plan: schema_version must be 1 (got {ver!r}), ignoring",
            file=sys.stderr,
        )
        return None
    return data


def _name_to_concept(modules: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for mod in modules:
        for c in mod.get("concepts") or []:
            n = (c.get("name") or "").strip()
            if n:
                out[n] = c
    return out


def _cluster_id_order(clusters: list[dict[str, Any]], cluster_order: list[str] | None) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    id_from_decl = [str(c["id"]).strip() for c in clusters if c.get("id")]
    if cluster_order:
        for cid in cluster_order:
            cid = str(cid).strip()
            if cid and cid in id_from_decl and cid not in seen:
                out.append(cid)
                seen.add(cid)
    for cid in id_from_decl:
        if cid not in seen:
            out.append(cid)
            seen.add(cid)
    return out


def compute_positions_from_plan(
    modules: list[dict[str, Any]],
    layout_plan: dict[str, Any],
    concept_height: Callable[[dict[str, Any]], float],
) -> dict[str, tuple[float, float]] | None:
    """
    Map-model modules + layout plan → pixel positions for each concept name.

    Returns None if the plan should be ignored (empty clusters, bad shape).
    Always assigns every concept in ``modules`` (unlisted names go in a grid below clusters).
    """
    clusters_raw = layout_plan.get("clusters")
    if not isinstance(clusters_raw, list) or len(clusters_raw) == 0:
        return None

    clusters: list[dict[str, Any]] = [c for c in clusters_raw if isinstance(c, dict) and c.get("id")]
    if not clusters:
        return None

    name_to_concept = _name_to_concept(modules)
    co = layout_plan.get("cluster_order")
    cluster_order: list[str] | None = co if isinstance(co, list) else None
    order_ids = _cluster_id_order(clusters, cluster_order)
    id_to_cluster = {str(c["id"]).strip(): c for c in clusters if c.get("id")}

    orientation = layout_plan.get("orientation") or "clusters_horizontal"
    if orientation not in ("clusters_horizontal", "clusters_vertical"):
        orientation = "clusters_horizontal"

    within = layout_plan.get("within_cluster") or "row"
    if within not in ("row", "column"):
        within = "row"

    positions: dict[str, tuple[float, float]] = {}
    placed: set[str] = set()

    def warn_skip(name: str, reason: str) -> None:
        print(f"class-diagram layout plan: skip {name!r} ({reason})", file=sys.stderr)

    if orientation == "clusters_horizontal":
        cx, cy = float(START_X), float(START_Y)
        for cid in order_ids:
            cl = id_to_cluster.get(cid)
            if not cl:
                continue
            members_raw = cl.get("members")
            if not isinstance(members_raw, list):
                continue
            members: list[str] = []
            for m in members_raw:
                n = str(m).strip()
                if not n:
                    continue
                if n not in name_to_concept:
                    warn_skip(n, "unknown concept")
                    continue
                if n in placed:
                    warn_skip(n, "duplicate across clusters")
                    continue
                members.append(n)

            if not members:
                continue

            if within == "row":
                lx, ly = cx, cy
                row_max_h = 0.0
                for name in members:
                    h = concept_height(name_to_concept[name])
                    positions[name] = (lx, ly)
                    placed.add(name)
                    lx += COL_WIDTH + GAP_WITHIN
                    row_max_h = max(row_max_h, h)
                cluster_w = len(members) * COL_WIDTH + max(0, len(members) - 1) * GAP_WITHIN
                cluster_h = row_max_h
            else:
                lx, ly = cx, cy
                for i, name in enumerate(members):
                    h = concept_height(name_to_concept[name])
                    positions[name] = (lx, ly)
                    placed.add(name)
                    ly += h
                    if i < len(members) - 1:
                        ly += GAP_WITHIN
                cluster_w = float(COL_WIDTH)
                cluster_h = ly - cy

            cx += cluster_w + GAP_CLUSTER

    else:  # clusters_vertical
        cx, cy = float(START_X), float(START_Y)
        for cid in order_ids:
            cl = id_to_cluster.get(cid)
            if not cl:
                continue
            members_raw = cl.get("members")
            if not isinstance(members_raw, list):
                continue
            members = []
            for m in members_raw:
                n = str(m).strip()
                if not n or n not in name_to_concept:
                    if n and n not in name_to_concept:
                        warn_skip(n, "unknown concept")
                    continue
                if n in placed:
                    warn_skip(n, "duplicate across clusters")
                    continue
                members.append(n)

            if not members:
                continue

            if within == "row":
                lx, ly = cx, cy
                row_max_h = 0.0
                for name in members:
                    h = concept_height(name_to_concept[name])
                    positions[name] = (lx, ly)
                    placed.add(name)
                    lx += COL_WIDTH + GAP_WITHIN
                    row_max_h = max(row_max_h, h)
                cluster_w = len(members) * COL_WIDTH + max(0, len(members) - 1) * GAP_WITHIN
                cluster_h = row_max_h
            else:
                lx, ly = cx, cy
                for i, name in enumerate(members):
                    h = concept_height(name_to_concept[name])
                    positions[name] = (lx, ly)
                    placed.add(name)
                    ly += h
                    if i < len(members) - 1:
                        ly += GAP_WITHIN
                cluster_w = float(COL_WIDTH)
                cluster_h = ly - cy

            cy += cluster_h + GAP_CLUSTER

    # Unassigned: grid below lowest cell
    max_bottom = float(START_Y)
    for name, (px, py) in positions.items():
        h = concept_height(name_to_concept[name])
        max_bottom = max(max_bottom, py + h)

    y0 = max_bottom + UNASSIGNED_TOP_GAP
    x, y = float(START_X), y0
    row_max_h = 0.0
    unassigned = sorted(
        (c for m in modules for c in m.get("concepts") or [] if c.get("name") not in positions),
        key=lambda c: str(c.get("name") or ""),
    )
    for j, concept in enumerate(unassigned):
        nm = str(concept.get("name") or "").strip()
        if not nm:
            continue
        h = concept_height(concept)
        positions[nm] = (x, y)
        row_max_h = max(row_max_h, h)
        x += COL_WIDTH
        if (j + 1) % COLS_PER_ROW_UNASSIGNED == 0:
            x = float(START_X)
            y += max(float(MIN_ROW_HEIGHT), row_max_h) + 20.0
            row_max_h = 0.0

    return positions
