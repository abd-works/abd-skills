#!/usr/bin/env python3
"""
validate_diagram.py — Comprehensive diagram validator.

Detects:
  V1  EDGE-CLASS OVERLAP   : an edge segment passes through a class body it doesn't connect to
  V2  EDGE-FRAME OVERLAP   : an edge segment passes through a module frame it isn't inside
  V3  EDGE-EDGE CROSSING   : two edges cross each other (segment–segment intersection)
  V4  EDGE-EDGE SHARING    : two edges share a ≥10-pixel segment (run on top of each other)
  V5  SHARED CONNECTION PT : two edges exit/enter the same pixel on a class
  V6  WRONG EXIT SIDE      : an edge should exit left/right but exits top/bottom (or vice versa)
  V7  MISSING BACKING FIELD: a composition/association arrow has no matching field in source class
  V8  DIRECT ROUTE EXISTS  : edge uses waypoints but a straight line would be shorter and clear
  V9  CLASS-CLASS OVERLAP  : two class bounding boxes overlap

Usage:
    python3 validate_diagram.py --file path/to/diagram.drawio [--verbose]
"""

import argparse
import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path
from typing import List, Optional, Tuple


# ── Data types ─────────────────────────────────────────────────────────────────

@dataclass
class Rect:
    x: float; y: float; w: float; h: float
    @property
    def x2(self): return self.x + self.w
    @property
    def y2(self): return self.y + self.h
    def contains_pt(self, px, py, margin=0):
        return (self.x - margin < px < self.x2 + margin and
                self.y - margin < py < self.y2 + margin)
    def overlaps(self, other, margin=0):
        return (self.x < other.x2 + margin and self.x2 > other.x - margin and
                self.y < other.y2 + margin and self.y2 > other.y - margin)


@dataclass
class ClassNode:
    id: str; name: str; rect: Rect
    fields: List[str] = field(default_factory=list)  # raw text of each field row
    field_ys: List[float] = field(default_factory=list)  # y-center of each field row in absolute coords


@dataclass
class FrameNode:
    name: str; rect: Rect; member_ids: List[str] = field(default_factory=list)


@dataclass
class Edge:
    id: str; src_id: str; tgt_id: str; label: str
    style: str
    path: List[Tuple[float, float]]   # full resolved pixel path [src_pt, *waypoints, tgt_pt]
    exit_x: Optional[float]; exit_y: Optional[float]
    entry_x: Optional[float]; entry_y: Optional[float]
    edge_type: str = ''   # 'composition', 'association', 'dependency', 'unknown'


# ── Geometry helpers ───────────────────────────────────────────────────────────

def seg_intersect(p1, p2, p3, p4):
    """Return True if segment p1–p2 strictly intersects segment p3–p4."""
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    def on_seg(p, q, r):
        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    if d1 == 0 and on_seg(p3, p1, p4): return True
    if d2 == 0 and on_seg(p3, p2, p4): return True
    if d3 == 0 and on_seg(p1, p3, p2): return True
    if d4 == 0 and on_seg(p1, p4, p2): return True

    return False


def seg_enters_rect(p1, p2, rect: Rect, margin=3) -> bool:
    """
    Return True if segment p1→p2 passes through the INTERIOR of rect.
    We expand the rect by -margin on all sides (strict interior check).
    We also skip the case where BOTH endpoints are on the rect boundary
    (edge legitimately terminates at the class).
    """
    r = Rect(rect.x + margin, rect.y + margin,
             rect.w - 2*margin, rect.h - 2*margin)
    if r.w <= 0 or r.h <= 0:
        return False

    # Check intersection with each of the 4 rect edges
    corners = [(r.x, r.y), (r.x2, r.y), (r.x2, r.y2), (r.x, r.y2)]
    sides = [(corners[i], corners[(i+1) % 4]) for i in range(4)]

    for (a, b) in sides:
        if seg_intersect(p1, p2, a, b):
            return True

    # Check if either endpoint is strictly inside
    if r.contains_pt(p1[0], p1[1]): return True
    if r.contains_pt(p2[0], p2[1]): return True

    return False


