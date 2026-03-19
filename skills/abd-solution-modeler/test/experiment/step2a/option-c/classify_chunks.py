"""Step 2a Option C — Code-only chunk evidence extraction. No AI calls.

For each chunk, identifies:
  1. Which concepts it evidences (by module)
  2. Cross-module relationships detected (via co-occurrence and pattern matching)

A chunk is NOT assigned to one module. It can evidence concepts in multiple
modules simultaneously. Relationships are recorded at read time.

Signals used (all code, no AI):
  1. Exact concept name match (whole word, case-insensitive) → primary concept evidence
  2. Definition pattern ("ConceptName is a...", "ConceptName:") → high-confidence evidence
  3. Co-occurrence pairs → relationship signals
  4. Table header patterns → module/concept context

Output:
  option-c/chunk_evidence.json   — per-chunk evidence and cross-module relationships
  option-c/run_log.json          — timing, counts, stats
"""
import argparse
import json
import re
import time
from pathlib import Path

# ── Module-specific co-occurrence pairs ──────────────────────────────────────
MODULE_COOCCURRENCE: dict[str, list[tuple[str, str]]] = {
    "Resolution": [
        ("difficulty class", "check"),
        ("dc", "roll"),
        ("degree", "success"),
        ("degree", "failure"),
        ("d20", "modifier"),
    ],
    "Character": [
        ("power points", "power level"),
        ("power level", "cap"),
        ("hero points", "complication"),
        ("power point", "budget"),
    ],
    "Character Traits": [
        ("agility", "dodge"),
        ("stamina", "fortitude"),
        ("fighting", "parry"),
        ("awareness", "will"),
        ("skill rank", "ability"),
        ("ability rank", "skill"),
    ],
    "Powers": [
        ("cost per rank", "effect"),
        ("extras", "flaws"),
        ("duration", "sustained"),
        ("alternate effect", "array"),
        ("power level", "effect rank"),
    ],
    "Combat": [
        ("attack check", "defense"),
        ("attack", "toughness"),
        ("initiative", "round"),
        ("standard action", "move action"),
        ("attack bonus", "dodge"),
    ],
}

# ── Known cross-module relationship patterns ──────────────────────────────────
# (pattern_a, pattern_b, from_concept, from_module, relationship, to_concept, to_module)
RELATIONSHIP_PATTERNS = [
    # AttackCheck extends Check
    ("attack check", "dc", "AttackCheck", "Combat", "inherits", "Check", "Resolution"),
    ("attack.*check", "difficulty class", "AttackCheck", "Combat", "inherits", "Check", "Resolution"),
    # Effect produces Condition
    ("effect", "condition", "Effect", "Powers", "produces", "Condition", "Combat"),
    # Effect.resolve uses Check
    ("effect", "resistance check", "Effect", "Powers", "uses", "Check", "Resolution"),
    ("effect", "check.*dc", "Effect", "Powers", "uses", "Check", "Resolution"),
    # Power uses PowerLevel
    ("power level", "effect rank", "Power", "Powers", "constrained_by", "PowerLevel", "Character"),
    ("power level", "cost per rank", "Power", "Powers", "constrained_by", "PowerLevel", "Character"),
    # Defense targeted by attacks
    ("attack.*dodge", None, "AttackCheck", "Combat", "targets", "Defense", "Character Traits"),
    ("attack.*parry", None, "AttackCheck", "Combat", "targets", "Defense", "Character Traits"),
    # Condition applied to Defense
    ("condition", "dodge", "Condition", "Combat", "impairs", "Defense", "Character Traits"),
    ("condition", "parry", "Condition", "Combat", "impairs", "Defense", "Character Traits"),
    # Advantage modifies Check
    ("advantage", "attack.*bonus", "Advantage", "Character Traits", "modifies", "AttackCheck", "Combat"),
    ("advantage", "defense.*bonus", "Advantage", "Character Traits", "modifies", "Defense", "Character Traits"),
    # HeroPoint spent to affect Check
    ("hero point", "re-roll", "HeroPoint", "Character", "modifies", "Check", "Resolution"),
    ("hero point", "check", "HeroPoint", "Character", "modifies", "Check", "Resolution"),
    # Skill uses Ability modifier
    ("skill", "ability", "Skill", "Character Traits", "uses_modifier_from", "Ability", "Character Traits"),
]


