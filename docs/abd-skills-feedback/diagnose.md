# /diagnose — abd-skills structural review

> `/diagnose` applied to `c:\dev\abd-skills` for the 11 themes in `themed-problems.md`. For each theme, this file enumerates **concrete file-level observations**: what is wired up, what is half-wired, what is missing. Every claim cites a real file path. Pair this with `self-grill-and-countermeasures.md` (countermeasures) and `code-research/` (deep dives).

---

## Methodology

1. Listed `practices/`, `stages/`, `common/` to map the skill catalog.
2. Read the four most-implicated SKILL.md files in full:
   `abd-context-driven-delivery`, `cdd-handoff`, `cdd-resume.prompt.md`, `abd-story-specification`, `abd-context-app-sandbox`, plus `common/grill-me-with-practice-skill.md` and `common/skill-index.md`.
3. Read two key scanners in full: `example-tables-domain-scanner.py`, `then-asserts-concrete-output-scanner.py`.
4. Cross-checked claims using `Grep` for: `docs/sessions/`, `domain-code-map`, `existing application`, `behavior` (as column-name suffix), boundary-step naming, MD ↔ JSON parity.

---

## Quick map — abd-skills layout

| Path | Function |
|---|---|
| `practices/context-driven-delivery/skills/abd-context-driven-delivery/` | Top-level orchestrator skill |
| `practices/context-driven-delivery/skills/abd-context-app-sandbox/` | Context-stage sandbox |
| `practices/context-driven-delivery/skills/abd-context-app-extractor/` | Context-stage runtime extractor |
| `practices/context-driven-delivery/skills/cdd-handoff/` | Session-pause skill |
| `practices/context-driven-delivery/prompts/cdd-resume.prompt.md` | Session-resume prompt |
| `practices/context-driven-delivery/instructions/cdd-self-correction.instructions.md` | Real-time correction-logging instruction |
| `practices/story-driven-delivery/skills/abd-story-mapping/` | Discovery story map (full) + Shaping outline |
| `practices/story-driven-delivery/skills/abd-story-acceptance-criteria/` | Exploration AC |
| `practices/story-driven-delivery/skills/abd-story-specification/` | Specification spec-by-example |
| `practices/story-driven-delivery/skills/abd-story-acceptance-test/` | Engineering acceptance tests |
| `practices/story-driven-delivery/skills/supporting/story-graph-ops/` | MD → graph conversion, graph CRUD, validation |
| `practices/story-driven-delivery/skills/supporting/drawio-story-sync/` | Story-map diagram sync |
| `practices/domain-driven-design/skills/abd-domain-language/` | Discovery domain language |
| `practices/domain-driven-design/skills/abd-domain-model/` | Exploration domain model |
| `practices/domain-driven-design/skills/abd-domain-specification/` | Specification typed model |
| `practices/domain-driven-design/skills/supporting/drawio-domain-sync/` | Domain-model diagram sync |
| `common/grill-me-with-practice-skill.md` | Grilling rules (one question at a time, sources of questions) |
| `common/skill-index.md` | Generated index of skills × perspective × fidelity |
| `common/folder-conventions.md` | Canonical `docs/` subtree |
| `common/skill-workflow.md` | Per-skill workflow shared rules |
| `common/scanner-runner` / `common/scripts/` | Scanner infrastructure |

---

## Theme-by-theme diagnostic findings

### Theme 1 — Orchestrator entry-point detection for existing apps

**Finding 1A — Entry-point algorithm has no "existing app" branch.**
- File: `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` lines 47–53.
- The six listed conditions are about source material and stage-by-stage artifacts. None of them is "running application without `docs/external/app-extraction/`".

**Finding 1B — Attached-skill signal is not consumed.**
- Same file, step `### 1. Assess entry point`. The algorithm reads `cdd-context-index.md`, the scaffold tree, and `skill-index.md` — it never inspects skills the user attached to the opening message.

