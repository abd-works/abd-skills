# Migrate an existing skill to repository standards

Use this when the skill **already exists** and you need to **align** it with **[`skill-repo-standards.md`](../library/skill-repo-standards.md)**, **[`skill-standards-section-3.md`](../library/skill-standards-section-3.md)**, and (where relevant) the **[authoring checklist](../library/authoring-checklist.md)** — not when you are **scaffolding from zero** (`scaffold_skill.py`).

## Outcome

1. A **delta report**: what differs from the standards, **where**, and **why it matters**.
2. A **user choice**: which deltas to fix now, later, or **won’t fix** (with rationale).

The abd-skill-builder agent (or a human) **does not** silently rewrite the whole tree; it **surfaces gaps** and applies fixes **only for items the user selects**.

---

## Process (human + AI)

### 1. Inventory

Walk the skill root and note:

| Area | Look at |
|------|---------|
| **Entry** | `SKILL.md` frontmatter, description |
| **Authoring checklist** | In **each skill** (or workspace): **`docs/authoring-checklist.md`** — copy from [`../library/authoring-checklist.md`](../library/authoring-checklist.md) in **abd-skill-builder** if missing; check off **`- [ ]` → `- [x]`** as you go (resume from first unchecked). **abd-skill-builder** does not keep a checklist under its own **`docs/`**. |
| **docs/ vs parts** | **`docs/`** — non-runtime only (manuals, plans, architecture, optional checklist copies, **`standards-delta.md`** in **abd-skill-builder** only). **Mergeable / operation-time** markdown lives under **`content/parts/`** (and **`library/`**, **`rules/`**). If **`docs/`** holds instruction bodies that should merge, **move** them into **`parts/`** and leave **`docs/`** as index or narrative only (see **`skill-repo-standards.md`**) |
| **Operator** | `skill-config.json` → `operator.*`, paths on disk |
| **Delivery** | `delivery.mode`, `AGENTS.md`, `content/built/` if `static_built` |
| **Content** | `content/parts/process.md`, phase slugs, `build.py` merge order |
| **Library** | `content/parts/library/` — cross-cutting concepts (definitions, tables, glossaries) reused across phases; merge order in `build.py`; no second home for cross-cutting material outside **`library/`** |
| **Rules / scanners** | `rules/`, `rules/scanners.json`, bindings |
| **Scripts** | `scripts/build.py`, scanners, `compileall_paths` |
| **Tests** | `test/` per **Tests & fixtures** in [`../library/skill-repo-standards.md`](../library/skill-repo-standards.md); pytest wiring if tests exist |
| **ABD / workspace** | `conf/abd-config.json`, `active_skill_workspace` |
| **Narrative / identity** | Phases, rules, `SKILL.md` describe **this skill’s** behavior — not chronic “vs other skill” or “we skip X because Y” stories (see **Documentation focus** in [`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)). Dependencies listed **explicitly** where needed. |

### 2. Compare to standards

For each row in **`skill-repo-standards.md`** (quick layout table) and the **§3** tables where applicable, mark:

- **Compliant** — matches normative text.
- **Partial** — close but missing rename, doc, or wiring.
- **Gap** — missing file, wrong shape, or contradicts standards.

### 3. Delta report (written artifact)

Produce a **single markdown or table** the user can keep in the skill (e.g. **`docs/standards-delta.md`**) with **one row per gap**:

| ID | Area | Current state | Expected (standard) | Severity (high/med/low) | Suggested fix |
|----|------|----------------|---------------------|-------------------------|---------------|
| D1 | … | … | … | … | … |

Optional: group by **Operator** vs **content** vs **tests** so fixes can be batched.

### 4. Ask the user what to fix

**Prompt (use verbatim spirit):**

> Here are the gaps between this skill and the repository standards (**N** items).  
> Which **IDs** should we fix in this session? You can choose **all**, **none** (document deferrals only), or a **subset**. For any item you **won’t** fix, say **defer** or **won’t fix** and a one-line reason.

Then:

- Apply **only** agreed fixes (edits, new files, `skill-config.json` updates).
- Re-run **operator** checks (Python compile check, `build.py`, scanners) after substantive changes.
- Update the delta report: mark rows **fixed**, **deferred**, or **accepted risk**.

---

## AI behavior

- **Be specific:** cite paths and standard sections (e.g. “§3.1 phase slugs”).
- **Don’t** treat every cosmetic difference as high severity.
- **Do** call out **operator** failures and **security**-sensitive paths (secrets, arbitrary paths) as **high**.
- If **`pytest`** was requested but missing: reference **When automated tests are asked for** in **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**.

---

## Related

- **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)** — full checklist for **after** migration (or in parallel for deep refactors).
- **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)** — index of conventions.
- **[agentic-skill-builder README](../../../agentic-skill-builder/README.md)** — strategize / delivery graph (for `conf/build-strategy.json`).
