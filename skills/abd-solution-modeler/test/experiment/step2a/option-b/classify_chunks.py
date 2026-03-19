"""Step 2a Option B — AI reads every chunk and extracts evidence + relationships.

Writes progress after EVERY batch:
  progress.log  — human-readable line per batch with timing and counts
  chunk_evidence.json — updated after every batch (resumable)
  run_log.json  — written on completion

Requires: OPENAI_API_KEY (loaded from .secrets if not in environment)
"""
import argparse
import json
import os
import re
import time
from pathlib import Path


def _load_secrets():
    secrets_path = Path(__file__).resolve().parent.parent.parent / ".secrets"
    if not secrets_path.exists():
        return
    for line in secrets_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key and not os.environ.get(key):
                os.environ[key] = value


_load_secrets()


def build_module_context(step1: dict) -> str:
    lines = []
    for pair in step1.get("modules_and_epics", []):
        module = pair.get("module", {})
        mname = module.get("name", "")
        desc = module.get("description", "")
        concepts = [c.get("name", "") for c in module.get("concepts", []) if c.get("name")]
        lines.append(f"- {mname}: {desc}\n  Concepts: {', '.join(concepts)}")
    return "\n".join(lines)


def parse_json_objects(text: str) -> list[dict]:
    """Extract top-level JSON objects that have chunk_id."""
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


def ai_extract_batch(batch: list[dict], module_context: str, model: str, log_path: Path, batch_num: int) -> tuple[list[dict], str]:
    """Returns (results, status). Streams response and writes raw AI output to log."""
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    except ImportError:
        return [], "api_error: openai not installed"

    prompt_chunks = "\n\n---\n\n".join([
        f"CHUNK_ID: {c['chunk_id']}\nSOURCE: {c.get('source','')}\nTEXT:\n{c['text']}"
        for c in batch
    ])

    system = "You are extracting domain evidence from game rulebook chunks. Output ONLY valid JSON objects, one per chunk, with no other text."

    user = f"""MODULES AND CONCEPTS:
{module_context}

For each chunk below, output exactly one JSON object:
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
- For inheritance: only if same resolution path (substitutability proven)
- If no domain content: {{"chunk_id": "id", "primary_concepts": [], "cross_module_relationships": []}}
- Output one JSON object per chunk, nothing else

CHUNKS:
{prompt_chunks}"""

    try:
        # Stream the response — write tokens to log as they arrive
        accumulated = []
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write(f"\n--- AI STREAM batch {batch_num} ---\n")
            log_f.flush()

            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
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
            return [], f"parse_error: no chunk_id objects. raw[:200]={text[:200]!r}"
        return results, "ok"
    except Exception as e:
        return [], f"api_error: {e}"


