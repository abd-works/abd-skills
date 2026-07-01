"""TypeScript emitter for the domain-graph → code bootstrap.

Used exclusively by the one-shot ``domain_graph_cli.py generate`` command. Never
overwrites existing files; the CLI is the last-write-only path (D22). After
bootstrap the AI edits the emitted files directly — the emitter is not run
again against the same tree.

Emits one file per Key Abstraction: ``<out>/<module-slug>/<ka-slug>.ts``.
Boundary classes go under ``<out>/<module-slug>/boundary/<class-slug>.ts``.

Two fidelities are supported (D26):

- ``model``         — real types only; no @stereotype, no @composition, no
                      invariant/interaction methods, no @initialisation.
- ``specification`` — everything ``model`` produces, plus @stereotype,
                      @composition/@aggregation/@association tags,
                      @initialisation, @invariant methods, @interaction
                      methods, and //region banners for phase grouping.

Legacy free-text invariants from markdown-derived graphs are converted to empty
methods whose names are camelCase slugs of the invariant text. The original
prose is preserved in a ``// TODO: rename`` comment so the AI can pick a
tighter name post-bootstrap.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


# ---------------------------------------------------------------------------
# Case helpers
# ---------------------------------------------------------------------------


_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*")


def _words(text: str) -> List[str]:
    return _WORD_RE.findall(text or "")


def to_kebab_case(name: str) -> str:
    """PascalCase / camelCase / Title Case → kebab-case."""
    if not name:
        return ""
    # Split camel/pascal boundaries, then split on non-alnum, then join.
    step1 = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name)
    step2 = re.sub(r"[^A-Za-z0-9]+", "-", step1)
    return step2.strip("-").lower()


def to_camel_case(text: str, *, max_words: int = 10) -> str:
    """Free text → camelCase identifier. Truncates to ``max_words`` words."""
    ws = _words(text)[:max_words]
    if not ws:
        return ""
    head = ws[0].lower()
    tail = "".join(w[:1].upper() + w[1:].lower() for w in ws[1:])
    return head + tail


def to_pascal_case(text: str) -> str:
    ws = _words(text)
    return "".join(w[:1].upper() + w[1:].lower() for w in ws)


# ---------------------------------------------------------------------------
# Type extraction — walk any type string and pull referenced type names.
# ---------------------------------------------------------------------------


_BUILTIN_TS_TYPES = frozenset(
    {
        "string",
        "number",
        "boolean",
        "void",
        "any",
        "unknown",
        "never",
        "null",
        "undefined",
        "Date",
        "Object",
        # Legacy domain-model PascalCase primitives — treated as builtins so we
        # don't emit spurious import placeholders. Rendered as lowercase in TS.
        "Boolean",
        "Integer",
        "Number",
        "String",
    }
)


_PRIMITIVE_ALIASES = {
    "Boolean": "boolean",
    "Integer": "number",
    "Number": "number",
    "String": "string",
}


def _referenced_type_names(type_string: str) -> Set[str]:
    """Return the set of PascalCase type names referenced in ``type_string``.

    Handles ``List<Foo>``, ``Dictionary<Key, Value>``, arrays, unions, etc. Only
    picks identifiers that start with an uppercase letter so we don't grab
    parameter names or built-in scalars.
    """
    names: Set[str] = set()
    if not type_string:
        return names
    for match in _WORD_RE.findall(type_string):
        if match[:1].isupper() and match not in _BUILTIN_TS_TYPES:
            names.add(match)
    return names


def _ts_render_type(type_string: str) -> str:
    """Map graph type strings to TypeScript type strings.

    ``List<X>`` → ``X[]``, ``Dictionary<K, V>`` → ``Record<K, V>``. Everything
    else is passed through unchanged; the AI will clean up any awkward
    residue post-bootstrap.
    """
    if not type_string:
        return "unknown"
    out = type_string.strip()
    # List<X> → X[]
    out = re.sub(r"\bList\s*<\s*([^<>,]+)\s*>", r"\1[]", out)
    # Dictionary<K,V> → Record<K, V>
    out = re.sub(
        r"\bDictionary\s*<\s*([^<>,]+)\s*,\s*([^<>,]+)\s*>",
        r"Record<\1, \2>",
        out,
    )
    # Legacy PascalCase primitives → TS lowercase primitives
    for legacy, ts in _PRIMITIVE_ALIASES.items():
        out = re.sub(rf"\b{legacy}\b", ts, out)
    return out


# ---------------------------------------------------------------------------
# Node walkers
# ---------------------------------------------------------------------------


def _iter_class_body_types(cls: Dict[str, Any]) -> Iterable[str]:
    ctor = cls.get("constructor") or {}
    for p in ctor.get("parameters", []) or []:
        yield p.get("type", "")
    for prop in cls.get("properties", []) or []:
        if str(prop.get("name", "")).strip() == "Invariant":
            continue  # parser artifact — skip
        yield prop.get("return_type", "")
    for op in cls.get("operations", []) or []:
        yield op.get("return_type", "")
        for pt in op.get("parameter_types", []) or []:
            yield pt
        for p in op.get("parameters", []) or []:
            yield p.get("type", "")
    parent = cls.get("extends")
    if parent:
        yield parent


def _all_referenced_types(classes: Sequence[Dict[str, Any]]) -> Set[str]:
    names: Set[str] = set()
    for cls in classes:
        for t in _iter_class_body_types(cls):
            names.update(_referenced_type_names(t))
        # Exclude self-references
        self_name = cls.get("name", "")
        if self_name in names:
            names.discard(self_name)
    return names


# ---------------------------------------------------------------------------
# Invariant / interaction name derivation
# ---------------------------------------------------------------------------


def _invariant_name(text: str, index: int, seen: Set[str]) -> str:
    """Derive a unique camelCase method name from a free-text invariant."""
    base = to_camel_case(text, max_words=10) if text else ""
    if not base:
        base = f"invariant{index}"
    candidate = base
    n = 2
    while candidate in seen:
        candidate = f"{base}{n}"
        n += 1
    seen.add(candidate)
    return candidate


def _interaction_name(op_name: str, index: int, seen: Set[str]) -> str:
    base = to_camel_case(op_name + " interaction", max_words=10) if op_name else f"interaction{index}"
    candidate = base
    n = 2
    while candidate in seen:
        candidate = f"{base}{n}"
        n += 1
    seen.add(candidate)
    return candidate


def _interaction_text_summary(interaction: Any) -> str:
    """Flatten a structured interaction into a single-line summary comment."""
    if interaction is None:
        return ""
    if isinstance(interaction, str):
        return interaction.strip()
    if isinstance(interaction, list):
        pieces: List[str] = []
        for step in interaction:
            if isinstance(step, str):
                pieces.append(step.strip())
            elif isinstance(step, dict):
                if "operation" in step:
                    obj = step.get("object", "")
                    op = step.get("operation", "")
                    pieces.append(f"{obj}.{op}(…)".lstrip("."))
                elif "property" in step:
                    pieces.append(str(step.get("property", "")))
                elif "return" in step:
                    pieces.append(f"return {step.get('return')}")
        return " → ".join(p for p in pieces if p)
    return ""


# ---------------------------------------------------------------------------
# Rendering — one class → TypeScript block
# ---------------------------------------------------------------------------


def _render_property(prop: Dict[str, Any], *, fidelity: str) -> List[str]:
    name = prop.get("name", "")
    rtype = _ts_render_type(prop.get("return_type", ""))
    lines: List[str] = []
    tag = _relationship_tag_from_note(prop.get("note", ""))
    if fidelity == "specification" and tag:
        lines.append(f"  /** @{tag} */")
    lines.append(f"  abstract {name}: {rtype}")
    return lines


def _relationship_tag_from_note(note: str) -> str:
    """Detect legacy ``<< composition >>`` / stereotype notes on properties."""
    if not note:
        return ""
    low = note.lower()
    if "composition" in low:
        return "composition"
    if "aggregation" in low:
        return "aggregation"
    if "association" in low:
        return "association"
    return ""


def _render_operation(op: Dict[str, Any]) -> str:
    name = op.get("name", "")
    rtype = _ts_render_type(op.get("return_type", "void"))
    parameters = op.get("parameters") or []
    if parameters:
        params = ", ".join(
            f"{p.get('name', 'arg')}: {_ts_render_type(p.get('type', 'unknown'))}"
            for p in parameters
        )
    else:
        params = ", ".join(
            f"arg{i + 1}: {_ts_render_type(t)}"
            for i, t in enumerate(op.get("parameter_types") or [])
        )
    return f"  abstract {name}({params}): {rtype}"


def _group_operations_by_phase(operations: Sequence[Dict[str, Any]]) -> List[Tuple[str, List[Dict[str, Any]]]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    order: List[str] = []
    for op in operations:
        phase = str(op.get("phase") or "").strip()
        if phase not in groups:
            groups[phase] = []
            order.append(phase)
    for op in operations:
        phase = str(op.get("phase") or "").strip()
        groups[phase].append(op)
    return [(phase, groups[phase]) for phase in order]


def _is_parser_invariant_artifact(prop: Dict[str, Any]) -> bool:
    """Detect a legacy Phase-1 parser artifact where an ``Invariant:`` line was
    captured as a property named ``Invariant`` with the constraint text as its
    return type. Emit these as class-level invariant methods instead."""
    return str(prop.get("name", "")).strip() == "Invariant"


def _extract_stray_invariant_prose(props: Sequence[Dict[str, Any]]) -> List[str]:
    """Pull free-text invariant strings from parser-artifact ``Invariant`` properties."""
    out: List[str] = []
    for p in props:
        if _is_parser_invariant_artifact(p):
            rt = str(p.get("return_type", "")).strip()
            if rt:
                out.append(rt)
    return out


def _real_properties(props: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [p for p in props if not _is_parser_invariant_artifact(p)]


def _render_class(cls: Dict[str, Any], *, fidelity: str) -> List[str]:
    lines: List[str] = []
    name = cls.get("name", "UnnamedClass")
    parent = cls.get("extends")
    header = f"export abstract class {name}"
    if parent:
        header += f" extends {parent}"
    header += " {"

    # JSDoc: stereotype, initialisation (spec fidelity only)
    if fidelity == "specification":
        tags: List[str] = []
        st = cls.get("stereotype")
        if st:
            tags.append(f" * @stereotype {st}")
        init = cls.get("initialisation")
        if init:
            tags.append(f" * @initialisation {init}")
        if tags:
            lines.append("/**")
            lines.extend(tags)
            lines.append(" */")

    lines.append(header)

    # Constructor
    ctor = cls.get("constructor") or {}
    ctor_params = ctor.get("parameters") or []
    if ctor_params:
        params = ", ".join(
            f"{p.get('name', 'arg')}: {_ts_render_type(p.get('type', 'unknown'))}"
            for p in ctor_params
        )
        lines.append(f"  constructor({params}) {{")
        for p in ctor_params:
            lines.append(f"    void {p.get('name', 'arg')}")
        lines.append("  }")
        lines.append("")

    # Properties (filter out parser-artifact Invariant pseudo-properties)
    all_props = cls.get("properties") or []
    stray_invariants = _extract_stray_invariant_prose(all_props)
    props = _real_properties(all_props)
    for prop in props:
        lines.extend(_render_property(prop, fidelity=fidelity))
    if props:
        lines.append("")

    # Operations, grouped by phase at spec fidelity
    ops = cls.get("operations") or []
    if fidelity == "specification":
        grouped = _group_operations_by_phase(ops)
        for phase, group in grouped:
            if phase:
                lines.append(f"  //region {phase}")
            for op in group:
                lines.append(_render_operation(op))
            if phase:
                lines.append(f"  //endregion")
                lines.append("")
    else:
        for op in ops:
            lines.append(_render_operation(op))
        if ops:
            lines.append("")

    # Invariant methods (spec fidelity only, from legacy free-text)
    if fidelity == "specification":
        seen_invariants: Set[str] = set()
        counter = 1
        invariant_lines: List[str] = []

        def emit_invariant(text: str) -> None:
            nonlocal counter
            mname = _invariant_name(text, counter, seen_invariants)
            counter += 1
            invariant_lines.append(f"  // TODO: rename — original: {text}")
            invariant_lines.append(f"  /** @invariant */")
            invariant_lines.append(f"  abstract {mname}(): void")
            invariant_lines.append("")

        for prop in props:
            for inv in prop.get("invariants") or []:
                emit_invariant(inv)
        for op in ops:
            for inv in op.get("invariants") or []:
                emit_invariant(inv)
        for stray in stray_invariants:
            emit_invariant(stray)
        if invariant_lines:
            lines.append("  //region Invariants — names derived from legacy prose; rename to tight names (D24)")
            lines.extend(invariant_lines)
            lines.append("  //endregion")
            lines.append("")

    # Interaction methods (spec fidelity only)
    if fidelity == "specification":
        seen_inter: Set[str] = set()
        counter = 1
        interaction_lines: List[str] = []
        for op in ops:
            interaction = op.get("interaction")
            if interaction:
                mname = _interaction_name(op.get("name", "operation"), counter, seen_inter)
                counter += 1
                summary = _interaction_text_summary(interaction)
                if summary:
                    interaction_lines.append(f"  // TODO: move narrative to domain-context.md — original: {summary}")
                interaction_lines.append(f"  /** @interaction */")
                interaction_lines.append(f"  abstract {mname}(): void")
                interaction_lines.append("")
        if interaction_lines:
            lines.append("  //region Interactions — names derived from legacy operations; rename to tight names (D24)")
            lines.extend(interaction_lines)
            lines.append("  //endregion")
            lines.append("")

    lines.append("}")
    return lines


# ---------------------------------------------------------------------------
# File assembly
# ---------------------------------------------------------------------------


_HEADER_BAR = "=" * 77


def _render_imports(referenced: Set[str], defined: Set[str]) -> List[str]:
    """Render a placeholder imports block. The AI fixes real paths after bootstrap."""
    missing = sorted(t for t in referenced if t not in defined)
    if not missing:
        return []
    return [
        "// TODO: adjust imports — the CLI cannot resolve module paths automatically",
        "// Referenced but not defined in this file:",
        "//   " + ", ".join(missing),
        "",
    ]


def render_ka_file(ka: Dict[str, Any], *, fidelity: str) -> str:
    """Render a single KA to a TypeScript file body."""
    classes = ka.get("classes") or []
    if not classes:
        return "// (empty key abstraction — no classes defined)\n"

    defined = {c.get("name", "") for c in classes if c.get("name")}
    referenced = _all_referenced_types(classes)

    parts: List[str] = []
    parts.append(f"// {_HEADER_BAR}")
    parts.append(f"// KA: {ka.get('name', 'Unnamed')}")
    intro = (ka.get("intro") or "").strip()
    if intro:
        for para in intro.splitlines():
            parts.append(f"// {para}")
    parts.append(f"// {_HEADER_BAR}")
    parts.append("")

    imports = _render_imports(referenced, defined)
    parts.extend(imports)

    for cls in classes:
        parts.extend(_render_class(cls, fidelity=fidelity))
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def render_boundary_class_file(cls: Dict[str, Any], *, fidelity: str) -> str:
    """Render a single boundary class to a TypeScript file body."""
    defined = {cls.get("name", "")}
    referenced = _all_referenced_types([cls])
    parts: List[str] = []
    parts.append(f"// {_HEADER_BAR}")
    parts.append(f"// Boundary class: {cls.get('name', 'Unnamed')}")
    owned_by = cls.get("owned_by", "")
    if owned_by:
        parts.append(f"// Owned by: {owned_by}")
    parts.append(f"// {_HEADER_BAR}")
    parts.append("")
    parts.extend(_render_imports(referenced, defined))
    parts.extend(_render_class(cls, fidelity=fidelity))
    parts.append("")
    return "\n".join(parts).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Path planning
# ---------------------------------------------------------------------------


def plan_output_files(graph: Dict[str, Any], out_root: Path) -> List[Tuple[Path, str, Dict[str, Any]]]:
    """Return a list of (target_path, kind, source_node) for the whole graph.

    ``kind`` is one of ``"ka"`` or ``"boundary"``. The source_node is passed
    back to the renderer to avoid a second walk.
    """
    plan: List[Tuple[Path, str, Dict[str, Any]]] = []
    for module in graph.get("modules", []) or []:
        module_slug = to_kebab_case(module.get("name", ""))
        module_root = out_root / module_slug
        for ka in module.get("key_abstractions", []) or []:
            ka_slug = to_kebab_case(ka.get("name", ""))
            plan.append((module_root / f"{ka_slug}.ts", "ka", ka))
        for cls in (module.get("boundary_domain") or {}).get("classes", []) or []:
            cls_slug = to_kebab_case(cls.get("name", ""))
            plan.append(
                (module_root / "boundary" / f"{cls_slug}.ts", "boundary", cls)
            )
    return plan
