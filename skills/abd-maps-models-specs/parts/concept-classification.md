# Steps 5 & 5a — Concept Classification

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
- **Step 5 (AI):** AI reads every chunk (or configured %), extracts concepts and relationships
- **Step 5a (Code):** Code scanner runs on full text with concept list from Step 5; merges gaps (catches concepts in text the AI didn't see when chunk-pct < 100%). Then `summarize.py` → `summary.md`, `relationships.md`

**Outputs:** `map-model-spec.json` (updated with evidence), `summary.md`, `relationships.md`
