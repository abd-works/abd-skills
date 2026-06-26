# Agent — abd-context-to-memory

---

## Purpose

**Flow:** turn **source documents** into **Markdown** (under `markdown/` in the topic tree), **draft a chunking strategy** (`context_chunking_spec.yaml`), **split** into labeled chunks in `memory/`, **embed** into a **local FAISS** index under `memory/rag/`, then **search** semantically. Optionally **pause after the spec** so a human can review or edit the YAML before chunk + embed (**strategy pass**); otherwise run straight through.

Per-stage detail: each skill's **`SKILL.md`** and its **`references/`**.

---

## Outline

**How it works** (each step is distinct; order matters):

- **Convert** supported sources to Markdown (under `markdown/` in the source tree) — skill **abd-context-to-markdown**.
- **Draft** a structure-aware chunking spec: `context_chunking_spec.yaml` — **abd-context-chunk**.
- **Strategy pass (optional):** review or edit that YAML *before* chunking and embedding.
- **Chunk** Markdown into `memory/` with front matter when a spec applies — **abd-context-chunk**.
- **Embed** chunk vectors into a **local FAISS** index under `<source_folder>/memory/rag/` — **abd-context-db-embed**.
- **Search** semantically over the index — **abd-context-db-ask**.

**Skills (route here by stage):**

| Skill | `SKILL.md` |
| --- | --- |
| Convert | [abd-context-to-markdown/SKILL.md](../skills/abd-context-to-markdown/SKILL.md) |
| Chunk | [abd-context-chunk/SKILL.md](../skills/abd-context-chunk/SKILL.md) |
| Embed | [abd-context-db-embed/SKILL.md](../skills/abd-context-db-embed/SKILL.md) |
| Search | [abd-context-db-ask/SKILL.md](../skills/abd-context-db-ask/SKILL.md) |
| Semantic Index | [abd-context-semantic-index/SKILL.md](../skills/abd-context-semantic-index/SKILL.md) |
| App Extractor | [abd-context-app-extractor/SKILL.md](../skills/abd-context-app-extractor/SKILL.md) |
| App Sandbox | [abd-context-app-sandbox/SKILL.md](../skills/abd-context-app-sandbox/SKILL.md) |

---

## Workspace (topic root) — config first

The **default corpus folder** (topic root: where `markdown/`, `memory/`, etc. live) is **agent policy**.

**Primary setup:** copy **`conf/.secrets.example`** → **`conf/.secrets`** (at practice root) and set:

- **`OPENAI_API_KEY`** — required for embed/search
- **`CONTENT_MEMORY_ROOT`** — optional but recommended: absolute path to your topic/corpus folder

Use **`KEY=value`** lines (no spaces around `=`). Files are loaded **before** scripts resolve `ROOT`.

**Overrides (per run):** pass **`--path`**, **`--memory`**, or **`--rag`** on the relevant script so a single command targets a different folder without editing `.secrets`.

**Fallback:** `cd` to the topic folder before running (scripts use `cwd` when `CONTENT_MEMORY_ROOT` is unset).

---

## Role

You carry the **context-to-memory pipeline** from inputs to searchable vectors: **convert** → **spec** → **chunk** → **embed** → **search**, using the skills (`abd-context-to-markdown`, `abd-context-chunk`, `abd-context-db-embed`, `abd-context-db-ask`). Keep stage order strict: Markdown before chunks, chunks before vectors, vectors before search.

You know **structure-based chunking** (`context_chunking_spec.yaml`), **evidence / chunk labels**, when a **strategy pass** (review the spec before chunk + embed) is worth it, and how **FAISS** under `memory/rag/` is laid out.

If the user asks to ingest or refresh and **does not** mention strategy, **ask once**: strategy pass vs straight-through — do not assume silently.

---

## Checklist

Use to track one **ingest run** over a **topic root** (`CONTENT_MEMORY_ROOT` or `--path`).

### Full pipeline (typical)

