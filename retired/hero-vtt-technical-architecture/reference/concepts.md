# Hero VTT Technical Architecture — Concepts

## Architecture layers

| Layer | Tech | Location | Responsibility |
| --- | --- | --- | --- |
| **Presentation** | WPF XAML + `*ViewModel.cs`, Prism `DelegateCommand`, `INotifyPropertyChanged` | `Module.HeroVirtualTabletop/{Feature}/` | Layout, binding, event routing. **Nothing else.** |
| **Domain** | Plain C# classes and interfaces | `Module.HeroVirtualTabletop/{Feature}/` | All business rules. No game internals. No concrete COH types. |
| **COH Integration** | `IGameCommandExecutor`, `IMemoryInstance`, `IIconInteractionUtility` | `Library/GameCommunicator/`, `Library/ProcessCommunicator/` | Exclusive seam between application and COH game engine. |

**Dependency direction:** Presentation → Domain → COH Integration interfaces. No arrow reverses.

---

## Mechanism: Skinny ViewModel

Every command handler is a one-liner calling one domain method. Observable properties are direct domain references — no copy, no sync, no local state. When a ViewModel accumulates structural plumbing, that is a domain extraction trigger: name the concept, create the domain class, delete the ViewModel plumbing.

---

## Mechanism: COH Game Bridge Seam

Three structurally different COH paths, each behind its own interface:

| Interface | Underlying path |
| --- | --- |
| `IGameCommandExecutor` | HookCostume.dll → WriteProcessMemory to COH command buffer |
| `IMemoryInstance` | MemorySharp → direct OS ReadProcessMemory/WriteProcessMemory at offsets |
| `IIconInteractionUtility` | P/Invoke → PowerHook data exports (hover NPC, 3D mouse, raycast) |

No domain class and no ViewModel ever references concrete implementations directly.

---

## Mechanism: Direct Memory Manipulation

`IMemoryInstance` exposes semantic operations (`SetPosition`, `SetFacing`, `ReadXYZ`). All COH offset constants live only in `MemoryInstance.cs`. No domain class holds a memory offset or imports `MemorySharp`.

---

## Test tiers

| Tier | Focus | COH | Project |
| --- | --- | --- | --- |
| **1 — Domain** | Domain invariants, rules, state transitions. No ViewModel, no COH. | `NoOpGameCommandExecutor` + `FakeMemoryInstance` | `Module.UnitTest` |
| **2 — ViewModel + Domain** | Binding and command delegation. Real domain, COH still stubbed. | Stubbed | `Module.UnitTest` |
| **3 — E2E key paths** | Architectural wiring — one test per critical path, not per scenario. | Stubbed | `Module.UnitTest` |
| **Game Bridge** | Live DLL injection + `RunPatch()`. One test per bridge path. | Real COH required | `Module.IntegrationTest` |
