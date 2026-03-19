# Step 2 — Index Chunks

## Purpose

Read every chunk in the corpus and extract domain evidence. For each chunk, the output records:
- Which domain concepts it evidences, with evidence type (definition, rule, example, table, mention)
- Which cross-module relationships it establishes between concepts, with the specific mechanic that justifies each relationship

The output is `chunk_evidence.json` — a complete forward index of the corpus. Every chunk is accounted for. Every concept mention and cross-module relationship is recorded with the chunk that evidenced it.

This index is used in Step 3 to deepen each module: instead of reading the corpus again, the AI reads only the chunks attributed to that module's concepts.

---

## Inputs

- `context/context_chunks.json` — all normalized chunks
- `step1-output.json` — modules, epics, and foundational concept names from Step 1

---

## Configuration

Before running, present these options to the user and confirm:

**Chunk text coverage** — what percentage of each chunk's text is sent to the AI. Every chunk is processed; this controls the character slice per chunk:

- `100%` (default) — full text of every chunk sent to AI. Complete coverage. Larger prompts, more cost.
- `50%` — first half of each chunk's text. Faster, cheaper. Misses content in the second half of long chunks.
- `25%` — first quarter of each chunk's text. Fastest. Similar to the original 1,000-character truncation. Most gaps.

At any setting below 100%, Pass 2 (code signals) runs on all chunks using full text and the extended concept list discovered in Pass 1 — partially filling gaps where AI saw truncated text.

**Model**:
- `gpt-4o-mini` (default) — fast, cheap, good for structured extraction
- `gpt-4o` — more thorough on dense rules text, ~6x cost

**Example prompt to user:**
> Step 2 is ready to run. Default: AI reads 100% of each chunk's text using gpt-4o-mini.
>
> Options:
> - Chunk text: 100% (default) | 50% | 25%
> - Model: gpt-4o-mini (default) | gpt-4o
>
> At 100%, every chunk is read in full — no text is skipped. Lower percentages are faster and cheaper but may miss content near the end of long chunks. The corpus average is ~4,700 characters per chunk.
>
> Confirm defaults or specify changes.

---

## How It Works

### Pass 1 — AI reads every chunk

Every chunk goes to the AI. The configured percentage controls how much of each chunk's text is included:

```
text_sent = chunk_text[:int(len(chunk_text) * chunk_pct / 100)]
```

At 100% the full chunk is sent. At 50% the first half is sent.

Batch size is calculated automatically from the average sent character count across a sample of chunks (target: ~8,000 tokens of chunk text per batch). Oversized chunks (>15,000 characters) are sent alone regardless of batch size.

The AI produces one JSON object per chunk identifying:
- Concepts evidenced, with module assignment and evidence type
- Cross-module relationships, with the specific mechanic that justifies each relationship

The AI may name concepts not in the Step 1 list if it finds them in the text. These discovered concept names accumulate across all batches.

Progress streams to `progress.log` in real time — you can watch the AI output as it arrives for each batch. `chunk_evidence.json` is updated after every batch so the run is always recoverable if interrupted.

### Pass 2 — Code signals on all chunks (always runs)

After the AI pass, the code scanner runs on all chunks using:
- **Full text** of every chunk — no truncation
- **Extended concept list** — all concept names discovered in Pass 1, not just the 13 from Step 1

The scanner does term matching, co-occurrence detection, and relationship pattern matching. New concept mentions and relationships found by code that the AI missed are merged into the evidence — AI evidence takes precedence, code fills gaps.

This always adds value: at 100% AI coverage it catches mentions the AI may have named differently or skipped. At lower coverage it partially compensates for truncated text by finding mentions of AI-discovered concept names in the full chunk.

---

## Outputs

### `step2a/chunk_evidence.json`

One entry per chunk:

```json
{
  "chunk_id": "4cd63373be61",
  "source": "HeroesHandbook.md__section_005",
  "classified_by": "ai | code | code+ai",
  "concept_count": 5,
  "relationship_count": 2,
  "primary_concepts": [
    {
      "concept": "Check",
      "module": "Resolution",
      "evidence_type": "definition | mention | rule | example | table",
      "note": "brief description of what this chunk says about this concept"
    }
  ],
  "cross_module_relationships": [
    {
      "from": {"concept": "AttackCheck", "module": "Combat"},
      "relationship": "inherits | produces | uses | modifies | constrained_by | targets | impairs",
      "to": {"concept": "Check", "module": "Resolution"},
      "justification": "citation of the mechanic that proves this relationship",
      "chunk": "4cd63373be61"
    }
  ]
}
```

### `step2a/progress.log`

Human-readable run log written after every batch:
- Timestamp, batch number, status, concept count, relationship count, elapsed time
- Full streamed AI response for each batch
- Per-chunk summary: what concepts and relationships were found

### `step2a/run_log.json`

Completion record: elapsed time, AI call count, model, chunk_pct, discovered concept count, total concepts and relationships, errors.

---

## After Running

Run the summarizer:

```
python test/experiment/step2a/summarize.py step2a/chunk_evidence.json
```

Produces:
- `step2a/summary.md` — concept evidence counts by module and evidence type
- `step2a/relationships.md` — all cross-module relationships with counts, justifications, and chunk citations

Review both before proceeding to Step 3. Key things to check:

1. Are any modules thin on concept evidence? May indicate coverage gaps — consider re-running at higher chunk_pct.
2. Are there surprising relationships? Cross-module relationships need review before Step 3 uses them.
3. Are there junk concept names in the index that should be removed?
4. Are there `[defer]` flags from Step 1 that are now resolved by what the index shows?
