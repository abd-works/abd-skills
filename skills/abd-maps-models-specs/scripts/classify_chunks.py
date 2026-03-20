"""Step 2 — Chunk classification with two-pass enrichment.

Writes directly to map-model-spec.json. Evidence (chunk_evidence, cross_module_relationships)
is merged into the spec — no separate index files.

--chunk-pct controls how much of each chunk's text is sent to the AI (default 100%).

  100% — full chunk text sent. Best coverage. Larger prompts, more cost.
   50% — first half of each chunk sent. Faster, cheaper. Misses content in second half.
   25% — first quarter sent. Equivalent to the original 1,000-char truncation bug.

Every chunk goes to the AI regardless of --chunk-pct.
The percentage controls the character slice within each chunk: text[:int(len * pct/100)].

Pass 2 (code, always runs after AI):
  Runs code signals on ALL chunks using the full concept list discovered in Pass 1.
  This catches mentions of AI-discovered concepts (e.g. HeroPoint, ExtraEffort)
  that appear in chunks where the AI only saw partial text.
  Results are merged — AI evidence takes precedence, code fills gaps.

Token estimation:
  Samples 10% of chunks at the configured --chunk-pct to get realistic average size.
  Sets batch size so each batch is ~8,000 tokens of chunk text.

Writes progress after every batch. Streams AI output to progress.log.
Writes map-model-spec.json after every batch with merged evidence (chunk_evidence per concept,
chunk_ids.identified/provisional, cross_module_relationships).

Usage:
    python classify_chunks.py --spec map-model-spec.json
    python classify_chunks.py --chunk-pct 50 --spec path/to/map-model-spec.json

Requires: OPENAI_API_KEY (loaded from .secrets)
"""
import argparse
import json
import math
import os
import re
import time
from pathlib import Path

# ── Secrets ───────────────────────────────────────────────────────────────────
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

