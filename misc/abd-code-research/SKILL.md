---
name: abd-code-research
description: >-
  Survey any codebase in two passes — Explorer and Deep Dive — to produce
  structured research that primes the architecture skill family.
---
# abd-code-research

## Purpose

Walking into an unfamiliar codebase without a map turns architecture work into guesswork. This skill makes the survey systematic: a first pass spans the codebase breadth-first, naming every meaningful research path and capturing raw source evidence; a second pass follows each path to the depth that architecture documentation needs. The two passes produce structured outputs that feed directly into `abd-architecture-outline`, `abd-architecture-blueprint`, and `abd-architecture-specification`, so those downstream skills start with evidence rather than assumptions. The skill works for any codebase — compiled or interpreted, monolith or modular, documented or bare — and scales from a 500-line script to a 200-file enterprise system.

---

## When to use this skill

Load this skill when **any** of the following apply:

- You are about to produce an architecture outline, blueprint, or reference for a codebase and **have not yet read it systematically**.
- The team disagrees about "how the system actually works" and you need **evidence from the code**, not memory or hearsay.
- A new engineer is onboarding and you want to **map the system before writing documentation** so the docs match reality.
- You are reverse-engineering a system that **has no architecture documentation** and you need a defensible starting point.
- A codebase has grown significantly since it was last documented and you want to **identify what changed** before updating any architecture artifact.

---

## What is a code research survey?

A **code research survey** is a two-pass reading of a codebase that produces structured notes an architecture practitioner can use immediately, without re-reading the source.

**Pass 1 — Explorer** walks the codebase breadth-first: entry points, folder structure, key dependencies, configuration, and any existing documentation. It identifies *research paths* — named, scoped lines of inquiry tied to specific files where meaningful architecture decisions are visible — and captures *raw source notes* for each: what the code says, not what the reader infers. Pass 1 outputs feed `abd-architecture-outline` and `abd-architecture-blueprint`.

**Pass 2 — Deep Dive** follows each research path from Pass 1 in depth: reading the implementation, extracting mechanisms, documenting participants, tracing flows, and naming patterns. Each path produces one deep-dive file. Pass 2 outputs feed `abd-architecture-specification`.

The two passes stay separated so a reviewer can inspect the Explorer output, challenge the research paths chosen, and redirect the Deep Dive before time is spent on the wrong question.

---

## Core concepts

### Research path

A **research path** is a named, scoped line of inquiry into one area of the codebase where an architecture decision, pattern, or mechanism is likely to be visible. A path names:

- A **name** — short noun phrase identifying the architectural concern (e.g. *Entity Lifecycle*, *Error Propagation*, *Cache Strategy*, *Auth Boundary*)
- A **concern kind** — one of: Layer, Mechanism, Component, Cross-Cutting, Pattern, or Boundary
- A **technology** — the language, framework, or runtime visible at this path
- **File evidence** — the specific files (or file clusters) where this concern is most legible
- A **feeds** line — which downstream skill(s) this path primes

Research paths are the unit of work for Pass 2. A good path is narrow enough to deep-dive in one sitting and important enough that architecture documentation depends on it.

### Source notes

**Source notes** are raw observations from the code — close-to-verbatim excerpts, type names, function signatures, constant values, comment text — with file paths and line numbers. They are the evidence layer: what the code says, not what the researcher infers. Inferences and pattern names go in the research path or deep-dive file, not in source notes.

### Deep-dive file

A **deep-dive file** covers one research path from Pass 1. It is structured in the same five-part shape that `abd-architecture-specification` expects — Principles & Patterns, File Structure, Participants, Flow, and Walkthrough Example — so the deep-dive can be promoted to a full mechanism reference section with minimal re-reading.

### Output folders

By convention, outputs live in a `code-research/` folder at the project root:

```
<project-root>/code-research/
├── agent-1-explorer/
│   ├── research-paths.md      ← Pass 1 primary output
│   └── sources.md             ← Pass 1 raw source notes
└── agent-2-deep-dive/
    ├── <path-name>.md         ← one file per research path
    └── ...
```

The folder name `code-research/` is the default. Teams with a different convention (e.g. `coh-research/`, `arch-notes/`) should agree on a name at the start of the session and keep it consistent across both passes.

### Downstream handoff

