# Context Specification (Phase 1)

Enduring reference for **`chunks/*.md`**, **`context_index.json`**, **manifest** provenance, **`context_chunking_spec`** YAML (chunking rules the **solution analyst** maintains in the workspace—see [`solution-analyst-role.md`](../solution-analyst-role.md)), and the **contract** those artifacts must satisfy. **Process** lives in the phase files, not here: **Phase 0** (AI-led chunking spec + human review) [`phases/context-chunking-approach.md`](../phases/context-chunking-approach.md); **Phase 1** (build, coherence, validate) [`phases/canonical-context.md`](../phases/canonical-context.md). The **built** chunk files + index + manifest are sometimes called the **context package** in prose; **this file** is the **spec** that defines them.

See [`content/parts/process.md`](../content/parts/process.md), [`phases/context-chunking-approach.md`](../phases/context-chunking-approach.md), [`phases/canonical-context.md`](../phases/canonical-context.md), and [`conf/README.md`](../../../conf/README.md).

Paths resolve from **`<skill_path>/conf/abd-config.json`** → **`active_skill_workspace`** (skill workspace root), then **`<skill_workspace>/solution.conf`**. `scripts/_config.py` implements the same layering: **`manifest_sources[]`** and paths live in `solution.conf`, not hardcoded in Python. Deprecated: `solution_workspace`, `skill_space_path`.

---

## Purpose

The **context specification** exists so we do not treat a large canonical Markdown corpus as an undifferentiated blob. The spec **defines the contract** for turning source material into **addressable units** (chunks + index) and for **classifying** each unit along **two** axes: **`evidence_type`** — **form** in the manuscript (definition block, rule, example, table, …); **`modeling_kind`** — **stance** for modeling (how much weight this chunk gets when citing for vocabulary, stories, types—not the same as literary “what kind of sentence is this,” and often **correlated** with `evidence_type` but **diverging** when form and purpose split). Those enums live in the **chunking spec** (`taxonomy`) so the same vocabulary is enforced by validators and shared across humans and tools—**not** invented per file or per prompt.

Doing it this way keeps **where** evidence lives and **what** it is as *source* separate from **what** it becomes in later artifacts (terms, mechanisms, stories, types). The spec does not mint domain concepts; it **labels and locates** slices of the corpus so promotion and citation can apply **layer-appropriate** rules. Chunk files, the index, and **`chunk_id`** are how we **find** and **cite** those slices consistently; they serve the contract above, and are not the purpose of the spec by themselves.

**Why YAML chunking rules + schemas:** The **solution analyst** needs a **single, editable control surface** (boundaries, splits, defaults, taxonomy) that tracks **document structure** when handbooks change. **Phase 0** ([`phases/context-chunking-approach.md`](../phases/context-chunking-approach.md)) is **AI-led**: an agent drafts that YAML from **`manifest_sources`** and **discloses** assumptions; the analyst **reviews** and lands the file. Deterministic code applies that spec when emitting chunks so grain and labels stay **reproducible**; a **coherence pass** (typically **LLM**—see [`phases/canonical-context.md`](../phases/canonical-context.md) **§2**) re-checks outputs **against the original canonical Markdown** and aligns **schema-allowed** fields so chunk text, `evidence_type` / `modeling_kind`, and index rows **do not contradict** each other or the **source**. Final output **must** still **validate** against the same shapes.

This specification is scoped to **structured evidence from canonical sources**. It does not define terms, story maps, or domain types—those layers consume this output under their own rules (see [`principles-and-rules.md`](principles-and-rules.md) on provenance vs promotion).

---

## What goes in a context spec (Phase 1)

A **context spec** is not one file—it is the **whole contract** that ties together **context rules** (how to cut and label the corpus), **evidence units** (what each slice carries), **corpus bookkeeping** (which **source files** were inputs, **sha256** integrity for each, and **`manifest.generator`**—**which script and version** produced the chunks and index), and **enforcement** (validators implement the shapes below). **How** Phase 1 emits **`chunks/`** and **`context_index.json`** and which **`scripts/`** you run is **not** defined here—see [`phases/canonical-context.md`](../phases/canonical-context.md) (Phase 1); authoring **`context_chunking_spec`** from sources is [`phases/context-chunking-approach.md`](../phases/context-chunking-approach.md) (Phase 0). Together those answer: *what counts as a unit of evidence, how is it classified, and how do we prove it came from the declared sources?*

**Out of scope:** Domain model, story map, shaped story map JSON, **`concepts[]`**—later phases consume this package under their own contracts.

