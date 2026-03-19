"""Step 2a Option E — True hybrid: code signals for all chunks, AI for high-density low-signal chunks.

Strategy:
  Pass 1 (code): Run all code signals (term match, co-occurrence, relationships) on all 267 chunks.
  Pass 2 (targeting): Identify chunks where code found <= 3 concepts BUT chunk has
                      high-density structural indicators (stat blocks, budget tables, all-caps runs).
  Pass 3 (AI): Send only those targeted chunks to AI for deep extraction.
  Merge: Combine code evidence (all chunks) + AI evidence (targeted chunks).

Expected: ~46 chunks to AI (~10 batch calls), vs 54 for full Option B.
Goal: Capture the character-sheet / stat-block relationships that code misses,
      without paying for AI on prose chunks that code handles well.

Writes progress after every batch. Streams AI output to progress.log.

Requires: OPENAI_API_KEY (loaded from .secrets)
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

# ── Load secrets ──────────────────────────────────────────────────────────────
def _load_secrets():
    secrets_path = Path(__file__).resolve().parent.parent.parent / ".secrets"
    if not secrets_path.exists():
        return
    for line in secrets_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key and not os.environ.get(key):
                os.environ[key] = value

_load_secrets()

# ── Code signals (same as Option C) ──────────────────────────────────────────
MODULE_COOCCURRENCE: dict[str, list[tuple[str, str]]] = {
    "Resolution": [("difficulty class", "check"), ("dc", "roll"), ("degree", "success"), ("degree", "failure"), ("d20", "modifier")],
    "Character": [("power points", "power level"), ("power level", "cap"), ("hero points", "complication"), ("power point", "budget")],
    "Character Traits": [("agility", "dodge"), ("stamina", "fortitude"), ("fighting", "parry"), ("awareness", "will"), ("skill rank", "ability"), ("ability rank", "skill")],
    "Powers": [("cost per rank", "effect"), ("extras", "flaws"), ("duration", "sustained"), ("alternate effect", "array"), ("power level", "effect rank")],
    "Combat": [("attack check", "defense"), ("attack", "toughness"), ("initiative", "round"), ("standard action", "move action"), ("attack bonus", "dodge")],
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
_RULE_TRIGGERS = re.compile(r'\b(if|when|unless|must|may not|cannot|can only|requires?|is required|on success|on failure|at least|no more than|equal to|divided by)\b', re.IGNORECASE)
_EXAMPLE_TRIGGERS = re.compile(r'\b(for example|for instance|such as|e\.g\.|as an example|a hero with|a character with)\b', re.IGNORECASE)
_ALLCAPS_WORD = re.compile(r'^[A-Z][A-Z\s\-/]{2,}$')
_TABLE_HEADER_SIGNATURES = {
    "Effect": ["ACTION", "RANGE", "DURATION", "COST"],
    "Power": ["ACTION", "RANGE", "DURATION", "COST"],
    "Ability": ["STRENGTH", "STAMINA", "AGILITY", "DEXTERITY", "FIGHTING"],
    "Defense": ["DODGE", "PARRY", "FORTITUDE", "TOUGHNESS", "WILL"],
    "Skill": ["ACROBATICS", "ATHLETICS", "DECEPTION", "EXPERTISE"],
    "Condition": ["DAZED", "STAGGERED", "INCAPACITATED"],
    "Action": ["STANDARD", "MOVE", "FREE", "REACTION"],
}

# ── High-density detection (for targeting) ───────────────────────────────────
STAT_KEYWORDS = re.compile(r'\b(STRENGTH|STAMINA|AGILITY|DEXTERITY|FIGHTING|INTELLECT|AWARENESS|PRESENCE|PL\s*\d+|Power Point Totals)\b')
NUMERIC_BUDGET = re.compile(r'\d+\s*\+\s*\d+\s*\+\s*\d+')
ALLCAPS_RUN = re.compile(r'(?:^[A-Z][A-Z\s]{2,20}$\n){2,}', re.MULTILINE)

def is_high_density(text: str) -> bool:
    return bool(STAT_KEYWORDS.search(text) or NUMERIC_BUDGET.search(text) or ALLCAPS_RUN.search(text))


def build_term_index(step1: dict) -> dict:
    index = {}
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


def _has_columnar_table(text: str) -> bool:
    lines = text.split('\n')
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


def _get_evidence_types(text, text_lower, cname):
    types = []
    defpat = re.compile(r'\b' + re.escape(cname.lower()) + r'\s*(?:is\s+a\b|refers?\s+to\b|:|—|–)', re.IGNORECASE)
    if defpat.search(text_lower):
        types.append("definition")
    concept_pos = [m.start() for m in re.finditer(r'\b' + re.escape(cname.lower()) + r'\b', text_lower)]
    for pos in concept_pos:
        window = text_lower[max(0, pos-150):pos+150]
        if _RULE_TRIGGERS.search(window):
            types.append("rule")
            break
    for pos in concept_pos:
        window = text_lower[max(0, pos-150):pos+150]
        if _EXAMPLE_TRIGGERS.search(window):
            types.append("example")
            break
    if _has_columnar_table(text):
        sigs = _TABLE_HEADER_SIGNATURES.get(cname, [])
        if sigs and any(sig in text for sig in sigs):
            types.append("table")
        elif not sigs and cname.lower() in text_lower:
            types.append("table")
    if not types:
        types.append("mention")
    return types


def extract_evidence_code(text, chunk_id, source, term_index):
    text_lower = text.lower()
    primary_concepts = []
    cross_module_relationships = []
    for module, concepts in term_index.items():
        for cname in concepts:
            pattern = r'\b' + re.escape(cname.lower()) + r'\b'
            if re.search(pattern, text_lower):
                evidence_types = _get_evidence_types(text, text_lower, cname)
                primary_concepts.append({"concept": cname, "module": module, "evidence_types": evidence_types, "primary_type": evidence_types[0]})
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
        "chunk_id": chunk_id, "source": source, "classified_by": "code",
        "primary_concepts": primary_concepts, "cross_module_relationships": cross_module_relationships,
        "concept_count": len(primary_concepts), "relationship_count": len(cross_module_relationships),
    }


def build_module_context(step1):
    lines = []
    for pair in step1.get("modules_and_epics", []):
        module = pair.get("module", {})
        mname = module.get("name", "")
        desc = module.get("description", "")
        concepts = [c.get("name", "") for c in module.get("concepts", []) if c.get("name")]
        lines.append(f"- {mname}: {desc}\n  Concepts: {', '.join(concepts)}")
    return "\n".join(lines)


def parse_json_objects(text):
    text = re.sub(r'```(?:json)?\s*', '', text)
    text = re.sub(r'```', '', text)
    results = []
    depth = 0
    start = None
    candidates = []
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                candidates.append(text[start:i+1])
                start = None
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict) and "chunk_id" in obj:
                results.append(obj)
        except json.JSONDecodeError:
            pass
    return results


def ai_extract_batch(batch, module_context, model, log_path, batch_num):
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    except ImportError:
        return [], "api_error: openai not installed"

    prompt_chunks = "\n\n---\n\n".join([
        f"CHUNK_ID: {c['chunk_id']}\nSOURCE: {c.get('source','')}\nTEXT:\n{c['text']}"
        for c in batch
    ])

    system = "You are extracting domain evidence from game rulebook chunks including character sheets and stat blocks. Output ONLY valid JSON objects, one per chunk."

    user = f"""MODULES AND CONCEPTS:
{module_context}

