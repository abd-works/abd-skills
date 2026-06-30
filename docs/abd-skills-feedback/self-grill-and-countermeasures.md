# Self-Grill — abd-skills countermeasures against the themed problems

> **`/grill-me`** applied to **myself**, scoped to `c:\dev\abd-skills`. For each theme in `themed-problems.md` I pose the hardest questions I can; each answer is sourced from real files in `abd-skills` (SKILL.md, rules, scanners, prompts, instructions). Countermeasures are concrete proposals — not implementations yet.
>
> **Convention for each Q→A:**
> - **Source** — exact file/lines where the answer comes from.
> - **Verdict** — does the existing scaffolding handle this, partly handle it, or miss it?
> - **Countermeasure** — what would close the gap.

---

## Theme 1 — Orchestrator self-routing fails for "existing application" entry

### Q1.1 — Does the CDD orchestrator skill explicitly distinguish "existing running application" from "existing static source material"?

**Source:** `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` lines 47–53.

The skill lists six entry-point conditions. The first is `No workspace memory or source material needs ingesting → context`. There is **no condition** for "an existing running application without runtime extraction → context". Context is described purely as ingestion of source material, not extraction from a running system.

**Verdict:** **Misses.** The orchestrator literally has no rule that says "existing running application → still Context phase (sandbox + extract first)". The skill catalogues `abd-context-app-sandbox` and `abd-context-app-extractor` but the entry-point assessment text never names them as preconditions.

**Countermeasure C1.1.** Add an explicit entry-point condition: `Existing running application + no extraction artifacts at docs/external/app-extraction/ → context (run abd-context-app-sandbox then abd-context-app-extractor first)`. Surface the rule in `### 1. Assess entry point` and reference the two skill names directly.

---

### Q1.2 — Does the orchestrator treat an "attached skill" as a routing signal?

**Source:** `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` lines 41–54. The skill scans the workspace for existing skill outputs and checks `cdd-context-index.md`. **Nothing in the assessment step instructs the orchestrator to inspect skills attached to the opening user message.**

**Verdict:** **Misses.** Attached-skill detection is not part of the entry-point algorithm.

**Countermeasure C1.2.** In `### 1. Assess entry point`, add step 0: "Read any skills attached to the user's opening message. If a Context-level skill is attached (`abd-context-app-sandbox`, `abd-context-app-extractor`), treat that as a strong signal that the user expects the Context phase — do not propose a later stage without first confirming Context-phase outputs exist."

---

### Q1.3 — Are corrections logged in the journal treated as mandatory, immediate forcing functions when a session resumes?

**Source:** `practices/context-driven-delivery/skills/cdd-handoff/SKILL.md` and `practices/context-driven-delivery/prompts/cdd-resume.prompt.md` lines 47–67. The resume prompt says "if the user provides corrections, add them to the journal `## Corrections` section and re-run the affected cell" — about **new** corrections. It does **not** say "corrections that already exist in the journal are non-negotiable from response 1, before any reading or generation".

**Verdict:** **Partly misses.** The journal accumulates corrections, but there is no forcing function in `cdd-resume.prompt.md` to treat them as immediate constraints. The agent in this session read the handoff, noted "DO NOT grill after generating", then began generating in the same turn anyway (journal lines 141–143).

**Countermeasure C1.3.** In `cdd-resume.prompt.md` step 2 (Locate and read the session), add: "Every entry in `## Corrections` is **mandatory and immediate**, in effect from your very first response. Before any read, any spawn, any generation, list the corrections in chat as a numbered preflight and confirm you are honoring them this turn." Mirror this rule into `cdd-handoff/SKILL.md` § "Where to start".

---

## Theme 2 — Grill discipline is fragile

### Q2.1 — Does `grill-me-with-practice-skill.md` say "one question at a time"?

**Source:** `common/grill-me-with-practice-skill.md` line 19. **Yes:** "You must ask questions **one at a time**, waiting for feedback before continuing."

