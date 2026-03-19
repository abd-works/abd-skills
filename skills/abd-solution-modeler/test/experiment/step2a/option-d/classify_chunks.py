"""Step 2a Option D — Hybrid: code signals first, AI for uncertain chunks.

Code pass (Option C signals) extracts concept mentions and known relationship patterns.
Chunks where code finds zero evidence OR only weak signals go to AI for deeper extraction.
AI reads those chunks and extracts concepts + cross-module relationships with justification.

This produces the same output format as Options B and C:
  - primary_concepts: concepts evidenced per chunk (multi-module OK)
  - cross_module_relationships: recorded at read time with justification

Output:
  option-d/chunk_evidence.json
  option-d/run_log.json

Requires: ANTHROPIC_API_KEY in environment for AI fallback chunks.
"""
import argparse
import json
import os
import re
import time
from pathlib import Path


# ── Shared code signals (same as Option C) ───────────────────────────────────

MODULE_COOCCURRENCE: dict[str, list[tuple[str, str]]] = {
    "Resolution": [
        ("difficulty class", "check"), ("dc", "roll"),
        ("degree", "success"), ("degree", "failure"), ("d20", "modifier"),
    ],
    "Character": [
        ("power points", "power level"), ("power level", "cap"),
        ("hero points", "complication"), ("power point", "budget"),
    ],
    "Character Traits": [
        ("agility", "dodge"), ("stamina", "fortitude"),
        ("fighting", "parry"), ("awareness", "will"),
        ("skill rank", "ability"), ("ability rank", "skill"),
    ],
    "Powers": [
        ("cost per rank", "effect"), ("extras", "flaws"),
        ("duration", "sustained"), ("alternate effect", "array"),
        ("power level", "effect rank"),
    ],
    "Combat": [
        ("attack check", "defense"), ("attack", "toughness"),
        ("initiative", "round"), ("standard action", "move action"),
        ("attack bonus", "dodge"),
    ],
}

RELATIONSHIP_PATTERNS = [
    ("attack check", "dc", "AttackCheck", "Combat", "inherits", "Check", "Resolution"),
    ("attack.*check", "difficulty class", "AttackCheck", "Combat", "inherits", "Check", "Resolution"),
    ("effect", "condition", "Effect", "Powers", "produces", "Condition", "Combat"),
    ("effect", "resistance check", "Effect", "Powers", "uses", "Check", "Resolution"),
    ("power level", "effect rank", "Power", "Powers", "constrained_by", "PowerLevel", "Character"),
    ("attack.*dodge", None, "AttackCheck", "Combat", "targets", "Defense", "Character Traits"),
    ("attack.*parry", None, "AttackCheck", "Combat", "targets", "Defense", "Character Traits"),
    ("condition", "dodge", "Condition", "Combat", "impairs", "Defense", "Character Traits"),
    ("hero point", "re-roll", "HeroPoint", "Character", "modifies", "Check", "Resolution"),
    ("skill", "ability", "Skill", "Character Traits", "uses_modifier_from", "Ability", "Character Traits"),
]


def build_term_index(step1: dict) -> dict[str, dict[str, list[str]]]:
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


def build_module_context(step1: dict) -> str:
    lines = []
    for pair in step1.get("modules_and_epics", []):
        module = pair.get("module", {})
        mname = module.get("name", "")
        desc = module.get("description", "")
        concepts = [c.get("name", "") for c in module.get("concepts", []) if c.get("name")]
        lines.append(f"- {mname}: {desc}\n  Concepts: {', '.join(concepts)}")
    return "\n".join(lines)


def extract_evidence_code(text: str, chunk_id: str, source: str, term_index: dict) -> dict:
    text_lower = text.lower()
    primary_concepts = []
    cross_module_relationships = []

    for module, concepts in term_index.items():
        for cname in concepts:
            pattern = r'\b' + re.escape(cname.lower()) + r'\b'
            if re.search(pattern, text_lower):
                defpat = re.compile(r'\b' + re.escape(cname.lower()) + r'\s*(?:is\s+a|refers?\s+to|:|—|–)', re.IGNORECASE)
                evidence_type = "definition" if defpat.search(text_lower) else "mention"
                primary_concepts.append({"concept": cname, "module": module, "evidence_type": evidence_type, "note": ""})

    for pat_a, pat_b, from_c, from_m, rel, to_c, to_m in RELATIONSHIP_PATTERNS:
        match_a = bool(re.search(pat_a, text_lower)) if pat_a else True
        match_b = bool(re.search(pat_b, text_lower)) if pat_b else True
        if match_a and match_b:
            cross_module_relationships.append({
                "from": {"concept": from_c, "module": from_m},
                "relationship": rel,
                "to": {"concept": to_c, "module": to_m},
                "justification": "detected by code pattern",
                "chunk": chunk_id,
            })

    return {
        "chunk_id": chunk_id,
        "source": source,
        "classified_by": "code",
        "primary_concepts": primary_concepts,
        "cross_module_relationships": cross_module_relationships,
        "concept_count": len(primary_concepts),
        "relationship_count": len(cross_module_relationships),
    }


