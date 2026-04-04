#!/usr/bin/env python3
# =============================================================================
# GENERATED FILE — DO NOT EDIT MANUALLY
# Canonical source: src/drawio/model_to_drawio.py
# Regenerate from repo root: python scripts/sync_drawio_vendor.py
# Generated at: 2026-04-02T14:30:24+00:00
# =============================================================================
"""
CANONICAL SOURCE — edit only in agilebydesign-skills/src/drawio/model_to_drawio.py

Copies under skills/*/scripts/ are generated; do not edit them by hand.
Regenerate: python scripts/sync_drawio_vendor.py (from repo root)

Generate DrawIO UML class diagrams.

Primary input — **map-model-spec.json** (e.g. ``abd-answers/spec/map-model-spec.json``):
  - ``modules_and_epics`` → modules with ``concepts`` (``name``, optional ``Base:Subtype`` in ``name``,
    ``properties``, ``operations``).
  - Optional ``cross_module_relationships``: ``{from, to, type}``.

Optional **class-diagram-layout-plan.json** (same directory as spec or passed explicitly):
  - Logical clusters and flow only (no x/y); emitter assigns geometry. If absent or invalid,
    layout falls back to tier + grid from inheritance.

Alternate input — **domain-model.md** (markdown, for other workspaces / legacy):
  # Module: X
  ## ClassName : BaseClass
  - property : Type
  - operation() → ReturnType
  Plus the Relationships table for edges.

Usage (ABD Answers — JSON only):
  python model_to_drawio.py path/to/map-model-spec.json [-o map-model-classes.drawio]
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

# Add scripts dir for drawio_tools import
_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from drawio_tools import (
    load_drawio,
    save_drawio,
    create_empty_mxfile,
    get_page,
    add_page,
    find_cell_by_name,
    create_class_cell,
    create_edge,
    next_id,
    calc_cell_height,
)

from layout_plan import compute_positions_from_plan, load_layout_plan


# Domain model format: - name : Type or - name : Type (desc)
PROP_RE = re.compile(r"^-\s+(.+?)\s*:\s*(.+?)(?:\s*\([^)]*\))?\s*$")
# - op() → Return or - op(args) → Return
OP_RE = re.compile(r"^-\s+(.+?)\s*→\s*(.+?)\s*$")
# - op(args) or - op() without return
OP_NO_RETURN_RE = re.compile(r"^-\s+(\w+\([^)]*\))\s*$")
# ## ClassName or ## ClassName : Base
CLASS_HEADING = re.compile(r"^#+\s+(?:Module:\s*)?(.+)$")
CLASS_WITH_BASE = re.compile(r"^(.+?)\s*:\s*(.+)$")


def parse_domain_model(content: str):
    """Parse domain-model.md into modules, concepts, and relationships."""
    modules = []
    relationships = []
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Module: # Module: Name
        mod_match = re.match(r"^#\s+Module:\s*(.+)$", stripped, re.I)
        if mod_match:
            mod_name = mod_match.group(1).strip()
            mod = {"name": mod_name, "concepts": []}
            modules.append(mod)
            i += 1
            continue

        # Relationships table row: | From | To | Type |
        if stripped.startswith("|") and "---" not in stripped and "From" not in stripped:
            parts = [p.strip() for p in stripped.split("|") if p.strip()]
            if len(parts) >= 3:
                relationships.append({"from": parts[0], "to": parts[1], "type": parts[2]})
            i += 1
            continue

        # Class: ## ClassName or ## ClassName : Base
        class_match = re.match(r"^##\s+(.+)$", stripped)
        if class_match and not stripped.startswith("## Module"):
            raw = class_match.group(1).strip()
            base = None
            if " : " in raw:
                parts = raw.split(" : ", 1)
                name = parts[0].strip()
                base = parts[1].strip()
            else:
                name = raw

            # Skip Relationships, Aggregate root, etc.
            if name in ("Relationships", "Aggregate root") or name.startswith("**"):
                i += 1
                continue

            concept = {"name": name, "base": base, "properties": [], "operations": [], "stereotype": None}
            mod = modules[-1] if modules else None
            if mod:
                mod["concepts"].append(concept)

            i += 1
            while i < len(lines):
                ln = lines[i]
                s = ln.strip()
                # Next class or module
                if re.match(r"^#+\s+", ln) and not s.startswith("-"):
                    break
                # [foundational] or [value object]
                if s.startswith("[") and s.endswith("]"):
                    concept["stereotype"] = s[1:-1]
                    i += 1
                    continue
                # Property: - name : Type
                prop_m = PROP_RE.match(s)
                if prop_m:
                    left, right = prop_m.group(1).strip(), prop_m.group(2).strip()
                    # op() → Return has no colon before arrow in left
                    if "()" in left or "(" in left:
                        op_m = OP_RE.match(s)
                        if op_m:
                            concept["operations"].append(f"{op_m.group(1).strip()} → {op_m.group(2).strip()}")
                    else:
                        concept["properties"].append(f"{left} : {right}")
                    i += 1
                    continue
                # Operation: - op() → Return
                op_m = OP_RE.match(s)
                if op_m:
                    concept["operations"].append(f"{op_m.group(1).strip()} → {op_m.group(2).strip()}")
                    i += 1
                    continue
                # Operation without return: - op(args)
                op_no_ret = OP_NO_RETURN_RE.match(s)
                if op_no_ret:
                    concept["operations"].append(op_no_ret.group(1).strip())
                    i += 1
                    continue
                # Empty or other
                if not s or s.startswith("|") or s.startswith("---"):
                    i += 1
                    continue
                i += 1
            continue

        # Relationships table header
        if "| From" in stripped and "| To" in stripped:
            i += 1
            continue

        i += 1

    return modules, relationships


def _format_prop_item(p):
    if isinstance(p, str):
        return p
    if isinstance(p, dict):
        n = (p.get("name") or "").strip()
        t = (p.get("type") or "").strip()
        return f"{n} : {t}" if t else n
    return str(p)


def _format_op_item(o):
    if isinstance(o, str):
        return o
    if isinstance(o, dict):
        name = (o.get("name") or o.get("signature") or "").strip()
        ret = (o.get("return") or o.get("returns") or "").strip()
        if name and ret:
            return f"{name} → {ret}"
        return name or str(o)
    return str(o)


def _depends_on_targets(obj: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for d in obj.get("depends_on") or []:
        if isinstance(d, dict):
            c = d.get("concept")
            if c:
                t = str(c).strip()
                if t:
                    out.append(t)
    return out


def parse_map_model_spec_data(data: dict[str, Any]) -> tuple[list, list]:
    """Parse map-model-spec dict into modules + relationships (same as JSON file load)."""
    modules = []
    relationships: list[dict[str, str]] = []
    dep_seen: set[tuple[str, str]] = set()

    def add_dependency(frm: str, to: str) -> None:
        key = (frm, to)
        if key in dep_seen:
            return
        dep_seen.add(key)
        relationships.append({"from": frm, "to": to, "type": "dependency"})

    for block in data.get("modules_and_epics") or []:
        mod_data = block.get("module") or {}
        mod_name = (mod_data.get("name") or "").strip()
        if not mod_name:
            continue
        mod = {"name": mod_name, "concepts": []}
        for raw in mod_data.get("concepts") or []:
            raw_name = (raw.get("name") or "").strip()
            if not raw_name:
                continue
            base = None
            display_name = raw_name
            if ":" in raw_name:
                parent, child = raw_name.split(":", 1)
                parent, child = parent.strip(), child.strip()
                if parent and child:
                    base = parent
                    display_name = child
                    relationships.append(
                        {"from": parent, "to": child, "type": "inheritance"}
                    )
            concept = {
                "name": display_name,
                "base": base,
                "properties": [_format_prop_item(p) for p in raw.get("properties") or []],
                "operations": [_format_op_item(o) for o in raw.get("operations") or []],
                "stereotype": raw.get("stereotype"),
            }
            mod["concepts"].append(concept)

            for tgt in _depends_on_targets(raw):
                add_dependency(display_name, tgt)
            for p in raw.get("properties") or []:
                if isinstance(p, dict):
                    for tgt in _depends_on_targets(p):
                        add_dependency(display_name, tgt)
            for o in raw.get("operations") or []:
                if isinstance(o, dict):
                    for tgt in _depends_on_targets(o):
                        add_dependency(display_name, tgt)
        modules.append(mod)

    for rel in data.get("cross_module_relationships") or []:
        if not isinstance(rel, dict):
            continue
        frm = (rel.get("from") or "").strip()
        to = (rel.get("to") or "").strip()
        rtype = (rel.get("type") or "association").strip()
        if frm and to:
            relationships.append({"from": frm, "to": to, "type": rtype})

    return modules, relationships


def load_map_model_spec_json(path: Path):
    """Load abd map-model-spec.json (modules_and_epics) into modules + relationships.

    Concept names may use ``Base:Subtype`` (one colon): first segment is the parent type,
    second is the class name shown on the diagram; an inheritance edge is added.
    ``depends_on`` on concepts, properties, or operations becomes UML dependency edges.
    Optional top-level ``cross_module_relationships``: list of {from, to, type}.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    return parse_map_model_spec_data(data)