**Artifacts at a glance**


| Role                      | Typical artifact                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------- |
| Canonical source list     | `manifest_sources[]` in `solution.conf`                                               |
| Chunking rules + taxonomy | `context_chunking_spec` YAML (path from `solution.conf`)                              |
| Evidence units            | `<context_path>/chunks/{chunk_id}.md`                                                 |
| Index + manifest          | `<context_path>/context_index.json`                                                   |
| Contract (shape rules)    | Defined **here** + **`rules/scanners.json`**; scanner **entry points** are described in [`canonical-context.md`](../phases/canonical-context.md) **§7.4** |
| Build pipeline / scripts  | [`canonical-context.md`](../phases/canonical-context.md) **§2** (two-pass model, **§2.1**–**§2.2**) |


Normative shapes follow **by file** under **Format**, with a **matching example** in each subsection (same MM3-style thread: **`powers_attack_003`**).

---

## Format (by file)

**Thread for examples:** MM3-style workspace, canonical handbook `docs/HeroesHandbook.md`, chunk id **`powers_attack_003`**—each fragment below is the **same** evidence unit across the four artifacts.

### `solution.conf` — `manifest_sources[]`

Authoritative **before** build: which canonical Markdown files count as sources.

- **Declared in** `<workspace>/solution.conf` → **`manifest_sources`**: array of `{ "path": "<relative-to-workspace>", "role": "<string>" }`. Example: `{ "path": "docs/HeroesHandbook.md", "role": "canonical_handbook" }` for the MM3 workspace under `test/mm3/`. Add or rename entries when the corpus changes—**do not** scatter paths only in prose or only in Python.
- **Also in** `solution.conf`: `context_path` (default `context/`), **`context_chunking_spec`** path (default `context_chunking_spec.yaml`), and other workspace keys—see [`conf/README.md`](../../../conf/README.md) and `scripts/_config.py`.
- **Recorded in** `context_index.json` → `manifest.sources[]` when the index is written (same `path` and `role`, plus runtime fields):
  - `path` — **workspace-relative** string (same strings as `solution.conf`, normalized to forward slashes).
  - `role` — copied from the declaration (e.g. `canonical_handbook`).
  - `sha256` — **required** when the file exists (hex digest of raw file bytes as read for the manifest, typically UTF-8 text).
  - Optional: `byte_length`, `note` (converter / generator id).
- **`_config.py`** exposes `resolved_manifest_sources()` so validators and Phase 0 hash the same files the index claims.

**Example (fragment from an MM3-style `solution.conf`):** keys vary by workspace; this shows how sources and chunking spec path hang together.

```json
{
  "output_dir": "abd-maps-models-specs",
  "context_path": "context",
  "source_path": "docs",
  "context_chunking_spec": "context_chunking_spec.yaml",
  "manifest_sources": [
    { "path": "docs/HeroesHandbook.md", "role": "canonical_handbook" }
  ]
}
```

### `context_chunking_spec` (YAML)

**Role:** Rules the **solution analyst** authors so the emit step knows **how** to split and default-label the corpus; **`taxonomy`** declares allowed `evidence_type` / `modeling_kind` values (closed-world for validators).

- **Path:** Resolved from `solution.conf` → `context_chunking_spec` (relative to **workspace root**—see `scripts/_config.py` → `context_chunking_spec_path()`). Default basename is `context_chunking_spec.yaml` beside `solution.conf`. When `conf/abd-config.json` sets `active_skill_workspace` to `test/mm3`, that workspace often keeps the YAML beside `solution.conf`—not required for every repo.
- **Contents (minimum sections):**
  - `section_boundaries` — `section_break_regex`, `chapter_break_regex`, `all_caps_standalone`, limits. Edit when handbook layout changes.
  - `splitting` — min/max chunk size, table handling (keep table in one chunk vs split), heading capture rules.
  - `defaults` — default `evidence_type` / `modeling_kind` when heuristics assign them.
  - `taxonomy` — allowed values for `evidence_type` and `modeling_kind` (single enum list for validators).

**Example (excerpt):** one workspace’s **real** chunking file would name regexes and limits that match *that* handbook’s Markdown (headings like `# Chapter 3 — Powers`, `## Attack`, tables that must stay whole). The lists below are the same values **`powers_attack_003`** uses in the chunk and index examples.

