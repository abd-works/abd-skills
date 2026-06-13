---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-architecture-blueprint
catalogue_one_liner: >-
  Second-level architecture — platform runtime, deployment topology, components in paragraphs, mechanisms deepened with component interactions and platform detail, data model, testing strategy, and ADRs.
description: >-
  Produce the second-level architecture document after the outline — a blueprint
  that adds platform runtime and deployment topology diagrams (with OS per node
  if more than one), names each architectural component in a paragraph or two,
  deepens every mechanism from the outline with component interactions and
  platform/deployment specifics, shows the data architecture at the entity level,
  captures the common testing strategy, and records decisions. Deep mechanism
  walkthroughs defer to abd-architecture-specification. Use when an outline
  exists and the team needs platform and deployment visibility, component-level
  detail, mechanism depth, data architecture, or preparation for architecture review.
---
# abd-architecture-blueprint

## Purpose

The outline answers "what is this system, what does it commit to mechanistically, and why?" — the blueprint answers "what does it actually run as and what is it made of?". It is the document a tech lead opens to see the full platform runtime, the deployment environments, how components are laid out and interact, and how each mechanism from the outline plays out in terms of specific components, platform infrastructure, and runtime behaviour. When the blueprint is in place, the **architecture reference** can go deep on one mechanism at a time without re-explaining the platform or the component landscape to its reader.

---

## Output files

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**Primary file:** `architecture-blueprint.md`. Add a `<name>-` prefix only when disambiguation is needed.

**Diagram element files** (under `docs/architecture/diagrams/`):
- `platform-architecture-elements.md`
- `deployment-architecture-elements.md`

**Draw.io sources** (under `docs/architecture/diagrams/`):
- `platform-architecture.drawio`
- `deployment-architecture.drawio`
- `component-overview.drawio`
- `entity-relationships.drawio`

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what a blueprint is, the platform and deployment diagrams (new at this level), components vs systems, how mechanisms are deepened from the outline (component interactions + platform/deployment detail), data architecture, testing architecture, decision records, and what the blueprint does NOT contain.
- **`reference/examples.md`** — typical blueprint file tree and the shape of a good blueprint.

Also read the project's **`architecture-outline.md`** to obtain the mechanism technology choices, NFR justifications, and guiding principles before starting. The blueprint deepens the outline — it does not re-state or re-decide what the outline recorded.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Step 2a — Produce the two new element-inventory files first:**

| Template | Output file |
| --- | --- |
| `templates/platform-architecture-elements.md` | `docs/architecture/diagrams/platform-architecture-elements.md` |
| `templates/deployment-architecture-elements.md` | `docs/architecture/diagrams/deployment-architecture-elements.md` |

Fill every section with real names and 1–2 sentence descriptions; no placeholder tokens (`{…}`) should remain. For the deployment file, include an **Operating systems** table when more than one OS image is in use across containers.

**Step 2b — Produce the blueprint document:**

| Template | What to produce |
| --- | --- |
| `templates/architecture-blueprint.md` | The blueprint document — scope, platform runtime (diagram + runtime-components table), deployment topology (diagram + environments table + OS table if needed), components, mechanisms in depth, data architecture, testing architecture, extension (if applicable), and ADR list. |
| `templates/decision-record.md` | One ADR per blueprint-level decision (component boundaries, test-tier vocabulary, data ownership patterns, extension contracts) under `docs/architecture/decisions/`. Number continues from the outline. |

**Mechanism guidance:** For every mechanism named in the outline, produce a blueprint subsection that adds:
- **Participating components** — which named components from section 4 implement or depend on the mechanism
- **Platform / deployment detail** — how the mechanism is configured in the running platform (secrets store, broker endpoint, cache cluster mode, sidecar, OS-level tooling, etc.)
- **Runtime behaviour** — step-by-step description of steady-state operation and key failure modes
- **Component interactions** — how participating components call into each other through the mechanism; what crosses component boundaries and in what direction

**Diagram workflow:**

1. Seed diagrams: `.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>`
2. Fill `platform-architecture.drawio`, `deployment-architecture.drawio`, `component-overview.drawio`, and `entity-relationships.drawio` from the matching element-inventory files and component subsections.
3. Export PNGs: `.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>`
4. Reference the PNGs from sections 2, 3, 4, and 6.

**Quality bar:** Platform and deployment element files fully described. Components described in 1–2 paragraphs. Every mechanism has participating components, platform/deployment detail, runtime behaviour, and component interactions. Data architecture is entity-level. OS table present when multiple OS images are in use.

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

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Platform element file present** — `platform-architecture-elements.md` under `docs/architecture/diagrams/`, fully described, no placeholder tokens.
- **Deployment element file present** — `deployment-architecture-elements.md` under `docs/architecture/diagrams/`, fully described, no placeholder tokens.
- **OS table present when multiple OS images exist** — if more than one container OS image is used, the deployment section includes a named OS/image table with a reason per entry.
- **Paired drawio for platform** — `platform-architecture.drawio` exists; verify prints PASS.
- **Paired drawio for deployment** — `deployment-architecture.drawio` exists; verify prints PASS.
- **Paired drawio for component overview** — `component-overview.drawio` exists; verify prints PASS.
- **Paired drawio for entity relationships** — `entity-relationships.drawio` exists; verify prints PASS.
- **Components in paragraphs, not internals** — every component has 1–2 paragraphs covering purpose, dependencies, and interactions; no class lists, no method tables, no file trees.
- **Component descriptions reference mechanisms** — at least the mechanisms each component participates in are named in the component's interactions paragraph.
- **Every mechanism has all four depth fields** — participating components, platform/deployment detail, runtime behaviour, and component interactions are present for every mechanism; no field is a placeholder.
- **No new mechanisms invented here** — the blueprint deepens outline mechanisms; it does not introduce mechanism technology choices not already in the outline.
- **Bespoke outline mechanisms deepened** — every novel or bespoke mechanism from the outline has a corresponding blueprint subsection at the same depth as the standard set.
- **Data architecture is entity-level** — entity relationship diagram and ownership table; no schemas, no DDL.
- **Testing architecture is common-across-the-system** — tiers, boundaries, common doubles only.
- **Extension section present only when warranted** — no "TBD" placeholder.
- **ADRs exist on disk** — every blueprint-level ADR cited has a matching file; numbering continues from the outline.
- **No outline-level material re-stated** — no technology stack table, no guiding principles list, no major-systems one-liners, no mechanism technology choice ADRs.
- **No reference-level material** — no code walkthroughs, no sequence diagrams with more than three participants.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