def seg_length(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def pt_on_seg(pt, p1, p2, tol=5):
    """Return True if point pt lies on segment p1–p2 within tolerance."""
    d_seg = seg_length(p1, p2)
    if d_seg < 1: return False
    d1 = seg_length(pt, p1)
    d2 = seg_length(pt, p2)
    return abs(d1 + d2 - d_seg) < tol


def seg_overlap_length(p1, p2, q1, q2) -> float:
    """
    Return the length of overlap between two co-linear segments (0 if not co-linear
    or not parallel within tolerance).
    """
    dx1, dy1 = p2[0]-p1[0], p2[1]-p1[1]
    dx2, dy2 = q2[0]-q1[0], q2[1]-q1[1]
    L1 = seg_length(p1, p2)
    L2 = seg_length(q1, q2)
    if L1 < 1 or L2 < 1: return 0

    # Check parallel
    cross = dx1 * dy2 - dy1 * dx2
    if abs(cross) > (L1 * L2) * 0.05:  # more than 5° angle → not parallel
        return 0

    # Check co-linear: p1 should lie on line through q1,q2
    cross2 = (q2[0]-q1[0])*(p1[1]-q1[1]) - (q2[1]-q1[1])*(p1[0]-q1[0])
    dist_to_line = abs(cross2) / L2 if L2 > 0 else 999
    if dist_to_line > 8:  # more than 8px off the line
        return 0

    # Project onto the direction of the first segment
    ux = dx1 / L1
    uy = dy1 / L1
    t1 = 0
    t2 = L1
    s1 = (q1[0]-p1[0])*ux + (q1[1]-p1[1])*uy
    s2 = (q2[0]-p1[0])*ux + (q2[1]-p1[1])*uy
    s_min = min(s1, s2)
    s_max = max(s1, s2)
    overlap = max(0, min(t2, s_max) - max(t1, s_min))
    return overlap


# ── XML parsing ────────────────────────────────────────────────────────────────

def strip_html(s):
    """Strip HTML tags, unescape HTML entities."""
    s = re.sub(r'<[^>]+>', ' ', s)
    s = unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def extract_class_name(raw):
    """Get the plain class name from a possibly HTML-decorated cell value."""
    clean = strip_html(raw)
    # Remove stereotypes like <<scan>>
    clean = re.sub(r'<<[^>]*>>', ' ', clean)
    clean = re.sub(r'[«»].*?[«»]', ' ', clean)
    tokens = [t for t in clean.split() if t]
    return tokens[-1] if tokens else ''


def _style_val(style, key, default=None):
    for part in style.split(';'):
        if part.startswith(f'{key}='):
            try: return float(part.split('=', 1)[1])
            except: return default
    return default


def parse_diagram(path):
    """Parse the draw.io XML and return (classes, frames, edges)."""
    tree = ET.parse(path)
    root = tree.getroot().find('.//root')
    all_cells = {c.get('id',''): c for c in root.findall('mxCell')}

    # ── Classes ──────────────────────────────────────────────────────────────
    classes: dict[str, ClassNode] = {}
    for c in root.findall('mxCell'):
        style = c.get('style','')
        if 'swimlane' not in style or 'childLayout=stackLayout' not in style:
            continue
        g = c.find('mxGeometry')
        if g is None: continue
        cid = c.get('id','')
        name = extract_class_name(c.get('value',''))
        rect = Rect(float(g.get('x',0)), float(g.get('y',0)),
                    float(g.get('width',200)), float(g.get('height',60)))
        node = ClassNode(id=cid, name=name, rect=rect)

        # Collect fields (direct children with text style)
        start_size = _style_val(style, 'startSize', 26) or 26
        y_cursor = rect.y + start_size + 4  # approximate top of first field row
        for ch in root.findall('mxCell'):
            if ch.get('parent','') != cid:
                continue
            ch_style = ch.get('style','')
            if 'text' not in ch_style and 'line' not in ch_style:
                continue
            val = strip_html(ch.get('value',''))
            if val and not ch_style.startswith('line'):
                cg = ch.find('mxGeometry')
                ch_h = float(cg.get('height', 26)) if cg is not None else 26
                node.fields.append(val)
                node.field_ys.append(y_cursor + ch_h / 2)
                y_cursor += ch_h
        classes[cid] = node

    # ── Frames ───────────────────────────────────────────────────────────────
    frames: list[FrameNode] = []
    for c in root.findall('mxCell'):
        if 'umlFrame' not in c.get('style',''):
            continue
        g = c.find('mxGeometry')
        if g is None: continue
        rect = Rect(float(g.get('x',0)), float(g.get('y',0)),
                    float(g.get('width',0)), float(g.get('height',0)))
        name = c.get('value','')
        # Find which classes are inside this frame (by overlap)
        members = [cid for cid, cn in classes.items()
                   if rect.contains_pt(cn.rect.x + cn.rect.w/2, cn.rect.y + cn.rect.h/2)]
        frames.append(FrameNode(name=name, rect=rect, member_ids=members))

    # ── Edges ─────────────────────────────────────────────────────────────────
    edges: list[Edge] = []
    for c in root.findall('mxCell'):
        if c.get('edge','') != '1':
            continue
        g = c.find('mxGeometry')
        if g is None: continue

        src_id = c.get('source','')
        tgt_id = c.get('target','')
        style  = c.get('style','')
        label  = strip_html(c.get('value',''))

        src = classes.get(src_id)
        tgt = classes.get(tgt_id)

        # Exit/entry fractions
        ex = _style_val(style, 'exitX', 0.5)
        ey = _style_val(style, 'exitY', 0.5)
        nx = _style_val(style, 'entryX', 0.5)
        ny = _style_val(style, 'entryY', 0.5)

        # Compute pixel exit/entry
        def ep(cls_node, fx, fy):
            if cls_node is None: return None
            return (cls_node.rect.x + fx * cls_node.rect.w,
                    cls_node.rect.y + fy * cls_node.rect.h)

        src_pt = ep(src, ex, ey)
        tgt_pt = ep(tgt, nx, ny)

        # Waypoints
        wpts = []
        arr = g.find('Array')
        if arr is not None:
            for pt in arr.findall('mxPoint'):
                wpts.append((float(pt.get('x',0)), float(pt.get('y',0))))

        # Full path
        path = []
        if src_pt: path.append(src_pt)
        path.extend(wpts)
        if tgt_pt: path.append(tgt_pt)

        # Edge type
        etype = 'unknown'
        if 'endArrow=ERmany' in style or 'endArrow=ERzeroToMany' in style:
            etype = 'composition'
        elif 'endFill=1' in style and 'diamond' in style.lower():
            etype = 'composition'
        elif 'dashed=1' in style or 'dashed=2' in style:
            etype = 'dependency'
        elif 'endArrow=open' in style or 'endArrow=block' in style:
            etype = 'association'
        # Draw.io defaults
        if etype == 'unknown':
            if 'diamond' in style.lower(): etype = 'composition'
            elif 'dashed' in style: etype = 'dependency'

        edges.append(Edge(
            id=c.get('id','')[:8],
            src_id=src_id, tgt_id=tgt_id, label=label,
            style=style, path=path,
            exit_x=ex, exit_y=ey, entry_x=nx, entry_y=ny,
            edge_type=etype,
        ))

    return classes, frames, edges


# ── Validator ─────────────────────────────────────────────────────────────────

class Issue:
    def __init__(self, code, severity, msg, detail=''):
        self.code = code
        self.severity = severity  # 'ERROR' or 'WARN'
        self.msg = msg
        self.detail = detail
    def __str__(self):
        s = f"[{self.severity}][{self.code}] {self.msg}"
        if self.detail: s += f"\n    → {self.detail}"
        return s


def edge_label(e, classes):
    src = classes.get(e.src_id)
    tgt = classes.get(e.tgt_id)
    sn = src.name if src else e.src_id[:8]
    tn = tgt.name if tgt else e.tgt_id[:8]
    lbl = f"[{e.label[:20]}]" if e.label else ''
    return f"{sn}→{tn}{lbl}"


def validate(diagram_path, verbose=False):
    classes, frames, edges = parse_diagram(diagram_path)
    issues = []

    # ──────────────────────────────────────────────────────────────────────────
    # V9: Class-class overlap
    # ──────────────────────────────────────────────────────────────────────────
    clist = list(classes.values())
    for i in range(len(clist)):
        for j in range(i+1, len(clist)):
            a, b = clist[i], clist[j]
            if a.rect.overlaps(b.rect, margin=-2):
                issues.append(Issue('V9','ERROR',
                    f"CLASS OVERLAP: '{a.name}' and '{b.name}' bounding boxes overlap",
                    f"{a.name}: ({a.rect.x},{a.rect.y}) {a.rect.w}x{a.rect.h} | "
                    f"{b.name}: ({b.rect.x},{b.rect.y}) {b.rect.w}x{b.rect.h}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V1: Edge segment passes through a class it does NOT connect to
    # ──────────────────────────────────────────────────────────────────────────
    for e in edges:
        if len(e.path) < 2: continue
        segs = [(e.path[k], e.path[k+1]) for k in range(len(e.path)-1)]
        connected_ids = {e.src_id, e.tgt_id}

        for cls in classes.values():
            if cls.id in connected_ids: continue
            for si, (p1, p2) in enumerate(segs):
                if seg_enters_rect(p1, p2, cls.rect, margin=3):
                    issues.append(Issue('V1','ERROR',
                        f"EDGE-CLASS OVERLAP: {edge_label(e, classes)} segment {si} "
                        f"passes through '{cls.name}'",
                        f"seg: {tuple(round(v) for v in p1)} → {tuple(round(v) for v in p2)} | "
                        f"class box: ({cls.rect.x},{cls.rect.y}) {cls.rect.w}x{cls.rect.h}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V2: Edge segment passes through a frame whose members it doesn't belong to
    # ──────────────────────────────────────────────────────────────────────────
    for e in edges:
        if len(e.path) < 2: continue
        segs = [(e.path[k], e.path[k+1]) for k in range(len(e.path)-1)]
        for fr in frames:
            # If BOTH endpoints are inside this frame, the edge is intra-frame → OK
            src_cls = classes.get(e.src_id)
            tgt_cls = classes.get(e.tgt_id)
            src_in = src_cls and fr.rect.contains_pt(src_cls.rect.x + src_cls.rect.w/2,
                                                       src_cls.rect.y + src_cls.rect.h/2)
            tgt_in = tgt_cls and fr.rect.contains_pt(tgt_cls.rect.x + tgt_cls.rect.w/2,
                                                       tgt_cls.rect.y + tgt_cls.rect.h/2)
            if src_in and tgt_in:
                continue  # Both inside → fine

            for si, (p1, p2) in enumerate(segs):
                # Allow tiny margin at the frame boundary (connection edges cross the border)
                if seg_enters_rect(p1, p2, fr.rect, margin=8):
                    issues.append(Issue('V2','WARN',
                        f"EDGE-FRAME OVERLAP: {edge_label(e, classes)} segment {si} "
                        f"passes through frame '{fr.name}'",
                        f"seg: {tuple(round(v) for v in p1)} → {tuple(round(v) for v in p2)} | "
                        f"frame: ({fr.rect.x},{fr.rect.y}) {fr.rect.w}x{fr.rect.h}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V3: Edge-edge crossing (segment–segment intersection)
    # ──────────────────────────────────────────────────────────────────────────
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            ea, eb = edges[i], edges[j]
            if len(ea.path) < 2 or len(eb.path) < 2: continue
            segs_a = [(ea.path[k], ea.path[k+1]) for k in range(len(ea.path)-1)]
            segs_b = [(eb.path[k], eb.path[k+1]) for k in range(len(eb.path)-1)]
            for sia, (a1, a2) in enumerate(segs_a):
                for sib, (b1, b2) in enumerate(segs_b):
                    # Skip if they share a class endpoint
                    shared = ({ea.src_id, ea.tgt_id} & {eb.src_id, eb.tgt_id})
                    if shared: continue
                    if seg_intersect(a1, a2, b1, b2):
                        issues.append(Issue('V3','ERROR',
                            f"EDGE-EDGE CROSSING: {edge_label(ea, classes)} seg{sia} "
                            f"× {edge_label(eb, classes)} seg{sib}",
                            f"{tuple(round(v) for v in a1)}→{tuple(round(v) for v in a2)} "
                            f"× {tuple(round(v) for v in b1)}→{tuple(round(v) for v in b2)}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V4: Edge-edge segment overlap (run on top of each other)
    # ──────────────────────────────────────────────────────────────────────────
    MIN_OVERLAP = 20  # pixels
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            ea, eb = edges[i], edges[j]
            if len(ea.path) < 2 or len(eb.path) < 2: continue
            segs_a = [(ea.path[k], ea.path[k+1]) for k in range(len(ea.path)-1)]
            segs_b = [(eb.path[k], eb.path[k+1]) for k in range(len(eb.path)-1)]
            for a1, a2 in segs_a:
                for b1, b2 in segs_b:
                    ov = seg_overlap_length(a1, a2, b1, b2)
                    if ov >= MIN_OVERLAP:
                        issues.append(Issue('V4','ERROR',
                            f"EDGE-EDGE OVERLAP: {edge_label(ea, classes)} and "
                            f"{edge_label(eb, classes)} share ~{ov:.0f}px of route",
                            f"seg: {tuple(round(v) for v in a1)}→{tuple(round(v) for v in a2)} "
                            f"≡ {tuple(round(v) for v in b1)}→{tuple(round(v) for v in b2)}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V5: Multiple edges share the same exit or entry point on a class
    # ──────────────────────────────────────────────────────────────────────────
    from collections import defaultdict
    exit_pts: dict[str, list] = defaultdict(list)
    entry_pts: dict[str, list] = defaultdict(list)
    for e in edges:
        if len(e.path) >= 1:
            src = classes.get(e.src_id)
            tgt = classes.get(e.tgt_id)
            if src and e.path:
                key = (e.src_id, round(e.path[0][0]/5)*5, round(e.path[0][1]/5)*5)
                exit_pts[key].append(edge_label(e, classes))
            if tgt and e.path:
                key = (e.tgt_id, round(e.path[-1][0]/5)*5, round(e.path[-1][1]/5)*5)
                entry_pts[key].append(edge_label(e, classes))

    for key, edge_names in exit_pts.items():
        if len(edge_names) > 1:
            cls = classes.get(key[0])
            cn = cls.name if cls else key[0][:8]
            issues.append(Issue('V5','ERROR',
                f"SHARED EXIT POINT on '{cn}' at ~({key[1]},{key[2]}): "
                f"{len(edge_names)} edges exit the same pixel",
                '; '.join(edge_names)))

    for key, edge_names in entry_pts.items():
        if len(edge_names) > 1:
            cls = classes.get(key[0])
            cn = cls.name if cls else key[0][:8]
            issues.append(Issue('V5','WARN',
                f"SHARED ENTRY POINT on '{cn}' at ~({key[1]},{key[2]}): "
                f"{len(edge_names)} edges enter the same pixel",
                '; '.join(edge_names)))

    # ──────────────────────────────────────────────────────────────────────────
    # V6: Wrong exit side (edge goes down when target is to the left, etc.)
    # ──────────────────────────────────────────────────────────────────────────
    for e in edges:
        src = classes.get(e.src_id)
        tgt = classes.get(e.tgt_id)
        if not src or not tgt: continue

        # Compute center-to-center direction
        src_cx = src.rect.x + src.rect.w / 2
        src_cy = src.rect.y + src.rect.h / 2
        tgt_cx = tgt.rect.x + tgt.rect.w / 2
        tgt_cy = tgt.rect.y + tgt.rect.h / 2
        dx = tgt_cx - src_cx
        dy = tgt_cy - src_cy

        # Expected side: if |dx| > |dy| → left/right exit; else top/bottom
        expected_horizontal = abs(dx) > abs(dy) * 0.7

        # Actual exit from source: exitY
        if e.exit_y is not None:
            actual_horizontal = (e.exit_y not in (0.0, 1.0))  # not top/bottom → left/right
            if e.exit_x is not None:
                actual_horizontal = (e.exit_x in (0.0, 1.0))  # 0=left, 1=right

        # We only flag if the source exit side is very wrong and causes an S-bend
        if e.exit_y is not None and e.exit_x is not None:
            # Exit from top (exitY=0) but target is below
            if e.exit_y == 0.0 and dy > 30 and len(e.path) >= 2:
                issues.append(Issue('V6','WARN',
                    f"WRONG EXIT SIDE: {edge_label(e, classes)} exits TOP but target is BELOW",
                    f"exit=({e.exit_x},{e.exit_y}) dy={dy:.0f}px"))
            # Exit from right side but target is to the left and far down
            if e.exit_x == 1.0 and dx < -100 and dy > 100 and len(e.path) >= 2:
                issues.append(Issue('V6','WARN',
                    f"WRONG EXIT SIDE: {edge_label(e, classes)} exits RIGHT but target is far LEFT+DOWN",
                    f"exit=({e.exit_x},{e.exit_y}) dx={dx:.0f} dy={dy:.0f}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V7: Association/composition has no matching field in source class
    # ──────────────────────────────────────────────────────────────────────────
    for e in edges:
        if e.edge_type == 'dependency': continue  # deps don't need backing fields
        src = classes.get(e.src_id)
        tgt = classes.get(e.tgt_id)
        if not src or not tgt: continue
        # The field in the SOURCE class should reference the TARGET class name
        tgt_name = tgt.name.lower()
        found = any(tgt_name in f.lower() for f in src.fields)
        if not found:
            issues.append(Issue('V7','WARN',
                f"MISSING BACKING FIELD: {edge_label(e, classes)} — "
                f"no field in '{src.name}' references '{tgt.name}'",
                f"Fields in {src.name}: {src.fields}"))

    # ──────────────────────────────────────────────────────────────────────────
    # V8: Direct route is clear but edge uses detour waypoints
    # ──────────────────────────────────────────────────────────────────────────
    for e in edges:
        if len(e.path) < 3: continue  # no waypoints
        src = classes.get(e.src_id)
        tgt = classes.get(e.tgt_id)
        if not src or not tgt: continue

        # Would the direct segment (path[0]→path[-1]) be clear of all other classes?
        direct_p1, direct_p2 = e.path[0], e.path[-1]
        direct_len = seg_length(direct_p1, direct_p2)
        actual_len = sum(seg_length(e.path[k], e.path[k+1]) for k in range(len(e.path)-1))

        if actual_len < direct_len * 1.3:
            continue  # detour is less than 30% longer → not flagging

        connected_ids = {e.src_id, e.tgt_id}
        direct_blocked = any(
            seg_enters_rect(direct_p1, direct_p2, cls.rect, margin=5)
            for cls in classes.values() if cls.id not in connected_ids
        )
        if not direct_blocked:
            issues.append(Issue('V8','WARN',
                f"NEEDLESS DETOUR: {edge_label(e, classes)} has {len(e.path)-2} waypoint(s) "
                f"but direct route is {(actual_len/direct_len - 1)*100:.0f}% longer and clear",
                f"direct={direct_len:.0f}px actual={actual_len:.0f}px"))

    return issues, classes, frames, edges


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description='Validate a draw.io UML class diagram')
    ap.add_argument('--file', '-f', required=True, help='Path to .drawio file')
    ap.add_argument('--verbose', '-v', action='store_true')
    args = ap.parse_args()

    path = args.file
    print(f"\n{'='*68}")
    print(f"VALIDATE: {Path(path).name}")
    print(f"{'='*68}\n")

    issues, classes, frames, edges = validate(path, verbose=args.verbose)

    if not issues:
        print("✓ No issues found — diagram is clean.\n")
        return

    # Group by code
    from collections import defaultdict
    by_code = defaultdict(list)
    for iss in issues:
        by_code[iss.code].append(iss)

    counts = {'ERROR': 0, 'WARN': 0}
    for iss in issues:
        counts[iss.severity] += 1

    code_order = ['V9','V1','V2','V3','V4','V5','V6','V7','V8']
    for code in code_order:
        group = by_code.get(code, [])
        if not group: continue
        for iss in group:
            print(iss)
        print()

    print(f"{'─'*68}")
    print(f"SUMMARY: {counts['ERROR']} error(s), {counts['WARN']} warning(s)  "
          f"[{len(classes)} classes, {len(edges)} edges]\n")


if __name__ == '__main__':
    main()
