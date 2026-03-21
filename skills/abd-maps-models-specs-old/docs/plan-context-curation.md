# Stage 1: Extract Context — Planning

Single source of truth for the enriched Stage 1 (Extract Context) design. Avoids revisiting the same decisions.

---

## Scope: Parser / Extractor / Filterer Only

Stage 1 is **pure up-front parsing, extraction, and filtering**. It produces artifacts that downstream consumers (modelers, indexers) can use directly.

**In scope:** Document-shape detection, semantic classification, purpose-built chunking, per-chunk metadata, output schema.


---

## What We're Going to Do (Exact Deliverables)

| # | Deliverable | What changes |
|---|-------------|--------------|
| 1 | **Document-shape detection** | Pre-pass: detect front matter, TOC, rules sections, tables, examples, sidebars, glossary, appendices, legal before block parsing. |
| 2 | **Richer taxonomy** | Extend `evidence_type` to: domain-rule, mechanic, actor-action, definition, state-change, variation/exception, example, flavor, metadata/noise. |
| 3 | **Purpose-built chunking** | Type-specific rules: definitions → small; rules → medium; tables → row-aware; examples → separate, lower priority. |
| 4 | **Multi-purpose split** | Split when a block has more than one dominant purpose (not just on size). |
| 5 | **Per-chunk metadata** | Add: candidate_concepts, actors, actions, state_terms, decision_terms, noise_score, modeling_priority, retrieval_tags. |
| 6 | **Output schema** | `chunks/*.md` (content: YAML front matter + markdown); `context_index.json` (single consolidated index: metadata + refs, no full text; forward + reverse indexes). |

---

## Q&A (user questions, answered once)

**Q: Do we need primary_label anymore?**  
A: No. Use `evidence_type` only. Same semantic notion; one field, one vocabulary.

**Q: What does "heuristic or config-based" mean?**  
A: **Config-based** = rules read from config. Config is **AI-discovered** (quick pass over markdown) — AI identifies how tables, headers, sections manifest and writes patterns to config. Code runs deterministically using that config.

**Q: Where does the detail go — process.md or context.md?**  
A: process.md stays minimal (Stage 1 table). All step detail lives in context.md.

---

## Strategy (from abd-localized-pipeline plan)

Invest in upfront context shaping so downstream modeling is not forced to recover from noise:

- **Document-shape first** — detect front matter, TOC, rules, examples, glossary, appendices before block parsing
- **Smaller structural units** — block-level (paragraph, list, table, heading), not section-level
- **Deterministic hierarchy preservation** — section_path from heading stack
- **One evidence_type per unit** — no multi-label sprawl; richer taxonomy (domain-rule, mechanic, actor-action, definition, state-change, variation/exception, example, flavor, metadata/noise)
- **Purpose-built chunking** — different rules by type (definitions small, rules medium, tables row-aware, examples separate)
- **Split on purpose, not just size** — split when a block has more than one dominant purpose
- **Per-chunk metadata** — candidate_concepts, actors, actions, state_terms, noise_score, modeling_priority, retrieval_tags for downstream filtering and retrieval
- **Early traceability** — chunk_id, source, line range
- **Early concept seed index** — TitleCase/acronym extraction for Step 2 hints

---

## Decisions

### 1. Use `evidence_type` only — no `primary_label`

**Decision:** Use `evidence_type` in the chunk schema. Do not add a separate `primary_label` field.

**Rationale:** `primary_label` (from abd-localized-pipeline) and `evidence_type` (from map-model-spec chunk_evidence) are the same semantic notion: what kind of evidence is this block? Having both is redundant. Step 1 assigns it; Step 3 can refine. One field, one vocabulary.

**Richer taxonomy (evidence_type values):**

| evidence_type | Description |
|---------------|-------------|
| definition | Formal definition of a term or concept |
| domain-rule | Domain rule or invariant |
| mechanic | Mechanic or procedure |
| actor-action | Actor performs an action |
| state-change | State transition or change |
| variation/exception | Variation, edge case, or exception |
| example | Example, illustration, or sample |
| flavor | Flavor text, narrative, non-mechanical |
| table | Tabular data (structural) |
| mention | Passing mention, heading-only |
| metadata/noise | Front matter, TOC, index, legal — excluded from curated output |

Excluded blocks (metadata/noise, structural heading only) go in the `excluded` section of context_index.json; content not written to chunks.

---

### 2. Config must be AI-discovered, not hand-written

**Requirement:** Classification is fully config-driven. The config is not hand-written — it is **discovered by a quick AI pass** over the converted markdown.

**Flow:**
1. **Step 1 (Convert):** Human runs convert; code produces markdown
2. **Step 2 (Discovery):** AI analyzes markdown; outputs patterns (regexes, cues, structural rules) to `context_curation` in solution.conf
3. **Step 3 (Parse and Curate):** Deterministic code runs using that config; produces chunks and context_index.json