# ── Code signals (same as Option C / E) ──────────────────────────────────────
MODULE_COOCCURRENCE = {
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
_RULE_TRIGGERS = re.compile(r'\b(if|when|unless|must|may not|cannot|can only|requires?|is required|on success|on failure|at least|no more than)\b', re.IGNORECASE)
_EXAMPLE_TRIGGERS = re.compile(r'\b(for example|for instance|such as|e\.g\.|a hero with|a character with)\b', re.IGNORECASE)
_ALLCAPS_WORD = re.compile(r'^[A-Z][A-Z\s\-/]{2,}$')
_TABLE_HEADER_SIGNATURES = {
    "Effect": ["ACTION", "RANGE", "DURATION", "COST"],
    "Power": ["ACTION", "RANGE", "DURATION", "COST"],
    "Ability": ["STRENGTH", "STAMINA", "AGILITY"],
    "Defense": ["DODGE", "PARRY", "FORTITUDE", "TOUGHNESS", "WILL"],
    "Skill": ["ACROBATICS", "ATHLETICS", "DECEPTION"],
    "Condition": ["DAZED", "STAGGERED", "INCAPACITATED"],
    "Action": ["STANDARD", "MOVE", "FREE", "REACTION"],
}

def _has_columnar_table(text):
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
    positions = [m.start() for m in re.finditer(r'\b' + re.escape(cname.lower()) + r'\b', text_lower)]
    for pos in positions:
        window = text_lower[max(0, pos-150):pos+150]
        if _RULE_TRIGGERS.search(window):
            types.append("rule")
            break
    for pos in positions:
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

# ── AI extraction ─────────────────────────────────────────────────────────────
def build_module_context(step1):
    lines = []
    for pair in step1.get("modules_and_epics", []):
        module = pair.get("module", {})
        mname = module.get("name", "")
        desc = module.get("description", "")
        concepts = [c.get("name", "") for c in module.get("concepts", []) if c.get("name")]
        lines.append(f"- {mname}: {desc}\n  Concepts: {', '.join(concepts)}")
    return "\n".join(lines)

def build_extended_context(step1, discovered_concepts: set[str]) -> str:
    """Module context augmented with concepts discovered in Pass 1."""
    base = build_module_context(step1)
    step1_names = {
        c.get("name", "")
        for pair in step1.get("modules_and_epics", [])
        for c in pair.get("module", {}).get("concepts", [])
    }
    new_names = sorted(discovered_concepts - step1_names)
    if new_names:
        base += f"\n\nAdditional concepts discovered in Pass 1 (use these names consistently):\n"
        base += "\n".join(f"  - {n}" for n in new_names)
    return base

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

def ai_extract_batch(batch, module_context, model, log_path, batch_label, chunk_pct=100.0):
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    except ImportError:
        return [], "api_error: openai not installed"

    prompt_chunks = "\n\n---\n\n".join([
        f"CHUNK_ID: {c['chunk_id']}\nSOURCE: {c.get('source','')}\nTEXT:\n{c['text'][:int(len(c['text']) * chunk_pct / 100)]}"
        for c in batch
    ])

    system = "You are extracting domain evidence from a game rulebook. Read each chunk fully — do not skip content at the end. Output ONLY valid JSON objects, one per chunk."

    user = f"""MODULES AND CONCEPTS (use these module names; you may discover additional concept names not listed):
{module_context}

For each chunk, output exactly one JSON object:
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
- Read the ENTIRE chunk text — do not stop early
- A chunk may evidence concepts in multiple modules
- You may name concepts not in the list above if you find them in the text
- For inheritance: only if same resolution path (substitutability proven)
- If no domain content: {{"chunk_id": "id", "primary_concepts": [], "cross_module_relationships": []}}
- Output one JSON object per chunk, nothing else

CHUNKS:
{prompt_chunks}"""

    try:
        accumulated = []
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write(f"\n--- AI STREAM {batch_label} ---\n")
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

# ── Chunk loading (context_chunks.json or context_index + chunks/*.md) ─────────
def load_chunks(chunks_path: str) -> list[dict]:
    """Load chunks from context_chunks.json (legacy) or context_index.json + chunks/*.md (new)."""
    p = Path(chunks_path)
    if p.is_file():
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        raise ValueError(f"Expected list of chunks, got {type(data)}")
    # Directory: look for context_index + chunks/
    if p.is_dir():
        index_path = p / "context_index.json"
        chunks_dir = p / "chunks"
        if index_path.exists() and chunks_dir.is_dir():
            index = json.loads(index_path.read_text(encoding="utf-8"))
            forward = index.get("forward_index", {})
            result = []
            for cid, meta in forward.items():
                chunk_file = chunks_dir / f"{cid}.md"
                if chunk_file.exists():
                    text = chunk_file.read_text(encoding="utf-8")
                    # Strip YAML front matter to get body
                    if text.startswith("---"):
                        parts = text.split("---", 2)
                        text = parts[2].lstrip("\n") if len(parts) > 2 else ""
                    result.append({
                        "chunk_id": cid,
                        "source": meta.get("source", ""),
                        "text": text,
                    })
            return result
        # Fallback: context_chunks.json in same dir
        legacy = p / "context_chunks.json"
        if legacy.exists():
            return json.loads(legacy.read_text(encoding="utf-8"))
        raise FileNotFoundError(f"No context_index.json+chunks/ or context_chunks.json in {p}")
    raise FileNotFoundError(f"Chunks path not found: {chunks_path}")


# ── Token estimation ──────────────────────────────────────────────────────────
CHARS_PER_TOKEN = 4
TARGET_CHUNK_TOKENS_PER_BATCH = 8000
OVERSIZE_THRESHOLD = 15000  # chars — gets own batch

def estimate_batch_size(chunks: list[dict], chunk_pct: float, sample_pct: float = 0.1) -> tuple[int, int]:
    """Sample chunks at the configured chunk_pct to estimate average sent char count."""
    n = max(1, int(len(chunks) * sample_pct))
    step = len(chunks) // n
    sample = [chunks[i] for i in range(0, len(chunks), step)][:n]
    avg_chars = sum(int(len(c["text"]) * chunk_pct / 100) for c in sample) / len(sample)
    avg_tokens = avg_chars / CHARS_PER_TOKEN
    batch_size = max(1, int(TARGET_CHUNK_TOKENS_PER_BATCH / avg_tokens))
    return batch_size, round(avg_tokens)

def make_batches(chunks: list[dict], batch_size: int) -> list[list[dict]]:
    """Build batches; oversized chunks get their own batch."""
    batches = []
    current = []
    for chunk in chunks:
        if len(chunk["text"]) > OVERSIZE_THRESHOLD:
            if current:
                batches.append(current)
                current = []
            batches.append([chunk])
        else:
            current.append(chunk)
            if len(current) >= batch_size:
                batches.append(current)
                current = []
    if current:
        batches.append(current)
    return batches


# ── Merge evidence into map-model-spec ─────────────────────────────────────────
IDENTIFIED_TYPES = {"definition", "rule", "example", "table"}
PROVISIONAL_TYPES = {"mention"}


def merge_evidence_into_spec(evidence_by_id: dict[str, dict], spec: dict) -> dict:
    """Merge chunk evidence into map-model-spec. Writes chunk_evidence per concept,
    chunk_ids (derived), chunk_ids.identified/provisional at pair level,
    and cross_module_relationships at top level. Preserves all existing spec structure."""
    from collections import defaultdict

    # (module, concept) -> {identified: set, provisional: set, evidence: [(cid, ev_type, note)]}
    module_concept_data: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"identified": set(), "provisional": set(), "evidence": []}
    )
    module_pair_chunks: dict[str, dict[str, set]] = defaultdict(
        lambda: {"identified": set(), "provisional": set()}
    )
    cross_module_relationships: list[dict] = []

    for entry in evidence_by_id.values():
        cid = entry.get("chunk_id") or entry.get("chunk")
        if not cid:
            continue
        for pc in entry.get("primary_concepts", []):
            module = pc.get("module", "")
            concept = pc.get("concept", "")
            if not module:
                continue
            ev_type = pc.get("evidence_type") or pc.get("evidence_types")
            if isinstance(ev_type, list):
                ev_type = ev_type[0] if ev_type else "mention"
            ev_type = (ev_type or "mention").lower()
            note = pc.get("note", "")

            key = (module, concept)
            module_concept_data[key]["evidence"].append({
                "chunk_id": cid,
                "evidence_type": ev_type,
                "note": note,
            })
            if ev_type in IDENTIFIED_TYPES:
                module_concept_data[key]["identified"].add(cid)
                module_pair_chunks[module]["identified"].add(cid)
            else:
                module_concept_data[key]["provisional"].add(cid)
                module_pair_chunks[module]["provisional"].add(cid)

        for rel in entry.get("cross_module_relationships", []):
            rel_copy = dict(rel)
            rel_copy["chunk"] = cid
            cross_module_relationships.append(rel_copy)

    pairs = spec.get("modules_and_epics", [])
    result_pairs = []

    for pair in pairs:
        module = pair.get("module", {})
        epic = pair.get("epic", {})
        module_name = module.get("name", "")
        if not module_name:
            result_pairs.append(pair)
            continue

        pair_identified = module_pair_chunks.get(module_name, {}).get("identified", set())
        pair_provisional = module_pair_chunks.get(module_name, {}).get("provisional", set())
        pair_provisional = pair_provisional - pair_identified

        concepts_out = []
        for c in module.get("concepts", []):
            cname = c.get("name", "")
            key = (module_name, cname)
            data = module_concept_data.get(key, {})
            evidence_list = data.get("evidence", [])
            all_cids = sorted(data.get("identified", set()) | data.get("provisional", set()))

            # Preserve existing concept fields; add/overwrite chunk_evidence and chunk_ids
            concept_out = dict(c)
            concept_out["chunk_evidence"] = evidence_list
            concept_out["chunk_ids"] = all_cids if all_cids else concept_out.get("chunk_ids", [])

            concepts_out.append(concept_out)

        result_pairs.append({
            **pair,
            "module": {**module, "concepts": concepts_out},
            "chunk_ids": {
                "identified": sorted(pair_identified),
                "provisional": sorted(pair_provisional),
                "ambiguous": pair.get("chunk_ids", {}).get("ambiguous", []),
            },
        })

    out = dict(spec)
    out["modules_and_epics"] = result_pairs
    out["cross_module_relationships"] = cross_module_relationships
    return out


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    base = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=str(base.parent / "map-model-spec.json"),
                        help="Path to map-model-spec.json. Read for module context; written with merged evidence.")
    parser.add_argument("--chunks", default=str(base.parent / "test/mm3/context"),
                        help="Path to context_chunks.json (legacy) or context dir with context_index.json + chunks/")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--chunk-pct", type=float, default=100.0,
                        help="Percent of each chunk's text to send to AI. Default 100 (full text).")
    args = parser.parse_args()

    progress_path = base / "progress.log"
    spec_path = Path(args.spec)
    chunk_pct = min(100.0, max(1.0, args.chunk_pct))

    print(f"Step 2 Option F — Configurable chunk text coverage")
    print(f"  Chunk text sent to AI: {chunk_pct:.0f}% of each chunk")
    print(f"  All {'{chunks}'} chunks go to AI — percentage controls text slice per chunk")
    print(f"  Pass 2 (code): runs on all chunks using concepts discovered in Pass 1")
    print(f"  Model:         {args.model}")
    print(f"  API key:       {'set' if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}")

    if not spec_path.exists():
        print(f"ERROR: Spec file not found: {spec_path}")
        return 1
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    try:
        all_chunks = load_chunks(args.chunks)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1

    # Estimate batch size based on sliced chunk size at configured chunk_pct
    batch_size, avg_tokens = estimate_batch_size(all_chunks, chunk_pct)
    print(f"\n  Corpus:       {len(all_chunks)} chunks")
    print(f"  Avg sent:     ~{avg_tokens} tokens/chunk at {chunk_pct:.0f}% text")
    print(f"  Auto batch:   {batch_size} chunks/batch (~{batch_size * avg_tokens:,} tokens/batch)")
    print(f"  Pass 1:       {len(all_chunks)} chunks (AI, {chunk_pct:.0f}% of each chunk's text)")
    print(f"  Pass 2:       {len(all_chunks)} chunks (code, full text, uses Pass 1 concept list)")

    progress_path.write_text(
        f"Option F progress log\n"
        f"Model: {args.model}  chunk-pct: {chunk_pct:.0f}%  Chunks: {len(all_chunks)}\n"
        f"Auto batch size: {batch_size} (avg {avg_tokens} tokens sent/chunk)\n"
        f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'='*60}\n",
        encoding="utf-8"
    )

    t_start = time.time()
    evidence_by_id: dict[str, dict] = {}
    ai_calls = 0
    errors = 0
    discovered_concepts: set[str] = set()

    # ── PASS 1: AI on all chunks, chunk_pct of each chunk's text ─────────────
    module_context = build_module_context(spec)
    pass1_batches = make_batches(all_chunks, batch_size)
    total_p1 = len(pass1_batches)
    print(f"\nPASS 1 (AI): {len(all_chunks)} chunks in {total_p1} batches, {chunk_pct:.0f}% of each chunk's text\n")
    write_progress(progress_path, f"\nPASS 1 (AI): {len(all_chunks)} chunks, {total_p1} batches, {chunk_pct:.0f}% text/chunk")

    for batch_num, batch in enumerate(pass1_batches, 1):
        batch_ids = [c["chunk_id"] for c in batch]
        t_batch = time.time()
        print(f"  P1 Batch {batch_num}/{total_p1}  ({len(batch)} chunks)  {batch_ids[:3]}{'...' if len(batch_ids)>3 else ''}")

        results, status = ai_extract_batch(batch, module_context, args.model, progress_path, f"P1-{batch_num}/{total_p1}", chunk_pct)
        ai_calls += 1
        batch_elapsed = time.time() - t_batch

        result_map = {r.get("chunk_id"): r for r in results}
        batch_concepts = 0
        batch_rels = 0

        for chunk in batch:
            cid = chunk["chunk_id"]
            r = result_map.get(cid, {"chunk_id": cid, "primary_concepts": [], "cross_module_relationships": []})
            r["source"] = chunk.get("source", "")
            r["classified_by"] = "ai"
            r["concept_count"] = len(r.get("primary_concepts", []))
            r["relationship_count"] = len(r.get("cross_module_relationships", []))
            batch_concepts += r["concept_count"]
            batch_rels += r["relationship_count"]
            evidence_by_id[cid] = r
            for pc in r.get("primary_concepts", []):
                if pc.get("concept"):
                    discovered_concepts.add(pc["concept"])

        if status != "ok":
            errors += 1

        elapsed_total = time.time() - t_start
        progress_line = (
            f"[{time.strftime('%H:%M:%S')}] P1 Batch {batch_num:3d}/{total_p1}  "
            f"status={status[:8]:8s}  concepts={batch_concepts:3d}  rels={batch_rels:2d}  "
            f"batch_time={batch_elapsed:.1f}s  total={elapsed_total:.0f}s"
        )
        print(f"    -> {progress_line[len('[HH:MM:SS] '):]}")
        write_progress(progress_path, progress_line)

        # Write incrementally to map-model-spec
        merged = merge_evidence_into_spec(evidence_by_id, spec)
        _write_spec(spec_path, merged, ai_calls, args, len(all_chunks),
                    chunk_pct, batch_num, total_p1, errors, t_start, "pass1")

    print(f"\n  Pass 1 complete. Discovered {len(discovered_concepts)} unique concept names.")
    write_progress(progress_path, f"\nPASS 1 COMPLETE. Discovered {len(discovered_concepts)} concept names.")

    # ── PASS 2: Code on all chunks using extended concept list ────────────────
    print(f"\nPASS 2 (code): all {len(all_chunks)} chunks, full text, {len(discovered_concepts)} concept names from Pass 1")
    write_progress(progress_path, f"\nPASS 2 (code): {len(all_chunks)} chunks, {len(discovered_concepts)} concepts")

    # Build extended term index: spec concepts + all discovered in Pass 1
    extended_index = {}
    for pair in spec.get("modules_and_epics", []):
        module = pair.get("module", {})
        mname = module.get("name", "")
        if not mname:
            continue
        concepts = {c.get("name", ""): [] for c in module.get("concepts", []) if c.get("name")}
        extended_index[mname] = concepts

    step1_names = {name for m in extended_index.values() for name in m}
    new_discovered = discovered_concepts - step1_names
    if new_discovered:
        extended_index["Discovered"] = {name: [] for name in new_discovered}

    p2_new_concepts = 0
    p2_new_rels = 0
    for chunk in all_chunks:
        cid = chunk["chunk_id"]
        code_result = extract_evidence_code(chunk["text"], cid, chunk.get("source", ""), extended_index)

        if cid not in evidence_by_id:
            # Chunk not in AI results (shouldn't happen at 100% but just in case)
            evidence_by_id[cid] = code_result
        else:
            # Merge: add code-found concepts/rels not already in AI results
            existing = evidence_by_id[cid]
            existing_concept_names = {pc["concept"] for pc in existing.get("primary_concepts", [])}
            new_concepts = [pc for pc in code_result["primary_concepts"] if pc["concept"] not in existing_concept_names]
            existing_rel_keys = {
                (r["from"]["concept"], r["relationship"], r["to"]["concept"])
                for r in existing.get("cross_module_relationships", [])
            }
            new_rels = [
                r for r in code_result["cross_module_relationships"]
                if (r["from"]["concept"], r["relationship"], r["to"]["concept"]) not in existing_rel_keys
            ]
            existing["primary_concepts"].extend(new_concepts)
            existing["cross_module_relationships"].extend(new_rels)
            existing["concept_count"] = len(existing["primary_concepts"])
            existing["relationship_count"] = len(existing["cross_module_relationships"])
            p2_new_concepts += len(new_concepts)
            p2_new_rels += len(new_rels)

    print(f"  Pass 2 complete. Code added {p2_new_concepts} new concept mentions, {p2_new_rels} new relationships.")
    write_progress(progress_path, f"PASS 2 COMPLETE. Code added: {p2_new_concepts} concepts, {p2_new_rels} rels.")

    # ── Final output ──────────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    evidence_list = list(evidence_by_id.values())
    total_concepts = sum(e["concept_count"] for e in evidence_list)
    total_rels = sum(e["relationship_count"] for e in evidence_list)

    run_log = {
        "option": "F",
        "chunk_pct": chunk_pct,
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(all_chunks),
        "ai_calls": ai_calls,
        "ai_model": args.model,
        "auto_batch_size": batch_size,
        "avg_tokens_sent_per_chunk": avg_tokens,
        "discovered_concepts": len(discovered_concepts),
        "pass2_new_concepts": p2_new_concepts,
        "pass2_new_relationships": p2_new_rels,
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_rels,
        "errors": errors,
        "status": "complete",
    }
    (base / "run_log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")
    merged = merge_evidence_into_spec(evidence_by_id, spec)
    _write_spec(spec_path, merged, ai_calls, args, len(all_chunks),
                chunk_pct, total_p1, total_p1, errors, t_start, "complete")

    write_progress(progress_path,
                   f"\nCOMPLETE  elapsed={elapsed:.1f}s  ai_calls={ai_calls}  "
                   f"concepts={total_concepts}  rels={total_rels}  discovered={len(discovered_concepts)}  errors={errors}")

    print(f"\n  Done in {elapsed:.1f}s  |  {ai_calls} AI calls  |  {errors} errors")
    print(f"  Unique concepts discovered: {len(discovered_concepts)}")
    print(f"  Total concept mentions:     {total_concepts}")
    print(f"  Total relationships:        {total_rels}")
    print(f"  Wrote evidence to {spec_path}")
    return 0


def _write_spec(spec_path: Path, merged_spec: dict, ai_calls: int, args, chunk_count: int,
                chunk_pct: float, p1_done: int, p1_total: int, errors: int, t_start: float, status: str):
    """Write merged map-model-spec with evidence. Adds classify_run metadata for provenance."""
    total_concepts = sum(
        len(c.get("chunk_evidence", []))
        for pair in merged_spec.get("modules_and_epics", [])
        for c in pair.get("module", {}).get("concepts", [])
    )
    total_rels = len(merged_spec.get("cross_module_relationships", []))
    out = dict(merged_spec)
    out["chunk_classify_run"] = {
        "option": "F",
        "description": f"AI reads {chunk_pct:.0f}% of each chunk's text. Code enriches with full text.",
        "chunk_pct": chunk_pct,
        "ai_calls": ai_calls,
        "ai_model": args.model,
        "elapsed_seconds": round(time.time() - t_start, 3),
        "chunk_count": chunk_count,
        "pass1_batches_complete": p1_done,
        "pass1_batches_total": p1_total,
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_rels,
        "errors": errors,
        "status": status,
    }
    spec_path.write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main() or 0)
