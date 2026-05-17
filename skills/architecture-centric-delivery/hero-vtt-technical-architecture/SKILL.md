---
name: hero-vtt-technical-architecture
description: >-
  Generate production Hero Virtual Tabletop (WPF C#) modules following the
  three-layer architecture — Presentation (ViewModel) · Domain · COH Integration.
  Enforces the Skinny ViewModel, COH Game Bridge Seam, and Direct Memory
  Manipulation mechanisms from inputs/architecture-reference.md.
---
# hero-vtt-technical-architecture

## Purpose

Generate production Hero Virtual Tabletop modules using the **architecture fixed in `inputs/architecture-reference.md`** — organizing by feature folder, enforcing strict layer purity (Presentation → Domain → COH Integration interfaces), and following the three mechanism patterns the reference defines.

This skill produces real, runnable C# files. Code is co-located by feature (`Module.HeroVirtualTabletop/{Feature}/`). ViewModels are thin binding adapters. Domain classes hold all business rules and call game operations only through injected interfaces. Every concrete COH type lives exclusively in `Library/GameCommunicator/` or `Library/ProcessCommunicator/`.

## When to use this skill

Load this skill when **any** of the following apply:

- You are **adding a new feature** and need the architecture-prescribed folder structure and file set.
- You are **adding a domain class** and need the constructor injection pattern wired up correctly.
- You are **writing a ViewModel** and need to confirm it stays thin — commands delegate, properties bind direct.
- You are **reviewing a PR** for architecture compliance against the reference's principles.
- You are **refactoring a fat ViewModel** (like `RosterExplorerViewModel`) toward the Skinny ViewModel pattern.
- You are **adding a test** and need to know which tier it belongs to and which doubles to use.

---

## Agent Instructions

1. **Read the reference first.** Load [`inputs/architecture-reference.md`](inputs/architecture-reference.md) before generating any code. The reference is authoritative. When the code and the reference disagree, the reference wins.

2. **Pick a generation mode.** This skill supports two modes:

   | Mode | What you get |
   | --- | --- |
   | **Feature module** | Full feature folder: `{Feature}View.xaml`, `{Feature}ViewModel.cs`, `{Feature}.cs` (domain), test files at all three tiers |
   | **Mechanism slice** | One mechanism only — e.g. add the COH Game Bridge seam to an existing domain class, or extract an `OptionGroup` concept from a fat ViewModel |

3. **Generate from templates.** Use every template in `templates/` appropriate to the mode.

   | Template | Generates |
   | --- | --- |
   | `feature-module.template.txt` | Full feature folder scaffold |
   | `viewmodel.template.cs` | A `{Feature}ViewModel.cs` in the Skinny ViewModel pattern |
   | `domain-class.template.cs` | A domain class with constructor-injected `IGameCommandExecutor` + `IMemoryInstance` |
   | `test-domain.template.cs` | Tier 1 domain test class (`FakeMemoryInstance`, `NoOpGameCommandExecutor`) |
   | `test-viewmodel.template.cs` | Tier 2 ViewModel + Domain test class |

4. **Apply rules while generating, not after.** Check each generated file against the bundled rules before presenting output.

5. **Test placement.** Every domain class gets a Tier 1 test. Every ViewModel gets a Tier 2 test. E2E tests (Tier 3) cover only new architectural paths, not scenarios. Game Bridge tests go in `Module.IntegrationTest` only.

---

## Core concepts

### Architecture layers

| Layer | Tech | Location | Responsibility |
| --- | --- | --- | --- |
| **Presentation** | WPF XAML + `*ViewModel.cs`, Prism `DelegateCommand`, `INotifyPropertyChanged` | `Module.HeroVirtualTabletop/{Feature}/` | Layout, binding, event routing. **Nothing else.** |
| **Domain** | Plain C# classes and interfaces | `Module.HeroVirtualTabletop/{Feature}/` | All business rules. No game internals. No concrete COH types. |
| **COH Integration** | `IGameCommandExecutor`, `IMemoryInstance`, `IIconInteractionUtility` | `Library/GameCommunicator/`, `Library/ProcessCommunicator/` | Exclusive seam between application and COH game engine. |

**Dependency direction:** Presentation → Domain → COH Integration interfaces. No arrow reverses.

### Mechanism: Skinny ViewModel

Every command handler is a one-liner calling one domain method. Observable properties are direct domain references — no copy, no sync, no local state. When a ViewModel accumulates structural plumbing (parallel collections, ordering logic, sync code), that is a domain extraction trigger: name the concept, create the domain class (`OptionGroup` is the canonical example), delete the ViewModel plumbing.

### Mechanism: COH Game Bridge Seam

Three structurally different COH paths, each behind its own interface:

| Interface | Underlying path |
| --- | --- |
| `IGameCommandExecutor` | HookCostume.dll → WriteProcessMemory to COH command buffer |
| `IMemoryInstance` | MemorySharp → direct OS ReadProcessMemory/WriteProcessMemory at offsets |
| `IIconInteractionUtility` | P/Invoke → PowerHook data exports (hover NPC, 3D mouse, raycast) |

No domain class and no ViewModel ever references `HookCostumeGameCommandExecutor`, `MemoryInstance`, or `IconInteractionUtility` directly.

### Mechanism: Direct Memory Manipulation

`IMemoryInstance` exposes semantic operations (`SetPosition`, `SetFacing`, `ReadXYZ`). All COH offset constants live only in `MemoryInstance.cs`. No domain class holds a memory offset or imports `MemorySharp`.

### Test tiers

| Tier | Focus | COH | Project |
| --- | --- | --- | --- |
| **1 — Domain** | Domain invariants, rules, state transitions. No ViewModel, no COH. | `NoOpGameCommandExecutor` + `FakeMemoryInstance` | `Module.UnitTest` |
| **2 — ViewModel + Domain** | Binding and command delegation. Real domain, COH still stubbed. | Stubbed | `Module.UnitTest` |
| **3 — E2E key paths** | Architectural wiring — one test per critical path, not per scenario. | Stubbed | `Module.UnitTest` |
| **Game Bridge** | Live DLL injection + `RunPatch()`. One test per bridge path. | Real COH required | `Module.IntegrationTest` |

---

## The shape of a good feature module

```
Module.HeroVirtualTabletop/{Feature}/
├── {Feature}View.xaml              ← Presentation: XAML only, no code-behind logic
├── {Feature}ViewModel.cs           ← Presentation: one-liner commands, direct domain bindings
└── {Feature}.cs                    ← Domain: all rules, no game internals

Module.UnitTest/Domain/
└── {Feature}DomainTest.cs          ← Tier 1: FakeMemoryInstance + NoOpGameCommandExecutor

Module.UnitTest/Presentation/
└── {Feature}ViewModelTest.cs       ← Tier 2: real domain + fakes; assert binding and domain state

Module.IntegrationTest/             ← Game Bridge tier only (never for domain or VM logic)
```

---

## Build (feature module mode)

1. **Name the feature and identify its domain class.** The domain class name comes from the ubiquitous language. The feature folder name matches the domain concept.

2. **Generate `{Feature}ViewModel.cs`** from `templates/viewmodel.template.cs`. Replace `{Feature}` and `{DomainClass}`. Add one `DelegateCommand` per user story action. Each command handler: one line, one domain method call.

3. **Generate `{Feature}.cs`** from `templates/domain-class.template.cs`. Replace `{Feature}` and inject `IGameCommandExecutor` and/or `IMemoryInstance` as needed. Business logic lives here. No MemorySharp imports. No concrete COH class references.

4. **Create `{Feature}View.xaml`.** Bind `ItemsSource`, `SelectedItem`, and command bindings from ViewModel properties. No code-behind logic beyond standard WPF wiring.

5. **Generate Tier 1 test** from `templates/test-domain.template.cs`. Construct the domain class with `FakeMemoryInstance` + `NoOpGameCommandExecutor`. Write one test method per acceptance criterion.

6. **Generate Tier 2 test** from `templates/test-viewmodel.template.cs`. Wire the real domain class to the ViewModel. Assert both binding state and domain post-state.

7. **Apply rules.** Walk every bundled rule against all generated files before declaring done.

---

## Build (mechanism slice mode)

Specify which mechanism is being added to an existing class, then use only the relevant template(s):

- **Add COH bridge seam to existing domain class:** inject `IGameCommandExecutor` or `IMemoryInstance` via constructor; replace any direct `MemorySharp` or DLL calls with interface calls; update Tier 1 test to use fakes.
- **Extract OptionGroup from fat ViewModel:** identify the parallel collections + ordering logic; create the domain class; expose it via the ViewModel as a direct reference; delete the ViewModel plumbing; update Tier 1 and Tier 2 tests.
- **Add FakeMemoryInstance test double:** implement `IMemoryInstance` with dictionary-backed state; add `SetXYZ`, `SetFacing`, `SetLabel` pre-seed helpers; register in `GameCommandTestAssemblyHooks`.

---

## Validate

Walk generated code and confirm:

- Every `{Feature}ViewModel` command handler is a one-liner. No ViewModel method is longer than three lines including the null guard.
- No ViewModel imports from `Library/GameCommunicator/` or `Library/ProcessCommunicator/` concrete types.
- No domain class imports `MemorySharp`, `HookCostumeGameCommandExecutor`, `MemoryInstance`, or `IconInteractionUtility`.
- Every domain class that touches game state receives `IGameCommandExecutor` and/or `IMemoryInstance` via constructor injection.
- Every domain class has a Tier 1 test. Every ViewModel has a Tier 2 test.
- No Tier 1 or Tier 2 test imports `Module.IntegrationTest` or any live COH type.
- All `[TestCategory("GameBridge")]` tests are in `Module.IntegrationTest` only.

---

## Deploy

```powershell
cd C:\dev\agilebydesign-skills
.\scripts\deploy-skills.ps1 -ide cursor -Force
```

| File | Deploy target |
| --- | --- |
| `ide-files/hero-vtt-technical-architecture.mdc` | `.cursor/rules/` |
| `ide-files/hero-vtt-technical-architecture.prompt.md` | `.cursor/commands/` |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/architecture-centric-delivery/hero-vtt-technical-architecture
-->
<!-- execute_rules:bundle_rules:end -->
