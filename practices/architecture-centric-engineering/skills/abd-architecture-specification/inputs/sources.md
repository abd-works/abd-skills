# Sources this skill consumes

This skill produces a reference document by joining two kinds of input: **architecture context** (what the layers are, what mechanisms are in play) and **code/test standards** (the project's coding standard and testing standard, which the walkthrough samples must obey). The skill does **not** assume any specific sibling skill is present — it asks for the *information*, and uses whichever sources the project actually has in scope.

## Required architecture context

| Information needed | Common sources |
|---|---|
| **Architecture flow** — one interaction end-to-end; diagram + `\| Tech \| File \| Instantiates from domain \|` table. Tech-specific. | Named spec (`specs/<arch>/architecture-specification.md`), layered description doc, ADR, or sibling skill output. |
| **Instantiating the Domain** — how domain classes and operations become code; module layout; naming contract. **Common to all specs.** | Domain model, domain language, or domain specification from the engagement; named spec section when assigning. |
| **Mechanism list** — tech-specific runtime concerns (e.g. Web Client, App Server, Persistence for MERN). One mechanism section per entry. | Architecture blueprint, mechanism inventory, or named spec. |

## Required code and test standards

| Information needed | Common sources |
|---|---|
| **Coding standard** — the conventions every production-code snippet in a walkthrough must follow. | Whatever the project has in scope: a style guide, an ESLint/Prettier config, a `CLAUDE.md` block, or **`abd-clean-code`** when that skill is in scope (default in agilebydesign-skills-anchored projects). |
| **Testing standard** — the conventions every test snippet in a walkthrough must follow. | Whatever the project has in scope: a test-style guide, the team's existing test patterns, or **`abd-story-acceptance-test`** when that skill is in scope (default in agilebydesign-skills-anchored projects). |

## Worked example

The shape of a finished reference is shown by the **filled illustrative example block at the bottom of [`templates/architecture-specification.md`](../templates/architecture-specification.md)** — a worked Error Handling mechanism complete with principles, file structure, participants, flow, walkthrough, and a tested fragment. Read it once before authoring new sections so the shape stays consistent. The skill keeps this example **inside the template** so the skill is self-contained and does not depend on any other repository or sibling skill being present.

The **runnable module shape** for the template slice is in [`reference/example.ts`](../reference/example.ts) — all template files merged into one parameterized TypeScript file (shared, server, client tiers). The AI Garden catalog uses this file as the skill hero preview, not a class diagram.

## Outputs

The reference document this skill produces is **not** stored under this skill. It is written into the **target project** (or under the implementation skill that will consume it) as a single file:

- `architecture-specification.md` (or legacy `architecture-specification.md`) — always one file. The mechanisms inside it are organized in one of two ways (combined section vs one section per mechanism) depending on count, per the `section-organization-matches-mechanism-count` rule.

**Template outputs** (same deliverables folder or `specs/<arch>/template/`):

| Output | Skill shape |
|--------|-------------|
| Runnable code under `template/` or `specs/<arch>/template/packages/` | This skill + coding/testing standards |
| `specification-by-example.md` | `abd-story-specification` |
| `domain-spec.md` | `abd-domain-specification` |

**Validation** (when template code is created or edited):

| Pass | Command target |
|------|----------------|
| Doc rules | `abd-architecture-specification/rules/` → specification document |
| Template rules + scanners | `specs/<arch>/rules/` + `run_scanners.py --skill-root specs/<arch> --workspace <template-root>` |

New named specs must ship with `rules/` and `scanners/` (copy from an existing spec such as `specs/mern/` when the stack matches). The template slice is not done until scanners pass.
