#!/usr/bin/env python3
"""
Build a Draw.io class diagram from the Delivery Agent Kanban domain model.

Usage:
    python scripts/build_domain_model_diagram.py
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_SCRIPTS = (
    REPO_ROOT.parents[2]
    / "domain-driven-design"
    / "skills"
    / "drawio-domain-sync"
    / "scripts"
)
sys.path.insert(0, str(SKILL_SCRIPTS))

from drawio_tools import (
    create_empty_mxfile,
    add_page,
    get_page,
    save_drawio,
    create_class_cell,
    create_edge,
    find_cell_by_name,
    audit_diagram_report,
)

CRC_PATH = REPO_ROOT / "docs" / "domain" / "domain model.md"
OUTPUT_PATH = REPO_ROOT / "docs" / "domain" / "domain model-class-diagram.drawio"

PAGE_W = 3000
PAGE_H = 1800


def parse_crc(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    kas = {}
    current_ka = None
    current_class = None
    in_references = False
    in_decisions = False

    for line in lines:
        stripped = line.strip()
        ka_match = re.match(r"^##\s+\*\*(.+?)\*\*\s*$", stripped)
        if ka_match:
            current_ka = ka_match.group(1)
            kas[current_ka] = {"classes": []}
            current_class = None
            in_references = False
            in_decisions = False
            continue

        class_match = re.match(r"^###\s+\*\*(.+?)\*\*\s*$", stripped)
        if class_match and current_ka and not in_references and not in_decisions:
            raw = class_match.group(1)
            base = None
            if " : " in raw:
                name, base = raw.split(" : ", 1)
                name, base = name.strip(), base.strip()
            else:
                name = raw
            current_class = {
                "name": name,
                "base": base,
                "responsibilities": [],
                "invariants": [],
            }
            kas[current_ka]["classes"].append(current_class)
            continue

        if stripped == "### references":
            in_references = True
            current_class = None
            continue
        if stripped == "### decisions made":
            in_decisions = True
            current_class = None
            continue
        if stripped == "---":
            in_references = False
            in_decisions = False
            continue

        if current_class is None or in_references or in_decisions:
            continue

        resp_match = re.match(r"^(.+?)\s*\|\s*(.*)$", stripped)
        if resp_match:
            left = resp_match.group(1).strip()
            right = resp_match.group(2).strip()
            if not left and right.startswith("invariant:"):
                current_class["invariants"].append(right[len("invariant:"):].strip())
            elif left:
                collabs = []
                if right and not right.startswith("invariant:") and not right.startswith("("):
                    collabs = [c.strip() for c in right.split(",") if c.strip()]
                current_class["responsibilities"].append({"name": left, "collaborators": collabs})

    return kas


def _class_content(cls):
    props = [r["name"] for r in cls["responsibilities"] if not r["collaborators"]]
    ops = [
        f'{r["name"]} : {", ".join(r["collaborators"])}'
        for r in cls["responsibilities"]
        if r["collaborators"]
    ]
    return props, ops, cls["invariants"][:5]


def _add_class(root, cls, x, y, imported_from=None):
    props, ops, invs = _class_content(cls)
    create_class_cell(
        root, cls["name"], base=cls.get("base"),
        properties=props, operations=ops, invariants=invs,
        x=x, y=y, imported_from=imported_from,
    )


def _lookup(all_kas, name):
    for data in all_kas.values():
        for cls in data["classes"]:
            if cls["name"] == name:
                return cls
    raise KeyError(name)


def _edge(root, src, tgt, kind="association", waypoints=None, **anchors):
    s = find_cell_by_name(root, src)
    t = find_cell_by_name(root, tgt)
    if s is None or t is None:
        return
    cell = create_edge(root, s.get("id"), t.get("id"), kind, **anchors)
    if waypoints:
        geo = cell.find("mxGeometry")
        arr = ET.SubElement(geo, "Array")
        arr.set("as", "points")
        for wx, wy in waypoints:
            pt = ET.SubElement(arr, "mxPoint")
            pt.set("x", str(int(wx)))
            pt.set("y", str(int(wy)))


def _add_local_edges(root, classes, edge_overrides=None):
    local = {c["name"] for c in classes}
    seen = set()
    edge_overrides = edge_overrides or {}
    for cls in classes:
        if cls.get("base") and cls["base"] in local:
            _edge(root, cls["name"], cls["base"], "inheritance-orthogonal")
        for resp in cls["responsibilities"]:
            for collab in resp["collaborators"]:
                if collab not in local or collab == cls["name"]:
                    continue
                pair = tuple(sorted([cls["name"], collab]))
                if pair in seen:
                    continue
                seen.add(pair)
                opts = edge_overrides.get((cls["name"], collab), {})
                kind = opts.pop("kind", "association")
                waypoints = opts.pop("waypoints", None)
                _edge(root, cls["name"], collab, kind=kind, waypoints=waypoints, **opts)


def _build_kanban_board_page(mxfile, classes, all_kas):
    add_page(mxfile, "Kanban Board", PAGE_W, PAGE_H)
    _, root = get_page(mxfile, "Kanban Board")
    by_name = {c["name"]: c for c in classes}

    _add_class(root, _lookup(all_kas, "Agent"), 2300, 40, "Agent and Skills")
    _add_class(root, _lookup(all_kas, "Skill"), 2600, 40, "Agent and Skills")

    _add_class(root, by_name["Kanban Board"], 1300, 620)
    _add_class(root, by_name["Stage"], 200, 620)
    _add_class(root, by_name["Stage Work Required"], 1300, 200)
    _add_class(root, by_name["Team"], 2400, 620)
    _add_class(root, by_name["Ticket"], 200, 1200)
    _add_class(root, by_name["Board Position"], 800, 1200)
    _add_class(root, by_name["Skill Progress"], 1800, 1200)

    overrides = {
        ("Kanban Board", "Stage"): {
            "exit_x": 0, "exit_y": 0.5, "entry_x": 1, "entry_y": 0.5,
        },
        ("Kanban Board", "Stage Work Required"): {
            "exit_x": 0.5, "exit_y": 0, "entry_x": 0.5, "entry_y": 1,
        },
        ("Kanban Board", "Team"): {
            "exit_x": 1, "exit_y": 0.5, "entry_x": 0, "entry_y": 0.5,
        },
        ("Kanban Board", "Ticket"): {
            "exit_x": 0.15, "exit_y": 1, "entry_x": 0.5, "entry_y": 0,
            "waypoints": [(1300, 1500), (330, 1500)],
        },
        ("Ticket", "Stage"): {
            "exit_x": 0.5, "exit_y": 0, "entry_x": 0.25, "entry_y": 1,
            "waypoints": [(330, 1100)],
        },
        ("Ticket", "Skill Progress"): {
            "exit_x": 1, "exit_y": 0.5, "entry_x": 0, "entry_y": 0.5,
            "waypoints": [(330, 1320), (1930, 1320)],
        },
        ("Ticket", "Team"): {
            "exit_x": 1, "exit_y": 0.7, "entry_x": 0, "entry_y": 1,
            "waypoints": [(330, 1580), (2550, 1580)],
        },
        ("Board Position", "Stage"): {
            "exit_x": 0.5, "exit_y": 0, "entry_x": 0.75, "entry_y": 1,
            "waypoints": [(930, 1100), (930, 520), (330, 520)],
        },
    }
    _add_local_edges(root, classes, overrides)


def _build_agent_skills_page(mxfile, classes, all_kas):
    add_page(mxfile, "Agent and Skills", PAGE_W, PAGE_H)
    _, root = get_page(mxfile, "Agent and Skills")
    by_name = {c["name"]: c for c in classes}

    for name, x in [
        ("Kanban Board", 200), ("Stage", 550), ("Stage Work Required", 900),
        ("Ticket", 1250), ("Skill Progress", 1600), ("Team", 1950),
    ]:
        _add_class(root, _lookup(all_kas, name), x, 40, "Kanban Board")

    _add_class(root, by_name["Kanban Lead"], 1300, 280)
    _add_class(root, by_name["Agent"], 200, 780)
    _add_class(root, by_name["Skill"], 900, 780)
    _add_class(root, by_name["Heartbeat"], 1600, 780)
    _add_class(root, by_name["Role Engagement"], 2300, 780)

    overrides = {
        ("Agent", "Skill"): {
            "exit_x": 1, "exit_y": 0.4, "entry_x": 0, "entry_y": 0.4,
        },
        ("Agent", "Heartbeat"): {
            "exit_x": 1, "exit_y": 0.7, "entry_x": 0, "entry_y": 0.7,
            "waypoints": [(200, 1050), (1600, 1050)],
        },
        ("Role Engagement", "Agent"): {
            "exit_x": 0, "exit_y": 0.5, "entry_x": 1, "entry_y": 0.5,
            "waypoints": [(2300, 1150), (200, 1150)],
        },
        ("Kanban Lead", "Heartbeat"): {
            "exit_x": 0.75, "exit_y": 1, "entry_x": 0.5, "entry_y": 0,
        },
        ("Kanban Lead", "Agent"): {
            "exit_x": 0.25, "exit_y": 1, "entry_x": 0.5, "entry_y": 0,
            "waypoints": [(1300, 600), (330, 600)],
        },
    }
    _add_local_edges(root, classes, overrides)


def main():
    print(f"Parsing: {CRC_PATH}")
    kas = parse_crc(CRC_PATH)

    mxfile = create_empty_mxfile()
    _build_kanban_board_page(mxfile, kas["Kanban Board"]["classes"], kas)
    _build_agent_skills_page(mxfile, kas["Agent and Skills"]["classes"], kas)

    save_drawio(OUTPUT_PATH, mxfile)
    print(f"Wrote: {OUTPUT_PATH}")

    report = audit_diagram_report(str(OUTPUT_PATH))
    print("\n" + report)
    if "[edge_crosses_class]" in report:
        sys.exit(1)


if __name__ == "__main__":
    main()
