# Concept Classification

Pipeline placement: **[Concept Classification](../process.md)** (Stage 2 — AI + code rows **6** and **6a**).

Read every chunk in the corpus and extract domain evidence. For each chunk, the scan records:
- Which domain concepts it evidences, with evidence type (definition, rule, example, table, mention) and optional note
- Which cross-module relationships it establishes between concepts, with the specific mechanic that justifies each relationship

**Evidence is written directly to map-model-spec.json** — no separate index files. The spec gains:
- `concept.chunk_evidence`: `[{chunk_id, evidence_type, note}, ...]` per concept
- `concept.chunk_ids`: derived from chunk_evidence
- `chunk_ids.identified` / `chunk_ids.provisional` per module/epic pair
- `cross_module_relationships` at top level

**Configuration** — present to user and confirm:
- Chunk text: 100% (default) | 50% | 25%
- Model: gpt-4o-mini (default) | gpt-4o

**How it works:**
- **Classification (AI):** AI reads every chunk (or configured %), extracts concepts and relationships
- **Classification (code):** Code scanner runs on full text with concept list from the AI pass; merges gaps (catches concepts in text the AI didn't see when chunk-pct < 100%). Then `summarize.py` → `summary.md`, `relationships.md`

**Outputs:** `map-model-spec.json` (updated with evidence), `summary.md`, `relationships.md`

---

## Why so many subtypes are "missing" (Pass 1 coarse-grained)

Pass 1 asks the AI to label each chunk with **primary_concepts** (concept name + module + evidence_type). The model tends to return **coarse** names: e.g. "Effect", "Modifier", "Advantage" rather than every power effect (Damage, Weaken, Healing, …), every advantage type, or every modifier type. So you get a limited set of unique concept names (e.g. 80) that are high-level. The finer-grained subtypes are either lumped under one concept or never named as first-class concepts.

---

## Will **[Concept Classes and Stories](../process.md)** find them?

**Sometimes.** **Concept Classes and Stories** **deepens** the concepts you already have and **Pass 1** re-harvests from the pair’s chunks — so **new** names can appear when the classification pass was coarse. The **default** is still: classification broadens coverage across the corpus; **Concept Classes and Stories** **must not** skip **Pass 1** harvest to “only deepen what exists.” If dozens of variants exist only in unclassified chunks, **Concept Classification** coverage matters most.

---

## Design: module-level evidence → then find them

**Your approach is right.** Put evidence at the **module** level (which chunks belong to this module), and have a **later** step read those chunks and discover the subtypes (all power effects, all advantage types, all modifiers).

- **What we have today:** Evidence is attached to **(module, concept)**. We also have **chunk_ids.identified** and **chunk_ids.provisional** per module/epic pair — i.e. the set of chunks that belong to that module. So we already have a module-level view of which chunks are in scope.
- **What’s missing:** A dedicated pass that says: “For this module, read its chunks and extract all subtype concept names (e.g. every effect type, every advantage type, every modifier).” That could be:
  - a new sub-step (e.g. “Discover subtypes from module chunks”), or
  - a variant of **Concept Classes and Stories** (e.g. “Pass 0: from module chunks, discover and add subtype concepts; then deepen as now”).

So: **we didn’t “miss” them forever** — we just didn’t ask Pass 1 to enumerate every subtype. The way to get them is to use the module-level chunk sets we already have and add a discovery step that finds the subtypes. No need to re-run Pass 1 for that; the evidence is already at the module level in `chunk_ids` and in the concept-level evidence for the coarse concepts (Effect, Modifier, Advantage). A later pass can use that to propose and attach finer-grained concepts.

---

## Regression: fewer concepts after "better context extraction" changes

If you used to get **many more** concepts and now get a much smaller set (e.g. ~80), something in the pipeline or inputs changed. **Concept Classes and Stories** **Pass 1** can add missing names from pair chunks, but it does not replace a weak **Concept Classification** corpus pass. So the fix is to find why **Concept Classification** Pass 1 is now returning fewer/different names.

**What drives concept count in Pass 1:**

1. **Seed spec (map-model-spec.json)** — `build_module_context(spec)` sends the AI: for each module, name + description + list of concept names. The **initial** concept list the AI sees is whatever is in the spec when you run **Concept Classification**. If that spec was minimal (e.g. **[Modules and Epics](../process.md)** with 30% sample → few concepts), the AI can still add more but may stay coarser. If the spec used to be richer (e.g. from a previous full run or hand-curated list), the AI had more hints and could produce more names.
2. **Chunk content** — The AI gets batches of chunks; each chunk's text is sliced by `chunk_pct` (default 100%). If chunks now have **less text** (e.g. YAML front matter stripped and the body is shorter, or chunking splits more finely), the model sees less evidence per chunk and may name fewer concepts.
3. **Chunk source** — **Concept Classification** loads from either `context_index.json` + `chunks/*.md` (strip YAML, use body) or legacy `context_chunks.json`. If you switched from one to the other, chunk count, order, or content may differ.
4. **chunk_pct** — If you run with `--chunk-pct 50` or `25`, the AI only sees the first part of each chunk; the rest is invisible to Pass 1.

**Checklist to compare before vs now:**

- [ ] **Spec at Concept Classification start** — How many concept names are in the spec when you invoke classify_chunks? If you used to run with a spec that already had many concepts (e.g. from a previous run), that primed the AI. If you now run with a fresh **[Modules and Epics](../process.md)** output, that could explain fewer.
- [ ] **Chunk path** — Same `--chunks` as before? (e.g. legacy context_chunks.json vs context_index + chunks/*.md)
- [ ] **Chunk count and sample** — Same number of chunks? For a few chunk IDs, compare length of text sent to the AI (after stripping). Shorter or different text per chunk can reduce discovery.
- [ ] **chunk_pct** — Same value (e.g. 100%)?
- [ ] **Step 3 (parse_and_curate)** — Did "better context extraction" change chunk boundaries, front matter vs body, or exclusions? That would change what the classifier sees.

**Quick diagnostic:** Before the AI pass, log the first 500 chars of `module_context` and the first chunk's full text length. Compare to any saved log or old run to see if inputs (seed concepts + chunk content) are smaller or different.


**At 100%, there is no truncation of chunk text.** The code sends exactly `text[:int(len(text) * chunk_pct/100)]`; when `chunk_pct` is 100, that is the full string. Every chunk’s full text is sent to the AI.

**What the “average length” is used for:** The script samples ~10% of chunks at the configured `chunk_pct`, computes average *sent* size (chars → tokens via `CHARS_PER_TOKEN`), then sets **batch size** so that each batch aims for ~8,000 tokens of chunk text. So “average” is used only to decide *how many chunks per API call*, not to truncate. Oversized chunks (raw length &gt; 15,000 chars) get their own single-chunk batch so one huge chunk doesn’t blow the prompt.

**“Buffer on top of average”:** There is no separate step that “adds a buffer so we never truncate.” We don’t need one for chunk content: at 100% we never cut chunk text. The only way content is shortened is when `chunk_pct` &lt; 100 (e.g. 50% or 25%). So for a run at 100% (e.g. mm3 with `chunk_pct: 100` in run_log.json), **no truncation of input happened**. If you ever want an extra safety (e.g. use 90th percentile + buffer to set a more conservative batch size so total prompt stays well under model context), that could be added; today we rely on the 8k-token target and the 15k-char oversize rule.
