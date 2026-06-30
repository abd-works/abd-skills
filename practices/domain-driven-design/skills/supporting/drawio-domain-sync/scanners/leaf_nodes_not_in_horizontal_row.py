#!/usr/bin/env python3
"""
Scanner: leaf_nodes_not_in_horizontal_row

A hub class connects to many leaf classes via composition or association edges.
When the generator places all leaves in a single horizontal row (same y ± tolerance),
the diagram becomes very wide and unreadable.

This scanner flags pages where a hub class has 4+ direct neighbours that all share
the same y-coordinate within a ±30px tolerance.

Usage:
  python leaf_nodes_not_in_horizontal_row.py <file.drawio> [--page PAGE]

Exit codes:
  0  no violations found
  1  one or more horizontal-row violations detected (or file error)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from drawio_tools import load_drawio, get_page  # noqa: E402

# Leaves at the same y ± this many pixels are considered "same row".
Y_TOLERANCE = 30
# Minimum number of leaves in the same row to trigger a violation.
MIN_ROW_SIZE = 4


def _get_vertex_geo(root: ET.Element) -> dict[str, tuple[float, float, float, float]]:
    """Return {cell_id: (x, y, w, h)} for all non-edge vertices."""
    geo: dict[str, tuple[float, float, float, float]] = {}
    for cell in root.findall("mxCell"):
        if cell.get("vertex") != "1":
            continue
        g = cell.find("mxGeometry")
        if g is None:
            continue
        w = g.get("width")
        h = g.get("height")
        if w is None or h is None:
            continue
        geo[cell.get("id", "")] = (
            float(g.get("x", 0)),
            float(g.get("y", 0)),
            float(w),
            float(h),
        )
    return geo


def _get_edges(root: ET.Element) -> list[tuple[str, str]]:
    """Return [(source_id, target_id)] for all edges."""
    edges = []
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        src = cell.get("source")
        tgt = cell.get("target")
        if src and tgt:
            edges.append((src, tgt))
    return edges


def _check_page(root: ET.Element, page_name: str) -> list[str]:
    """Return a list of violation description strings for this page."""
    geo = _get_vertex_geo(root)
    edges = _get_edges(root)

    # Build adjacency: hub -> set of neighbour ids
    neighbours: dict[str, set[str]] = {}
    for src, tgt in edges:
        if src in geo:
            neighbours.setdefault(src, set()).add(tgt)

    violations = []
    for hub_id, leaf_ids in neighbours.items():
        if len(leaf_ids) < MIN_ROW_SIZE:
            continue

        # Group leaves by rounded y-bucket (round to nearest Y_TOLERANCE).
        row_groups: dict[int, list[str]] = {}
        for lid in leaf_ids:
            if lid not in geo:
                continue
            y = geo[lid][1]
            bucket = round(y / Y_TOLERANCE)
            row_groups.setdefault(bucket, []).append(lid)

        for bucket, members in row_groups.items():
            if len(members) < MIN_ROW_SIZE:
                continue
            y_vals = [geo[m][1] for m in members]
            y_spread = max(y_vals) - min(y_vals)
            x_vals = [geo[m][0] for m in members]
            x_spread = max(x_vals) - min(x_vals)
            # A true horizontal row has large x-spread and small y-spread.
            if y_spread <= Y_TOLERANCE and x_spread > 600:
                # Find hub name for the message.
                hub_cell = root.find(f"mxCell[@id='{hub_id}']")
                hub_name = hub_id
                if hub_cell is not None:
                    import re as _re
                    raw = hub_cell.get("value") or hub_id
                    # Strip HTML tags, then take only the first "word" (class name).
                    text = _re.sub(r"<[^>]+>", "", raw)
                    text = _re.sub(r"&[a-z]+;", " ", text)
                    # First token before any space or + is the class name.
                    hub_name = _re.split(r"[\s+]", text.strip())[0] or hub_id
                violations.append(
                    f"{hub_name} has {len(members)} leaf neighbours in a horizontal row "
                    f"(y~{int(sum(y_vals)/len(y_vals))}, x-span={int(x_spread)}px)"
                )

    return violations


def scan(path: Path, page: str | None = None) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    _, mxfile = load_drawio(str(path))

    if page:
        page_names = [page]
    else:
        page_names = [d.get("name", "") for d in mxfile.findall("diagram")]

    total_violations = 0
    for pname in page_names:
        _, root = get_page(mxfile, pname)
        if root is None:
            print(f"  [{pname}] page not found", file=sys.stderr)
            total_violations += 1
            continue

        vs = _check_page(root, pname)
        if not vs:
            print(f"[PASS] {pname}: no horizontal-row leaf clusters")
        else:
            total_violations += len(vs)
            print(f"[FAIL] {pname}: {len(vs)} horizontal-row violation(s)")
            for v in vs:
                print(f"  - {v}")

    return 0 if total_violations == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Path to .drawio file")
    parser.add_argument("--page", default=None, help="Optional page name to limit scan")
    args = parser.parse_args()
    sys.exit(scan(args.file, args.page))


if __name__ == "__main__":
    main()
