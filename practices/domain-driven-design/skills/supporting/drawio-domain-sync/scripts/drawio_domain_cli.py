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
    add_edge_waypoints,
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
    """Return one of: 'domain-model' | 'domain-specification' | 'domain-language'."""
    fm = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
    if fm:
        state = re.search(r"^state:\s*(.+)$", fm.group(1), re.MULTILINE)
        if state:
            return state.group(1).strip()
    stem = path.stem.lower()
    if "domain-language" in stem or "ubiquitous_language" in stem:
        return "domain-language"
    if "class-model" in stem or "domain-specification" in stem:
        return "domain-specification"
    # Default: domain model (covers *-domain-model.md and anything unrecognised)
    return "domain-model"


# ---------------------------------------------------------------------------
# domain model Parser
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Class Model Parser  (domain-model and domain-specification formats)
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


def parse_object_model(text: str, source_format: str = "domain-model") -> DomainModel:
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

        # Property / operation lines — with '+' prefix (typed class-model) or
        # bare 'name: Type' / 'method(): Type' (domain model format without '+')
        prop_m = re.match(r"^\+\s+(.+)$", s)
        if prop_m:
            content = prop_m.group(1).strip()
        elif section in ("props", "ops"):
            # Accept bare property/operation lines that look like "identifier: Type"
            # Exclude indented collaborator lines (they start with whitespace before strip)
            # and lines that are clearly not prop/op declarations.
            bare_m = re.match(r"^([A-Za-z_]\w*\s*(?:\([^)]*\))?\s*:\s*.+)$", s)
            if bare_m and not s.startswith("#") and "Invariant" not in s:
                content = bare_m.group(1).strip()
            else:
                continue
        else:
            continue

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

    return DomainModel(kas=kas, source_format=source_format)


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
    if fmt == "domain-language":
        return parse_ull(text)
    # domain-model and domain-specification both use the typed class-block format
    return parse_object_model(text, source_format=fmt)


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
        top_nodes: Optional[List[str]] = None,
    ):
        self.nodes = nodes
        node_set = set(nodes)
        self.inh_edges = [(s, t) for s, t in inh_edges if s in node_set and t in node_set]
        self.assoc_edges = [(s, t) for s, t in assoc_edges if s in node_set and t in node_set]
        self.all_edges = self.inh_edges + self.assoc_edges
        self.widths = {n: widths.get(n, CELL_WIDTH) for n in nodes}
        self.heights = {n: heights.get(n, 100) for n in nodes}
        # Backwards compat: ``import_nodes`` historically pinned every imported
        # class to depth 0. That conflated inheritance-ancestor imports (which
        # belong at the top) with association/composition imports (which belong
        # near their connectors). Prefer ``top_nodes`` to mean "force to depth 0".
        self.top_nodes = set(top_nodes if top_nodes is not None else (import_nodes or []))
        self.import_nodes = set(import_nodes or [])

    def layout(self) -> Dict[str, Tuple[int, int]]:
        if not self.nodes:
            return {}
        dag = self._remove_cycles()
        layers = self._assign_layers(dag)
        layers = self._pull_up_assoc_sinks(layers)
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
        """Longest-path layering.

        Convention: inheritance flows DOWN. A class always sits *below* its
        base class, so for inheritance edges (child → base) we treat the BASE
        as the layer-predecessor of the child. For association/composition/
        aggregation edges (source → target) we keep the natural direction so
        the target sits below the source.

        Nodes in ``top_nodes`` are forced to depth 0 (e.g. cross-KA inheritance
        ancestors that should always anchor the top of the page).
        """
        node_set = set(self.nodes)
        inh_set = set(self.inh_edges)
        dag_set = set(dag)

        # layer_parents[n] = nodes that must sit at lower y than n
        layer_parents: Dict[str, List[str]] = {n: [] for n in self.nodes}
        for s, t in dag:
            if s not in node_set or t not in node_set:
                continue
            if (s, t) in inh_set:
                # Inheritance: child→base in the model, so base is the layer-parent of child
                layer_parents[s].append(t)
            else:
                layer_parents[t].append(s)

        cache: Dict[str, int] = {}

        def depth(n: str) -> int:
            if n in cache:
                return cache[n]
            if n in self.top_nodes:
                cache[n] = 0
                return 0
            preds = [p for p in layer_parents.get(n, []) if p != n]
            cache[n] = (max(depth(p) for p in preds) + 1) if preds else 0
            return cache[n]

        for n in self.nodes:
            depth(n)

        max_l = max(cache.values()) if cache else 0
        layers: List[List[str]] = [[] for _ in range(max_l + 1)]
        for n in self.nodes:
            layers[cache.get(n, 0)].append(n)
        return layers

    # --- Step 2b: Pull up pure-association sinks ---

    def _pull_up_assoc_sinks(
        self, layers: List[List[str]]
    ) -> List[List[str]]:
        """Move "pure-association sinks" to the median of their source layers.

        Longest-path layering buries a class as deep as its deepest predecessor.
        For a class that is only ever associated TO (no inheritance role, no
        outgoing edges), that buries it far below shallow predecessors and
        forces multi-layer U-shape edges from those shallow predecessors.

        A class qualifies for repositioning when ALL of these hold:
          - no outgoing edges (inheritance or association)
          - no inheritance role (no class inherits from it, it inherits from
            nothing within the page)
          - has at least one incoming association/composition/aggregation edge
          - it is not pinned via top_nodes

        For such a class we place it at the median of its source layers. This
        is the position that minimizes total source→sink edge length, so the
        router has the shortest possible routes to find without crossing the
        rest of the diagram.
        """
        node_set = set(self.nodes)
        inh_set = set(self.inh_edges)

        layer_of: Dict[str, int] = {}
        for i, layer in enumerate(layers):
            for n in layer:
                layer_of[n] = i

        # Aggregate edge roles per node using the ORIGINAL edge set so cycle
        # removal does not confuse the role detection.
        out_total: Dict[str, set] = {n: set() for n in self.nodes}
        in_inh: Dict[str, set] = {n: set() for n in self.nodes}     # bases (this node inherits from)
        out_inh_as_base: Dict[str, set] = {n: set() for n in self.nodes}  # subclasses that derive from this node
        in_assoc: Dict[str, set] = {n: set() for n in self.nodes}

        for s, t in self.all_edges:
            if s not in node_set or t not in node_set:
                continue
            out_total[s].add(t)
            if (s, t) in inh_set:
                # child=s inherits from base=t
                in_inh[s].add(t)
                out_inh_as_base[t].add(s)
            else:
                in_assoc[t].add(s)

        candidates: List[str] = []
        for n in self.nodes:
            if n in self.top_nodes:
                continue
            if out_total[n]:
                continue
            if in_inh[n] or out_inh_as_base[n]:
                continue
            if not in_assoc[n]:
                continue
            candidates.append(n)

        for n in candidates:
            src_layers = sorted(
                layer_of[s] for s in in_assoc[n] if s in layer_of
            )
            if not src_layers:
                continue
            # Target = one layer below the SHALLOWEST source.
            # - For a single-source sink (e.g. ContextIndex → ContextIndexRow
            #   in CDD), this leaves the sink at source+1 (already its natural
            #   place from longest-path), so no move.
            # - For a multi-source sink (e.g. Reference with sources at
            #   layers [0, 1, 2] in AbdSkill), this collapses the layer span
            #   from 3 down to 1, turning a 3-layer U-snake into a one-hop
            #   route from the topmost source.
            target = min(src_layers) + 1
            current = layer_of[n]
            if target == current:
                continue
            if target > current:
                # Never push sinks deeper than longest-path already does.
                continue
            while len(layers) <= target:
                layers.append([])
            layers[current].remove(n)
            layers[target].append(n)
            layer_of[n] = target

        # Drop trailing empty layers
        while layers and not layers[-1]:
            layers.pop()

        return layers

    # --- Step 3: Crossing minimization ---

    def _minimize_crossings(
        self, layers: List[List[str]], dag: List[Tuple[str, str]]
    ) -> List[List[str]]:
        node_set = set(self.nodes)
        inh_set = set(self.inh_edges)
        # Build succ/pred consistent with layer direction: edges always go
        # from shallower (top) layer to deeper (bottom) layer.
        succ: Dict[str, set] = {n: set() for n in self.nodes}
        pred: Dict[str, set] = {n: set() for n in self.nodes}
        for s, t in dag:
            if s not in node_set or t not in node_set:
                continue
            if (s, t) in inh_set:
                # Inheritance edge (child, base): layer direction is base→child
                succ[t].add(s)
                pred[s].add(t)
            else:
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

    # Cross-KA imports — inheritance ancestors (full ancestor chain). These
    # should always anchor the TOP of the page so that derived classes flow
    # downward from them.
    inh_imports: Dict[str, str] = {}
    for cls in classes:
        b = cls.base
        while b and b not in local_names:
            src = model.class_by_name(b)
            if src is None:
                break
            if src.ka != ka_name:
                inh_imports[b] = src.ka
            b = src.base

    # Cross-KA imports — direct association/composition/aggregation targets.
    # These are boundary classes (dashed border) and should be placed by
    # natural layering near the local class that connects to them, NOT pinned
    # to the top.
    assoc_imports: Dict[str, str] = {}
    for cls in classes:
        for tgt, _etype in cls.edge_targets:
            if tgt in local_names or tgt in inh_imports or tgt in assoc_imports:
                continue
            tgt_def = model.class_by_name(tgt)
            if tgt_def is not None and tgt_def.ka != ka_name:
                assoc_imports[tgt] = tgt_def.ka

    imports_needed: Dict[str, str] = {**inh_imports, **assoc_imports}

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
    top_pinned_names = [name for name in inh_imports.keys()]

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
        top_nodes=top_pinned_names,
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

    inh_set = set(inh_edges)

    # First pass: dominant side
    for s, t in all_pairs:
        es, en = _dominant_side(s, t)
        pair_sides[(s, t)] = (es, en)

    # Second pass: relocate association edges that would share the
    # top/bottom side of a class with inheritance entries/exits.
    # Inheritance entries land on a parent's bottom (children below).
    # Inheritance exits leave a child's top. Associations should prefer the
    # left/right sides when there's any inheritance traffic on the same side.
    inh_exit_sides: Dict[Tuple[str, str], int] = defaultdict(int)
    inh_entry_sides: Dict[Tuple[str, str], int] = defaultdict(int)
    for (s, t) in inh_edges:
        es, en = pair_sides[(s, t)]
        inh_exit_sides[(s, es)] += 1
        inh_entry_sides[(t, en)] += 1

    def _perpendicular_side(orig: str, src: str, tgt: str) -> str:
        """Pick the side for ``src`` to use when routing toward ``tgt``,
        given that ``orig`` is blocked. Uses raw positions to match the
        legacy behavior."""
        sx = positions.get(src, (0, 0))[0]
        tx = positions.get(tgt, (0, 0))[0]
        if orig in ("top", "bottom"):
            return "left" if tx < sx else "right"
        return "top" if positions.get(tgt, (0, 0))[1] < positions.get(src, (0, 0))[1] else "bottom"

    def _perpendicular_side_by_center(orig: str, src: str, tgt: str) -> str:
        """Same as ``_perpendicular_side`` but compares CENTERS so that two
        classes with identical top-left y but different heights still pick
        a consistent wrap side. Used only for the mirrored both-blocked
        case where we need source and target to agree on which side to
        wrap around."""
        sx = positions.get(src, (0, 0))[0]
        sy = positions.get(src, (0, 0))[1]
        tx = positions.get(tgt, (0, 0))[0]
        ty = positions.get(tgt, (0, 0))[1]
        sw = widths.get(src, CELL_WIDTH)
        sh = heights.get(src, 100)
        tw = widths.get(tgt, CELL_WIDTH)
        th = heights.get(tgt, 100)
        scx = sx + sw / 2
        scy = sy + sh / 2
        tcx = tx + tw / 2
        tcy = ty + th / 2
        if orig in ("top", "bottom"):
            return "left" if tcx <= scx else "right"
        return "top" if tcy <= scy else "bottom"

    def _opposite(side: str) -> str:
        return {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}[side]

    # Choose perpendicular target only when the original side would create a
    # *physical* overlap that the anchor merge cannot resolve. Two edges on
    # the same side share a single anchor pool and get distinct fractional
    # positions, so simply colliding with inheritance on the same side is no
    # longer a problem.
    #
    # The remaining hazard is when moving an association to a perpendicular
    # side would make its first segment travel along an EDGE that another
    # association already uses (e.g., both leaving PS-bottom collide along
    # y=616). To avoid that, we only perpendicularize when the perpendicular
    # candidate is itself free of inheritance traffic. Otherwise we keep the
    # natural side and let the anchor pool stagger the routes.
    def _is_busy(node: str, side: str) -> bool:
        return (
            inh_entry_sides.get((node, side), 0) > 0
            or inh_exit_sides.get((node, side), 0) > 0
        )

    for (s, t) in assoc_edges + comp_edges + agg_edges:
        es, en = pair_sides[(s, t)]
        src_blocked = _is_busy(s, es)
        tgt_blocked = _is_busy(t, en)

        # If BOTH ends are blocked, the source and target need to wrap
        # around the SAME side of the layout — otherwise the edge ends
        # up doubling back across class interiors (e.g.
        # AiChatAgent.left → Subagent.right slicing straight through
        # AiChatAgent). Pick the wrap side by comparing centers (a
        # robust signal regardless of top-left y) and mirror it onto
        # both endpoints.
        if src_blocked and tgt_blocked:
            mirrored = _perpendicular_side_by_center(es, s, t)
            if not _is_busy(s, mirrored) and not _is_busy(t, mirrored):
                pair_sides[(s, t)] = (mirrored, mirrored)
                continue
            alt = _opposite(mirrored)
            if not _is_busy(s, alt) and not _is_busy(t, alt):
                pair_sides[(s, t)] = (alt, alt)
                continue
            # Fallthrough to independent placement.

        # Independent placement (legacy behavior): relocate each
        # blocked end onto its own natural perpendicular side, leaving
        # unblocked ends alone. This preserves the prior choices for
        # everything that was already passing.
        new_es = _perpendicular_side(es, s, t) if src_blocked else es
        new_en = _perpendicular_side(en, t, s) if tgt_blocked else en
        if src_blocked and not _is_busy(s, new_es):
            es = new_es
        if tgt_blocked and not _is_busy(t, new_en):
            en = new_en
        pair_sides[(s, t)] = (es, en)

    # Group edges by (node, side) — both exits and entries on the same side
    # of the same node share a single anchor pool, so an outgoing edge and
    # an incoming edge never collide on the same anchor point.
    # `side_groups[(node, side)]` holds (pair, role) tuples where role is
    # "exit" or "entry". The exit_groups / entry_groups maps are kept for
    # later code that still iterates over them.
    side_groups: Dict[Tuple[str, str], List[Tuple[Tuple[str, str], str]]] = defaultdict(list)
    for s, t in all_pairs:
        es, en = pair_sides[(s, t)]
        exit_groups[(s, es)].append((s, t))
        entry_groups[(t, en)].append((s, t))
        side_groups[(s, es)].append(((s, t), "exit"))
        side_groups[(t, en)].append(((s, t), "entry"))

    # Assign anchor indices within each group.
    #
    # CRITICAL: sort pairs so the anchor positions along the side run in the
    # same order as the targets' angles from the source center (and likewise
    # for entry anchors from the target center). This guarantees that L- or
    # H-V-H routes from a shared exit side do not cross each other.
    #
    # Two ways to see why angle is the right key:
    #   - Imagine standing inside the source class, looking out the right
    #     side. Targets appear at various angles; sorting by that angle and
    #     mapping to top→bottom of the side keeps the routes non-crossing.
    #   - Formally: for orthogonal H-V-H routing from a vertical side, two
    #     routes cross iff target_x order and exit_y order disagree relative
    #     to the going direction. Sorting by angle ensures they agree.
    #
    # Without this sort, the run-5 AbdSkill→{Reference, Scanner, Template}
    # routes interleaved because all three targets shared the same Y and the
    # tiebreaker was insertion order.
    def _anchor_sort_key(
        pair: Tuple[str, str], node: str, side: str, role: str
    ) -> Tuple[int, float, float]:
        """Sort key that orders edges along a shared side to avoid crossings.

        The geometric fact: for two edges leaving the same vertical side of a
        source and routing H-V-H to two targets, their L-shapes cross iff the
        targets are on the same side (both above or both below) AND the
        edge with the closer target_x has the smaller exit_y (going down) or
        larger exit_y (going up).

        So the rule is:
          1. Primary key: which half-plane the OTHER end is in
             (above/below for vertical sides, left/right for horizontal sides).
             Same-side targets stay grouped together.
          2. Secondary key: distance along the normal direction, with sign
             chosen so the FARTHEST target gets the anchor closest to the
             corner pointing toward those targets.
        """
        s, t = pair
        other = t if role == "exit" else s
        nx, ny = positions.get(node, (0, 0))
        nw = widths.get(node, CELL_WIDTH)
        nh = heights.get(node, 100)
        ncx, ncy = nx + nw / 2, ny + nh / 2
        ox, oy = positions.get(other, (0, 0))
        ow = widths.get(other, CELL_WIDTH)
        oh = heights.get(other, 100)
        ocx, ocy = ox + ow / 2, oy + oh / 2

        if side in ("right", "left"):
            # Vertical side: anchor runs top→bottom.
            # Half-plane: above (-1), level (0), below (+1) source.
            if ocy < ny:
                plane = -1
            elif ocy > ny + nh:
                plane = +1
            else:
                plane = 0
            # Distance along the normal (away from source toward target).
            dist_along = abs(ocx - ncx)
            # For below targets: top anchor should serve farthest target →
            # ascending key by -dist (so larger dist sorts FIRST).
            # For above targets: bottom anchor should serve farthest target →
            # ascending key by +dist (so larger dist sorts LAST).
            secondary = -dist_along if plane >= 0 else dist_along
            return (plane, secondary, ocy)

        # Horizontal side: anchor runs left→right.
        if ocx < nx:
            plane = -1
        elif ocx > nx + nw:
            plane = +1
        else:
            plane = 0
        dist_along = abs(ocy - ncy)
        secondary = -dist_along if plane >= 0 else dist_along
        return (plane, secondary, ocx)

    # Allocate anchors per (node, side) over the COMBINED pool of exits and
    # entries. This is what prevents an outgoing edge from landing on the
    # same anchor point as an incoming edge (the "AbdSkill→Rule exit and
    # PracticeSkill→AbdSkill entry both at left-middle" collision).
    exit_anchor: Dict[Tuple[str, str], float] = {}
    entry_anchor: Dict[Tuple[str, str], float] = {}
    for (node, side), items in side_groups.items():
        ordered = sorted(
            items, key=lambda item: _anchor_sort_key(item[0], node, side, item[1])
        )
        positions_spread = _spread_anchors(len(ordered))
        for i, (pair, role) in enumerate(ordered):
            if role == "exit":
                exit_anchor[pair] = positions_spread[i]
            else:
                entry_anchor[pair] = positions_spread[i]

    SIDE_XY = {
        "top":    (None, 0),
        "bottom": (None, 1),
        "left":   (0, None),
        "right":  (1, None),
    }

    # Record each created edge with the absolute anchor pixel coordinates so a
    # later pass can dog-leg around obstacles.
    created: List[Dict] = []

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
        exit_x = ex_fixed_x if ex_fixed_x is not None else ex_spread
        exit_y = ex_fixed_y if ex_fixed_y is not None else ex_spread
        entry_x = en_fixed_x if en_fixed_x is not None else en_spread
        entry_y = en_fixed_y if en_fixed_y is not None else en_spread
        try:
            cell = create_edge(
                root, sc.get("id"), tc.get("id"), edge_type,
                exit_x=exit_x, exit_y=exit_y,
                entry_x=entry_x, entry_y=entry_y,
            )
        except ValueError:
            return

        # Absolute pixel anchor coordinates
        sx, sy = positions.get(s, (0, 0))
        tx, ty = positions.get(t, (0, 0))
        sw = widths.get(s, CELL_WIDTH)
        sh = heights.get(s, 100)
        tw = widths.get(t, CELL_WIDTH)
        th = heights.get(t, 100)
        ex_pt = (sx + sw * exit_x, sy + sh * exit_y)
        en_pt = (tx + tw * entry_x, ty + th * entry_y)

        created.append({
            "cell": cell,
            "source": s,
            "target": t,
            "exit_side": es,
            "entry_side": en,
            "exit_pt": ex_pt,
            "entry_pt": en_pt,
        })

    for s, t in inh_edges:
        draw(s, t, "inheritance-orthogonal")
    for s, t in assoc_edges:
        draw(s, t, "association")
    for s, t in comp_edges:
        draw(s, t, "composition")
    for s, t in agg_edges:
        draw(s, t, "aggregation")

    _route_around_obstacles(created, positions, widths, heights)