def props_ops_for_drawio(concept):
    """Convert concept to DrawIO format: + name : Type and + op() → Return."""
    props = [f"+ {p}" for p in concept["properties"]]
    ops = [f"+ {o}" for o in concept["operations"]]
    return props, ops


def _concept_cell_height(concept) -> float:
    props, ops = props_ops_for_drawio(concept)
    return float(calc_cell_height(len(props), len(ops), 0))


def _tier_grid_positions(modules, relationships) -> dict[str, tuple[float, float]]:
    """Default layout: inheritance tiers, grid within each tier."""
    tiers = _compute_tiers(modules, relationships)
    tier_to_concepts = {}
    for mod in modules:
        for concept in mod["concepts"]:
            t = tiers.get(concept["name"], 0)
            tier_to_concepts.setdefault(t, []).append(concept)

    positions: dict[str, tuple[float, float]] = {}
    col_width = 280
    min_row_height = 100
    cols_per_row = 5
    tier_gap = 60
    start_x, start_y = 40, 40

    bottom_y = start_y
    for tier in sorted(tier_to_concepts.keys()):
        concepts = tier_to_concepts[tier]
        y = bottom_y
        x = start_x
        row_max_h = 0
        for j, concept in enumerate(concepts):
            props, ops = props_ops_for_drawio(concept)
            h = calc_cell_height(len(props), len(ops), 0)
            row_max_h = max(row_max_h, h)
            positions[concept["name"]] = (float(x), float(y))
            x += col_width
            if (j + 1) % cols_per_row == 0:
                x = start_x
                y += max(min_row_height, row_max_h) + 20
                row_max_h = 0
        bottom_y = y + max(min_row_height, row_max_h) + tier_gap
    return positions