**Verdict:** **Rule exists but was violated in the session** (journal lines 145–147). The rule is in the right place but there is no detector — nothing flags when a single response contains five numbered grill questions.

**Countermeasure C2.1.** Strengthen the rule with a self-check at the top of every grill turn: "Before sending, count the `?` characters and the numbered prompts in your draft. If more than one grill question is present, delete all but the most blocking one and queue the rest." Optionally add a static checker for proposed responses in critique mode.

---

### Q2.2 — Does the grill skill direct the agent to search the skill's own rules and existing outputs **before** asking the user?

**Source:** `common/grill-me-with-practice-skill.md` lines 21–22 and 42–44 and 60–66.

The skill does say: "If a question can be answered by reading existing skill outputs or the codebase, read them instead of asking" (line 21–22) and lists `## Grill prompts` and `rules/*.md` FAIL examples as sources for questions (lines 60–66). But there is **no step that says**: "for each grill question, before sending it to the user, publicly answer it yourself from (1) the skill's grill prompts, (2) each FAIL example in rules/, (3) existing workspace outputs — and only surface to the user what genuinely cannot be answered from those sources."

**Verdict:** **Partly handles.** The inputs are listed but the ordered procedure isn't.

**Countermeasure C2.2.** Add the explicit "answer yourself first" loop to `common/grill-me-with-practice-skill.md` immediately after the `### Where your questions come from` section. The session journal even documents the corrected procedure verbatim (lines 198–208) — it can be lifted directly.

---

### Q2.3 — Does any skill prevent "grill after generate"?

**Source:** `common/grill-me-with-practice-skill.md` line 11 says "When a skill is invoked **without** "grill me", it generates directly. Grill mode is opt-in." This is the opposite signal — it tells the agent it's OK to generate without grilling unless explicitly asked. The CDD orchestrator says to grill (`abd-context-driven-delivery` line 65) but not where grilling fits relative to spawn.

**Verdict:** **Misses.** No rule says "if you started grilling, finish grilling before generating; never resume grilling after the output exists."

**Countermeasure C2.3.** Add to `abd-context-driven-delivery/SKILL.md` `### 2. Walk the grid` (step 2: Grill): "Once you start grilling for a cell, you must complete grilling before spawning. If a question arises after spawning, it is a **consistency-check** question (post-output) — not a grill question — and it triggers a re-run of the cell with the new constraint added."

---

## Theme 3 — Folder & granularity conventions drift

### Q3.1 — Where in `abd-skills` does the old `docs/sessions/...` path still appear?

**Source:** `rg "docs/sessions/" c:\dev\abd-skills` returned 8 files:

| File | Concern |
|---|---|
| `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` | The orchestrator skill itself still references `docs/sessions/` (line 43) |
| `practices/context-driven-delivery/scripts/session-setup.ps1` / `.sh` | Bootstrapping scripts |
| `practices/context-driven-delivery/scripts/detect-correction.ps1` / `.sh` | Tooling |
| `common/decision-record.md` | Reference doc |
| `docs/eval-loop-planning.md` | Planning doc |
| `catalog/doc/skill/abd-context-driven-delivery/SKILL.html` | Generated catalog page |

**Verdict:** **Misses.** The rename from `docs/sessions/` to `cdd-sessions/` is incomplete across the repo. `cdd-handoff/SKILL.md` correctly uses `docs/cdd-sessions/` (line 24) but the orchestrator skill, the bootstrap scripts, and the decision record still use the old path. Until the canonical path is consistent in every file, fresh agents will pick the wrong one.

**Countermeasure C3.1.** Bulk rename `docs/sessions/` → `docs/cdd-sessions/` in those 8 files. Add a lint pass to CI (`scan.prompt.md` could include this) that fails on `docs/sessions/` outside the `retired/` folder.

---

### Q3.2 — Does any skill enforce one-checklist-line-per-skill-invocation granularity?