def build_term_index(step1: dict) -> dict[str, dict[str, list[str]]]:
    """Build module_name -> {concept_name: [terms]} from step1 output."""
    index: dict[str, dict[str, list[str]]] = {}
    for pair in step1.get("modules_and_epics", []):
        module = pair.get("module", {})
        mname = module.get("name", "")
        if not mname:
            continue
        concepts = {}
        for concept in module.get("concepts", []):
            cname = concept.get("name", "").strip()
            if cname and len(cname) > 2:
                concepts[cname] = [cname]
        index[mname] = concepts
    return index


# ── Evidence type patterns ────────────────────────────────────────────────────

# Rule patterns: conditional/normative language near a concept
_RULE_TRIGGERS = re.compile(
    r'\b(if|when|unless|must|may not|cannot|can only|requires?|is required|'
    r'on success|on failure|at least|no more than|equal to|divided by)\b',
    re.IGNORECASE
)

# Example patterns
_EXAMPLE_TRIGGERS = re.compile(
    r'\b(for example|for instance|such as|e\.g\.|as an example|'
    r'consider|suppose|imagine|a hero with|a character with)\b',
    re.IGNORECASE
)

# Table detection: this corpus uses plain-text columnar tables, NOT pipe-delimited markdown.
# Headers are all-caps words on their own lines, repeated as a group.
# Strategy: look for 2+ all-caps column header words appearing on separate lines
# within a short span — a strong signal of a tabular structure.
_ALLCAPS_WORD = re.compile(r'^[A-Z][A-Z\s\-/]{2,}$')

def _has_columnar_table(text: str) -> bool:
    """Detect plain-text columnar tables (all-caps headers on separate lines)."""
    lines = text.split('\n')
    allcaps_runs = 0
    consecutive = 0
    for line in lines:
        stripped = line.strip()
        if stripped and _ALLCAPS_WORD.match(stripped) and len(stripped) <= 25:
            consecutive += 1
            if consecutive >= 2:
                return True
        else:
            consecutive = 0
    return False

# Per-concept table header signatures — all-caps column names that appear near this concept
# in a tabular structure. Used to confirm a table chunk is relevant to a specific concept.
_TABLE_HEADER_SIGNATURES: dict[str, list[str]] = {
    "Effect": ["ACTION", "RANGE", "DURATION", "COST"],
    "Power": ["ACTION", "RANGE", "DURATION", "COST"],
    "Modifier": ["EXTRAS", "FLAWS"],
    "Ability": ["STRENGTH", "STAMINA", "AGILITY", "DEXTERITY", "FIGHTING"],
    "Defense": ["DODGE", "PARRY", "FORTITUDE", "TOUGHNESS", "WILL"],
    "Skill": ["ACROBATICS", "ATHLETICS", "DECEPTION", "EXPERTISE"],
    "Advantage": ["ACCURATE", "AGILE", "ALL-OUT"],
    "Condition": ["DAZED", "STAGGERED", "INCAPACITATED"],
    "Action": ["STANDARD", "MOVE", "FREE", "REACTION"],
}


def _get_evidence_types(text: str, text_lower: str, concept_name: str) -> list[str]:
    """Return list of evidence types for this concept in this chunk."""
    types = []

    # Definition: concept name immediately followed by defining syntax
    defpat = re.compile(
        r'\b' + re.escape(concept_name.lower()) + r'\s*(?:is\s+a\b|refers?\s+to\b|:|—|–)',
        re.IGNORECASE
    )
    if defpat.search(text_lower):
        types.append("definition")

    # Rule: concept name appears near conditional/normative language
    concept_pos = [m.start() for m in re.finditer(r'\b' + re.escape(concept_name.lower()) + r'\b', text_lower)]
    for pos in concept_pos:
        window = text_lower[max(0, pos-150):pos+150]
        if _RULE_TRIGGERS.search(window):
            types.append("rule")
            break

    # Example: concept name appears near example language
    for pos in concept_pos:
        window = text_lower[max(0, pos-150):pos+150]
        if _EXAMPLE_TRIGGERS.search(window):
            types.append("example")
            break

    # Table: chunk contains a columnar plain-text table (all-caps headers on separate lines)
    if _has_columnar_table(text):
        # Check if this table is relevant to this concept via header signatures
        sigs = _TABLE_HEADER_SIGNATURES.get(concept_name, [])
        if sigs:
            if any(sig in text for sig in sigs):
                types.append("table")
        else:
            # No signature defined — concept appears in a table chunk, flag it
            types.append("table")

    # Fallback: plain mention
    if not types:
        types.append("mention")

    return types


