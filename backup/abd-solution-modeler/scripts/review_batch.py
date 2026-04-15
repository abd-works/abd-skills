#!/usr/bin/env python3
"""Serve a hypothesis review batch for AI iteration.

AI calls this script with a batch number. Script loads that batch, outputs
instructions, and tells the AI which batch to call next.

Usage:
  python scripts/review_batch.py --batch 1
  python scripts/review_batch.py --batch 2
  ...

Flow:
  1. AI runs: python scripts/review_batch.py --batch 1
  2. Script outputs batch path, concept list, and instructions
  3. AI reads the batch file, analyzes concepts, applies fixes to hypothesis.json
  4. AI runs: python scripts/review_batch.py --batch 2
  5. Repeat until batch N is the last batch
"""
import argparse
import json
from pathlib import Path

CONCEPTS_PER_BATCH = 12
CHUNK_MAX_CHARS = 2500


def load_chunk_lookup(context_path: Path) -> dict[str, str]:
    chunks_file = context_path / "context_chunks.json"
    if not chunks_file.exists():
        return {}
    data = json.loads(chunks_file.read_text(encoding="utf-8"))
    return {c["chunk_id"]: c.get("text", "") for c in data if "chunk_id" in c}


def ensure_batch_exists(workspace: Path, batch_num: int, concepts: dict) -> Path:
    """Regenerate batch file if needed so it matches current hypothesis."""
    batch_dir = workspace / "generated" / "ai_review_batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    batch_path = batch_dir / f"batch_{batch_num:03d}.md"

    concept_names = list(concepts.keys())
    start_idx = (batch_num - 1) * CONCEPTS_PER_BATCH
    batch_names = concept_names[start_idx : start_idx + CONCEPTS_PER_BATCH]
    if not batch_names:
        return batch_path

    context_path = workspace / "context"
    chunk_lookup = load_chunk_lookup(context_path)

    def truncate(text: str, max_chars: int) -> str:
        return text[:max_chars] + "\n\n[... truncated ...]" if len(text) > max_chars else text

    prompt = """## Classification instructions

For each concept below, read its referenced chunks and classify:

| Classification | Meaning |
|----------------|---------|
| **real** | Genuine domain concept with clear identity |
| **amalgamation** | Two loosely related concepts merged; should be split |
| **instance** | Example of a concept (add type property or state) |
| **subtype** | Should be under a parent in concept_hierarchy |
| **false_positive** | Chunk doesn't support the concept; remove or fix chunk_ids |

Output format (one block per concept):
```
Concept: <name>
Classification: <real|amalgamation|instance|subtype|false_positive>
Parent (if subtype): <parent concept name or "">
Suggested change: <brief description>
```

"""

    lines = [f"# Hypothesis concept review - batch {batch_num}", "", prompt, "---", ""]
    for name in batch_names:
        c = concepts[name]
        chunk_ids = c.get("chunk_ids") or []
        lines.append(f"## Concept: {name}")
        lines.append("")
        lines.append(f"Chunk count: {len(chunk_ids)}")
        if c.get("performs"):
            lines.append(f"Performs actions: {c['performs'][:5]}{'...' if len(c['performs']) > 5 else ''}")
        if c.get("receives"):
            lines.append(f"Receives actions: {c['receives'][:5]}{'...' if len(c['receives']) > 5 else ''}")
        lines.append("")
        lines.append("### Chunk texts")
        lines.append("")
        for j, cid in enumerate(chunk_ids, 1):
            text = chunk_lookup.get(cid, f"[chunk {cid} not found]")
            lines.append(f"**Chunk {j}** (`{cid}`):")
            lines.append("")
            lines.append("```")
            lines.append(truncate(text, CHUNK_MAX_CHARS))
            lines.append("```")
            lines.append("")
        lines.append("---")
        lines.append("")

    batch_path.write_text("\n".join(lines), encoding="utf-8")
    return batch_path


def main():
    parser = argparse.ArgumentParser(description="Serve hypothesis review batch for AI")
    parser.add_argument("--batch", type=int, default=1, help="Batch number (1-based)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    workspace = skill_dir / "test" / "mm3" / "solution"
    batch_dir = workspace / "generated" / "ai_review_batches"
    hypothesis_path = workspace / "generated" / "hypothesis.json"

    if not hypothesis_path.exists():
        print("ERROR: hypothesis.json not found")
        return 1

    hypothesis = json.loads(hypothesis_path.read_text(encoding="utf-8"))
    concepts = hypothesis.get("concepts", {})
    concept_names = list(concepts.keys())
    total_concepts = len(concept_names)
    total_batches = (total_concepts + CONCEPTS_PER_BATCH - 1) // CONCEPTS_PER_BATCH

    batch_num = max(1, min(args.batch, total_batches))
    start_idx = (batch_num - 1) * CONCEPTS_PER_BATCH
    end_idx = min(start_idx + CONCEPTS_PER_BATCH, total_concepts)
    batch_concepts = concept_names[start_idx:end_idx]

    batch_path = ensure_batch_exists(workspace, batch_num, concepts)

    # Output for AI
    print("=" * 60)
    print(f"HYPOTHESIS REVIEW - BATCH {batch_num} of {total_batches}")
    print("=" * 60)
    print()
    print(f"Concepts in this batch ({len(batch_concepts)}):")
    for c in batch_concepts:
        print(f"  - {c}")
    print()
    print(f"Batch file (read this): {batch_path}")
    print()
    print("-" * 60)
    print("INSTRUCTIONS")
    print("-" * 60)
    print("""
1. Read the batch file above. It contains each concept with its referenced chunk texts.

2. For each concept, classify based on chunk content:
   - real         = Genuine domain concept; keep
   - amalgamation = Two concepts merged; split or merge into one
   - instance     = Example of a concept; add type/state
   - subtype      = Belongs under parent in concept_hierarchy
   - false_positive = Chunk doesn't support concept; remove or fix chunk_ids

3. Apply fixes to hypothesis.json:
   - Remove concepts (false_positive, amalgamation merge)
   - Add to concept_hierarchy (subtype)
   - Add states (instance, amalgamation)
   - Remove bad chunk_ids from concepts

4. When done with this batch, run the next batch:
""")
    if batch_num < total_batches:
        next_batch = batch_num + 1
        print(f"   python scripts/review_batch.py --batch {next_batch}")
        print()
        print(f"NEXT_BATCH={next_batch}")
    else:
        print("   (This was the last batch. Review complete.)")
        print()
        print("NEXT_BATCH=done")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