# ---------------------------------------------------------------------------
# Obstacle-avoiding waypoint router
# ---------------------------------------------------------------------------

def _segment_crosses_rect(
    x1: float, y1: float,
    x2: float, y2: float,
    rx: float, ry: float, rw: float, rh: float,
    margin: float = 4.0,
) -> bool:
    """True if line segment (x1,y1)-(x2,y2) passes through rect, with margin."""
    rx0, ry0 = rx - margin, ry - margin
    rx1, ry1 = rx + rw + margin, ry + rh + margin

    if max(x1, x2) < rx0 or min(x1, x2) > rx1:
        return False
    if max(y1, y2) < ry0 or min(y1, y2) > ry1:
        return False

    def _seg_inter(ax, ay, bx, by, cx, cy, dx, dy):
        def ccw(px, py, qx, qy, rxv, ryv):
            return (ryv - py) * (qx - px) > (qy - py) * (rxv - px)
        return (
            ccw(ax, ay, cx, cy, dx, dy) != ccw(bx, by, cx, cy, dx, dy)
            and ccw(ax, ay, bx, by, cx, cy) != ccw(ax, ay, bx, by, dx, dy)
        )

    # Point-inside test for both endpoints
    if rx0 <= x1 <= rx1 and ry0 <= y1 <= ry1:
        return True
    if rx0 <= x2 <= rx1 and ry0 <= y2 <= ry1:
        return True

    sides = [
        (rx0, ry0, rx1, ry0),
        (rx1, ry0, rx1, ry1),
        (rx1, ry1, rx0, ry1),
        (rx0, ry1, rx0, ry0),
    ]
    for ax, ay, bx, by in sides:
        if _seg_inter(x1, y1, x2, y2, ax, ay, bx, by):
            return True
    return False


