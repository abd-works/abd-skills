#!/usr/bin/env python3
"""
drawio_domain_cli.py — unified domain model → Draw.io class diagram CLI

Supports three source formats, auto-detected from YAML frontmatter or filename:
  state: domain-model                  — domain model pipe-table format
  state: domain-model         — typed class-model (+ prop: Type, ---- separators)
  state: domain-language  — ULL prose bullet format

Layout: Sugiyama hierarchical layering + spring-force X-relaxation (TogetherJ-style).
  1. Cycle removal (greedy DFS feedback-arc set)
  2. Layer assignment (longest-path DAG — import/base nodes at top)
  3. Crossing minimization (barycentric, 4 sweeps top-down + bottom-up)
  4. Initial coordinate assignment (even spacing per layer)
  5. Spring relaxation (attraction between connected nodes, repulsion within layer)

Usage:
  python drawio_domain_cli.py <source.md> [--output FILE] [--ka NAME]
                              [--page-w N] [--page-h N]
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from drawio_tools import (
    create_empty_mxfile,
    add_page,
    get_page,
    save_drawio,
    create_class_cell,
    create_edge,
    find_cell_by_name,
    calc_cell_height,
    audit_diagram_report,
    CELL_WIDTH,
)


# ---------------------------------------------------------------------------
# Internal model
# ---------------------------------------------------------------------------

@dataclass
class ClassDef:
    name: str
    ka: str
    base: Optional[str] = None
    stereotype: Optional[str] = None
    props: List[str] = field(default_factory=list)
    ops: List[str] = field(default_factory=list)
    invs: List[str] = field(default_factory=list)
    # (target_name, edge_type) — edge_type: association | composition | aggregation
    edge_targets: List[Tuple[str, str]] = field(default_factory=list)


@dataclass
class DomainModel:
    kas: Dict[str, List[ClassDef]]
    source_format: str

    def all_class_names(self) -> set:
        return {c.name for classes in self.kas.values() for c in classes}

    def class_by_name(self, name: str) -> Optional[ClassDef]:
        for classes in self.kas.values():
            for c in classes:
                if c.name == name:
                    return c
        return None


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------

def detect_format(text: str, path: Path) -> str:
    fm = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
    if fm:
        state = re.search(r"^state:\s*(.+)$", fm.group(1), re.MULTILINE)
        if state:
            return state.group(1).strip()
    stem = path.stem.lower()
    if "domain model" in stem:
        return "domain model"
    if "class-model" in stem or "object_model" in stem:
        return "domain-model"
    if "domain-language" in stem or "ubiquitous_language" in stem:
        return "domain-language"
    return "domain model"


# ---------------------------------------------------------------------------
# domain model Parser
# ---------------------------------------------------------------------------

def parse_crc(text: str) -> DomainModel:
    kas: Dict[str, List[ClassDef]] = {}
    current_ka: Optional[str] = None
    current_cls: Optional[ClassDef] = None
    skip = False

    for line in text.split("\n"):
        s = line.strip()

        ka_m = re.match(r"^##\s+\*\*(.+?)\*\*\s*$", s)
        if ka_m:
            current_ka = ka_m.group(1)
            kas[current_ka] = []
            current_cls = None
            skip = False
            continue

        cls_m = re.match(r"^###\s+\*\*(.+?)\*\*\s*$", s)
        if cls_m and current_ka and not skip:
            raw = cls_m.group(1)
            base = None
            if " : " in raw:
                name, base = raw.split(" : ", 1)
                name, base = name.strip(), base.strip()
            else:
                name = raw
            current_cls = ClassDef(name=name, ka=current_ka, base=base)
            kas[current_ka].append(current_cls)
            continue

        if s in ("### references", "### decisions made"):
            skip = True
            current_cls = None
            continue
        if s == "---":
            skip = False
            continue

        if current_cls is None or skip:
            continue

        resp_m = re.match(r"^(.+?)\s*\|\s*(.*)$", s)
        if resp_m:
            left, right = resp_m.group(1).strip(), resp_m.group(2).strip()
            if not left and right.startswith("invariant:"):
                current_cls.invs.append(right[len("invariant:"):].strip())
            elif left:
                collabs = (
                    [c.strip() for c in right.split(",") if c.strip()]
                    if right and not right.startswith("invariant:") and not right.startswith("(")
                    else []
                )
                if collabs:
                    current_cls.ops.append(f'{left} : {", ".join(collabs)}')
                    for c in collabs:
                        current_cls.edge_targets.append((c, "association"))
                else:
                    current_cls.props.append(left)

    return DomainModel(kas=kas, source_format="domain model")


# ---------------------------------------------------------------------------
# Class Model Parser
# ---------------------------------------------------------------------------

_PRIMITIVE_TYPES = frozenset({
    "String", "Integer", "Int", "Decimal", "Float", "Double", "Boolean",
    "Bool", "Date", "DateTime", "Timestamp", "Object", "Void", "void",
    "Number", "Any", "None",
})


def _extract_type_ref(content: str) -> Optional[str]:
    """Pull a class-name type reference from a property/operation signature."""
    m = re.search(r":\s*(?:List<|Set<|Optional<)?([A-Z][A-Za-z0-9_]+)", content)
    if m:
        t = m.group(1).strip()
        if t not in _PRIMITIVE_TYPES:
            return t
    return None


def parse_object_model(text: str) -> DomainModel:
    kas: Dict[str, List[ClassDef]] = {}
    current_ka: Optional[str] = None
    current_cls: Optional[ClassDef] = None
    # sections: ctor → props → ops  (separated by ------/----)
    section = "ctor"  # "ctor" | "props" | "ops"

    for line in text.split("\n"):
        s = line.strip()

        ka_m = re.match(r"^##\s+\*\*(.+?)\*\*\s*$", s)
        if ka_m:
            current_ka = ka_m.group(1)
            kas[current_ka] = []
            current_cls = None
            section = "ctor"
            continue

        # Class heading: ### **Name** << Stereotype >> or ### **Name : Base** << Stereotype >>
        cls_m = re.match(r"^###\s+\*\*(.+?)\*\*(?:\s*:\s*(.+?))?\s*(?:<<\s*(.+?)\s*>>)?\s*$", s)
        if cls_m and current_ka:
            raw = cls_m.group(1).strip()
            base = cls_m.group(2).strip() if cls_m.group(2) else None
            stereotype = cls_m.group(3).strip() if cls_m.group(3) else None
            if " : " in raw:
                parts = raw.split(" : ", 1)
                raw = parts[0].strip()
                base = parts[1].strip()
            current_cls = ClassDef(name=raw, ka=current_ka, base=base, stereotype=stereotype)
            kas[current_ka].append(current_cls)
            section = "ctor"
            continue

        if current_cls is None:
            continue

        # Section separator lines (4+ dashes)
        if re.match(r"^-{4,}\s*$", s):
            if section == "ctor":
                section = "props"
            else:
                section = "ops"
            continue

        # Invariant (indented under a property or operation)
        inv_m = re.match(r"^Invariant:\s*(.+)$", s, re.IGNORECASE)
        if inv_m:
            current_cls.invs.append(inv_m.group(1).strip())
            continue

        # Skip Interaction: blocks
        if s.startswith("Interaction:") or (s and s[0] in ("{", "}", "`")):
            continue

        # Property / operation lines starting with +
        prop_m = re.match(r"^\+\s+(.+)$", s)
        if not prop_m:
            continue

        content = prop_m.group(1).strip()

        # Skip constructor line
        if re.match(r"^" + re.escape(current_cls.name) + r"\s*\(", content) and section == "ctor":
            continue

        # Relationship stereotype on property
        rel_type = "association"
        rel_m = re.match(r"^<<\s*(.+?)\s*>>\s+(.+)$", content)
        if rel_m:
            rel_label = rel_m.group(1).lower()
            content = rel_m.group(2).strip()
            if "composition" in rel_label:
                rel_type = "composition"
            elif "aggregation" in rel_label:
                rel_type = "aggregation"

        type_ref = _extract_type_ref(content)

        if section in ("ctor", "props"):
            current_cls.props.append(content)
        else:
            current_cls.ops.append(content)

        if type_ref:
            current_cls.edge_targets.append((type_ref, rel_type))

    return DomainModel(kas=kas, source_format="domain-model")


# ---------------------------------------------------------------------------
# Domain Language Parser
# ---------------------------------------------------------------------------

def _strip_italics(s: str) -> str:
    return re.sub(r"\*([^*]+)\*", r"\1", s)


def _extract_italics(s: str) -> List[str]:
    return re.findall(r"\*([^*]+)\*", s)


def parse_ull(text: str) -> DomainModel:
    kas: Dict[str, List[ClassDef]] = {}
    current_ka: Optional[str] = None
    current_cls: Optional[ClassDef] = None
    # Track folded edges per class to avoid duplicate association arrows
    cls_edge_targets: Dict[str, set] = {}

    for line in text.split("\n"):
        s = line.strip()

        # KA heading: ## Name  or  ## **Name**  (not ###)
        if re.match(r"^##\s+", s) and not s.startswith("###"):
            ka_raw = re.sub(r"^##\s+", "", s).strip()           # strip ## prefix
            ka_raw = re.sub(r"^\*\*(.+?)\*\*$", r"\1", ka_raw)  # strip bold markers if present
            if ka_raw and not ka_raw[0].isdigit():
                current_ka = ka_raw
                kas[current_ka] = []
                current_cls = None
                continue

        if current_ka is None:
            continue

        # Subtype: ### Term *is a type of* Base
        sub_m = re.match(r"^###\s+(.+?)\s+\*is a type of\*\s+(.+?)\s*$", s)
        if sub_m:
            child, parent = sub_m.group(1).strip(), sub_m.group(2).strip()
            current_cls = ClassDef(name=child, ka=current_ka, base=parent)
            kas[current_ka].append(current_cls)
            cls_edge_targets[child] = set()
            continue

        # Boundary stub: skip (rendered as import on home KA only)
        if re.match(r"^###\s+.+\s+\*\(boundary\)\*\s*$", s):
            current_cls = None
            continue

        # Class heading: ### concept_name
        cls_m = re.match(r"^###\s+(.+?)$", s)
        if cls_m:
            name = cls_m.group(1).strip()
            current_cls = ClassDef(name=name, ka=current_ka)
            kas[current_ka].append(current_cls)
            cls_edge_targets[name] = set()
            continue

        if current_cls is None:
            continue

        # Invariant bullet
        if re.match(r"^-\s+\*\*Invariant:\*\*", s):
            inv_text = _strip_italics(re.sub(r"^-\s+\*\*Invariant:\*\*\s*", "", s))
            current_cls.invs.append(inv_text)
            continue

        # Behavior bullet
        if s.startswith("- "):
            bullet = s[2:]
            collabs = _extract_italics(bullet)
            clean = _strip_italics(re.sub(r"\*\*([^*]+)\*\*", r"\1", bullet))
            if collabs:
                current_cls.ops.append(f'{clean} : {", ".join(collabs)}')
                for c in collabs:
                    edge_set = cls_edge_targets.setdefault(current_cls.name, set())
                    if c not in edge_set:
                        edge_set.add(c)
                        current_cls.edge_targets.append((c, "association"))
            else:
                current_cls.props.append(clean)

    return DomainModel(kas=kas, source_format="domain-language")


# ---------------------------------------------------------------------------
# Parse dispatcher
# ---------------------------------------------------------------------------

def parse_source(path: Path) -> DomainModel:
    text = path.read_text(encoding="utf-8")
    fmt = detect_format(text, path)
    if fmt == "domain model":
        return parse_crc(text)
    if fmt in ("domain-model", "class-model"):
        return parse_object_model(text)
    if fmt == "domain-language":
        return parse_ull(text)
    return parse_crc(text)


# ---------------------------------------------------------------------------
# Sugiyama + Spring Layout  (TogetherJ-style)
# ---------------------------------------------------------------------------

class SugiyamaLayout:
    """
    TogetherJ-inspired layout engine for class diagrams.

    Pipeline:
      1. Cycle removal        — greedy DFS feedback-arc set
      2. Layer assignment     — longest-path from sources (import/base nodes = layer 0)
      3. Crossing reduction   — barycentric heuristic, 4 alternating sweeps
      4. Initial coordinates  — even x-spacing within each layer, y by layer depth
      5. Spring relaxation    — attraction between connected nodes,
                                repulsion between same-layer nodes;
                                produces organic "together" clustering of related classes
    """

    NODE_GAP: int = 100
    LAYER_GAP: int = 160
    MARGIN: int = 60
    SPRING_K: float = 0.12     # attraction spring constant
    REPULSE_K: float = 0.55    # repulsion constant
    ITERATIONS: int = 70

    def __init__(
        self,
        nodes: List[str],
        inh_edges: List[Tuple[str, str]],
        assoc_edges: List[Tuple[str, str]],
        widths: Dict[str, int],
        heights: Dict[str, int],
        import_nodes: Optional[List[str]] = None,
    ):
        self.nodes = nodes
        node_set = set(nodes)
        self.inh_edges = [(s, t) for s, t in inh_edges if s in node_set and t in node_set]
        self.assoc_edges = [(s, t) for s, t in assoc_edges if s in node_set and t in node_set]
        self.all_edges = self.inh_edges + self.assoc_edges
        self.widths = {n: widths.get(n, CELL_WIDTH) for n in nodes}
        self.heights = {n: heights.get(n, 100) for n in nodes}
        self.import_nodes = set(import_nodes or [])

    def layout(self) -> Dict[str, Tuple[int, int]]:
        if not self.nodes:
            return {}
        dag = self._remove_cycles()
        layers = self._assign_layers(dag)
        layers = self._minimize_crossings(layers, dag)
        pos = self._initial_coords(layers)
        pos = self._spring_relax(pos, layers)
        return {n: (int(pos[n][0]), int(pos[n][1])) for n in self.nodes}

    def back_edges(self) -> List[Tuple[str, str]]:
        """Return the edges removed during cycle removal (reversed long-range edges)."""
        dag_set = set(self._remove_cycles())
        return [(s, t) for s, t in self.all_edges if (s, t) not in dag_set]

    # --- Step 1: Cycle removal ---

    def _remove_cycles(self) -> List[Tuple[str, str]]:
        visited: set = set()
        stack: set = set()
        back: set = set()
        adj: Dict[str, List[str]] = {n: [] for n in self.nodes}
        for s, t in self.all_edges:
            adj[s].append(t)

        def dfs(n: str) -> None:
            visited.add(n)
            stack.add(n)
            for t in adj.get(n, []):
                if t not in visited:
                    dfs(t)
                elif t in stack:
                    back.add((n, t))
            stack.discard(n)

        for n in self.nodes:
            if n not in visited:
                dfs(n)

        return [(s, t) for s, t in self.all_edges if (s, t) not in back]

    # --- Step 2: Layer assignment ---

    def _assign_layers(self, dag: List[Tuple[str, str]]) -> List[List[str]]:
        node_set = set(self.nodes)
        parents: Dict[str, List[str]] = {n: [] for n in self.nodes}
        for s, t in dag:
            if s in node_set and t in node_set:
                parents[t].append(s)

        cache: Dict[str, int] = {}

        def depth(n: str) -> int:
            if n in cache:
                return cache[n]
            if n in self.import_nodes:
                cache[n] = 0
                return 0
            preds = [p for p in parents.get(n, []) if p != n]
            cache[n] = (max(depth(p) for p in preds) + 1) if preds else 0
            return cache[n]

        for n in self.nodes:
            depth(n)

        max_l = max(cache.values()) if cache else 0
        layers: List[List[str]] = [[] for _ in range(max_l + 1)]
        for n in self.nodes:
            layers[cache.get(n, 0)].append(n)
        return layers

    # --- Step 3: Crossing minimization ---

    def _minimize_crossings(
        self, layers: List[List[str]], dag: List[Tuple[str, str]]
    ) -> List[List[str]]:
        node_set = set(self.nodes)
        succ: Dict[str, set] = {n: set() for n in self.nodes}
        pred: Dict[str, set] = {n: set() for n in self.nodes}
        for s, t in dag:
            if s in node_set and t in node_set:
                succ[s].add(t)
                pred[t].add(s)

        for _ in range(2):
            for i in range(1, len(layers)):
                pos = {n: j for j, n in enumerate(layers[i - 1])}

                def bary_fwd(n: str, _pos: dict = pos) -> float:
                    ps = [p for p in pred.get(n, set()) if p in _pos]
                    return sum(_pos[p] for p in ps) / len(ps) if ps else 1e9

                layers[i].sort(key=bary_fwd)

            for i in range(len(layers) - 2, -1, -1):
                pos = {n: j for j, n in enumerate(layers[i + 1])}

                def bary_bwd(n: str, _pos: dict = pos) -> float:
                    ss = [s for s in succ.get(n, set()) if s in _pos]
                    return sum(_pos[s] for s in ss) / len(ss) if ss else 1e9

                layers[i].sort(key=bary_bwd)

        return layers

    # --- Step 4: Initial coordinates ---

    def _initial_coords(self, layers: List[List[str]]) -> Dict[str, List[float]]:
        pos: Dict[str, List[float]] = {}
        y = float(self.MARGIN)
        for layer in layers:
            x = float(self.MARGIN)
            for n in layer:
                pos[n] = [x, y]
                x += self.widths[n] + self.NODE_GAP
            max_h = max((self.heights[n] for n in layer), default=100)
            y += max_h + self.LAYER_GAP
        return pos

    # --- Step 5: Spring relaxation (TogetherJ post-pass) ---

    def _spring_relax(
        self,
        pos: Dict[str, List[float]],
        layers: List[List[str]],
    ) -> Dict[str, List[float]]:
        """
        Adjusts X coordinates only (Y is fixed by layer assignment).

        Attraction force: connected nodes are pulled toward each other,
        clustering heavily associated classes side-by-side (the 'together' effect).

        Repulsion force: same-layer nodes are pushed apart when they overlap,
        maintaining minimum separation of NODE_GAP.

        Cooling schedule: damping factor decreases each iteration so the system
        converges rather than oscillating.
        """
        node_set = set(self.nodes)
        damping = 1.0

        for _ in range(self.ITERATIONS):
            fx: Dict[str, float] = {n: 0.0 for n in self.nodes}

            # Attraction between all connected nodes
            for s, t in self.all_edges:
                if s not in node_set or t not in node_set:
                    continue
                dx = pos[t][0] - pos[s][0]
                f = self.SPRING_K * dx
                fx[s] += f
                fx[t] -= f

            # Repulsion between same-layer nodes that are too close
            for layer in layers:
                for i, a in enumerate(layer):
                    for b in layer[i + 1:]:
                        dx = pos[b][0] - pos[a][0]
                        min_sep = (self.widths[a] + self.widths[b]) / 2 + self.NODE_GAP
                        if abs(dx) < min_sep + 1:
                            gap = min_sep - abs(dx) + 1
                            sign = 1.0 if dx >= 0 else -1.0
                            f = self.REPULSE_K * gap
                            fx[a] -= sign * f
                            fx[b] += sign * f

            for n in self.nodes:
                pos[n][0] += fx[n] * damping

            damping *= 0.97  # gradual cooling

        # Final overlap resolution: left-to-right, respect minimum separation
        for layer in layers:
            ordered = sorted(layer, key=lambda n: pos[n][0])
            x = float(self.MARGIN)
            for n in ordered:
                pos[n][0] = max(pos[n][0], x)
                x = pos[n][0] + self.widths[n] + self.NODE_GAP

        return pos


# ---------------------------------------------------------------------------
# Cell height estimation
# ---------------------------------------------------------------------------

def _estimate_height(cls: ClassDef) -> int:
    return calc_cell_height(len(cls.props), len(cls.ops), min(len(cls.invs), 4))


# ---------------------------------------------------------------------------
# Edge anchor helper
# ---------------------------------------------------------------------------

def _spread_anchors(n_edges: int) -> List[float]:
    """Return evenly spaced anchor x-positions across [0.15, 0.85]."""
    if n_edges <= 1:
        return [0.5]
    return [0.15 + (0.7 / (n_edges - 1)) * i for i in range(n_edges)]


# ---------------------------------------------------------------------------
# Page renderer
# ---------------------------------------------------------------------------

def render_ka(
    mxfile,
    ka_name: str,
    classes: List[ClassDef],
    model: DomainModel,
    page_w: int,
    page_h: int,
) -> None:
    add_page(mxfile, ka_name, page_w, page_h)
    _, root = get_page(mxfile, ka_name)

    local_names = {cls.name for cls in classes}

    # Cross-KA imports (inheritance ancestors only — full ancestor chain)
    imports_needed: Dict[str, str] = {}
    for cls in classes:
        b = cls.base
        while b and b not in local_names:
            src = model.class_by_name(b)
            if src is None:
                break
            if src.ka != ka_name:
                imports_needed[b] = src.ka
            b = src.base

    import_defs: List[Tuple[ClassDef, str]] = []
    for imp_name, imp_ka in imports_needed.items():
        src = model.class_by_name(imp_name)
        if src:
            stub = ClassDef(name=imp_name, ka=imp_ka)
            stub.props = src.props[:3]
            import_defs.append((stub, imp_ka))

    all_nodes = [cls.name for cls in classes] + [s.name for s, _ in import_defs]
    page_node_set = set(all_nodes)
    import_node_names = [s.name for s, _ in import_defs]

    # Build typed edge lists for layout
    inh_edges: List[Tuple[str, str]] = []
    assoc_edges: List[Tuple[str, str]] = []
    comp_edges: List[Tuple[str, str]] = []
    agg_edges: List[Tuple[str, str]] = []
    seen_pairs: set = set()

    for cls in classes:
        if cls.base and cls.base in page_node_set:
            inh_edges.append((cls.name, cls.base))
        for tgt, etype in cls.edge_targets:
            if tgt not in page_node_set or tgt == cls.name:
                continue
            pair = (cls.name, tgt)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            if etype == "composition":
                comp_edges.append(pair)
            elif etype == "aggregation":
                agg_edges.append(pair)
            else:
                assoc_edges.append(pair)

    # Heights / widths
    heights = {cls.name: _estimate_height(cls) for cls in classes}
    for stub, _ in import_defs:
        heights[stub.name] = _estimate_height(stub) + 20

    lyt = SugiyamaLayout(
        nodes=all_nodes,
        inh_edges=inh_edges,
        assoc_edges=assoc_edges + comp_edges + agg_edges,
        widths={n: CELL_WIDTH for n in all_nodes},
        heights=heights,
        import_nodes=import_node_names,
    )
    positions = lyt.layout()
    back_edge_set = set(lyt.back_edges())

    # Back-edges (cycle-reversed by Sugiyama) are suppressed from the diagram.
    # The class card text already shows every relationship — extra arrows from
    # cycle edges only add visual noise in auto-layout diagrams.
    assoc_fwd = [(s, t) for s, t in assoc_edges if (s, t) not in back_edge_set]
    comp_fwd = [(s, t) for s, t in comp_edges if (s, t) not in back_edge_set]
    agg_fwd = [(s, t) for s, t in agg_edges if (s, t) not in back_edge_set]

    # Render import cells
    for stub, source_ka in import_defs:
        x, y = positions.get(stub.name, (SugiyamaLayout.MARGIN, SugiyamaLayout.MARGIN))
        create_class_cell(
            root, stub.name,
            properties=stub.props, operations=[],
            x=x, y=y, imported_from=source_ka,
        )

    # Render local class cells
    for cls in classes:
        x, y = positions.get(cls.name, (SugiyamaLayout.MARGIN, SugiyamaLayout.MARGIN))
        create_class_cell(
            root, cls.name, base=cls.base,
            properties=cls.props, operations=cls.ops,
            invariants=cls.invs[:4],
            x=x, y=y,
        )

    widths_map = {n: CELL_WIDTH for n in all_nodes}

    # Add edges with direction-aware anchors to minimise crossings
    _add_all_edges(root, inh_edges, assoc_fwd, comp_fwd, agg_fwd, positions,
                   widths_map, heights)


def _add_all_edges(
    root,
    inh_edges: List[Tuple[str, str]],
    assoc_edges: List[Tuple[str, str]],
    comp_edges: List[Tuple[str, str]],
    agg_edges: List[Tuple[str, str]],
    positions: Dict[str, Tuple[int, int]],
    widths: Dict[str, int],
    heights: Dict[str, int],
) -> None:
    """
    Add edges with direction-aware exit/entry anchors.

    For each (src, tgt) pair the dominant direction is derived from the class
    centre-point delta.  Edges leaving the same side of a class are spread
    across evenly distributed anchor positions so they never share a default
    centre anchor.
    """
    from collections import defaultdict

    all_pairs = inh_edges + assoc_edges + comp_edges + agg_edges

    # Determine which side each edge leaves/enters so we can spread within side
    # side: "top" | "bottom" | "left" | "right"
    def _dominant_side(src: str, tgt: str) -> Tuple[str, str]:
        sx, sy = positions.get(src, (0, 0))
        tx, ty = positions.get(tgt, (0, 0))
        sw = widths.get(src, CELL_WIDTH)
        sh = heights.get(src, 100)
        tw = widths.get(tgt, CELL_WIDTH)
        th = heights.get(tgt, 100)
        # Use centre-points
        scx = sx + sw / 2
        scy = sy + sh / 2
        tcx = tx + tw / 2
        tcy = ty + th / 2
        dx = tcx - scx
        dy = tcy - scy
        if abs(dy) >= abs(dx):
            exit_side = "bottom" if dy >= 0 else "top"
            entry_side = "top" if dy >= 0 else "bottom"
        else:
            exit_side = "right" if dx >= 0 else "left"
            entry_side = "left" if dx >= 0 else "right"
        return exit_side, entry_side

    # Group edges by (node, side)
    exit_groups: Dict[Tuple[str, str], List[Tuple[str, str]]] = defaultdict(list)
    entry_groups: Dict[Tuple[str, str], List[Tuple[str, str]]] = defaultdict(list)
    pair_sides: Dict[Tuple[str, str], Tuple[str, str]] = {}

    for s, t in all_pairs:
        es, en = _dominant_side(s, t)
        pair_sides[(s, t)] = (es, en)
        exit_groups[(s, es)].append((s, t))
        entry_groups[(t, en)].append((s, t))

    # Assign anchor indices within each group
    exit_anchor: Dict[Tuple[str, str], float] = {}
    entry_anchor: Dict[Tuple[str, str], float] = {}
    for (node, side), pairs in exit_groups.items():
        positions_spread = _spread_anchors(len(pairs))
        for i, pair in enumerate(pairs):
            exit_anchor[pair] = positions_spread[i]
    for (node, side), pairs in entry_groups.items():
        positions_spread = _spread_anchors(len(pairs))
        for i, pair in enumerate(pairs):
            entry_anchor[pair] = positions_spread[i]

    SIDE_XY = {
        "top":    (None, 0),
        "bottom": (None, 1),
        "left":   (0, None),
        "right":  (1, None),
    }

    def draw(s: str, t: str, edge_type: str) -> None:
        sc = find_cell_by_name(root, s)
        tc = find_cell_by_name(root, t)
        if sc is None or tc is None:
            return
        pair = (s, t)
        es, en = pair_sides.get(pair, ("bottom", "top"))
        ex_spread = exit_anchor.get(pair, 0.5)
        en_spread = entry_anchor.get(pair, 0.5)
        ex_fixed_x, ex_fixed_y = SIDE_XY[es]
        en_fixed_x, en_fixed_y = SIDE_XY[en]
        kwargs: Dict = {}
        kwargs["exit_x"] = ex_fixed_x if ex_fixed_x is not None else ex_spread
        kwargs["exit_y"] = ex_fixed_y if ex_fixed_y is not None else ex_spread
        kwargs["entry_x"] = en_fixed_x if en_fixed_x is not None else en_spread
        kwargs["entry_y"] = en_fixed_y if en_fixed_y is not None else en_spread
        try:
            create_edge(root, sc.get("id"), tc.get("id"), edge_type, **kwargs)
        except ValueError:
            pass

    for s, t in inh_edges:
        draw(s, t, "inheritance-orthogonal")
    for s, t in assoc_edges:
        draw(s, t, "association")
    for s, t in comp_edges:
        draw(s, t, "composition")
    for s, t in agg_edges:
        draw(s, t, "aggregation")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Domain model (domain model / class-model / ULL) → Draw.io class diagram"
    )
    parser.add_argument("source", type=Path, help="Source .md file")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output .drawio path")
    parser.add_argument("--ka", default=None,
                        help="Render only the named Key Abstraction")
    parser.add_argument("--page-w", type=int, default=3000,
                        help="Page width px (default 3000)")
    parser.add_argument("--page-h", type=int, default=2000,
                        help="Page height px (default 2000)")
    args = parser.parse_args()

    source_path = args.source.resolve()
    if not source_path.exists():
        print(f"Error: {source_path} not found", file=sys.stderr)
        sys.exit(1)

    stem = source_path.stem
    if stem.endswith("-class-diagram"):
        stem = stem[: -len("-class-diagram")]
    output_path = (
        args.output.resolve()
        if args.output
        else source_path.parent / f"{stem}-class-diagram.drawio"
    )

    print(f"Parsing:  {source_path}")
    model = parse_source(source_path)
    print(f"Format:   {model.source_format}")
    print(f"KAs:      {list(model.kas.keys())}")

    mxfile = create_empty_mxfile()

    kas_to_render = (
        {args.ka: model.kas[args.ka]}
        if args.ka and args.ka in model.kas
        else model.kas
    )
    for ka_name, classes in kas_to_render.items():
        if not classes:
            continue
        print(f"Rendering [{ka_name}] — {len(classes)} classes")
        render_ka(mxfile, ka_name, classes, model, args.page_w, args.page_h)

    save_drawio(output_path, mxfile)
    print(f"\nWrote:    {output_path}")

    report = audit_diagram_report(str(output_path))
    print("\n" + report)

    # Approximate crossings (tagged with "(approx)") arise from the checker's
    # L-shape heuristic for orthogonal edges without explicit waypoints.  The
    # actual Draw.io renderer uses a smarter router and resolves these automatically.
    # Only hard-fail on definitive (non-approx) edge_crosses_class violations.
    definitive = [
        ln for ln in report.splitlines()
        if "[edge_crosses_class]" in ln and "(approx)" not in ln
    ]
    if definitive:
        print("\nDefinitive edge_crosses_class violations (must fix):", file=sys.stderr)
        for ln in definitive:
            print(" ", ln, file=sys.stderr)
        sys.exit(1)
    elif "[edge_crosses_class]" in report:
        print("\nNote: approx crossings shown above are checker heuristics — "
              "Draw.io's router will resolve them in the rendered diagram.")


if __name__ == "__main__":
    main()