def write_progress(log_path: Path, line: str):
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

    print("Step 2a Option B - AI (OpenAI) chunk evidence extraction")
    print(f"  Step1:      {args.step1}")
    print(f"  Chunks:     {args.chunks}")
    print(f"  Model:      {args.model}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  API key:    {'set' if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}")
    print(f"  Progress:   {progress_path}")

    step1 = json.loads(Path(args.step1).read_text(encoding="utf-8"))
    chunks = json.loads(Path(args.chunks).read_text(encoding="utf-8"))
    module_context = build_module_context(step1)

    # Clear progress log (total_batches computed below after batching)
    progress_path.write_text(
        f"Option B progress log\nModel: {args.model}  Chunks: {len(chunks)}  Full text: yes\n"
        f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'='*60}\n",
        encoding="utf-8"
    )

    t_start = time.time()
    evidence_results = []
    ai_calls = 0
    total_concepts = 0
    total_relationships = 0
    errors = 0

    # Build batches — oversized chunks (>15k chars) get their own batch
    OVERSIZE_THRESHOLD = 15000
    batches = []
    current_batch = []
    for chunk in chunks:
        if len(chunk["text"]) > OVERSIZE_THRESHOLD:
            if current_batch:
                batches.append(current_batch)
                current_batch = []
            batches.append([chunk])  # alone
        else:
            current_batch.append(chunk)
            if len(current_batch) >= args.batch_size:
                batches.append(current_batch)
                current_batch = []
    if current_batch:
        batches.append(current_batch)

    total_batches = len(batches)
    print(f"\n  Chunks: {len(chunks)} -> {total_batches} batches (oversized chunks get own batch)\n")

    for batch_num, batch in enumerate(batches, 1):
        batch_chunk_ids = [c["chunk_id"] for c in batch]

        t_batch = time.time()
        print(f"  Batch {batch_num}/{total_batches}  chunks: {batch_chunk_ids} ...")

        results, status = ai_extract_batch(batch, module_context, args.model, progress_path, batch_num)
        ai_calls += 1
        batch_elapsed = time.time() - t_batch

        # Map results by chunk_id
        result_map = {r.get("chunk_id"): r for r in results}
        batch_concepts = 0
        batch_relationships = 0
        batch_results = []

        for chunk in batch:
            cid = chunk["chunk_id"]
            r = result_map.get(cid, {"chunk_id": cid, "primary_concepts": [], "cross_module_relationships": []})
            r["source"] = chunk.get("source", "")
            r["classified_by"] = "ai"
            r["concept_count"] = len(r.get("primary_concepts", []))
            r["relationship_count"] = len(r.get("cross_module_relationships", []))
            batch_concepts += r["concept_count"]
            batch_relationships += r["relationship_count"]
            total_concepts += r["concept_count"]
            total_relationships += r["relationship_count"]
            evidence_results.append(r)
            batch_results.append(r)

        if status != "ok":
            errors += 1

        # Progress log entry
        elapsed_total = time.time() - t_start
        progress_line = (
            f"[{time.strftime('%H:%M:%S')}] "
            f"Batch {batch_num:3d}/{total_batches}  "
            f"status={status[:8] if len(status)>8 else status:8s}  "
            f"concepts={batch_concepts:3d}  rels={batch_relationships:2d}  "
            f"batch_time={batch_elapsed:.1f}s  total={elapsed_total:.0f}s"
        )
        print(f"    -> {progress_line[len('[HH:MM:SS] '):]}")
        write_progress(progress_path, progress_line)

        # Write AI results detail to progress log
        for r in batch_results:
            cid = r["chunk_id"]
            nc = r["concept_count"]
            nr = r["relationship_count"]
            concepts_brief = ", ".join(
                f"{c['concept']}({c.get('evidence_type','?')[:3]})"
                for c in r.get("primary_concepts", [])[:5]
            )
            write_progress(progress_path, f"        {cid}  C:{nc} R:{nr}  {concepts_brief}")

        # Write chunk_evidence.json after every batch (incremental)
        partial_output = {
            "option": "B",
            "description": "AI (OpenAI) reads every chunk, extracts concepts + cross-module relationships. No code pre-filter.",
            "ai_calls": ai_calls,
            "ai_model": args.model,
            "elapsed_seconds": round(time.time() - t_start, 3),
            "chunk_count": len(chunks),
            "batches_complete": batch_num,
            "batches_total": total_batches,
            "total_concept_mentions": total_concepts,
            "total_relationships_detected": total_relationships,
            "errors": errors,
            "status": "in_progress" if batch_num < total_batches else "complete",
            "evidence": evidence_results,
        }
        output_path.write_text(json.dumps(partial_output, indent=2), encoding="utf-8")

    elapsed = time.time() - t_start

    # Final run_log
    run_log = {
        "option": "B",
        "elapsed_seconds": round(elapsed, 3),
        "chunk_count": len(chunks),
        "ai_calls": ai_calls,
        "ai_model": args.model,
        "total_concept_mentions": total_concepts,
        "total_relationships_detected": total_relationships,
        "errors": errors,
        "status": "complete",
    }
    (base / "run_log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")
    write_progress(progress_path, f"\nCOMPLETE  elapsed={elapsed:.1f}s  calls={ai_calls}  concepts={total_concepts}  rels={total_relationships}  errors={errors}")

    print(f"\n  Done in {elapsed:.1f}s  |  {ai_calls} AI calls  |  {errors} errors")
    print(f"  Concepts:      {total_concepts}")
    print(f"  Relationships: {total_relationships}")
    print(f"  Progress log:  {progress_path}")
    print(f"  Output:        {output_path}")


if __name__ == "__main__":
    main()