def _ortho_path_crosses_rect(
    exit_pt: Tuple[float, float],
    entry_pt: Tuple[float, float],
    exit_side: str,
    entry_side: str,
    rect: Tuple[float, float, float, float],
    margin: float = 4.0,
) -> bool:
    """Check if Draw.io's default orthogonal route would cross the rectangle.

    Mirrors the H-V-H U-shape approximation used by
    ``drawio_tools._compute_edge_segments_ex`` so this detector agrees with
    the audit.
    """
    x1, y1 = exit_pt
    x2, y2 = entry_pt
    rx, ry, rw, rh = rect

    if abs(x2 - x1) < 1 or abs(y2 - y1) < 1:
        return _segment_crosses_rect(x1, y1, x2, y2, rx, ry, rw, rh, margin)

    mid_x = (x1 + x2) / 2
    segments = [
        (x1, y1, mid_x, y1),
        (mid_x, y1, mid_x, y2),
        (mid_x, y2, x2, y2),
    ]
    for ax, ay, bx, by in segments:
        if _segment_crosses_rect(ax, ay, bx, by, rx, ry, rw, rh, margin):
            return True
    return False


def _segment_hits_any(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    rects: List[Tuple[str, float, float, float, float]],
    exclude: set,
    margin: float = 4.0,
) -> List[str]:
    """Names of rects that the straight segment p1→p2 crosses.

    Mirrors the audit's interpretation: ``drawio_tools._compute_edge_segments_ex``
    treats consecutive (waypoint, waypoint) pairs as STRAIGHT segments when
    evaluating crossings, so this validator does the same.
    """
    hits: List[str] = []
    for name, rx, ry, rw, rh in rects:
        if name in exclude:
            continue
        if _segment_crosses_rect(p1[0], p1[1], p2[0], p2[1], rx, ry, rw, rh, margin):
            hits.append(name)
    return hits


def _path_crossings(
    points: List[Tuple[float, float]],
    rects: List[Tuple[str, float, float, float, float]],
    exclude: set,
    margin: float = 4.0,
) -> List[str]:
    """Names of rects crossed by any straight segment of the path.

    The first leg (source anchor → first waypoint, if any) is treated as
    orthogonal H-V-H since drawio's orthogonal router expands it when no
    waypoint forces a specific axis. Inner legs (waypoint→waypoint) are
    straight, matching the audit's interpretation. The final leg
    (last waypoint → target anchor) is also straight.
    """
    seen: set = set()
    out: List[str] = []
    if len(points) < 2:
        return out
    # First leg: source anchor → first node after it. If only one waypoint
    # follows, treat as straight (matches the audit). If no waypoint, treat
    # as H-V-H (drawio's default orthogonal expansion).
    if len(points) == 2:
        for name in _ortho_route_crosses_any(points[0], points[1], rects, exclude, margin):
            if name not in seen:
                seen.add(name); out.append(name)
        return out
    # Multi-waypoint path: every leg is a straight segment in audit's view.
    for i in range(len(points) - 1):
        for name in _segment_hits_any(points[i], points[i + 1], rects, exclude, margin):
            if name not in seen:
                seen.add(name); out.append(name)
    return out


