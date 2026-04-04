# skill-plan — my-skill

Fill this during **Stage 1 — Plan**. Lives at `docs/skill-plan.md` in your skill workspace. See [`templates/skill-plan.md.template`](../../templates/skill-plan.md.template) for authoring guidance.

## Action checklist

- [ ] **Delivery mode** chosen and recorded below (`skill-config.json` → `delivery.mode`).
- [ ] **Phases** listed in table below; aligned with `content/parts/process.md`.
- [ ] **Rules and scanners** listed, or explicitly "none yet."
- [ ] **Library files** decided — which cross-cutting norms will phases inject?
- [ ] **Actor / role** identified (human, AI, mixed).
- [ ] **Operator chain** understood: compile → `build.py` → scanners.
- [ ] **Workspace:** `conf/abd-config.json` → `active_skill_workspace` set correctly.

## Delivery mode

- **Choice:** `static_built` | `runtime_injection` *(circle one; match `skill-config.json`)*
- **Rationale:**

## Phases

| # | Phase slug | Purpose |
|---|-----------|---------|
| 0 | workspace-and-config | Confirm paths; install conf |
| 1 | author | Write skill content |

## Rules and scanners

*None yet — add in Stage 2.*

| Rule file | Scanner | What it checks |
|-----------|---------|----------------|

## Library components

- *(Which files from `content/parts/library/` will phases inject?)*

## Actor / role

- *(Who runs each phase; what the skill optimises for.)*

## Operator, workspace, and delivery

- **Static vs dynamic:** *(How parts assemble into `AGENTS.md` or are injected at runtime.)*
- **Operator chain:** compile → `python scripts/build.py` → scanners.
- **`active_skill_workspace`:** *(Absolute path set in `conf/abd-config.json`. Run `python scripts/set_workspace.py <path>` to set.)*

## Authoring checklist

*Populated by scaffold from `abd-skill-builder/content/parts/library/authoring-checklist.md`. The first unchecked box is where you resume after an interruption.*

---

### Before you start (every session)

- [ ] **Working copy:** `docs/skill-plan.md` includes this **## Authoring checklist** section.
- [ ] **Resume:** Find the **first unchecked** `- [ ]` and continue from there.
- [ ] **Optional:** Note the date and "stopped at §…" in **Gaps / follow-ups** when pausing.
- [ ] **`docs/` vs `content/parts/`:** No runtime markdown under `docs/` — phases, library bodies, and anything `build.py` merges/injects stay in `parts/`.

---

### Greenfield vs existing skill

- [ ] **New skill:** Ran scaffold so the base tree exists (`skill-scaffold/` copied and renamed).
- [ ] **Existing skill:** Ran migration plan before bulk edits — or consciously skipped with a note in **Gaps / follow-ups**.

---

### Scaffold files present and reviewed

- [ ] **`SKILL.md`** — front matter and description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; `phase_rules` lists rule stems.
- [ ] **`conf/abd-config.json`** — `active_skill_workspace` set.
- [ ] **`scripts/set_workspace.py`** — present.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in `process.md`.
- [ ] **`scripts/build.py`** — merge/injection driver present.
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout.

---

### Gaps / follow-ups

*(Record date and where you stopped when pausing. Continue from first unchecked box.)*
