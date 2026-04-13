# Chunking spec (`context_chunking_spec.yaml`)

## Chunker vs converter

Separate three jobs—conversion, drafting the spec, and chunking—so you do not blame the chunker for bad markdown or a bad spec.

**Convert sources to navigable markdown.** Use the **core converter**, shared **post-processors** such as `pdf_markdown_post`, and **corpus-specific scripts** under the topic’s `scripts/` when the default pipeline is not enough. Aim for real headings, sections that match the book, intact tables, and less PDF noise (running headers, page junk).

**Draft the chunking spec (`draft_chunking_spec.py`).** Read structural signals in the markdown (headings, tables, patterns) and **write a first draft** of `context_chunking_spec.yaml` so you are not hand-authoring YAML from zero. Treat it as a starting point, not a repair pass for broken conversion.

**Chunk the markdown (`chunk_markdown.py`).** Cut files to your size rules and the boundaries in the spec—`section_boundaries`, heading levels, `max_chunk_chars`, and the rest. The tool only follows structure the markdown and spec already expose; it does not infer meaning from a wall of text.

**Fix markdown and spec settings when boundaries are wrong.** Adjust structure and noise in the markdown and the regexes or fields in `context_chunking_spec.yaml`; do not wait for a “smarter chunker” to invent hierarchy.

---

## Where the spec lives

- **Canonical:** `memory/context_chunking_spec.yaml`
- **`chunk_markdown.py`** reads `section_boundaries`, `splitting`, and `defaults` for splitting and YAML front matter.
- **`taxonomy`** documents corpus-specific labels (AI- or human-authored); the emitter may warn if `defaults` omit labels while taxonomy lists are non-empty.

**`chunk_inputs`** (optional): topic-relative paths, e.g. `["markdown/Book.md"]`. When set, **only** those files are chunked—useful when the folder also has backups, notes, or duplicate stems. Without it, the chunker scans all `.md` under the topic root (see `chunk_markdown.py`).

**Corpus preprocess:** If markdown must be **reformatted using additional code processors** before boundaries work, look in **`<topic_root>/scripts/`** (not the skill’s `scripts/`). Details → [../process.md](../process.md) (*Corpus preprocess scripts*).

If no spec exists, chunking uses built-in heuristics and chunks may get `<!-- Source: … -->` instead of full YAML front matter (unless implemented otherwise).

---

## Minimum shape (example)

```yaml
# Optional: restrict chunking to specific markdown files (POSIX paths from topic root).
chunk_inputs: ["markdown/PrimarySource.md"]

section_boundaries:
  chapter_break_regex: "^CHAPTER\\s+\\d+"
  section_break_regex: "^##\\s+"
  all_caps_standalone: true

splitting:
  min_chunk_chars: 400
  max_chunk_chars: 8000
  keep_markdown_tables_intact: true
  split_on_heading_level: 2

defaults:
  evidence_type: mixed
  chunk_type: prose_block

taxonomy:
  evidence_type: []
  chunk_type: []
```

The chunk spec script drafter leaves **`taxonomy`** empty by design. After you classify the source, fill `evidence_type` and `chunk_type` lists and set  in `defaults` (the chunker may still accept `modeling_kind` as an alias for one release path).

---

## Sections (reference)

| Section | Purpose |
|---------|---------|
| `chunk_inputs` | Optional allow-list of topic-relative `.md` paths; if omitted, all eligible markdown under the topic is considered |
| `section_boundaries` | Regexes that start a new major unit; informs where splits are meaningful |
| `splitting` | Size limits, heading level for splits, `keep_markdown_tables_intact` (logged by chunker; valid pipe tables are still fixed in **convert**—chunker only splits at headings/markers) |
| `defaults` | Fallback `evidence_type` / `chunk_type` on each chunk’s front matter |
| `taxonomy` | Allowed labels for *this* corpus—filled by you after reading the source, not a global enum in tooling |

---

## `evidence_type` vs `chunk_type`

Two axes on each chunk when a spec is active (from `defaults` until you add finer labeling):

| Axis | Question | Examples |
|------|----------|----------|
| `evidence_type` | What does this chunk look like as exported text? (form) | `prose`, `table`, `list`, `mixed`, `metadata_noise` |
| `chunk_type` | What **role or structure** in *this* manuscript? | Corpus-specific: `chapter`, `archetype_sheet`, `stat_block`, `powers`, `toc_or_index`, … |

They diverge when form and role differ (e.g. `evidence_type: table`, `chunk_type: stat_block`).

---

## Why review the YAML? (`draft_chunking_spec.py` is a guess)

