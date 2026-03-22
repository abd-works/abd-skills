# Context corpus: chunks, index, and how this skill uses them

This skill **consumes** a **chunked corpus** plus an **index** (`chunks/*.md` + `context_index.json`). **Normative schema, config locations, and validators** for Phase 1 are in [`context-package.md`](context-package.md).

**Producing** that package is **Phase 1**: canonical Markdown (paths from **`solution.conf` → `manifest_sources[]`**, resolved by `_config.py`) → chunking per **`context_chunking_spec`** (YAML named in `solution.conf`) → validated **`chunks/`** + **`context_index.json`**. The MM3 fixture lists `docs/HeroesHandbook.md` there; your workspace lists its own files—**do not** rely on a single hardcoded repo path in docs alone.

**Pipeline shape (this skill):** conversion to canonical Markdown (when needed) → **Phase 1** context-build entry point under **`scripts/`** (see [`context-package.md`](context-package.md)) → chunk files + index → **`validate_context_contract.py`**. The chunking spec is the operator-editable control surface; automation reads it.

On a **greenfield** fixture, Phase 0 uses the same criteria as **acceptance tests** for the **first** Phase 1 output once `chunks/` and the index exist.

---

## What a healthy corpus provides

1. **Stable IDs** — Chunks or blocks addressable for citations (`chunk_id` / `block_id` aligned with files).
2. **Evidence typing** — `evidence_type` (and related fields) usable for **stratified sampling** and **promotion gates** (rule vs example vs noise).
3. **Coverage** — Domain-relevant material is represented; excluded material is **explicit** in the index.
4. **Versioning** — Source hash or date + generator provenance when rebuilding.

---

## Typical flow (conceptual)

| Step | Role | What happens |
| --- | --- | --- |
| **Convert** | Human + tooling | Source files (PDF, DOCX, …) → canonical Markdown where needed |
| **Configure** | Human | Edit **`solution.conf`** (`manifest_sources`, `context_chunking_spec`, paths) and the chunking YAML (boundaries, splits, taxonomy defaults) |
| **Build** | Code | Context builder under `scripts/` reads canonical MD + spec → `chunks/*.md` + `context_index.json` |
| **Validate** | Code | `validate_context_contract.py` enforces [`context-package.md`](context-package.md) |

**Curate** (classify regions, exclude noise, assign `evidence_type`) lives **inside** the builder’s rules and spec—not as a separate undocumented script path.

### Illustrative chunk file

```yaml
---
chunk_id: blk_00042
source: HeroesHandbook
evidence_type: domain-rule
section_path: ["Chapter 3", "Abilities", "Ability Ranks"]
---
The actual chunk content in markdown.
```

### Illustrative index role

The index holds **metadata + refs**; full text lives in chunk files. **Lookup:** filter the index → `chunk_id`s → read files.

---

## This skill’s gates on top

**Readiness** ([context readiness](../content/parts/phases/context-readiness.md)) applies when a package exists; it is a **stage** of judgment. **Canonical context** ([canonical-context](../content/parts/phases/canonical-context.md)) is where you **build** (or adopt and **freeze**) the contract—including after **PDF → MD** and first chunking.

---

## Rules location

- **Normative process:** [`content/parts/process.md`](../content/parts/process.md) and phase files under [`content/parts/phases/`](../content/parts/phases/).
- **Principles:** [`principles-and-rules.md`](principles-and-rules.md).
- **Execution order:** [`execution-and-success.md`](execution-and-success.md).
