#!/usr/bin/env python3
"""Run diagnostic across ALL concepts in hypothesis.json.

For each concept, checks every referenced chunk:
- Does chunk text contain the concept name?
- Is concept a subtype (in a list)?
- Is chunk unrelated (false positive)?
- Is concept an amalgamation (two words, only one strongly supported)?

Output: comprehensive report to stdout and hypothesis_diagnostic_report.md
"""
import json
import re
from pathlib import Path


def load_chunk_lookup(context_path: Path) -> dict[str, str]:
    """Build chunk_id -> text lookup from context_chunks.json."""
    chunks_file = context_path / "context_chunks.json"
    if not chunks_file.exists():
        return {}
    data = json.loads(chunks_file.read_text(encoding="utf-8"))
    return {c["chunk_id"]: c.get("text", "") for c in data if "chunk_id" in c}


def normalize_for_match(name: str) -> str:
    """Normalize concept name for matching (lowercase, collapse spaces)."""
    return re.sub(r"\s+", " ", name.lower().strip())


def concept_in_chunk(concept_name: str, chunk_text: str) -> tuple[bool, bool, bool]:
    """Check if concept appears in chunk. Returns (exact, partial, list_member)."""
    norm_name = normalize_for_match(concept_name)
    text_lower = chunk_text.lower()
    # Exact phrase
    exact = norm_name in text_lower
    # Word-by-word (all words appear)
    words = [w for w in re.split(r"\W+", norm_name) if len(w) > 1]
    partial = all(w in text_lower for w in words) if words else False
    # List pattern: "• Concept" or "Concept, " or "Concept:" as list item
    list_pattern = rf"(?:^|\n|\•|\*)\s*{re.escape(concept_name)}[\s:,]"
    list_member = bool(re.search(list_pattern, chunk_text, re.IGNORECASE))
    return exact, partial, list_member


def classify_concept(
    name: str,
    chunk_ids: list[str],
    chunk_lookup: dict[str, str],
) -> dict:
    """Classify a concept based on its chunks."""
    supported = []
    unsupported = []
    list_member_count = 0
    for cid in chunk_ids:
        text = chunk_lookup.get(cid, "")
        if not text:
            unsupported.append((cid, "chunk not found"))
            continue
        exact, partial, list_member = concept_in_chunk(name, text)
        if list_member:
            list_member_count += 1
        if exact or partial:
            supported.append((cid, "exact" if exact else "partial"))
        else:
            # Check for word overlap (loose match)
            words = [w for w in re.split(r"\W+", normalize_for_match(name)) if len(w) > 2]
            overlap = sum(1 for w in words if w in text.lower())
            if overlap >= len(words) * 0.5:
                supported.append((cid, "loose"))
            else:
                unsupported.append((cid, "no match"))

    # Classification
    total = len(chunk_ids)
    supp_count = len(supported)
    unsupp_count = len(unsupported)

    if total == 0:
        classification = "no_chunks"
        suggested = "add chunks or remove"
    elif unsupp_count == total:
        classification = "false_positive"
        suggested = "remove concept or fix chunk_ids"
    elif unsupp_count > 0 and unsupp_count >= total * 0.5:
        classification = "mixed_evidence"
        suggested = "remove unsupported chunk_ids"
    elif list_member_count >= supp_count * 0.5 and supp_count > 0:
        classification = "subtype"
        suggested = "add to concept_hierarchy under parent"
    elif " " in name and not any(exact for _, t in supported if t == "exact"):
        # Multi-word, no exact match
        classification = "possible_amalgamation"
        suggested = "verify: split or merge into parent"
    else:
        classification = "real"
        suggested = "keep; ensure in hierarchy if has subtypes"

    return {
        "supported": supported,
        "unsupported": unsupported,
        "list_member_count": list_member_count,
        "classification": classification,
        "suggested": suggested,
    }


def main():
    # Paths - assume run from skill dir or workspace
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    # Default: test/mm3/solution
    workspace = skill_dir / "test" / "mm3" / "solution"
    context_path = workspace / "context"
    hypothesis_path = workspace / "generated" / "hypothesis.json"

    if not hypothesis_path.exists():
        print(f"hypothesis.json not found: {hypothesis_path}")
        return 1

    hypothesis = json.loads(hypothesis_path.read_text(encoding="utf-8"))
    chunk_lookup = load_chunk_lookup(context_path)
    concepts = hypothesis.get("concepts", {})

    results = []
    for name, c in concepts.items():
        chunk_ids = c.get("chunk_ids") or []
        r = classify_concept(name, chunk_ids, chunk_lookup)
        results.append({
            "name": name,
            "chunk_count": len(chunk_ids),
            **r,
        })

    # Summary counts
    by_class = {}
    for r in results:
        c = r["classification"]
        by_class[c] = by_class.get(c, 0) + 1

    # Write report
    report_path = workspace / "generated" / "hypothesis_diagnostic_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Hypothesis Concept Diagnostic Report",
        "",
        "Full scan across ALL concepts. For each concept, every chunk was checked for support.",
        "",
        "## Summary by Classification",
        "",
        "| Classification | Count |",
        "|----------------|-------|",
    ]
    for c, n in sorted(by_class.items(), key=lambda x: -x[1]):
        lines.append(f"| {c} | {n} |")
    lines.extend([
        "",
        "## Per-Concept Results",
        "",
        "| Concept | Chunks | Supported | Unsupported | Classification | Suggested |",
        "|---------|--------|-----------|--------------|----------------|-----------|",
    ])

    for r in results:
        supp = len(r["supported"])
        unsupp = len(r["unsupported"])
        lines.append(
            f"| {r['name']} | {r['chunk_count']} | {supp} | {unsupp} | {r['classification']} | {r['suggested']} |"
        )

    lines.extend([
        "",
        "## Detail: Unsupported Chunks (Potential False Positives)",
        "",
    ])

    for r in results:
        if r["unsupported"]:
            lines.append(f"### {r['name']}")
            for cid, reason in r["unsupported"]:
                lines.append(f"- `{cid}`: {reason}")
            lines.append("")

    lines.extend([
        "",
        "## Detail: Possible Amalgamations",
        "",
    ])
    for r in results:
        if r["classification"] == "possible_amalgamation":
            lines.append(f"- **{r['name']}**: {r['suggested']}")
    lines.append("")

    lines.extend([
        "",
        "## Detail: Subtypes (Add to concept_hierarchy)",
        "",
    ])
    for r in results:
        if r["classification"] == "subtype":
            lines.append(f"- **{r['name']}**: {r['suggested']}")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {report_path}")
    print("\nSummary:", by_class)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