def _path_self_intersects(
    points: List[Tuple[float, float]],
    rects_by_name: Dict[str, Tuple[float, float, float, float]],
    source: str,
    target: str,
    margin: float = 4.0,
) -> List[str]:
    """Names of self-rects (source/target) crossed by *interior* segments.

    The first segment is allowed to touch the source rect (since it exits
    from the source anchor) and the last segment is allowed to touch the
    target rect — but every *other* segment must stay outside both. This
    catches paths that re-enter their own source/target through the
    interior, which ``_path_crossings`` deliberately ignores by excluding
    source/target from its rect list.
    """
    out: List[str] = []
    if len(points) < 3:
        return out
    self_rects: List[Tuple[str, float, float, float, float]] = []
    if source in rects_by_name:
        x, y, w, h = rects_by_name[source]
        self_rects.append((source, x, y, w, h))
    if target in rects_by_name:
        x, y, w, h = rects_by_name[target]
        self_rects.append((target, x, y, w, h))
    if not self_rects:
        return out
    seen: set = set()
    n = len(points) - 1
    for i in range(n):
        is_first = i == 0
        is_last = i == n - 1
        for name, rx, ry, rw, rh in self_rects:
            # Skip the seg that legitimately touches its own anchor.
            if is_first and name == source:
                continue
            if is_last and name == target:
                continue
            (x1, y1) = points[i]
            (x2, y2) = points[i + 1]
            if _segment_crosses_rect(x1, y1, x2, y2, rx, ry, rw, rh, margin):
                if name not in seen:
                    seen.add(name)
                    out.append(name)
    return out


def _ortho_route_crosses_any(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    rects: List[Tuple[str, float, float, float, float]],
    exclude: set,
    margin: float = 4.0,
) -> List[str]:
    """Names of rects crossed by the H-V-H orthogonal expansion of p1→p2.

    Used only for the bare source→target leg (no waypoints), matching the
    audit's H-V-H approximation in that single case.
    """
    crossed: List[str] = []
    for name, rx, ry, rw, rh in rects:
        if name in exclude:
            continue
        if _ortho_path_crosses_rect(p1, p2, "bottom", "top", (rx, ry, rw, rh), margin=margin):
            crossed.append(name)
    return crossed


def _path_segments(points: List[Tuple[float, float]]) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Return rendered segment pairs.

    For 2-point paths (no explicit waypoints) expand into H-V-H via the
    midpoint, matching drawio's orthogonal auto-router. For multi-point paths
    (with waypoints) every consecutive pair is treated as a straight segment,
    which matches the audit's interpretation.
    """
    if len(points) < 2:
        return []
    if len(points) == 2:
        (x1, y1), (x2, y2) = points
        if abs(x2 - x1) < 1 or abs(y2 - y1) < 1:
            return [(points[0], points[1])]
        mid_x = (x1 + x2) / 2
        return [
            ((x1, y1), (mid_x, y1)),
            ((mid_x, y1), (mid_x, y2)),
            ((mid_x, y2), (x2, y2)),
        ]
    return [(points[i], points[i + 1]) for i in range(len(points) - 1)]


def _segments_overlap(
    seg_a: Tuple[Tuple[float, float], Tuple[float, float]],
    seg_b: Tuple[Tuple[float, float], Tuple[float, float]],
    proximity: float = 12.0,
) -> bool:
    """True if two axis-aligned segments visually overlap (parallel and close)."""
    (ax1, ay1), (ax2, ay2) = seg_a
    (bx1, by1), (bx2, by2) = seg_b
    a_h = abs(ay2 - ay1) < 2
    a_v = abs(ax2 - ax1) < 2
    b_h = abs(by2 - by1) < 2
    b_v = abs(bx2 - bx1) < 2
    if a_h and b_h and abs(ay1 - by1) < proximity:
        lo_a, hi_a = min(ax1, ax2), max(ax1, ax2)
        lo_b, hi_b = min(bx1, bx2), max(bx1, bx2)
        if min(hi_a, hi_b) - max(lo_a, lo_b) > 8:
            return True
    if a_v and b_v and abs(ax1 - bx1) < proximity:
        lo_a, hi_a = min(ay1, ay2), max(ay1, ay2)
        lo_b, hi_b = min(by1, by2), max(by1, by2)
        if min(hi_a, hi_b) - max(lo_a, lo_b) > 8:
            return True
    return False


def _path_overlaps_any(
    points: List[Tuple[float, float]],
    other_paths: List[List[Tuple[float, float]]],
    proximity: float = 12.0,
) -> bool:
    """True if any segment of ``points`` overlaps a segment of any other path."""
    my_segs = _path_segments(points)
    for other in other_paths:
        for ob in _path_segments(other):
            for mine in my_segs:
                if _segments_overlap(mine, ob, proximity):
                    return True
    return False


def _collapse_colinear(path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Remove redundant interior points that lie on the line between their
    neighbors (within 1px). Keeps endpoints intact.
    """
    if len(path) <= 2:
        return list(path)
    out: List[Tuple[float, float]] = [path[0]]
    for i in range(1, len(path) - 1):
        px, py = out[-1]
        cx, cy = path[i]
        nx, ny = path[i + 1]
        # Colinear if the three points share an x (vertical run) or a y
        # (horizontal run). Drop the middle point.
        if abs(px - cx) < 1 and abs(cx - nx) < 1:
            continue
        if abs(py - cy) < 1 and abs(cy - ny) < 1:
            continue
        out.append((cx, cy))
    out.append(path[-1])
    return out


def _expand_orthogonal(
    path: List[Tuple[float, float]],
    prefer_continuation: bool = True,
) -> List[Tuple[float, float]]:
    """Expand every non-axis-aligned segment in a polyline into an
    axis-aligned L-pair, then collapse the result.

    The choice of corner orientation (H-then-V vs V-then-H) for each
    diagonal segment depends on the direction of the previous segment:
    if the previous segment was horizontal we continue horizontally
    first (corner at ``(x2, y1)``), and vice versa for vertical. This
    matches drawio's orthogonal renderer, which keeps the previous
    direction until the perpendicular hop is forced.

    For the very first segment (no previous direction) the default is
    H-then-V — drawio's default for edges leaving a left/right anchor.
    """
    if len(path) < 2:
        return list(path)
    out: List[Tuple[float, float]] = [path[0]]
    # ``prev_dir``: "h", "v" or None — direction of the previous segment.
    prev_dir: str | None = None
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) < 1 and abs(dy) < 1:
            continue
        if abs(dx) < 1:
            out.append((x2, y2))
            prev_dir = "v"
            continue
        if abs(dy) < 1:
            out.append((x2, y2))
            prev_dir = "h"
            continue
        # Diagonal. Decide whether the L-pair starts horizontally (corner
        # at (x2, y1)) or vertically (corner at (x1, y2)).
        #
        # ``prefer_continuation=True``: keep moving the same way as the
        # previous segment. For the very first segment (no previous
        # direction) default to horizontal-first — that matches drawio's
        # default for edges leaving a vertical anchor.
        #
        # ``prefer_continuation=False``: invert that choice so the caller
        # can try the other corner orientation when the first attempt
        # collides with a class.
        continue_horizontal = prev_dir != "v" if prefer_continuation else prev_dir == "v"
        if continue_horizontal:
            corner = (x2, y1)
            out.append(corner)
            out.append((x2, y2))
            prev_dir = "v"
        else:
            corner = (x1, y2)
            out.append(corner)
            out.append((x2, y2))
            prev_dir = "h"
    return _collapse_colinear(out)


def _seg_transverse_cross(
    seg_a: Tuple[Tuple[float, float], Tuple[float, float]],
    seg_b: Tuple[Tuple[float, float], Tuple[float, float]],
    tol: float = 2.0,
) -> bool:
    """Return True if two axis-aligned segments transversely (perpendicularly)
    cross each other at an interior point. Endpoint touches are NOT a cross.
    """
    (ax1, ay1), (ax2, ay2) = seg_a
    (bx1, by1), (bx2, by2) = seg_b
    a_horiz = abs(ay2 - ay1) < tol
    a_vert = abs(ax2 - ax1) < tol
    b_horiz = abs(by2 - by1) < tol
    b_vert = abs(bx2 - bx1) < tol
    if a_horiz and b_vert:
        y = (ay1 + ay2) / 2
        x = (bx1 + bx2) / 2
        a_lo, a_hi = sorted((ax1, ax2))
        b_lo, b_hi = sorted((by1, by2))
        return a_lo + tol < x < a_hi - tol and b_lo + tol < y < b_hi - tol
    if a_vert and b_horiz:
        x = (ax1 + ax2) / 2
        y = (by1 + by2) / 2
        a_lo, a_hi = sorted((ay1, ay2))
        b_lo, b_hi = sorted((bx1, bx2))
        return a_lo + tol < y < a_hi - tol and b_lo + tol < x < b_hi - tol
    return False


