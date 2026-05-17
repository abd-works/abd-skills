# Hero VTT Technical Architecture

Use the `hero-vtt-technical-architecture` skill to generate WPF C# code in the Hero Virtual Tabletop architecture.

## Inputs required

- **Feature name** — the domain concept from the ubiquitous language (e.g. `IdentityEditor`, `MovementEditor`)
- **Generation mode** — `feature-module` (full scaffold) or `mechanism-slice` (one mechanism only)
- **User stories / AC** — the acceptance criteria that drive domain method names and test scenarios

## What the skill produces

**Feature module mode:**
- `{Feature}ViewModel.cs` — Skinny ViewModel: one-liner commands, direct domain property bindings
- `{Feature}.cs` — Domain class: constructor-injected `IGameCommandExecutor` + `IMemoryInstance`, all business rules
- `{Feature}View.xaml` — XAML bindings only
- `Test{Feature}Domain.cs` — Tier 1 domain test (no ViewModel, no live COH)
- `Test{Feature}ViewModel.cs` — Tier 2 ViewModel + real domain test

**Mechanism slice mode:**
- One or more of the above files, focused on adding a specific mechanism to existing code

## How to invoke

> Load the skill and generate a `{FeatureName}` feature module following the Hero VTT technical architecture. Stories: [paste AC here].