```yaml
# Excerpt only — full file would add more tuning per project.
taxonomy:
  evidence_type: [definition, rule, example, table, metadata_noise, mixed]
  modeling_kind: [definition, rule, example, noise, structural_only]
section_boundaries:
  chapter_break_regex: "^#\\s+Chapter\\s+\\d+"
  section_break_regex: "^##\\s+"
  all_caps_standalone: true
splitting:
  min_chunk_chars: 400
  max_chunk_chars: 8000
  keep_markdown_tables_intact: true
  split_on_heading_level: 3
defaults:
  evidence_type: rule
  modeling_kind: rule
```

### Chunk files — `chunks/{chunk_id}.md`

**Role:** One **evidence unit** per file: classification + provenance + body text. The index **summarizes** chunks; it does not replace them.

- **Directory:** `<workspace>/<context_path>/chunks/` (`context_path` from `solution.conf`, default `context/chunks/`).
- **Filename:** `{chunk_id}.md` where `chunk_id` matches `^[a-z0-9_]+$` (or project convention documented once—must match index).
- **Body:** YAML **front matter** + Markdown **body** (body = evidence text only).

**Required front matter keys:**


| Key             | Type   | Meaning                                                                                                                                                                                                          |
| --------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chunk_id`      | string | Must equal filename stem.                                                                                                                                                                                        |
| `source`        | object | Provenance anchor (see below).                                                                                                                                                                                   |
| `evidence_type` | string | Taxonomy enum (e.g. `definition`, `rule`, `example`, `table`, `metadata_noise`, `mixed`). Aligned with index.                                                                                                    |
| `modeling_kind` | string | How **later modeling phases** should **treat** this chunk (see below). Allowed values come from **`taxonomy`** in the chunking spec—often overlapping labels with `evidence_type`, but **meaning** is different. |

### `evidence_type` vs `modeling_kind`

They are **two axes**, not two names for the same thing. The confusion is that both taxonomies often reuse words like `rule` or `example`—so they **look** redundant when they **match**. They differ when **form in the manuscript** and **how we use the chunk for modeling** come apart.


| Axis | Question it answers | Think of it as |
| --- | --- | --- |
| **`evidence_type`** | **What does this chunk look like in the source?** (genre / layout of the text) | **Form** — definition block, rule paragraph, worked example, table, boilerplate, mixed block, … |
| **`modeling_kind`** | **How should modeling work treat this chunk** when we cite it for vocabulary, stories, and types—not linguistics, but **weight and purpose** | **Stance** — substantive backing vs illustration-only vs out of scope for domain truth |


**Why values overlap:** In many chunks, form and stance **align**: a “rule” in the book is also **substantive** for the model, so `evidence_type: rule` and `modeling_kind: rule` are both **correct** and **correlated**. That is normal. The second field is still there for **mismatches** (below) and for tooling that keys off **stance** without re-deriving it from layout.

**When they differ (this is the real distinction):**


| `evidence_type` (form) | `modeling_kind` (stance) | What’s going on                                                                                                                             |
| ---------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `table`                | `rule`                   | The **surface** is a table; for modeling we treat it as **normative** (e.g. authoritative numbers or constraints).                          |
| `example`              | `example`                | The **source** is a **worked example**; modeling uses it as **illustration**, not as a shortcut to mint types.                              |
| `rule`                 | `noise`                  | The text is **phrased** as a rule, but for **this** solution it’s **repeated boilerplate** or out-of-scope—we don’t cite it for vocabulary. |
| `definition`           | `structural_only`        | It **looks** like a definition line, but it’s **nav / chapter chrome**—we don’t mine it for terms.                                          |


If you **never** need that split, defaults can keep both fields in sync—but **`evidence_type` alone cannot express** “table-shaped, but normative for modeling” vs “table-shaped, illustration only.”

**Promotion** (later phases) is still **separate**: `modeling_kind` does **not** create terms or `concepts[]` rows; it only signals **how** to use the chunk when **you** promote with evidence (see [`principles-and-rules.md`](principles-and-rules.md) on provenance vs promotion).

**When would something ever be “promoted”?** Only when **you** (or a gated phase) **explicitly** promote it: e.g. Phase 2 **terms**, Phase 3 **story map** with **`evidence_chunk_ids[]`**, Phase 4+ **`concepts[]`** with evidence links. Relabeling or splitting chunks can change stance without changing the handbook.

**Optional taxonomy tweak:** If overlapping words stay confusing, your **`taxonomy`** can use **stance-only** labels for `modeling_kind` (e.g. `substantive`, `illustrative`, `ignore_for_domain`) instead of reusing `rule` / `example`—as long as validators and the index stay consistent.

**`source` object (at least one checkable anchor):**

- `canonical_path` — relative path string matching manifest (e.g. `docs/HeroesHandbook.md`).
- **Either:**
  - `line_start` / `line_end` — inclusive 1-based line numbers in that file after normalization used when emitting chunks (documented in spec), **or**
  - `heading_path` — array of strings (e.g. `["Chapter 3", "Powers"]`) **plus** optional `line_start` / `line_end` for disambiguation.

Validators **must** verify line numbers against actual file line count when `line_`* is present.

**Example (`context/chunks/powers_attack_003.md`):**

```markdown
---
chunk_id: powers_attack_003
source:
  canonical_path: docs/HeroesHandbook.md
  line_start: 1204
  line_end: 1238