**Finding 1C — `cdd-resume.prompt.md` does not declare existing-journal corrections as mandatory preflight.**
- File: `practices/context-driven-delivery/prompts/cdd-resume.prompt.md` lines 47–67. Corrections are mentioned only as something the user might newly add ("If the user provides corrections, add them..."). There is no step that says "list every entry in `## Corrections` as a numbered preflight before any work".

**Finding 1D — Self-correction instruction is real and well-scoped.**
- File: `practices/context-driven-delivery/instructions/cdd-self-correction.instructions.md`. This instruction correctly says "write the correction first, then fix" (lines 14–34). It is **about logging when something goes wrong now** — it does not say "on resume, treat journal corrections as immediate constraints".

---

### Theme 2 — Grill discipline

**Finding 2A — One-question-at-a-time rule exists.**
- File: `common/grill-me-with-practice-skill.md` line 19. The rule is in the right place. The session journal's repeat violation indicates the rule is read but not detected.

**Finding 2B — "Answer yourself first" loop is implied but not codified.**
- Same file, lines 21–22 and 60–66. The sources are listed; the procedure (search rules + FAIL examples + existing outputs publicly before asking the user) is not.

**Finding 2C — "Grill mode is opt-in" sends a confusing signal.**
- Same file, line 11: "When a skill is invoked **without** "grill me", it generates directly. Grill mode is opt-in." This appears to give the agent permission to skip grilling. The CDD orchestrator (`abd-context-driven-delivery/SKILL.md` line 65) does instruct to grill at each cell, but a reader of the grill skill alone would not infer that.

---

### Theme 3 — Folder & granularity conventions

**Finding 3A — `docs/sessions/` references remain in 8 files.**
Confirmed list (from `Grep`):
- `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` (line 43)
- `practices/context-driven-delivery/scripts/session-setup.ps1`
- `practices/context-driven-delivery/scripts/session-setup.sh`
- `practices/context-driven-delivery/scripts/detect-correction.ps1`
- `practices/context-driven-delivery/scripts/detect-correction.sh`
- `common/decision-record.md`
- `docs/eval-loop-planning.md`
- `catalog/doc/skill/abd-context-driven-delivery/SKILL.html` (generated)

The canonical `cdd-handoff/SKILL.md` line 24 correctly uses `docs/cdd-sessions/`. The mismatch is a partially-completed rename.

**Finding 3B — Granularity rule is solid at the top level, missing for nested plans.**
- `abd-context-driven-delivery/SKILL.md` lines 143–187 shows one-skill-per-line in the canonical template.
- `abd-context-app-sandbox/SKILL.md` lines 51–84 embed multiple skill invocations (story map / AC / domain language at stub-focus) but the orchestrator does not explain how to project this onto the checklist.

---

### Theme 4 — Proxy / midtier semantics

**Finding 4A — `abd-story-acceptance-criteria` is system-agnostic about proxy vs owner.**
- File: `practices/story-driven-delivery/skills/abd-story-acceptance-criteria/SKILL.md` (5,376 bytes).
- Grill prompts in `common/skill-index.md` lines 188–200: Hidden actors / One story or a bundle / Unstated negative paths / Domain vocabulary drift / Observable vs. internal. **No proxy-specific prompt.**

**Finding 4B — `abd-story-specification` knows about stubs but not the two-phase pattern.**
- File: `practices/story-driven-delivery/skills/abd-story-specification/SKILL.md` line 88: stub-in-Given is correct. Two-phase **When → Then → When → Then** is not named.
- Rule file: `rules/stub-service-interaction-structure.md` (3,103 bytes) covers stub structure but does not encode the proxy two-phase shape.

**Finding 4C — No rule requires bold-system + backtick-operation at boundary steps.**
- `Grep` for `to \*\*Mavenir|to \*\*\\w+` returns no rule body matches. Journal lines 254–255 explicitly note this gap.

