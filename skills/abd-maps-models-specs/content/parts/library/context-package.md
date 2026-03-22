# Canonical context package (Phase 1)

Normative **file shapes**, **config**, **validators**, and **generation** for Phase 1 only: frozen **`chunks/*.md`** + **`context_index.json`** with provenance. This is the **evidence layer**—not terms, story maps, or domain types (those are later phases; see [`content/parts/process.md`](../content/parts/process.md)).

Paths resolve from **`<skill_path>/conf/abd-config.json`** → **`active_skill_workspace`** (skill workspace root), then **`<skill_workspace>/solution.conf`** (see [`conf/README.md`](../../../conf/README.md)). `scripts/_config.py` implements the same layering: **`manifest_sources[]`** and paths live in `solution.conf`, not hardcoded in Python. Deprecated: `solution_workspace`, `skill_space_path`.

**Process context:** Stage 1 Phase 1 in [`content/parts/process.md`](../content/parts/process.md) and [`phases/canonical-context.md`](../content/parts/phases/canonical-context.md).

---

## Runnable pipeline (scripts)

Runnable automation for Phase 1 lives under **`scripts/`**. This is **the same phase** as “write chunking spec + produce chunks + index” in the process table—not a separate front-loaded step.

**Context build** (entry point name TBD, e.g. `build_context.py`) performs:

