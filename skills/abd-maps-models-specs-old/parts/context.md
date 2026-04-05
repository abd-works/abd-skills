# Stage 1 — Extract Context

**Prerequisites:** (1) `skill-config.json` sets **required** `solution_workspace` and that directory contains `solution.conf` (see `conf/README.md`). (2) Source documents (PDF, DOCX, PPTX, XLSX, HTML, etc.) in a folder under that workspace (or passed explicitly to scripts).

## Purpose

Convert source documents to markdown, discover structure, parse into structural blocks, curate (classify, exclude, split), and produce `chunks/*.md` (content) and `context_index.json` (metadata + indexes) for Stage 2 onward. This stage creates the corpus that the rest of the pipeline consumes.

**Scope:** Parser / extractor / filterer only. No orchestration, layered memory, or branching.

**Planning:** See [docs/plan-context-curation.md](../docs/plan-context-curation.md) for strategy, decisions, and exact deliverables.

---

## Steps (by initiator)

| Step | Initiator | What it does |
|------|-----------|--------------|
| **1. Convert** | Human → Code | Source files (PDF, DOCX, PPTX, etc.) → markdown |
| **2. Discovery** | AI | Analyze markdown; identify how tables, headers, sections, document-shape regions manifest; output patterns to `context_curation` |
| **3. Parse and Curate** | Code | Document-shape detection → parse → **curate** (classify + exclude) → purpose-built chunking → per-chunk metadata → write chunks/*.md and context_index.json |

**Step 3** includes: document-shape pre-pass, block parsing, **curate** (classification with richer taxonomy; exclusion of noise headings, structural headings, out-of-scope sections, below-min chunks), purpose-built chunking, multi-purpose split, per-chunk metadata, and writing outputs. There is no separate “curate” step—curate is done inside this step.

---

## Exact deliverables

1. **Document-shape detection** — Pre-pass tags regions (front matter, TOC, rules, examples, glossary, appendix, legal).
2. **Richer taxonomy** — evidence_type: domain-rule, mechanic, actor-action, definition, state-change, variation/exception, example, flavor, table, mention, metadata/noise.
3. **Purpose-built chunking** — Definitions small; rules medium; tables row-aware; examples separate. `min_chunk` filters out tiny fragments (e.g. single table cells, orphan bullets). `merge_table_like` merges consecutive short paragraph blocks (PDF-converted tables) into cohesive table chunks. `merge_header_with_next` prepends short all-caps header lines (e.g. TRADE-OFFS) into the following content block instead of excluding them. `merge_definition_runs` merges consecutive short definition blocks (e.g. Parry & Toughness, Fortitude & Will) and skips trivial separators (single bullets) between them.
4. **Multi-purpose split** — Split when block has more than one dominant purpose.
5. **Per-chunk metadata** — candidate_concepts, actors, actions, state_terms, decision_terms, noise_score, modeling_priority, retrieval_tags.
6. **Output schema** — chunks/*.md (content: YAML front matter + markdown); context_index.json (single consolidated index: metadata + refs, forward + reverse indexes).

---

## Classification: Heuristic vs Config-based

**Heuristic (code):** Rules hardcoded in Python. E.g. `structural_type == 'table'` → `evidence_type = 'table'`. No config.

**Config-based:** Rules read from `solution.conf` → `context_curation`. E.g. `document_region_keywords`, `noise_heading_keywords`, `definition_cues`, `example_cues`, `chunking`. User can customize without editing code.

We use both: structural rules are heuristic; keyword/cue matching and chunking rules are config-based.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `convert_to_markdown.py` | Convert PDF, DOCX, PPTX, XLSX, HTML, etc. to markdown. Requires `pip install "markitdown[all]"`. |
| `discover_context_structure.py` | AI pass over markdown; outputs document_region_keywords, chunking rules, cues to `context_curation`. Run after convert, before parse_and_curate. |
| `parse_and_curate.py` | Document-shape detection; parse → blocks; classify (richer taxonomy); purpose-built chunking + multi-purpose split; per-chunk metadata; write chunks/*.md and context_index.json. |

---

## Usage

**1. Convert source folder to markdown**

```bash
python scripts/convert_to_markdown.py --path <source_folder> [--output <output_folder>]
```

**2. Discovery (optional AI pass)**

```bash
python scripts/discover_context_structure.py --path <markdown_folder>
```

Populates `context_curation` in solution.conf. Run after convert, before parse_and_curate.

**3. Parse and curate**

```bash
python scripts/parse_and_curate.py --path <markdown_folder> [--output <context_folder>]
```

When `--output` is omitted, writes to `context_path` from solution.conf (default: `output_dir/context`).

---

## Prompt for study: when assisting with Extract Context

When the user asks you to **extract context** (or to run Convert / Discovery / Parse and Curate for context):

1. **Ask why if they don’t say.** If the user does not state the purpose or scope of the extraction (e.g. “for character creation only”, “for the combat chapter”, “for domain modeling”), ask: *What is this context for? Which parts of the source do you actually need?* Use the answer to guide what to keep or drop.

2. **Review the source and call out unhelpful sections.** After you see the document(s) or markdown (e.g. table of contents, chapter list, section headers), go through the context and explicitly say which sections you think **will not be helpful** for their stated purpose. For example: “I don’t think these sections are going to be helpful for [purpose]: [list sections]. They’re [reason: out of scope / reference-only / setting fluff / legal / etc.].”

3. **Suggest removing them.** Propose removing those sections (or whole chapters) from the corpus—at conversion time (e.g. strip chapters or ranges when converting to markdown) or via config (e.g. `out_of_scope_section_keywords`) so they never become chunks.

4. **Get approval before removing.** Do not remove or strip content until the user approves. Summarize what you propose to remove and ask: “Do you want to drop these from the context?” Only then apply the change (re-convert with strip, edit markdown, or update solution.conf).

---

## Output Format

**chunks/{chunk_id}.md** — one file per chunk. YAML front matter + markdown body. IDE indexable, human readable.

```yaml
---
chunk_id: blk_00042
source: HeroesHandbook
evidence_type: domain-rule
section_path: ["Chapter 3", "Abilities", "Ability Ranks"]
---
The actual chunk content in markdown.
```

**context_index.json** — single consolidated index. Metadata + refs only; no full text. Content lives in chunks/*.md.

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

## Config (solution.conf)

`context_curation` is populated by the AI discovery pass (Step 2). Example schema:

```json
{
  "output_dir": "maps-models-specs",
  "context_path": "maps-models-specs/context",
  "context_curation": {
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
      "example": {"max_words": 150, "min_words": 15, "priority": 0.5},
      "min_chunk": {"min_words": 2, "min_chars": 15},
      "merge_table_like": {"enabled": true, "max_cell_chars": 50, "min_run_length": 2},
      "merge_header_with_next": {"enabled": true, "max_header_chars": 60},
      "merge_definition_runs": {"enabled": true, "max_words_per_block": 80, "max_merged_words": 250, "min_run_length": 2, "skip_trivial_separators": true}
    },
    "multi_purpose_split": true
  }
}
```

---

## Workspace Layout

After Stage 1 (Steps 1–3):

```
maps-models-specs/
├── context/
│   ├── chunks/           # Content: one .md per chunk (YAML front matter + markdown)
│   │   ├── blk_00042.md
│   │   ├── blk_00043.md
│   │   └── ...
│   └── context_index.json   # Metadata + forward/reverse indexes (no full text)
```

---

## Prerequisite for Stage 2

Stage 2 (Discover) requires `context_index.json` and `chunks/*.md` in the context folder.