| Pass 1 output | Downstream skill |
|---|---|
| `research-paths.md` | `abd-architecture-outline` — layers, guiding principles, major systems |
| `research-paths.md` + `sources.md` | `abd-architecture-blueprint` — components, mechanisms catalogue |
| `agent-2-deep-dive/<path>.md` | `abd-architecture-specification` — mechanism section (Principles & Patterns, File Structure, Participants, Flow, Walkthrough) |

---

## Example

### research-paths.md excerpt

```markdown
## Research Path: COH Bridge Seam

Concern kind: Boundary / Mechanism
Technology: C# P/Invoke + Win32 memory API
Files:
  - src/Crowds/CharacterExplorerViewModel.cs (lines 1–120)
  - src/Identities/Camera.cs
  - src/Roster/CharacterActivator.cs

Summary: The app reads/writes COH process memory via ReadProcessMemory /
         WriteProcessMemory. The seam between managed C# and unmanaged COH
         state is the primary cross-cutting concern for the entire desktop client.

Feeds: abd-architecture-outline (COH Bridge Seam as guiding principle),
       abd-architecture-specification (COH Bridge Seam mechanism section)
```

### sources.md excerpt

```markdown
## Path: COH Bridge Seam — Source notes

### src/Crowds/CharacterExplorerViewModel.cs  lines 42–58
```csharp
[DllImport("kernel32.dll")]
static extern bool ReadProcessMemory(
    IntPtr hProcess, IntPtr lpBaseAddress,
    [Out] byte[] lpBuffer, int nSize, out int lpNumberOfBytesRead);
```
Observation: P/Invoke declaration at ViewModel level — no infrastructure adapter layer.

### src/Identities/Camera.cs  lines 11–19
```csharp
private static readonly IntPtr CameraOffset = new IntPtr(0x00AC3F10);
```
Observation: Hardcoded memory offset. Address versioning not visible here.
```

### deep-dive file excerpt (agent-2-deep-dive/coh-bridge-seam.md)

```markdown
# Deep Dive: COH Bridge Seam

## Principles & Patterns
- Direct memory coupling — no adapter layer wraps the P/Invoke boundary
- Offset table strategy: offsets declared as constants, no runtime discovery
- Read/write parity: every address written must be readable at the same offset

## File Structure
src/
  Crowds/CharacterExplorerViewModel.cs    ← primary P/Invoke caller
  Identities/Camera.cs                   ← per-entity offset constants
  Roster/CharacterActivator.cs           ← writes entity activation state

## Participants
| Class | Layer | Role |
|---|---|---|
| CharacterExplorerViewModel | Presentation | Orchestrates memory read/write calls |
| Camera | Domain | Holds camera offset constant |
| CharacterActivator | Domain | Writes activation state to COH memory |

## Flow
1. User action triggers ViewModel command
2. ViewModel calls ReadProcessMemory at entity offset
3. Value decoded to domain type
4. Domain mutation applied to COH memory via WriteProcessMemory

## Walkthrough Example
Activating a character: CharacterActivator.Activate(entity) writes the entity's
activation flag at offset CameraOffset + 0x04 via WriteProcessMemory, then
signals the UI binding.
```

---

## Build

**Goal:** Run the two-pass survey and produce structured research outputs that are directly usable by the architecture skill family.

### Pass 1 — Explorer

