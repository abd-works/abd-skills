# Generating-skill front matter convention

## Purpose

Every artifact produced by an abd practice skill should carry a `generating-skill` key in its YAML front matter. This makes it trivial for an agent or developer opening the file to identify which skill produced it — and therefore which skill to read before continuing, extending, or correcting the artifact.

## Front matter block

All artifact files produced by abd skills must open with a YAML front matter block that includes `generating-skill` and `type`:

```yaml
---
generating-skill: abd-architecture-blueprint
type: package
fidelity: blueprint
---
```

The value of `generating-skill` is the kebab-case skill identifier — the same name used in the skill's folder under `practices/` and in the deployed `.cursor/skills/` area.

## `type` values

The `type` key describes the architectural role of the documented artifact:

| Value | Meaning |
|---|---|
| `mechanism` | A named, cross-cutting code shape — a pattern other developers follow (e.g. Authentication, Error Handling, System Entity Controllers) |
| `package` | A seam owner with explicit constraints — an integration, service, or entity folder with meaningful surface area and a clear boundary |
| `utility` | A thin shared helper or grab-bag folder — not a primary seam; not a growth target |

The root `src/architecture-context.md` (master system document) carries no `type` — it is the system record itself.

## Standard skill identifiers

| Skill | Identifier |
|---|---|
| Architecture Outline | `abd-architecture-outline` |
| Architecture Blueprint | `abd-architecture-blueprint` |
| Architecture Specification | `abd-architecture-specification` |
| BDD Behavior | `abd-bdd-behavior` |
| BDD Specification | `abd-bdd-specification` |
| Domain Language | `abd-domain-language` |
| Domain Model | `abd-domain-model` |
| Domain Specification | `abd-domain-specification` |
| Story Mapping | `abd-story-mapping` |
| Story Acceptance Criteria | `abd-story-acceptance-criteria` |
| Story Specification | `abd-story-specification` |
| UX Information Architecture | `abd-ux-information-architecture` |
| UX Mockup | `abd-ux-mockup` |
| UX Specification | `abd-ux-specification` |

For skills not listed here, use the folder name under `practices/<family>/skills/`.

## How agents use this

When an agent opens an artifact file, it should check for `generating-skill` in the front matter before doing any work. If the key is present, the agent **must read that skill's full package** (rules, reference, templates) before continuing, extending, or correcting the artifact. The `type` key tells the agent immediately what template applies and what scope of content to expect. This is the fastest path to context without asking the user to explain what was already decided.

If the key is absent (legacy file), the agent should infer the skill from the artifact's filename, location, and fidelity value — then read the inferred skill package before proceeding.

## Agent prompt pattern

A user who opens an `architecture-context.md` and says "I'd like to continue exploring this" is implicitly invoking the skill named in `generating-skill`. The agent should:

1. Read `generating-skill` from the front matter.
2. Read `type` to know which template applies (`mechanism`, `package`, or `utility`).
3. Read the full skill package for that skill (rules, reference, templates) — exactly as the skill-workflow Bootstrap + Read-gates require.
4. Proceed as if the user had explicitly invoked that skill, but with existing artifacts already present (existing-system path, not greenfield).

## Placement

`generating-skill` must be the **first key** in the front matter block, followed immediately by `type`, then `fidelity`. This order ensures agents scanning file headers find role and origin without reading the full front matter.

