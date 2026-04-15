"""Summarize map-model-spec.json (or legacy module_chunk_index.json) in human-readable form.

Reads map-model-spec.json which now contains chunk_evidence and cross_module_relationships
from Step 2. Same structure as legacy module_chunk_index.json.

Usage:
    python summarize.py [map-model-spec.json]

Writes:
    <dir>/relationships.md  — all cross-module relationships as readable statements
    <dir>/summary.md        — concept mentions and relationship counts
Prints the same to stdout.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

try:
    from _config import map_model_spec_path

    _default_spec = map_model_spec_path()
except ImportError as e:
    print(f"Error: could not import _config: {e}", file=sys.stderr)
    sys.exit(1)

path = Path(sys.argv[1]) if len(sys.argv) > 1 else _default_spec
data = json.loads(path.read_text(encoding="utf-8"))
option_dir = path.parent

run = data.get("chunk_classify_run", {})
chunk_count = run.get("chunk_count") or data.get("chunk_count", 0)
ai_calls = run.get("ai_calls") or data.get("ai_calls", 0)
elapsed = run.get("elapsed_seconds") or data.get("elapsed_seconds", 0)
total_mentions = run.get("total_concept_mentions") or data.get("total_concept_mentions", 0)
total_rels = run.get("total_relationships_detected") or data.get("total_relationships_detected", len(data.get("cross_module_relationships", [])))
if not total_mentions:
    total_mentions = sum(
        len(c.get("chunk_evidence", []))
        for pair in data.get("modules_and_epics", [])
        for c in pair.get("module", {}).get("concepts", [])
    )

header = f"=== {path.parent.name.upper()} SUMMARY ==="
stats = (
    f"Chunks: {chunk_count}  |  AI calls: {ai_calls}  |  Time: {elapsed}s\n"
    f"Concept mentions: {total_mentions}  |  Relationships: {total_rels}"
)

# ── Concept evidence by module and type ──────────────────────────────────────
by_module = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
for pair in data.get("modules_and_epics", []):
    module_name = pair.get("module", {}).get("name", "")
    for c in pair.get("module", {}).get("concepts", []):
        concept = c.get("name", "")
        for ev in c.get("chunk_evidence", []):
            t = ev.get("evidence_type", "mention")
            by_module[module_name][concept][t] += 1

EVIDENCE_ORDER = ["definition", "table", "rule", "example", "mention"]

module_lines = []
for module in sorted(by_module.keys()):
    concepts = by_module[module]
    total_chunks = sum(sum(types.values()) for types in concepts.values())
    module_lines.append(f"\n### {module}")
    module_lines.append(f"Total evidence instances: {total_chunks} across {len(concepts)} concepts\n")
    for concept, types in sorted(concepts.items(), key=lambda x: -sum(x[1].values())):
        type_parts = []
        for t in EVIDENCE_ORDER:
            if t in types:
                type_parts.append(f"{t}:{types[t]}")
        module_lines.append(f"  **{concept}**  [{' | '.join(type_parts)}]")

# ── Relationship aggregation ──────────────────────────────────────────────────
rel_counts: dict[tuple, int] = defaultdict(int)
rel_justifications: dict[tuple, list[str]] = defaultdict(list)
rel_chunks: dict[tuple, list[str]] = defaultdict(list)
for rel in data.get("cross_module_relationships", []):
    cid = rel.get("chunk", "")
    key = (
        rel["from"]["concept"], rel["from"]["module"],
        rel["relationship"],
        rel["to"]["concept"], rel["to"]["module"],
    )
    rel_counts[key] += 1
    rel_chunks[key].append(cid)
    just = rel.get("justification", "")
    if just and just not in rel_justifications[key]:
        rel_justifications[key].append(just)

# ── Build relationship statements ─────────────────────────────────────────────
rel_statements = []
for key, count in sorted(rel_counts.items(), key=lambda x: -x[1]):
    from_concept, from_module, relationship, to_concept, to_module = key
    justifications = rel_justifications[key]
    chunks_list = rel_chunks[key]

    # Human-readable relationship verb
    verb_map = {
        "inherits": "extends / inherits from",
        "produces": "produces",
        "uses": "uses / depends on",
        "modifies": "modifies",
        "constrained_by": "is constrained by",
        "targets": "targets",
        "impairs": "impairs",
        "uses_modifier_from": "uses modifier from",
    }
    verb = verb_map.get(relationship, relationship)

    stmt = f"[{count}x] **{from_concept}** ({from_module}) {verb} **{to_concept}** ({to_module})"
    if justifications:
        stmt += f"\n       Justification: {justifications[0]}"
    stmt += f"\n       Evidence chunks ({min(5, len(chunks_list))} of {len(chunks_list)}): {', '.join(chunks_list[:5])}"
    rel_statements.append((count, stmt))

# ── Write relationships.md ────────────────────────────────────────────────────
rel_md_lines = [
    f"# Cross-Module Relationships — {path.parent.name}",
    "",
    f"Source: {path.name}",
    f"Option: {data.get('chunk_classify_run', {}).get('option', data.get('option', '?'))}  |  {data.get('chunk_classify_run', {}).get('description', data.get('description', ''))}",
    f"Total relationships detected: {total_rels}",
    f"Unique relationship types: {len(rel_counts)}",
    "",
    "Each entry: [count] **FromConcept** (FromModule) --relationship--> **ToConcept** (ToModule)",
    "Count = number of chunks where this relationship signal was detected.",
    "",
    "---",
    "",
]
for count, stmt in rel_statements:
    rel_md_lines.append(stmt)
    rel_md_lines.append("")

rel_md = "\n".join(rel_md_lines)
(option_dir / "relationships.md").write_text(rel_md, encoding="utf-8")

# ── Write summary.md ──────────────────────────────────────────────────────────
summary_lines = [
    f"# Summary — {path.parent.name}",
    "",
    stats,
    "",
    "## Concept Evidence by Module",
    "",
    "Format per concept: [definition:N | table:N | rule:N | example:N | mention:N]",
    "",
] + module_lines + [
    "",
    "## Cross-Module Relationships",
    "",
]
for count, stmt in rel_statements:
    summary_lines.append(stmt)
    summary_lines.append("")

summary_md = "\n".join(summary_lines)
(option_dir / "summary.md").write_text(summary_md, encoding="utf-8")

# ── Print to stdout ───────────────────────────────────────────────────────────
print(header)
print(stats)
print()
print("=== CONCEPT EVIDENCE BY MODULE ===")
print("\n".join(module_lines))
print()
print("=== CROSS-MODULE RELATIONSHIPS ===")
for count, stmt in rel_statements:
    print(stmt)
    print()

print(f"\nFiles written:")
print(f"  {option_dir / 'relationships.md'}")
print(f"  {option_dir / 'summary.md'}")