def _compute_tiers(modules, relationships):
    """Assign tier to each concept: 0 = base, 1 = extends tier 0, etc.
    Returns dict name -> tier."""
    name_to_tier = {}
    # Inheritance: From=parent, To=child. Child extends parent.
    child_to_parents = {}
    for rel in relationships:
        if rel["type"].lower() != "inheritance":
            continue
        parent = rel["from"]
        for child in (n.strip() for n in rel["to"].split(",")):
            child_to_parents.setdefault(child, []).append(parent)

    def tier_for(name):
        if name in name_to_tier:
            return name_to_tier[name]
        parents = child_to_parents.get(name, [])
        if not parents:
            name_to_tier[name] = 0
            return 0
        parent_tiers = [tier_for(p) for p in parents if p in _all_names]
        if not parent_tiers:
            name_to_tier[name] = 0
            return 0
        name_to_tier[name] = max(parent_tiers) + 1
        return name_to_tier[name]

    _all_names = {c["name"] for m in modules for c in m["concepts"]}
    for m in modules:
        for c in m["concepts"]:
            tier_for(c["name"])
    return name_to_tier


def _build_domain_mxfile(modules, relationships, layout_plan: dict | None = None):
    """Build mxfile element tree: UML class cells + edges (same as map-model / domain model)."""
    mxfile = create_empty_mxfile()
    add_page(mxfile, "Domain Model")
    _, root = get_page(mxfile, "Domain Model")

    positions: dict[str, tuple[float, float]]
    if layout_plan:
        planned = compute_positions_from_plan(modules, layout_plan, _concept_cell_height)
        positions = planned if planned is not None else _tier_grid_positions(modules, relationships)
    else:
        positions = _tier_grid_positions(modules, relationships)

    name_to_id = {}
    for mod in modules:
        for concept in mod["concepts"]:
            nm = concept["name"]
            x, y = positions[nm]
            props, ops = props_ops_for_drawio(concept)
            cell = create_class_cell(
                root,
                nm,
                base=concept.get("base"),
                properties=props,
                operations=ops,
                x=x,
                y=y,
            )
            name_to_id[nm] = cell.get("id")

    for rel in relationships:
        from_name, to_raw, rel_type = rel["from"], rel["to"], rel["type"].lower()
        to_names = [n.strip() for n in to_raw.split(",")]
        edge_type = rel_type if rel_type in ("inheritance", "composition", "aggregation", "association", "dependency") else "association"

        for to_name in to_names:
            if from_name not in name_to_id or to_name not in name_to_id:
                continue
            src_cell = find_cell_by_name(root, from_name)
            tgt_cell = find_cell_by_name(root, to_name)
            if src_cell is None or tgt_cell is None:
                continue
            if edge_type == "inheritance":
                src_id, tgt_id = tgt_cell.get("id"), src_cell.get("id")
            else:
                src_id, tgt_id = src_cell.get("id"), tgt_cell.get("id")
            try:
                create_edge(root, src_id, tgt_id, edge_type)
            except ValueError:
                pass

    return mxfile


