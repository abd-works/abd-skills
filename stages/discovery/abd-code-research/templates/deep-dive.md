# Deep Dive: <!-- Research Path Name — e.g. COH Bridge Seam -->

**Project:** <!-- e.g. Hero Virtual Tabletop -->
**Concern kind:** <!-- Layer | Mechanism | Component | Cross-Cutting | Pattern | Boundary -->
**Technology:** <!-- e.g. C# P/Invoke + Win32 memory API -->
**Source root:** <!-- e.g. C:\hero-desktop\city-of-heroes-virtual-tabletop\src -->
**Feeds:** `abd-architecture-specification` — <!-- mechanism section name -->

---

## Principles & Patterns

<!-- Name the principle(s) this code enforces, explicitly or implicitly.
     Name the pattern if one applies (e.g. Repository, Adapter, Strategy, Offset Table).
     Be specific: "Direct memory coupling with no adapter layer" is better than "low-level memory access."
     If evidence is insufficient, write: TBD — needs further reading of <file(s)>  -->

---

## File Structure

<!-- Show the files involved in this mechanism, annotated with their role.
     Use a tree or flat list — whichever reveals the structure better.
     Example:
       src/
         Crowds/CharacterExplorerViewModel.cs   ← primary P/Invoke caller
         Identities/Camera.cs                   ← per-entity offset constants
         Roster/CharacterActivator.cs           ← writes activation state
-->

---

## Participants

| Class / Module | Layer | Role |
|---|---|---|
| <!-- ClassName --> | <!-- Presentation / Domain / Infrastructure / etc. --> | <!-- One-line role description --> |
| <!-- ClassName --> | | |
| <!-- ClassName --> | | |

<!-- Add rows as needed. If participant list is incomplete, add a row:
     | TBD | — | needs further reading of <file> |  -->

---

## Flow

<!-- Number the steps that show how this mechanism runs end-to-end.
     Each step should name the class and operation involved.
     Example:
       1. User action triggers ViewModel command
       2. ViewModel calls ReadProcessMemory at entity offset
       3. Value decoded to domain type
       4. Domain mutation applied to COH memory via WriteProcessMemory
     If flow is incomplete: 
       TBD — needs further reading to trace the full call sequence.  -->

1.
2.
3.
4.

---

## Walkthrough Example

<!-- Show one concrete scenario end-to-end using real class and method names
     from the source notes. This is a prose walkthrough, not a code block.
     Example:
       Activating a character: CharacterActivator.Activate(entity) writes the
       entity's activation flag at offset CameraOffset + 0x04 via
       WriteProcessMemory, then signals the UI binding.
     If not yet traced: TBD — needs further reading of <file(s)>  -->

---

## Open Questions

<!-- List anything that needs a second reading pass or a call with the team.
     Delete this section if there are no open questions. -->

- <!-- e.g. Where is the offset table versioned for different COH builds? -->
