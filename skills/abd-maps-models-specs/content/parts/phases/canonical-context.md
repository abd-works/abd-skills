# Canonical context (Phase 1) — build and validate the package

**Goal:** A **single, versioned** context package—`**chunks/*.md`**, `**context_index.json`**, manifest provenance—so later phases cite stable `**chunk_id**` values. This is **not** vocabulary, story maps, or domain types.

**Prerequisite:** [Phase 0 — Context chunking approach](context-chunking-approach.md) yields a `**context_chunking_spec`** aligned with current `**manifest_sources`**. **Normative procedure for Phase 1:** **this document**. **Artifact shapes and checklist:** [context-spec.md](../library/context-spec.md). `[process.md](../process.md)` is pipeline **summary** only.

---

## 1. What Phase 1 is for

You turn **canonical Markdown** (declared sources) into a **validated** context package:

- Later work can cite `**chunk_id`** rows that exist on disk and in the index.
- **No** invented files, **no** mystery sources—paths and hashes live in `**solution.conf`** and the index `**manifest`**.

**Skill workspace:** The folder that contains `**solution.conf`**, selected by `**conf/abd-config.json` → `active_skill_workspace`** (paths inside `**solution.conf**` are relative to that folder—same rules as `**scripts/_config.py**`).

Downstream **consumes** this package; it does not replace it.

---

## 2. Pipeline shape and context build

**Producing** the package: canonical Markdown (from `**solution.conf` → `manifest_sources[]`**, resolved by `**scripts/_config.py`**) → chunking per `**context_chunking_spec**` → `**chunks/**` + `**context_index.json**` → **coherence** → **contract** validation. Example paths like `docs/HeroesHandbook.md` are **fixtures**; **your** workspace lists **your** files.

**Why code then AI/human (two stages):** The intent—**deterministic cut first**, then **sense-check against the original Markdown**—is spelled out in [context-chunking-approach.md](context-chunking-approach.md). **This section** is **procedure** only.

**Prerequisite (Phase 0):** Canonical Markdown for every source (**[context-chunking-approach.md](context-chunking-approach.md) §1**), **`solution.conf`** (workspace wiring: **`manifest_sources`**, paths), and the reviewed **`context_chunking_spec`** (chunking YAML) are **Phase 0** deliverables. Phase 1 **consumes** them; it does **not** run PDF/DOCX conversion or replace that work. The table below starts after Phase 0—**emit**, **coherence**, **validate** only.


| Step          | Role            | What happens                                                                                                                                                                 |
| ------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Build**     | Code            | Read `**manifest_sources`** + `**context_chunking_spec`** → write `**chunks/*.md**` + `**context_index.json**` (how you run that step is up to your workspace; see **§2.1**) |
| **Coherence** | LLM or human    | Align schema-allowed fields with chunk text and index (**§2.1**)                                                                                                             |
| **Validate**  | Code            | Contract scanner (**§7.4**) enforces [context-spec.md](../library/context-spec.md)                                                                                           |


Substantive vs noise, default labels, and **taxonomy** are declared in `**context_chunking_spec`** during [Phase 0](context-chunking-approach.md). Phase 1 **applies** that YAML; it does not invent structure you never scanned for.

### 2.1 Automation: emit package, coherence, validate

**Contract** (what “valid” means): `**context_index_contract.py`** / `**validate_context_contract.py`** per [context-spec.md](../library/context-spec.md). That is **not** Pass 1—it runs **after** `**chunks/`** and `**context_index.json`** exist.

**Emit (Pass 1):** Deterministic code reads `**manifest_sources`** + `**context_chunking_spec`** and writes `**chunks/*.md**` + `**context_index.json**`. This skill’s repo **does not ship** that emitter yet; you may use your own script, a one-off, or external tooling—as long as outputs match [context-spec.md](../library/context-spec.md). A dedicated module under `**scripts/`** may appear later; there is **no** fixed filename today.

**Typical emit flow** (one script or several—your choice):