**Source:** `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` lines 143–187 show the canonical checklist template. Each line names exactly one skill. That convention is clear at the **top-level** grid. But the embedded multi-step plan inside `abd-context-app-sandbox` (which itself invokes `abd-story-mapping`, `abd-story-acceptance-criteria`, `abd-domain-language` in stub-focus mode) is not reflected in the orchestrator template — there is no guidance for **how to expand a single grid cell into multiple checklist lines when the cell's skill embeds a sub-plan**.

**Verdict:** **Misses for nested plans.** Top-level convention is solid; sub-plan expansion is not addressed.

**Countermeasure C3.2.** Add a section to the CDD orchestrator skill called `### Expanding skills that embed multi-step plans`: when a skill (e.g. `abd-context-app-sandbox`) embeds multiple skill invocations at different fidelity levels, the checklist must expand that cell into one line per embedded invocation, each with its own fidelity tag.

---

## Theme 4 — Proxy / midtier semantics not native to story & spec skills

### Q4.1 — Does `abd-story-acceptance-criteria` know about proxy/mediator systems?

**Source:** `practices/story-driven-delivery/skills/abd-story-acceptance-criteria/SKILL.md` (5,376 bytes). Searching its grill prompts in `common/skill-index.md` (lines 188–200) shows: Hidden actors / One story or a bundle / Unstated negative paths / Domain vocabulary drift / Observable vs. internal. **No proxy-specific prompts.**

**Verdict:** **Misses.** The skill does not distinguish "system under test owns this behavior" from "system under test proxies this behavior".

**Countermeasure C4.1.** Add a grill prompt + a `rules/` entry: `proxy-then-clauses-describe-the-midtier.md` — the THEN clause must describe what the midtier sends or returns; it must never describe what an external system does internally. Include a fail example using the journal's wording (lines 129–133).

---

### Q4.2 — Does `abd-story-specification` know about the two-phase proxy pattern?

**Source:** `practices/story-driven-delivery/skills/abd-story-specification/SKILL.md` line 88 mentions stubbed services: "declare the stub in **Given**, express the system-captures → system-forwards → service-returns sequence in **When**, assert only the business outcome in **Then**". This is close but not the full two-phase pattern (journal lines 231–234): app → midtier → external → midtier → app should produce **When → Then → When → Then**, not one fat When.

The existing rule `rules/stub-service-interaction-structure.md` covers stub structure but not the **two-phase When-Then-When-Then shape** specifically.

**Verdict:** **Partly handles.** Stub-in-Given is correct; two-phase shape is missing.

**Countermeasure C4.2.** Add `rules/two-phase-proxy-when-then.md` to `abd-story-specification/rules/`. Spell out:
- Phase 1: `When app calls midtier → Then midtier constructs and forwards`
- Phase 2: `When external responds → Then midtier transforms and returns`
The rule should explicitly forbid jamming both phases into one When.

---

### Q4.3 — Does any rule require naming the target system and operation at boundary-crossing steps?

**Source:** `rg "to \*\*" c:\dev\abd-skills\practices\story-driven-delivery` finds no rule requiring the **bolded system name + backtick operation** pattern. The corrections in journal lines 243–255 explicitly note: "no existing rule or scanner checks whether `Then` steps include explicit system + operation attribution for external calls."

**Verdict:** **Misses entirely.**

