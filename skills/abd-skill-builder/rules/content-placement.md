# Content placement (abd-skill-builder)

**Rule:** Normative, mergeable bodies for this skill live under **`content/parts/`**, not under **`docs/`**.

| Location | Purpose |
|----------|---------|
| **`content/parts/library/`** | **Stable, reusable meaning** — definitions, glossaries, artifact shapes, naming, invariants, standards text. **`scripts/build.py`** merges these into **`AGENTS.md`** in a fixed order. **Not** where you write phase-local procedures (see **Library vs phase documents** below). |
| **`content/parts/phases/`** | **Person-to-process** phase markdown — what to do *in this phase*: steps, checklists, script invocations, inputs/outputs, done criteria. One file per process-table phase. |
| **`content/parts/process.md`** | Process table + pipeline overview; links into **`library/`** and **`phases/`**. |
| **`rules/`** | Governance rules (this file, scanners binding) — **not** merged as full library bodies unless you explicitly add them to **`build.py`**. |
| **`docs/`** | **Non-runtime** only. In **abd-skill-builder**: **`standards-delta.md`** only. **Authoring checklist** working copies live under **`<skill>/docs/authoring-checklist.md`** in the skill or workspace you edit (scaffold copies from **`library/`**). Merge/delivery lookup: skill **`README.md`**. No duplicate stubs of **`library/`** bodies. |

**Do not** put instruction bodies that **`build.py`** must merge only under **`docs/`** — move them to **`library/`** or **`phases/`** and leave **`docs/`** as index or narrative.

## Library vs phase documents (mandatory split)

**`library/`** holds **what things are** — content that would stay true and worth repeating if several phases touch the same idea (domain constructs, document types, schemas, tables, voice/standards). It must **not** be a second home for **how the pipeline runs**.

| Put in **`library/`** | Do **not** put in **`library/`** (use **`phases/`**, **`process.md`**, or **`rules/`**) |
| --- | --- |
| Definitions, glossaries, stable templates, artifact contracts | Numbered **procedures** (“Step 1… Step 2…”) for doing a phase |
| Structure of a concept used in **multiple** phases | **Order of operations** for the skill (that is **`process.md`** + phase order in **`build.py`**) |
| Normative **rules** as *reference* copy when also mirrored in **`rules/`** | **Phase-specific** narrative (“in this phase you…”) beyond a short pointer |
| Optional **`<!-- abd:begin/end -->`** slices for injection | **Shell / CLI runbooks** (`python scripts/…`, exact commands) for a phase |
| | **Which phase comes when** or other **phase-detail** that belongs in **`process.md`** or **`phases/<slug>.md`** |

**`phases/<slug>.md`** holds **what you do** in that phase: purpose, inputs/outputs, **steps**, **scripts to run**, checklists, and **links** into **`library/`** for definitions. Phase files must **not** replace **`library/`** with long, reusable spec text—if two phases need the same deep definition, **one library doc** + **short links** from each phase.

**`rules/`** remains the home for **must-hold** constraints (often machine-checked). Do not bury enforceable “must” lists only inside **`library/`** if they belong in **`rules/`** as well.

See **[`documentation-standards.md`](../parts/library/documentation-standards.md)** and **[`skill-standards-section-3.md`](../parts/library/skill-standards-section-3.md)** (library vs phase split).