**Problem:** `draft_chunking_spec.py` infers patterns from headings, tables, slides, and noise heuristics. Odd layouts, mixed templates, or PDF junk can yield **wrong regexes** or **empty/wrong taxonomy** → poor splits and weak labels → bad retrieval.

**Passes:**

| Pass | Who | What happens |
|------|-----|----------------|
| **1 — Structural (automatic)** | Scripts | Convert → `draft_chunking_spec.py` writes **`markdown/structural_scan_report.*`** and drafts **`memory/context_chunking_spec.yaml`** when no spec exists yet (same scan drives both; console shows the structural scan). |
| **2 — Strategy (human + AI)** | You | Compare the draft to real `markdown/` files. Adjust boundary regexes, table/list handling, noise vs signal, fill **`taxonomy`**, tune **`defaults`**. |

---

## When to pause (two events)

The pipeline **does not** insert a mandatory stop in code. **You** choose when to pause. Default expectation: **pause for strategy** unless the user explicitly asked for a single straight-through run (see [../process.md](../process.md) — *Strategy: ask once*).

### Event A — After the spec is drafted, before you trust chunks

| | |
|--|--|
| **What the tool does** | A full `index_memory.py` run **drafts** the spec (when needed), then **continues in the same process**: chunk → embed. It does **not** wait for you. |
| **What you should do** | **Pause** after the draft exists: open and edit `memory/context_chunking_spec.yaml` (and rely on the structural report) **before** treating `memory/` chunk files as final. To avoid chunking until YAML is ready, use the **split workflow** in [../process.md](../process.md): convert + draft only → edit YAML → `index_memory.py --skip-convert --skip-spec`. |
| **What the user does** | Chooses **strategy pass** vs **straight through** when asked; if strategy pass, expects a review step before embeddings are treated as production-ready. |

### Event B — Chunk output looks wrong (splits, sizes, counts)

| | |
|--|--|
| **What went wrong** | Examples: split mid-table, wrong sections, **one giant chunk**, **absurd split counts**. |
| **What you should do** | **Pause**—do **not** hand off or declare success. **Edit** the spec and/or **preprocess** markdown (inject headings, dedupe running headers, fix regexes). Set **`chunk_inputs`** if extra `.md` files pollute the scan. **Re-run** `chunk_markdown.py` or `index_memory.py --skip-convert --skip-spec`. **Verify** chunk count and spot-check files. **Repeat** until boundaries and sizes look right, then involve the user. |
| **What the user does** | Gets a corpus that is actually retrievable—not a first-cut disaster—because you stopped and fixed instead of shipping bad chunks. |

### Event C — Markdown is semantically messy (no trustworthy headings)

| | |
|--|--|
| **What you should do** | **Before** relying only on regex tweaks, run an **AI semantic pass**: infer what belongs together, name topics and sub-topics, inject structure or a cleaned file, **finish one full pass**, then review and iterate. See [convert-to-markdown.md](convert-to-markdown.md) (*Last resort: semantic / topic pass*). |
| **Rule** | The chunker follows **structure you give it**; it does not replace reading for meaning. |

```bash
python scripts/index_memory.py --path <source_folder> --skip-convert --skip-spec
```

Use `--rebuild` when only embeddings must refresh from existing chunks.

---

## Before the user trusts chunked output — checklist

| Topic | You check |
|-------|-----------|
| **Boundaries** | Do `section_boundaries` regexes match real chapter/section breaks? False positives? |
| **Tables / lists** | Should tables stay intact? Templates that need their own rule? |
| **Noise** | ToC, headers, license blocks—exclude or tag (`metadata_noise`, etc.)? |
| **Taxonomy** | Did you fill `evidence_type` / `chunk_type` from **this** source (not a generic list)? |
| **Defaults** | Do defaults match “most chunks” until you relabel? |

**Tell the user** what was inferred from structure vs what still needs eyeballing on the real markdown.

---

## Workflow (ordered)

1. **You** run `draft_chunking_spec.py --path <source>` (or a full `index_memory` once, then **pause**—see Event A). Outputs include **`markdown/structural_scan_report.*`** and **`memory/context_chunking_spec.yaml`** when new.
2. **You** review and edit `context_chunking_spec.yaml` (especially taxonomy and boundaries).
3. **You** run `index_memory.py --path <source> --skip-convert --skip-spec` when the spec is ready (`--skip-spec` skips **re-drafting**; an existing file is **loaded** for chunking).

Full command matrices and strategy vs straight-through: [../process.md](../process.md) and [script-invocation.md](script-invocation.md).
