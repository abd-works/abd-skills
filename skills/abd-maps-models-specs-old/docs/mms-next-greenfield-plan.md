# Maps, Models & Specs — next generation (greenfield plan)

This document is the **line-in-the-sand checkpoint** companion: **abd-maps-models-specs** has reached the limit of incremental repair for the current pipeline design (see `pipeline-deep-dive.md`). The **next** skill is a **clean implementation** of the target approach, **reusing** corpus, tests, and lessons—not scripts as-is unless they still match the new gates.

**Naming (suggested):**

| Artifact | Suggested name |
|----------|----------------|
| Frozen snapshot of current skill | `abd-maps-models-specs` @ commit tagged **`mms-v1-checkpoint`** (or branch `archive/mms-v1`) |
| New skill (blank scaffold + corpus) | `abd-maps-models-specs-next` (or `abd-maps-models-specs-v2`) until promoted |

---

## 1. What to carry forward unchanged (initially)

### 1.1 MM3 markdown corpus

- **`test/mm3/context/chunks/*.md`** — **Keep as the v1 evidence corpus** for the fixture. IDs (`unit_*`) stay stable so traces and future golden diffs stay comparable.
- **Optional:** a single **Heroes’ Handbook** (or source) `.md` if you maintain a monolithic export elsewhere; chunks remain the **unit of citation** for the pipeline.

### 1.2 When to re-chunk

**Start without re-chunking.** The deep dive’s issue was **pipeline behavior** (noun explosion, regex inheritance, alignment rules), not necessarily bad chunk files.

**Re-chunk later** if, after the **new Stage 1** is defined, you need:

- **Semantic boundaries** — one chunk = one *modeling_kind* focus (definition vs example vs table vs rule block).
- **Smaller N** — fewer, larger chunks for breadth sampling; or **larger N** — finer splits for precise citation.
- **Stable `modeling_kind` / `evidence_type` per chunk** — if tags are wrong often, fix chunk boundaries or merge/split rules.

Until then, **treat existing chunks as given inputs** and put new intelligence in **metadata layers** (terms, mechanisms, candidates) and **gates**, not in re-cutting the corpus on day one.

### 1.3 From the old skill (reference, not blind copy)

Copy **ideas and selective artifacts**, not the whole tree:

| Lift | Purpose |
|------|---------|
| `docs/pipeline-deep-dive.md` | Failure modes and target behavior |
| `test/mm3/maps-models-specs/object-model-critique.md` | Fixture-specific critique pattern |
| Scanner **concepts** (rules) | Rewrite implementations to match new JSON shapes |
| `skill-config.json` patterns | Endpoints, paths—only if unchanged |

Do **not** copy wholesale: `classify_chunks.py` **regex inheritance**, monolithic `build.py` **without** replacing the merge model with **candidate queue + integrate**.

---

## 2. End-to-end pipeline (overview)

**North star:** *document-grounded, behaviorally coherent OO* — not *maximal `concepts[]` rows per chunk mention*.

| Phase | Name (working) | Purpose |
|-------|----------------|---------|
| 0 | **Source → Markdown** | Canonical human/LLM-readable corpus; versioned. |
| 1 | **Ingest & index chunks** | Chunks + **rich metadata**; **no** automatic class minting. |
| 2 | **Terms & mechanisms** | Glossary (A), named processes (B); **candidates** for types, not `concepts[]` yet. |
| 3 | **Story map** | **Behavioral** stories: actor → behavior → concept → state change; optional supporting interaction. |
| 4 | **Domain types (`concepts[]`)** | **Sparse** types; promotion from candidates with **reject gate**. |
| 5 | **Variant classification** | Per family: **enum vs `extends`**; **no** spine-time trees. |
| 6 | **Deepen** | Responsibilities, collaborations, chunk evidence on **approved** types. |
| 7 | **Integrate** | Merge synonyms, repoint `extends`, enum decisions; **merge candidates → concepts** here or in 4/5. |
| 8 | **Validate & render** | Scanners, reports, human/“critic” review. |

Below, **Stage 1** is detailed; **2–8** are specified enough to sequence work without locking every prompt.

---

## 3. Stage 0 — Source → Markdown

**Goal:** One **canonical** markdown representation of the source (handbook, PDF export, etc.), suitable for chunking.

**Steps:**

1. **Establish source of truth** — e.g. `HeroesHandbook.md` or chapter files; **pin** version (commit hash, date).
2. **Conversion** — PDF/DOCX → Markdown using your existing **abd-context-to-memory** / Pandoc / whatever you already trust; **preserve** headings and tables.
3. **Lint** — broken links, empty sections; **optional** front-matter (`source_edition`, `license`).
4. **Freeze** — file(s) under `context/source/` or equivalent in the **new** skill; **do not** hand-edit without bumping version.

