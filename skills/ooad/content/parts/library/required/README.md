# Required Files — Per-Skill Narrative

This directory contains **required** narrative and identity files that are generated/created when a skill is scaffolded from abd-skill-builder. Unlike `base/` (which is frozen shared norms from abd-skill-builder), files here are **per-skill** and should be authored by the skill maintainer.

## Files

| File | Purpose |
|------|---------|
| **`purpose.md`** | One-paragraph statement of what this skill does (solves which problem) |
| **`outline.md`** | Capability summary: problems this skill solves → capabilities provided. Maps to abd-skill-builder's outline.md structure. |
| **`role.md`** | Who uses this skill and what role they play (e.g., "domain modeler", "skill author", etc.) |
| **`principles.md`** | Operating principles and philosophy that guide the skill's work |
| **`README.md`** | This file |

## How They're Used

These files are **included in AGENTS.md** (the merged instructions) so that when the skill is invoked:

1. **AGENTS.md preamble** extracts key sections from SKILL.md (quick start, workspace capability, how to use)
2. **required/ files** provide deeper context about purpose, role, principles, and capability overview
3. **Phase details** follow (from `content/parts/phases/`)

The files in `required/` are loaded into the full skill bundle so users understand the **why** and **what** before diving into the **how** (which phases/steps to follow).

## Relationship to Other Directories

- **`base/`** — Frozen, normative standards copied from abd-skill-builder (checklist.md, critical-quality-steps.md, rules-and-scanners.md, delivery-modes.md, etc.). Do not edit; refresh from upstream when standards change.
- **`required/`** — Per-skill narrative (this directory). Authored by skill maintainers. Answers "what is this skill?", "who uses it?", "what principles guide it?"
- **`../`** (root library) — Optional extra shards and custom content specific to this skill.

## When to Update

- **purpose.md** — When the skill's goal or scope changes
- **outline.md** — When capabilities are added, removed, or significantly refactored
- **role.md** — When the target user or use case changes
- **principles.md** — When operating philosophy or constraints evolve

## Reference

See `library/base/skill-structure-and-concepts.md` for the overall skill directory layout and how `required/`, `base/`, and skill-specific library files fit together.

See `SKILL.md` at the skill root for discoverable metadata and quick-start examples.
