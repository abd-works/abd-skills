# Canonical context — build and validate the package

**You will** produce a **single, versioned** context package with manifest provenance so later work cites well-structured, well-understood context from a modeling perspective.

**You will** turn **canonical Markdown** into a **validated** context package:

- **You must** ensure later work can cite `**chunk_id`** rows that exist on disk and in the index.
- **You must not** invent files or leave mystery sources

**Skill workspace:** **You will** treat the folder that contains `**solution.conf`** (selected by `**conf/abd-config.json` → `active_skill_workspace`**) as the root for every path in `**solution.conf`**—the same rules `**scripts/_config.py**` uses.

---

## Phase automation (emit)

All paths are under the **abd-maps-models-specs** skill package (the folder that contains `scripts/` and `conf/`).


| Script                                | Purpose                                                                                         |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `**python scripts/build_context.py`** | Emit `chunks/*.md` and `context_index.json`. Optional: `--dry-run`, `--config <solution.conf>`. |


Segmentation matches `**skills/abd-context-to-memory/scripts/chunk_markdown.py**`; implementation lives in `**scripts/context_chunk_from_memory.py**`. **Full schema** (front matter, index, manifest): [context-spec.md](../library/context-spec.md).

---

## Order of work

Work happens **in this order**: **code** (emit) → **AI** (coherence) → **code** (validate). Rationale: cut the corpus deterministically first, then judge whether cuts and labels match the manuscript, then check structure mechanically.

---

### 1. Emit the package (**code**)

**Actor:** Code (`build_context.py`).

**Inputs (read for you by `_config.py`):**

- `**conf/abd-config.json`** → workspace root.
- `**solution.conf`** → `manifest_sources[]`, `context_path`, `context_chunking_spec`.
- Each file listed in `**manifest_sources[]**` that ends in `**.md**`.
- `**context_chunking_spec**` — at minimum, `**defaults**` supply `**evidence_type**` and `**modeling_kind**` for new chunks until you change them in coherence.

**Outputs (under `<workspace>/<context_path>/`):**

- `**chunks/{chunk_id}.md`** — one file per chunk; YAML front matter + body per [context-spec.md](../library/context-spec.md).
- `**context_index.json`** — `spec_version`, `**manifest**` (sources + hashes + generator id), `**blocks[]**` aligned to those files.

**What the code does *not* do:** It does not decide whether a split is *wise* for your domain

---

### 2. Coherence pass (**AI or human**)

**Actor:** You (LLM session), **not** the emit script and **not** the contract scanner.

The **rule-bound** automated check (see [stage-1-context-decisions](../../rules/stage-1-context-decisions.md) and [scanners.json](../../rules/scanners.json)) verifies **shape** (files, ids, required fields). It does **not** read the whole handbook and ask “should this block be labeled `rule`?” — that is **your** job here.

**Inputs you use:**

- The **original** canonical Markdown at the paths in `**manifest_sources[]`** (ground truth).
- The emitted `**chunks/*.md`** and `**context_index.json**`.

**What you do:**

1. **Splits** — Walk the source and the chunks. Do boundaries follow the chunking **intent** (e.g. no half-table, no orphan heading, no merged topics that should be separate)? If not, adjust **chunk bodies** and/or **index** so they still obey [context-spec.md](../library/context-spec.md), or go back and fix `**context_chunking_spec`** / re-emit if the problem is structural.
2. **Labels** — Within **taxonomy** allowed by the chunking spec, set `**evidence_type`** and `**modeling_kind`** in front matter **and** matching `**blocks[]`** rows so they match **what the chunk text actually is** (form vs modeling stance — see context-spec). Fix `**preview`** text so it reflects the body, not a generic stub.
3. **Consistency** — Front matter, index row, and chunk body must **agree** (same `chunk_id`, same anchors, no contradictions).

**Rules:**

- Only edit fields the **schema allows**; do not invent free-form “evidence” without a `**chunk_id`**.
- **Do not** promote to terms, mechanisms, types, or `concepts[]` here — this phase **packages** evidence only.
- After you change chunks or the index, run **`python scripts/build.py`** (or the same pipeline your CI uses) so the **stage-1-context-decisions** check runs again.

---

### 3. Validate (**code**)

**Actor:** Automation for rule **stage-1-context-decisions** (scanner path in [scanners.json](../../rules/scanners.json)); executed from **`python scripts/build.py`** via **`operator.build_pipeline`**.

**Inputs:** Existing `**context_index.json`** and `**chunks/*.md`** (and workspace paths from config). If there is **no** index yet, the check exits success (greenfield).

**Outcome:** Exit **0** means the contract in [context-spec.md](../library/context-spec.md) is satisfied (e.g. every `blocks[]` row has a file, every chunk file is indexed or `**excluded`**, `chunk_id` in front matter matches filename, manifest/source checks as implemented). Exit **non-zero** means fix the artifacts and re-run **`build.py`**.

Treat this as a **hard gate** before later stages cite `**chunk_id`**.

---

## Other notes

- Rule ↔ scanner bindings: [scanners.json](../../rules/scanners.json) (`rule_scanner_bindings`).

---

## Related documents


| Topic                                  | Document                                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------------------ |
| Workspace + `solution.conf`            | [set-workspace.md](set-workspace.md)                                                       |
| Canonical `.md` + `manifest_sources[]` | [context-markdown.md](context-markdown.md)                                                 |
| Draft/review chunking YAML             | [context-chunking-approach.md](context-chunking-approach.md)                               |
| Schema and contract detail             | [context-spec.md](../library/context-spec.md)                                              |
| Pipeline overview                      | [process.md](../process.md), [principles.md](../library/principles.md) |


