# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` (`principles-and-rules.md`, `execution-and-success.md`, `pipeline_invariants.md`); **link** from `content/parts/` where needed | Restate every phase inside them; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and fixture paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.
