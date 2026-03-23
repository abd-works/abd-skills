# Context chunking approach (Phase 0)

**Normative procedure for Phase 0:** **this document**. It covers **(1)** getting **canonical Markdown** for every evidence source, **(2)** workspace wiring, and **(3)** how **`context_chunking_spec`** is produced so splits and labels match real structure. You cannot honestly inventory headings, tables, lists, or export noise until the manuscript exists as Markdown the pipeline can read.

**Phase 1 procedure** (produce **`chunks/`** + **`context_index.json`**, coherence, contract validation) is **[canonical-context.md](canonical-context.md)**—a separate process file. **Artifact shapes and validation rules** are **[context-spec.md](../library/context-spec.md)**.

**You will** read every **`manifest_sources`** file **after** §1 conversion, perform the structural inventory in **§3**, **draft** the YAML (**`section_boundaries`**, **`splitting`**, **`defaults`**, **`taxonomy`**, …) per [context-spec.md](../library/context-spec.md) § Chunking spec, and **disclose** what **you** did—assumptions, uncertainties, and anything **you** could not infer from structure alone.

**You will not skip this:** After **your** draft, you will present results to the user to spot‑check against the real Markdown, correct wrong patterns, tighten taxonomy, and **accept** the spec before Phase 1 runs.

**If the spec already fits the sources,** **you will** **not** re-run a full inventory—only revisit when layout or **`manifest_sources`** change materially.

[`process.md`](../process.md) is the pipeline **summary** (table row), not the full procedure.

---

## 1. Convert to canonical Markdown (step one)

**Role:** Human + tooling (and optionally an AI-assisted pass for cleanup). **Phase 0 owns this:** any importers, converters, or one-off scripts (for example PDF, DOCX, PPTX → Markdown) live in **your** workspace or toolchain—not as an unnamed prerequisite of Phase 1.

**You will:**

1. Produce **canonical Markdown** for each source that is not already Markdown (fix encoding, strip or tag conversion artifacts you already know about, and land paths you can list in **`manifest_sources`**).
2. Keep conversion **repeatable** where it matters: document the command, script, or skill (e.g. a content-to-memory / document-ingest pipeline) so a refresh of the source file does not silently change chunk boundaries.
3. Only after those **`.md`** files exist and are stable enough to open, run the **structural inventory** in **§3** and draft **`context_chunking_spec`** (landed per **§4**).

Phase 1 emitters assume **`manifest_sources[]`** points at **Markdown** on disk. They do **not** substitute for Phase 0 conversion.

---

## 2. Configure the workspace and which files you cover

**Configure (human):** Land **`solution.conf`** in the active skill workspace: **`manifest_sources`**, **`context_path`** / output conventions, and the **`context_chunking_spec`** pointer (default `context_chunking_spec.yaml` beside `solution.conf`). The chunking YAML **contents** follow **§3–§4** and are reviewed before Phase 1. Phase 1 emitters **read** this same wiring via **`scripts/_config.py`**—[canonical-context.md](canonical-context.md) assumes it already exists.

**You will** cover **every** file that matters for evidence.

**You will** use **`solution.conf` → `manifest_sources[]`** in the **active skill workspace** (the folder that contains `solution.conf`; the skill selects it via `conf/abd-config.json` → `active_skill_workspace`).

- Each entry has a **`path`** (Markdown file, **relative to the workspace root**) and a **`role`** (source anchor for provenance).
- **You will** ingest **full contents** of those paths—**your** rules **must** speak to **this** export, not a generic handbook. **Human (solution analyst)** **will** confirm nothing important was skipped or misread.

The list of **`path`** values is the corpus **your** **`context_chunking_spec`** **must** cover. When the workspace **runs** Phase 1, path resolution for **`solution.conf`**, chunking YAML, **`context_path`**, and outputs follows **`scripts/_config.py`** (same **skill workspace** as above).

---

## 3. Structural scan (inventory you will encode)