**Outputs:** Versioned `.md` source; **changelog** line when the handbook updates.

**Exit criteria:** Markdown is **complete enough** to chunk; no requirement yet for perfect semantics.

---

## 4. Stage 1 — Ingest & index chunks (detailed)

**Goal:** Chunks are **units of evidence** with **explicit non-class labels**, so later steps cannot treat “mentioned here” as “define a class here” by default.

### 4.1 Chunk production

1. **Split strategy** — either:
   - **Reuse v1 chunk files** (`unit_*.md`) as-is for MM3 fixture, **or**
   - Run a **chunk script** from Stage 0 markdown with **documented rules** (max tokens, heading boundaries, table = one chunk, etc.).
2. **Stable IDs** — `chunk_id` immutable once published; merges produce `unit_X_merged` with **provenance** pointing to merged-from IDs.
3. **Store path** — e.g. `test/mm3/context/chunks/{chunk_id}.md` (new skill) mirroring old layout for tooling continuity.

### 4.2 Per-chunk metadata (required fields)

| Field | Purpose |
|-------|---------|
| `chunk_id` | Stable key |
| `source_path` / `source_anchor` | Trace back to Stage 0 file + heading or line range |
| `modeling_kind` | **definition** \| **rule** \| **table** \| **example** \| **narrative_aside** \| **structural_layout** \| **other** |
| `evidence_type` | Align with old skill where useful: `domain-rule`, `example`, etc. |
| `modeling_priority` | **high** \| **medium** \| **low** for stratified sampling |
| `candidate_terms` | String list — **glossary** candidates, **not** classes |
| `raw_text_hash` | Optional — detect silent edits |

**Rule:** **`example`** and **`narrative_aside`** chunks **cannot** introduce **`extends`** or new `concepts[]` rows** without** an explicit **promotion** step (human or checklist).

### 4.3 Chunk index artifact

- **Single JSON** (or SQLite later): `chunk-index.json` listing all chunks + metadata.
- **Reverse index** (like old `mms-chunk-index.json`) is **generated** from spec **later**, not hand-maintained in Stage 1.

### 4.4 Explicitly **not** in Stage 1

- No **`inherits`** edges from **regex** co-occurrence.
- No **merge** of chunk terms into **`concepts[]`**.
- No **story map** yet.

### 4.5 Exit criteria (Stage 1)

- [ ] Every chunk file has **metadata** record with `modeling_kind` and `evidence_type`.
- [ ] **Stratified sample** possible: top **K** by `modeling_priority` per module area (module tagging can be **light** in 1 or deferred to 2).
- [ ] Documented **re-chunk** triggers (see §1.2) for future you.

### 4.6 First implementation slice (suggested)

1. Copy **only** `test/mm3/context/chunks/` + minimal `chunk-index.json` **schema** + one **validation script** (`python` checks every file on disk matches index).
2. Backfill **`modeling_kind`** with a **single** LLM or human pass **per chunk** (batch), **or** heuristic + spot-check—full automation can wait.

---

## 5. Stage 2 — Terms & mechanisms layer

**Goal:** Separate **terms** and **named processes** from **domain types**.

**Activities:**

1. **Glossary (layer A)** — term, definition, optional `chunk_id`s; **no** `extends`.
2. **Mechanisms (layer B)** — named workflows (“resolution pipeline”, “turn sequence”): **steps**, links to chunks; **still not** automatic classes.
3. **Candidate type queue** — “might be a class” with **reason** + **chunk evidence**; **not** in `concepts[]` until promotion.

**Outputs:** `terms.json`, `mechanisms.json`, `candidates.json` (names illustrative).

**Exit criteria:** Clear **promotion rule**: candidate → `concepts[]` only after Stage 4 gate.

**Level:** Implement after Stage 1 is stable; can start **manual** (spreadsheet → JSON) for MM3.

---

## 6. Stage 3 — Story map (behavioral)

**Goal:** Epics/stories that satisfy the **confirming story** definition (see `pipeline-deep-dive.md`): **primary actor** → **behavior** → **concept** → **state change**; optional supporting actor/concept.

**Activities:**

1. **Verb–noun discipline** — story titles and AC reference **operations on concepts**, not bare policy phrases.
2. **Alignment** — stories may reference **term IDs** or **concept IDs**; **forbid** pure **string** forcing every story noun into `concepts[].name`.
3. **Validation script** — **optional** first version: checklist LLM or human until automated.

