# Code Research — Pass 1 Explorer: `c:\dev\abd-skills`

**Subject codebase:** `c:\dev\abd-skills` (the AgileByDesign skills repository).
**Scoping question:** for each of the 11 themed problems from `themed-problems.md`, where does meaningful architectural evidence live in the repo?
**Method:** breadth-first survey of `practices/`, `stages/`, `common/`. Top-level docs read first (`README.md` not exhaustively, `common/skill-index.md` and `common/grill-me-with-practice-skill.md` in full), then drilled into the most-cited skill folders.

Seven research paths are named below. Pass 2 deep-dives live in `../agent-2-deep-dive/`. Raw source excerpts for each path live in `sources.md`.

---

## Research Path: CDD Orchestrator Entry Point

**Concern kind:** Cross-Cutting (workflow / routing)
**Technology:** Markdown skill body + prompt files (no executable orchestration code at this layer; orchestration is contractual)
**Files:**
- `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` (286 lines)
- `practices/context-driven-delivery/skills/cdd-handoff/SKILL.md` (105 lines)
- `practices/context-driven-delivery/prompts/cdd-resume.prompt.md` (79 lines)
- `practices/context-driven-delivery/instructions/cdd-self-correction.instructions.md` (49 lines)

**Summary.** The orchestrator decides which stage × perspective × skill to run next. Its entry-point algorithm is the single most consequential routing decision in any session — and it is implemented purely as prose checks against the workspace tree. The "existing application" case is not a first-class branch of the algorithm. Corrections logged in the journal are not converted into preflight constraints on resume.

**Feeds:** `themed-problems.md` Theme 1 (entry-point); Theme 2 (grill discipline — partly); Theme 3 (folder conventions); Theme 9 (alignment is a gate).

---

## Research Path: Grill Skill

**Concern kind:** Cross-Cutting (interaction protocol)
**Technology:** Markdown reference
**Files:**
- `common/grill-me-with-practice-skill.md` (83 lines)
- `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` step 2 "Walk the grid" (lines 56–117)

**Summary.** Grilling rules (one question at a time; ask before generating; search rules+outputs before asking the user) are documented but lack forcing functions — there is no counter that flags "your draft has 3 questions in it", no check that says "you started generating before grilling completed", no instruction to *publicly answer questions from rule FAIL examples first*. All three failure modes in the session journal are pure compliance gaps.

**Feeds:** Theme 2.

---

## Research Path: Folder Conventions & Session Paths

**Concern kind:** Convention (filesystem layout)
**Technology:** Markdown + PowerShell/Bash scripts
**Files:**
- `practices/context-driven-delivery/skills/cdd-handoff/SKILL.md` line 24 — canonical `docs/cdd-sessions/`
- `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` line 43 — legacy `docs/sessions/`
- `practices/context-driven-delivery/scripts/session-setup.{ps1,sh}` — bootstrap; uses legacy path
- `practices/context-driven-delivery/scripts/detect-correction.{ps1,sh}` — tooling; uses legacy path
- `common/decision-record.md` — uses legacy path
- `docs/eval-loop-planning.md` — uses legacy path
- `catalog/doc/skill/abd-context-driven-delivery/SKILL.html` — generated; uses legacy path

**Summary.** A repository-wide rename from `docs/sessions/` to `docs/cdd-sessions/` is partly complete. Authoritative skills are split (some use the new path, some the old). Fresh agents pick whichever they read first and inconsistencies follow.

**Feeds:** Theme 3.

---

## Research Path: Story Specification — Rules & Scanners

**Concern kind:** Mechanism (rule enforcement)
**Technology:** Markdown rules + Python scanners (`scanner_bases`, `story_scanner`, `domain.json` schema)
**Files:**
- `practices/story-driven-delivery/skills/abd-story-specification/SKILL.md` (117 lines)
- `practices/story-driven-delivery/skills/abd-story-specification/rules/example-tables-use-domain-language.md` (102 lines)
- `practices/story-driven-delivery/skills/abd-story-specification/rules/stub-service-interaction-structure.md` (70 lines)
- `practices/story-driven-delivery/skills/abd-story-specification/rules/given-describes-state-not-actions.md` (31 lines)
- `practices/story-driven-delivery/skills/abd-story-specification/rules/then-asserts-concrete-output.md`
- `practices/story-driven-delivery/skills/abd-story-specification/scanners/example-tables-domain-scanner.py` (≈290 lines)
- `practices/story-driven-delivery/skills/abd-story-specification/scanners/then-asserts-concrete-output-scanner.py` (131 lines)