**You will** model the manuscript’s real shape before YAML is finalized. **You are going to** deliver **(a)** a short **structural report** (what **you** observed, risks, open questions) and **(b)** the **draft `context_chunking_spec`**. This is not a pass/fail score. If **your** inventory is shallow, Phase 1 code will split mid-table or treat boilerplate as rules—and Phase 1 coherence **still needs the source** to catch drift; neither pass can fix a wrong **split policy** without updating the spec or the emitter.

### 3.1 Outline and navigation

**You will** examine and record:

- **Heading ladder** — Which `#` … `######` levels mean part, chapter, section, subsection? Are levels consistent?
- **Numbering** — Do `1.`, `1.2.3`, or appendix letters align with headings, or do lists float without a heading boundary?
- **Navigation chrome** — ToCs, “in this section,” breadcrumbs: **content** to chunk, or **noise** to exclude or tag per [context-spec.md](../library/context-spec.md)?

### 3.2 Dense and atomic regions

**You will** apply these constraints when **you** encode rules:

- **Tables** — Never split **through** a row; split above/below the table block.
- **Lists and definition lists** — A rule plus its bullets is often **one** unit.
- **Stat blocks, callouts, boxed examples** — Note delimiters. Repeated shapes → **pattern rules** in YAML, not one-off IDs.
- **Code fences** — Often stay with the prose that introduces them.

### 3.3 Noise vs signal

**You will** classify:

- **Export junk** — Running headers, page numbers, license blobs, conversion artifacts.
- **Policy** — Exclude (and use **`excluded[]`** where the contract allows), or **include and tag** (`metadata_noise`, `noise`, `structural_only`). Field meanings: [context-spec.md](../library/context-spec.md).

### 3.4 Repeated templates

**You will** encode the **pattern** in **`section_boundaries`** / splitting rules and set **`defaults`** + **`taxonomy`** for that pattern.

### 3.5 Capture sheet (you fill; human verifies)

| You will determine… | So the spec can encode… |
| ------------------- | ----------------------- |
| What **starts** a new major unit? | `chapter_break_regex` / `section_break_regex` ([context-spec.md](../library/context-spec.md) § Chunking spec). |
| What must **never** be split inside? | **`splitting`** (e.g. keep tables intact). |
| When tiny bits **merge**? | **`min_chunk_chars`**, merge rules. |
| What is **out of scope** for modeling? | **`modeling_kind`** defaults, exclusions. |
| Which **taxonomy** values apply? | Closed-world enums aligned with [context-spec.md](../library/context-spec.md). |

---

## 4. Produce and land `context_chunking_spec`

1. **You will** write the YAML at **`solution.conf` → `context_chunking_spec`** (default basename `context_chunking_spec.yaml` beside `solution.conf`). **Fields and examples:** [context-spec.md](../library/context-spec.md) § Chunking spec. **Minimum areas:** **`section_boundaries`**, **`splitting`**, **`defaults`**, **`taxonomy`**.

2. **You will** disclose in the same turn or an accompanying note: **sources read**, **assumptions**, **low-confidence rules**, and **gaps** (e.g. “could not infer appendix boundary pattern”). **Human (solution analyst)** **will** use this during review.

3. **Human (solution analyst):** **You will** run a secondary pass on the manuscript vs draft YAML: fix wrong headings/tables/noise calls, tighten taxonomy, and ensure the spec is **valid** per [context-spec.md](../library/context-spec.md). The landed file is **owned** by the workspace; the AI draft is not sufficient without this review.

---

## 5. If `chunks/` and an index already exist

**You will** feed learning back into the spec when asked—often **you** run another full Phase 0 pass (structural report + draft YAML) and **Human (solution analyst)** **will** review again: coverage, misfiring defaults, new section shapes. That is **spec maintenance** for Phase 0—not Phase 1’s validator.

---

## See also

- **[canonical-context.md](canonical-context.md)** — Phase 1: emit package, coherence, validate.
- **[context-spec.md](../library/context-spec.md)** — Normative chunk/index/manifest shapes and checklist.
