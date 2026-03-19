"""Summarize a chunk_evidence.json file in human-readable form.

Usage:
    python summarize.py <chunk_evidence.json>

Writes:
    <option>/relationships.md  — all cross-module relationships as readable statements
    <option>/summary.md        — concept mentions and relationship counts
Prints the same to stdout.
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "option-c/chunk_evidence.json"
data = json.loads(path.read_text(encoding="utf-8"))
option_dir = path.parent

header = f"=== {path.parent.name.upper()} SUMMARY ==="
stats = (
    f"Chunks: {data['chunk_count']}  |  AI calls: {data['ai_calls']}  |  Time: {data['elapsed_seconds']}s\n"
    f"Concept mentions: {data['total_concept_mentions']}  |  Relationships: {data['total_relationships_detected']}"
)

# ── Concept evidence by module and type ──────────────────────────────────────
# by_module[module][concept][evidence_type] = count of chunks
by_module = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
for chunk in data["evidence"]:
    cid = chunk["chunk_id"]
    for pc in chunk["primary_concepts"]:
        module = pc["module"]
        concept = pc["concept"]
        # Support both old format (evidence_type string) and new (evidence_types list)
        types = pc.get("evidence_types", [pc.get("evidence_type", "mention")])
        if isinstance(types, str):
            types = [types]
        for t in types:
            by_module[module][concept][t] += 1

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
# key = (from_concept, from_module, relationship, to_concept, to_module)
rel_counts: dict[tuple, int] = defaultdict(int)
rel_justifications: dict[tuple, list[str]] = defaultdict(list)
rel_chunks: dict[tuple, list[str]] = defaultdict(list)

for chunk in data["evidence"]:
    cid = chunk["chunk_id"]
    for rel in chunk["cross_module_relationships"]:
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
    f"Option: {data.get('option', '?')}  |  {data.get('description', '')}",
    f"Total relationships detected: {data['total_relationships_detected']}",
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