evidence_type: rule
modeling_kind: rule
---

When you make an attack roll, compare your result to the target’s defense. If you hit, apply damage from the power or weapon used; if the power says otherwise, follow that text instead.
```

### `context_index.json`

**Role:** Aggregate **schema version**, **manifest** (sources + hashes + **`generator`** name/version), **`blocks[]`** (one row per chunk), optional **`excluded[]`**.

- **Path:** `<workspace>/<context_path>/context_index.json` (`CONTEXT_INDEX` in `_config.py`).
- **`spec_version`:** `"1"` (bump when breaking).

**Top-level keys:**


| Key            | Meaning                                                                            |
| -------------- | ---------------------------------------------------------------------------------- |
| `spec_version` | String.                                                                            |
| `manifest`     | Sources + `generator`: `{ "name": "<script>", "version": "<semver or git sha>" }`. |
| `blocks`       | Array of block records (one per chunk for 1:1 mapping).                            |
| `excluded`     | Optional: `{ "chunk_id": "...", "reason": "..." }[]` for explicit drops.           |


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

**Example (`context/context_index.json`, fragment):** same handbook path, **`powers_attack_003`**, and preview text aligned with the chunk body above. The **`sha256`** is illustrative (computed from the real file bytes). *Bump `spec_version` when the schema breaks compatibility.*

```json
{
  "spec_version": "1",
  "manifest": {
    "sources": [
      {
        "path": "docs/HeroesHandbook.md",
        "role": "canonical_handbook",
        "sha256": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
      }
    ],
    "generator": { "name": "build_context.py", "version": "0.1.0" }
  },
  "blocks": [
    {
      "chunk_id": "powers_attack_003",
      "section_path": ["Chapter 3 — Powers", "Attack"],
      "evidence_type": "rule",
      "modeling_kind": "rule",
      "source_anchor": {
        "canonical_path": "docs/HeroesHandbook.md",
        "line_start": 1204,
        "line_end": 1238
      },
      "preview": "When you make an attack roll, compare your result to the target’s defense."
    }
  ]
}
```

---

## Validation checklist

**Coherence (automated pipeline)**

- A **coherence pass** has run after deterministic chunk generation: outputs have been checked **against the original canonical Markdown** so chunking **strategy** is plausible; **`evidence_type`**, **`modeling_kind`**, **`preview`**, and other schema fields **match** chunk body and **source** intent (no “rule” label on pure fluff, no preview that contradicts the text). Use an **LLM** constrained to schema-allowed edits, or a **human review** with the same bar—see [`canonical-context.md`](../phases/canonical-context.md) **§2**.

**Contract (when `context_index.json` exists)**

- **Enforcement:** the skill’s **contract scanners** implement the checks below (see [`canonical-context.md`](../phases/canonical-context.md) **§7.4** and **`rules/scanners.json`** for script paths).
- Every `blocks[]` entry has a file `chunks/{chunk_id}.md`.
- Every `chunks/*.md` is listed in `blocks[]` **or** listed under `excluded` with reason.
- Front matter parses; required keys present; `chunk_id` matches filename.
- `source.line_*` within source file length; `canonical_path` matches a `manifest.sources[].path`.
- No duplicate `chunk_id`.

**Sources and manifest**

- `manifest_sources[]` in `solution.conf` lists every canonical file that may appear in the index manifest; paths stay workspace-relative and consistent with the index manifest.

**Chunking spec**

- `context_chunking_spec` path resolves; YAML includes enough structure for **`section_boundaries`**, **`splitting`**, **`defaults`**, **`taxonomy`** (allowed enums for validators).

**Downstream**

- Later phases can resolve every cited **`chunk_id`** to chunk file + index row + source anchor.

