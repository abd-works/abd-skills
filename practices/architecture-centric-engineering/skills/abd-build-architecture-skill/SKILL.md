---
name: abd-build-architecture-skill
description: >-
  Build a new implementation skill — a full practice-skill package that
  generates code in a chosen architecture — from an architecture-mechanism
  reference document. Input is a finished reference (one file with layered
  description and one section per mechanism, covering principles,
  patterns, file structure, participants, flow, walkthrough, and testing).
  Output is a complete practice-skill folder: SKILL.md, templates/ that
  produce real domain modules, rules/*.md that validate generated code
  against the reference's principles and patterns, ide-files/, and a
  scanners/ stub. Use this skill when you have a finished architecture
  reference and need the agent / team to be able to generate code that
  follows that architecture, one mechanism at a time or one domain module
  at a time.
---
# abd-build-architecture-skill

## Purpose

A team can write down its architecture and still ship code that drifts from it within a quarter. Documents do not enforce themselves. This skill closes that gap by turning a finished architecture document into an **active, automatable practice** — a packaged generator that produces real code in the architecture on demand, with checkable rules an agent or reviewer can run against any change. The output is itself a skill: a folder with `SKILL.md`, `templates/`, `rules/`, and `ide-files/` ready to be loaded and run. When this skill is done, the architecture is no longer just written down somewhere; it is something the team can *invoke* — to scaffold a new module, to check a pull request, to onboard a new engineer — and get the same answer every time.

## When to use this skill

Load this skill when **any** of the following apply:

- A team has agreed an architecture on paper but the actual code keeps drifting; you want a **single command** that produces code in the agreed shape so new work starts in the right place.
- You are **standing up a new project** in an architecture that does not have an automated way of generating modules yet — and you want the agent (and humans) to produce the same layout every time.
- Code review for the same architectural concerns (layer leaks, anemic domain objects, missing tests at the right tier) keeps catching the same mistakes; you want those checks **enforced at generation time**, not at review time.
- The team has multiple sibling stacks (one Node service, one Python worker, one Go gateway) and each needs its own *named, loadable* way to produce code in its own architecture — so an agent can be told "use the X architecture" and produce the right thing.
- An onboarding engineer can read the architecture document but still cannot produce a correct module on their first try; you want a generator that does the boilerplate so they can focus on the domain.

---

## Agent Instructions

1. **Gather the reference context first.** You need an **architecture-mechanism reference document** in front of you — one that names the architecture's principles, patterns, file structure, participants, flow, and a walkthrough for every mechanism in scope. It can be a fresh document, an ADR set, a wiki page that has already been used by humans on real code, or output produced by a sibling skill. The shape matters more than the source: every mechanism should already have its **Principles & Patterns**, **File Structure**, **Participants**, **Flow**, and **Walkthrough Example** filled in. If pieces are missing, stop and finish the reference before generating the implementation skill — what is not in the reference cannot be enforced by the skill you are about to author.

   The shape of the **target skill** this skill produces lives in [`templates/generated-SKILL.md`](templates/generated-SKILL.md). Read it once before generating a new skill so the shape stays consistent — that template is the worked example of what comes out, and it is self-contained inside this skill.

2. **Templates.** This skill ships **two** templates for the output skill, plus a rule scaffold. Use **every** template; do not skip the rule scaffold.

   | Template | What it produces (in the generated skill) |
   | --- | --- |
   | `templates/generated-SKILL.md` | The `SKILL.md` of the implementation skill being built |
   | `templates/generated-domain-module.template.txt` | The implementation template the generated skill ships under `templates/` |
   | `templates/generated-rule.md` | One rule file (copy per mechanism / per principle) the generated skill ships under `rules/` |

3. **One generated rule per principle.** Walk the **Principles & Patterns** subsection of every mechanism in the reference. Each principle becomes one `rules/<principle-slug>.md` in the generated skill, with `DO` / `DO NOT` / examples that judge real code against that principle. Each pattern becomes the **pass-side example** in that rule.

4. **One template variant per language tier.** If the architecture has multiple language tiers (e.g. MERN has TypeScript shared/server/client; Python clean might have only one tier), produce a templates entry per tier and have the generated `SKILL.md` reference it.

5. **Rules of this skill.** Generate content following the rules attached to this skill (bundled below). After writing, peer-review the generated skill against this skill's rules — and also check that the generated skill's bundled rules each trace back to a reference document principle.

6. **Verify with scanners.** After producing the generated skill, run:

   ```bash
   python skill-builder/skills/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root engineering/skills/<generated-skill-name>
   python skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
     --skill-root skill-builder/skills/abd-author-practice-skill \
     --workspace C:/dev/agilebydesign-skills/architecture-centric-engineering/skills/<generated-skill-name>
   ```

   The first command bundles `rules/*.md` into the generated skill's `SKILL.md`; the second runs the `mdc-instructions-parity` scanner against the generated skill's `ide-files/`.

7. **Assembling this skill.** After editing rules in **this** skill, run:

   ```bash
   python skill-builder/skills/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root engineering/skills/abd-build-architecture-skill
   ```

---

## What is an "architecture implementation skill"?

An **architecture implementation skill** is a packaged practice — same shape as every other `abd-*` skill — that takes a project's domain requirements (a story, an entity, a sub-epic) and **emits code that already obeys a specific architecture**. It is the inverse of a reference document: the reference tells you what the architecture is; the implementation skill turns that knowledge into runnable folders, files, and tests. The full shape an implementation skill takes lives in [`templates/generated-SKILL.md`](templates/generated-SKILL.md): a complete `SKILL.md` with Purpose / When to use / Build / Validate, plus a `templates/` set that produces real domain modules, a `rules/` set that fails on code which violates the architecture's principles, an `ide-files/` triple, and an optional `scanners/` folder.

This skill is a **skill that produces such a skill**. It is loaded once per architecture (not per domain module) and the generated skill is then loaded per module from that point on.

---

## Core concepts

### Reference → skill: one-to-one mapping

The reference document fixes the architecture; the generated skill fixes how to write code in it. The mapping is intentional:

| Reference document part | Generated skill part |
|---|---|
| **Overview** (principles list) | `SKILL.md` **Purpose** + **What is …** sections |
| **Architecture Layers** | `SKILL.md` **Core concepts → Layers** table + `templates/` folder structure |
| **Mechanism: File Structure** | `templates/<mechanism>.template.txt` folder tree |
| **Mechanism: Participants** | `templates/` named files / classes; `SKILL.md` **The shape of a good module** block |
| **Mechanism: Flow** | `SKILL.md` **Build steps** numbered list |
| **Mechanism: Walkthrough Example** | `SKILL.md` **Example** section (one full filled example) |
| **Mechanism: Principles & Patterns** | One `rules/<principle-slug>.md` per principle, with the pattern as the `Example (pass)` |
| **Mechanism: Testing the mechanism** | `rules/test-structure.md` plus the generated skill's `Validate` checklist |

If a part of the reference has no corresponding part in the generated skill, either the reference is missing material or the generated skill is missing scope; both are bugs to fix before declaring the generated skill done.

### The generated skill is a regular practice skill

The output of this skill is **just a practice skill**. It has a `SKILL.md` with **Purpose**, **When to use**, **Core concepts**, **Build**, **Validate**, an `ide-files/` triple, and a bundled `rules/*.md` block. It can be deployed with the same `Deploy-SkillOutputs.ps1` and validated with the same `mdc-instructions-parity` scanner as any other skill in this repository. There is **nothing special** about it being generated — that is by design.

### Mechanism slice vs. domain slice

The generated skill can be invoked in **two slicing modes**, and the `SKILL.md` it produces must support both:

- **Domain slice** — generate a full domain module (e.g. `recipients`, `payments`, `invoices`) that covers every mechanism for one capability.
- **Mechanism slice** — generate only the code for one mechanism (e.g. just the caching side-car around an existing repository, or just the error-mapper) without re-emitting the whole module.

Both modes share the same `templates/` files but call out different subsets in the generated `Build` steps.

### Scanners are optional but expected

If the architecture has machine-checkable invariants (no `mongoose` import in `shared/`, no `process.env` outside the composition root), the generated skill should ship `scanners/<lang>/<scanner>.py` that enforce them. This skill does **not** invent scanner scripts that do not exist; instead, the generated `SKILL.md` references future scanner names with a `# TODO` block, and the corresponding `scanner:` YAML field is only added to a rule when the script is actually present on disk.

### Sections and rules

`SKILL.md` carries teaching and workflow order. `rules/*.md` validate **the generated skill** — required parts, traceability to the reference, template coverage, ide-files parity. The generated skill in turn has its own `rules/*.md` that validate **generated code**.

---

## Example

For a reference document with layers **Presentation / Application / Domain / Infrastructure** and three mechanisms (Error Handling, Caching, Persistence), this skill produces a folder like:

```
architecture-centric-engineering/skills/<arch-name>-technical-architecture/
├── SKILL.md                          # one section per layer + Build/Validate
├── inputs/
│   └── architecture-reference.md     # copied from abd-architecture-template
├── templates/
│   ├── domain-module.template.txt    # the full folder tree the generated skill emits
│   └── domain-module/                # (optional) sub-templates per layer
├── rules/
│   ├── maintain-layer-purity.md      # from "Domain never imports infrastructure"
│   ├── implement-domain-entities-correctly.md   # from "Behavior on entity"
│   ├── handle-errors-at-boundary.md  # from Error Handling principle
│   ├── cache-via-side-car.md         # from Caching principle
│   ├── use-repository-for-persistence.md
│   ├── use-ubiquitous-language.md    # inherited from project's coding standard (e.g. abd-clean-code)
│   └── test-story-driven.md          # inherited from project's testing standard (e.g. abd-acceptance-test-driven-development)
├── ide-files/
│   ├── <arch-name>-technical-architecture.mdc
│   ├── <arch-name>-technical-architecture.instructions.md
│   └── <arch-name>-technical-architecture.prompt.md
└── scanners/
    └── README.md                     # listed targets; populated as scanners are written
```

The generated `SKILL.md` follows the structure laid out in `templates/generated-SKILL.md` — same headings, same rules block, same bundled-rules markers — but the **content** of every rule and every template is bound to the reference document's principles and patterns.

---

## The shape of a good generated skill

```
<arch>-technical-architecture/
├── SKILL.md
│   ├── Purpose                       (paragraph + bullet principles)
│   ├── When to use                   (5 triggers)
│   ├── Agent Instructions            (Read reference → Templates → Rules → Scanners → Verify)
│   ├── What is <Arch>?               (one-sentence positioning + 4 principles)
│   ├── Core concepts                 (Layers table + key abstractions)
│   ├── Example                       (one filled mini-module)
│   ├── The shape of a good module    (folder tree)
│   ├── Build                         (numbered steps; mechanism-by-mechanism)
│   ├── Validate                      (checklist)
│   └── bundled rules block
├── inputs/architecture-reference.md  (the contract; copied)
├── templates/                        (one .template.txt per language tier or per mechanism)
├── rules/                            (one per principle from the reference, plus inherited rules)
├── ide-files/                        (.mdc, .instructions.md, .prompt.md — body parity)
└── scanners/                         (per-language; optional; only referenced if present)
```

Each generated rule file must be **traceable** back to a specific reference document principle. A reviewer should be able to read the rule, then open the reference, and find the source sentence on first try.

---

## Build

**Goal:** From one architecture reference document, produce one complete implementation skill that any agent can load to generate code in that architecture.

- **Outputs:** A new folder `architecture-centric-engineering/skills/<arch-name>-technical-architecture/` (or under another namespace if the user specifies) containing `SKILL.md`, `inputs/architecture-reference.md`, `templates/`, `rules/`, `ide-files/`, and an empty `scanners/` placeholder.
- **Per format:** `SKILL.md` follows the abd-author-practice-skill bundled rules (clear English everywhere, opening sections are outcomes not mechanics, anti-patterns live in rules). Templates ship at least one filled mini-example. Rules each have `DO` / `DO NOT` / Example (pass) / Example (fail).
- **While writing:** Every generated rule traces back to a reference principle; every generated template traces back to a reference file-structure block; every generated `Example` traces back to a reference walkthrough.

**Build steps:**

1. **Confirm and copy the reference.** Read the reference document. Copy it into the generated skill at `inputs/architecture-reference.md` — always a single file, mechanisms organized inside it in one combined section or one section per mechanism. The generated skill **owns its own copy** so it does not silently drift if the source reference changes.

2. **Scaffold the generated folder.** Create `architecture-centric-engineering/skills/<arch-name>-technical-architecture/` with empty `templates/`, `rules/`, `ide-files/`, `scanners/`. Pick `<arch-name>` from the reference document's title (lowercase, hyphens, no spaces).

3. **Generate `SKILL.md` from `templates/generated-SKILL.md`.** Fill in the Purpose / When to use / Agent Instructions / What is `<Arch>` / Core concepts / Example / The shape of a good module / Build / Validate sections from the reference document content. Keep `SKILL.md` under 500 lines; push deep examples into the inputs reference instead.

4. **Generate one `rules/<principle-slug>.md` per principle** using `templates/generated-rule.md`. The principle line from the reference becomes the rule's opening paragraph. The named pattern becomes the `Example (pass)` block; an anti-pattern (often the "WRONG" example from the reference's walkthrough) becomes the `Example (fail)` block. Add canonical inherited rules from the **project's coding standard and testing standard** (typically `abd-clean-code` and `abd-acceptance-test-driven-development` when those are in scope — use-ubiquitous-language, use-domain-language, test-story-driven, etc.) by **name reference**, not by copy.

5. **Generate `templates/`.** Produce one `.template.txt` (or per-language equivalent) that, taken together with the reference's File Structure blocks, lays out every file the generated skill expects a module to contain. Each template must ship at least one **filled** mini-example (per the `templates-include-ideal-filled-examples-for-audience` rule in `abd-author-practice-skill`).

6. **Generate `ide-files/`.** Produce the three-file IDE bundle: `<arch-name>-technical-architecture.mdc`, `<arch-name>-technical-architecture.instructions.md` (byte-equivalent body), and `<arch-name>-technical-architecture.prompt.md`. The body of the first two must match after normalization — the `mdc-instructions-parity` scanner will enforce this.

7. **Bundle the generated rules.** From the agilebydesign-skills repo root, run:

   ```bash
   python skill-builder/skills/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root engineering/skills/<arch-name>-technical-architecture
   ```

8. **Run the mdc-instructions-parity scanner** against the generated skill (absolute `--workspace` path):

   ```bash
   python skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
     --skill-root skill-builder/skills/abd-author-practice-skill \
     --workspace C:/dev/agilebydesign-skills/architecture-centric-engineering/skills/<arch-name>-technical-architecture
   ```

9. **Peer-review.** Walk this skill's bundled rules against the generated skill. Then walk the **generated skill's** bundled rules against a synthetic generated module to confirm the generated skill itself is internally consistent. Fix violations before considering the work done.

---

## Validate

**Goal:** Inspect the **generated** skill the way a reviewer would inspect any new practice skill.

- **Who is checking:** Software Architect (does the generated skill's principles match the reference?), Tech Lead (can a new engineer load it and produce a module without further questions?), Skill Curator (does it follow the abd-author-practice-skill conventions?).
- **Cross-artifact parity:** Every rule in the generated skill traces back to a principle in `inputs/architecture-reference.md`. Every template traces back to a File Structure block. Every Example traces back to a Walkthrough.

Checklist for the **generated** skill folder:

- **Reference present and owned** — `inputs/architecture-reference.md` exists in the generated skill (a single file) so the skill is self-contained.
- **One rule per principle** — every principle from the reference appears as a `rules/<slug>.md`, and the rule's `Example (pass)` matches the reference's named pattern.
- **Templates cover the file structure** — every file path mentioned in the reference's File Structure blocks appears in at least one template; templates ship at least one filled mini-example.
- **`SKILL.md` shape** — Purpose, When to use, Agent Instructions, What is, Core concepts, Example, Build, Validate, bundled rules — and Purpose stays outcome-not-mechanics (per the `opening-sections-give-outcomes-not-package-mechanics` rule from abd-author-practice-skill).
- **`ide-files/` parity** — `.mdc` and `.instructions.md` bodies match after normalization (mdc-instructions-parity scanner passes).
- **Bundle is fresh** — the inlined rule block at the bottom of the generated `SKILL.md` matches the on-disk `rules/*.md`.
- **No invented mechanisms** — the generated skill does not enforce a principle that is **not** in the reference document.
- **Code conventions inherited** — the generated skill references the project's coding standard and testing standard (typically `abd-clean-code` and `abd-acceptance-test-driven-development` when those are in scope) rather than reinventing those checks.
- **Scanners honest** — `scanner:` YAML fields appear in rule files only when `scanners/<stem>-scanner.py` exists; otherwise the rule sits under Manual review.

---

<!-- execute_rules:bundle_rules:begin -->
##### Rule: Generated skill ships ide-files with .mdc and .instructions.md body parity

Every generated implementation skill must ship an `ide-files/` folder containing **three** files: `<skill-name>.mdc`, `<skill-name>.instructions.md`, and `<skill-name>.prompt.md`. The `.mdc` and `.instructions.md` files must have **byte-equivalent bodies after normalization** — same headings, same bullets, same paths — because they are deployed to Cursor (`.mdc`) and VS Code (`.instructions.md`) and must teach the same agent the same way. The `.prompt.md` file is intentionally a different, short "run this skill" invocation, not the rule body. Passing means the three files exist, the `.mdc` and `.instructions.md` bodies match, and the `mdc-instructions-parity` scanner reports PASS on the generated skill. Failing means one of the three is missing, the bodies have drifted, or `.prompt.md` has been confused with the `.mdc`.

###### DO

- Create `ide-files/<skill-name>.mdc` with YAML frontmatter (`description:` plus `alwaysApply: true`) and an instruction body that names the skill and points at `SKILL.md`.

  **Example (pass):**
  ```markdown
  ---
  description: Generate <arch> modules from the reference document
  alwaysApply: true
  ---

  # Run <arch>-technical-architecture

  Read `architecture-centric-engineering/skills/<arch>-technical-architecture/SKILL.md`...
  ```

- Create `ide-files/<skill-name>.instructions.md` whose entire content is the body of the `.mdc` after the frontmatter, byte-identical after newline normalization.

  **Example (pass):** Diffing the two files after stripping the `.mdc` YAML header yields zero differences.

- Create `ide-files/<skill-name>.prompt.md` as a separate, short slash-command invocation with its own frontmatter (`description:` only).

  **Example (pass):**
  ```markdown
  ---
  description: Run <arch>-technical-architecture to generate a module
  ---

  Read **`architecture-centric-engineering/skills/<arch>-technical-architecture/SKILL.md`** and follow the Build steps.
  ```

- After generating the three files, run the parity scanner:

  ```bash
  python skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
    --skill-root skill-builder/skills/abd-author-practice-skill \
    --workspace C:/absolute/path/to/architecture-centric-engineering/skills/<arch>-technical-architecture
  ```

  Confirm it reports PASS for `mdc-instructions-parity`.

###### DO NOT

- Ship only `.mdc` and `.prompt.md` and skip `.instructions.md` because "VS Code is not used here".

  **Example (fail):** `ide-files/` contains `<skill-name>.mdc` and `<skill-name>.prompt.md` only. The parity scanner reports MISSING `.instructions.md` and the skill cannot deploy to VS Code.

- Treat `.prompt.md` as the twin of `.mdc` and skip `.instructions.md`.

  **Example (fail):** The body of `.prompt.md` is the full instruction set and `.instructions.md` is empty. The Cursor command becomes a wall of text and VS Code parity is missing.

- Edit `.mdc` and forget to update `.instructions.md`.

  **Example (fail):** A new bullet "After scanners pass, run vitest" is added to `.mdc`; `.instructions.md` still has the previous three bullets. The parity scanner reports MISMATCH.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); enforces the same parity rule bundled in `abd-author-practice-skill` (mdc-instructions-parity).

##### Rule: Generated skill ships its own copy of the architecture reference

The generated implementation skill must contain its own copy of the architecture reference at `inputs/architecture-reference.md` — a single file, mechanisms organized inside it as the upstream authoring chose (combined section or one section per mechanism). The generated skill is the source of truth for the architecture it implements; depending on a link to another skill folder is brittle, and a copy guarantees the generated skill stays self-contained when it is deployed or moved. Passing means a reviewer can open the generated skill, read `inputs/architecture-reference.md`, and recover the full reference. Failing means the generated skill only links out, copies a partial reference, or splits the file into pieces it was not authored as.

###### DO

- Copy the **entire** reference document into the generated skill's `inputs/architecture-reference.md` exactly as it was authored. Do not reformat, split, or merge sections.

  **Example (pass):** The reference covers six mechanisms in per-mechanism sections. The generated skill's `inputs/architecture-reference.md` contains the same TOC, Overview, Architecture Layers, six `## Mechanism: <Name>` sections, Testing Architecture, and References — byte-for-byte the same body.

- In the generated `SKILL.md`'s Agent Instructions step 1, point readers at `inputs/architecture-reference.md` by relative path.

  **Example (pass):** Agent Instructions step 1 reads: "Load [`inputs/architecture-reference.md`](inputs/architecture-reference.md) to understand the authoritative architecture: layers, principles, patterns, file structure, participants, flow, walkthrough, testing."

- Document the source so a maintainer can resync if the reference is updated upstream.

  **Example (pass):** A note at the top of `inputs/architecture-reference.md` reads: `Source: architecture-centric-engineering/skills/abd-architecture-template output for {{ArchName}} produced on YYYY-MM-DD.`

###### DO NOT

- Leave `inputs/` empty in the generated skill and rely on the absolute path to where the reference happens to live today.

  **Example (fail):** The generated `SKILL.md` step 1 says "Read `C:/dev/some-project/architecture-reference.md`". When that machine path changes, the skill silently breaks.

- Copy only the Overview and skip the mechanism sections.

  **Example (fail):** `inputs/architecture-reference.md` contains the Table of Contents and Overview, but every mechanism section is replaced with `<!-- See original document -->`.

- Allow the generated skill's rules to cite mechanisms that are not in the copied reference.

  **Example (fail):** `rules/cache-via-side-car.md` cites `inputs/architecture-reference.md` "Mechanism: Caching", but the copy of the reference in `inputs/` does not contain a Caching section.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill).

##### Rule: Generated skill inherits the project's coding and testing standards by reference

The generated implementation skill must **inherit** the **project's chosen coding standard and testing standard** by **naming them explicitly** in `SKILL.md` and citing the relevant rule basenames — **not** by copying those rule files in. Whichever guides are in scope (in an agilebydesign-skills-anchored project these will typically be `abd-clean-code` and `abd-acceptance-test-driven-development`; in another project they may be a different skill, a style guide, or a corporate standard) already enforce naming, function size, dependency injection, encapsulation, test-class-per-story, and Given/When/Then helpers — duplicating those rules creates drift the moment the upstream guide is updated. Passing means the generated `SKILL.md` calls out both standards in its Agent Instructions and Validate sections, and the generated rules block does not re-implement rules that already exist upstream. Failing means the generated skill silently re-defines `use-domain-language.md` or `test-story-driven.md`, contradicts the upstream guide, or never mentions either upstream standard.

###### DO

- In the generated `SKILL.md` Agent Instructions, name the **coding standard in scope** for the project (typically `abd-clean-code` in an agilebydesign-skills-anchored project) and state that all generated production code follows it. Name the **testing standard in scope** (typically `abd-acceptance-test-driven-development`) and state that all generated test code follows it.

  **Example (pass):** Agent Instructions step 3 reads: "Code generated under this skill follows the project's coding standard (`abd-clean-code` in scope here: domain language, small functions, constructor injection, no anemic data bags). Test code follows the project's testing standard (`abd-acceptance-test-driven-development` in scope here: class per story, Given/When/Then helpers, no defensive checks)."

- In the generated `Validate` checklist, reference the upstream rule basenames by name.

  **Example (pass):** "Code passes the project's coding rules — e.g. when `abd-clean-code` is in scope: `use-domain-language`, `keep-functions-small-focused`, `enforce-encapsulation`."

- When the architecture has an **architecture-specific** twist on one of those rules (e.g. "in this architecture, ALL helpers extend a tier-base helper"), express that twist as a new rule file in the generated skill — and make the rule's opening paragraph cite the upstream rule it specializes.

  **Example (pass):** `rules/extend-tier-base-helper.md` opens: "This rule specializes `abd-acceptance-test-driven-development/rules/object-oriented-test-helpers.md` for this architecture: every tier helper extends a single base class so test data is shared."

- When the project uses a non-agilebydesign standard, cite *that* by name and link to it — same structure, different upstream.

  **Example (pass):** Agent Instructions step 3 reads: "Code generated under this skill follows the project's coding standard at `docs/coding-standards.md`. Test code follows the project's testing standard at `docs/test-style.md`."

###### DO NOT

- Copy `use-domain-language.md` from `abd-clean-code` (or the equivalent rule from whichever guide is in scope) into the generated skill's `rules/`.

  **Example (fail):** Generated `rules/use-domain-language.md` is a byte-for-byte copy of `agilebydesign-skills/architecture-centric-engineering/skills/abd-clean-code/rules/use-domain-language.md`. Updates upstream will not propagate.

- Generate a `SKILL.md` that never names the coding standard or testing standard the project is operating under.

  **Example (fail):** The generated SKILL.md describes how to build domain modules and walkthrough tests but never mentions `abd-clean-code`, `abd-acceptance-test-driven-development`, or any other style/testing guide. Reviewers have no anchor.

- Re-define a rule in the generated skill in a way that contradicts the upstream guide.

  **Example (fail):** Generated `rules/test-style.md` says "tests may use `try/catch` to guard against environment flakiness." The project's testing standard (`abd-acceptance-test-driven-development` or otherwise) says the opposite. Future code authors do not know which rule wins.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill). The generated skill inherits the project's existing code-style and test-style decisions rather than duplicating or contradicting them.

##### Rule: One generated rule per reference principle

For every **Principles & Patterns** subsection in the reference document, the generated skill must ship one corresponding `rules/<principle-slug>.md` file whose `Example (pass)` block matches the principle's named pattern and whose `Example (fail)` block matches the anti-pattern named in (or strongly implied by) the reference walkthrough. This is the **one-to-one trace** that lets a reviewer hold the reference and the generated skill side-by-side and confirm coverage. Passing means each principle has a rule, each rule has a pass and fail example, and a reviewer can match them in either direction. Failing means a principle has no rule, a rule does not name the principle it implements, or the same rule tries to cover three unrelated principles.

###### DO

- Walk every `Mechanism: <Name>` section's `Principles & Patterns` subsection. For each principle line, create one rule file named after the **valid state** the principle guards (e.g. `maintain-layer-purity.md`, `handle-errors-at-boundary.md`, `cache-via-side-car.md`).

  **Example (pass):** Reference's Caching mechanism states "Principle: the application layer is unaware of the cache." → generated skill contains `rules/keep-application-unaware-of-cache.md` whose opening paragraph begins "The application layer must never call cache APIs directly. From the Caching section of `inputs/architecture-reference.md`..."

- Use the pattern named in the reference as the rule's `Example (pass)`; use the "WRONG" code from the reference's walkthrough (or a paraphrase) as the `Example (fail)`.

  **Example (pass):** `rules/keep-application-unaware-of-cache.md` `Example (pass)` shows the `CachingRecipientsRepository` side-car (the named pattern); `Example (fail)` shows a service calling `redis.get(...)` directly (the anti-pattern).

- Tag each generated rule with a `Source:` line that points back at the reference section.

  **Example (pass):** Rule ends with `Source: inputs/architecture-reference.md — section "Mechanism: Caching", under "Principles & Patterns".`

###### DO NOT

- Skip principles the reference lists because "they're obvious" or "they're already in the project's coding standard".

  **Example (fail):** Reference lists four principles for Error Handling; generated skill has only two rule files, the other two are silently dropped.

- Lump multiple principles into one rule file.

  **Example (fail):** `rules/architecture-correctness.md` has six `DO` bullets pulled from six different reference principles. A reviewer cannot tell which violation maps to which `DO`.

- Invent a rule that is **not** in the reference (even if it sounds sensible).

  **Example (fail):** Generated skill includes `rules/use-graphql-instead-of-rest.md`. The reference does not mention GraphQL — the generated skill has drifted from its source.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); the reference→rule trace is what makes the generated skill auditable against its source document.

##### Rule: Scanner YAML field appears only when the scanner script exists

A generated rule may declare `scanner: <stem>` in its YAML frontmatter **only** when the file `scanners/<stem>-scanner.py` exists in the generated skill on disk. The frontmatter is a claim that an automated check exists; lying about that check breaks `run_scanners.py` and erodes trust in the skill. If a useful scanner is planned but not yet written, the rule sits under **Manual review** and a `# TODO scanner: <stem>` comment is added near the bottom of the rule body to record the intent. Passing means every `scanner:` value points at a real `.py` file with the same stem; missing scanners are tracked as TODOs in the rule body rather than as fake YAML fields. Failing means a rule advertises a scanner the skill does not actually ship.

###### DO

- Before adding `scanner: layer_purity` to `rules/maintain-layer-purity.md`, confirm `scanners/typescript/layer_purity_scanner.py` (or the language-appropriate path) exists and exits with a sensible code.

  **Example (pass):** `rules/maintain-layer-purity.md` opens with frontmatter `scanner: layer_purity_scanner` and the file `scanners/typescript/layer_purity_scanner.py` exists and contains a `main()` function.

- For rules that **should** have a scanner but don't yet, leave the frontmatter clean (no `scanner:` line) and add a body line `**Scanner:** Manual review (TODO: write scanners/<stem>-scanner.py).`

  **Example (pass):** `rules/keep-application-unaware-of-cache.md` body line reads `**Scanner:** Manual review (TODO: write scanners/python/cache_unawareness_scanner.py).` — the maintainer can grep for `TODO: write scanners` to find work.

- Run the bundle script after adding or removing a `scanner:` field so the inlined block in `SKILL.md` stays in sync.

  **Example (pass):** After adding the scanner field, `python skill-builder/skills/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root engineering/skills/<arch>-technical-architecture` is run, and the inlined rule block now shows the new line.

###### DO NOT

- Add `scanner: layer_purity` to a rule when no `layer_purity_scanner.py` exists.

  **Example (fail):** `rules/maintain-layer-purity.md` declares `scanner: layer_purity` but `scanners/` is empty. Running `run_scanners.py` fails with "scanner stem not found".

- Rename a scanner script without updating the YAML field.

  **Example (fail):** `scanners/python/cache_scanner.py` is renamed to `cache_awareness_scanner.py`; the rule still declares `scanner: cache_scanner`. The scanner runs zero rules.

- Use one `scanner:` stem for unrelated rules to look more "covered" than the skill actually is.

  **Example (fail):** Both `rules/maintain-layer-purity.md` and `rules/handle-errors-at-boundary.md` declare `scanner: layer_purity`. The error-handling rule is not really enforced; the field is decoration.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); aligns with `skill-md-bundle-matches-rules-md-files-scanner-stem-matches-py-filename` bundled in `abd-author-practice-skill`.

##### Rule: Generated templates cover every file in the reference's File Structure, with filled examples

The generated skill must ship a `templates/` set such that **every file path** named in the reference's mechanism `File Structure` blocks appears in **at least one** template entry, with a filled mini-example (not just placeholders) showing what that file looks like when correctly implemented. The filled examples are the audience contract: a practitioner reading the template should see runnable code, not headings and `{{TOKENS}}`. Passing means a reviewer can take any file path from the reference, search the templates, and find a worked example. Failing means a file from the reference has no template entry, or every entry is empty scaffolding.

###### DO

- For each mechanism, list every file path from its `File Structure` block in `templates/domain-module.template.txt` (or per-tier templates) and attach a filled mini-example to each.

  **Example (pass):** Reference's Persistence mechanism File Structure lists `packages/<domain>/server/mongo-recipients.repository.ts`. The template entry for that path shows a complete, compilable `MongoRecipientsRepository` class with constructor, `findAll`, `findByIds`, `findByEnterprise` methods — not just method stubs.

- Make filled examples runnable in isolation as much as possible — they double as smoke tests when the generated skill is invoked.

  **Example (pass):** The filled `RecipientStatus.ts` example in the template compiles standalone with `tsc --noEmit` against a minimal `tsconfig.json`; no missing import surprises.

- Cite the source mechanism above each filled example.

  **Example (pass):** Above the `RecipientStatus.ts` example, a comment line reads: `// Pattern: Value Object (Persistence mechanism, inputs/architecture-reference.md).`

###### DO NOT

- Ship a template entry whose body is `## TODO` or a bare `{{ENTITY_NAME}}` placeholder for files the reference explicitly lists.

  **Example (fail):** Template entry for `recipients.repository.ts` has body: `export class {{ENTITY}}Repository {}` and nothing else. The reader has no idea what `findAll` should look like.

- Skip files the reference names because they are "language-specific" or "framework-specific" and rely on the implementer to fill them in from memory.

  **Example (fail):** Reference's File Structure names `index.ts` and `package.json` for each tier. The template ships only the `.ts` source files; `index.ts` and `package.json` are missing. The generated skill quietly produces broken packages.

- Provide a template whose filled example contradicts the reference's named pattern.

  **Example (fail):** Reference's pattern is `Result<T, DomainException>`. The filled example in the template throws raw `Error` and uses `try/catch`. Future generated code copies the wrong pattern.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); aligns with the `templates-include-ideal-filled-examples-for-audience` rule bundled in `abd-author-practice-skill`.
<!-- execute_rules:bundle_rules:end -->