**Finding 4D — `given-describes-state-not-actions.md` exists (1,480 bytes) but presumably lacks the proxy-specific FAIL example.**
- File: `practices/story-driven-delivery/skills/abd-story-specification/rules/given-describes-state-not-actions.md`. The session correction (lines 235–242) introduces this specific FAIL — implying the rule did not contain it before.

---

### Theme 5 — Spec example tables drift from domain model

**Finding 5A — `example-tables-use-domain-language.md` rule text requires BOTH table names and column names to match.**
- File: `practices/story-driven-delivery/skills/abd-story-specification/rules/example-tables-use-domain-language.md` lines 17–18 and 51.

**Finding 5B — `example-tables-domain-scanner.py` checks columns only, not table names.**
- File: `practices/story-driven-delivery/skills/abd-story-specification/scanners/example-tables-domain-scanner.py` lines 175–290. Reads `scenario.examples_columns`; never references a `scenario.examples_table_name` (or equivalent) attribute against `domain.json`.
- Confirms the journal correction at line 225.

**Finding 5C — No rule forbids opaque "behavior" / "stub_response" columns.**
- `Grep "behavior" rules/` returns no specific rule about disallowed suffixes.

**Finding 5D — No mandatory read of service-specific domain model modules.**
- `abd-story-specification/SKILL.md` lines 49–63 lists Class Model / domain model / domain language. The pattern `docs/domain/model/modules/{service}-domain-model.md` is project-specific, not standardized in the skill.

---

### Theme 6 — Scanner reliability

**Finding 6A — `then-asserts-concrete-output-scanner.py` checks step text, never cells.**
- File: `practices/story-driven-delivery/skills/abd-story-specification/scanners/then-asserts-concrete-output-scanner.py` lines 86–120.
- The walk is `for step in scenario.steps:` — table cells are not iterated.

**Finding 6B — No shared "verify no `{...}` placeholders remain" helper.**
- Searched `common/scripts/`, `common/`, `practices/*/skills/*/scripts/`. No helper named like `verify_no_placeholders` exists. Each diagram-sync skill would need to roll its own.

**Finding 6C — No "scanner is necessary but not sufficient" general guidance.**
- `common/skill-workflow.md` does not have such a section. The closest is the rule-checklist (`common/rule-checklist.md`) which lists rules to check but does not say "scanner + manual independent verification".

---

### Theme 7 — Stubs and fixtures referenced, not duplicated

**Finding 7A — `abd-story-acceptance-test` has a `Stub fixture completeness` grill prompt** (skill-index line 319) but no rule body found by quick search. The journal correction (lines 259–270) introduces the duplication rule for the first time.

---

### Theme 8 — Domain code map

**Finding 8A — `domain-code-map` does not exist anywhere in `practices/domain-driven-design/`.**
- `Grep "domain-code-map|code map" c:\dev\abd-skills\practices\domain-driven-design` returns **zero matches**.
- The artifact is absent from the catalog, the skill-index, and any DDD skill body. Yet the session journal (lines 271–341) shows the artifact is essential for reverse-engineering existing systems.

**Finding 8B — Specification stage in CDD orchestrator does not call for a code map.**
- `abd-context-driven-delivery/SKILL.md` line 174: `Specification: Domain — abd-domain-specification + abd-domain-walk`. No code-map step.

---

### Theme 9 — Story map ↔ graph ↔ spec ↔ test alignment

**Finding 9A — `story-graph-ops` provides MD → JSON one-way conversion.**
- File: `practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md` line 175 lists `md_story_map_to_story_graph.py`.

**Finding 9B — No MD ↔ JSON parity checker exists.**
- The same SKILL.md and `scripts/` folder contain a `story_graph_cli.py` with `read / write / sha` operations (line 117) — used for conflict avoidance — but no `check-parity-with-md` command.