def ai_extract_batch(batch: list[dict], module_context: str, model: str) -> list[dict]:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    except ImportError:
        print("  [ERROR] anthropic not installed")
        return []

    prompt_chunks = "\n\n---\n\n".join([
        f"CHUNK_ID: {c['chunk_id']}\nSOURCE: {c.get('source','')}\nTEXT:\n{c['text'][:1000]}"
        for c in batch
    ])

    prompt = f"""You are extracting domain evidence from game rulebook chunks.

MODULES AND CONCEPTS:
{module_context}

For each chunk, output a JSON object (one per line):
{{
  "chunk_id": "id",
  "primary_concepts": [
    {{"concept": "ConceptName", "module": "ModuleName", "evidence_type": "definition|mention", "note": "what this chunk says"}}
  ],
  "cross_module_relationships": [
    {{
      "from": {{"concept": "ConceptA", "module": "ModuleA"}},
      "relationship": "inherits|produces|uses|modifies|constrained_by|targets|impairs",
      "to": {{"concept": "ConceptB", "module": "ModuleB"}},
      "justification": "cite the mechanic that proves this",
      "chunk": "chunk_id"
    }}
  ]
}}

Rules:
- A chunk may evidence concepts in MULTIPLE modules simultaneously
- Record cross-module relationships at read time — do not defer
- For inheritance: only if mechanics share the same resolution path (substitutability proven)
- If no domain content: {{"chunk_id": "id", "primary_concepts": [], "cross_module_relationships": []}}
- Output ONLY JSON lines, one per chunk

CHUNKS:
{prompt_chunks}"""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        results = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("{"):
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return results
    except Exception as e:
        print(f"  [ERROR] AI call failed: {e}")
        return []


def main():
    base = Path(__file__).resolve().parent
    skill_dir = base.parent.parent.parent.parent

    parser = argparse.ArgumentParser()
    parser.add_argument("--step1", default=str(base.parent.parent / "step1-output-v2.json"))
    parser.add_argument("--chunks", default=str(skill_dir / "test/mm3/solution/context/context_chunks.json"))
    parser.add_argument("--output", default=str(base / "chunk_evidence.json"))
    parser.add_argument("--model", default="claude-haiku-4-5")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--ai-threshold", type=int, default=0,
                        help="Chunks with concept_count <= this go to AI. Default 0 = only zero-evidence chunks.")
    args = parser.parse_args()

    print("Step 2a Option D — Hybrid: code evidence + AI for uncertain chunks")
    print(f"  Step1:         {args.step1}")
    print(f"  Chunks:        {args.chunks}")
    print(f"  Model:         {args.model}")
    print(f"  AI threshold:  concept_count <= {args.ai_threshold}")

    step1 = json.loads(Path(args.step1).read_text(encoding="utf-8"))
    chunks = json.loads(Path(args.chunks).read_text(encoding="utf-8"))
    term_index = build_term_index(step1)
    module_context = build_module_context(step1)

    t_start = time.time()
    evidence_results = {}
    ai_fallback = []
    ai_calls = 0
    total_concepts = 0
    total_relationships = 0

    # Code pass
    for chunk in chunks:
        cid = chunk["chunk_id"]
        result = extract_evidence_code(chunk.get("text", ""), cid, chunk.get("source", ""), term_index)
        if result["concept_count"] <= args.ai_threshold:
            ai_fallback.append(chunk)
        else:
            evidence_results[cid] = result
            total_concepts += result["concept_count"]
            total_relationships += result["relationship_count"]

    print(f"\n  Code pass: {len(evidence_results)} extracted, {len(ai_fallback)} to AI")

    # AI pass for uncertain chunks
    for i in range(0, len(ai_fallback), args.batch_size):
        batch = ai_fallback[i:i + args.batch_size]
        batch_num = i // args.batch_size + 1
        total_ai_batches = (len(ai_fallback) + args.batch_size - 1) // args.batch_size
        print(f"  AI batch {batch_num}/{total_ai_batches} ({len(batch)} chunks)...")

        results = ai_extract_batch(batch, module_context, args.model)
        ai_calls += 1

        result_map = {r.get("chunk_id"): r for r in results}
        for chunk in batch:
            cid = chunk["chunk_id"]
            r = result_map.get(cid, {"chunk_id": cid, "primary_concepts": [], "cross_module_relationships": []})
            r["source"] = chunk.get("source", "")
            r["classified_by"] = "ai"
            r["concept_count"] = len(r.get("primary_concepts", []))
            r["relationship_count"] = len(r.get("cross_module_relationships", []))
            evidence_results[cid] = r
            total_concepts += r["concept_count"]
            total_relationships += r["relationship_count"]

    elapsed = time.time() - t_start

    output = {
        "option": "D",
        "description": "Hybrid: code signals extract evidence; AI handles zero-evidence chunks for deeper extraction.",
        "ai_calls": ai_calls,
        "ai_model": args.model,
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(chunks),
        "code_classified": len(chunks) - len(ai_fallback),
        "ai_classified": len(ai_fallback),
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_relationships,
        "evidence": list(evidence_results.values()),
    }

    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    run_log = {
        "option": "D",
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(chunks),
        "ai_calls": ai_calls,
        "ai_model": args.model,
        "code_classified": len(chunks) - len(ai_fallback),
        "ai_classified": len(ai_fallback),
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_relationships,
    }
    (base / "run_log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")

    print(f"\n  Done in {elapsed:.3f}s — {ai_calls} AI batch calls")
    print(f"  Code classified:          {len(chunks) - len(ai_fallback)}")
    print(f"  AI classified:            {len(ai_fallback)}")
    print(f"  Total concept mentions:   {total_concepts}")
    print(f"  Cross-module relationships:{total_relationships}")
    print(f"  Output: {args.output}")


if __name__ == "__main__":
    main()