**Why:** Source format varies (Word, PDF, etc.). Converted markdown structure varies. We tell the AI: "Here are the classification pieces we care about (evidence_type, structural_type, noise sections). Go look at the markdown and tell us how they manifest in this document." The AI produces config; the code executes it.

**What the AI discovers (examples):**
- Table patterns — how tables appear in this markdown (pipe syntax, HTML, other)
- Heading patterns — how sections/headers are marked
- Noise sections — headings that indicate TOC, index, glossary
- Definition/example cues — phrases that signal definition vs example in this domain

---

### 3. What we drop (no backward compatibility)

| Dropped | Why |
|---------|-----|
| Single JSON with full text | Content lives in chunks/*.md; index has metadata + ref only. |
| `chunk_markdown.py` | Block-level parsing replaces section-level chunking. |
| Hash-based chunk_id | Use stable block/unit id (e.g. `blk_00042`, `unit_00042_s1`) for traceability. |

---

### 4. What we keep (base fields)

| Field | Purpose |
|-------|---------|
| chunk_id | Stable id for citation; ref to `chunks/{chunk_id}.md`. |
| source | Document identifier for traceability. |
| section_path | Heading hierarchy. |
| structural_type | paragraph, list, table, heading. |
| evidence_type | Richer taxonomy (see Decision 1). |
| start_line, end_line | Line range for debugging. |

**Content:** Lives in `chunks/{chunk_id}.md` (YAML front matter + markdown body). Index has metadata only; no `text` field.

### 5. Per-chunk metadata (in index, not in chunk file)

| Field | Purpose |
|-------|---------|
| candidate_concepts | TitleCase/acronym terms extracted from chunk (for concept discovery). |
| actors | Actor terms if present. |
| actions | Action/verb terms if present. |
| state_terms | State-related terms. |
| decision_terms | Decision-related terms. |
| noise_score | 0–1; higher = more noise. |
| modeling_priority | 0–1; higher = more valuable for modeling. |
| retrieval_tags | Tags for downstream retrieval. |

---

## Stage 1: Extract Context — Steps (document in context.md)

Steps are grouped by **initiator** (who/what kicks off the step):

| Step | Initiator | What it does |
|------|-----------|--------------|
| **1. Convert** | Human → Code | Source (PDF, DOCX, PPTX, etc.) → markdown |
| **2. Discovery** | AI | Analyze markdown; identify how tables, headers, sections, document-shape regions, noise manifest; output patterns/regexes/cues to `context_curation` |
| **3. Parse and Curate** | Code | Document-shape detection → parse → classify → purpose-built chunking → per-chunk metadata → write chunks/*.md and context_index.json |

**Note:** Step 2 (Discovery) populates config. Step 3 (Parse and Curate) is deterministic and runs after config exists.

---

## Output schema

**chunks/{chunk_id}.md** — one file per chunk. Content: YAML front matter + markdown body. IDE indexable, human readable.

```yaml
---
chunk_id: blk_00042
source: HeroesHandbook
evidence_type: domain-rule
section_path: ["Chapter 3", "Abilities", "Ability Ranks"]
---
The actual chunk content in markdown.
```

**context_index.json** — single consolidated index. Metadata + refs only; no full text.

```json
{
  "manifest": {
    "sources": ["HeroesHandbook"],
    "section_counts": {"Chapter 3": 12, "Chapter 4": 8},
    "evidence_type_counts": {"definition": 45, "domain-rule": 120, "example": 30},
    "total_chunks": 195,
    "excluded_count": 22
  },
  "forward_index": {
    "blk_00042": {
      "source": "HeroesHandbook",
      "section_path": ["Chapter 3", "Abilities", "Ability Ranks"],
      "document_region": "rules",
      "structural_type": "paragraph",
      "evidence_type": "domain-rule",
      "start_line": 145,
      "end_line": 152,
      "candidate_concepts": ["Ability", "Rank"],
      "actors": [],
      "actions": ["apply", "modify"],
      "state_terms": [],
      "decision_terms": [],
      "noise_score": 0.1,
      "modeling_priority": 0.8,
      "retrieval_tags": ["abilities", "ranks"]
    }
  },
  "concept_seeds": [{"concept": "Ability", "count": 45}, {"concept": "Rank", "count": 32}],
  "reverse_indexes": {
    "by_concept": {"Ability": ["blk_00042", "blk_00043"], "Rank": ["blk_00042", "blk_00051"]},
    "by_evidence_type": {"domain-rule": ["blk_00042", "blk_00043"], "definition": ["blk_00001", ...]}
  },
  "excluded": [{"block_id": "...", "section_path": [...], "reason": "noise", "evidence_type": "metadata/noise", "text_preview": "..."}]
}
```

**Content lookup:** Index → filter/search → get chunk_ids → read `chunks/{chunk_id}.md` for text. No duplication.

---

## Config extension (solution.conf)

`context_curation` is **populated by the AI discovery pass** (phase 1a2). Schema example — AI fills in values based on document analysis:

```json
{
  "output_dir": "maps-models-specs",
  "context_path": "maps-models-specs/context",
  "context_curation": {
    "table_pattern": "regex or description of how tables appear",
    "heading_pattern": "regex or description of section headers",
    "document_region_keywords": {
      "front_matter": ["---", "title:", "author:"],
      "toc": ["table of contents", "contents"],
      "rules": ["rules", "mechanics", "how it works"],
      "examples": ["examples", "for example", "sample"],
      "glossary": ["glossary", "definitions"],
      "appendix": ["appendix", "appendices"],
      "legal": ["copyright", "license", "terms"]
    },
    "noise_heading_keywords": ["table of contents", "index", "glossary"],
    "definition_cues": ["refers to", "is a", "means", ":"],
    "example_cues": ["for example", "for instance", "such as", "e.g."],
    "chunking": {
      "definition": {"max_words": 80, "min_words": 10},
      "rule": {"max_words": 200, "min_words": 20},
      "table": {"row_aware": true},
      "example": {"max_words": 150, "min_words": 15, "priority": 0.5}
    },
    "multi_purpose_split": true
  }
}
```

AI discovers corpus-specific values; code uses them deterministically.

---

## Impact on downstream

| Step | Change |
|-----|--------|
| 4 | Use context_index.concept_seeds as hint; stratify sampling by evidence_type (reverse_indexes.by_evidence_type); use modeling_priority for weighting. Read content from chunks/*.md. |
| 5 | Use forward_index metadata (evidence_type, candidate_concepts, etc.) for concept mapping; use retrieval_tags for retrieval. Read content from chunks/*.md. |
| 6–7 | No change. |
| 8 | Use evidence_type and modeling_priority for prioritization; use noise_score to filter. Iterate forward_index; read chunks/*.md for full corpus. |

---

## Code changes implied

1. **New script:** `discover_context_structure.py` (or equivalent) — AI pass over converted markdown; outputs structural patterns, regexes, document_region_keywords, chunking rules to `context_curation` in solution.conf. Run after convert, before parse_and_curate.
2. **parse_and_curate.py** — Step 3. Reads config; document-shape detection; parses blocks; classifies with richer taxonomy; purpose-built chunking + multi-purpose split; builds per-chunk metadata during parse; writes chunks/*.md (content) and context_index.json (manifest, forward_index, concept_seeds, reverse_indexes, excluded). Fully config-driven.
3. **Remove/deprecate:** chunk_markdown.py, build_context_chunks.py.
4. **Update:** build_chunk_index.py, classify_chunks.py to read context_index.json and chunks/*.md.
5. **Update:** context.md with steps 1–3 (by initiator), document-shape, purpose-built chunking, multi-purpose split, per-chunk metadata, new output format.
6. **Update:** process.md scripts table; workspace layout.

---

## How better classification benefits Step 3

| Step 3 task | Benefit from better Step 1 classification |
|-------------|--------------------------------------------|
| **Concept mapping** (chunk → concept) | `section_path` gives module/epic context — "Chapter 3 Abilities" → concept likely in Character/Abilities module. `evidence_type` lets Step 2 stratify sampling (more definition/rule chunks for orientation). Step 3 AI can use chunk.evidence_type as prior: definition chunks → focus on extracting definitions; rule chunks → focus on relationships. |
| **Evidence type refinement** | Step 1 assigns initial evidence_type. Step 3 AI can override when needed, but starting with a good classification reduces refinement workload. Less noise = fewer false concept mentions; code pass (Pass 2) can trust or augment rather than re-compute from scratch. |

**Pragmatic take:** Better Step 1 means Step 3 spends less effort recovering from noise and more on concept mapping. The plan in abd-localized-pipeline says exactly this: "upstream context shaping is weak enough that downstream modeling is being forced to recover from noise."

---

## What to borrow from abd-localized-pipeline

**Path:** `C:\dev\abd-localized-pipeline\src\abd_localized_pipeline`

| Borrow | What | Notes |
|--------|------|------|
| **context_curation.py** | Parse, classify, split logic | Already adapted into parse_and_curate.py. Use as reference for AI discovery output format. |
| **evidence.py** | Label-driven evidence extraction | Uses `primary_label` to drive extraction: decision-logic → decision records; state-change → state records. We can use `evidence_type` similarly: definition → definition records; rule → relationship extraction. |
| **models.py** | CandidateBlock, CuratedUnit | Schema reference. We use our own (chunk_id, evidence_type, etc.). |
| **modeling.py** | Heuristic domain/interaction model | Placeholder. maps-models-specs has its own Step 3–5; no direct borrow. |
| **graph.py, main.py** | LangGraph orchestrator | **Do not borrow.** User does not want the orchestrator. maps-models-specs runs scripts directly. |

**Plan (docs/plan.md):** The plan does not explicitly say "leverage better structured content for X." It says Phase 0 is the first leverage point because downstream is forced to recover from noise. The benefit is: better Phase 0 → less recovery work downstream. No orchestrator in the borrow list.
