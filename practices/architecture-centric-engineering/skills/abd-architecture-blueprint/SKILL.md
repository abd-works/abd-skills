---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-architecture-blueprint
catalogue_one_liner: >-
  Show what every mechanism and module means in code — so the whole team sees what a change touches.
description: >-
  Name every mechanism's code constraint and every module's scope so the team sees what a change touches. Use when deepening an outline into build-ready architecture.
context-perspective: architecture
context-fidelity:
  - level: discovery
    mode: blueprint
---
# abd-architecture-blueprint

## Purpose

Make architecture legible by naming every mechanism that constrains how code is built, listing every module with its business scope and dependencies, and defining diagrams that show how requests flow through mechanisms at runtime — including test flow.

---

## Output files

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

Generate from all templates in `templates/`, preserving subfolder structure. Write to `docs/architecture/`. Add a `<name>-` prefix to `architecture-blueprint.md` only when disambiguation is needed.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Mechanism code shape** — for each mechanism we're naming, can you describe the concrete constraint it places on code — or is it still just a label? If you can't say what a developer must do differently because of this mechanism, it isn't blueprint-ready.
- **Module boundaries vs. business scope** — are these modules drawn around business capabilities, or are they just reflecting folder structure or framework conventions? What would break if you merged two of them or split one?
- **Runtime flow vs. assumed flow** — when you trace a request through the mechanisms, are you describing how this system actually behaves, or how systems like this typically behave? Where would you be surprised if you watched real traffic?
- **Mechanism overlap** — are any two mechanisms doing the same work at different layers, or is there a gap between them where no mechanism owns the concern? What falls through?
- **Testing tiers vs. team reality** — do the test tiers in this blueprint match how the team actually tests, or are they an idealized model? Which tier is the team least likely to write, and what risk does that leave uncovered?

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what a blueprint is, the platform diagram, modules vs mechanisms, how mechanisms are deepened from the outline (module interactions + platform detail), testing architecture, decision records, and what the blueprint does NOT contain.
- **`reference/examples.md`** — typical blueprint file tree and the shape of a good blueprint.

Also read the project's **`architecture-outline.md`** to obtain the mechanism technology choices, NFR justifications, and guiding principles before starting. The blueprint deepens the outline — it does not re-state or re-decide what the outline recorded.

### 2. Generate

**Step 2a — Produce the platform element-inventory file:**

| Template | Output file |
| --- | --- |
| `templates/platform-architecture-elements.md` | `docs/architecture/platform-architecture-elements.md` |

Fill every section with real names and 1-2 sentence descriptions; no placeholder tokens (`{…}`) should remain.

**Step 2b — Produce the blueprint document:**

| Template | What to produce |
| --- | --- |
| `templates/architecture-blueprint.md` | The blueprint document — scope, platform runtime (diagram + runtime-components table), mechanisms (technology + how modules implement each), architecture flow diagram(s), modules (mechanism-modules + domain modules), testing architecture, and ADR list. |
| `templates/decisions/decision-record.md` | One ADR per blueprint-level decision (module boundaries, test-tier vocabulary, data ownership patterns) under `docs/architecture/decisions/`. Number continues from the outline. |

**Mechanism guidance:** Mechanisms go first — they define the code shapes modules must adopt. For each mechanism:
- Technology and platform (brief)
- 1-2 prose paragraphs: how modules implement or extend the mechanism (the code shape it requires)
- Note if the mechanism also has a concrete module surface (e.g. Security — Identity module)

**Module guidance:** Modules come after mechanisms. Two kinds:
- **Mechanism-modules** — mechanisms that also have a concrete implementation surface; describe their functional behaviour and surface API in 1-2 paragraphs
- **Domain modules** — 1-2 sentence business scope; mechanisms used (list, using *common set* shorthand + module-specific extras); dependencies on other modules

**Diagram workflow:**

1. Seed diagrams: `.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>`
2. Fill `platform-architecture.drawio`, `module-overview.drawio`, and `architecture-flow.drawio` from the element-inventory file and module subsections.
3. Fill `testing-flow.drawio` from the testing architecture tiers.
4. Export PNGs: `.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>`

**Quality bar:** Platform element file fully described. Mechanisms described in prose (code shape each module must adopt). Mechanism-modules described with functional surface. Domain modules described in 1-2 sentences + mechanisms + dependencies. Module diagram has legend for universal mechanisms.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

Also verify diagrams:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Platform element file present** — `platform-architecture-elements.md` under `docs/architecture/`, fully described, no placeholder tokens.
- **Paired drawio for platform** — `platform-architecture.drawio` exists; verify prints PASS.
- **Paired drawio for module overview** — `module-overview.drawio` exists; verify prints PASS.
- **Paired drawio for architecture flow** — `architecture-flow.drawio` exists; mechanism labels visible on diagram.
- **Paired drawio for testing flow** — `testing-flow.drawio` exists; all four tiers (Domain/Application/Integration/E2E) present as columns; entry points blue; real layers green; faked layers yellow.
- **Mechanisms described as code shapes** — each mechanism section has technology + 1-2 prose paragraphs on how modules implement it; no bullet lists of features.
- **Mechanism-modules described with surface** — App Server Bootstrap and Identity (or equivalent) described with functional behaviour and surface in 1-2 paragraphs.
- **Domain modules described in 1-2 sentences** — each domain module has: business scope (1-2 sentences), mechanisms used (universal set via legend + module-specific), and dependencies list.
- **No new mechanisms invented here** — the blueprint deepens outline mechanisms; it does not introduce mechanism technology choices not already in the outline.
- **Bespoke outline mechanisms deepened** — every novel or bespoke mechanism from the outline has a corresponding blueprint subsection.
- **Testing architecture is common-across-the-system** — tiers, boundaries, common doubles, and testing-flow.drawio reference only.
- **ADRs exist on disk** — every blueprint-level ADR cited has a matching file; numbering continues from the outline.
- **No outline-level material re-stated** — no technology stack table, no guiding principles list, no major-systems one-liners, no mechanism technology choice ADRs.
- **No reference-level material** — no code walkthroughs, no sequence diagrams with more than three participants.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