**Summary.** The rule set covers most of what the journal flagged — Given vs. action, stub interaction structure, example-table column grounding, Then asserting concrete output. **What's missing:** (a) the two-phase proxy flow as a named pattern; (b) bold-system + backtick-operation requirement at boundary-crossing steps; (c) scanner enforcement of *table NAMES* against `domain.json` (rule says it, scanner doesn't); (d) scanner enforcement of *cell contents* being atomic data (scanner only walks step text); (e) a rule forbidding opaque "behavior"/"response" stub columns.

**Feeds:** Themes 4, 5, 6.

---

## Research Path: Story Graph Operations & MD ↔ JSON Sync

**Concern kind:** Mechanism (artifact lifecycle)
**Technology:** Python CLI + helper modules (`story_map.py`, `story_graph_file.py`, `md_story_map_to_story_graph.py`)
**Files:**
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md` (340+ lines)
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_cli.py`
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_story_map_to_story_graph.py`
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py`
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py`

**Summary.** The skill provides a one-way pipeline MD → JSON for three input types: story map, acceptance criteria, thin slicing. There is **no reverse pipeline** (JSON → MD) and **no parity checker** ensuring the on-disk JSON and the on-disk MD describe the same set of sub-epics. When a script patches the JSON directly without touching the MD, drift is silent — exactly the failure documented in the journal.

**Feeds:** Theme 9.

---

## Research Path: Diagram Sync & Template Writing

**Concern kind:** Mechanism (template-to-XML rendering)
**Technology:** Python + draw.io XML (mxGraph format with HTML entities for newlines)
**Files:**
- `practices/story-driven-delivery/skills/supporting/drawio-story-sync/SKILL.md`
- `practices/story-driven-delivery/skills/supporting/drawio-story-sync/scripts/` (renderer)
- `practices/domain-driven-design/skills/supporting/drawio-domain-sync/SKILL.md`
- `practices/domain-driven-design/skills/supporting/drawio-domain-sync/scripts/`
- `common/scripts/` (no shared placeholder verifier exists)

**Summary.** Two diagram-sync skills generate draw.io XML from templates. The XML format escapes newlines as `&#10;`, which means a naive `str.replace("{TOKEN}", "line1\nline2")` against the template no-ops silently because the literal `\n` does not match the entity-encoded `&#10;`. There is no shared "after-write, verify no `{...}` placeholder tokens remain" helper, and the per-skill `## Validate` blocks do not call any such verifier.

**Feeds:** Theme 10.

---

## Research Path: Domain Code Map Absence

**Concern kind:** Mechanism — **missing**
**Technology:** N/A — the artifact does not exist in the codebase
**Files:**
- *(none — `Grep "domain-code-map|code map"` in `practices/domain-driven-design` returned zero matches)*

**Summary.** The session journal repeatedly produced a `domain-code-map.md` artifact and refined its conventions (KA heading naming, source-type-row placement, role-aware column sets, multi-layer canonical operations). None of this exists in `abd-skills` — neither as a skill, a template, a rule, nor a scanner. The artifact is required for documenting existing systems but the catalog does not know about it.

**Feeds:** Theme 8.

---

## Path count — 7 (within the 5–10 bound)

| Path | Themes covered |
|---|---|
| CDD Orchestrator Entry Point | 1, 3, parts of 2 and 9 |
| Grill Skill | 2 |
| Folder Conventions & Session Paths | 3 |
| Story Specification — Rules & Scanners | 4, 5, 6, partly 11 |
| Story Graph Operations & MD ↔ JSON Sync | 9 |
| Diagram Sync & Template Writing | 10, partly 6 |
| Domain Code Map Absence | 8 |

Themes 7 (fixtures duplicated) and 11 (semantic drift) are touched within the "Story Specification" deep-dive — they share the same skill folder and the same scanner-insufficiency root cause.