1. **Map the folder structure.** List the top-level directories and identify the language(s), runtime, and build system. Open any existing documentation files (`README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `CLAUDE.md`, `docs/`) first — they often name the architecture the team intended, which you will verify or contradict with the code.

2. **Identify entry points.** Find the main program entry (e.g. `WinMain()`, `main()`, `Program.cs`, `index.ts`, `app.py`) and the primary bootstrapping path. Note what gets wired at startup — this reveals the dependency injection strategy, the layer topology, and the first cross-cutting concerns.

3. **Scan the most significant files.** Start with the 50–100 files that are largest by line count, most referenced by other files, or inside directories whose names suggest cross-cutting concerns (e.g. `services/`, `domain/`, `infrastructure/`, `middleware/`, `adapters/`). For each file, record the file path, the primary types/classes/functions it exports, and a one-line observation about its role.

4. **Identify research paths.** From the scan, name 5–10 research paths using the template at `templates/research-paths.md`. Every path must be tied to specific files and must name the architectural concern it exposes. If the codebase seems bigger than 10 natural research paths, group related mechanisms into one path and note the grouping.

5. **Capture source notes for each path.** For each research path, copy 3–10 representative excerpts from the code: type definitions, function signatures, key constant values, comment text. Every excerpt must carry its file path and line range. Do not paraphrase — if the code says `ProcessMemory(handle, addr, len)`, write that verbatim.

6. **Write `agent-1-explorer/research-paths.md`** using the template at `templates/research-paths.md`.

7. **Write `agent-1-explorer/sources.md`** using the template at `templates/sources.md`.

### Pass 2 — Deep Dive

8. **For each research path in `research-paths.md`**, read the named files in depth. Identify: the principle the code enforces (whether explicitly or implicitly), the named pattern (if one exists), the participants and their layers, the call flow, and one representative scenario that shows the mechanism in action end-to-end.

9. **Write `agent-2-deep-dive/<path-name>.md`** for each path using the template at `templates/deep-dive.md`. Use the kebab-case version of the path name as the filename (e.g. path *COH Bridge Seam* → `coh-bridge-seam.md`). The five-part shape matches `abd-architecture-specification` sections so it can be promoted with minimal re-work.

10. **Apply the rules.** Walk each rule in `rules/` against the produced files. Fix violations before handing off to any downstream architecture skill.

- **Outputs:** `code-research/agent-1-explorer/research-paths.md`, `code-research/agent-1-explorer/sources.md`, and one `code-research/agent-2-deep-dive/<path-name>.md` per research path.
- **While writing:** Every source excerpt carries file path + line range. Every research path names a concern kind, technology, and file evidence. Deep-dive files follow the five-part shape so `abd-architecture-specification` can promote them without re-reading the source.

---

## Validate

**Goal:** Inspect the produced research files as a reviewer — check coverage and traceability, not prose style.

- **Who is checking:** Architecture Reviewer (are the research paths the right ones for this system?), Tech Lead (does source evidence match what the code actually says?), Downstream Author (can I open `research-paths.md` and start `abd-architecture-outline` immediately?).
- **Cross-artifact parity:** Every research path named in `research-paths.md` has a matching deep-dive file in `agent-2-deep-dive/`.

Checklist:

- [ ] `research-paths.md` contains 5–10 paths — not fewer (coverage gaps), not more than 10 top-level entries (over-partitioned).
- [ ] Each path has **concern kind**, **technology**, and **file evidence** pointing to real files on disk.
- [ ] Each path has a **Feeds** line naming at least one downstream architecture skill.
- [ ] `sources.md` has verbatim excerpts — file path and line range present on every excerpt, no paraphrased summaries.
- [ ] One deep-dive file exists per research path, filename matches the kebab-case path name.
- [ ] Each deep-dive has all five sections: **Principles & Patterns**, **File Structure**, **Participants**, **Flow**, **Walkthrough Example** (stubs with "TBD" are acceptable for sections that need more reading).
- [ ] No source citation references a file that does not exist on disk — spot-check at least three citations.
- [ ] `research-paths.md` and `sources.md` are in `agent-1-explorer/`; deep-dive files are in `agent-2-deep-dive/`.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy to any project:

```powershell
& "c:\dev\agilebydesign-skills\scripts\deploy-skills.ps1" -Force -DeployRoot "<project-root>"
```

| File | Deploy target |
|---|---|
| `ide-files/abd-code-research.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/abd-code-research.prompt.md` | `.cursor/commands/` |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root practices/architecture-centric-engineering/skills/abd-code-research
-->

## Rule: Research paths cite real file evidence

Every research path in `research-paths.md` must name at least one file that exists on disk and must specify where in that file the architectural concern is visible.

### DO

- Name specific files with paths relative to the project root.
- Include line numbers or line ranges when the concern is localized.
- When an entire file is relevant, write the path without line numbers.

### DO NOT

- Do not create a research path that names only a folder or module without a concrete file.
- Do not reference files that have not been opened and verified to exist.
- Do not describe the concern without pointing to where in the codebase it is visible.

### Examples

**DO** — ties concern to a specific file and line range:
```
Files:
  - src/Crowds/CharacterExplorerViewModel.cs (lines 42–58)
  - src/Identities/Camera.cs
```

**DO NOT** — names only a directory, no file evidence:
```
Files: src/Crowds/ (all ViewModel files)
```

---

## Rule: Sources are verbatim excerpts with location

Every entry in `sources.md` must be a verbatim (or close-to-verbatim) excerpt from the code — the actual text the code contains — accompanied by the file path and line range. Inferences and pattern-name labels belong in the research path or deep-dive, not in source notes.

### DO

- Copy type definitions, function signatures, constant declarations, and comment text exactly as they appear in the source.
- Include a file path and line range on every excerpt.
- Add a brief observation line below an excerpt when a fact needs flagging (e.g. "P/Invoke at ViewModel level — no adapter").
- Keep observations short and factual; save interpretation for the deep-dive.

### DO NOT

- Do not paraphrase code in plain English as a source note (e.g. "the method reads memory" instead of showing the actual signature).
- Do not omit file path and line range.
- Do not include inferred pattern names or architectural judgments in the source note body.

### Examples

**DO** — verbatim excerpt with location and brief factual observation:
```
### src/Crowds/CharacterExplorerViewModel.cs  lines 42–47
```csharp
[DllImport("kernel32.dll")]
static extern bool ReadProcessMemory(
    IntPtr hProcess, IntPtr lpBaseAddress,
    [Out] byte[] lpBuffer, int nSize, out int lpNumberOfBytesRead);
```
Observation: P/Invoke declaration at ViewModel level — no adapter layer.
```

**DO NOT** — paraphrase without code, no line range:
```
### CharacterExplorerViewModel
The class reads memory from the COH process using Windows kernel functions.
```

---

## Rule: Deep-dive files follow the five-part shape

Every deep-dive file under `agent-2-deep-dive/` must contain all five sections in order: **Principles & Patterns**, **File Structure**, **Participants**, **Flow**, and **Walkthrough Example**. Sections may be stubs marked "TBD — needs further reading" when the research is incomplete, but they must be present.

### DO

- Use exactly the five section headings listed above (level 2 headings `##`).
- Place sections in order: Principles & Patterns → File Structure → Participants → Flow → Walkthrough Example.
- Write stub content ("TBD — needs further reading") rather than omitting a section.
- Name files in kebab-case matching the research path name (e.g. path *Entity Lifecycle* → `entity-lifecycle.md`).

### DO NOT

- Do not omit any of the five sections even when evidence is thin.
- Do not rename sections (e.g. "Design Principles" instead of "Principles & Patterns").
- Do not place Walkthrough Example before Flow.

### Examples

**DO** — correct five-part shape with stub:
```markdown
## Principles & Patterns
Direct memory coupling — no adapter layer. Offset-table strategy.

## File Structure
src/Crowds/CharacterExplorerViewModel.cs  ← P/Invoke caller

## Participants
| Class | Layer | Role |
|---|---|---|
| CharacterExplorerViewModel | Presentation | Reads/writes COH memory |

## Flow
1. User action triggers ViewModel command
2. ViewModel calls ReadProcessMemory at entity offset

## Walkthrough Example
TBD — needs further reading of CharacterActivator.cs
```

**DO NOT** — missing sections, renamed heading:
```markdown
## Design Principles
Direct memory coupling.

## Flow
1. ViewModel calls ReadProcessMemory
```

---

## Rule: Research path count is bounded

`research-paths.md` must contain between 5 and 10 research paths. Fewer than 5 indicates under-coverage of the codebase. More than 10 top-level paths indicates over-partitioning; related mechanisms should be grouped.

### DO

- Aim for 6–8 paths as the working target for most codebases.
- Group closely related mechanisms under one path name with a note (e.g. *Entity State Sync (covers both read and write paths)*).
- Add a path for each layer boundary, major mechanism, and cross-cutting concern that the downstream architecture skills will need to document.

### DO NOT

- Do not produce fewer than 5 paths for any codebase larger than 500 lines.
- Do not produce more than 10 top-level paths without grouping; the Deep Dive phase becomes unmanageable.
- Do not create a path that duplicates a concern already covered by another path.

### Examples

**DO** — 7 paths covering the key concerns of a WPF desktop client:
1. MVVM Binding
2. ViewModel Coordination
3. COH Bridge Seam
4. Entity State Sync
5. Costume Loading
6. Command Dispatch
7. Crowd / Roster Management

**DO NOT** — 14 micro-paths that should be grouped:
1. Memory Read
2. Memory Write
3. Offset Table
4. P/Invoke Declarations
5. Handle Management
... (all 5 belong under one *COH Bridge Seam* path)

<!-- execute_rules:bundle_rules:end -->