**Finding 9C — `abd-story-specification` does not require reading `story-map.md` in `### 1. Read context`.**
- File: `practices/story-driven-delivery/skills/abd-story-specification/SKILL.md` lines 49–63. Lists Class Model / domain model / domain language. Story map is not required.

**Finding 9D — Consistency check runs after generation, not before.**
- `abd-context-driven-delivery/SKILL.md` lines 107–116. By design it is post-output. Pre-generation alignment is not a defined step.

---

### Theme 10 — Diagram tooling reliability

**Finding 10A — Risk pattern is generic to any template-write step.**
- Templates exist throughout abd-skills (`templates/` folders in nearly every skill). Any Python script doing `str.replace` against `&#10;`-encoded XML inherits the silent-no-op bug.
- No central guard exists.

**Finding 10B — Diagram sync skills exist** at `drawio-story-sync` and `drawio-domain-sync` but their `## Validate` blocks do not call a shared placeholder verifier.

---

### Theme 11 — Semantic vs structural consistency

**Finding 11A — `abd-context-driven-delivery/SKILL.md` consistency check dimensions are Glossary / Behaviour / Structure / Scope (lines 107–116).**
- Behaviour is described at the artifact level (stories ↔ UX ↔ architecture describing the same interactions).
- There is no "AC expected outcome vs current code execution path" check.

**Finding 11B — Implementation gaps end up as prose in the journal.**
- The 401/403 finding (session journal lines 180–194) is correctly identified by the agent in the consistency check but lands in the journal as a "Recommendation". There is no skill that emits a tracked artifact (`docs/cdd-sessions/<date>/implementation-gaps.md`).

---

## Severity rollup

| Theme | Severity | Why |
|---|---|---|
| 1. Orchestrator entry-point | **HIGH** | Recurs on every reverse-engineering session; user has to correct it manually |
| 2. Grill discipline | **HIGH** | The skill text is correct; what's missing is a behavioral forcing function — affects every session |
| 3. Folder/granularity drift | **MEDIUM** | Confusing but easily fixed by a rename + lint |
| 4. Proxy/midtier semantics | **HIGH** | Affects any API/proxy/integration-layer project; rules+scanners needed |
| 5. Tables drift from domain | **HIGH** | Cascades into untestable specs; scanner is half-complete |
| 6. Scanners insufficient | **HIGH** | Cross-cutting; small additions to `common/` would help every skill |
| 7. Fixtures duplicated | **MEDIUM** | Localized to engineering stage; rule + small scanner closes most of it |
| 8. No domain-code-map skill | **HIGH** | Entire artifact is missing from the catalog; reverse-engineering depends on it |
| 9. Alignment cleanup, not gate | **HIGH** | Most disruptive — late discovery = rework |
| 10. Template tooling | **MEDIUM** | Silent failure mode; one shared helper fixes the class of bug |
| 11. Semantic drift surface | **MEDIUM** | Currently relies on a human noticing — a tracked artifact promotes it |

---

## Suggested order of work (if user pursues fixes)

1. **Theme 1, 2, 3** — process-level changes; cheap to write, immediate impact. Bulk-renames + a few rule additions.
2. **Theme 9** — add `story-map.md` as a mandatory read in `abd-story-specification`; add a parity script to `story-graph-ops`. High-leverage gate.
3. **Theme 5 + Theme 6** — extend `example-tables-domain-scanner.py` for table names; add `example-cells-are-atomic-data-scanner.py`. Closes the loop on the most-cited spec-quality issues.
4. **Theme 4** — proxy two-phase rule + boundary system+operation rule + scanner. Substantial but localized to `abd-story-specification`.
5. **Theme 8** — new `abd-domain-code-map` skill. Larger effort; needs templates, rules, and orchestrator integration.
6. **Theme 10, 11, 7** — incremental closeouts.

---

## What this file is NOT

- Not an implementation plan with timelines.
- Not a code-research deep dive — that's in `code-research/`. This is a structural diagnosis at the file-and-line level for the 11 themes.
