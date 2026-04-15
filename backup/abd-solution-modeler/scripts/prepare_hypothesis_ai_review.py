#!/usr/bin/env python3
"""Prepare hypothesis concepts for AI-driven classification.

Outputs batches of concepts with their chunk texts and prompts, ready to feed
to an AI. Each batch is a self-contained markdown file you can paste into
an AI chat.

Output:
  generated/ai_review_batches/batch_001.md, batch_002.md, ...
  generated/ai_review_input.json (full structured input for programmatic use)
"""
import json
from pathlib import Path

CHUNK_MAX_CHARS = 2500  # Truncate long chunks to stay within context
CONCEPTS_PER_BATCH = 12


def load_chunk_lookup(context_path: Path) -> dict[str, str]:
    """Build chunk_id -> text lookup from context_chunks.json."""
    chunks_file = context_path / "context_chunks.json"
    if not chunks_file.exists():
        return {}
    data = json.loads(chunks_file.read_text(encoding="utf-8"))
    return {c["chunk_id"]: c.get("text", "") for c in data if "chunk_id" in c}


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[... truncated ...]"


def build_prompt() -> str:
    return """## Classification instructions

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


def main():
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    workspace = skill_dir / "test" / "mm3" / "solution"
    context_path = workspace / "context"
    hypothesis_path = workspace / "generated" / "hypothesis.json"

    if not hypothesis_path.exists():
        print(f"hypothesis.json not found: {hypothesis_path}")
        return 1

    hypothesis = json.loads(hypothesis_path.read_text(encoding="utf-8"))
    chunk_lookup = load_chunk_lookup(context_path)
    concepts = hypothesis.get("concepts", {})

    # Build items: {name, chunk_ids, chunk_texts, performs, receives}
    items = []
    for name, c in concepts.items():
        chunk_ids = c.get("chunk_ids") or []
        chunk_texts = []
        for cid in chunk_ids:
            text = chunk_lookup.get(cid, f"[chunk {cid} not found]")
            chunk_texts.append({"chunk_id": cid, "text": truncate(text, CHUNK_MAX_CHARS)})
        items.append({
            "name": name,
            "chunk_ids": chunk_ids,
            "chunk_texts": chunk_texts,
            "performs": c.get("performs") or [],
            "receives": c.get("receives") or [],
        })

    # Write JSON (full input for programmatic use)
    out_dir = workspace / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "ai_review_input.json"
    json_path.write_text(
        json.dumps({"concepts": items, "prompt_template": build_prompt()}, indent=2),
        encoding="utf-8",
    )
    print(f"JSON: {json_path}")

    # Write markdown batches
    batch_dir = out_dir / "ai_review_batches"
    batch_dir.mkdir(parents=True, exist_ok=True)

    prompt_header = build_prompt()
    for i in range(0, len(items), CONCEPTS_PER_BATCH):
        batch = items[i : i + CONCEPTS_PER_BATCH]
        batch_num = (i // CONCEPTS_PER_BATCH) + 1
        batch_path = batch_dir / f"batch_{batch_num:03d}.md"

        lines = [
            "# Hypothesis concept review – batch " + str(batch_num),
            "",
            prompt_header,
            "---",
            "",
        ]

        for item in batch:
            lines.append(f"## Concept: {item['name']}")
            lines.append("")
            lines.append(f"Chunk count: {len(item['chunk_ids'])}")
            if item["performs"]:
                lines.append(f"Performs actions: {item['performs'][:5]}{'...' if len(item['performs']) > 5 else ''}")
            if item["receives"]:
                lines.append(f"Receives actions: {item['receives'][:5]}{'...' if len(item['receives']) > 5 else ''}")
            lines.append("")
            lines.append("### Chunk texts")
            lines.append("")
            for j, ct in enumerate(item["chunk_texts"], 1):
                lines.append(f"**Chunk {j}** (`{ct['chunk_id']}`):")
                lines.append("")
                lines.append("```")
                lines.append(ct["text"])
                lines.append("```")
                lines.append("")
            lines.append("---")
            lines.append("")

        batch_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Batch: {batch_path} ({len(batch)} concepts)")

    print(f"\nDone. {len(items)} concepts in {(len(items) + CONCEPTS_PER_BATCH - 1) // CONCEPTS_PER_BATCH} batches.")
    print("Feed each batch_XXX.md to an AI for classification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
