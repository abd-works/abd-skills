#!/usr/bin/env python3
"""
drawio_cli.py — CLI for creating and editing Draw.io UML class diagrams.

Follows Jeff's OOAD notation style as documented in the class-diagrams video:
  - swimlane classes with bold name header
  - fields above the divider, methods below
  - correct arrow styles for each relationship type
  - abstract members in italic (fontStyle=2)
  - association labels + multiplicities on both ends
  - UML frames for packages

Usage:
  python drawio_cli.py COMMAND [OPTIONS] --file DIAGRAM.drawio

Run `python drawio_cli.py --help` or `python drawio_cli.py COMMAND --help`
for details.
"""

import argparse
import json
import os
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
from html import unescape

# ─── Styles ───────────────────────────────────────────────────────────────────

CLASS_STYLE = (
    "swimlane;fontStyle=1;align=center;verticalAlign=top;"
    "childLayout=stackLayout;horizontal=1;startSize=26;"
    "horizontalStack=0;resizeParent=1;resizeParentMax=0;"
    "resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
)
FIELD_STYLE = (
    "text;strokeColor=none;fillColor=none;align=left;"
    "verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;"
    "rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
    "whiteSpace=wrap;html=1;"
)
FIELD_STYLE_ABSTRACT = FIELD_STYLE + "fontStyle=2;"
DIVIDER_STYLE = (
    "line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;"
    "spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;"
    "labelPosition=right;points=[];portConstraint=eastwest;strokeColor=inherit;"
)
ASSOCIATION_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
    "jettySize=auto;html=1;"
)
INHERITANCE_STYLE = (
    "endArrow=block;dashed=1;endFill=0;endSize=12;html=1;rounded=0;"
)
COMPOSITION_STYLE = (
    # filled diamond at the WHOLE end; orthogonal routing for clean corners
    "endArrow=diamondThin;endFill=1;endSize=24;html=1;rounded=0;"
    "edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;"
)
AGGREGATION_STYLE = (
    "endArrow=open;html=1;endSize=12;"
    "startArrow=diamondThin;startSize=14;startFill=0;"
    "edgeStyle=orthogonalEdgeStyle;rounded=0;"
)
DEPENDENCY_STYLE = (
    "endArrow=open;endSize=12;dashed=1;html=1;rounded=0;"
)
FRAME_STYLE = (
    "shape=umlFrame;whiteSpace=wrap;html=1;pointerEvents=0;"
)
EDGE_LABEL_STYLE = (
    "edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];"
)
OBJECT_STYLE = (
    "verticalAlign=top;align=left;overflow=fill;html=1;whiteSpace=wrap;"
)

# ─── Layout constants ─────────────────────────────────────────────────────────

DEFAULT_WIDTH      = 200
HEADER_HEIGHT      = 26   # class name row
CELL_HEIGHT        = 26   # one field or method row
DIVIDER_HEIGHT     = 8
GRID_COLS          = 4
GRID_COL_SPACING   = 80   # horizontal gap between columns
GRID_ROW_SPACING   = 60   # vertical gap between rows
START_X            = 100
START_Y            = 100

# ─── Helpers ──────────────────────────────────────────────────────────────────

def new_id():
    """Generate a short unique cell ID."""
    return str(uuid.uuid4()).replace("-", "")[:20]


