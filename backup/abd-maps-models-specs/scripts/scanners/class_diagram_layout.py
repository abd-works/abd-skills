"""Scanner: layout/readability heuristics for map-model-class-diagram.drawio.

Rule: class-diagram

Checks (v1 -- geometry + graph, not aesthetics):
- Valid XML with mxfile/diagram content
- **Violations (exit 1):** duplicate directed edges (same source + target); axis-aligned overlap between class boxes
- **Warnings (exit 0):** self-loops; vertex degree above threshold; very high edge:vertex ratio

Missing file -> skip (0). Malformed XML -> 1.

Usage:
    python scripts/scanners/class_diagram_layout.py [--input <path>]

Default input: <output_dir>/map-model-class-diagram.drawio
"""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


RULE_ID = "class-diagram"
DEFAULT_BASENAME = "map-model-class-diagram.drawio"

# Above this total degree (in + out), emit a warning.
WARN_VERTEX_DEGREE = 22


def _local(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def _parse_geometry(cell: ET.Element) -> tuple[float, float, float, float] | None:
    for ch in cell:
        if _local(ch.tag) != "mxGeometry":
            continue
        a = ch.attrib
        try:
            x = float(a.get("x", 0))
            y = float(a.get("y", 0))
            w = float(a.get("width", 0))
            h = float(a.get("height", 0))
        except ValueError:
            return None
        if w <= 0 or h <= 0:
            return None
        return (x, y, w, h)
    return None


def _overlap_area(
    a: tuple[float, float, float, float], b: tuple[float, float, float, float]
) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix0 = max(ax, bx)
    iy0 = max(ay, by)
    ix1 = min(ax + aw, bx + bw)
    iy1 = min(ay + ah, by + bh)
    if ix1 <= ix0 or iy1 <= iy0:
        return 0.0
    return (ix1 - ix0) * (iy1 - iy0)


def analyze_drawio(path: Path) -> tuple[list[str], list[str]]:
    """Returns (violations, warnings)."""
    violations: list[str] = []
    warnings: list[str] = []

    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return ([f"invalid XML: {e}"], [])

    root = tree.getroot()
    if _local(root.tag) != "mxfile":
        violations.append(f"expected root <mxfile>, got {_local(root.tag)!r}")
        return (violations, warnings)

    vertices: dict[str, tuple[float, float, float, float]] = {}
    edges: list[tuple[str, str]] = []

    for el in root.iter():
        if _local(el.tag) != "mxCell":
            continue
        vid = el.attrib.get("id")
        if el.attrib.get("vertex") == "1":
            if not vid:
                continue
            g = _parse_geometry(el)
            if g is not None:
                vertices[vid] = g
        elif el.attrib.get("edge") == "1":
            s, t = el.attrib.get("source"), el.attrib.get("target")
            if s and t:
                edges.append((s, t))

    if not vertices and not edges:
        violations.append("no mxCell vertices/edges found - empty or unexpected diagram")
        return (violations, warnings)

    for s, t in edges:
        if s == t:
            warnings.append(f"self-loop on cell id {s!r} - remove unless modeling true recursion")

    pair_counts: Counter[tuple[str, str]] = Counter(edges)
    for (s, t), n in pair_counts.items():
        if n > 1:
            violations.append(f"duplicate directed edge {s!r} -> {t!r} ({n} copies) - keep one")

    ids = list(vertices.keys())
    for i, ia in enumerate(ids):
        for ib in ids[i + 1 :]:
            a, b = vertices[ia], vertices[ib]
            area = _overlap_area(a, b)
            if area > 1.0:
                violations.append(
                    f"overlapping class boxes id {ia!r} vs {ib!r} (overlap area ~ {area:.0f})"
                )

    deg: defaultdict[str, int] = defaultdict(int)
    for s, t in edges:
        deg[s] += 1
        deg[t] += 1
    for vid, d in deg.items():
        if d > WARN_VERTEX_DEGREE:
            warnings.append(
                f"high edge count on cell {vid!r} (degree {d} > {WARN_VERTEX_DEGREE}) - consider splitting diagram or reducing fan-out"
            )

    ec, vc = len(edges), len(vertices)
    if vc >= 10 and ec > 4 * vc:
        warnings.append(
            f"very dense graph ({ec} edges, {vc} classes) - consider multiple pages or swimlanes"
        )

    return (violations, warnings)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from _config import output_dir

    parser = argparse.ArgumentParser(
        description=f"Class diagram layout scanner. Rule: {RULE_ID}"
    )
    default_in = output_dir() / DEFAULT_BASENAME
    parser.add_argument("--input", default=str(default_in), help="Path to .drawio file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"{RULE_ID}: no file at {input_path} - skip")
        return 0

    violations, warnings = analyze_drawio(input_path)
    for w in warnings:
        print(f"WARN [{RULE_ID}] {w}", flush=True)

    if not violations:
        print(f"PASS [{RULE_ID}] - layout heuristics OK for {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] - {len(violations)} in {input_path.name}")
    for msg in violations:
        print(f"  {msg}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
