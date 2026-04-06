---
name: abd-ooad
description: >-
  **Object-Oriented Analysis and Design (OOAD) from raw material.** Use this skill whenever you're working with specifications, game manuals, policy docs, messy code, or rule books that need to be modeled as object-oriented domain models. Agile by Design methodology: Steps 0–2 (Domain Scan, Extraction, Refinement) with built-in Draw.io diagram generation via scripts/drawio_cli.py. ALWAYS use this skill when a user provides domain material and asks you to extract domain concepts, build class diagrams, identify responsibilities, or create object models. Create domain-scan-model.md and domain-scan-model.drawio files in the project workspace.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
  capabilities:
    - workspace: "Ability to specify project workspace directory where domain models are created"
    - diagram-templates: "Built-in Draw.io diagram generation via scripts/drawio_cli.py and templates/"
    - actor-registry: "Track domain concepts through lifecycle with UML stereotypes (<<anchor>>, <<candidate>>, <<tension>>)"
---

# Object Oriented Analysis and Design (OOAD)

**Agile by Design — `abd-ooad` skill** for turning raw material (specs, manuals, code, policies) into robust object-oriented domain models.

## Quick Start

The core process is **linear and methodical**: Steps 0 → 1 → 2 (Scan → Extract → Refine).

**Step 0: Domain Scan** — Orientation, not extraction
- Read table of contents / section headings
- Identify 3–7 high-confidence anchors
- Flag suspected tensions/ambiguities
- Create **Actor Registry** to track concepts

**Step 1: Extraction & Validation** — Nouns, verbs, rules, states
- Read carefully for domain concepts
- Build candidate class list
- Validate against key scenarios

**Step 2: Refinement** — Relationships, responsibilities, invariants
- Add relationships and cardinality
- Encode domain rules into model
- Validate with walkthroughs

## Where This Skill Fits

This skill handles **model discovery, initial design, and diagram generation** end-to-end. Diagram tooling is built in:
- `scripts/drawio_cli.py` — create, verify, relayout, fix-edge-styles
- `templates/` — domain model and domain realization templates
- `content/parts/library/` — class diagram and sequence diagram layout rules

## Workspace Capability

When you invoke this skill, **specify the project workspace** where domain models will be created:

```
workspace: /path/to/project/directory
```

This workspace becomes the default location for:
- `domain-scan-model.md` — Step 0 output (source map, anchors, tensions, actor registry)
- `domain-scan-model.drawio` — Step 0 initial class diagram
- `step-1-extraction.md` — Step 1 detailed findings
- Any subsequent step outputs

If no workspace is provided, assume the current working directory.

## How to Use This Skill

**When you have domain material** (specs, manual, code, policy docs) and need to extract an object-oriented model:

1. Provide the **source material** (text, code, spec excerpt, etc.)
2. Specify the **workspace directory** where outputs should be created
3. Ask Claude to "**perform a Step 0 domain scan**" or similar

Claude will then:
- Analyze the material using appropriate technique (spec, code, transcript, expert)
- Create `domain-scan-model.md` with source map, anchors, tensions, actor registry
- Create `domain-scan-model.drawio` with initial class diagram (anchors only)
- Output both files to your workspace

Continue with **Step 1 (Extraction)** and **Step 2 (Refinement)** for deeper modeling.

## Key Output Artifacts

| Step | Markdown | Diagram |
|------|----------|---------|
| Step 0 | `domain-scan-model.md` (source map, anchors, tensions, actor registry) | `domain-scan-model.drawio` (anchor classes only) |
| Step 1 | `step-1-extraction.md` (nouns, verbs, rules, states, candidates) | `step-1-extraction.drawio` (candidates added) |
| Step 2 | `step-2-refined-model.md` (responsibilities, relationships, invariants) | `step-2-refined-model.drawio` (full class diagram) |

Always maintain **both** Markdown and diagram side-by-side; keep them synchronized as you refine.

## Complete OOAD Methodology

For the full 20-step walkthrough with detailed techniques, worked examples, ASCII diagram notation, and battle-tested patterns, see **`content/parts/process.md`**.

For Step 0 details by source type (specification, codebase, transcript, domain expert), see **`content/parts/domain-scan.md`**.

For diagram CLI usage and layout rules, see **`content/parts/library/using-diagram-cli.md`**.
