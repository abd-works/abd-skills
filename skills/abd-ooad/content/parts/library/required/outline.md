# Capability Summary

Skills built with abd-ooad (or skills that adopt capabilities from abd-ooad) will be able to solve the following problems with the following capabilities.

```
skill: abd-ooad
Entry point — domain modeling skill (SKILL.md) and assembled OOAD instructions (AGENTS.md)
│
│   raw domain material with no clear structure; unclear what concepts exist
├── ┌─────────────────────────────────────────────────────┐
│   │  Workspace Configuration                            │
│   │  skill-config.json + set_workspace.py               │
│   │  Route all domain models to correct project         │
│   └─────────────────────────────────────────────────────┘
│
│   no roadmap through 24 OOAD phases; people don't know what step to take next
├── ┌─────────────────────────────────────────────────────┐
│   │  Phases and Process Files                           │
│   │  process.md + phases/<phase>.md (24 steps)          │
│   │  Ordered methodology: Scan → Extract → Refine       │
│   └─────────────────────────────────────────────────────┘
│
│   losing track of which phase we're in; steps get skipped or repeated
├── ┌─────────────────────────────────────────────────────┐
│   │  Activity Checklists                                │
│   │  process-checklist.md + per-phase checklists        │
│   │  Track progress through the pipeline                │
│   └─────────────────────────────────────────────────────┘
│
│   guidance buried in huge documents; AI instruction loses focus
├── ┌─────────────────────────────────────────────────────┐
│   │  Build from Parts                                   │
│   │  Library + phases + rules → assemble AGENTS.md      │
│   │  Phase-scoped prompts for focused work              │
│   └─────────────────────────────────────────────────────┘
│
│   hard to maintain cross-cutting guidance; standards drift
├── ┌─────────────────────────────────────────────────────┐
│   │  Rules and Scanners                                 │
│   │  content/parts/library/ standards + validation      │
│   │  Enforce domain rules, catch model violations       │
│   └─────────────────────────────────────────────────────┘
│
│   domain model artifacts have inconsistent structure; hard to consume downstream
├── ┌─────────────────────────────────────────────────────┐
│   │  Templates                                          │
│   │  Markdown shapes for scan, extraction, refinement output  │
│   │  Consistent artifact format across sessions         │
│   └─────────────────────────────────────────────────────┘
│
│   changes to phases or rules break past work without automated proof
└── ┌─────────────────────────────────────────────────────┐
    │  Tests                                              │
    │  Pytest suites and fixtures                         │
    │  Validate skill structure and build pipeline        │
    └─────────────────────────────────────────────────────┘
```

---

## Adopted Capabilities (from abd-skill-builder)

### ✓ Workspace and Configuration

**Problem:** Domain models written to wrong project directory; paths ambiguous between skill install and workspace.

**Solution:** `skill-config.json` stores `active_skill_workspace` (project root). `scripts/base/set_workspace.py` manages workspace routing. All outputs go to `<workspace>/abd-ooad/`.

**Reference:** `library/base/workspace-and-config.md`, `content/parts/phases/workspace-and-config.md`, `scripts/base/set_workspace.py`.

---

### ✓ Skill Structure Standards

**Problem:** No consistent layout for domain modeling skills; hard to audit or extend.

**Solution:** SKILL.md, skill-config.json, content/parts/, library/, phases/, scripts/ follow abd-skill-builder directory standards. Every skill has this shape.

**Reference:** `library/base/skill-structure-and-concepts.md`, this file structure.

---

## Partially Implemented Capabilities (to be fully adopted)

### ⏳ Phases and Process Files

**Status:** Implemented but build system is simplified (not yet full abd-skill-builder pattern).

**Problem:** No visible pipeline; unclear what order phases run and what each does.

**Solution:** `process.md` defines ordered pipeline (24 rows, one per phase). Each phase links to `phases/<slug>.md` with inputs, outputs, procedure.

**Current Gap:** Build system doesn't yet use ContentAssembler, scanners, or explicit build pipeline from abd-skill-builder. Will enhance.

**Reference:** `content/parts/process.md`, `content/parts/phases/`, `skill-config.json` → `phase_files`.

---

### ⏳ Activity Checklists

**Status:** Template structure in place; progress files generated at runtime.

**Problem:** No shared place to track "where are we in the 24 phases?"; steps skipped or repeated.

**Solution:** `process.md` drives creation of `<workspace>/abd-ooad/progress/process-checklist.md` (overall pipeline). Each phase may have `## Action Checklist` section; live copy written to `progress/<phase>-checklist.md`.

**Current:** Implemented implicitly; not yet using generate.py fully.

**Reference:** `library/base/checklist.md`, `scripts/base/generate.py`.

---

### ⏳ Build from Parts

**Status:** Implemented (build.py, library organization) but simplified vs abd-skill-builder.

**Problem:** Monolithic instructions hard to maintain; AI loses focus over huge prompts.

**Solution:** Authors edit `content/parts/` (process.md, library/, phases/). `build.py` merges into `AGENTS.md`. `generate.py` returns one phase per session. Extract from SKILL.md into AGENTS.md preamble.

**Current:** Working but needs full abd-skill-builder pattern (merge order, scanners, pipeline).

**Reference:** `scripts/base/build.py`, `scripts/base/generate.py`, `AGENTS.md` (generated).

---

### ⏳ Rules and Scanners

**Status:** Structure exists; no scanners yet.

**Problem:** Silent violations; output looks right but breaks model structure.

**Solution:** `rules/` holds normative prose. `rules/scanners.json` binds scanner scripts. `build.py` runs post-merge scanners.

**Current:** Rules directory structure exists, but no scanner scripts yet implemented.

**Reference:** `rules/`, `skill-config.json` → `build.scanners`.

---

## Not Yet Adopted (Ready for Future Work)

### ⏹ Templates

**Purpose:** Standardize shape of scan, extraction, and refinement outputs.

**Example:** domain-scan-results.md template with sections: source-map, anchors, tensions, scan-strategy. Term registry lives separately in term-registry.md.

**Status:** domain-scan output template exists. Extraction and refinement templates not yet formalized.

---

### ⏹ Tests

**Purpose:** Validate build.py, scanner behavior, phase links.

**Status:** Not yet implemented.

**Path:** `test/` (pytest suites, fixtures, optional workspace snapshots).

---

## Capability Hierarchy (from outline.md)

This skill adopts and builds from:
1. **workspace** (required)
2. **phases & process** (required)
3. **checklists** (required)
4. **build from parts** (required)
5. **rules & scanners** (required but not fully implemented)
6. **templates** (optional; step 0 is formalized)
7. **tests** (optional; future work)

See `SKILL.md` for quick start and `content/parts/process.md` for the 24-phase OOAD pipeline.
