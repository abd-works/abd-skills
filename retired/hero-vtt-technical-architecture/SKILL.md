---
name: hero-vtt-technical-architecture
catalog_garden_family: architecture-centric-engineering
catalogue_one_liner: >-
  WPF C# modules for Hero Virtual Tabletop — three-layer architecture with Skinny ViewModel and COH Game Bridge Seam.
description: >-
  Generate production Hero Virtual Tabletop (WPF C#) modules following the
  three-layer architecture — Presentation (ViewModel) · Domain · COH Integration.
  Enforces the Skinny ViewModel, COH Game Bridge Seam, and Direct Memory
  Manipulation mechanisms from inputs/architecture-reference.md. Use when
  adding a new feature, writing a ViewModel, adding domain classes, reviewing
  PRs for architecture compliance, or refactoring fat ViewModels.
---
# hero-vtt-technical-architecture

## Purpose

Generate production Hero Virtual Tabletop modules using the **architecture fixed in `inputs/architecture-reference.md`** — organizing by feature folder, enforcing strict layer purity (Presentation → Domain → COH Integration interfaces), and following the three mechanism patterns the reference defines.

This skill produces real, runnable C# files. ViewModels are thin binding adapters. Domain classes hold all business rules and call game operations only through injected interfaces. Every concrete COH type lives exclusively in `Library/GameCommunicator/` or `Library/ProcessCommunicator/`.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** Feature module files under `Module.HeroVirtualTabletop/{Feature}/` with corresponding test files.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — architecture layers, three mechanisms (Skinny ViewModel, COH Game Bridge Seam, Direct Memory Manipulation), and test tiers.
- **`inputs/architecture-reference.md`** — the authoritative reference with full mechanism details.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/feature-module.template.txt` | Full feature folder scaffold |
| `templates/viewmodel.template.cs` | `{Feature}ViewModel.cs` in Skinny ViewModel pattern |
| `templates/domain-class.template.cs` | Domain class with constructor-injected interfaces |
| `templates/test-domain.template.cs` | Tier 1 domain test class |
| `templates/test-viewmodel.template.cs` | Tier 2 ViewModel + Domain test class |

**Two generation modes:**
- **Feature module** — full feature folder with View, ViewModel, Domain class, and tests at all tiers.
- **Mechanism slice** — add one mechanism to an existing class (e.g. inject COH bridge seam, extract OptionGroup).

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/hero-vtt-technical-architecture \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Skinny ViewModels** — every command handler is a one-liner; no ViewModel method longer than three lines.
- **No concrete COH in ViewModel** — no imports from `Library/GameCommunicator/` or `Library/ProcessCommunicator/`.
- **No game internals in Domain** — no `MemorySharp`, `HookCostumeGameCommandExecutor`, `MemoryInstance`, or `IconInteractionUtility`.
- **Constructor injection** — every domain class that touches game state receives interfaces via constructor.
- **Test coverage** — every domain class has Tier 1 test; every ViewModel has Tier 2 test.
- **Test isolation** — no Tier 1/2 test imports `Module.IntegrationTest` or live COH types.
- **Game Bridge tests isolated** — all `[TestCategory("GameBridge")]` in `Module.IntegrationTest` only.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
