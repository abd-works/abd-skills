# Golden Pass Fixture — pml-midtier Architecture Specification

This fixture is the canonical example of a passing architecture-specification
artefact set produced by `abd-architecture-specification`. Every rule in
`rules/` must report **clean** against every file in this fixture.

## What's here

- `docs/architecture/specification/architecture-specification.md`
  The main spec. Short — entry-point + mechanism one-liners + package context
  list + source layout + instantiating-the-domain commentary + testing pointer.
- `src/entities/architecture-context.md`
  **Mechanism-tier** context file. Full template: principles, file structure,
  participants, flow, walkthrough.
- `src/services/Zendesk/architecture-context.md`
  **Package-tier** context file. Functional area with enough complexity to
  document its purpose, usage, and downstream consumers in detail.
- `src/services/Logger/architecture-context.md`
  **Miscellaneous-tier** context file. One sentence describing what it is.
- `src/helpers/architecture-context.md`
  **Miscellaneous-tier** grab-bag. Flat list of utilities with one-liner each;
  flags legacy entries explicitly.

## Why this exists

Sourced from the real `paradise-mobile/pml-midtier` repo on 2026-06-30 after
the documentation rewrite that established the new shape. Any change to the
template or rules must continue to validate this fixture clean; if it doesn't,
either the rule is wrong or the fixture needs updating to reflect a real
architectural improvement.

## Minor divergences from the live file

The live `pml-midtier/docs/architecture/specification/architecture-specification.md`
at the time of capture had two cosmetic issues that the fixture corrects so it
can serve as the canonical pass example:

1. The first H2 was `## Grilling Qestions -- What Technology Should This Feature
   Touch?` (typo + draft name). The fixture renames it to the canonical
   `## Where to Start -- What Does This Feature Touch?` per the
   `opens-with-where-to-start-table` rule.
2. The intro paragraph under that H2 had drafting typos
   ("archiecture", "undersatand"). The fixture rewrites it to a clean
   two-paragraph intro that matches the template guidance.

If the live file is later updated to the canonical naming, re-syncing the
fixture from disk should produce a no-op diff.