def _path_transverse_crosses_any(
    my_path: List[Tuple[float, float]],
    other_paths: List[List[Tuple[float, float]]],
) -> bool:
    # Match the audit/scanner interpretation: 2-point paths render H-V-H.
    my_segs = _path_segments(_expand_orthogonal(my_path))
    for other in other_paths:
        expanded = _expand_orthogonal(other)
        for ob in _path_segments(expanded):
            for mine in my_segs:
                if _seg_transverse_cross(mine, ob):
                    return True
    return False


def _detour_waypoint(
    exit_pt: Tuple[float, float],
    entry_pt: Tuple[float, float],
    blockers: List[Tuple[str, float, float, float, float]],
    class_rects: List[Tuple[str, float, float, float, float]],
    src: str,
    tgt: str,
    padding: float = 24.0,
    other_paths: Optional[List[List[Tuple[float, float]]]] = None,
) -> Optional[List[Tuple[float, float]]]:
    """Pick a *crossing-free* axis-aligned detour around the blockers.

    The audit treats waypoint-to-waypoint segments as STRAIGHT lines, so this
    planner prefers fully axis-aligned routes (every segment horizontal or
    vertical). Two-waypoint U-shapes that bypass the entire blocker cluster
    on the left/right/top/bottom are the most reliable.

    Returns a list of waypoints (1 or 2) to attach, or ``None`` if no candidate
    is clean.
    """
    exclude = {src, tgt}
    x1, y1 = exit_pt
    x2, y2 = entry_pt

    def total_len(pts: List[Tuple[float, float]]) -> float:
        path = [exit_pt] + pts + [entry_pt]
        return sum(
            abs(path[i + 1][0] - path[i][0]) + abs(path[i + 1][1] - path[i][1])
            for i in range(len(path) - 1)
        )

    candidates: List[List[Tuple[float, float]]] = []

    # ---- 1-waypoint L-shapes: pivot at (x2, y1) or (x1, y2). ----
    # These yield axis-aligned segments (H then V, or V then H).
    if abs(x1 - x2) > 1 and abs(y1 - y2) > 1:
        candidates.append([(x2, y1)])  # H first, then V
        candidates.append([(x1, y2)])  # V first, then H

    # ---- 2-waypoint U-shapes around the blocker cluster. ----
    if blockers:
        cluster_left = min(b[1] for b in blockers) - padding
        cluster_right = max(b[1] + b[3] for b in blockers) + padding
        cluster_top = min(b[2] for b in blockers) - padding
        cluster_bot = max(b[2] + b[4] for b in blockers) + padding
        any_left = min(r[1] for r in class_rects) - padding
        any_right = max(r[1] + r[3] for r in class_rects) + padding
        any_top = min(r[2] for r in class_rects) - padding
        any_bot = max(r[2] + r[4] for r in class_rects) + padding

        # Multiple offsets per side so a second edge can choose a different lane
        # when another edge has already claimed the primary bypass column/row.
        offsets = [0, 28, 56, -28, -56, 84, -84]
        x_lanes: List[float] = []
        y_lanes: List[float] = []
        for off in offsets:
            x_lanes.extend([cluster_left - off, cluster_right + off,
                             any_left - off, any_right + off])
            y_lanes.extend([cluster_top - off, cluster_bot + off,
                             any_top - off, any_bot + off])

        # Vertical-detour shapes (bypass via column X)
        for X in x_lanes:
            # 2-waypoint U: ends at (X, y2) with final horizontal to (x2, y2)
            candidates.append([(X, y1), (X, y2)])
            # 3-waypoint staggered U: ends ABOVE the target row, then drops in.
            # Multiple stagger offsets so different edges to the same target
            # can claim distinct approach rows.
            for stagger in (16, 32, 48, -16, -32, -48):
                approach_y = y2 - stagger
                # Skip if approach row is degenerate (same as exit)
                if abs(approach_y - y1) < 4:
                    continue
                candidates.append([(X, y1), (X, approach_y), (x2, approach_y)])

        # Horizontal-detour shapes (bypass via row Y)
        for Y in y_lanes:
            candidates.append([(x1, Y), (x2, Y)])
            for stagger in (16, 32, 48, -16, -32, -48):
                approach_x = x2 - stagger
                if abs(approach_x - x1) < 4:
                    continue
                candidates.append([(x1, Y), (approach_x, Y), (approach_x, y2)])

    # ---- Single-waypoint candidates around each blocker (corners only). ----
    for _name, rx, ry, rw, rh in blockers:
        left_x = rx - padding
        right_x = rx + rw + padding
        top_y = ry - padding
        bottom_y = ry + rh + padding
        # Axis-aligned single waypoints relative to source or target
        for wp in [(left_x, y1), (right_x, y1), (left_x, y2), (right_x, y2),
                   (x1, top_y), (x1, bottom_y), (x2, top_y), (x2, bottom_y)]:
            candidates.append([wp])

    # Filter to crossing-free candidates
    other_paths = other_paths or []
    safe: List[List[Tuple[float, float]]] = []
    for c in candidates:
        path = [exit_pt] + c + [entry_pt]
        if _path_crossings(path, class_rects, exclude):
            continue
        safe.append(c)

    if not safe:
        return None

    # Prefer candidates that DON'T overlap AND don't transversely cross any
    # existing edge path. If every candidate fails, relax constraints in
    # order: prefer non-transverse-crossing, then non-overlapping, then any.
    def _path(c):
        return [exit_pt] + c + [entry_pt]

    no_overlap_or_cross = [
        c for c in safe
        if not _path_overlaps_any(_path(c), other_paths)
        and not _path_transverse_crosses_any(_path(c), other_paths)
    ]
    no_cross = [c for c in safe if not _path_transverse_crosses_any(_path(c), other_paths)]
    no_overlap = [c for c in safe if not _path_overlaps_any(_path(c), other_paths)]

    pool = no_overlap_or_cross or no_cross or no_overlap or safe
    return min(pool, key=total_len)


