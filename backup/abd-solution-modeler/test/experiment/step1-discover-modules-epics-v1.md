# Step 1 — Discover Modules and Epics (v1)

## Purpose

Perform the first discovery pass over the source corpus. Produce a paired list of **modules** (domain view) and **epics** (interaction view). Each pair describes the same area of the domain from two angles simultaneously.

This is the foundation. Every subsequent step operates within the structure produced here. Getting this right matters more than anything else.

---

## Inputs

- `context/context_chunks.json` — all normalized chunks from the source corpus

---

## Sampling Strategy

Read **30% of chunks**, spread evenly across the corpus:
- Divide `context_chunks.json` into thirds (beginning, middle, end)
- Read 10% from each third
- This ensures you see introductory definitions, core rules, and specialized sections

Do not read chunks sequentially from the start. Sample across the whole corpus.

---

## What You Are Looking For

For each major area of the domain you discover, you will produce **two things simultaneously**:

**Module (domain view):** A named grouping of concepts that collaborate around the same mechanism. A module holds concepts that hold state, make decisions, enforce rules, and relate to each other. Ask: *what are the things in this area and what do they do?*

**Epic (interaction view):** The named user/system interaction that corresponds to this module. An epic describes what actors do with the concepts in this module and what observable outcomes result. Ask: *what does someone do with this area of the domain and what changes as a result?*

These are two views of the same coin. Discover them together. A module with no epic is incomplete. An epic with no module has no domain grounding.

---

## Discovery Instructions

### Pass 1: Orient

Read the sampled chunks. Do not classify yet. Ask:

- What are the major mechanisms in this system?
- What are actors doing, and to what?
- What holds state, enforces rules, makes decisions?
- Where does behavior visibly vary by type, mode, or category?
- What cross-cuts everything (e.g. resolution mechanics, cost systems, validation rules)?

### Pass 2: Identify Module/Epic Pairs

For each distinct area you identified, produce one entry. Each entry must answer:

**Module side:**
- What is this area called? (module name — noun phrase)
- What does it do in one sentence?
- What is the dominant mechanism or rule cluster here?

**Epic side:**
- What is the actor doing with this module? (epic name — verb noun)
- What triggers this interaction?
- What is the observable outcome?

### Pass 3: Index Evidence

For each module/epic pair, record every chunk that supported your discovery of it.

Chunks fall into three confidence levels:

- **identified** — this chunk clearly belongs to this module/epic pair
- **provisional** — this chunk seems related to this area but the specific concept or story is not yet clear; place it in the module bucket for later resolution in Step 2
- **ambiguous** — this chunk may belong here or somewhere else; flag it for Step 4 (canonicalize)

Record all three. Do not discard provisional or ambiguous chunks — they carry evidence that later steps will resolve.

---

## Human Gate

Before producing output, ask yourself:

1. Does every module have a paired epic?
2. Does every epic name an actor, a verb, and an observable outcome?
3. Can I point to at least one chunk that confirms each pair?
4. Are there areas of the corpus that feel important but don't fit any pair yet? (If so, add a provisional entry.)

---

## Output

Write to: `test/experiment/step1-output.json`

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Module Name",
        "description": "One sentence: what this area is and what mechanism it centers on.",
        "dominant_mechanism": "The core rule or resolution pattern that defines this area."
      },
      "epic": {
        "name": "Verb Noun",
        "actor": "Who triggers this",
        "trigger": "What they do",
        "outcome": "What observable state results"
      },
      "chunk_ids": {
        "identified": ["chunk_id_1", "chunk_id_2"],
        "provisional": ["chunk_id_3"],
        "ambiguous": ["chunk_id_4"]
      }
    }
  ],
  "notes": "Any observations about the corpus structure, cross-cutting concerns, or areas of uncertainty."
}
```

---

## Stop for Review

After producing output, **stop**. Do not proceed to Step 2 until the user reviews and confirms the module/epic list.

Present the pairs to the user in a readable summary (not raw JSON). Ask:

- Does this list capture all the major areas?
- Are any pairs obviously wrong or misnamed?
- Are there areas that are missing?
- Are any pairs duplicates of each other under different names?

A wrong module/epic structure here cascades into everything downstream.