def extract_evidence(text: str, chunk_id: str, source: str, term_index: dict) -> dict:
    text_lower = text.lower()

    primary_concepts = []  # concepts this chunk directly evidences
    cross_module_relationships = []  # relationships detected

    # Signal 1 + 2+: concept name match + evidence type detection
    for module, concepts in term_index.items():
        for cname, terms in concepts.items():
            for term in terms:
                pattern = r'\b' + re.escape(term.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    evidence_types = _get_evidence_types(text, text_lower, cname)
                    primary_concepts.append({
                        "concept": cname,
                        "module": module,
                        "evidence_types": evidence_types,
                        "primary_type": evidence_types[0],  # most specific found first
                    })
                    break  # one match per concept per chunk is enough

    # Signal 3: cross-module relationship patterns
    for rel_tuple in RELATIONSHIP_PATTERNS:
        pat_a, pat_b, from_concept, from_module, relationship, to_concept, to_module = rel_tuple
        match_a = bool(re.search(pat_a, text_lower)) if pat_a else True
        match_b = bool(re.search(pat_b, text_lower)) if pat_b else True
        if match_a and match_b:
            cross_module_relationships.append({
                "from": {"concept": from_concept, "module": from_module},
                "relationship": relationship,
                "to": {"concept": to_concept, "module": to_module},
                "detected_by": "pattern",
                "chunk": chunk_id,
            })

    # Signal 4: co-occurrence module signals (supplement, not replace)
    module_signals = {}
    for module, pairs in MODULE_COOCCURRENCE.items():
        hits = []
        for a, b in pairs:
            if a in text_lower and b in text_lower:
                hits.append(f"{a}+{b}")
        if hits:
            module_signals[module] = hits

    return {
        "chunk_id": chunk_id,
        "source": source,
        "primary_concepts": primary_concepts,
        "cross_module_relationships": cross_module_relationships,
        "module_signals": module_signals,
        "concept_count": len(primary_concepts),
        "relationship_count": len(cross_module_relationships),
    }


def main():
    base = Path(__file__).resolve().parent
    skill_dir = base.parent.parent.parent.parent

    parser = argparse.ArgumentParser()
    parser.add_argument("--step1", default=str(base.parent.parent / "step1-output-v2.json"))
    parser.add_argument("--chunks", default=str(skill_dir / "test/mm3/solution/context/context_chunks.json"))
    parser.add_argument("--output", default=str(base / "chunk_evidence.json"))
    args = parser.parse_args()

    print("Step 2a Option C — Code-only chunk evidence extraction")
    print(f"  Step1:  {args.step1}")
    print(f"  Chunks: {args.chunks}")

    step1 = json.loads(Path(args.step1).read_text(encoding="utf-8"))
    chunks = json.loads(Path(args.chunks).read_text(encoding="utf-8"))
    term_index = build_term_index(step1)

    t_start = time.time()
    results = []
    total_concepts = 0
    total_relationships = 0
    no_evidence = 0

    for chunk in chunks:
        evidence = extract_evidence(
            chunk.get("text", ""),
            chunk["chunk_id"],
            chunk.get("source", ""),
            term_index,
        )
        results.append(evidence)
        total_concepts += evidence["concept_count"]
        total_relationships += evidence["relationship_count"]
        if evidence["concept_count"] == 0:
            no_evidence += 1

    elapsed = time.time() - t_start

    output = {
        "option": "C",
        "description": "Code-only: term match + definition patterns + co-occurrence + relationship patterns. No AI calls.",
        "ai_calls": 0,
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(chunks),
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_relationships,
        "chunks_with_no_evidence": no_evidence,
        "evidence": results,
    }

    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    run_log = {
        "option": "C",
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(chunks),
        "ai_calls": 0,
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_relationships,
        "chunks_with_no_evidence": no_evidence,
    }
    (base / "run_log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")

    print(f"\n  Done in {elapsed:.3f}s — no AI calls")
    print(f"  Chunks processed:          {len(chunks)}")
    print(f"  Total concept mentions:    {total_concepts}")
    print(f"  Cross-module relationships:{total_relationships}")
    print(f"  Chunks with no evidence:   {no_evidence}")
    print(f"  Output: {args.output}")


if __name__ == "__main__":
    main()