1. Load Markdown from `**manifest_sources[]`** (`path` + `role`); use `**source_path`** when the workspace names a docs directory for discovery. Load chunking rules from `**context_chunking_spec**` (default `context_chunking_spec.yaml`).
2. Write chunk files and `**context_index.json**` per [context-spec.md](../library/context-spec.md)—deterministic **code-first** generation.

**Coherence (Pass 2):** LLM or human uses `**manifest_sources`** Markdown as **ground truth**—check that **splits and labels** fit the manuscript; then, within **schema-allowed fields only**, align front matter, index rows (`evidence_type`, `modeling_kind`, `preview`, …), and chunk bodies so they **do not contradict** each other or the source. Re-run `**validate_context_contract.py`** after edits. No free-text “evidence” without `**chunk_id**`.

`**scripts/build.py**` (full workspace run, not `--merge-only`): runs `**validate_context_contract.py**` / `**context_index_contract.py**` when an index exists. It does **not** emit chunks—emit is **outside** this script until an emitter is added here.

**Generation (code-first, then coherence)**

- **Pass 1 — deterministic Python** applies **only** rules from the chunking spec, assigns `**chunk_id`** deterministically, writes chunks + index.
- **Pass 2 — coherence:** LLM or **human** checks those artifacts **against the original Markdown** (strategy sense-check), then refines **allowed** fields so labels and previews **match** chunk text and the **source**. **Promotion** to terms/types is **not** Phase 1. Final output **must** pass `**validate_context_contract.py**` / `**context_index_contract.py**`.

### 2.2 Which script does what (and run order)

**Python** checks **shape** or prints **stats**; it does not re-read the **whole source** for “does this chunking strategy make sense?” **Coherence** (**§2.1**) does that (LLM or human), using **original Markdown** plus chunk/index output.


| Kind                                                                 | What it is                                                                                                                    | What it does **not** do                                          |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `**context_index_contract.py`** / `**validate_context_contract.py`** | Contract validation per [context-spec.md](../library/context-spec.md)                                                         | Not an LLM; not coherence; not “strategy vs source” review       |
| **Coherence (**§2.1**)**                                             | Second pass: LLM or human uses **source Markdown** + artifacts to validate chunking **sense**, then aligns **allowed** fields | Not the contract scanner; does not replace fixing a bad **spec** |


**Run order** (workspace `**scripts/build.py`**, not `--merge-only`): `**validate_context_contract.py**` / `**context_index_contract.py**` when `**context_index.json**` exists (after your Phase 1 emitter runs). **Emit** Pass 1 is **separate**—run your emitter **before** the contract scanner can pass.

`**python scripts/build.py --merge-only`** (this **skill repo** only) rebuilds composed docs (`AGENTS.md`, `content/built/`, embedded bundles). It does **not** run workspace audits or contract scanners—use when **editing skill markdown**, not when **building a context package**.

**Injectable paths:** `**rules/scanners.json`**.

---

## 3. What a healthy package provides

1. **Stable IDs** — `chunk_id` / `block_id` aligned with files and index.
2. **Evidence typing** — `evidence_type` and related fields usable for sampling and promotion gates—see **§5** and [context-spec.md](../library/context-spec.md).
3. **Coverage** — Domain-relevant material represented; exclusions **explicit** where allowed (`excluded[]`, …).
4. **Versioning** — Manifest pins sources and generator provenance.

---

## 4. Chunking spec (from Phase 0, used here)

`**context_chunking_spec`** is **produced** during [Phase 0](context-chunking-approach.md) (**Markdown conversion §1**, **configure §2**, **AI-led draft + human review §3–§4**). **Normative** fields: [context-spec.md](../library/context-spec.md) § Chunking spec. Phase 1 **points** `**solution.conf` → `context_chunking_spec`** at that file and **uses** it when emitting chunks and the index.

---

## 5. Evidence types, `modeling_kind`, and promotion

Chunk front matter and index rows carry `**evidence_type`** (form in the source) and `**modeling_kind`** (stance for modeling). Enums come from chunking spec `**taxonomy**`—[context-spec.md](../library/context-spec.md) § Chunking spec and § Chunk files.