**Countermeasure C4.3.** Add `rules/boundary-step-names-system-and-operation.md` to `abd-story-specification/`. Rule body:
- Every step that implies a boundary crossing must include the **bolded target system** (`**Mavenir**`) and the **operation in backticks** (\`GET customer\`).
- Forbid vague verbs (`fetches`, `verifies`, `detects`, `validates`, `runs the order sequence`) when the implied action crosses a boundary.
- Add a scanner under `scanners/boundary-step-names-system-and-operation-scanner.py` that flags `Then`/`And` steps containing boundary-implying verbs but no `**Word**` + backtick token.

---

### Q4.4 — Does `given-describes-state-not-actions.md` cover the "Given as domain entity state, not stub behavior" correction?

**Source:** `practices/story-driven-delivery/skills/abd-story-specification/rules/given-describes-state-not-actions.md` (1,480 bytes). I have not read it line by line, but its name covers the general principle. It almost certainly addresses verbs in Given, but it likely doesn't address the specific **midtier proxy** failure mode where Given says "Mavenir is stubbed to..." instead of "Mavenir has the following BillingAccount...".

**Verdict:** **Partly handles** — the general rule is right; the proxy-specific FAIL example is missing.

**Countermeasure C4.4.** Add a FAIL example to `given-describes-state-not-actions.md` covering stub-behavior-as-Given:
- WRONG: `Given Mavenir is stubbed so GET customerDetails returns MavenirCustomer with BillingAccount`
- RIGHT: `Given Mavenir has the following BillingAccount for cus_stub_001: [table]`

---

## Theme 5 — Spec example tables drift from the domain model

### Q5.1 — Does `example-tables-use-domain-language.md` require table NAMES (not just columns) to match domain concepts?

**Source:** `practices/story-driven-delivery/skills/abd-story-specification/rules/example-tables-use-domain-language.md` lines 17–18 and 51:

> Table names MUST correspond to a concept in the domain model … Column names MUST correspond to attributes …

The **rule text** clearly requires both. The **scanner** (`example-tables-domain-scanner.py`, see Q6.1 below) implements only the column check.

**Verdict:** **Rule says it; scanner doesn't.** Conformance depends entirely on the AI honoring the rule text, which is exactly what failed.

**Countermeasure C5.1.** Extend `example-tables-domain-scanner.py` to:
1. Extract every table heading (e.g. the line above each pipe-delimited table) and normalize against `domain.json` concept names.
2. Emit an error for any table heading that does not match a concept (with case/underscore normalization mirroring the column check).
3. List the closest matches in the message to nudge the author.

---

### Q5.2 — Is there a rule that forbids opaque "behavior" columns like `mavenir_stub_behavior`?

**Source:** `rg "behavior" c:\dev\abd-skills\practices\story-driven-delivery\skills\abd-story-specification\rules` returns no hit specifically about disallowed column suffixes/names.

**Verdict:** **Misses.**

**Countermeasure C5.2.** Add `rules/stub-columns-are-domain-fields-not-behavior.md`. Rule body:
- Forbid column names containing `_behavior`, `_response`, `_setup`, `_outcome`, `_action`, `_state` when paired with an external-system prefix.
- Require stub columns to follow the pattern `{system}.{field}` where `{field}` is an attribute of the response type in the service-specific domain model module.
- FAIL examples lifted from journal lines 373–381.

---

### Q5.3 — Does any rule force the author to look up the service-specific domain model module before writing stub columns?

**Source:** None — `abd-story-specification/SKILL.md` line 56 says read `domain-model.md` but does not say "read the service-specific module file under `docs/domain/model/modules/`".

**Verdict:** **Misses.**

**Countermeasure C5.3.** In `abd-story-specification/SKILL.md` `### 1. Read context`, add: "For every external system referenced in any scenario, also read `docs/domain/model/modules/{service}-domain-model.md`. If that file does not exist, flag the gap and stop — do not invent field names."

---

## Theme 6 — Scanners give false confidence; AI verification missing

### Q6.1 — What does `example-tables-domain-scanner.py` actually check?

**Source:** `practices/story-driven-delivery/skills/abd-story-specification/scanners/example-tables-domain-scanner.py` lines 175–290. The scanner walks each scenario's `examples_columns`, applies a denormalization heuristic on column shape (lines 220–252), and counts concept families across columns (lines 254–290). **It never reads the table's name/heading.**

**Verdict:** **Confirms the gap from journal line 225.**

**Countermeasure C6.1.** See C5.1.

---

### Q6.2 — Does any scanner inspect example-table cell contents?

**Source:** `then-asserts-concrete-output-scanner.py` lines 86–120. The scanner walks `scenario.steps` only and checks each Then/And step for `{token}`, `*italic*`, or `"quoted"`. Cell content is never inspected.

**Verdict:** **Misses.**

**Countermeasure C6.2.** Add `scanners/example-cells-are-atomic-data-scanner.py`:
- For every cell in every Examples table, fail if the cell contains a verb-like word from a small list (`respond`, `succeeds`, `returns`, `creates`, `responds`, etc.) OR is longer than ~40 characters without being a recognizable atomic literal (number, ISO timestamp, UUID, JSON-able primitive).
- Pair with rule `rules/example-cells-are-atomic-data.md`.

---

### Q6.3 — Does any scanner enforce post-write placeholder absence in diagram files?

**Source:** No file in `practices/*/skills/*/scanners` matches that responsibility. The diagram-sync scripts (under `drawio-domain-sync/scripts`, `drawio-story-sync/scripts`) write XML but I see no shared "fail if `{` remains in the output" verifier.

**Verdict:** **Misses.**

**Countermeasure C6.3.** Add a tiny shared verifier under `common/scripts/verify_no_placeholders_remain.py`. Every skill that writes a templated file (diagram sync, scaffold copy, etc.) should call it as the last step of its `## Diagram workflow` / `### 2. Generate` block. Make it part of the `## Validate` checklist in any skill that writes from a template.

---

### Q6.4 — Does the CDD orchestrator say "AI must independently verify rule compliance even when scanners pass"?

**Source:** `abd-context-driven-delivery/SKILL.md` line 82 says "Check diagram outputs — inspect the skill's `## Diagram workflow` section". No general "scanners are necessary but not sufficient" rule.

**Verdict:** **Misses.**

**Countermeasure C6.4.** Add to `common/skill-workflow.md` or to a new `common/scanner-is-not-sufficient.md`: "Scanners check what they were designed to. After every scanner pass, the agent MUST also read the upstream source (domain model, story map, fixture data) and independently verify the artifact matches it. A clean scanner output is permission to look harder, not permission to stop."

---

## Theme 7 — Stubs and fixtures duplicated by hand instead of referenced

### Q7.1 — Does any rule in the engineering / acceptance-test skills require fixtures to reference stub data rather than duplicate it?

**Source:** `practices/story-driven-delivery/skills/abd-story-acceptance-test` exists. The skill-index entry (lines 308–319) lists a `Stub fixture completeness` grill prompt. I have not opened the rules folder yet, but the journal correction (lines 259–270) introduces this rule for the first time — implying it was not present.

**Verdict:** **Likely misses** — needs confirmation by opening the skill's `rules/` folder.

**Countermeasure C7.1.** Add `rules/scenario-fixtures-reference-stub-data.md` to `abd-story-acceptance-test/rules/`:
- DO: build scenario fixtures by composing from `stubs/data/` exports.
- DO NOT: manually reconstruct a fixture object whose data already exists in `stubs/data/`.
- DO NOT: hardcode display strings derived from stub values; derive them from the canonical constant.
- FAIL examples lifted from journal lines 261–268.
- Optional scanner: a small AST/regex walk that flags hand-typed literals in fixtures matching values present in `stubs/data/`.

---

## Theme 8 — Domain code map conventions inconsistent across system roles

### Q8.1 — Does `abd-domain-model` or `abd-domain-specification` define a `domain-code-map.md` artifact?

**Source:** `rg "domain-code-map|code map" c:\dev\abd-skills\practices\domain-driven-design` returns **no results**. The artifact does not exist in the DDD practice at all.

**Verdict:** **Misses entirely.** The domain code map is a real artifact this session needed; it has no skill, no template, no rules, no scanner.

**Countermeasure C8.1.** Create a new supporting skill: `practices/domain-driven-design/skills/supporting/abd-domain-code-map/SKILL.md`. The skill must:
- Take a canonical `domain-model.md` (or `domain-specification.md`) as input.
- Emit `domain-code-map.md` with **role-aware column sets** (client / proxy-mediator / domain-service) — exactly as journal lines 291–314 prescribe.
- Use the heading conventions from journal lines 273–287 (KA = canonical concept name; class heading carries `Concept → ImplementationType — path/to/file.ts`).
- Be **required output** when reverse-engineering an existing system; the orchestrator's Specification stage should flag its absence.
- Support multi-layer mode: one canonical operation list under `domain-model.md`; each system's code map references the same canonical row by id.

---

### Q8.2 — Does the orchestrator know that an existing-system Specification stage needs a code map?

**Source:** The Specification stage in `abd-context-driven-delivery/SKILL.md` line 174 lists `abd-domain-specification + abd-domain-walk`. No mention of a code map.

**Verdict:** **Misses.**

**Countermeasure C8.2.** In the Specification stage of the orchestrator checklist (line 174), add `abd-domain-code-map` as a step **conditional on "system being specified is existing code"**. Mark it required when the entry point was Context (sandbox + extract).

---

## Theme 9 — Story map ↔ graph ↔ spec ↔ test alignment is a cleanup pass, not a gate

### Q9.1 — Does `story-graph-ops` enforce MD ↔ JSON parity?

**Source:** `practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md` line 175 lists `md_story_map_to_story_graph.py` — a one-way MD → JSON converter. No reverse script (JSON → MD), no parity checker, no guard preventing JSON-only patches.

**Verdict:** **Misses.** The conversion is unidirectional; nothing prevents the JSON from being edited without the MD.

**Countermeasure C9.1.** Add either:
- (a) A parity script `scripts/check_story_map_graph_parity.py` that re-runs the MD → JSON conversion and diffs against the on-disk JSON; non-zero diff = error. Run it from a new rule + scanner.
- (b) A `story-graph-ops` CLI guard mode that refuses to write the JSON unless the corresponding MD has been touched within N seconds, or unless `--allow-md-stale` is passed (so any drift becomes a conscious decision).

---

### Q9.2 — Does `abd-story-specification` require reading the story map before writing `## Story:` headings?

**Source:** `abd-story-specification/SKILL.md` `### 1. Read context` (lines 49–63) lists Class Model, domain model, domain language — but does NOT list `story-map.md` as a required read.

**Verdict:** **Misses.**

**Countermeasure C9.2.** Add `story-map.md` (or `story-graph.json`) as a **first mandatory read** in `abd-story-specification/SKILL.md` `### 1. Read context`. Add a rule `rules/spec-story-headings-match-story-map.md`:
- Every `## Story:` heading in the spec must appear in `story-map.md` as a sub-epic.
- No `## Story:` heading may be invented.
- Scanner: parse spec `## Story:` lines; parse story-map sub-epics; diff; report any heading-only-in-spec or sub-epic-only-in-map.

---

### Q9.3 — Is alignment a gate or a cleanup in the current orchestrator?

**Source:** `abd-context-driven-delivery/SKILL.md` `### 6. Consistency checks` (lines 107–116) runs after each skill generates output. It checks Glossary / Behaviour / Structure / Scope. There is no **pre-generation** gate for "story map ↔ graph ↔ spec heading count agreement".

**Verdict:** **Misses.** Consistency check is post-generation by design.

**Countermeasure C9.3.** Introduce a `pre-generation alignment check` for the Specification stage:
- Before any `abd-story-specification` run, verify story-map sub-epics ↔ graph sub-epics ↔ existing `## Story:` headings agree. Any mismatch is a **blocker**, not a note. Resolve in order: MD → graph → spec — never out of order.

---

## Theme 10 — Diagram / template tooling silently fails on HTML entities

### Q10.1 — Do the existing diagram-sync scripts write XML from templates, and how?

**Source:** `practices/story-driven-delivery/skills/supporting/drawio-story-sync/`, `practices/domain-driven-design/skills/supporting/drawio-domain-sync/`. I have not opened the writer scripts in this turn, but the journal correction (lines 135–139) is explicit that a Python `str.replace` against a draw.io template containing `&#10;` no-ops silently.

**Verdict:** **Pattern is risky regardless of which script.** Any code that does naive `str.replace` against XML templates has this hazard.

**Countermeasure C10.1.**
- (a) Adopt `xml.etree.ElementTree` (or `lxml`) for any draw.io XML mutation — never `str.replace`.
- (b) Add the post-write placeholder verifier from C6.3 to every diagram-sync `## Validate` block.
- (c) Document this hazard in `common/skill-workflow.md` so every future template-driven skill inherits the guidance.

---

## Theme 11 — Semantic ↔ implementation drift surface (HTTP 401 vs 403)

### Q11.1 — Does the orchestrator's consistency check distinguish structural alignment from semantic correctness?

**Source:** `abd-context-driven-delivery/SKILL.md` lines 107–116 lists Glossary / Behaviour / Structure / Scope. **Behaviour** is the closest match — but it is described as "stories, UX, and architecture must describe the same interactions", which is symbol-level, not code-execution-level.

**Verdict:** **Misses.** There is no consistency-check tier for "AC's expected outcome vs what the current code actually does at runtime".

**Countermeasure C11.1.** Add a 5th consistency dimension: **Semantic Outcome** — for every AC scenario, the expected response code / payload shape / observable side-effect must be traceable to a corresponding execution path in the codebase. Where it is not, generate a tracked **Implementation Gap** entry in a new artifact `docs/cdd-sessions/<date>/implementation-gaps.md` — not a paragraph buried in the journal.

This raises the journal's 401/403 finding from a recommendation to a tracked, namespaced action item.

---

## Cross-theme — countermeasures that pay down multiple themes at once

| Countermeasure | Pays down |
|---|---|
| Add explicit "existing application + no extraction → Context" entry-point rule (C1.1) and treat attached skills as signals (C1.2) | Theme 1 |
| Add "corrections are mandatory from response 1" to `cdd-resume.prompt.md` (C1.3) | Theme 1, partly 2 |
| Strengthen grill skill: one-question count check + "answer yourself first" loop (C2.1, C2.2) | Theme 2 |
| Bulk rename `docs/sessions/` → `docs/cdd-sessions/` + lint pass (C3.1) | Theme 3 |
| Sub-plan expansion rule for nested-plan skills (C3.2) | Theme 3 |
| Two-phase proxy rule + boundary system+operation rule + proxy-specific Given FAIL examples (C4.2, C4.3, C4.4) | Theme 4 |
| Add table-name validation to existing scanner (C5.1) + new stub-column rule and scanner (C5.2, C6.2) | Themes 5, 6 |
| Service-specific domain-model-module mandatory read (C5.3) | Themes 5, 8 |
| Shared `verify_no_placeholders_remain.py` (C6.3) used by every templated writer (C10.1) | Themes 6, 10 |
| "Scanner is not sufficient" cross-cutting rule (C6.4) | Theme 6 |
| New `abd-domain-code-map` skill, conditionally required in Specification (C8.1, C8.2) | Theme 8 |
| MD ↔ JSON parity guard for story-graph-ops (C9.1) + spec-headings-match-story-map rule (C9.2) + pre-generation alignment gate (C9.3) | Theme 9 |
| Semantic-outcome consistency tier + `implementation-gaps.md` tracked artifact (C11.1) | Theme 11 |

---

## What this list is NOT yet

- Not implementations. Every countermeasure names the file path and the type of change; none has been applied.
- Not prioritized. Sequencing is a separate exercise once the user picks which themes to address first.
- Not exhaustive. Several rule files were referenced by name (`given-describes-state-not-actions.md`, `stub-service-interaction-structure.md`) but not opened line by line in this pass — the deep-dive notes below in `code-research/agent-2-deep-dive/` go deeper on the highest-leverage areas.
