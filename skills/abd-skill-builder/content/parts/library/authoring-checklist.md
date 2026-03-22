# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Copy this file into the skill you are working on** and check items off as you go — if you stop, the next session continues from the **first unchecked** box.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, plans, architecture, optional authoring-checklist copies, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**; copy this checklist to **`<your-skill>/docs/authoring-checklist.md`** when you track work.)

---

## Before you start (every session)

- [ ] **Working copy:** Copy **`content/parts/library/authoring-checklist.md`** (from **abd-skill-builder**) to **`docs/authoring-checklist.md`** inside **the skill you are building** (under **`active_skill_workspace`** / your project). **abd-skill-builder** does not maintain its own **`docs/authoring-checklist.md`**.
- [ ] **Resume:** Find the **first unchecked** `- [ ]` below and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, architecture, migration notes, **authoring-checklist** only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[migrate.md](content/parts/phases/migrate.md)** (inventory + delta report + user chose fixes) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent.
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`content/parts/process.md`** lists the real pipeline (ordered phases).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **`rules/scanners.json`** + **`skill-config.json`** `operator.scanners` aligned if scanners exist.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Copy** into **your skill** (or workspace) as **`docs/authoring-checklist.md`** before deep work — from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.
