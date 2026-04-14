# Phase — Migrate existing skill (execute)

Use this when the skill **already exists** and you are **applying** the plan from **[`plan-migrate.md`](plan-migrate.md)** (**Stage 1b**): **move** files into the **correct layout**, **rename**, **rewire** **`build.py`** / **`skill-config.json`**, and **patch** only what the user **already selected** in the **delta**—**straight execution**, not a second full standards inventory.

**Not here:** writing the **initial** **[`docs/standards-delta.md`](../../docs/standards-delta.md)** table or comparing every row to §3—that is **`plan-migrate.md`**.

**Not here:** **scaffolding from zero** — use **[`scaffold.md`](scaffold.md)** (**Stage 2** in **`process.md`**).

---

## Prerequisites

- **[`plan-migrate.md`](plan-migrate.md)** completed: a **delta** artifact (e.g. **`docs/standards-delta.md`**) with **IDs**, and the user’s **choice** of which **IDs** to fix in this pass.

---

## Outcome

1. **Tree** changes that implement **only** agreed **IDs** (moves, new files, config updates).
2. **Delta** rows updated: **fixed**, **deferred**, or **accepted risk**.
3. **Validation** passes after substantive edits (**Python compile**, **`build.py`**, **scanners**).

---

## Process

1. **Re-read** the selected **IDs** from the delta—**no** scope creep.
2. **Apply** each fix: path moves, **`content/parts/`** layout, **`rules/`**, **`skill-config.json`**, **`build.py`** merge lists—whatever the **ID** requires.
3. Run **`python scripts/base/build.py`**; fix **sources**, not **AGENTS.md** by hand.
4. Re-run **validation** steps (compile paths, **build**, scanners).
5. **Update** the delta file: mark rows **fixed** / **deferred** / **accepted risk**.

---

## AI behavior

- **Straight delta:** implement **only** what **1b** and the user agreed—**no** silent full rewrites.
- **Be specific** in commits/edits: one **ID** per logical change when practical.
- After **migrate**, consider **[`fill-scaffold-parts.md`](fill-scaffold-parts.md)** (**2c**) if **`library/`** / **`rules/`** still need **authoring** beyond layout fixes.
