#!/usr/bin/env python3
"""
Scanner: edges_do_not_cross_other_edges

Verifies that no two edges cross each other at a single point (one segment
passes through another segment perpendicularly or transversely).

This is distinct from edges_do_not_overlap_edges, which checks for collinear
overlap (segments lying on top of each other). Both classes of problem
hurt readability, but transverse crossings are the most visually offensive.

Usage:
  python edges_do_not_cross_other_edges.py <file.drawio> [--page PAGE]

Exit codes:
  0  no crossings found
  1  one or more edge-on-edge crossings detected (or file error)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from drawio_tools import (  # noqa: E402
    load_drawio,
    get_page,
    get_all_classes,
    _compute_edge_segments,
)


def _segments_cross(seg_a, seg_b, endpoint_tol=2):
    """Return True if two non-collinear axis-aligned segments cross.

    A crossing means the two segments share exactly one interior point.
    Touching at endpoints does not count (edges legitimately share anchors).
    """
    (ax1, ay1), (ax2, ay2) = seg_a
    (bx1, by1), (bx2, by2) = seg_b

    a_horiz = abs(ay2 - ay1) < 2
    a_vert = abs(ax2 - ax1) < 2
    b_horiz = abs(by2 - by1) < 2
    b_vert = abs(bx2 - bx1) < 2

    if a_horiz and b_vert:
        y = (ay1 + ay2) / 2
        x = (bx1 + bx2) / 2
        a_lo_x, a_hi_x = sorted((ax1, ax2))
        b_lo_y, b_hi_y = sorted((by1, by2))
        if a_lo_x + endpoint_tol < x < a_hi_x - endpoint_tol and b_lo_y + endpoint_tol < y < b_hi_y - endpoint_tol:
            return True, (x, y)
    if a_vert and b_horiz:
        x = (ax1 + ax2) / 2
        y = (by1 + by2) / 2
        a_lo_y, a_hi_y = sorted((ay1, ay2))
        b_lo_x, b_hi_x = sorted((bx1, bx2))
        if a_lo_y + endpoint_tol < y < a_hi_y - endpoint_tol and b_lo_x + endpoint_tol < x < b_hi_x - endpoint_tol:
            return True, (x, y)

    return False, None


def _describe_edge(edge_cell, id_to_name):
    src = id_to_name.get(edge_cell.get("source", ""), "?")
    tgt = id_to_name.get(edge_cell.get("target", ""), "?")
    return f"{src} -> {tgt}"


def scan(path: Path, page: str | None = None) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    _, mxfile = load_drawio(str(path))

    if page:
        pages = [(page,)]
    else:
        pages = [(d.get("name"),) for d in mxfile.findall("diagram")]

    total_violations = 0
    for (pname,) in pages:
        _, root = get_page(mxfile, pname)
        if root is None:
            print(f"  [{pname}] page not found", file=sys.stderr)
            total_violations += 1
            continue

        classes = get_all_classes(root)
        id_to_name = {cid: name for cid, name, *_ in classes}
        id_to_geo = {cid: (x, y, w, h) for cid, name, x, y, w, h in classes}
        edges = [c for c in root.findall("mxCell") if c.get("edge") == "1"]

        edge_segs = []
        for ec in edges:
            segs = _compute_edge_segments(ec, id_to_geo)
            edge_segs.append((ec, segs))

        crossings = []
        for i in range(len(edge_segs)):
            ec_a, segs_a = edge_segs[i]
            for j in range(i + 1, len(edge_segs)):
                ec_b, segs_b = edge_segs[j]
                # Skip pairs that share an endpoint class — those are legal
                # at the shared anchor.
                shared = {ec_a.get("source"), ec_a.get("target")} & {
                    ec_b.get("source"),
                    ec_b.get("target"),
                }
                # Even with shared endpoints, crossings AWAY from the shared
                # anchor still count; only ignore literal endpoint touches.
                for sa in segs_a:
                    for sb in segs_b:
                        crossed, pt = _segments_cross(sa, sb)
                        if not crossed:
                            continue
                        # Skip if the crossing point coincides with a shared
                        # anchor (within a small tolerance).
                        if shared:
                            shared_pts = []
                            for sid in shared:
                                geo = id_to_geo.get(sid)
                                if not geo:
                                    continue
                                gx, gy, gw, gh = geo
                                shared_pts.append((gx + gw / 2, gy + gh / 2))
                            if any(
                                abs(pt[0] - sx) < gw / 2 + 5 and abs(pt[1] - sy) < gh / 2 + 5
                                for sx, sy in shared_pts
                            ):
                                continue
                        crossings.append(
                            (
                                _describe_edge(ec_a, id_to_name),
                                _describe_edge(ec_b, id_to_name),
                                f"cross at ~({int(pt[0])},{int(pt[1])})",
                            )
                        )
                        break
                    else:
                        continue
                    break

        if not crossings:
            print(f"[PASS] {pname}: no edges cross other edges")
            continue

        total_violations += len(crossings)
        print(f"[FAIL] {pname}: {len(crossings)} edge_crosses_edge violation(s)")
        for desc_a, desc_b, detail in crossings:
            print(f"  - {desc_a} crosses {desc_b}: {detail}")

    return 0 if total_violations == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Path to .drawio file")
    parser.add_argument("--page", default=None, help="Optional page name to limit scan")
    args = parser.parse_args()

    sys.exit(scan(args.file, args.page))


if __name__ == "__main__":
    main()
