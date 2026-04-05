# Phase — Plan skill migration

This is **phase 1b** in [`../process.md`](../process.md) (**Stage 1 — Plan**). Use it when the skill **already exists** and you need a **written plan** before **moving** anything: inventory, **compare to standards**, **delta table**, user **selection** of what to fix. **Execution** (moves, patches) is **[`migrate.md`](migrate.md)** (after this plan) — not here.

For **greenfield** planning (new skill, no tree yet), use **[`plan-script-build.md`](plan-script-build.md)** (**1a**).

Emit this file for an AI session with:

```bash
python scripts/base/generate.py --phase plan-migrate
```

---

## Outcome

1. A **delta report**: what differs from the standards, **where**, and **why it matters**.
2. A **user choice**: which deltas to fix in the **migrate** phase (now, later, or **won’t fix** with rationale).

The agent (or a human) **does not** apply bulk rewrites in this phase—it **surfaces gaps** and **records** the plan.

---

## Process (human + AI)

### 1. Inventory

Walk the skill root and note:

| Area | Look at |
|------|---------|
| **Entry** | `SKILL.md` frontmatter, description |
| **Checklist reference** | **[How checklists are created](../library/base/checklist.md)** — stable **`content/parts/library/base/checklist.md`**; workspace **`…/progress/process-checklist.md`** and per-phase **`…/progress/<slug>-checklist.md`** from **`generate.py`**. Check off **`- [ ]` → `- [x]`** in **`progress/`** as you go. |
| **docs/ vs parts** | **`docs/`** — non-runtime only (manuals, plans, architecture, optional checklist copies, **`standards-delta.md`** in **abd-skill-builder** only). **Mergeable / operation-time** markdown lives under **`content/parts/`** (and **`library/`**, **`rules/`**). If **`docs/`** holds instruction bodies that should merge, **move** them into **`parts/`** and leave **`docs/`** as index or narrative only (see **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)** — **`docs/` vs mergeable markdown**) |
| **Build / validation** | `skill-config.json` → **`build.*`**, paths on disk |
| **Delivery** | `delivery.mode`, `AGENTS.md`, `content/built/` if `static_built` |
| **Content** | `content/parts/process.md`, phase slugs, `build.py` merge order |
| **Library** | `content/parts/library/` — cross-cutting concepts (definitions, tables, glossaries) reused across phases; merge order in `build.py`; no second home for cross-cutting material outside **`library/`** |
| **Rules / scanners** | `rules/`, `rules/scanners.json`, bindings |
| **Scripts** | `scripts/base/build.py`, scanners, `compileall_paths` |
| **Tests** | `test/` layout and expectations in **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md#repository-shape-skill-package-root)** (repo table) and **[#validation-and-tests](../library/skill-structure-and-concepts.md#validation-and-tests)**; pytest wiring if tests exist |
| **ABD / workspace** | `skill-config.json`, `active_skill_workspace` |
| **Narrative / identity** | Phases, rules, `SKILL.md` describe **this skill’s** behavior — not chronic “vs other skill” or “we skip X because Y” stories (see **Skill identity** in **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md#skill-identity)**). Dependencies listed **explicitly** where needed. |

### 2. Compare to standards

For each row in the **repository shape** table and the **`skill-config.json` / pipeline** guidance in **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)**, mark:

- **Compliant** — matches normative text.
- **Partial** — close but missing rename, doc, or wiring.
- **Gap** — missing file, wrong shape, or contradicts standards.

Use **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)** as the bar.

### 3. Delta report (written artifact)

Produce a **single markdown or table** the user can keep in the skill (e.g. **`docs/standards-delta.md`**) with **one row per gap**:

| ID | Area | Current state | Expected (standard) | Severity (high/med/low) | Suggested fix |
|----|------|----------------|---------------------|-------------------------|---------------|
| D1 | … | … | … | … | … |

Optional: group by **validation** vs **content** vs **tests** so **[`migrate.md`](migrate.md)** can batch fixes.

### 4. Ask the user what to fix (next phase)

**Prompt (use verbatim spirit):**

> Here are the gaps between this skill and the repository standards (**N** items).  
> Which **IDs** should we fix in the **migrate** phase? You can choose **all**, **none** (document deferrals only), or a **subset**. For any item you **won’t** fix, say **defer** or **won’t fix** and a one-line reason.

Record selections; **[`migrate.md`](migrate.md)** applies **only** those IDs.

---

## AI behavior

- **Be specific:** cite paths and standard sections (e.g. “§3.1 phase slugs”).
- **Don’t** treat every cosmetic difference as high severity.
- **Do** call out **build/validation** failures and **security**-sensitive paths (secrets, arbitrary paths) as **high**.
- If **`pytest`** was requested but missing: reference **[Validation and tests](../library/skill-structure-and-concepts.md#validation-and-tests)** in **skill-structure-and-concepts.md**.
