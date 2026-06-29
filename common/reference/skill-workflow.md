# Skill Workflow

**You were sent here from a practice skill's `SKILL.md`.** Read this file **in its entirety** before generating, grilling, or validating. Order: **bootstrap** (engagement context) → **read-gates** (skill package) → generate → validate ([`rule-checklist.md`](./rule-checklist.md) Steps 2–4).

---

## Bootstrap (engagement context)

**Hard gate before skill read-gates.** The skill package defines *how* to work; the engagement defines *what already exists*.

1. **`cdd-context-index.md`** at the workspace root — artifact paths when present ([`folder-conventions.md`](./folder-conventions.md) § Non-standard locations).
2. **Existing deliverables** for this scope — upstream phase output and peer-perspective artifacts (filenames in [`skill-index.md`](./skill-index.md)).
3. **Decision records** — read every **`DR-*.md`** / **`ADR-*.md`** under decision folders relevant to the active skill's practice context ([`decision-record.md`](./decision-record.md)). Read **Accepted** records in full; respect **Superseded** / **Deprecated**; treat **Proposed** as unsettled. Check at minimum:
   - `docs/decisions/` (project-wide)
   - Practice folder when applicable: `docs/stories/decisions/`, `docs/domain/decisions/`, `docs/architecture/decisions/`, `docs/ux/decisions/`
   - `docs/sessions/<session>/decisions/` when working in a named session

When a choice meets DR criteria during this run, write a new record per [`decision-record.md`](./decision-record.md) — do not bury major decisions in chat or deliverable prose only.

---

## Output file resolution (deliverables)

**Where to write** — resolve `<deliverables-folder>` in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **`cdd-context-index.md` at the workspace root.** If this file lists a path for this artifact, use that path. Update the row if it changes.
3. **Where the engagement already keeps deliverables.** Write next to existing phase output in the **same** folder.
4. **Canonical scaffold path** from [`folder-conventions.md`](./folder-conventions.md) for the active skill.
5. **The workspace root.** Last resort only.

**File name** — after the folder is resolved:

1. If the active skill has **`reference/output.md`**, read it for file name, naming pattern, or non-`docs/` rules (e.g. project test folder).
2. Otherwise use the file name in [`folder-conventions.md`](./folder-conventions.md) for this skill (typically `<artifact-stem>.md`).
3. Add a `<name>-` prefix only when disambiguation is needed.

Most skills need no `reference/output.md` — `folder-conventions.md` is enough. Add `reference/output.md` only when the skill breaks the default (tests in project tree, multiple named outputs, non-`.md` deliverable).

---

## Read-gates

Before authoring any artifact — **hard gate, no exceptions.** Read in this order:

1. **`rules/`** — **every** file for the active skill, **read in full**.
2. **`reference/`** — **every** file in the skill's `reference/` folder, **read in full**, except **`grill-me.md`** (grill mode only — step 5).
3. **`templates/`** — **every** file in the skill's `templates/` folder, **read in full** (layout contracts and filled examples — do not copy `## Instructions` blocks into deliverables).
4. **Practice family `reference/`** — read **every** file in the practice `<family>-perspective.md` shared-reference table, plus **every** practice file linked from **any** file in this skill's `reference/` folder, **read in full**.
5. **Grill mode only** — if the invocation includes **"grill me"**, read [`grill-me-with-practice-skill.md`](./grill-me-with-practice-skill.md) and the active skill's **`reference/grill-me.md`** **in full**; ask questions one at a time from `reference/grill-me.md` only (not from `input-traps.md`).

**Read each file in full** — no skimming, no summarizing from memory, no skipping sections. Do not rely on the SKILL body alone. Complete **§ Bootstrap** first, then steps 1–4 (and step 5 when grill mode is active). No main task starts until bootstrap and read-gates are done.

---

## Generate (deliverables)

After read-gates:

- Author to **every** file in `rules/` — each DO / DO NOT is a shape contract.
- Produce **one deliverable per file** in `templates/` (and for any new template added later).
- Generated project files contain **stakeholder-facing content only** — never paste template `## Instructions` or maintainer notation sections into deliverables.

Skill-specific workflow order, fidelity branching, and pre-scanners live in **`reference/generate.md`** when that file exists. Shape contracts are in **`rules/`** and **`templates/`** — do not duplicate them in `SKILL.md`.

---

## Validate output

After generating, run [`rule-checklist.md`](./rule-checklist.md) **Steps 2–4** in full. Step 1 confirms § Read-gates above were completed before work started.

---

## Diagram workflow (non-blocking)

After the scanner pass, check whether the active skill has **`reference/diagram-workflow.md`**. If it does, launch a **background sub-agent** (Task tool, `run_in_background: true`) with that file's contents and enough context (deliverables folder, output paths) for it to execute the CLI command independently. Do not wait for the sub-agent before returning to the user.

---

## Correction process

When something is wrong: identify → log → re-generate → iterate on the output until correct, then optionally improve the source skill. See `skill-helpers/instructions/log-and-fix-skill-errors` for the full loop. Put the log under the engagement tree — not inside the skill package.
