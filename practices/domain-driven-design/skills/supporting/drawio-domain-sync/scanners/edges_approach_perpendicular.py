#!/usr/bin/env python3
"""
Scanner: edges_approach_perpendicular

Verifies that every edge's *final* segment approaches the destination
class perpendicular to the edge it ends at — i.e. the arrow tip hits the
side, it does not slide along it.

Example violation:

    +-----------+
    | Template  |
    |           |
    | <---------|----+   <-- segment goes DOWN along Template's LEFT side
    |           |    |
    +-----------+    |
                     |
                     |   <-- final segment is VERTICAL but the entry is
                     |       on Template's LEFT (a vertical) edge, so the
                     |       arrow tip slides along the side instead of
                     |       hitting it head-on.

What the rule requires:

  entry on LEFT or RIGHT side  →  final segment must be horizontal
  entry on TOP  or BOTTOM side →  final segment must be vertical

The same check is also applied to the *first* segment vs the source's
exit side (so the arrow LEAVES head-on too — otherwise the line slides
along the source class boundary before turning).

Usage:
  python edges_approach_perpendicular.py <file.drawio> [--page PAGE]

Exit codes:
  0  no violations found
  1  one or more parallel-approach segments detected (or file error)
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
    _compute_edge_segments_ex,
)


def _classify_edge(style: str) -> str:
    style = (style or "").lower()
    if "endarrow=block" in style and "startarrow=block" not in style:
        if "endfill=0" in style:
            return "inheritance-orthogonal" if "orthogonal" in style else "inheritance"
        return "association"
    if "startarrow=diamondthin" in style or "startarrow=diamond" in style:
        return "composition" if "startfill=1" in style else "aggregation"
    return "association"


def _anchor_side(frac_x: float | None, frac_y: float | None) -> str | None:
    """Return "left", "right", "top", "bottom" if the anchor sits on a
    side of the bounding box; ``None`` if it is interior or unspecified.
    """
    if frac_x is None or frac_y is None:
        return None
    if abs(frac_x - 0) < 1e-3:
        return "left"
    if abs(frac_x - 1) < 1e-3:
        return "right"
    if abs(frac_y - 0) < 1e-3:
        return "top"
    if abs(frac_y - 1) < 1e-3:
        return "bottom"
    return None


def _parse_style(style: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for kv in (style or "").split(";"):
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        try:
            out[k] = float(v)
        except ValueError:
            continue
    return out


def _segment_direction(seg) -> str | None:
    """Return ``"h"`` for horizontal, ``"v"`` for vertical, or ``None`` if
    the segment is too short / not axis-aligned (within 1 px).
    """
    (x1, y1), (x2, y2) = seg
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if dx < 1 and dy < 1:
        return None
    if dx < 1:
        return "v"
    if dy < 1:
        return "h"
    return None


def _segment_direction_signed(seg) -> str | None:
    """Return the SIGNED dominant direction: "left", "right", "up",
    "down", or None."""
    (x1, y1), (x2, y2) = seg
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) < 1 and abs(dy) < 1:
        return None
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def _expected_direction_for_side(side: str | None) -> str | None:
    if side in ("left", "right"):
        return "h"
    if side in ("top", "bottom"):
        return "v"
    return None


def _outward_direction(side: str | None) -> str | None:
    """Direction the first segment must travel to leave through ``side``."""
    return {"left": "left", "right": "right", "top": "up", "bottom": "down"}.get(side or "")


def _inward_direction(side: str | None) -> str | None:
    """Direction the last segment must travel to enter through ``side``.

    Approaching the LEFT side from outside means moving RIGHTWARD into it;
    approaching the TOP side means moving DOWNWARD into it.
    """
    return {"left": "right", "right": "left", "top": "down", "bottom": "up"}.get(side or "")


def check_edges_approach_perpendicular(root):
    """Return a list of violation tuples
    ``(edge_desc, end, expected, actual)``
    where ``end`` is "source" or "target".
    """
    classes = get_all_classes(root)
    id_to_name = {cid: name for cid, name, *_ in classes}
    id_to_geo = {cid: (x, y, w, h) for cid, name, x, y, w, h in classes}

    violations = []
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        src_id = cell.get("source", "")
        tgt_id = cell.get("target", "")
        if src_id not in id_to_name or tgt_id not in id_to_name:
            continue

        style = cell.get("style", "")
        attrs = _parse_style(style)
        exit_side = _anchor_side(attrs.get("exitX"), attrs.get("exitY"))
        entry_side = _anchor_side(attrs.get("entryX"), attrs.get("entryY"))

        segs, _ = _compute_edge_segments_ex(cell, id_to_geo)
        if not segs:
            continue

        etype = _classify_edge(style)
        desc = f"{id_to_name[src_id]}->{id_to_name[tgt_id]} ({etype})"

        # Source end — both orientation (H/V) AND direction (sign).
        # A horizontal first segment that goes RIGHT from a LEFT exit
        # cuts straight through the source class, so we need the signed
        # check too.
        expected_orient = _expected_direction_for_side(exit_side)
        actual_orient = _segment_direction(segs[0])
        if expected_orient and actual_orient and actual_orient != expected_orient:
            violations.append((desc, "source", exit_side, expected_orient, actual_orient))
        else:
            want = _outward_direction(exit_side)
            got = _segment_direction_signed(segs[0])
            if want and got and got != want:
                violations.append((desc, "source", exit_side, want, got))

        # Target end
        expected_orient = _expected_direction_for_side(entry_side)
        actual_orient = _segment_direction(segs[-1])
        if expected_orient and actual_orient and actual_orient != expected_orient:
            violations.append((desc, "target", entry_side, expected_orient, actual_orient))
        else:
            want = _inward_direction(entry_side)
            got = _segment_direction_signed(segs[-1])
            if want and got and got != want:
                violations.append((desc, "target", entry_side, want, got))

    return violations


def scan(path: Path, page: str | None = None) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    _, mxfile = load_drawio(str(path))
    if page:
        pages = [(page,)]
    else:
        pages = [(d.get("name"),) for d in mxfile.findall("diagram")]

    total = 0
    for (pname,) in pages:
        _, root = get_page(mxfile, pname)
        if root is None:
            print(f"  [{pname}] page not found", file=sys.stderr)
            total += 1
            continue
        viols = check_edges_approach_perpendicular(root)
        if not viols:
            print(
                f"[PASS] {pname}: every edge approaches its endpoints "
                f"perpendicular to the touched side"
            )
            continue
        total += len(viols)
        print(f"[FAIL] {pname}: {len(viols)} parallel-approach violation(s)")
        for desc, end, side, expected, actual in viols:
            print(
                f"  - {desc}: {end} segment goes {actual} but anchor is on "
                f"the {side} side (expected {expected})"
            )

    return 0 if total == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Path to .drawio file")
    parser.add_argument("--page", default=None, help="Optional page name to limit scan")
    args = parser.parse_args()
    sys.exit(scan(args.file, args.page))


if __name__ == "__main__":
    main()
