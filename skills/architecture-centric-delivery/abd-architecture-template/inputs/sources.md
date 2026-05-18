# Sources this skill consumes

This skill produces a reference document by joining two kinds of input: **architecture context** (what the layers are, what mechanisms are in play) and **code/test standards** (the project's coding standard and testing standard, which the walkthrough samples must obey). The skill does **not** assume any specific sibling skill is present — it asks for the *information*, and uses whichever sources the project actually has in scope.

## Required architecture context

| Information needed | Common sources |
|---|---|
| **Architecture layers** — layer names, tech per layer, responsibility per layer, the layer-stack diagram. Copied (or summarized) into the reference document's **Architecture Layers** section; names must match. | A layered description doc, an ADR, a wiki page, or the output of a sibling skill such as **`abd-architecture-description`** when it is in scope. |
| **Mechanism list** — the list of mechanisms in scope for this architecture (e.g. error handling, caching, persistence, validation, auth, messaging, observability) with a one-line statement of intent for each. One mechanism section per entry. | A mechanism inventory doc, an architecture playbook, or the output of a sibling skill such as **`abd-architecture-mechanisms`** when it is in scope. |

## Required code and test standards

| Information needed | Common sources |
|---|---|
| **Coding standard** — the conventions every production-code snippet in a walkthrough must follow. | Whatever the project has in scope: a style guide, an ESLint/Prettier config, a `CLAUDE.md` block, or **`abd-clean-code`** when that skill is in scope (default in agilebydesign-skills-anchored projects). |
| **Testing standard** — the conventions every test snippet in a walkthrough must follow. | Whatever the project has in scope: a test-style guide, the team's existing test patterns, or **`abd-acceptance-test-driven-development`** when that skill is in scope (default in agilebydesign-skills-anchored projects). |

## Worked example

The shape of a finished reference is shown by the **filled illustrative example block at the bottom of [`templates/architecture-reference.md`](../templates/architecture-reference.md)** — a worked Error Handling mechanism complete with principles, file structure, participants, flow, walkthrough, and a tested fragment. Read it once before authoring new sections so the shape stays consistent. The skill keeps this example **inside the template** so the skill is self-contained and does not depend on any other repository or sibling skill being present.

## Outputs

The reference document this skill produces is **not** stored under this skill. It is written into the **target project** (or under the implementation skill that will consume it) as a single file:

- `inputs/architecture-reference.md` — always one file. The mechanisms inside it are organized in one of two ways (combined section vs one section per mechanism) depending on count, per the `section-organization-matches-mechanism-count` rule.
