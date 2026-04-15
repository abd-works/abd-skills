# Context chunking approach


**You will** read every file listed in **`manifest_sources`**, perform structural inventory, **draft** the YAML per [context-spec.md](../library/context-spec.md) chunking spec, and **disclose** what **you** did—assumptions, uncertainties, and anything **you** could not infer from structure alone.

**You will not skip this:** After **your** draft, you will present results to the user to spot‑check against the real Markdown, correct wrong patterns, tighten taxonomy, and **accept** the spec before **canonical context** runs.

**If the spec already fits the sources,** **you will** **not** re-run a full inventory—only revisit when layout or **`manifest_sources`** change materially.

---

## 1. Structural scan (inventory you will encode)

**You will** model the manuscript’s real shape before YAML is finalized. **You are going to** deliver **(a)** a short **structural report** (what **you** observed, risks, open questions) and **(b)** the **draft `context_chunking_spec`**. This is not a pass/fail score. If **your** inventory is shallow, canonical-context tooling will split mid-table or treat boilerplate as rules—and coherence **still needs the source** to catch drift; neither pass can fix a wrong **split policy** without updating the spec or the emitter.

### 1.1 Outline and navigation

**You will** examine and record:

- **Heading ladder** — Which `#` … `######` levels mean part, chapter, section, subsection? Are levels consistent?
- **Numbering** — Do `1.`, `1.2.3`, or appendix letters align with headings, or do lists float without a heading boundary?
- **Navigation chrome** — ToCs, “in this section,” breadcrumbs: **content** to chunk, or **noise** to exclude or tag per [context-spec.md](../library/context-spec.md)?

### 1.2 Dense and atomic regions

**You will** apply these constraints when **you** encode rules:

- **Tables** — Never split **through** a row; split above/below the table block.
- **Lists and definition lists** — A rule plus its bullets is often **one** unit.
- **Stat blocks, callouts, boxed examples** — Note delimiters. Repeated shapes → **pattern rules** in YAML, not one-off IDs.
- **Code fences** — Often stay with the prose that introduces them.

### 1.3 Noise vs signal

**You will** classify:

- **Export junk** — Running headers, page numbers, license blobs, conversion artifacts.
- **Policy** — Exclude (and use `**excluded[]`** where the contract allows), or **include and tag** (`metadata_noise`, `noise`, `structural_only`). Field meanings: [context-spec.md](../library/context-spec.md).

### 1.4 Repeated templates

**You will** encode the **pattern** in `**section_boundaries`** / splitting rules and set `**defaults**` + `**taxonomy**` for that pattern.

### 1.5 Capture sheet (you fill; human verifies)


| You will determine…                    | So the spec can encode…                                                                                        |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| What **starts** a new major unit?      | `chapter_break_regex` / `section_break_regex` ([context-spec.md](../library/context-spec.md) § Chunking spec). |
| What must **never** be split inside?   | `**splitting`** (e.g. keep tables intact).                                                                     |
| When tiny bits **merge**?              | `**min_chunk_chars`**, merge rules.                                                                            |
| What is **out of scope** for modeling? | `**modeling_kind`** defaults, exclusions.                                                                      |
| Which **taxonomy** values apply?       | Closed-world enums aligned with [context-spec.md](../library/context-spec.md).                                 |


---

## 2. Produce and land `context_chunking_spec`

1. **You will** write the YAML at `**solution.conf` → `context_chunking_spec`** (default basename `context_chunking_spec.yaml` beside `solution.conf`). **Fields and examples:** [context-spec.md](../library/context-spec.md) § Chunking spec. **Minimum areas:** `**section_boundaries`**, `**splitting`**, `**defaults**`, `**taxonomy**`.
2. **You will** disclose in the same turn or an accompanying note: **sources read**, **assumptions**, **low-confidence rules**, and **gaps** (e.g. “could not infer appendix boundary pattern”). **Human (solution analyst)** **will** use this during review.
3. **Human (solution analyst):** **You will** run a secondary pass on the manuscript vs draft YAML: fix wrong headings/tables/noise calls, tighten taxonomy, and ensure the spec is **valid** per [context-spec.md](../library/context-spec.md). The landed file is **owned** by the workspace; the AI draft is not sufficient without this review.

The list of **`manifest_sources`** **`path`** values is the corpus this spec **must** cover. Path resolution for **`solution.conf`**, chunking YAML, **`context_path`**, and outputs follows **`scripts/_config.py`** (same skill workspace as [set-workspace.md](set-workspace.md)).

---

## 3. If chunk `*.md` files under **context_path** and an index already exist

**You will** feed learning back into the spec when asked—often **you** run another full chunking pass (structural report + draft YAML) and **Human (solution analyst)** **will** review again: coverage, misfiring defaults, new section shapes. That is **spec maintenance** for this phase—not canonical context’s contract validator.

---

## See also

- **[set-workspace.md](set-workspace.md)** — Workspace root and **`solution.conf`** wiring.
- **[context-markdown.md](context-markdown.md)** — **`manifest_sources`** and canonical **`.md`**.
- **[canonical-context.md](canonical-context.md)** — Context package (chunks, index, validate).
- **[context-spec.md](../library/context-spec.md)** — Normative chunk/index/manifest shapes and checklist.
