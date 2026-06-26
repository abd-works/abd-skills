---
catalog_garden_tier: practice
catalog_garden_order: 10
name: abd-architecture-outline
catalogue_one_liner: >-
  First architecture artifact — system context diagram with functions and tech per system, mechanisms catalogue with tech choices and NFR justifications, and guiding principles.
description: >-
  Produce the first shared canonical picture of a system — system context, mechanisms catalogue, principles, and decisions. Use when starting architecture on a new or unfamiliar system, onboarding, or preparing for review.
context-perspective: architecture
context-fidelity:
  - level: shaping
    mode: system-context
---
# abd-architecture-outline

## Purpose

Establish the shared canonical picture of a system — what systems exist, how they connect, what mechanisms govern cross-cutting behavior, and what principles guide decisions — so the team starts deeper architecture work from agreed facts, not assumptions.

---

## Output files

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

Generate from all templates in `templates/`, preserving subfolder structure. Write to `docs/architecture/diagrams/`. Add a `<name>-` prefix to `architecture-outline.md` only when disambiguation is needed.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **System identity** — when someone says "the system," do all stakeholders picture the same boundary? What gets left out when you draw the box, and what gets accidentally included?
- **Hidden neighbors** — are there systems, services, or manual processes that interact with this system that nobody has mentioned yet? The ones that surface during integration are the ones nobody named during shaping.
- **Mechanism relevance** — which cross-cutting concerns actually matter here, and which are you including because they're "standard"? A mechanism that doesn't serve a real NFR adds complexity without value.
- **Connection assumptions** — for each arrow between systems, do you know the protocol, who initiates, and what happens when the other side is unavailable? Or are those details being deferred without anyone tracking the deferral?
- **Principles vs. preferences** — can each guiding principle be applied to a real code decision with a clear yes-or-no answer, or is it a sentiment that sounds wise but doesn't constrain anything?
- **What's deliberately excluded** — what have you decided is out of scope for this outline, and does the team agree it's out of scope — or are they assuming someone else is covering it?

---

## Diagram workflow

Produces `docs/architecture/diagrams/system-context.drawio`. Must exist and verify PASS before the cell is marked done.

```powershell
# 1. Seed — creates system-context.drawio under docs/architecture/diagrams/
.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>

# 2. Fill system-context.drawio with real names from system-context-elements.md (edit the seeded file)

# 3. Export PNG
.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>

# 4. Verify — must print PASS
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an outline is, the system context diagram, the extended system-context scope (functions + tech + protocols), the mechanisms catalogue concept, guiding principles, major systems catalogue, and decision records.
- **`reference/system-context.md`** — deeper guidance on the system context diagram.

### 2. Generate

**Step 2a — Produce the element-inventory file first:**

Using `templates/system-context-elements.md` as the starting structure, fill in every section with real system names and 1–2 sentence descriptions. No placeholder tokens (`{…}`) should remain.

For the **system-context** file: add **Major functions** and **Platform technology** (app stack, persistence, tools/libs) to every owned system entry; add **Protocol** to every relationship entry.

Complete the element file before proceeding to step 2b.

| Template | Output file |
| --- | --- |
| `templates/system-context-elements.md` | `docs/architecture/diagrams/system-context-elements.md` |

**Step 2b — Produce the draw.io source and outline document:**

Only after the element file is complete:

| Template | What to produce |
| --- | --- |
| `templates/architecture-outline.md` | The outline document — a System Context section describing each owned system, an Architecture Mechanisms section with tech-choice + NFR justification per mechanism, guiding principles, tech stack table, major systems table, and ADR list. |
| `templates/decisions/decision-record.md` | One ADR file per outline-level decision (platform, architectural style, each mechanism technology choice) under `docs/architecture/decisions/`. |

**Mechanism guidance:** Cover all eight standard mechanisms (Security, Error Handling & Resilience, Logging & Observability, Validation, Configuration & Secrets, Caching, Persistence, Communication). Then identify any context-specific or bespoke mechanisms this system requires that the standard set does not cover and add them as additional subsections. Do not leave any mechanism empty or placeholder; derive real choices from the project context.

**Diagram workflow:**

1. Seed diagram: `.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>`
2. Fill placeholders in `system-context.drawio` using the element-inventory file as the source of truth.
3. Export PNG: `.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>`
4. Reference the PNG and link the element file from the outline markdown.

**Quality bar:** Element-inventory file present and fully described (no placeholder tokens). System context element file includes functions + platform tech per system and protocol per relationship. Diagram present and matching its element file, accompanied by a caption of three sentences or fewer. Every mechanism has a named technology choice and NFR justification. ADRs on disk for all mechanism choices and platform decisions.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

Also verify diagram:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Element-inventory file present** — `system-context-elements.md` — under `docs/architecture/diagrams/`.
- **Every element has a 1–2 sentence description** — no entry has a blank body, a single-word body, or an unfilled placeholder token.
- **System context element file has functions + tech per system** — every owned system entry has a `**Major functions:**` list and a `**Platform technology:**` block with app stack, persistence, and tools.
- **System context element file has protocol per relationship** — every relationship entry includes a `**Protocol:**` line.
- **Element file and diagram are in sync** — every element named in the element file appears in the `.drawio`; no element is in the diagram without a file entry.
- **System context diagram present** — with a caption of three sentences or fewer.
- **No separate platform-architecture, layered-architecture, or deployment-architecture diagram** — those live in the blueprint; no `layered-architecture.drawio`, `platform-architecture.drawio`, `deployment-architecture.drawio` or their element files at this level.
- **Diagram has a paired `.drawio` source** — `.\scripts\arch-drawio.ps1 verify` prints PASS.
- **Diagram section in the outline links its element file** — `> Element inventory: [diagrams/system-context-elements.md](…)` is present under the diagram reference.
- **Canonical filename used** — `system-context.drawio`.
- **Systems section present** — the outline describes every owned system with functions and tech; content mirrors the system-context-elements.md.
- **Mechanisms section present** — all eight standard mechanisms have a named technology choice, 1–2 paragraphs, and an NFR or justification sentence.
- **Bespoke mechanisms present when context demands** — at least one novel mechanism added if the standard set does not fully cover the system's concerns.
- **ADRs exist on disk for mechanism choices** — every mechanism technology choice that warranted a decision has a matching ADR file under `docs/architecture/decisions/`.
- **Principles are decidable** — every principle is one sentence and could be applied to a real code change.
- **Technology stack is a table** — Layer / Technology / Version / Purpose; no narrative paragraphs.
- **Major systems are one line each** — no internal component descriptions.
- **No deployment or platform runtime detail** — no infrastructure nodes, no container instances, no CDN or load-balancer specifics — those live in the blueprint.
- **No data model** — entity relationships and persistence schemas are absent.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