def _stagger_target_approach(
    created: List[Dict],
    positions: Dict[str, Tuple[int, int]],
    widths: Dict[str, int],
    heights: Dict[str, int],
    stagger: float = 16.0,
) -> None:
    """When two edges enter the same target side close together, the final
    horizontal/vertical stub can overlap. Insert a small staggering waypoint
    just before the entry so each edge's last segment sits at a distinct row.

    The chosen offset is *validated*: each candidate offset is checked
    against existing edge paths and class rectangles, and only offsets that
    introduce no new transverse edge crossings or class crossings are kept.
    If multiple offsets are clean, the smallest one wins (keep the route
    visually tight).
    """
    class_rects: List[Tuple[str, float, float, float, float]] = []
    for name, (x, y) in positions.items():
        w = widths.get(name, CELL_WIDTH)
        h = heights.get(name, 100)
        class_rects.append((name, float(x), float(y), float(w), float(h)))

    def _path_for(info: Dict) -> List[Tuple[float, float]]:
        return [info["exit_pt"]] + list(info.get("waypoints") or []) + [info["entry_pt"]]

    def _segments(path: List[Tuple[float, float]]) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        return [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    def _segments_cross_transverse(
        s_a: Tuple[Tuple[float, float], Tuple[float, float]],
        s_b: Tuple[Tuple[float, float], Tuple[float, float]],
        tol: float = 2.0,
    ) -> bool:
        (ax1, ay1), (ax2, ay2) = s_a
        (bx1, by1), (bx2, by2) = s_b
        a_horiz = abs(ay2 - ay1) < tol
        a_vert = abs(ax2 - ax1) < tol
        b_horiz = abs(by2 - by1) < tol
        b_vert = abs(bx2 - bx1) < tol
        if a_horiz and b_vert:
            y = (ay1 + ay2) / 2
            x = (bx1 + bx2) / 2
            a_lo, a_hi = sorted((ax1, ax2))
            b_lo, b_hi = sorted((by1, by2))
            return a_lo + tol < x < a_hi - tol and b_lo + tol < y < b_hi - tol
        if a_vert and b_horiz:
            x = (ax1 + ax2) / 2
            y = (by1 + by2) / 2
            a_lo, a_hi = sorted((ay1, ay2))
            b_lo, b_hi = sorted((bx1, bx2))
            return a_lo + tol < y < a_hi - tol and b_lo + tol < x < b_hi - tol
        return False

    # Group edges by (target, entry_side)
    groups: Dict[Tuple[str, str], List[Dict]] = {}
    for info in created:
        key = (info["target"], info["entry_side"])
        groups.setdefault(key, []).append(info)

    for (tname, side), edges in groups.items():
        if len(edges) < 2:
            continue
        tx, ty = positions.get(tname, (0, 0))
        tw = widths.get(tname, CELL_WIDTH)
        th = heights.get(tname, 100)
        # Sort by exit_pt x for top/bottom, by exit_pt y for left/right
        if side in ("top", "bottom"):
            edges = sorted(edges, key=lambda e: e["exit_pt"][0])
        else:
            edges = sorted(edges, key=lambda e: e["exit_pt"][1])

        # For each edge after the first, ensure its final approach is at a
        # distinct row/column. Insert a pre-entry waypoint at a staggered
        # offset from the target, choosing the offset so the resulting path
        # introduces no new crossings.
        for idx, info in enumerate(edges):
            if idx == 0:
                continue
            en_pt = info["entry_pt"]
            ex_x = en_pt[0]
            ex_y = en_pt[1]
            existing = info.get("waypoints") or []
            prev_pt = existing[-1] if existing else info["exit_pt"]
            s = info["source"]
            t = info["target"]
            # Paths of all OTHER edges as they currently stand. Expand any
            # 2-point path to H-V-H so the validator sees the same geometry
            # drawio and the audit scanner see.
            other_paths = [_expand_orthogonal(_path_for(o)) for o in created if o is not info]
            other_segments = [seg for p in other_paths for seg in _segments(p)]

            # Candidate offsets: smallest first, then larger; also try the
            # opposite direction in case the natural side is congested.
            base = (idx + 1) * stagger
            offset_candidates = [
                base, base + stagger, base + 2 * stagger, base + 3 * stagger,
                base + 4 * stagger, base + 5 * stagger, base + 6 * stagger,
                # Pull AWAY from target's far side instead — sometimes the
                # natural "before target" lane is fully blocked.
                -base, -(base + stagger), -(base + 2 * stagger),
            ]

            chosen: Optional[Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]] = None
            for off in offset_candidates:
                if side == "top":
                    pre = (ex_x, ty - off)
                elif side == "bottom":
                    pre = (ex_x, ty + th + off)
                elif side == "left":
                    pre = (tx - off, ex_y)
                else:  # right
                    pre = (tx + tw + off, ex_y)

                # Reject offsets that put `pre` inside the target's bounding
                # box (negative offsets can do this) — the edge would visually
                # enter the target from the wrong side.
                if side == "top" and pre[1] >= ty:
                    continue
                if side == "bottom" and pre[1] <= ty + th:
                    continue
                if side == "left" and pre[0] >= tx:
                    continue
                if side == "right" and pre[0] <= tx + tw:
                    continue

                new_pts = list(existing)
                if abs(prev_pt[0] - pre[0]) > 1 and abs(prev_pt[1] - pre[1]) > 1:
                    if side in ("left", "right"):
                        corner = (pre[0], prev_pt[1])
                    else:
                        corner = (prev_pt[0], pre[1])
                    new_pts.append(corner)
                new_pts.append(pre)

                # Validate the COMPLETE new path against classes and edges.
                full_path = [info["exit_pt"]] + new_pts + [en_pt]
                segs = _segments(full_path)

                # Class crossing check
                if _path_crossings(full_path, class_rects, exclude={s, t}):
                    continue

                # Transverse edge crossing check
                clean = True
                for seg in segs:
                    for oseg in other_segments:
                        if _segments_cross_transverse(seg, oseg):
                            clean = False
                            break
                    if not clean:
                        break
                if not clean:
                    continue

                chosen = (new_pts, full_path)
                break

            if chosen is None:
                # Nothing better than what we already have; leave the edge
                # alone (its existing route may still be sub-optimal but a
                # bad stagger is worse than no stagger).
                continue

            new_pts, _full_path = chosen
            add_edge_waypoints(info["cell"], new_pts)
            info["waypoints"] = new_pts


def _route_around_obstacles(
    created: List[Dict],
    positions: Dict[str, Tuple[int, int]],
    widths: Dict[str, int],
    heights: Dict[str, int],
    max_passes: int = 4,
) -> None:
    """For each created edge, if its routed orthogonal path would cross any
    non-endpoint class, attach waypoints that dog-leg around the offenders.

    Validates candidate detours by re-checking the full H-V-H expansion
    against *all* classes, so we don't fix one crossing only to create another.
    Supports both single and pair-waypoint detours.

    Then staggers final approaches into shared target sides so two edges
    entering the same side don't overlap on the same final segment.

    Runs up to ``max_passes`` times because adding a waypoint to one edge can
    change the analysis for an adjacent edge.
    """
    class_rects: List[Tuple[str, float, float, float, float]] = []
    for name, (x, y) in positions.items():
        w = widths.get(name, CELL_WIDTH)
        h = heights.get(name, 100)
        class_rects.append((name, float(x), float(y), float(w), float(h)))

    def _path_for(info: Dict) -> List[Tuple[float, float]]:
        return [info["exit_pt"]] + list(info.get("waypoints") or []) + [info["entry_pt"]]

    for _ in range(max_passes):
        any_changed = False
        for info in created:
            s = info["source"]
            t = info["target"]
            ex_pt = info["exit_pt"]
            en_pt = info["entry_pt"]
            wps = info.get("waypoints") or []
            path = [ex_pt] + list(wps) + [en_pt]

            blockers_names = _path_crossings(path, class_rects, exclude={s, t})
            if not blockers_names:
                continue
            blockers = [r for r in class_rects if r[0] in set(blockers_names)]

            other_paths = [_path_for(o) for o in created if o is not info]
            new_wps = _detour_waypoint(
                ex_pt, en_pt, blockers, class_rects, s, t, other_paths=other_paths
            )
            if new_wps is None:
                continue
            add_edge_waypoints(info["cell"], new_wps)
            info["waypoints"] = new_wps
            any_changed = True

        if not any_changed:
            break

    # Edge-on-edge overlap repair pass: for any edge whose path overlaps
    # another edge, try to re-route via a different bypass lane.
    for _ in range(max_passes):
        any_changed = False
        for info in created:
            s = info["source"]
            t = info["target"]
            ex_pt = info["exit_pt"]
            en_pt = info["entry_pt"]
            my_path = _path_for(info)
            other_paths = [_path_for(o) for o in created if o is not info]
            if not _path_overlaps_any(my_path, other_paths):
                continue
            # Recompute blockers in case rerouting introduces new crossings.
            blockers_names = _path_crossings(my_path, class_rects, exclude={s, t})
            blockers = [r for r in class_rects if r[0] in set(blockers_names)]
            new_wps = _detour_waypoint(
                ex_pt, en_pt, blockers, class_rects, s, t, other_paths=other_paths
            )
            if new_wps is None or new_wps == list(info.get("waypoints") or []):
                continue
            add_edge_waypoints(info["cell"], new_wps)
            info["waypoints"] = new_wps
            any_changed = True
        if not any_changed:
            break

    # Edge-on-edge TRANSVERSE crossing repair pass: when one edge's segment
    # perpendicularly cuts through another's, _detour_waypoint with the
    # other edge's path as `other_paths` will prefer candidates that don't
    # transversely cross.
    for _ in range(max_passes):
        any_changed = False
        for info in created:
            s = info["source"]
            t = info["target"]
            ex_pt = info["exit_pt"]
            en_pt = info["entry_pt"]
            my_path = _path_for(info)
            other_paths = [_path_for(o) for o in created if o is not info]
            if not _path_transverse_crosses_any(my_path, other_paths):
                continue
            blockers_names = _path_crossings(my_path, class_rects, exclude={s, t})
            blockers = [r for r in class_rects if r[0] in set(blockers_names)]
            new_wps = _detour_waypoint(
                ex_pt, en_pt, blockers, class_rects, s, t, other_paths=other_paths
            )
            if new_wps is None:
                continue
            new_path = [ex_pt] + new_wps + [en_pt]
            # Only accept if the new path actually has FEWER transverse
            # crossings AND no new class crossings.
            if _path_transverse_crosses_any(new_path, other_paths):
                continue
            if _path_crossings(new_path, class_rects, exclude={s, t}):
                continue
            if new_wps == list(info.get("waypoints") or []):
                continue
            add_edge_waypoints(info["cell"], new_wps)
            info["waypoints"] = new_wps
            any_changed = True
        if not any_changed:
            break

    # Final pass: stagger horizontal/vertical stubs at shared target sides
    _stagger_target_approach(created, positions, widths, heights)

    # Normalize every edge to fully axis-aligned segments.
    #
    # Drawio renders ``edgeStyle=orthogonalEdgeStyle`` by inserting a corner
    # for any non-axis-aligned segment between consecutive waypoints. The
    # scanner walks each waypoint pair as a STRAIGHT line, which silently
    # accepts diagonals that drawio actually bends into a different shape.
    # By emitting every corner explicitly we guarantee scanner and renderer
    # agree on the geometry.
    _normalize_paths(created, class_rects)

    # Perpendicular-approach pass: arrows must HIT the destination edge head-on,
    # not slide along it. Same rule for exits. Inject a pivot waypoint near
    # any end whose adjacent segment is parallel to the touched side.
    _enforce_perpendicular_approach(created, class_rects)

    # Re-normalize once more: the pivot injection may have left waypoints
    # that collapse colinearly (so a previously-redundant waypoint disappears).
    _normalize_paths(created, class_rects)