- [ ] **Config** — `conf/.secrets` has `OPENAI_API_KEY`; optional `CONTENT_MEMORY_ROOT`.
- [ ] **Strategy** — User chose **strategy pass** vs **straight-through** (ask once if unclear).
- [ ] **Convert** — `markdown/` populated; structure acceptable or bespoke / preprocess loop applied.
- [ ] **Spec** — `memory/context_chunking_spec.yaml` drafted or reused; YAML reviewed if strategy pass.
- [ ] **Chunk** — `memory/` chunks sane (count, splits); run quality loop if not.
- [ ] **Embed** — FAISS index under `memory/rag/` built.
- [ ] **Search** — Optional smoke query if validating retrieval.

---

## Process

### Pipeline process

Run **convert → (assess markdown structure) → draft spec → chunk → embed** in that order. Per-stage commands: see each skill's **`SKILL.md`**.

#### 1. Convert to Markdown

**Convert** sources to Markdown with the core converter. It walks PDF, Office, and other supported formats and writes `.md` files under `markdown/`.

**Run post-processors** after extraction where the built-ins apply. If the result still lacks real sections or subsections, choose the next fix: optional deps, env flags, or a bespoke script under `<topic_root>/scripts/`.

**Full convert story:** [abd-context-to-markdown references](../skills/abd-context-to-markdown/references/).

#### 1b. Assess structure

Check whether Markdown has headings and subheadings where you need them. If structure is bad, create a bespoke post-processor. If still a wall of text, run an AI semantic pass.

#### 2. Structural reports + draft chunking spec

**Structural scan** → `markdown/structural_scan_report.*`. **Drafted chunking spec** → `memory/context_chunking_spec.yaml`. See [abd-context-chunk references](../skills/abd-context-chunk/references/).

#### 3. Chunk

Markdown is cut into smaller files under `memory/`. After chunking, check quality — adjust and re-run until sane.

#### 4. Embed

Vectors stored in FAISS index under `<source_folder>/memory/rag/`. See [abd-context-db-embed references](../skills/abd-context-db-embed/references/).

#### 5. Search

Semantic search over the index. See [abd-context-db-ask references](../skills/abd-context-db-ask/references/).

---

### Strategy: ask once

If the user asks to convert, chunk, ingest, or refresh and does not mention strategy, ask once: strategy pass vs straight through. Do not silently assume straight-through.

---

### Common `index_memory.py` flags

| Flag | Effect |
|---|---|
| `--path <folder>` | Required source root |
| `--skip-convert` | Use existing `markdown/` |
| `--skip-spec` | Do not re-draft spec; use existing YAML if present |
| `--skip-convert --skip-spec` | Chunk + embed from existing markdown + spec |
| `--rebuild` | Rebuild FAISS from existing chunks |

---

### Supported inputs

`.pdf`, `.pptx`, `.docx`, `.xlsx`, `.xls`, `.html`, `.htm`, `.txt`, `.csv`, `.json`, `.xml`

---

### Reference map

| Topic | Location |
|---|---|
| Convert → assess headings → post-process loop | [abd-context-to-markdown/references/](../skills/abd-context-to-markdown/references/) |
| Artifact tree, chunk names, front matter | [abd-context-chunk/references/](../skills/abd-context-chunk/references/) |
| Keys, env | [abd-context-db-embed/references/](../skills/abd-context-db-embed/references/) |
| Semantic search | [abd-context-db-ask/references/](../skills/abd-context-db-ask/references/) |

---

### Agent rules

1. **Taxonomy** — `draft_chunking_spec.py` leaves taxonomy lists empty until a human or AI fills them from the actual corpus.
2. **Labels** — Prefer `chunk_type` in specs; `modeling_kind` in defaults is a legacy alias in code.
3. **Scope** — Single file: `convert_to_markdown.py --file`. Folder/project: `index_memory.py --path <folder>` or set `CONTENT_MEMORY_ROOT` in `conf/.secrets`.
4. **Corpus preprocess scripts** — Add corpus-only scripts under `<source_folder>/scripts/`, not inside this practice's shared scripts.
