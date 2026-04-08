# OOAD Capability Summary

The `abd-ooad` skill provides a structured, multi-step pipeline for Object-Oriented Analysis and Design (OOAD). It transforms unstructured domain material (specifications, transcripts, codebases) into rigorous, validated domain models.

```text
skill: abd-ooad
Entry point — domain modeling skill (SKILL.md) and assembled OOAD instructions (AGENTS.md)
│
│   Raw domain material with no clear structure; unclear what concepts exist
├── ┌─────────────────────────────────────────────────────┐
│   │  Domain Scan                                        │
│   │  Orientation and anchor module identification       │
│   │  Produces: Source map, anchors, tensions, sketch    │
│   └─────────────────────────────────────────────────────┘
│
│   Need to find entities, values, processes, and rules
├── ┌─────────────────────────────────────────────────────┐
│   │  Extraction (Nouns, Verbs, Rules, States)           │
│   │  Careful extraction from source material            │
│   │  Produces: Raw candidate list and Term Registry     │
│   └─────────────────────────────────────────────────────┘
│
│   Need to shape raw candidates into a cohesive model
├── ┌─────────────────────────────────────────────────────┐
│   │  Refinement (15+ focused passes)                    │
│   │  Thing vs data, responsibilities before operations, │
│   │  composition over inheritance, state transitions    │
│   │  Produces: Refined class structures and boundaries  │
│   └─────────────────────────────────────────────────────┘
│
│   Need to ensure the model actually solves the problem
└── ┌─────────────────────────────────────────────────────┐
    │  Validation & Finalization                          │
    │  Validate with scenarios, refine names, model in    │
    │  layers (domain, application, infrastructure)       │
    │  Produces: Final domain-model.md and .drawio        │
    └─────────────────────────────────────────────────────┘
```

## Core Capabilities

### 1. Phased Extraction and Refinement
**Problem:** Attempting to extract classes, attributes, methods, and relationships all at once leads to superficial models that miss core domain tension.
**Solution:** A pipeline that separates concerns. It forces the AI to identify responsibilities before operations, separate independent entities from data about a thing, and enforce invariants before drawing relationships.

### 2. Term Registry Management
**Problem:** Inconsistent naming and lost concepts across modeling sessions.
**Solution:** The skill maintains a `term-registry.md` that tracks every concept from raw extraction through to final classification (anchor, candidate, property, discarded) with explicit confidence levels.

### 3. Diagram Generation and Sync
**Problem:** Text models and visual diagrams drift out of sync.
**Solution:** The skill integrates with `drawio_cli.py` to generate, layout, and validate `.drawio` diagrams directly from the Markdown model. It enforces strict layout rules (e.g., core classes inside anchor module frames).

### 4. Scenario Validation
**Problem:** Models look elegant but fail when applied to actual use cases.
**Solution:** The pipeline concludes with scenario walkthroughs, testing the structural model against behavioral requirements to ensure responsibilities are correctly assigned and state transitions are valid.

## Pipeline Architecture

This skill utilizes the standard layout pattern:
- **`SKILL.md`**: Entry point and quick start.
- **`process.md`**: The ordered pipeline of phases.
- **`content/parts/phases/`**: Granular instructions for each step.
- **`scripts/base/build.py`**: Compiles the granular phases into the unified `AGENTS.md` and `content/built/` artifacts.
- **`scripts/base/generate.py`**: Delivers instructions for a single phase on demand to keep the AI focused.