**Outputs:** `story-map.json` (or embedded section) **linked** to `chunk_id`s for **acceptance** evidence, not for **type** creation.

**Exit criteria:** No epic exists **only** to satisfy name-alignment scanners from v1.

---

## 7. Stage 4 — Domain types (`concepts[]`) — sparse

**Goal:** **`concepts[]`** rows only for **stateful** abstractions that pass **“not reducible to a property on a broader type”** (see deep dive §9).

**Activities:**

1. **Promotion** from `candidates.json` with **reject** reasons logged.
2. **No** auto-row from **chunk primary_concepts** without gate.
3. **Module** assignment + **`depends_on`** for ordering deepen.

**Exit criteria:** Concept count **bounded** on MM3 vs v1 explosion; critique doc tracks **why** each concept exists.

---

## 8. Stage 5 — Variant classification

**Goal:** Per **family**, decide **enum vs `extends`** **before** bulk property churn.

**Activities:**

1. **Gate** between scaffold breadth and **full** classification (per deep dive §10 item 3).
2. **Decision log** — family name, chosen representation, chunk evidence.

**Exit criteria:** No **unexamined** `extends` from “looks like a subtype” prose.

---

## 9. Stage 6 — Deepen

**Goal:** Responsibilities, collaborations, **chunk references** — **only** for **approved** concepts.

**Activities:**

1. Replace v1 **“harvest every noun”** with **“map terms to mechanisms; map approved types to evidence.”**
2. Topological **`depends_on`** for module order preserved.

**Exit criteria:** `chunks_must_be_referenced` means **evidence**, not **permission to mint**.

---

## 10. Stage 7 — Integrate

**Goal:** Synonym merge, `extends` repointing, **candidate drain** — **final** `map-model-spec.json` shape.

**Activities:**

1. **Merge** candidates into concepts **here** if not in 4.
2. **Human or batch** review of **large** `extends` graphs.

**Exit criteria:** Single **canonical** JSON for downstream render.

---

## 11. Stage 8 — Validate & render

**Goal:** Scanners + **reports** + optional **critic** pass.

**Activities:**

1. **Port scanner ideas** from v1; **rewrite** against new schema.
2. **`map-model-spec.md`** / inheritance report **generated**, not hand-edited.
3. **Critic checklist** (OO + pipeline-deep-dive failures) run by **second** agent or human.

**Exit criteria:** CI runs **pytest** + scanners on MM3 fixture; diff **golden** outputs on intentional changes only.

---

## 12. Testing & orchestration

### 12.1 Automated

- **Fixture:** `test/mm3/` corpus + **golden** outputs (or **assertions** on counts: max concepts, no regex `inherits`).
- **Per-stage artifacts** — each stage writes **one** primary artifact; tests **pin** stage N before N+1.

### 12.2 Human + critic agent

- **You** approve stage transitions.
- **Builder** agent (or you) produces artifact N.
- **Critic** agent uses **fixed checklist** from `pipeline-deep-dive.md` + **behavioral story** rules—**not** a substitute for pytest.

### 12.3 Orchestrator (later)

- Chat **orchestrator** invokes **build** subtask then **critique** subtask; **logs** decisions. **Start manual** until repetitive.

---

## 13. Repo steps (checklist for you)

1. **Commit** current `abd-maps-models-specs` with message like:  
   `mms-v1: checkpoint before greenfield rewrite (pipeline limit reached)`
2. **Tag** `mms-v1-checkpoint` (or branch `archive/mms-v1`).
3. **Create** new skill folder: `skills/abd-maps-models-specs-next/`.
4. **Seed** it with:
   - `test/mm3/context/chunks/**/*.md` (copy)
   - Optional: `test/mm3/maps-models-specs/*.md` **critique reports** as **reference baselines** only—not as targets to reproduce v1 bugs
   - `docs/pipeline-deep-dive.md` (copy)
   - **This file** (`mms-next-greenfield-plan.md`)
   - Minimal `README.md` pointing to v1 tag
5. **SKILL.md** — stub: “under construction; see greenfield plan.”
6. **Implement** Stage 1 slice (§4.6) first PR in the new skill.

---

## 14. Success metrics (v2 vs v1 on MM3)

| Metric | Direction |
|--------|-----------|
| `concepts[]` count at same “depth” | **Lower** or **same** with **documented** additions only |
| Spurious `extends` edges | **Zero** from code regex |
| Confirming stories | **Behavioral** (actor / operation / concept / state) |
| Time to **explain** the model | **Shorter** — fewer types, clearer mechanisms |

---

*This plan is the **map**; the **first footpath** is Stage 0–1 with MM3 chunks preserved and metadata gates added before any new `concepts[]` automation.*