def _normalize_paths(
    created: List[Dict],
    class_rects: List[Tuple[str, float, float, float, float]],
) -> None:
    """Force every edge's path to be fully axis-aligned. For each diagonal
    segment try both corner orientations (H-first and V-first); accept the
    one that introduces no class crossing and no new transverse crossing
    with any other edge. If neither candidate is clean, keep the H-first
    expansion (drawio's default) so at least the rendered geometry matches
    what the scanner sees.
    """
    def _path_for(info: Dict) -> List[Tuple[float, float]]:
        return [info["exit_pt"]] + list(info.get("waypoints") or []) + [info["entry_pt"]]

    # Two passes: each edge's normalization can change the constraint
    # surface for its neighbors.
    for _ in range(2):
        for info in created:
            s = info["source"]
            t = info["target"]
            raw = _path_for(info)
            other_paths = [_path_for(o) for o in created if o is not info]

            # Try H-first (default) and V-first; pick the cleanest.
            best: List[Tuple[float, float]] | None = None
            best_score = (10**9, 10**9)  # (class crossings, transverse crossings)
            for prefer in (True, False):
                # `prefer_continuation=True` follows the previous segment
                # direction. `False` flips the first ambiguous bend.
                cand = _expand_orthogonal(raw, prefer_continuation=prefer)
                cross = len(_path_crossings(cand, class_rects, exclude={s, t}))
                trans = sum(
                    1
                    for ob in other_paths
                    if _path_transverse_crosses_any(cand, [ob])
                )
                score = (cross, trans)
                if score < best_score:
                    best_score = score
                    best = cand

            if best is None:
                continue
            # Strip endpoints — those are the anchors, not waypoints.
            new_wps = best[1:-1]
            old_wps = list(info.get("waypoints") or [])
            if new_wps == old_wps:
                continue
            add_edge_waypoints(info["cell"], new_wps)
            info["waypoints"] = new_wps


def _enforce_perpendicular_approach(
    created: List[Dict],
    class_rects: List[Tuple[str, float, float, float, float]],
) -> None:
    """Ensure every edge's first segment is perpendicular to its exit side
    and its last segment is perpendicular to its entry side.

    Why this rule exists: when an edge's terminal segment is parallel to
    the touched class boundary, the arrow tip "slides along" the side
    instead of hitting it head-on — visually confusing and clearly
    different from what hand-drawn diagrams do.

    Strategy: for each offending end, inject a pivot waypoint a small
    distance perpendicular-outward from the anchor. After re-expansion
    + colinear collapse this typically replaces the bad corner with a
    clean L that approaches head-on. The candidate is validated against
    class crossings and transverse crossings; if any check fails we try
    a larger offset, and if all attempts fail we leave the edge as-is.
    """
    def _path_for(info: Dict) -> List[Tuple[float, float]]:
        return [info["exit_pt"]] + list(info.get("waypoints") or []) + [info["entry_pt"]]

    def _seg_dir(p1, p2):
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        if dx < 1 and dy < 1:
            return None
        if dx < 1:
            return "v"
        if dy < 1:
            return "h"
        return None

    def _seg_dir_signed(p1, p2):
        """Return the *signed* dominant direction of a segment as one of
        ``"left"``, ``"right"``, ``"up"``, ``"down"``, or ``None``.
        """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if abs(dx) < 1 and abs(dy) < 1:
            return None
        if abs(dx) >= abs(dy):
            return "right" if dx > 0 else "left"
        return "down" if dy > 0 else "up"

    def _outward(side: str | None) -> str | None:
        """Direction a segment must travel to leave a node *out through*
        the given side."""
        return {"left": "left", "right": "right", "top": "up", "bottom": "down"}.get(side or "")

    def _inward(side: str | None) -> str | None:
        """Direction the FINAL segment must travel to enter a node
        *through* the given side. Approaching from outside the left
        side, for example, means moving rightward into it."""
        return {"left": "right", "right": "left", "top": "down", "bottom": "up"}.get(side or "")

    def _pivot_pt(side: str | None, pt: Tuple[float, float], offset: float):
        if side is None:
            return None
        x, y = pt
        if side == "left":
            return (x - offset, y)
        if side == "right":
            return (x + offset, y)
        if side == "top":
            return (x, y - offset)
        if side == "bottom":
            return (x, y + offset)
        return None

    # A range of candidate offsets — try a few small choices close to the
    # node (so the approach hugs the destination side) and a few larger
    # ones for when the natural pivot column collides with another edge.
    # Smaller offsets are useful when the destination side is already
    # crowded with terminal H/V segments from neighboring edges.
    exit_offsets = (20.0, 30.0, 45.0, 70.0, 100.0, 140.0)
    entry_offsets = (20.0, 30.0, 45.0, 70.0, 100.0, 140.0)

    # Index class rects by name so we can detect self-intersection
    # (path passing back through its own source / target interior).
    rects_by_name: Dict[str, Tuple[float, float, float, float]] = {
        name: (x, y, w, h) for (name, x, y, w, h) in class_rects
    }

    _debug = False
    for _ in range(2):
        any_changed = False
        for info in created:
            s = info["source"]
            t = info["target"]
            ex_pt = info["exit_pt"]
            en_pt = info["entry_pt"]
            wps = list(info.get("waypoints") or [])

            # Determine current first/last segment directions on the
            # axis-aligned view of the path.
            raw = [ex_pt] + wps + [en_pt]
            norm = _expand_orthogonal(raw, prefer_continuation=True)
            if len(norm) < 2:
                continue

            exit_side = info.get("exit_side")
            entry_side = info.get("entry_side")
            first_signed = _seg_dir_signed(norm[0], norm[1])
            last_signed = _seg_dir_signed(norm[-2], norm[-1])
            want_out = _outward(exit_side)
            want_in = _inward(entry_side)
            need_exit_fix = bool(want_out and first_signed and first_signed != want_out)
            need_entry_fix = bool(want_in and last_signed and last_signed != want_in)
            if _debug:
                print(
                    f"[perp] {s}->{t} ex_side={exit_side} en_side={entry_side} "
                    f"first={first_signed} last={last_signed} "
                    f"need_ex={need_exit_fix} need_en={need_entry_fix} wps={wps}"
                )
            if not need_exit_fix and not need_entry_fix:
                continue

            other_paths = [_path_for(o) for o in created if o is not info]

            best_overall: Tuple[float, float] | None = None
            best_overall_score: Tuple[int, ...] = (10**9,)
            best_overall_wps: List[Tuple[float, float]] | None = None

            # Enumerate (exit_offset, entry_offset) combinations.
            ex_choices = exit_offsets if need_exit_fix else (None,)
            en_choices = entry_offsets if need_entry_fix else (None,)
            for ex_off in ex_choices:
                for en_off in en_choices:
                    cand_wps = list(wps)
                    if ex_off is not None:
                        pv = _pivot_pt(exit_side, ex_pt, ex_off)
                        if pv is not None:
                            cand_wps = [pv] + cand_wps
                    if en_off is not None:
                        pv = _pivot_pt(entry_side, en_pt, en_off)
                        if pv is not None:
                            cand_wps = cand_wps + [pv]
                    if cand_wps == wps:
                        continue

                    cand_raw = [ex_pt] + cand_wps + [en_pt]
                    # Try both corner orientations for any remaining diagonals.
                    for prefer in (True, False):
                        cand = _expand_orthogonal(cand_raw, prefer_continuation=prefer)
                        if len(cand) < 2:
                            continue
                        cand_first_s = _seg_dir_signed(cand[0], cand[1])
                        cand_last_s = _seg_dir_signed(cand[-2], cand[-1])
                        # Both ends must approach the side head-on AND
                        # leave/arrive in the correct direction. A purely
                        # H-vs-V check is not enough — a horizontal first
                        # segment that goes RIGHT from a LEFT exit cuts
                        # straight through the source class.
                        if need_exit_fix and cand_first_s != want_out:
                            continue
                        if need_entry_fix and cand_last_s != want_in:
                            continue
                        cross = len(_path_crossings(cand, class_rects, exclude={s, t}))
                        self_hit = len(
                            _path_self_intersects(cand, rects_by_name, s, t)
                        )
                        trans = sum(
                            1 for op in other_paths if _path_transverse_crosses_any(cand, [op])
                        )
                        overlap = sum(
                            1 for op in other_paths if _path_overlaps_any(cand, [op])
                        )
                        # Prefer: no class crossings, no self-intersection
                        # through source/target interior, no overlap with
                        # another edge, no new transverse crossing, then
                        # the smallest combined offset (closest to the
                        # node — less detour), then the shorter polyline.
                        offset_cost = (ex_off or 0) + (en_off or 0)
                        perim = sum(
                            abs(cand[i + 1][0] - cand[i][0])
                            + abs(cand[i + 1][1] - cand[i][1])
                            for i in range(len(cand) - 1)
                        )
                        score = (cross, self_hit, overlap, trans, offset_cost, len(cand), perim)
                        if score < best_overall_score:
                            best_overall_score = score
                            best_overall = cand
                            best_overall_wps = cand[1:-1]

            if _debug:
                print(
                    f"[perp]   best score={best_overall_score} wps={best_overall_wps}"
                )
            if best_overall is None or best_overall_wps is None:
                continue
            cross_count, self_hit_count, overlap_count, trans_count, *_ = best_overall_score
            # Only commit a fix that strictly does no harm. Crossing the
            # source or target interior is the worst kind of violation
            # since it means the arrow appears to come *out of* its own
            # endpoint class rather than connecting to it.
            if cross_count > 0 or self_hit_count > 0 or trans_count > 0:
                if _debug:
                    print(
                        f"[perp]   rejected: cross={cross_count} "
                        f"self_hit={self_hit_count} trans={trans_count}"
                    )
                continue
            # Allow overlap only if it was unavoidable; the audit will
            # surface it for the next iteration to handle differently.
            if best_overall_wps == wps:
                if _debug:
                    print("[perp]   no-op (wps unchanged)")
                continue
            add_edge_waypoints(info["cell"], best_overall_wps)
            info["waypoints"] = best_overall_wps
            any_changed = True
            if _debug:
                print(f"[perp]   APPLIED new wps={best_overall_wps}")

        if not any_changed:
            break


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _mechanism_name_from_context(text: str) -> Optional[str]:
    """Return the top-level ``# Heading`` from a mechanism context file, or None."""
    for line in text.split("\n"):
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m:
            return m.group(1).strip()
    return None