For each chunk, output exactly one JSON object. Pay special attention to stat blocks, character sheets, and power point budget tables — these are information-dense and contain important relationships.

{{
  "chunk_id": "id",
  "primary_concepts": [
    {{"concept": "ConceptName", "module": "ModuleName", "evidence_type": "definition|mention|rule|example|table", "note": "brief"}}
  ],
  "cross_module_relationships": [
    {{
      "from": {{"concept": "ConceptA", "module": "ModuleA"}},
      "relationship": "inherits|produces|uses|modifies|constrained_by|targets|impairs",
      "to": {{"concept": "ConceptB", "module": "ModuleB"}},
      "justification": "cite the mechanic",
      "chunk": "chunk_id"
    }}
  ]
}}

Rules:
- A chunk may evidence concepts in MULTIPLE modules simultaneously
- For stat blocks: extract ALL trait types shown (Abilities, Skills, Powers, Advantages, Defenses) and their budget constraints
- For inheritance: only if same resolution path (substitutability proven)
- If no domain content: {{"chunk_id": "id", "primary_concepts": [], "cross_module_relationships": []}}
- Output one JSON object per chunk, nothing else

CHUNKS:
{prompt_chunks}"""

    try:
        accumulated = []
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write(f"\n--- AI STREAM batch {batch_num} ---\n")
            log_f.flush()
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                max_tokens=4096,
                temperature=0,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    accumulated.append(delta)
                    log_f.write(delta)
                    log_f.flush()
            log_f.write("\n--- END STREAM ---\n")
            log_f.flush()
        text = "".join(accumulated)
        results = parse_json_objects(text)
        if not results:
            return [], f"parse_error: raw[:200]={text[:200]!r}"
        return results, "ok"
    except Exception as e:
        return [], f"api_error: {e}"


def write_progress(log_path, line):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    base = Path(__file__).resolve().parent
    skill_dir = base.parent.parent.parent.parent

    parser = argparse.ArgumentParser()
    parser.add_argument("--step1", default=str(base.parent.parent / "step1-output-v2.json"))
    parser.add_argument("--chunks", default=str(skill_dir / "test/mm3/solution/context/context_chunks.json"))
    parser.add_argument("--output", default=str(base / "chunk_evidence.json"))
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--batch-size", type=int, default=3)
    args = parser.parse_args()

    progress_path = base / "progress.log"
    output_path = Path(args.output)

    print("Step 2a Option E - True hybrid: code for all, AI for high-density low-signal chunks")
    print(f"  Model: {args.model}  |  API key: {'set' if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}")

    step1 = json.loads(Path(args.step1).read_text(encoding="utf-8"))
    chunks = json.loads(Path(args.chunks).read_text(encoding="utf-8"))
    term_index = build_term_index(step1)
    module_context = build_module_context(step1)

    progress_path.write_text(
        f"Option E progress log\nModel: {args.model}\nStarted: {time.strftime('%Y-%m-%d %H:%M:%S')}\n{'='*60}\n",
        encoding="utf-8"
    )

    t_start = time.time()

    # Pass 1: code signals on all chunks
    print("\nPass 1: code signals on all 267 chunks...")
    evidence_by_id = {}
    ai_candidates = []

    for chunk in chunks:
        cid = chunk["chunk_id"]
        text = chunk.get("text", "")
        result = extract_evidence_code(text, cid, chunk.get("source", ""), term_index)
        evidence_by_id[cid] = result

        # Target for AI: low code signal + high information density
        if result["concept_count"] <= 3 and is_high_density(text):
            ai_candidates.append(chunk)

    print(f"  Code pass complete. {len(ai_candidates)} chunks targeted for AI.")
    write_progress(progress_path, f"Code pass: {len(chunks)} chunks. {len(ai_candidates)} targeted for AI.")

    # Pass 2: AI on targeted chunks
    total_ai_batches = (len(ai_candidates) + args.batch_size - 1) // args.batch_size
    print(f"\nPass 2: AI on {len(ai_candidates)} chunks ({total_ai_batches} batches)...")

    ai_calls = 0
    total_ai_concepts = 0
    total_ai_rels = 0
    errors = 0

    for i in range(0, len(ai_candidates), args.batch_size):
        batch = ai_candidates[i:i + args.batch_size]
        batch_num = i // args.batch_size + 1
        batch_ids = [c["chunk_id"] for c in batch]

        t_batch = time.time()
        print(f"  AI Batch {batch_num}/{total_ai_batches}  {batch_ids} ...")

        results, status = ai_extract_batch(batch, module_context, args.model, progress_path, batch_num)
        ai_calls += 1
        batch_elapsed = time.time() - t_batch

        result_map = {r.get("chunk_id"): r for r in results}
        batch_concepts = 0
        batch_rels = 0

        for chunk in batch:
            cid = chunk["chunk_id"]
            r = result_map.get(cid, {"chunk_id": cid, "primary_concepts": [], "cross_module_relationships": []})

            # Merge AI results INTO code results (AI supplements, doesn't replace)
            existing = evidence_by_id[cid]
            existing_concept_names = {pc["concept"] for pc in existing["primary_concepts"]}
            new_concepts = [pc for pc in r.get("primary_concepts", []) if pc["concept"] not in existing_concept_names]
            existing["primary_concepts"].extend(new_concepts)

            existing_rel_keys = {
                (rel["from"]["concept"], rel["relationship"], rel["to"]["concept"])
                for rel in existing["cross_module_relationships"]
            }
            new_rels = [
                rel for rel in r.get("cross_module_relationships", [])
                if (rel["from"]["concept"], rel["relationship"], rel["to"]["concept"]) not in existing_rel_keys
            ]
            existing["cross_module_relationships"].extend(new_rels)
            existing["concept_count"] = len(existing["primary_concepts"])
            existing["relationship_count"] = len(existing["cross_module_relationships"])
            existing["classified_by"] = "code+ai"

            batch_concepts += len(new_concepts)
            batch_rels += len(new_rels)
            total_ai_concepts += len(new_concepts)
            total_ai_rels += len(new_rels)

        if status != "ok":
            errors += 1

        elapsed_total = time.time() - t_start
        progress_line = (
            f"[{time.strftime('%H:%M:%S')}] AI Batch {batch_num:3d}/{total_ai_batches}  "
            f"status={status[:8]:8s}  new_concepts={batch_concepts:3d}  new_rels={batch_rels:2d}  "
            f"batch_time={batch_elapsed:.1f}s  total={elapsed_total:.0f}s"
        )
        print(f"    -> {progress_line[len('[HH:MM:SS] '):]}")
        write_progress(progress_path, progress_line)

        # Write incrementally
        evidence_list = list(evidence_by_id.values())
        total_concepts = sum(e["concept_count"] for e in evidence_list)
        total_rels = sum(e["relationship_count"] for e in evidence_list)
        partial = {
            "option": "E",
            "description": "Hybrid: code signals all chunks; AI supplements high-density low-signal chunks only.",
            "ai_calls": ai_calls,
            "ai_model": args.model,
            "elapsed_seconds": round(time.time() - t_start, 3),
            "chunk_count": len(chunks),
            "ai_targeted_chunks": len(ai_candidates),
            "ai_batches_complete": batch_num,
            "ai_batches_total": total_ai_batches,
            "total_concept_mentions": total_concepts,
            "total_relationships_detected": total_rels,
            "errors": errors,
            "status": "in_progress" if batch_num < total_ai_batches else "complete",
            "evidence": evidence_list,
        }
        output_path.write_text(json.dumps(partial, indent=2), encoding="utf-8")

    elapsed = time.time() - t_start
    evidence_list = list(evidence_by_id.values())
    total_concepts = sum(e["concept_count"] for e in evidence_list)
    total_rels = sum(e["relationship_count"] for e in evidence_list)

    run_log = {
        "option": "E",
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(chunks),
        "ai_calls": ai_calls,
        "ai_targeted_chunks": len(ai_candidates),
        "ai_model": args.model,
        "ai_new_concepts": total_ai_concepts,
        "ai_new_relationships": total_ai_rels,
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_rels,
        "errors": errors,
        "status": "complete",
    }
    (base / "run_log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")
    write_progress(progress_path, f"\nCOMPLETE  elapsed={elapsed:.1f}s  ai_calls={ai_calls}  ai_new_concepts={total_ai_concepts}  ai_new_rels={total_ai_rels}  errors={errors}")

    print(f"\n  Done in {elapsed:.1f}s  |  {ai_calls} AI calls (vs 54 for full B)")
    print(f"  AI added:      {total_ai_concepts} new concepts, {total_ai_rels} new relationships")
    print(f"  Total:         {total_concepts} concepts, {total_rels} relationships")
    print(f"  Progress log:  {progress_path}")
    print(f"  Output:        {output_path}")


if __name__ == "__main__":
    main()