1. Loads **canonical Markdown** from paths declared in **`solution.conf`**: `manifest_sources[]` lists each file (`path` + `role`) under the workspace; `source_path` names the docs directory for discovery when needed. The chunking spec file is named by `context_chunking_spec` (default `context_chunking_spec.yaml` next to `solution.conf`).
2. Loads the **chunking spec** YAML (see [Chunking spec](#chunking-spec-config-not-vibes)).
3. Writes **`CHUNKS_DIR`** and **`CONTEXT_INDEX`** per [Chunk files](#chunk-files) and [Index file](#index-file).
4. Optionally runs a **post-pass** classification step (optional LLM in [Generation](#generation-code-first)) that fills only fields already allowed by the schema.

**`scripts/build.py`** runs `phase0_context_audit.py` first (Phase 0), then **`validate_context_contract.py`** when an index exists, then invokes this Phase 1 entry point **when the builder is implemented** and a rebuild is requested. Until then, Phase 0 records readiness; Phase 1 outputs are produced manually or by external tooling but must still satisfy this document before freeze.

When chunking rules change, **update the single Phase 1 entry point** in `scripts/` so one implementation path reflects the new rule set.

---

## Purpose

Downstream phases cite **`chunk_id`** only. Provenance means: every `chunk_id` resolves to **(a)** a chunk file, **(b)** a row in the index, **(c)** a machine-checkable location in the canonical source.

---

## Canonical sources

- **Declared in** `<workspace>/solution.conf` → **`manifest_sources`**: an array of `{ "path": "<relative-to-workspace>", "role": "<string>" }`. Example: `{ "path": "docs/HeroesHandbook.md", "role": "canonical_handbook" }` for the MM3 workspace under `test/mm3/`. Add or rename entries here when the corpus changes—**do not** scatter paths only in prose or only in Python.
- **Recorded in** `context_index.json` → `manifest.sources[]` by the builder (same `path` and `role`, plus runtime fields):
  - `path` — **workspace-relative** string (same strings as `solution.conf`, normalized to forward slashes).
  - `role` — copied from the declaration (e.g. `canonical_handbook`).
  - `sha256` — **required** when the file exists (hex digest of raw file bytes as read by the builder, typically UTF-8 text).
  - Optional: `byte_length`, `note` (converter / generator id).
- **`_config.py`** exposes `resolved_manifest_sources()` so validators and Phase 0 hash the same files the index claims.

---

## Chunk files

- **Directory:** `<workspace>/<context_path>/chunks/` (`context_path` from `solution.conf`, default `context/chunks/`).
- **Filename:** `{chunk_id}.md` where `chunk_id` matches `^[a-z0-9_]+$` (or project convention documented once—must match index).
- **Format:** YAML **front matter** + Markdown **body** (body = evidence text only).

**Required front matter keys:**

| Key             | Type   | Meaning                                                                                                       |
| --------------- | ------ | ------------------------------------------------------------------------------------------------------------- |
| `chunk_id`      | string | Must equal filename stem.                                                                                     |
| `source`        | object | Provenance anchor (see below).                                                                                |
| `evidence_type` | string | Taxonomy enum (e.g. `definition`, `rule`, `example`, `table`, `metadata_noise`, `mixed`). Aligned with index. |
| `modeling_kind` | string | What **not** to promote blindly (e.g. `definition`, `rule`, `example`, `noise`, `structural_only`).           |

**`source` object (at least one checkable anchor):**

- `canonical_path` — relative path string matching manifest (e.g. `docs/HeroesHandbook.md`).
- **Either:**
  - `line_start` / `line_end` — inclusive 1-based line numbers in that file after normalization used by the builder (documented in spec), **or**
  - `heading_path` — array of strings (e.g. `["Chapter 3", "Powers"]`) **plus** optional `line_start` / `line_end` for disambiguation.

Validators **must** verify line numbers against actual file line count when `line_*` is present.

---

## Index file

- **Path:** `<workspace>/<context_path>/context_index.json` (`CONTEXT_INDEX` in `_config.py`).
- **`spec_version`:** `"1"` (bump when breaking).

**Top-level keys:**

| Key            | Meaning                                                                             |
| -------------- | ----------------------------------------------------------------------------------- |
| `spec_version` | String.                                                                             |
| `manifest`     | See [Canonical sources](#canonical-sources) + `generator`: `{ "name": "<script>", "version": "<semver or git sha>" }`. |
| `blocks`       | Array of block records (one per chunk for 1:1 mapping).                             |
| `excluded`     | Optional: `{ "chunk_id": "...", "reason": "..." }[]` for explicit drops.            |

**Each `blocks[]` element (minimum):**

| Field                    | Meaning                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `block_id` or `chunk_id` | Same as chunk filename stem (pick one name in schema; **must** match chunk file).     |
| `section_path`           | Array of strings (breadcrumb).                                                        |
| `evidence_type`          | Same enum as front matter.                                                            |
| `modeling_kind`          | Same as front matter.                                                                 |
| `modeling_priority`      | Optional number or string for stratified reading.                                     |
| `source_anchor`          | Duplicate of `source` from front matter (enables queries without opening every file). |
| `preview`                | Short plain-text preview (first N chars).                                             |
| `reason`                 | Optional: e.g. `structural heading only`, `below_min_chunk`, `merged_table`.          |

Optional forward indexes (`concept_seeds`, `reverse_indexes`) **supplement** `blocks[]` and chunk files; **citations** for modeling still resolve through `blocks[]` and `chunks/{chunk_id}.md`.

---

## Validation (deterministic code)

- **Script:** `scripts/validate_context_contract.py` (implements chunk + index checks described here).
- **Rules:**
  - Every `blocks[]` entry has a file `chunks/{chunk_id}.md`.
  - Every `chunks/*.md` is listed in `blocks[]` **or** listed under `excluded` with reason.
  - Front matter parses; required keys present; `chunk_id` matches filename.
  - `source.line_*` within source file length; `canonical_path` matches a `manifest.sources[].path`.
  - No duplicate `chunk_id`.

---

## Chunking spec (config, not vibes)

- **File:** Resolved from `solution.conf` → `context_chunking_spec` (path relative to **workspace root**). The MM3 fixture uses `test/mm3/context_chunking_spec.yaml`. Operators may point another workspace at a shared file under `conf/` if needed.
- **Contents (minimum sections):**
  - `section_boundaries` — `section_break_regex`, `chapter_break_regex`, `all_caps_standalone`, limits. **Operators edit** this spec when handbook layout changes; the context builder reads these values from the YAML.
  - `splitting` — min/max chunk size, table handling (keep table in one chunk vs split), heading capture rules.
  - `defaults` — default `evidence_type` / `modeling_kind` when heuristics assign them.
  - `taxonomy` — allowed values for `evidence_type` and `modeling_kind` (single enum list for validators).

---

## Generation (code-first)

- **Deterministic Python** loads canonical MD, applies **only** rules from `context_chunking_spec.yaml`, assigns `chunk_id` (deterministic algorithm: e.g. hash of anchor + ordinal, or sequential `unit_001` with stable sort), writes chunks + index.
- **Optional LLM** (not required for Phase 1 exit): may **refine** `evidence_type` / `modeling_kind` **after** blocks exist. Output **must** be written back as **valid** front matter + index rows and **pass** `validate_context_contract.py`. No free-text “evidence” without `chunk_id`.

---

## Downstream citation rule

Phases **2–8** reference evidence by **`chunk_id`** (and optional story anchors). Substantive claims in automated artifacts **cite** those ids; the index and chunk files are the resolution path.

---

*Bump `spec_version` in the index when this schema breaks compatibility.*