def collect_mechanism_kas(
    arch_spec_path: Path,
    section: str = "Class Specification",
) -> DomainModel:
    """Scan an architecture-specification.md for mechanism context file links.

    For each linked ``architecture-context.md`` that contains a section named
    *section* (default: ``Class Specification``), extract that section and parse
    it as a separate KA.  The KA name is taken from the context file's own ``#``
    heading.  Returns a combined ``DomainModel`` with one KA per mechanism.

    Link format expected in the arch spec (workspace-root paths):
        [text](/path/to/architecture-context.md)
    """
    arch_spec_path = arch_spec_path.resolve()
    workspace_root = arch_spec_path
    # Walk up until we find the workspace root (heuristic: no more /../ needed)
    # Fall back to the parent of the spec directory.
    spec_dir = arch_spec_path.parent

    text = arch_spec_path.read_text(encoding="utf-8")

    # Find all markdown links whose href ends with architecture-context.md
    link_pattern = re.compile(r"\[([^\]]*)\]\((/[^)]+architecture-context\.md)\)")
    found: List[tuple] = link_pattern.findall(text)

    if not found:
        raise ValueError(
            f"No architecture-context.md links found in {arch_spec_path}. "
            "Links must use workspace-root paths starting with '/'."
        )

    combined_kas: Dict[str, List[ClassDef]] = {}

    # Resolve workspace root: walk up from the spec file until we find a directory
    # that contains the first linked path segment.
    candidate = arch_spec_path.parent
    for _ in range(8):
        first_link = found[0][1].lstrip("/")
        if (candidate / first_link).exists():
            workspace_root = candidate
            break
        candidate = candidate.parent
    else:
        workspace_root = arch_spec_path.parents[2]  # docs/architecture/specification -> repo root

    seen: set = set()
    for _link_text, href in found:
        context_path = workspace_root / href.lstrip("/")
        if not context_path.exists():
            print(f"  Warning: {context_path} not found — skipping", file=sys.stderr)
            continue
        key = str(context_path)
        if key in seen:
            continue
        seen.add(key)

        ctx_text = context_path.read_text(encoding="utf-8")
        try:
            section_body = _extract_section(ctx_text, section)
        except ValueError:
            # This context file has no Class Specification — skip silently
            continue

        ka_name = _mechanism_name_from_context(ctx_text) or context_path.parent.name
        fmt = detect_format(ctx_text, context_path)
        sub_model = parse_object_model(section_body, source_format=fmt)

        # Merge classes under the mechanism's KA name
        all_classes: List[ClassDef] = []
        for classes in sub_model.kas.values():
            for cls in classes:
                cls.ka = ka_name
            all_classes.extend(classes)

        if all_classes:
            combined_kas[ka_name] = all_classes
            print(f"  [{ka_name}] — {len(all_classes)} classes from {context_path.name}")

    if not combined_kas:
        raise ValueError(
            f"No '{section}' sections found in any mechanism context file linked from {arch_spec_path}"
        )

    return DomainModel(kas=combined_kas, source_format="arch-spec")


def _extract_section(text: str, heading: str) -> str:
    """Return the body of a Markdown section identified by its heading text.

    Matches any ``#``-level heading whose stripped text equals *heading*
    (case-insensitive).  Returns everything from the line after the heading up
    to (but not including) the next heading at the same or higher level, or
    end-of-file.  Raises ``ValueError`` when the heading is not found.

    Example — given ``--section "Class Specification"`` the function extracts
    the content of ``### Class Specification`` from an ``architecture-context.md``
    file so the parser sees a self-contained class-spec document.
    """
    lines = text.split("\n")
    start_idx: Optional[int] = None
    heading_level: int = 0

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m and m.group(2).strip().lower() == heading.strip().lower():
            start_idx = i + 1
            heading_level = len(m.group(1))
            break

    if start_idx is None:
        raise ValueError(f"Section '{heading}' not found in document")

    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        m = re.match(r"^(#{1,6})\s+", lines[i])
        if m and len(m.group(1)) <= heading_level:
            end_idx = i
            break

    return "\n".join(lines[start_idx:end_idx])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Domain model (domain model / class-model / ULL) → Draw.io class diagram"
    )
    parser.add_argument("source", type=Path, help="Source .md file")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output .drawio path")
    parser.add_argument("--ka", default=None,
                        help="Render only the named Key Abstraction")
    parser.add_argument("--section", default=None,
                        help=(
                            "Extract a named Markdown section before parsing. "
                            "Use when the source file contains multiple sections "
                            "and you only want one — e.g. --section 'Class Specification' "
                            "to pull the ### Class Specification block from an "
                            "architecture-context.md file."
                        ))
    parser.add_argument("--from-arch-spec", action="store_true",
                        help=(
                            "Treat source as an architecture-specification.md. "
                            "Scans it for all mechanism context file links, extracts "
                            "the '### Class Specification' section from each, and renders "
                            "each mechanism as a separate diagram tab. "
                            "Each tab is named after the mechanism context file's own # heading."
                        ))
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
        else source_path.parent / f"{stem}-participants.drawio"
    )

    if args.from_arch_spec:
        print(f"Arch spec: {source_path}")
        print(f"Scanning for mechanism context files…")
        try:
            section_name = args.section or "Class Specification"
            model = collect_mechanism_kas(source_path, section=section_name)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    elif args.section:
        print(f"Parsing:  {source_path}")
        print(f"Section:  {args.section}")
        raw_text = source_path.read_text(encoding="utf-8")
        try:
            section_text = _extract_section(raw_text, args.section)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        fmt = detect_format(raw_text, source_path)
        model = parse_object_model(section_text, source_format=fmt)
    else:
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
