#!/usr/bin/env python3
"""Emit map-model-spec.md from map-model-spec.json (template shape)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def esc(s: str) -> str:
    return (s or "").replace("`", "\\`")


def bullets_depends_on(deps: list | None) -> str:
    if not deps:
        return "—"
    lines = []
    for d in deps:
        lines.append(
            f"- **{d.get('module', '?')}** provides `{', '.join(d.get('provides_concepts') or [])}` "
            f"for dependents `{', '.join(d.get('dependent_concepts') or [])}` — {d.get('reason', '')}"
        )
    return "\n".join(lines)


def render_concept(c: dict) -> str:
    lines = [
        f"#### **{esc(c.get('name', ''))}**",
        "",
        f"- **Evidence stage:** {esc(str(c.get('evidence_stage', '')))}",
        f"- **Foundational (concept):** {c.get('foundational', '—')}",
        f"- **Chunk ids:** {', '.join('`' + str(x) + '`' for x in (c.get('chunk_ids') or []))}",
    ]
    ce = c.get("chunk_evidence")
    if ce:
        lines.append("- **Chunk evidence:**")
        for e in ce:
            lines.append(f"  - `{e.get('chunk_id')}` (*{e.get('evidence_type', '')}*): {e.get('note', '')}")
    else:
        lines.append("- **Chunk evidence:** —")
    lines.append(f"- **Owns:** {esc(c.get('owns', ''))} — *chunk:* `{esc(str(c.get('owns_chunk', '')))}`")
    if c.get("extends"):
        lines.append(f"- **extends:** `{esc(str(c['extends']))}`")
    props = c.get("properties") or []
    if props:
        lines.append("- **Properties:**")
        for p in props:
            lines.append(f"  - {esc(p.get('definition', ''))} — *chunk:* `{esc(str(p.get('chunk', '')))}`")
    else:
        lines.append("- **Properties:** —")
    ops = c.get("operations") or []
    if ops:
        lines.append("- **Operations:**")
        for o in ops:
            lines.append(f"  - {esc(o.get('definition', ''))} — *chunk:* `{esc(str(o.get('chunk', '')))}`")
    else:
        lines.append("- **Operations:** —")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    oq = data.get("open_questions") or []
    oq_md = "\n".join(f"- {x}" for x in oq) if oq else "*None.*"
    cc = (data.get("cross_cutting_notes") or "").strip()
    cc_md = cc if cc else "*None.*"

    n_chunks = data.get("N_chunks")
    n_cell = str(n_chunks) if n_chunks is not None else "*(not stored in JSON per breadth step; see context index)*"

    parts: list[str] = [
        "# Map model spec — " + esc(str(data.get("source_corpus", ""))),
        "",
        "_Human-readable twin of `map-model-spec.json`._",
        "",
        "## Document metadata",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Phase | {esc(str(data.get('phase', '')))} |",
        f"| Source corpus | {esc(str(data.get('source_corpus', '')))} |",
        f"| Context index | `{esc(str(data.get('context_index', '')))}` |",
        f"| N chunks | {n_cell} |",
        f"| Phase note | {esc(str(data.get('phase_note', '')))} |",
        "",
        "## Open questions",
        "",
        oq_md,
        "",
        "## Cross-cutting notes",
        "",
        cc_md,
        "",
        "---",
        "",
    ]

    for i, pair in enumerate(data.get("modules_and_epics") or [], start=1):
        mod = pair.get("module") or {}
        epic = pair.get("epic") or {}
        mname = esc(str(mod.get("name", "")))
        ename = esc(str(epic.get("name", "")))
        concepts = mod.get("concepts") or []
        cnames = ", ".join(f"**{esc(str(c.get('name', '')))}**" for c in concepts)

        parts.append(f"## {i}. {mname} · {ename}")
        parts.append("")
        parts.append("### Domain model")
        parts.append("")
        parts.append(f"### Module: {mname}")
        parts.append("")
        parts.append(f"- **Foundational (module):** {mod.get('foundational', '—')}")
        parts.append(
            f"- **Description:** {esc(str(mod.get('description', '')))} — *chunk:* `{esc(str(mod.get('description_chunk', '')))}`"
        )
        parts.append(f"- **Depends on:**\n{bullets_depends_on(mod.get('depends_on'))}")
        parts.append(f"- **Concepts:** {cnames}")
        parts.append("")

        for c in concepts:
            parts.append(render_concept(c))

        parts.append("### Story map")
        parts.append("")
        parts.append(f"### Epic: {ename}")
        parts.append("")
        parts.append(
            f"**Full statement:** {esc(str(epic.get('statement', '')))} — *chunk:* `{esc(str(epic.get('statement_chunk', '')))}`"
        )
        parts.append("")
        pc = epic.get("pre_condition")
        pcc = epic.get("pre_condition_chunk")
        if pc:
            parts.append(f"- **Pre-Condition:** {esc(str(pc))} — *chunk:* `{esc(str(pcc or ''))}`")
        parts.append(f"- **Triggering actor:** {esc(str(epic.get('triggering_actor', '')))}")
        parts.append(f"- **Responding actor:** {esc(str(epic.get('responding_actor', '')))}")
        parts.append("- **Confirming stories (scaffold):**")
        for j, st in enumerate(epic.get("confirming_stories") or [], start=1):
            parts.append(f"  {j}. {esc(str(st))}")
        parts.append("")
        cid = pair.get("chunk_ids") or {}
        parts.append("### Evidence buckets (pair)")
        parts.append("")
        parts.append("| Bucket | Chunk ids |")
        parts.append("|--------|-----------|")
        parts.append(f"| identified | {', '.join('`' + str(x) + '`' for x in (cid.get('identified') or []))} |")
        parts.append(f"| provisional | {', '.join('`' + str(x) + '`' for x in (cid.get('provisional') or []))} |")
        parts.append(f"| ambiguous | {', '.join('`' + str(x) + '`' for x in (cid.get('ambiguous') or []))} |")
        parts.append("")
        parts.append("---")
        parts.append("")

    Path(args.output).write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
