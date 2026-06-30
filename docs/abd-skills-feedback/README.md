# abd-skills feedback — session 2026-06-26-reverse-engineer-discovery-to-test

This folder consolidates the corrections that surfaced during the
`reverse-engineer-discovery-to-test` CDD session against `pml-midtier`,
themes them into a problem list, and works each theme through self-grill,
diagnose, and code-research lenses against `C:\dev\abd-skills`.

The goal is **not** to fix `abd-skills` in this session. The goal is to
produce a defensible, evidence-grounded brief that a future engineer (or
agent) can pick up and turn into countermeasures with minimal re-reading.

## Reading order

1. **`themed-problems.md`** — start here. Eleven themed problems plus three
   cross-cutting concerns, derived from the session journal. No proposed
   solutions; intentionally just the problems.

2. **`self-grill-and-countermeasures.md`** — for each themed problem, hard
   questions answered against `abd-skills` source files, plus concrete
   proposed countermeasures (the *what would fix this* layer).

3. **`diagnose.md`** — structural review of `abd-skills` per theme, with
   file-and-line citations of where each issue lives or where a countermeasure
   would attach. Includes a severity rollup.

4. **`delivery-graph-injection.md`** — proposal for **Phase 6.5** sitting next
   to `c:\dev\abd-skills\docs\delivery-graph-solution.md`. Specifies how the
   existing `sessionStart` / `userPromptSubmitted` hooks should be rewritten
   to emit a **generated read-gate instruction** derived from the taxonomy,
   the context graph, and the active skill's front matter — so the agent is
   told every turn which upstream artifacts to load, and what to do if any
   are missing. This is the highest-leverage edit against the "artifacts
   not getting used" meta-problem (cross-cutting concern C1).

5. **`code-research/`** — Pass 1 / Pass 2 from `abd-code-research` applied to
   `abd-skills` itself.
   - `agent-1-explorer/research-paths.md` — 7 research paths covering the
     themed problems.
   - `agent-1-explorer/sources.md` — verbatim excerpts with file paths and
     line ranges, per research path.
   - `agent-2-deep-dive/<path>.md` — one deep-dive per path in the five-part
     shape (Principles & Patterns, File Structure, Participants, Flow,
     Walkthrough).

## Research paths covered

| # | Path | Deep-dive file |
|---|---|---|
| 1 | CDD Orchestrator Entry Point | `code-research/agent-2-deep-dive/cdd-orchestrator-entry-point.md` |
| 2 | Grill Skill | `code-research/agent-2-deep-dive/grill-skill.md` |
| 3 | Folder Conventions & Session Paths | `code-research/agent-2-deep-dive/folder-conventions-and-session-paths.md` |
| 4 | Story Specification — Rules & Scanners | `code-research/agent-2-deep-dive/story-specification-rules-and-scanners.md` |
| 5 | Story Graph Operations & MD ↔ JSON Sync | `code-research/agent-2-deep-dive/story-graph-md-sync.md` |
| 6 | Diagram Sync & Template Writing | `code-research/agent-2-deep-dive/diagram-sync-and-template-writing.md` |
| 7 | Domain Code Map Absence | `code-research/agent-2-deep-dive/domain-code-map-absence.md` |

## Themes covered (eleven from `themed-problems.md`)

1. Entry-point detection ignores attached skills and existing artifacts
2. Grill discipline (opt-in, one question, read first) not enforced
3. Folder convention drift (`docs/sessions/` vs `docs/cdd-sessions/`)
4. Corrections are written but not re-applied on resume
5. Rule statements drift from scanner enforcement
6. Scanners stop at structural shape; they don't read example-table cells
7. Story graph JSON ↔ story map MD can silently diverge
8. Diagram templates filled via fragile string replacement
9. No "domain code map" artifact linking domain concepts to existing files
10. Midtier / proxy specification patterns are absent
11. Stub data and route conventions are improvised at spec time

## Cross-cutting concerns

- **Single source of truth, mechanically enforced** — applies to themes 3, 7, 8.
- **Validate before generate** — applies to themes 1, 2, 4, 6.
- **Scanners are necessary but not sufficient** — applies to themes 5, 6, 11.

## Inputs (what was read)

- `cdd-session-journal.md` (session under review)
- `cdd-session-checklist.md` (session under review)
- `abd-context-driven-delivery/SKILL.md`, `cdd-resume.prompt.md`, `cdd-self-correction.instructions.md`
- `cdd-handoff/SKILL.md`
- `abd-context-app-sandbox/SKILL.md`
- `common/grill-me-with-practice-skill.md`
- `abd-story-specification/SKILL.md` and its `rules/*.md` + `scanners/*.py`
- `abd-story-mapping/SKILL.md`
- `story-graph-ops/SKILL.md` and its conversion scripts
- `abd-domain-*` skills (language, glossary, model, specification)
- `drawio-story-sync/`, `drawio-domain-sync/` (template patterns)

## Not done (out of scope for this session)

- Implementing any of the proposed countermeasures.
- Touching `abd-skills` itself.
- Promoting any deep-dive into `abd-architecture-specification` mechanism
  sections.