def load_diagram(path):
    """Load a .drawio file and return (tree, root_cell) where root_cell is the
    <root> element inside mxGraphModel."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    tree = ET.parse(path)
    mxfile = tree.getroot()
    root = mxfile.find(".//root")
    if root is None:
        raise ValueError("Invalid .drawio file: no <root> element found.")
    return tree, root


def save_diagram(tree, path):
    ET.indent(tree.getroot(), space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def create_new_diagram(path):
    """Create a brand-new empty .drawio file."""
    diagram_id = new_id()
    xml_str = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio_cli" version="29.0.3">
  <diagram name="Page-1" id="{diagram_id}">
    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1" page="1"
                  pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    Path(path).write_text(xml_str, encoding="utf-8")


def _extract_class_name(value):
    """Extract the plain class name from a potentially HTML-formatted cell value.

    Handles:
    - Plain name: 'Character'
    - Old stereotype format: '«scan»<br><b>Character</b>'
    - New stereotype format: '<font ...>&lt;&lt;scan&gt;&gt;</font><br>Character'
    """
    import re
    from html import unescape

    # 1. Prefer content inside <b>...</b> — explicit bold = class name
    bold_match = re.search(r'<b>(.*?)</b>', value, re.IGNORECASE)
    if bold_match:
        return bold_match.group(1).strip()

    # 2. Strip all HTML tags, unescape HTML entities, remove UML stereotype tokens
    stripped = re.sub(r'<[^>]+>', ' ', value)   # remove tags
    stripped = unescape(stripped)                # &lt; → <  etc.
    stripped = re.sub(r'«[^»]*»', ' ', stripped)   # remove «...» guillemet stereotypes
    stripped = re.sub(r'<<[^>]*>>', ' ', stripped)  # remove <<...>> angle-bracket stereotypes
    stripped = stripped.strip()

    # 3. Return the last non-empty whitespace token (class name is always last after <br>)
    tokens = [t for t in stripped.split() if t]
    return tokens[-1] if tokens else value.strip()


def get_all_classes(root):
    """Return a dict of {name: mxCell_element} for all class swimlane cells."""
    classes = {}
    for cell in root.findall("mxCell"):
        style = cell.get("style", "")
        if "swimlane" in style and "shape=umlFrame" not in style:
            raw = cell.get("value", "").strip()
            name_clean = _extract_class_name(raw)
            if name_clean:
                classes[name_clean] = cell
    return classes


def find_class(root, class_name):
    """Find a class cell by name, case-sensitive. Raises if not found."""
    classes = get_all_classes(root)
    if class_name not in classes:
        available = ", ".join(sorted(classes.keys())) or "(none)"
        raise KeyError(f"Class '{class_name}' not found. Available: {available}")
    return classes[class_name]


def find_field_row(root, class_name, field_text):
    """Find a field-row cell inside *class_name* whose value matches *field_text*.

    Matching is done after stripping HTML tags and normalising whitespace so
    labels like '<b>+ abilities: Ability [1..*]</b>' still match the plain
    string '+ abilities: Ability [1..*]'.

    Returns the mxCell element or raises KeyError.
    """
    import html, re as _re

    def _plain(v):
        v = html.unescape(v or "")
        v = _re.sub(r"<[^>]+>", "", v)
        return " ".join(v.split())

    cls = find_class(root, class_name)
    cls_id = cls.get("id")
    needle = _plain(field_text)
    for cell in root.findall("mxCell"):
        if cell.get("parent") != cls_id:
            continue
        if cell.get("vertex") != "1":
            continue
        if "line;" in cell.get("style", ""):
            continue  # skip divider
        if _plain(cell.get("value", "")) == needle:
            # Add portConstraint=eastwest so the diamond connects to left/right
            style = cell.get("style", "")
            if "portConstraint" not in style:
                cell.set("style", style.rstrip(";") + ";portConstraint=eastwest;")
            return cell
    available = [
        _plain(c.get("value", ""))
        for c in root.findall("mxCell")
        if c.get("parent") == cls_id and c.get("vertex") == "1"
        and "line;" not in c.get("style", "")
    ]
    raise KeyError(
        f"Field '{field_text}' not found in class '{class_name}'. "
        f"Available: {available}"
    )


def get_class_children(root, class_id):
    """Return all child cells of a class (fields, divider, methods)."""
    return [c for c in root.findall("mxCell") if c.get("parent") == class_id]


def get_divider(root, class_id):
    """Return the divider cell for a class, or None."""
    for cell in get_class_children(root, class_id):
        if "line;" in cell.get("style", ""):
            return cell
    return None


def class_content_height(root, class_id):
    """Calculate current total height of a class from its children.

    In Draw.io's swimlane/stackLayout, child y-coordinates are measured from
    the very top of the swimlane cell (i.e. they already include the header
    offset of HEADER_HEIGHT=26).  So the class height == max(child.y + child.h).
    """
    children = get_class_children(root, class_id)
    if not children:
        return HEADER_HEIGHT + DIVIDER_HEIGHT
    max_bottom = HEADER_HEIGHT + DIVIDER_HEIGHT
    for child in children:
        geo = child.find("mxGeometry")
        if geo is not None:
            y = float(geo.get("y", 0))
            h = float(geo.get("height", CELL_HEIGHT))
            max_bottom = max(max_bottom, y + h)
    return int(max_bottom)


def update_class_height(root, class_cell):
    """Recompute and set the height of a class based on its children.

    Child y-values already count from the top of the swimlane (header
    included), so class height = max(child.y + child.h).  We must NOT add
    HEADER_HEIGHT a second time.
    """
    class_id = class_cell.get("id")
    children = get_class_children(root, class_id)
    if not children:
        total_h = HEADER_HEIGHT + DIVIDER_HEIGHT
    else:
        last_y = 0
        last_h = 0
        for c in children:
            geo = c.find("mxGeometry")
            if geo is not None:
                y = float(geo.get("y", 0))
                h = float(geo.get("height", CELL_HEIGHT))
                if y + h > last_y + last_h:
                    last_y = y
                    last_h = h
        total_h = int(last_y + last_h)   # child y already includes header

    geo = class_cell.find("mxGeometry")
    if geo is not None:
        geo.set("height", str(total_h))


def next_class_position(root):
    """Placeholder position at add-class time (heights unknown yet).
    Always call relayout after all fields/methods are added."""
    classes = get_all_classes(root)
    n = len(classes)
    col = n % GRID_COLS
    row = n // GRID_COLS
    x = START_X + col * (DEFAULT_WIDTH + GRID_COL_SPACING)
    y = START_Y + row * (320 + GRID_ROW_SPACING)
    return x, y


def _build_inheritance_graph(root, classes):
    """Return (parent_of, children_of) dicts keyed by class name."""
    from collections import defaultdict
    parent_of   = {}            # child_name  → parent_name
    children_of = defaultdict(list)   # parent_name → [child_names]
    id_to_name  = {v.get("id"): k for k, v in classes.items()}
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        s = cell.get("style", "")
        # Inheritance: dashed block arrow, no diamond
        if "dashed=1" in s and "block" in s and "diamondThin" not in s:
            src = id_to_name.get(cell.get("source", ""))
            tgt = id_to_name.get(cell.get("target", ""))
            if src and tgt and src in classes and tgt in classes:
                parent_of[src] = tgt
                if src not in children_of[tgt]:
                    children_of[tgt].append(src)
    return parent_of, children_of


def _compute_depths(classes, parent_of):
    """Return {class_name: depth} where depth 0 = root (no parent)."""
    depths = {}
    def depth(name):
        if name in depths:
            return depths[name]
        p = parent_of.get(name)
        depths[name] = 0 if p is None else depth(p) + 1
        return depths[name]
    for n in classes:
        depth(n)
    return depths


def _hierarchical_positions(classes, root_xml, h_gap, v_gap):
    """
    Compute {name: (x, y)} using a hierarchical tree layout.

    Rules:
    - Depth 0 (no parent in any inheritance edge) = top row
    - Each successive depth level = one row lower
    - Within a row, siblings are kept together under their parent
    - Classes with no inheritance relationships (islands) go in the final row
    - Row y-start = sum of all previous rows' max-heights + v_gap each

    This ensures parents are always visually above children (readable top→bottom)
    and siblings cluster together (readable left→right).
    """
    from collections import defaultdict

    parent_of, children_of = _build_inheritance_graph(root_xml, classes)
    depths = _compute_depths(classes, parent_of)

    widths  = {n: float(c.find("mxGeometry").get("width",  DEFAULT_WIDTH))
               for n, c in classes.items()}
    heights = {n: float(c.find("mxGeometry").get("height", 100))
               for n, c in classes.items()}

    max_depth = max(depths.values()) if depths else 0

    # Group into depth levels, sort siblings together under their parent
    levels = defaultdict(list)
    for name in classes:
        levels[depths[name]].append(name)

    def sort_key(name):
        p = parent_of.get(name)
        if p is None:
            return (0, name)
        p_level = levels[depths.get(p, 0)]
        p_idx = p_level.index(p) if p in p_level else 0
        return (p_idx, name)

    for d in range(max_depth + 1):
        levels[d].sort(key=sort_key)

    positions = {}
    y_cursor = START_Y
    for d in range(max_depth + 1):
        level = levels[d]
        if not level:
            continue
        level_h = max(heights[n] for n in level)
        x_cursor = START_X
        for name in level:
            positions[name] = (x_cursor, y_cursor)
            x_cursor += widths[name] + h_gap
        y_cursor += level_h + v_gap

    return positions


def _refit_frames(root, classes, padding=30):
    """Re-expand UML frames to tightly wrap their enclosed classes."""
    for frame in root.findall("mxCell"):
        if "shape=umlFrame" not in frame.get("style", ""):
            continue
        fg = frame.find("mxGeometry")
        if fg is None:
            continue
        # A frame's value is its package name; we stored which classes belong
        # to it when we created it.  Post-relayout we don't have that mapping,
        # so instead we look for classes whose centre falls inside an expanded
        # version of the old frame bbox (generous 300px margin).
        fx = float(fg.get("x", 0));  fy = float(fg.get("y", 0))
        fw = float(fg.get("width", 400)); fh = float(fg.get("height", 300))
        inside = []
        for name, cls in classes.items():
            g = cls.find("mxGeometry")
            if g is None:
                continue
            cx = float(g.get("x", 0)); cy = float(g.get("y", 0))
            cw = float(g.get("width", DEFAULT_WIDTH))
            ch = float(g.get("height", 100))
            # class centre
            mx = cx + cw / 2;  my = cy + ch / 2
            if (fx - 300 <= mx <= fx + fw + 300 and
                    fy - 300 <= my <= fy + fh + 300):
                inside.append((cx, cy, cw, ch))
        if inside:
            min_x = min(c[0] for c in inside) - padding
            min_y = min(c[1] for c in inside) - padding - 20
            max_x = max(c[0] + c[2] for c in inside) + padding
            max_y = max(c[1] + c[3] for c in inside) + padding
            fg.set("x", str(int(min_x)));   fg.set("y", str(int(min_y)))
            fg.set("width",  str(int(max_x - min_x)))
            fg.set("height", str(int(max_y - min_y)))


def cmd_relayout(args):
    """Re-position all classes using actual heights + hierarchical tree ordering.

    ALWAYS run this AFTER all add-field / add-method commands so heights are real.
    The algorithm:
      1. Build inheritance graph (dashed-block edges).
      2. Assign each class a depth (0 = abstract root, 1 = first subclass, etc.).
      3. Each depth level occupies one row; row height = tallest class in that row.
      4. Within a row, siblings are grouped under their parent (left-to-right order).
      5. Classes with no inheritance go in the last row.
    Result: parents always above children, siblings grouped, no overlaps.
    """
    tree, root = load_diagram(args.file)
    classes = get_all_classes(root)
    if not classes:
        print("No classes to relayout.")
        return

    h_gap = args.hgap if (hasattr(args, "hgap") and args.hgap) else GRID_COL_SPACING
    v_gap = args.vgap if (hasattr(args, "vgap") and args.vgap) else GRID_ROW_SPACING

    positions = _hierarchical_positions(classes, root, h_gap, v_gap)

    for name, (x, y) in positions.items():
        geo = classes[name].find("mxGeometry")
        geo.set("x", str(int(x)))
        geo.set("y", str(int(y)))

    _refit_frames(root, classes)
    save_diagram(tree, args.file)

    n_levels = len(set(_compute_depths(classes, _build_inheritance_graph(root, classes)[0]).values()))
    print(f"✓ Hierarchical relayout: {len(classes)} classes across {n_levels} depth levels.")


# ─── Verify ───────────────────────────────────────────────────────────────────

def cmd_verify(args):
    """
    Audit a diagram for layout and style problems.

    Checks performed (with XML-level detail so issues are unambiguous):

    V1  CLASS OVERLAP      — two class bounding boxes intersect
    V2  PARENT ABOVE CHILD — a subclass has lower y than its superclass
                             (child should be BELOW parent on the canvas)
    V3  EDGE STYLE         — inheritance must NOT have edgeStyle= (straight
                             diagonal lines); structural edges (association,
                             composition, aggregation) MUST have
                             edgeStyle=orthogonalEdgeStyle
    V4  WAYPOINTS          — edges with explicit <Array as="points"> waypoints
                             may produce unnecessary bends; flag them

    Exit code 0 = clean, 1 = issues found (useful for scripting).
    Pass --fix to automatically apply what can be fixed programmatically
    (overlap → relayout, edge styles → rewrite style strings).
    Waypoints and direction issues require relayout to fix.
    """
    tree, root = load_diagram(args.file)
    classes = get_all_classes(root)
    id_to_name = {v.get("id"): k for k, v in classes.items()}

    issues = []

    # ── V1: Class bounding-box overlaps ──────────────────────────────────────
    # Two rects overlap iff:
    #   A.x < B.x+B.w  AND  A.x+A.w > B.x
    #   A.y < B.y+B.h  AND  A.y+A.h > B.y
    boxes = []
    for name, cls in classes.items():
        g = cls.find("mxGeometry")
        if g is None:
            continue
        boxes.append((name,
                       float(g.get("x", 0)),  float(g.get("y", 0)),
                       float(g.get("width", DEFAULT_WIDTH)),
                       float(g.get("height", 100))))

    for i, (n1, x1, y1, w1, h1) in enumerate(boxes):
        for n2, x2, y2, w2, h2 in boxes[i+1:]:
            if x1 < x2+w2 and x1+w1 > x2 and y1 < y2+h2 and y1+h1 > y2:
                overlap_w = min(x1+w1, x2+w2) - max(x1, x2)
                overlap_h = min(y1+h1, y2+h2) - max(y1, y2)
                issues.append({
                    "code": "V1",
                    "severity": "ERROR",
                    "msg": (f"CLASS OVERLAP: '{n1}' and '{n2}' overlap by "
                            f"{int(overlap_w)}×{int(overlap_h)}px"),
                    "detail": (f"  {n1}: x={int(x1)} y={int(y1)} "
                               f"w={int(w1)} h={int(h1)} "
                               f"→ right={int(x1+w1)} bottom={int(y1+h1)}\n"
                               f"  {n2}: x={int(x2)} y={int(y2)} "
                               f"w={int(w2)} h={int(h2)} "
                               f"→ right={int(x2+w2)} bottom={int(y2+h2)}\n"
                               f"  Fix: run `relayout`"),
                })

    # ── V2: Parent should be above (lower y) than child ───────────────────────
    parent_of, _ = _build_inheritance_graph(root, classes)
    depths        = _compute_depths(classes, parent_of)
    for child, parent in parent_of.items():
        cg = classes[child].find("mxGeometry")
        pg = classes[parent].find("mxGeometry")
        if cg is None or pg is None:
            continue
        cy = float(cg.get("y", 0))
        py = float(pg.get("y", 0))
        if cy <= py:   # child is at same row or ABOVE parent — wrong
            issues.append({
                "code": "V2",
                "severity": "ERROR",
                "msg": (f"DIRECTION: '{child}' (y={int(cy)}) should be BELOW "
                        f"its parent '{parent}' (y={int(py)})"),
                "detail": (f"  In UML class diagrams the inheritance arrow points "
                           f"UP from subclass to superclass, so the subclass must "
                           f"sit lower on the canvas (higher y value).\n"
                           f"  Fix: run `relayout` — it places classes by depth "
                           f"so parents are always in an earlier row than children."),
            })

    # ── V3: Edge style correctness ────────────────────────────────────────────
    # Inheritance  → NO edgeStyle= token (Draw.io draws a straight diagonal)
    # Association  → edgeStyle=orthogonalEdgeStyle  (right-angle routing)
    # Composition  → edgeStyle=orthogonalEdgeStyle
    # Aggregation  → edgeStyle=orthogonalEdgeStyle
    # Dependency   → no edgeStyle required (dashed straight is fine)
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        s  = cell.get("style", "")
        eid = cell.get("id", "?")
        src_name = id_to_name.get(cell.get("source", ""), "?")
        tgt_name = id_to_name.get(cell.get("target", ""), "?")
        label    = f"{src_name} → {tgt_name}"

        is_inheritance  = "dashed=1" in s and "block" in s and "diamondThin" not in s
        is_composition  = "diamondThin" in s and "endFill=1" in s
        is_aggregation  = "diamondThin" in s and "startFill=0" in s
        is_association  = (not is_inheritance and not is_composition
                           and not is_aggregation and "dashed=1" not in s
                           and cell.get("source") and cell.get("target"))

        has_ortho = "edgeStyle=orthogonalEdgeStyle" in s
        has_edge_style = "edgeStyle=" in s

        if is_inheritance and has_edge_style:
            issues.append({
                "code": "V3",
                "severity": "WARN",
                "msg": (f"EDGE STYLE: inheritance edge ({label}) has an "
                        f"edgeStyle — should be a straight diagonal line"),
                "detail": (f"  Correct inheritance style (no edgeStyle):\n"
                           f"    endArrow=block;dashed=1;endFill=0;endSize=12;"
                           f"html=1;rounded=0;\n"
                           f"  Current: {s[:80]}"),
            })

        if (is_composition or is_aggregation or is_association) and not has_ortho:
            rel = ("composition" if is_composition
                   else "aggregation" if is_aggregation else "association")
            issues.append({
                "code": "V3",
                "severity": "WARN",
                "msg": (f"EDGE STYLE: {rel} edge ({label}) is missing "
                        f"edgeStyle=orthogonalEdgeStyle — will not have "
                        f"right-angle corners"),
                "detail": (f"  Add edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;"
                           f"jettySize=auto; to the style string.\n"
                           f"  Current: {s[:80]}\n"
                           f"  Fix: run `fix-edge-styles`"),
            })

    # ── V4: Explicit waypoints cause extra bends ──────────────────────────────
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        geo = cell.find("mxGeometry")
        if geo is None:
            continue
        pts = geo.find("Array[@as='points']")
        if pts is not None and len(pts) > 0:
            src_name = id_to_name.get(cell.get("source", ""), "?")
            tgt_name = id_to_name.get(cell.get("target", ""), "?")
            n_pts = len(pts)
            issues.append({
                "code": "V4",
                "severity": "INFO",
                "msg": (f"WAYPOINTS: edge {src_name}→{tgt_name} has "
                        f"{n_pts} explicit waypoint(s) — may cause extra bends"),
                "detail": (f"  Explicit waypoints override Draw.io's auto-routing. "
                           f"Remove the <Array as=\"points\"> element to let "
                           f"orthogonal routing find the minimum-bend path.\n"
                           f"  Fix: run `fix-edge-styles` (removes waypoints too)"),
            })

    # ── V5: Multiple edges sharing the same connection point ─────────────────
    # Flag when 2+ edges converge on (or leave) the same class without explicit
    # entryX/entryY (or exitX/exitY) port constraints — they pile up visually.
    from collections import defaultdict as _defaultdict
    _tgt_groups = _defaultdict(list)
    _src_groups = _defaultdict(list)
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        tgt = cell.get("target", "")
        src = cell.get("source", "")
        style = cell.get("style", "")
        has_entry = "entryX=" in style or "entryY=" in style
        has_exit  = "exitX="  in style or "exitY="  in style
        if tgt:
            _tgt_groups[tgt].append((cell, has_entry))
        if src:
            _src_groups[src].append((cell, has_exit))

    for tgt_id, grp in _tgt_groups.items():
        unconstrained = [c for c, has_c in grp if not has_c]
        if len(unconstrained) >= 2:
            tgt_name = id_to_name.get(tgt_id, f"[{tgt_id[:8]}]")
            src_names = [id_to_name.get(c.get("source", ""), "?")
                         for c in unconstrained]
            issues.append({
                "code": "V5",
                "severity": "WARN",
                "msg": (f"SHARED ENDPOINT: {len(unconstrained)} edges converge on "
                        f"'{tgt_name}' with no entryX/entryY — arrows will pile up"),
                "detail": (f"  Sources without entry constraints: "
                           f"{', '.join(src_names)}\n"
                           f"  Fix: run `fix-shared-endpoints` to spread "
                           f"connection points automatically."),
            })

    for src_id, grp in _src_groups.items():
        unconstrained = [c for c, has_c in grp if not has_c]
        if len(unconstrained) >= 2:
            src_name = id_to_name.get(src_id, f"[{src_id[:8]}]")
            tgt_names = [id_to_name.get(c.get("target", ""), "?")
                         for c in unconstrained]
            issues.append({
                "code": "V5",
                "severity": "WARN",
                "msg": (f"SHARED ENDPOINT: {len(unconstrained)} edges leave "
                        f"'{src_name}' with no exitX/exitY — arrows will pile up"),
                "detail": (f"  Targets without exit constraints: "
                           f"{', '.join(tgt_names)}\n"
                           f"  Fix: run `fix-shared-endpoints` to spread "
                           f"connection points automatically."),
            })

    # ── V6: Straight-line edge corridor intersects an unrelated class ─────────
    # For edges without orthogonal routing (straight dependencies), the path is
    # approximated as a line segment from source center to target center.
    # Flag any third class whose bounding box that segment crosses.
    def _seg_rect_intersects(x1, y1, x2, y2, rx, ry, rw, rh):
        """True if segment P1–P2 crosses the axis-aligned rectangle."""
        rx2, ry2 = rx + rw, ry + rh
        def _in(px, py):
            return rx < px < rx2 and ry < py < ry2
        if _in(x1, y1) or _in(x2, y2):
            return True
        dx, dy = x2 - x1, y2 - y1
        for sx1, sy1, sx2, sy2 in [
            (rx, ry, rx2, ry), (rx, ry2, rx2, ry2),
            (rx, ry, rx, ry2), (rx2, ry, rx2, ry2),
        ]:
            dxs, dys = sx2 - sx1, sy2 - sy1
            cross = dx * dys - dy * dxs
            if abs(cross) < 1e-10:
                continue
            t = ((sx1 - x1) * dys - (sy1 - y1) * dxs) / cross
            u = ((sx1 - x1) * dy  - (sy1 - y1) * dx)  / cross
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                return True
        return False

    _box_map = {}
    for name, cls in classes.items():
        g = cls.find("mxGeometry")
        if g is not None:
            _box_map[name] = (float(g.get("x", 0)), float(g.get("y", 0)),
                              float(g.get("width", DEFAULT_WIDTH)),
                              float(g.get("height", 100)))

    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        src_id = cell.get("source", "")
        tgt_id = cell.get("target", "")
        if not src_id or not tgt_id:
            continue
        src_name = id_to_name.get(src_id)
        tgt_name = id_to_name.get(tgt_id)
        if src_name is None or tgt_name is None:
            continue
        style = cell.get("style", "")
        # Only straight-line edges (no orthogonal auto-routing) can cross boxes
        if "edgeStyle=orthogonalEdgeStyle" in style:
            continue
        if src_name not in _box_map or tgt_name not in _box_map:
            continue
        sx, sy, sw, sh = _box_map[src_name]
        tx, ty, tw, th = _box_map[tgt_name]
        scx, scy = sx + sw / 2, sy + sh / 2
        tcx, tcy = tx + tw / 2, ty + th / 2

        # Build the polyline: src_center → [waypoints] → tgt_center
        # Waypoints in <Array as="points"><mxPoint x=… y=…/></Array> are
        # absolute canvas coordinates and bend the otherwise-straight edge.
        geo = cell.find("mxGeometry")
        waypoints = []
        if geo is not None:
            pts_el = geo.find("Array[@as='points']")
            if pts_el is not None:
                for pt in pts_el.findall("mxPoint"):
                    try:
                        waypoints.append((float(pt.get("x", 0)),
                                          float(pt.get("y", 0))))
                    except (TypeError, ValueError):
                        pass

        poly = [(scx, scy)] + waypoints + [(tcx, tcy)]

        # Shrink test rects by 5 px to avoid false positives at shared borders
        MARGIN = 5
        blockers = set()
        for seg_i in range(len(poly) - 1):
            p1x, p1y = poly[seg_i]
            p2x, p2y = poly[seg_i + 1]
            for other, (ox, oy, ow, oh) in _box_map.items():
                if other in (src_name, tgt_name):
                    continue
                if _seg_rect_intersects(p1x, p1y, p2x, p2y,
                                        ox + MARGIN, oy + MARGIN,
                                        ow - 2 * MARGIN, oh - 2 * MARGIN):
                    blockers.add(other)

        if blockers:
            issues.append({
                "code": "V6",
                "severity": "WARN",
                "msg": (f"ARROW OVERLAP: straight edge {src_name}→{tgt_name} "
                        f"passes through {', '.join(sorted(blockers))}"),
                "detail": (f"  The dependency line from {src_name} to "
                           f"{tgt_name} crosses: {', '.join(sorted(blockers))}.\n"
                           f"  Fix: run `fix-arrow-overlaps` — it picks the "
                           f"shortest bypass waypoint around the blocking class."),
            })

    # ── Report ────────────────────────────────────────────────────────────────
    errors   = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]
    infos    = [i for i in issues if i["severity"] == "INFO"]

    if not issues:
        print(f"✓ Diagram looks clean — no overlaps, correct edge styles, "
              f"parents above children.")
        return

    print(f"\n{'='*64}")
    print(f"Verify: {args.file}")
    print(f"{'='*64}")
    print(f"  {len(errors)} error(s)   {len(warnings)} warning(s)   {len(infos)} info(s)\n")

    for issue in issues:
        icon = {"ERROR": "✗", "WARN": "⚠", "INFO": "ℹ"}[issue["severity"]]
        print(f"{icon} [{issue['code']}] {issue['msg']}")
        if args.verbose if hasattr(args, "verbose") else False:
            print(issue["detail"])
            print()

    if not (args.verbose if hasattr(args, "verbose") else False):
        print("\n(run with --verbose for XML-level detail and fix suggestions)")

    if errors:
        sys.exit(1)


def cmd_fix_edge_styles(args):
    """
    Fix V3 and V4 issues in-place:
    - Add edgeStyle=orthogonalEdgeStyle to association/composition/aggregation edges
    - Remove explicit waypoint arrays (let Draw.io re-route automatically)
    - Remove edgeStyle from pure inheritance edges
    """
    tree, root = load_diagram(args.file)
    fixed = 0

    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        s = cell.get("style", "")

        is_inheritance = "dashed=1" in s and "block" in s and "diamondThin" not in s
        is_structural  = (("diamondThin" in s) or
                          ("edgeStyle=orthogonalEdgeStyle" in s) or
                          (not is_inheritance and cell.get("source")
                           and cell.get("target") and "dashed=1" not in s))

        new_s = s

        # Inheritance: strip any edgeStyle token
        if is_inheritance and "edgeStyle=" in s:
            import re
            new_s = re.sub(r"edgeStyle=[^;]+;?", "", new_s)
            new_s = re.sub(r"orthogonalLoop=[^;]+;?", "", new_s)
            new_s = re.sub(r"jettySize=[^;]+;?", "", new_s)
            new_s = new_s.replace(";;", ";").strip(";") + ";"

        # Structural: ensure orthogonal routing
        if is_structural and "edgeStyle=orthogonalEdgeStyle" not in s:
            new_s = "edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;" + new_s

        if new_s != s:
            cell.set("style", new_s)
            fixed += 1

        # Remove explicit waypoints (V4)
        geo = cell.find("mxGeometry")
        if geo is not None:
            pts = geo.find("Array[@as='points']")
            if pts is not None:
                geo.remove(pts)
                fixed += 1

    save_diagram(tree, args.file)
    print(f"✓ Fixed edge styles on {fixed} element(s).")


def cmd_fix_shared_endpoints(args):
    """
    Fix V5: distribute entryX/entryY (and exitX/exitY) on classes that have
    two or more unconstrained edges converging at the same connection point.

    For each class with 2+ incoming edges that lack entryX/entryY:
      - determines the dominant approach side (top / bottom / left / right)
        by comparing each source's center to the target's center
      - assigns evenly-spaced fractional entry points along that side
    The same logic applies to outgoing edges that lack exitX/exitY.
    """
    import re as _re
    from collections import defaultdict as _dd

    tree, root = load_diagram(args.file)
    classes = get_all_classes(root)
    id_to_name = {v.get("id"): k for k, v in classes.items()}

    def _bbox(cls_name):
        cls = classes.get(cls_name)
        if cls is None:
            return None
        g = cls.find("mxGeometry")
        if g is None:
            return None
        return (float(g.get("x", 0)), float(g.get("y", 0)),
                float(g.get("width", DEFAULT_WIDTH)),
                float(g.get("height", 100)))

    def _center(cls_name):
        bb = _bbox(cls_name)
        if bb is None:
            return 0.0, 0.0
        x, y, w, h = bb
        return x + w / 2, y + h / 2

    def _dominant_entry_side(src_centers, tgt_bb):
        """Which side of the target do the sources approach from?"""
        tx, ty, tw, th = tgt_bb
        tcx, tcy = tx + tw / 2, ty + th / 2
        votes = {"top": 0, "bottom": 0, "left": 0, "right": 0}
        for sx, sy in src_centers:
            dx, dy = sx - tcx, sy - tcy
            if abs(dy) >= abs(dx):
                votes["bottom" if dy > 0 else "top"] += 1
            else:
                votes["right" if dx > 0 else "left"] += 1
        return max(votes, key=votes.get)

    def _dominant_exit_side(tgt_centers, src_bb):
        """Which side of the source do the targets sit on?"""
        sx, sy, sw, sh = src_bb
        scx, scy = sx + sw / 2, sy + sh / 2
        votes = {"top": 0, "bottom": 0, "left": 0, "right": 0}
        for tx, ty in tgt_centers:
            dx, dy = tx - scx, ty - scy
            if abs(dy) >= abs(dx):
                votes["bottom" if dy > 0 else "top"] += 1
            else:
                votes["right" if dx > 0 else "left"] += 1
        return max(votes, key=votes.get)

    def _strip_port(style, prefix):
        """Remove existing entry*/exit* port tokens from a style string."""
        style = _re.sub(rf"{prefix}[XY]=[^;]+;?", "", style)
        style = _re.sub(rf"{prefix}D[xy]=[^;]+;?", "", style)
        return style.replace(";;", ";").strip(";")

    def _entry_tokens(idx, n, side):
        frac = round((idx + 1) / (n + 1), 3)
        if side == "bottom":
            return f"entryX={frac};entryY=1;entryDx=0;entryDy=0;"
        if side == "top":
            return f"entryX={frac};entryY=0;entryDx=0;entryDy=0;"
        if side == "left":
            return f"entryX=0;entryY={frac};entryDx=0;entryDy=0;"
        return     f"entryX=1;entryY={frac};entryDx=0;entryDy=0;"

    def _exit_tokens(idx, n, side):
        frac = round((idx + 1) / (n + 1), 3)
        if side == "top":
            return f"exitX={frac};exitY=0;exitDx=0;exitDy=0;"
        if side == "bottom":
            return f"exitX={frac};exitY=1;exitDx=0;exitDy=0;"
        if side == "left":
            return f"exitX=0;exitY={frac};exitDx=0;exitDy=0;"
        return     f"exitX=1;exitY={frac};exitDx=0;exitDy=0;"

    all_edges = [c for c in root.findall("mxCell") if c.get("edge") == "1"]
    fixed = 0

    # ── Incoming: group by target, find unconstrained edges ──────────────────
    tgt_map = _dd(list)
    for cell in all_edges:
        tgt = cell.get("target", "")
        if not tgt or tgt not in id_to_name:
            continue
        s = cell.get("style", "")
        if "entryX=" not in s and "entryY=" not in s:
            tgt_map[tgt].append(cell)

    for tgt_id, cells in tgt_map.items():
        if len(cells) < 2:
            continue
        tgt_name = id_to_name[tgt_id]
        tgt_bb = _bbox(tgt_name)
        if tgt_bb is None:
            continue

        src_centers = [_center(id_to_name.get(c.get("source", ""), ""))
                       for c in cells]
        side = _dominant_entry_side(src_centers, tgt_bb)

        # Sort by the axis perpendicular to the entry side so ports are ordered
        axis = 0 if side in ("top", "bottom") else 1
        sorted_cells = sorted(cells,
                              key=lambda c: _center(
                                  id_to_name.get(c.get("source", ""), "")
                              )[axis])
        n = len(sorted_cells)
        for idx, cell in enumerate(sorted_cells):
            base = _strip_port(cell.get("style", ""), "entry")
            cell.set("style", base + ";" + _entry_tokens(idx, n, side))
            fixed += 1

        tgt_name2 = id_to_name[tgt_id]
        src_names = [id_to_name.get(c.get("source", ""), "?") for c in sorted_cells]
        print(f"  ✓ Spread {n} entry points on '{tgt_name2}' "
              f"({side} side): {', '.join(src_names)}")

    # ── Outgoing: group by source, find unconstrained edges ──────────────────
    src_map = _dd(list)
    for cell in all_edges:
        src = cell.get("source", "")
        if not src or src not in id_to_name:
            continue
        s = cell.get("style", "")
        if "exitX=" not in s and "exitY=" not in s:
            src_map[src].append(cell)

    for src_id, cells in src_map.items():
        if len(cells) < 2:
            continue
        src_name = id_to_name[src_id]
        src_bb = _bbox(src_name)
        if src_bb is None:
            continue

        tgt_centers = [_center(id_to_name.get(c.get("target", ""), ""))
                       for c in cells]
        side = _dominant_exit_side(tgt_centers, src_bb)

        axis = 0 if side in ("top", "bottom") else 1
        sorted_cells = sorted(cells,
                              key=lambda c: _center(
                                  id_to_name.get(c.get("target", ""), "")
                              )[axis])
        n = len(sorted_cells)
        for idx, cell in enumerate(sorted_cells):
            base = _strip_port(cell.get("style", ""), "exit")
            cell.set("style", base + ";" + _exit_tokens(idx, n, side))
            fixed += 1

        tgt_names = [id_to_name.get(c.get("target", ""), "?") for c in sorted_cells]
        print(f"  ✓ Spread {n} exit points from '{src_name}' "
              f"({side} side): {', '.join(tgt_names)}")

    save_diagram(tree, args.file)
    print(f"✓ fix-shared-endpoints: distributed {fixed} connection point(s).")


def cmd_fix_arrow_overlaps(args):
    """
    Fix V6: add a single bypass waypoint to straight-line edges that cross
    an unrelated class bounding box.

    Algorithm:
      For each offending edge (source → target that crosses blocker B):
        1. Compute the centre of the blocker.
        2. Try 4 bypass waypoints — just outside each side of B with a
           configurable clearance gap (default 30 px).
        3. Pick the candidate that minimises total path length
           dist(src_centre, waypoint) + dist(waypoint, tgt_centre).
        4. Write the chosen point as <Array as="points"><mxPoint …/></Array>
           inside the edge's <mxGeometry>.

    Only straight-line edges (no edgeStyle=orthogonalEdgeStyle) are processed;
    orthogonal edges route themselves automatically.
    """
    import math as _math

    DETECT_MARGIN = 5    # shrink blocker box for detection (matches verify V6)
    BYPASS_GAP    = 30   # clearance past the blocker's edge for the waypoint

    tree, root = load_diagram(args.file)
    classes = get_all_classes(root)
    id_to_name = {v.get("id"): k for k, v in classes.items()}

    box_map = {}
    for name, cls in classes.items():
        g = cls.find("mxGeometry")
        if g is not None:
            box_map[name] = (float(g.get("x", 0)), float(g.get("y", 0)),
                             float(g.get("width",  DEFAULT_WIDTH)),
                             float(g.get("height", 100)))

    def _seg_rect_intersects(x1, y1, x2, y2, rx, ry, rw, rh):
        rx2, ry2 = rx + rw, ry + rh
        def _in(px, py):
            return rx < px < rx2 and ry < py < ry2
        if _in(x1, y1) or _in(x2, y2):
            return True
        dx, dy = x2 - x1, y2 - y1
        for sx1, sy1, sx2, sy2 in [
            (rx, ry, rx2, ry), (rx, ry2, rx2, ry2),
            (rx, ry, rx, ry2), (rx2, ry, rx2, ry2),
        ]:
            dxs, dys = sx2 - sx1, sy2 - sy1
            cross = dx * dys - dy * dxs
            if abs(cross) < 1e-10:
                continue
            t = ((sx1 - x1) * dys - (sy1 - y1) * dxs) / cross
            u = ((sx1 - x1) * dy  - (sy1 - y1) * dx)  / cross
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                return True
        return False

    fixed = 0

    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        src_id = cell.get("source", "")
        tgt_id = cell.get("target", "")
        if not src_id or not tgt_id:
            continue
        src_name = id_to_name.get(src_id)
        tgt_name = id_to_name.get(tgt_id)
        if src_name is None or tgt_name is None:
            continue
        style = cell.get("style", "")
        if "edgeStyle=orthogonalEdgeStyle" in style:
            continue  # orthogonal edges route themselves
        if src_name not in box_map or tgt_name not in box_map:
            continue

        sx, sy, sw, sh = box_map[src_name]
        tx, ty, tw, th = box_map[tgt_name]
        scx, scy = sx + sw / 2, sy + sh / 2
        tcx, tcy = tx + tw / 2, ty + th / 2

        # Collect all blocking classes (shrunk by DETECT_MARGIN)
        blockers = [
            (bname, box_map[bname])
            for bname in box_map
            if bname not in (src_name, tgt_name)
            and _seg_rect_intersects(
                scx, scy, tcx, tcy,
                box_map[bname][0] + DETECT_MARGIN,
                box_map[bname][1] + DETECT_MARGIN,
                box_map[bname][2] - 2 * DETECT_MARGIN,
                box_map[bname][3] - 2 * DETECT_MARGIN,
            )
        ]

        if not blockers:
            continue

        # Use the first (primary) blocker — usually only one
        blocker_name, (rx, ry, rw, rh) = blockers[0]
        rcx, rcy = rx + rw / 2, ry + rh / 2

        # 8 candidate bypass waypoints: 4 edge-midpoints + 4 corners
        # Placed just outside the blocker's bounding box with BYPASS_GAP clearance.
        candidates = [
            (rcx,                    ry  - BYPASS_GAP,       "above"),
            (rcx,                    ry  + rh + BYPASS_GAP,  "below"),
            (rx  - BYPASS_GAP,       rcy,                    "left"),
            (rx  + rw + BYPASS_GAP,  rcy,                    "right"),
            # corners
            (rx  - BYPASS_GAP,       ry  - BYPASS_GAP,       "top-left"),
            (rx  + rw + BYPASS_GAP,  ry  - BYPASS_GAP,       "top-right"),
            (rx  - BYPASS_GAP,       ry  + rh + BYPASS_GAP,  "bottom-left"),
            (rx  + rw + BYPASS_GAP,  ry  + rh + BYPASS_GAP,  "bottom-right"),
        ]

        # ── helper: does segment (ax,ay)→(bx,by) cross any unrelated class? ──
        def _seg_free(ax, ay, bx, by):
            shrink = DETECT_MARGIN
            for oname, (ox, oy, ow, oh) in box_map.items():
                if oname in (src_name, tgt_name):
                    continue
                ow2 = ow - 2 * shrink
                oh2 = oh - 2 * shrink
                if ow2 <= 0 or oh2 <= 0:
                    continue
                if _seg_rect_intersects(ax, ay, bx, by,
                                        ox + shrink, oy + shrink, ow2, oh2):
                    return False
            return True

        def _dist(ax, ay, bx, by):
            return _math.hypot(bx - ax, by - ay)

        # ── generate the 8 bypass candidates for a given blocker box ─────────
        def _bypass_candidates(bx, by, bw, bh):
            bcx, bcy = bx + bw / 2, by + bh / 2
            return [
                (bcx,              by  - BYPASS_GAP,       "above"),
                (bcx,              by  + bh + BYPASS_GAP,  "below"),
                (bx  - BYPASS_GAP, bcy,                    "left"),
                (bx  + bw + BYPASS_GAP, bcy,               "right"),
                (bx  - BYPASS_GAP,       by  - BYPASS_GAP,       "top-left"),
                (bx  + bw + BYPASS_GAP,  by  - BYPASS_GAP,       "top-right"),
                (bx  - BYPASS_GAP,       by  + bh + BYPASS_GAP,  "bottom-left"),
                (bx  + bw + BYPASS_GAP,  by  + bh + BYPASS_GAP,  "bottom-right"),
            ]

        # ── first-blocker encountered along a segment ─────────────────────────
        def _first_blocker_t(ax, ay, bx, by):
            shrink = DETECT_MARGIN
            best = None
            dx, dy = bx - ax, by - ay
            length_sq = dx * dx + dy * dy
            for oname, (ox, oy, ow, oh) in box_map.items():
                if oname in (src_name, tgt_name):
                    continue
                ow2 = ow - 2 * shrink
                oh2 = oh - 2 * shrink
                if ow2 <= 0 or oh2 <= 0:
                    continue
                if _seg_rect_intersects(ax, ay, bx, by,
                                        ox + shrink, oy + shrink, ow2, oh2):
                    # project blocker centre onto segment to get t
                    bcx2 = ox + ow / 2
                    bcy2 = oy + oh / 2
                    t = 0.0
                    if length_sq > 1e-10:
                        t = ((bcx2 - ax) * dx + (bcy2 - ay) * dy) / length_sq
                    if best is None or t < best[0]:
                        best = (t, oname, (ox, oy, ow, oh))
            return best  # None or (t, name, box)

        # ── recursive path finder (max depth controls max extra waypoints) ─────
        def _find_waypoints(ax, ay, bx, by, depth):
            """Return list of (x,y) waypoints between (ax,ay) and (bx,by), or None."""
            if _seg_free(ax, ay, bx, by):
                return []          # direct segment is clear
            if depth <= 0:
                return None        # give up

            hit = _first_blocker_t(ax, ay, bx, by)
            if hit is None:
                return []

            _, _, (rx, ry, rw, rh) = hit
            bypass = _bypass_candidates(rx, ry, rw, rh)

            # Sort bypass candidates by total detour length
            bypass.sort(key=lambda c: _dist(ax, ay, c[0], c[1]) +
                                       _dist(c[0], c[1], bx, by))

            for cwx, cwy, _ in bypass:
                sub1 = _find_waypoints(ax, ay,  cwx, cwy, depth - 1)
                if sub1 is None:
                    continue
                sub2 = _find_waypoints(cwx, cwy, bx, by,  depth - 1)
                if sub2 is None:
                    continue
                return sub1 + [(cwx, cwy)] + sub2

            return None  # no bypass found

        # Try to find a clean path — up to 2 intermediate waypoints
        waypoint_list = _find_waypoints(scx, scy, tcx, tcy, depth=2)

        if not waypoint_list:
            # Last resort: shortest of the 8 bypass candidates regardless
            best = min(candidates,
                       key=lambda c: _dist(scx, scy, c[0], c[1]) +
                                     _dist(c[0], c[1], tcx, tcy))
            waypoint_list = [(best[0], best[1])]
            direction = "fallback"
        else:
            direction = f"{len(waypoint_list)}-pt"

        # Ensure mxGeometry exists
        geo = cell.find("mxGeometry")
        if geo is None:
            geo = ET.SubElement(cell, "mxGeometry")
            geo.set("relative", "1")
            geo.set("as", "geometry")

        # Replace any existing points array
        existing = geo.find("Array[@as='points']")
        if existing is not None:
            geo.remove(existing)

        pts = ET.SubElement(geo, "Array")
        pts.set("as", "points")
        for pwx, pwy in waypoint_list:
            pt = ET.SubElement(pts, "mxPoint")
            pt.set("x", str(int(pwx)))
            pt.set("y", str(int(pwy)))

        coords = " → ".join(f"({int(x)},{int(y)})" for x, y in waypoint_list)
        print(f"  ✓ {src_name}→{tgt_name}: routed via {coords} [{direction}]")
        fixed += 1

    save_diagram(tree, args.file)
    print(f"✓ fix-arrow-overlaps: added {fixed} bypass waypoint(s).")


# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_new(args):
    create_new_diagram(args.file)
    print(f"✓ Created new diagram: {args.file}")


def cmd_add_class(args):
    tree, root = load_diagram(args.file)
    classes = get_all_classes(root)

    if args.name in classes:
        print(f"⚠  Class '{args.name}' already exists — skipping.")
        return

    x = args.x if args.x is not None else next_class_position(root)[0]
    y = args.y if args.y is not None else next_class_position(root)[1]
    w = args.width or DEFAULT_WIDTH

    class_id = new_id()
    divider_id = new_id()

    # Class container
    # If a stereotype is provided, embed it in the header as «stereotype»<br><b>Name</b>
    # so draw.io renders it above the class name in the title cell.
    if getattr(args, 'stereotype', None):
        # Use HTML-encoded angle brackets so draw.io renders <<scan>> literally.
        # Class name remains bold (swimlane fontStyle=1) but stereotype line
        # overrides to non-bold italic via inline span.
        header_label = (
            f"<font style=\"font-weight:normal;font-style:italic;\">"
            f"&lt;&lt;{args.stereotype}&gt;&gt;</font><br>{args.name}"
        )
        header_height = HEADER_HEIGHT + 18  # extra line for stereotype
    else:
        header_label = args.name
        header_height = HEADER_HEIGHT

    cls = ET.SubElement(root, "mxCell")
    cls.set("id", class_id)
    cls.set("value", header_label)
    cls.set("style", CLASS_STYLE.replace("startSize=26", f"startSize={header_height}"))
    cls.set("vertex", "1")
    cls.set("parent", "1")
    geo = ET.SubElement(cls, "mxGeometry")
    geo.set("x", str(x))
    geo.set("y", str(y))
    geo.set("width", str(w))
    geo.set("height", str(header_height + DIVIDER_HEIGHT))
    geo.set("as", "geometry")

    # Divider (separates fields from methods).
    # y=header_height because child coords are from the top of the whole
    # swimlane cell — the header occupies y=0..header_height, content below.
    div = ET.SubElement(root, "mxCell")
    div.set("id", divider_id)
    div.set("value", "")
    div.set("style", DIVIDER_STYLE)
    div.set("vertex", "1")
    div.set("parent", class_id)
    dgeo = ET.SubElement(div, "mxGeometry")
    dgeo.set("y", str(header_height))
    dgeo.set("width", str(w))
    dgeo.set("height", str(DIVIDER_HEIGHT))
    dgeo.set("as", "geometry")

    save_diagram(tree, args.file)
    print(f"✓ Added class: {args.name}")


def cmd_add_field(args):
    tree, root = load_diagram(args.file)
    cls = find_class(root, args.class_name)
    class_id = cls.get("id")
    w = int(cls.find("mxGeometry").get("width", DEFAULT_WIDTH))

    divider = get_divider(root, class_id)
    if divider is None:
        raise ValueError(f"Class '{args.class_name}' has no divider — corrupted class?")

    div_geo = divider.find("mxGeometry")
    div_y = float(div_geo.get("y", 0))

    # Collect all children; shift divider + anything after it down by CELL_HEIGHT
    children = get_class_children(root, class_id)
    for child in children:
        child_geo = child.find("mxGeometry")
        if child_geo is None:
            continue
        child_y = float(child_geo.get("y", 0))
        if child_y >= div_y:
            child_geo.set("y", str(int(child_y) + CELL_HEIGHT))

    # Insert field just before where the divider was
    field_id = new_id()
    style = FIELD_STYLE_ABSTRACT if args.abstract else FIELD_STYLE

    # Draw.io renders field values as HTML (html=1 in FIELD_STYLE).
    # Pre-escape < and > so they display as literal characters, not HTML tags.
    import html as _html
    safe_text = _html.escape(args.text, quote=False)

    field = ET.SubElement(root, "mxCell")
    field.set("id", field_id)
    field.set("value", safe_text)
    field.set("style", style)
    field.set("vertex", "1")
    field.set("parent", class_id)
    fgeo = ET.SubElement(field, "mxGeometry")
    fgeo.set("y", str(int(div_y)))
    fgeo.set("width", str(w))
    fgeo.set("height", str(CELL_HEIGHT))
    fgeo.set("as", "geometry")

    update_class_height(root, cls)
    save_diagram(tree, args.file)
    print(f"✓ Added field to {args.class_name}: {args.text}")


def cmd_add_method(args):
    tree, root = load_diagram(args.file)
    cls = find_class(root, args.class_name)
    class_id = cls.get("id")
    w = int(cls.find("mxGeometry").get("width", DEFAULT_WIDTH))

    # Find the y position after the last child
    children = get_class_children(root, class_id)
    if not children:
        insert_y = 0
    else:
        last_y = 0
        last_h = 0
        for c in children:
            g = c.find("mxGeometry")
            if g is not None:
                y = float(g.get("y", 0))
                h = float(g.get("height", CELL_HEIGHT))
                if y + h > last_y + last_h:
                    last_y = y
                    last_h = h
        insert_y = int(last_y + last_h)

    style = FIELD_STYLE_ABSTRACT if args.abstract else FIELD_STYLE

    method_id = new_id()
    method = ET.SubElement(root, "mxCell")
    method.set("id", method_id)
    method.set("value", args.text)
    method.set("style", style)
    method.set("vertex", "1")
    method.set("parent", class_id)
    mgeo = ET.SubElement(method, "mxGeometry")
    mgeo.set("y", str(insert_y))
    mgeo.set("width", str(w))
    mgeo.set("height", str(CELL_HEIGHT))
    mgeo.set("as", "geometry")

    update_class_height(root, cls)
    save_diagram(tree, args.file)
    print(f"✓ Added method to {args.class_name}: {args.text}")


def _compute_field_exit_entry(root, source_cell, target_cell, field_text, is_exit=True):
    """Compute exitX/exitY or entryX/entryY for a field row.

    Args:
        root: XML root element
        source_cell: source class mxCell (for position)
        target_cell: target class mxCell (for position)
        field_text: field row text to match
        is_exit: True to compute exit coords (from source field), False for entry (from target field)

    Returns:
        (exitX/entryX, exitY/entryY) tuple, or (None, None) if field not found
    """
    # Determine which class to search
    search_class_cell = source_cell if is_exit else target_cell
    search_class_name = _extract_class_name(search_class_cell.get("value", ""))

    # Find the field row
    try:
        field_cell = find_field_row(root, search_class_name, field_text)
    except KeyError:
        return None, None

    # Get field y position and class total height
    field_geo = field_cell.find("mxGeometry")
    if field_geo is None:
        return None, None

    field_y = float(field_geo.get("y", 0))
    field_h = float(field_geo.get("height", CELL_HEIGHT))
    field_y_center = field_y + field_h / 2.0

    # Get class height
    class_cell = source_cell if is_exit else target_cell
    class_geo = class_cell.find("mxGeometry")
    if class_geo is None:
        return None, None
    class_h = float(class_geo.get("height", 100))

    # Normalize to 0..1 range
    y_ratio = field_y_center / class_h if class_h > 0 else 0.5

    # Determine X based on relative positions
    source_geo = source_cell.find("mxGeometry")
    target_geo = target_cell.find("mxGeometry")
    if source_geo is None or target_geo is None:
        return None, None

    source_x = float(source_geo.get("x", 0)) + float(source_geo.get("width", DEFAULT_WIDTH)) / 2.0
    target_x = float(target_geo.get("x", 0)) + float(target_geo.get("width", DEFAULT_WIDTH)) / 2.0

    # Determine exit/entry side
    if is_exit:
        # Exit: if target is to right, exit from right (exitX=1); else from left (exitX=0)
        x_ratio = 1.0 if target_x > source_x else 0.0
    else:
        # Entry: if source is to left, entry from left (entryX=0); else from right (entryX=1)
        x_ratio = 0.0 if source_x < target_x else 1.0

    return x_ratio, y_ratio


def _add_edge(root, source_id, target_id, style, label=None,
              from_mult=None, to_mult=None, stereotype=None):
    """Add a directed edge (relationship) between two classes."""
    edge_id = new_id()
    edge = ET.SubElement(root, "mxCell")
    edge.set("id", edge_id)
    edge.set("value", "")
    edge.set("style", style)
    edge.set("edge", "1")
    edge.set("parent", "1")
    edge.set("source", source_id)
    edge.set("target", target_id)
    ET.SubElement(edge, "mxGeometry").set("as", "geometry")

    # Middle label (association name or stereotype)
    mid_text = label or ""
    if stereotype:
        mid_text = f"&lt;&lt;{stereotype}&gt;&gt;" if not mid_text else mid_text

    if mid_text:
        lbl = ET.SubElement(root, "mxCell")
        lbl.set("id", new_id())
        lbl.set("value", mid_text)
        lbl.set("style", EDGE_LABEL_STYLE)
        lbl.set("vertex", "1")
        lbl.set("connectable", "0")
        lbl.set("parent", edge_id)
        lg = ET.SubElement(lbl, "mxGeometry")
        lg.set("x", "0")
        lg.set("y", "0")
        lg.set("relative", "1")
        lg.set("as", "geometry")

    # Source-end multiplicity
    if from_mult:
        lbl = ET.SubElement(root, "mxCell")
        lbl.set("id", new_id())
        lbl.set("value", from_mult)
        lbl.set("style", EDGE_LABEL_STYLE)
        lbl.set("vertex", "1")
        lbl.set("connectable", "0")
        lbl.set("parent", edge_id)
        lg = ET.SubElement(lbl, "mxGeometry")
        lg.set("x", "-0.85")
        lg.set("y", "0")
        lg.set("relative", "1")
        lg.set("as", "geometry")

    # Target-end multiplicity
    if to_mult:
        lbl = ET.SubElement(root, "mxCell")
        lbl.set("id", new_id())
        lbl.set("value", to_mult)
        lbl.set("style", EDGE_LABEL_STYLE)
        lbl.set("vertex", "1")
        lbl.set("connectable", "0")
        lbl.set("parent", edge_id)
        lg = ET.SubElement(lbl, "mxGeometry")
        lg.set("x", "0.85")
        lg.set("y", "0")
        lg.set("relative", "1")
        lg.set("as", "geometry")

    return edge_id


def cmd_add_association(args):
    tree, root = load_diagram(args.file)
    src = find_class(root, args.from_class)
    tgt = find_class(root, args.to_class)

    style = ASSOCIATION_STYLE

    # Apply field-level exit/entry constraints if provided
    if hasattr(args, 'exit_field') and args.exit_field:
        exit_x, exit_y = _compute_field_exit_entry(root, src, tgt, args.exit_field, is_exit=True)
        if exit_x is not None and exit_y is not None:
            style = (style.rstrip(";") +
                    f";exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;")

    if hasattr(args, 'entry_field') and args.entry_field:
        entry_x, entry_y = _compute_field_exit_entry(root, src, tgt, args.entry_field, is_exit=False)
        if entry_x is not None and entry_y is not None:
            style = (style.rstrip(";") +
                    f";entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;")

    _add_edge(root, src.get("id"), tgt.get("id"), style,
              label=args.label, from_mult=args.from_mult, to_mult=args.to_mult)
    save_diagram(tree, args.file)
    print(f"✓ Added association: {args.from_class} → {args.to_class}"
          + (f" [{args.label}]" if args.label else "")
          + (f" (exit-field: {args.exit_field})" if hasattr(args, 'exit_field') and args.exit_field else "")
          + (f" (entry-field: {args.entry_field})" if hasattr(args, 'entry_field') and args.entry_field else ""))


def cmd_add_composition(args):
    """Composition: the WHOLE 'contains' the PART (filled diamond at whole end).
    Arrow goes: part → whole (diamond at whole/target end via endArrow).

    When --source-field is given the diamond lands on a specific field row inside
    the WHOLE class instead of on the class border.  This is the Section-5a
    field-anchored pattern.  The field row gets portConstraint=eastwest so the
    diamond arrives from the left or right, and the PART exits from its right
    side (exitX=1) by default, producing a clean orthogonal route.

    When --exit-field is given, the exit point on the PART class is anchored to
    that field row. When --entry-field is given, the entry point on the WHOLE class
    is anchored to that field row.
    """
    tree, root = load_diagram(args.file)
    part = find_class(root, args.part)
    whole = find_class(root, args.whole)

    if args.source_field:
        # Target = specific field row inside the whole class (legacy mode)
        field_cell = find_field_row(root, args.whole, args.source_field)
        target_id  = field_cell.get("id")
        # Field-anchored style: part exits RIGHT side, diamond enters LEFT of field row
        style = (COMPOSITION_STYLE.rstrip(";")
                 + ";exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
                 + "entryX=0;entryY=0.5;entryDx=0;entryDy=0;")
    else:
        target_id = whole.get("id")
        style = COMPOSITION_STYLE

        # Apply field-level exit/entry constraints if provided (new mode)
        if hasattr(args, 'exit_field') and args.exit_field:
            exit_x, exit_y = _compute_field_exit_entry(root, part, whole, args.exit_field, is_exit=True)
            if exit_x is not None and exit_y is not None:
                style = (style.rstrip(";") +
                        f";exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;")

        if hasattr(args, 'entry_field') and args.entry_field:
            entry_x, entry_y = _compute_field_exit_entry(root, part, whole, args.entry_field, is_exit=False)
            if entry_x is not None and entry_y is not None:
                style = (style.rstrip(";") +
                        f";entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;")

    _add_edge(root, part.get("id"), target_id, style,
              label=args.label, from_mult=args.mult)
    save_diagram(tree, args.file)
    print(f"✓ Added composition: {args.whole} ◆── {args.part}"
          + (f" [field: {args.source_field}]" if args.source_field else "")
          + (f" [{args.mult}]" if args.mult else "")
          + (f" (exit-field: {args.exit_field})" if hasattr(args, 'exit_field') and args.exit_field else "")
          + (f" (entry-field: {args.entry_field})" if hasattr(args, 'entry_field') and args.entry_field else ""))


def cmd_add_aggregation(args):
    """Aggregation: the WHOLE 'aggregates' PARTs (hollow diamond at whole end).
    Arrow: whole (diamond) → part."""
    tree, root = load_diagram(args.file)
    whole = find_class(root, args.whole)
    part  = find_class(root, args.part)
    _add_edge(root, whole.get("id"), part.get("id"), AGGREGATION_STYLE,
              label=args.label, to_mult=args.mult)
    save_diagram(tree, args.file)
    print(f"✓ Added aggregation: {args.whole} ◇── {args.part}"
          + (f" [{args.mult}]" if args.mult else ""))


def cmd_add_inheritance(args):
    """Inheritance: subclass --▷ superclass (dashed with hollow block arrow)."""
    tree, root = load_diagram(args.file)
    sub   = find_class(root, args.subclass)
    super_ = find_class(root, args.superclass)
    _add_edge(root, sub.get("id"), super_.get("id"), INHERITANCE_STYLE)
    save_diagram(tree, args.file)
    print(f"✓ Added inheritance: {args.subclass} --▷ {args.superclass}")


def cmd_add_dependency(args):
    """Dependency/usage: dashed open arrow, optional «stereotype» label."""
    tree, root = load_diagram(args.file)
    src = find_class(root, args.from_class)
    tgt = find_class(root, args.to_class)
    _add_edge(root, src.get("id"), tgt.get("id"), DEPENDENCY_STYLE,
              stereotype=args.stereotype)
    save_diagram(tree, args.file)
    label_str = f" «{args.stereotype}»" if args.stereotype else ""
    print(f"✓ Added dependency: {args.from_class} -->{label_str} {args.to_class}")


def cmd_add_frame(args):
    """Add a UML frame/package that visually groups listed classes."""
    tree, root = load_diagram(args.file)

    class_names = [c.strip() for c in args.classes.split(",") if c.strip()] if args.classes else []

    # Compute bounding box around listed classes
    padding = 30
    if class_names:
        min_x, min_y, max_x, max_y = 9999, 9999, 0, 0
        for cname in class_names:
            try:
                cls = find_class(root, cname)
                g = cls.find("mxGeometry")
                cx = float(g.get("x", 0))
                cy = float(g.get("y", 0))
                cw = float(g.get("width", DEFAULT_WIDTH))
                ch = float(g.get("height", 100))
                min_x = min(min_x, cx)
                min_y = min(min_y, cy)
                max_x = max(max_x, cx + cw)
                max_y = max(max_y, cy + ch)
            except KeyError:
                pass
        x = min_x - padding
        y = min_y - padding - 20   # extra room for frame tab
        w = max_x - min_x + padding * 2
        h = max_y - min_y + padding * 2 + 20
    else:
        x, y, w, h = START_X, START_Y, 400, 300

    frame_id = new_id()
    frame = ET.SubElement(root, "mxCell")
    frame.set("id", frame_id)
    frame.set("value", args.name)
    frame.set("style", FRAME_STYLE)
    frame.set("vertex", "1")
    frame.set("parent", "1")
    fg = ET.SubElement(frame, "mxGeometry")
    fg.set("x", str(int(x)))
    fg.set("y", str(int(y)))
    fg.set("width", str(int(w)))
    fg.set("height", str(int(h)))
    fg.set("as", "geometry")

    save_diagram(tree, args.file)
    print(f"✓ Added frame: {args.name}"
          + (f" around [{args.classes}]" if class_names else ""))


def cmd_add_object(args):
    """Add a UML object instance box (InstanceName:ClassName format)."""
    tree, root = load_diagram(args.file)
    classes = get_all_classes(root)

    x, y = args.x or next_class_position(root)[0], args.y or next_class_position(root)[1]

    # Build HTML content for the object box
    title = f'<p style="margin:0px;margin-top:4px;text-align:center;' \
            f'text-decoration:underline;"><b>{args.name}</b></p>'
    fields_html = ""
    if args.fields:
        pairs = [f.strip() for f in args.fields.split(",") if f.strip()]
        lines = "<br>".join(pairs)
        fields_html = f'<hr size="1" style="border-style:solid;">' \
                      f'<p style="margin:0px;margin-left:8px;">{lines}</p>'
    value = title + fields_html

    obj_id = new_id()
    obj = ET.SubElement(root, "mxCell")
    obj.set("id", obj_id)
    obj.set("value", value)
    obj.set("style", OBJECT_STYLE)
    obj.set("vertex", "1")
    obj.set("parent", "1")
    og = ET.SubElement(obj, "mxGeometry")
    og.set("x", str(int(x)))
    og.set("y", str(int(y)))
    og.set("width", "160")
    og.set("height", str(40 + 20 * (len(args.fields.split(",")) if args.fields else 0)))
    og.set("as", "geometry")

    save_diagram(tree, args.file)
    print(f"✓ Added object instance: {args.name}")


def cmd_add_instance_of(args):
    """Add «instance of» dashed arrow from an object node to its class."""
    tree, root = load_diagram(args.file)

    # Find the object by name (searching all cells with value matching)
    obj_cell = None
    for cell in root.findall("mxCell"):
        val = cell.get("value", "")
        if args.object_name in val and "verticalAlign=top" in cell.get("style", ""):
            obj_cell = cell
            break
    if obj_cell is None:
        raise KeyError(f"Object '{args.object_name}' not found. Add it with add-object first.")

    cls = find_class(root, args.class_name)

    _add_edge(root, obj_cell.get("id"), cls.get("id"), DEPENDENCY_STYLE,
              stereotype="instance of")
    save_diagram(tree, args.file)
    print(f"✓ Added instance-of: {args.object_name} --«instance of»--> {args.class_name}")


def cmd_list_classes(args):
    _, root = load_diagram(args.file)
    classes = get_all_classes(root)
    if not classes:
        print("No classes found.")
        return
    print(f"Classes in {args.file}:")
    for name in sorted(classes.keys()):
        print(f"  • {name}")


def cmd_show_class(args):
    _, root = load_diagram(args.file)
    cls = find_class(root, args.class_name)
    class_id = cls.get("id")
    children = get_class_children(root, class_id)

    divider = get_divider(root, class_id)
    div_y = float(divider.find("mxGeometry").get("y", 0)) if divider else 9999

    fields = []
    methods = []
    for child in children:
        if "line;" in child.get("style", ""):
            continue
        geo = child.find("mxGeometry")
        if geo is None:
            continue
        child_y = float(geo.get("y", 0))
        val = child.get("value", "")
        if child_y < div_y:
            fields.append(val)
        else:
            methods.append(val)

    print(f"\nClass: {args.class_name}")
    print(f"  Fields ({len(fields)}):")
    for f in fields:
        print(f"    {f}")
    print(f"  Methods ({len(methods)}):")
    for m in methods:
        print(f"    {m}")

    # Show relationships
    rels = []
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        src = cell.get("source", "")
        tgt = cell.get("target", "")
        if src != class_id and tgt != class_id:
            continue
        style = cell.get("style", "")
        if "diamondThin" in style and "endFill=1" in style:
            rel_type = "composition"
        elif "diamondThin" in style and "startFill=0" in style:
            rel_type = "aggregation"
        elif "dashed=1" in style and "block" in style:
            rel_type = "inheritance"
        elif "dashed=1" in style:
            rel_type = "dependency"
        else:
            rel_type = "association"

        # Resolve names
        classes = get_all_classes(root)
        id_to_name = {v.get("id"): k for k, v in classes.items()}
        src_name = id_to_name.get(src, src[:8])
        tgt_name = id_to_name.get(tgt, tgt[:8])
        rels.append(f"    {rel_type}: {src_name} → {tgt_name}")

    if rels:
        print(f"  Relationships:")
        for r in rels:
            print(r)
    print()


def cmd_describe(args):
    """Print a full human-readable + AI-readable summary of the diagram."""
    _, root = load_diagram(args.file)
    classes = get_all_classes(root)

    print(f"\n{'='*60}")
    print(f"Diagram: {args.file}")
    print(f"{'='*60}")
    print(f"\nClasses ({len(classes)}):")

    for name, cls in sorted(classes.items()):
        class_id = cls.get("id")
        children = get_class_children(root, class_id)
        divider = get_divider(root, class_id)
        div_y = float(divider.find("mxGeometry").get("y", 0)) if divider else 9999

        fields, methods = [], []
        for child in children:
            if "line;" in child.get("style", ""):
                continue
            geo = child.find("mxGeometry")
            if geo is None:
                continue
            child_y = float(geo.get("y", 0))
            val = child.get("value", "")
            is_abstract = "fontStyle=2" in child.get("style", "")
            tag = " [abstract]" if is_abstract else ""
            if child_y < div_y:
                fields.append(f"{val}{tag}")
            else:
                methods.append(f"{val}{tag}")

        geo = cls.find("mxGeometry")
        pos = f"({geo.get('x')},{geo.get('y')})" if geo is not None else ""
        print(f"\n  ┌─ {name} {pos}")
        if fields:
            print(f"  │  Fields:")
            for f in fields:
                print(f"  │    {f}")
        if methods:
            print(f"  │  Methods:")
            for m in methods:
                print(f"  │    {m}")
        print(f"  └─")

    # Relationships
    id_to_name = {v.get("id"): k for k, v in classes.items()}
    print(f"\nRelationships:")
    found = False
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        src = cell.get("source", "")
        tgt = cell.get("target", "")
        if not src or not tgt:
            continue
        style = cell.get("style", "")

        if "diamondThin" in style and "endFill=1" in style:
            rel_type = "composition ◆"
        elif "diamondThin" in style and "startFill=0" in style:
            rel_type = "aggregation ◇"
        elif "dashed=1" in style and "block" in style:
            rel_type = "inheritance --▷"
        elif "dashed=1" in style:
            rel_type = "dependency - ->"
        else:
            rel_type = "association →"

        src_name = id_to_name.get(src, f"[{src[:8]}]")
        tgt_name = id_to_name.get(tgt, f"[{tgt[:8]}]")

        # Collect labels from children
        labels = []
        edge_id = cell.get("id")
        for lbl in root.findall("mxCell"):
            if lbl.get("parent") == edge_id:
                labels.append(lbl.get("value", "").strip())
        label_str = "  " + ", ".join(f'"{l}"' for l in labels if l) if labels else ""

        print(f"  {src_name} {rel_type} {tgt_name}{label_str}")
        found = True
    if not found:
        print("  (none)")

    # Frames
    frames = [c for c in root.findall("mxCell")
              if "shape=umlFrame" in c.get("style", "")]
    if frames:
        print(f"\nFrames/Packages:")
        for f in frames:
            print(f"  • {f.get('value', '')}")

    print()


# ─── Argument parsing ─────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="drawio_cli.py",
        description="Create and edit Draw.io UML class diagrams from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python drawio_cli.py new --file vehicles.drawio
  python drawio_cli.py add-class Car --file vehicles.drawio
  python drawio_cli.py add-field Car "+ driver: Person" --file vehicles.drawio
  python drawio_cli.py add-method Car "+ turn(degrees:Number): void" --file vehicles.drawio
  python drawio_cli.py add-class Wheel --file vehicles.drawio
  python drawio_cli.py add-composition Car Wheel --mult 4 --label "has" --file vehicles.drawio
  python drawio_cli.py add-class Vehicle --file vehicles.drawio
  python drawio_cli.py add-inheritance Car Vehicle --file vehicles.drawio
  python drawio_cli.py add-frame "Vehicles" --classes "Vehicle,Car,Wheel" --file vehicles.drawio
  python drawio_cli.py describe --file vehicles.drawio
""")

    parser.add_argument("--file", "-f", required=True, metavar="FILE",
                        help="Path to the .drawio file to work with")

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # new
    p = sub.add_parser("new", help="Create a new empty .drawio diagram")

    # add-class
    p = sub.add_parser("add-class", help="Add a class to the diagram")
    p.add_argument("name", help="Class name (e.g. Car)")
    p.add_argument("--x", type=int, help="X position (auto if omitted)")
    p.add_argument("--y", type=int, help="Y position (auto if omitted)")
    p.add_argument("--width", type=int, help=f"Width (default {DEFAULT_WIDTH})")
    p.add_argument("--stereotype", metavar="NAME",
                   help="UML stereotype shown above the class name, e.g. scan")

    # add-field
    p = sub.add_parser("add-field",
                       help='Add a field to a class (e.g. "+ speed: Number")')
    p.add_argument("class_name", metavar="CLASS",
                   help="Class to add the field to")
    p.add_argument("text", help='Field text, e.g. "+ speed: Number"')
    p.add_argument("--abstract", action="store_true",
                   help="Mark as abstract (italic)")

    # add-method
    p = sub.add_parser("add-method",
                       help='Add a method to a class (e.g. "+ drive(): void")')
    p.add_argument("class_name", metavar="CLASS",
                   help="Class to add the method to")
    p.add_argument("text", help='Method text, e.g. "+ drive(speed:Number): void"')
    p.add_argument("--abstract", action="store_true",
                   help="Mark as abstract (italic)")

    # add-association
    p = sub.add_parser("add-association",
                       help="Add a directed association arrow")
    p.add_argument("from_class", metavar="FROM", help="Source class")
    p.add_argument("to_class",   metavar="TO",   help="Target class")
    p.add_argument("--label",     help='Label in the middle, e.g. "drives a"')
    p.add_argument("--from-mult", metavar="MULT",
                   help="Multiplicity at source end, e.g. 1")
    p.add_argument("--to-mult",   metavar="MULT",
                   help="Multiplicity at target end, e.g. 0..3")
    p.add_argument("--exit-field", metavar="FIELD",
                   help="Field row text in source class to anchor exit point")
    p.add_argument("--entry-field", metavar="FIELD",
                   help="Field row text in target class to anchor entry point")

    # add-composition
    p = sub.add_parser("add-composition",
                       help="Add composition (filled diamond): WHOLE ◆── PART")
    p.add_argument("whole", metavar="WHOLE", help="The containing class")
    p.add_argument("part",  metavar="PART",  help="The contained class")
    p.add_argument("--mult",  metavar="MULT", help='Multiplicity, e.g. "4"')
    p.add_argument("--label", help="Optional relationship label")
    p.add_argument("--source-field", metavar="FIELD",
                   help="Field row text in WHOLE to anchor the diamond to "
                        "(Section 5a field-anchored pattern, legacy mode)")
    p.add_argument("--exit-field", metavar="FIELD",
                   help="Field row text in PART to anchor exit point")
    p.add_argument("--entry-field", metavar="FIELD",
                   help="Field row text in WHOLE to anchor entry point (diamond destination)")

    # add-aggregation
    p = sub.add_parser("add-aggregation",
                       help="Add aggregation (hollow diamond): WHOLE ◇── PART")
    p.add_argument("whole", metavar="WHOLE", help="The aggregating class")
    p.add_argument("part",  metavar="PART",  help="The aggregated class")
    p.add_argument("--mult",  metavar="MULT", help='Multiplicity, e.g. "1..*"')
    p.add_argument("--label", help="Optional relationship label")

    # add-inheritance
    p = sub.add_parser("add-inheritance",
                       help="Add inheritance arrow: SUBCLASS --▷ SUPERCLASS")
    p.add_argument("subclass",   metavar="SUBCLASS",   help="The child class")
    p.add_argument("superclass", metavar="SUPERCLASS", help="The parent class")

    # add-dependency
    p = sub.add_parser("add-dependency",
                       help="Add a dependency (dashed arrow), optionally with «stereotype»")
    p.add_argument("from_class", metavar="FROM", help="Source class")
    p.add_argument("to_class",   metavar="TO",   help="Target class")
    p.add_argument("--stereotype", metavar="LABEL",
                   help='Stereotype text, e.g. "created by" or "uses"')

    # add-frame
    p = sub.add_parser("add-frame",
                       help="Add a UML package/frame around a set of classes")
    p.add_argument("name", help="Package/frame name")
    p.add_argument("--classes", metavar="LIST",
                   help='Comma-separated class names to enclose, e.g. "Car,Wheel,Person"')

    # add-object
    p = sub.add_parser("add-object",
                       help='Add a UML object instance box, e.g. "Dash8:Plane"')
    p.add_argument("name", help='Object name in "InstanceName:ClassName" format')
    p.add_argument("--fields", metavar="PAIRS",
                   help='Comma-separated field=value pairs, e.g. "pilot=Bob,speed=200"')
    p.add_argument("--x", type=int)
    p.add_argument("--y", type=int)

    # add-instance-of
    p = sub.add_parser("add-instance-of",
                       help='Add «instance of» arrow from object box to its class')
    p.add_argument("object_name", metavar="OBJECT",
                   help='Object box name (e.g. "Dash8:Plane")')
    p.add_argument("class_name",  metavar="CLASS",
                   help="The class being instantiated")

    # list-classes
    sub.add_parser("list-classes", help="List all classes in the diagram")

    # show-class
    p = sub.add_parser("show-class", help="Show fields, methods, and relationships of a class")
    p.add_argument("class_name", metavar="CLASS")

    # describe
    sub.add_parser("describe", help="Print a full readable summary of the diagram")

    # relayout — the key post-build step
    p = sub.add_parser("relayout",
        help="Hierarchical re-layout: parents above children, siblings grouped. "
             "Run AFTER all add-field/add-method calls.")
    p.add_argument("--hgap", type=int, default=GRID_COL_SPACING,
                   help=f"Horizontal gap between classes in px (default {GRID_COL_SPACING})")
    p.add_argument("--vgap", type=int, default=GRID_ROW_SPACING,
                   help=f"Vertical gap between rows in px (default {GRID_ROW_SPACING})")

    # verify — QA pass
    p = sub.add_parser("verify",
        help="Audit diagram for overlaps, bad edge styles, wrong parent/child direction.")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Show XML-level detail and fix suggestions for each issue")

    # fix-edge-styles
    sub.add_parser("fix-edge-styles",
        help="Fix V3/V4: add orthogonal routing to structural edges, "
             "remove waypoints, strip edgeStyle from inheritance edges.")

    # fix-shared-endpoints
    sub.add_parser("fix-shared-endpoints",
        help="Fix V5: distribute entryX/entryY (and exitX/exitY) when 2+ edges "
             "converge on the same class without explicit port constraints.")

    # fix-arrow-overlaps
    sub.add_parser("fix-arrow-overlaps",
        help="Fix V6: add a bypass waypoint to straight-line edges that pass "
             "through an unrelated class — picks the shortest of 4 candidates "
             "(above / below / left / right of the blocking class).")

    return parser


COMMAND_MAP = {
    "new":              cmd_new,
    "add-class":        cmd_add_class,
    "add-field":        cmd_add_field,
    "add-method":       cmd_add_method,
    "add-association":  cmd_add_association,
    "add-composition":  cmd_add_composition,
    "add-aggregation":  cmd_add_aggregation,
    "add-inheritance":  cmd_add_inheritance,
    "add-dependency":   cmd_add_dependency,
    "add-frame":        cmd_add_frame,
    "add-object":       cmd_add_object,
    "add-instance-of":  cmd_add_instance_of,
    "list-classes":     cmd_list_classes,
    "show-class":       cmd_show_class,
    "describe":         cmd_describe,
    "relayout":         cmd_relayout,
    "verify":                cmd_verify,
    "fix-edge-styles":       cmd_fix_edge_styles,
    "fix-shared-endpoints":  cmd_fix_shared_endpoints,
    "fix-arrow-overlaps":    cmd_fix_arrow_overlaps,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command not in COMMAND_MAP:
        parser.print_help()
        sys.exit(1)

    try:
        COMMAND_MAP[args.command](args)
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
