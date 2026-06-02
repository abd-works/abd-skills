# E2E skill fixtures

Pre-baked, **valid-but-minimal** deliverables for every skill on the `pawplace-stubs` kanban rails.

Content is trimmed from [abd-pet-store-demo](https://github.com/agilebydesign/abd-pet-store-demo) Increment 1 (walk-in driver).

**Scatter shape:** 3 partition modules → 4 increments in `abd-thin-slicing.md` (2 in module 1). Shaping complete on `project-all` scatters to `1-product-catalog`, `2-store-operations`, `3-checkout-and-fulfillment`. Discovery complete on a partition ticket scatters to increment tickets per module section.

## Usage

1. Reset workspace: `scripts/reset-e2e-fixture.ps1 -Fixture pawplace-stubs`
2. Point board UI planning root at `tests/e2e/data/pawplace-stubs/docs/planning`
3. Spawn kanban agents — they copy from here via `skill-fixtures.json` and mark done without running skills

## Files

| File | Skill |
| --- | --- |
| `abd-story-mapping-*.md` | Story map (shaping outline + discovery full) |
| `story-graph-*.json` | Graph at outline / increments / AC / scenarios fidelity |
| `abd-thin-slicing.md` | Increments |
| `sprint-groupings.md` | Sprint scatter |
| `abd-domain-terms.md` | Domain |
| `abd-ubiquitous-language.md` | Domain (exploration) |
| `abd-acceptance-criteria.md` | Stories + AC |
| `abd-ux-mockup.md` | UX |
| `abd-information-architecture.md` | UX (discovery) |
| `abd-architecture-*.md` | Architecture (outline, blueprint, template, reference) |
| `abd-class-responsibility-collaborator.md` | CRC |
| `abd-specification-by-example.md` | Spec by example |
| `abd-interface-design.md` | Interface design |
| `abd-object-model.md` | Object model |
| `abd-acceptance-test-driven-development.py` | ATDD stub |
| `abd-clean-code-product_catalog.py` | Clean code stub |