def generate_drawio(modules, relationships, output_path, layout_plan: dict | None = None):
    """Create DrawIO file with one page containing all classes and edges.

    With ``layout_plan``, uses cluster geometry; otherwise tier + grid (inheritance order).
    """
    mxfile = _build_domain_mxfile(modules, relationships, layout_plan=layout_plan)
    save_drawio(output_path, mxfile)
    return output_path


def map_model_spec_to_drawio_xml(spec: dict[str, Any], layout_plan: dict | None = None) -> str:
    """map-model-spec dict → Draw.io XML string (UML class diagram, not story-map styling)."""
    modules, relationships = parse_map_model_spec_data(spec)
    mxfile = _build_domain_mxfile(modules, relationships, layout_plan=layout_plan)
    return ET.tostring(mxfile, encoding="unicode", xml_declaration=True)


def write_map_model_class_diagram(
    spec_path: Path, out_path: Path, layout_plan_path: Path | None = None
) -> None:
    """map-model-spec.json path → `.drawio` file (UML class diagram).

    Optional ``layout_plan_path``: JSON logical layout (``schema_version`` 1). Missing file → tier grid.
    """
    modules, relationships = load_map_model_spec_json(spec_path)
    plan = load_layout_plan(layout_plan_path) if layout_plan_path else None
    generate_drawio(modules, relationships, out_path, layout_plan=plan)


def main():
    parser = argparse.ArgumentParser(
        description="Generate DrawIO class diagrams from map-model-spec.json (or domain-model.md)"
    )
    parser.add_argument(
        "model",
        type=Path,
        help="Path to map-model-spec.json (preferred) or domain-model.md",
    )
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output .drawio path")
    args = parser.parse_args()

    model_path = args.model.resolve()
    if not model_path.exists():
        print(f"Error: {model_path} not found", file=sys.stderr)
        sys.exit(1)

    suffix = model_path.suffix.lower()
    if suffix == ".json":
        modules, relationships = load_map_model_spec_json(model_path)
        default_out = model_path.parent / "map-model-classes.drawio"
    else:
        content = model_path.read_text(encoding="utf-8")
        modules, relationships = parse_domain_model(content)
        default_out = model_path.parent / "domain-class-diagram.drawio"

    output_path = (args.output or default_out).resolve()

    total_concepts = sum(len(m["concepts"]) for m in modules)
    print(f"Parsed {len(modules)} modules, {total_concepts} classes, {len(relationships)} relationships")

    generate_drawio(modules, relationships, output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
