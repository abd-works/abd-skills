---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-architecture-blueprint
catalogue_one_liner: >-
  Describe every mechanism as a code shape and every module as a business area so the whole team can see what a change touches.
description: >-
  Give every mechanism and module an explicit code shape and surface so the whole team can see what a system change touches.
---
# abd-architecture-blueprint

## Purpose

Architecture documents often describe what a system is without saying what it means to write code against it. This skill makes architecture legible for the whole team: every mechanism names the constraint it places on code, every module states its business scope and dependencies, diagrams show how requests flow through the mechanisms at runtime, and the testing flow diagram shows which layers each test tier actually exercises.

---

## Output files

**Deliverables folder:** see `../agent-protocol.md` ? Output file resolution.

**Primary file:** `architecture-blueprint.md`. Add a `<name>-` prefix only when disambiguation is needed.

**Diagram element files** (under `docs/architecture/`):
- `platform-architecture-elements.md`


**Draw.io sources** (under `docs/architecture/`):
- `platform-architecture.drawio`
- `module-overview.drawio`
- `architecture-flow.drawio`
- `testing-flow.drawio`

---

## Agent Instructions

> **MANDATORY ? read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** ? what a blueprint is, the platform diagram, modules vs mechanisms, how mechanisms are deepened from the outline (module interactions + platform detail), testing architecture, decision records, and what the blueprint does NOT contain.
- **`reference/examples.md`** ? typical blueprint file tree and the shape of a good blueprint.

Also read the project's **`architecture-outline.md`** to obtain the mechanism technology choices, NFR justifications, and guiding principles before starting. The blueprint deepens the outline ? it does not re-state or re-decide what the outline recorded.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Step 2a ? Produce the platform element-inventory file:**

| Template | Output file |
| --- | --- |
| `templates/platform-architecture-elements.md` | `docs/architecture/platform-architecture-elements.md` |

Fill every section with real names and 1?2 sentence descriptions; no placeholder tokens (`{?}`) should remain.

**Step 2b ? Produce the blueprint document:**

| Template | What to produce |
| --- | --- |
| `templates/architecture-blueprint.md` | The blueprint document ? scope, platform runtime (diagram + runtime-components table), mechanisms (technology + how modules implement each), architecture flow diagram(s), modules (mechanism-modules + domain modules), testing architecture, and ADR list. |
| `templates/decision-record.md` | One ADR per blueprint-level decision (module boundaries, test-tier vocabulary, data ownership patterns) under `docs/architecture/decisions/`. Number continues from the outline. |

**Mechanism guidance:** Mechanisms go first ? they define the code shapes modules must adopt. For each mechanism:
- Technology and platform (brief)
- 1?2 prose paragraphs: how modules implement or extend the mechanism (the code shape it requires)
- Note if the mechanism also has a concrete module surface (e.g. Security ? Identity module)

**Module guidance:** Modules come after mechanisms. Two kinds:
- **Mechanism-modules** ? mechanisms that also have a concrete implementation surface; describe their functional behaviour and surface API in 1?2 paragraphs
- **Domain modules** ? 1?2 sentence business scope; mechanisms used (list, using *common set* shorthand + module-specific extras); dependencies on other modules

**Diagram workflow:**

1. Seed diagrams: `.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>`
2. Fill `platform-architecture.drawio`, `module-overview.drawio`, and `architecture-flow.drawio` from the element-inventory file and module subsections.
3. Fill `testing-flow.drawio` from the testing architecture tiers.
4. Export PNGs: `.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>`

**Quality bar:** Platform element file fully described. Mechanisms described in prose (code shape each module must adopt). Mechanism-modules described with functional surface. Domain modules described in 1?2 sentences + mechanisms + dependencies. Module diagram has legend for universal mechanisms.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-architecture-blueprint \
  --workspace <path-to-output>
```

Then verify diagrams:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built ? read the artifacts as reviewers.

- **Platform element file present** ? `platform-architecture-elements.md` under `docs/architecture/`, fully described, no placeholder tokens.
- **Paired drawio for platform** ? `platform-architecture.drawio` exists; verify prints PASS.
- **Paired drawio for module overview** ? `module-overview.drawio` exists; verify prints PASS.
- **Paired drawio for architecture flow** ? `architecture-flow.drawio` exists; mechanism labels visible on diagram.
- **Paired drawio for testing flow** ? `testing-flow.drawio` exists; all four tiers (Domain/Application/Integration/E2E) present as columns; entry points blue; real layers green; faked layers yellow.
- **Mechanisms described as code shapes** ? each mechanism section has technology + 1?2 prose paragraphs on how modules implement it; no bullet lists of features.
- **Mechanism-modules described with surface** ? App Server Bootstrap and Identity (or equivalent) described with functional behaviour and surface in 1?2 paragraphs.
- **Domain modules described in 1?2 sentences** ? each domain module has: business scope (1?2 sentences), mechanisms used (universal set via legend + module-specific), and dependencies list.
- **No new mechanisms invented here** ? the blueprint deepens outline mechanisms; it does not introduce mechanism technology choices not already in the outline.
- **Bespoke outline mechanisms deepened** ? every novel or bespoke mechanism from the outline has a corresponding blueprint subsection.
- **Testing architecture is common-across-the-system** ? tiers, boundaries, common doubles, and testing-flow.drawio reference only.
- **ADRs exist on disk** ? every blueprint-level ADR cited has a matching file; numbering continues from the outline.
- **No outline-level material re-stated** ? no technology stack table, no guiding principles list, no major-systems one-liners, no mechanism technology choice ADRs.
- **No reference-level material** ? no code walkthroughs, no sequence diagrams with more than three participants.
- **No bundle markers** ? `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
