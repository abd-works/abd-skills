#!/usr/bin/env python3
"""Phase 3: Extract concept signals from chunks (unguided).

Runs extraction using extraction_config.json if present, else defaults.
Produces: term_candidates.json, definition_candidates.json, dependency_actions.json,
cooccurrence_graph.json, table_vocabularies.json.
Evidence speaks first; concepts follow.
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent

# Definition patterns: "X is a", "X represents", etc.
_DEFINITION_RE = re.compile(
    r"\b([A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,3})\s+(?:is|represents|refers to|describes|means)\s+",
    re.IGNORECASE,
)
# Relationship hints for dependency extraction
_REL_HINT_RE = re.compile(
    r"\b(has|have|contains?|includes?|uses?|requires?|applies?|targets?|modifies?|affects?)\b",
    re.IGNORECASE,
)
# Table header pattern
_TABLE_HEADER_RE = re.compile(r"^\s*\|([^|]+)\|", re.MULTILINE)


def _load_json(path: Path) -> dict | list:
    if not path.exists():
        return {} if "config" in str(path) else []
    return json.loads(path.read_text(encoding="utf-8"))


def _load_chunks(context_path: Path) -> list[dict]:
    data = _load_json(context_path)
    if isinstance(data, list):
        return data
    return data.get("chunks", data.get("rule_chunks", []))


def _title_terms(text: str) -> list[str]:
    """Extract title-case terms."""
    pats = re.findall(r"\b([A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,4})\b", text)
    return [p.strip() for p in pats if 2 < len(p.strip()) < 50]


def _extract_term_candidates(chunks: list[dict], config: dict) -> list[dict]:
    """Term frequency + structural weighting."""
    weights = config.get("weights", {})
    heading_weight = weights.get("heading", 5)
    default_weight = weights.get("default", 1)

    counts: Counter = Counter()
    weighted: dict[str, float] = defaultdict(float)

    for chunk in chunks:
        text = chunk.get("text", "")
        lines = text.split("\n")
        for i, line in enumerate(lines):
            w = heading_weight if (i < 3 and line.strip().endswith(":")) else default_weight
            for term in _title_terms(line):
                key = term.strip()
                if len(key) > 2:
                    counts[key] += 1
                    weighted[key] += w

    out = []
    for i, (term, count) in enumerate(counts.most_common(200)):
        if count < 2:
            continue
        out.append({
            "term_id": f"term_{i:04d}",
            "name": term,
            "count": count,
            "weighted_score": round(weighted[term], 2),
        })
    return out


def _extract_definition_candidates(chunks: list[dict]) -> list[dict]:
    """Definition sentence detection."""
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        cid = chunk.get("chunk_id", "")
        for m in _DEFINITION_RE.finditer(text):
            concept = m.group(1).strip()
            if len(concept) > 2:
                out.append({
                    "definition_id": f"def_{len(out):04d}",
                    "concept": concept,
                    "source_chunk": cid,
                    "raw": text[max(0, m.start() - 20) : m.end() + 80],
                })
    return out


def _extract_dependency_actions(chunks: list[dict]) -> list[dict]:
    """Subject-verb-object triples from relationship hints."""
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        cid = chunk.get("chunk_id", "")
        for sent in re.split(r"[.!?;]\s+", text):
            if not _REL_HINT_RE.search(sent) or len(sent) < 40:
                continue
            terms = _title_terms(sent)
            if len(terms) >= 2:
                m = _REL_HINT_RE.search(sent)
                pred = m.group(1).lower() if m else "relates to"
                out.append({
                    "dep_id": f"dep_{len(out):04d}",
                    "subject": terms[0],
                    "predicate": pred,
                    "object": terms[1],
                    "source_chunk": cid,
                    "raw": sent[:200],
                })
    return out


def _extract_cooccurrence(chunks: list[dict], term_candidates: list[dict]) -> dict:
    """Co-occurrence graph of terms."""
    term_set = {t["name"] for t in term_candidates}
    pairs: Counter = Counter()
    for chunk in chunks:
        text = chunk.get("text", "")
        terms_in_chunk = [t for t in _title_terms(text) if t in term_set]
        for i, a in enumerate(terms_in_chunk):
            for b in terms_in_chunk[i + 1 :]:
                if a != b:
                    pairs[(a, b)] += 1
    edges = [{"from": a, "to": b, "count": c} for (a, b), c in pairs.most_common(300)]
    return {"edges": edges, "node_count": len(term_set)}


def _extract_table_vocabularies(chunks: list[dict]) -> list[dict]:
    """Table names, headers, row labels."""
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        cid = chunk.get("chunk_id", "")
        for m in _TABLE_HEADER_RE.finditer(text):
            headers = [h.strip() for h in m.group(1).split("|") if h.strip()]
            if headers:
                out.append({
                    "table_id": f"tbl_{len(out):04d}",
                    "headers": headers,
                    "source_chunk": cid,
                })
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3: Extract concept signals")
    parser.add_argument("--input", "-i", required=True, help="Path to context_chunks.json")
    parser.add_argument("--config", "-c", help="Path to extraction_config.json (optional)")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    out_dir = Path(args.output_dir).resolve()
    config_path = Path(args.config).resolve() if args.config else None

    config = _load_json(config_path) if config_path and config_path.exists() else {}

    chunks = _load_chunks(in_path)
    if not chunks:
        print("No chunks found.", file=__import__("sys").stderr)
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    term_candidates = _extract_term_candidates(chunks, config)
    definition_candidates = _extract_definition_candidates(chunks)
    dependency_actions = _extract_dependency_actions(chunks)
    cooccurrence_graph = _extract_cooccurrence(chunks, term_candidates)
    table_vocabularies = _extract_table_vocabularies(chunks)

    out_dir.mkdir(parents=True, exist_ok=True)
    for name, data in [
        ("term_candidates.json", term_candidates),
        ("definition_candidates.json", definition_candidates),
        ("dependency_actions.json", dependency_actions),
        ("cooccurrence_graph.json", cooccurrence_graph),
        ("table_vocabularies.json", table_vocabularies),
    ]:
        (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"Extracted: {len(term_candidates)} terms, {len(definition_candidates)} definitions, "
        f"{len(dependency_actions)} dependencies, {len(cooccurrence_graph.get('edges', []))} co-occurrences, "
        f"{len(table_vocabularies)} tables -> {out_dir}"
    )


if __name__ == "__main__":
    main()
