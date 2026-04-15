#!/usr/bin/env python3
"""Emit inheritance report: plain `extends` outline + one section per concept with handbook chunk text."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

SPEC = Path(__file__).resolve().parent / "map-model-spec.json"
CHUNKS_DIR = Path(__file__).resolve().parent.parent / "context" / "chunks"


def split_frontmatter(raw: str) -> tuple[dict[str, str | list], str]:
    """Parse leading YAML frontmatter between --- lines; return meta dict and body."""
    raw = raw.lstrip("\ufeff")
    if not raw.startswith("---"):
        return {}, raw.strip()
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw.strip()
    meta_block = parts[1].strip()
    body = parts[2].strip()
    meta: dict[str, str | list] = {}
    for line in meta_block.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val.startswith("["):
            try:
                meta[key] = json.loads(val)
            except json.JSONDecodeError:
                meta[key] = val
        else:
            meta[key] = val
    return meta, body


def format_section_path(meta: dict) -> str:
    sp = meta.get("section_path")
    if isinstance(sp, list):
        return " / ".join(str(x) for x in sp)
    if isinstance(sp, str):
        return sp
    return ""


def attribution_line(meta: dict, chunk_id: str) -> str:
    src = meta.get("source", "unknown source")
    sp = format_section_path(meta)
    tail = f", section_path: {sp}" if sp else ""
    return f"— {src}, chunk {chunk_id}{tail}"


def strip_chunk_leading_h2(body: str) -> str:
    """Remove one leading `## ` from the first line so the spec concept heading stays the only H2."""
    lines = body.splitlines()
    if lines and lines[0].startswith("## "):
        lines[0] = lines[0][3:].strip()
    return "\n".join(lines).strip()


def load_chunk(chunk_id: str) -> tuple[dict, str] | None:
    path = CHUNKS_DIR / f"{chunk_id}.md"
    if not path.is_file():
        return None
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    body = strip_chunk_leading_h2(body)
    return meta, body


def chunk_ids_for(row: dict) -> list[str]:
    ids = row.get("chunk_ids")
    if ids:
        return list(ids)
    oc = row.get("owns_chunk")
    return [oc] if oc else []


def main() -> None:
    data = json.loads(SPEC.read_text(encoding="utf-8"))

    concept_by_name: dict[str, dict] = {}
    for pair in data.get("modules_and_epics", []):
        for c in pair.get("module", {}).get("concepts", []):
            n = c.get("name")
            if not n:
                continue
            if n in concept_by_name:
                raise SystemExit(f"Duplicate concept name in spec: {n!r}")
            concept_by_name[n] = c

    all_names = set(concept_by_name)

    children: dict[str, list[str]] = defaultdict(list)
    for name, row in concept_by_name.items():
        p = row.get("extends")
        if p and p in all_names:
            children[p].append(name)
    for p in children:
        children[p].sort()

    def is_top(name: str) -> bool:
        p = concept_by_name[name].get("extends")
        return not p or p not in all_names

    roots = sorted(n for n in all_names if is_top(n))

    order: list[str] = []
    emitted: set[str] = set()

    def walk(name: str, stack: frozenset[str]) -> None:
        if name in stack:
            return
        emitted.add(name)
        order.append(name)
        for ch in children.get(name, []):
            walk(ch, stack | {name})

    for r in roots:
        walk(r, frozenset())

    for n in sorted(all_names - emitted):
        walk(n, frozenset())

    lines: list[str] = []
    lines.append("# Domain object inheritance — `extends` trees (MM3)")
    lines.append("")
    lines.append(
        "Each concept below is listed in **depth-first** order. Under each name: excerpt from the "
        "handbook chunk(s) linked in `map-model-spec.json`, then a one-line source line."
    )
    lines.append("")

    lines.append("## Outline")
    lines.append("")

    def outline(name: str, depth: int, stack: frozenset[str]) -> None:
        if name in stack:
            lines.append(f"{'  ' * depth}…cycle: `{name}`")
            return
        lines.append(f"{'  ' * depth}{name}")
        for ch in children.get(name, []):
            outline(ch, depth + 1, stack | {name})

    for r in roots:
        outline(r, 0, frozenset())
    lines.append("")

    lines.append("## Concepts and evidence")
    lines.append("")

    for name in order:
        row = concept_by_name[name]
        lines.append(f"### {name}")
        lines.append("")
        ids = chunk_ids_for(row)
        if not ids:
            owns = row.get("owns", "").strip()
            if owns:
                lines.append(owns)
            else:
                lines.append("_No `chunk_ids` / `owns_chunk` and no `owns` text in spec._")
            lines.append("")
            continue

        any_loaded = False
        for cid in ids:
            loaded = load_chunk(cid)
            if loaded is None:
                lines.append(f"_(Missing chunk file: `{CHUNKS_DIR / (cid + '.md')}`)_")
                lines.append("")
                continue
            meta, body = loaded
            if any_loaded:
                lines.append("")
                lines.append("* * *")
                lines.append("")
            lines.append(body)
            lines.append("")
            lines.append(attribution_line(meta, cid))
            any_loaded = True
        if not any_loaded:
            owns = row.get("owns", "").strip()
            if owns:
                lines.append(owns)
                lines.append("")
        else:
            lines.append("")

    out_path = SPEC.parent / "inheritance-tree-report.md"
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({len(order)} concepts, {len(roots)} top-level types)")


if __name__ == "__main__":
    main()
