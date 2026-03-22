# abd-skill-builder

Standalone skill for **repo layout standards**, **scaffolding new skills**, and **AGENTS.md assembly** — use it from any editor or agent without depending on a specific host app.

**Normative bodies** live under **`content/parts/library/`** and **`content/parts/phases/`**; **`docs/`** holds planning notes (**`standards-delta.md`**), **`docs/delivery.md`** (merge / **`static_built`** lookup), **`docs/authoring-checklist.md`** (working copy), and short stubs that link into **`content/parts/`**. See **`rules/content-placement.md`**.

**Delivery:** **`skill-config.json`** → **`delivery.mode`**: **`static_built`**. Pre-merged outputs: root **`AGENTS.md`** and **`content/built/AGENTS.md`** (identical). See **`docs/delivery.md`**. **Commit policy:** this repo commits **`content/built/*`** after meaningful part/build changes; teams may instead regenerate in CI and omit commits (document in your fork).

## Quick start

- **§3 layout & content (normative):** `content/parts/library/skill-standards-section-3.md` (stub: `docs/reference/skill-standards-section-3.md`)
- **Index + Operator checklist:** `content/parts/library/skill-repo-standards.md` (stub: `docs/skill-repo-standards.md`)
- **Builder vs Operator:** `content/parts/library/builder-vs-operator.md` (stub: `docs/builder-vs-operator.md`)
- **Authoring checklist (ask / AI-suggest / track):** canonical `content/parts/library/authoring-checklist.md`; **working copy:** `docs/authoring-checklist.md` (copy into other skills as `docs/authoring-checklist.md`)
- **Migrate existing skill to standards (deltas → user picks fixes):** `content/parts/phases/migrate.md` (stub: `docs/migrate-skill-to-standards.md`)
- **Scaffold a new skill:**  
  `python scripts/scaffold_skill.py --name my-skill --out ../my-skill --purpose "…"`
- **Build AGENTS.md (this skill):**  
  `python scripts/build.py`
- **Minimal valid skill example (polite dialogue phases):** `test/fixture/toy-polite-dialogue/` — same layout **`agentic-skill-builder`** operator tests use (path resolved from monorepo root).

## Relation to agentic-skill-builder

**`agentic-skill-builder`** runs **`operator.run_operator()`** against a skill directory (**compileall** + **`scripts/build.py`** + scanners). This skill supplies the **standards**, **`scaffold_skill.py`**, and **templates** used to **create** compliant trees; Operator **validates** them.

See **`../agentic-skill-builder/README.md`**.

## Deploy to Cursor skills (junction)

Cursor loads installable skills from **`%USERPROFILE%\.cursor\skills\`** (each skill is a folder with `SKILL.md` at the root). To keep a **single source of truth** in this repo, use a **directory junction** on Windows:

```bat
cmd /c mklink /J "%USERPROFILE%\.cursor\skills\abd-skill-builder" "c:\dev\agilebydesign-skills\skills\abd-skill-builder"
```

- If `abd-skill-builder` already exists there, remove it first (only if it is not the junction you want): `rmdir "%USERPROFILE%\.cursor\skills\abd-skill-builder"` — **do not** use `rmdir` on the repo side; junction removal only deletes the link.
- After linking, the skill appears alongside e.g. `.cursor\skills\content-memory`.
