# Rule: Deep-dive files follow the five-part shape

Every deep-dive file under `agent-2-deep-dive/` must contain all five sections in order: **Principles & Patterns**, **File Structure**, **Participants**, **Flow**, and **Walkthrough Example**. Sections may be stubs marked "TBD — needs further reading" when research is incomplete, but they must be present.

## DO

- Use exactly the five section headings listed above as level-2 headings (`##`).
- Place sections in order: Principles & Patterns → File Structure → Participants → Flow → Walkthrough Example.
- Write stub content ("TBD — needs further reading") rather than omitting a section entirely.
- Name the file in kebab-case matching the research path name (e.g. path *Entity Lifecycle* → `entity-lifecycle.md`).

## DO NOT

- Do not omit any of the five sections, even when evidence is thin.
- Do not rename sections (e.g. "Design Principles" instead of "Principles & Patterns").
- Do not place Walkthrough Example before Flow.
- Do not use a different file naming convention than the kebab-case path name.

## Examples

**DO** — correct five-part shape, stub used where reading is incomplete:
```markdown
## Principles & Patterns
Direct memory coupling — no adapter layer. Offset-table strategy.

## File Structure
src/Crowds/CharacterExplorerViewModel.cs  ← primary P/Invoke caller
src/Identities/Camera.cs                  ← per-entity offset constants

## Participants
| Class | Layer | Role |
|---|---|---|
| CharacterExplorerViewModel | Presentation | Reads/writes COH memory |
| Camera | Domain | Holds camera offset constant |

## Flow
1. User action triggers ViewModel command
2. ViewModel calls ReadProcessMemory at entity offset
3. Value decoded to domain type
4. Domain mutation written back via WriteProcessMemory

## Walkthrough Example
TBD — needs further reading of CharacterActivator.cs
```

**DO NOT** — missing Walkthrough Example, renamed Principles heading:
```markdown
## Design Principles
Direct memory coupling.

## File Structure
src/Crowds/CharacterExplorerViewModel.cs

## Participants
...

## Flow
1. ViewModel reads memory
```