**Promotion vs evidence:** Phase 1 **packages** evidence only. Turning a citation into a **term**, **mechanism**, **story**, **property**, or `**concepts[]` row** is **not** automatic. See [principles-and-rules.md](../library/principles-and-rules.md), [pipeline_invariants.md](../library/pipeline_invariants.md), and later-phase contracts. `**example`** / `**metadata/noise`** do not silently become types or edges here.

---

## 6. Illustrative chunk and index

```yaml
---
chunk_id: blk_00042
source: HeroesHandbook
evidence_type: domain-rule
section_path: ["Chapter 3", "Abilities", "Ability Ranks"]
---
The actual chunk content in markdown.
```

**Index:** metadata + refs; full text in chunk files. **Lookup:** index → `chunk_id`s → `chunks/{chunk_id}.md`. Full schema: [context-spec.md](../library/context-spec.md).

---

## 7. What you do (ordered work)

### 7.1 Wire the chunking spec

Ensure `**context_chunking_spec`** reflects current sources ([Phase 0](context-chunking-approach.md)). Set `**context_chunking_spec`** in `**solution.conf**`. Schema: [context-spec.md](../library/context-spec.md).

### 7.2 Produce `chunks/*.md` and `context_index.json`

- **Emit** per **§2.1**: any deterministic process you use is fine **if** outputs satisfy [context-spec.md](../library/context-spec.md).

Outputs: `<workspace>/<context_path>/chunks/*.md` and `context_index.json`.

### 7.3 Pin provenance

Index `**manifest`**: sha256 (and generator id where applicable) for `**manifest_sources`**, per [context-spec.md](../library/context-spec.md).

### 7.4 Validate

When `**context_index.json**` exists, run `**scripts/scanners/context_index_contract.py**` (same as `**validate_context_contract.py**`) — **hard gate**: bidirectional chunk ↔ index, required front matter, duplicate IDs, line bounds. Fix all violations before handoff.

### 7.5 Do **not**

- Do **not** add `**concepts[]`**, story-map JSON, or terms/mechanisms here.
- Do **not** introduce `**extends` / inheritance** edges as a shortcut.
- You **only** package evidence cited by `**chunk_id`**.

---

## 8. How you know Phase 1 is complete

Before Stages 2–4 cite `**chunk_id`**:

1. `**context_index.json**` exists and `**validate_context_contract.py**` / `**context_index_contract.py**` exits **0** ([context-spec.md](../library/context-spec.md)).
2. **Chunk files** match the index—no orphans, no missing files.
3. **Manifest** pins sources and provenance (**sha256**, etc.).
4. **Chunking spec** and **manifest** match the **same** source snapshot you split.

---

## 9. Artifacts (summary)


| Artifact                   | Role                                                                               |
| -------------------------- | ---------------------------------------------------------------------------------- |
| Chunking YAML              | `**solution.conf` → `context_chunking_spec`**                                      |
| `**chunks/{chunk_id}.md`** | One chunk per file; front matter per [context-spec.md](../library/context-spec.md) |
| `**context_index.json**`   | `**manifest**` + `**blocks[]**` (+ optional `**excluded[]**`)                      |
| Contract scanner           | [context-spec.md](../library/context-spec.md); paths in `**rules/scanners.json**`  |


---

## 10. Adoption and migration

Migrate or extend schema in place, fill `**modeling_kind**` where required, **pin** v1 in the manifest. Revisit [Phase 0](context-chunking-approach.md) if sources change.

---

## 11. Where to read more


| Topic                                          | Document                                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Phase 0** — AI-led spec draft + human review | [context-chunking-approach.md](context-chunking-approach.md)                               |
| **Schema / contract**                          | [context-spec.md](../library/context-spec.md)                                              |
| **Principles, gates, pipeline summary**        | [principles-and-rules.md](../library/principles-and-rules.md), [process.md](../process.md) |


