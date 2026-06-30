# Delivery graph — generated read-gate injection (Phase 6.5)

> **Status:** Proposal. Sits next to `c:\dev\abd-skills\docs\delivery-graph-solution.md` without modifying it. Names the missing mechanism between the *plan* (Phase 6 "read-gates on pilot skills") and the *outcome* (artifacts get used, not skipped).
>
> **One-line shape:** Convert the existing `sessionStart` / `userPromptSubmitted` hooks from emitting a hand-written paragraph into emitting an **instruction generated from the taxonomy + the context graph + the active skill's front matter** — so the agent is told, every turn, exactly which upstream artifacts to load and what to do if they're missing.

---

## Problem this addresses

`delivery-graph-solution.md` lines 11–13:
> "Skills are told to 'read upstream artifacts,' which is expensive in tokens and easy to skip. Connections drift because they are copied into prose instead of declared once."

The skill prose says "read upstream first." The session journal of
`2026-06-26-reverse-engineer-discovery-to-test` shows agents skipping it repeatedly (themed problems 2, 5, 7, 8, 9, plus the meta-theme "artifacts not used").

Static prose in each `SKILL.md` is the wrong layer. The right layer is the
**injection hook that already exists** and already prepends a standing
instruction to every response.

---

## What already exists — and what it does not do today

| Asset | Path | What it does | What it does not do |
|---|---|---|---|
| Hook definition | `practices/context-driven-delivery/hooks/detect-cdd-corrections.json` | Wires `sessionStart` → `session-setup.ps1` and `userPromptSubmitted` → `detect-correction.ps1` | n/a |
| sessionStart hook script | `practices/context-driven-delivery/scripts/session-setup.ps1` | Returns `{additionalContext: "<paragraph>"}` JSON that gets prepended to context | Paragraph is **hand-written**; ignores active skill, taxonomy, context graph, and `cdd-context-index.md` |
| userPromptSubmitted hook script | `practices/context-driven-delivery/scripts/detect-correction.ps1` | Pattern-matches correction phrases in the prompt; appends to `corrections-pending.md` | Detects *the user correcting the agent*; does nothing to *prevent* the next failure |
| Taxonomy (perspective + fidelity dependencies) | `common/context-taxonomy.md` lines 22, 36–41, 64–80 | Declares perspective order, fidelity ladder, YAML front matter for every skill | Prose only; nothing parses it at runtime |
| Context index (non-canonical paths) | `common/context-scaffold/cdd-context-index.md` + `common/folder-conventions.md` § "Non-standard locations" | Maps artifact → actual file when paths deviate | **Not autoloaded** into the injected context; agent must find it manually |
| Delivery-graph design | `docs/delivery-graph-solution.md` lines 384–391 (Phase 6 "Read time") | Specifies the runtime contract: load graph → resolve scope → fetch upstream → flag gaps | The script that performs it does not exist yet |

**Net:** every piece of the dependency knowledge is already on disk. Nothing assembles it at hook time.

---

## The mechanism — generated read-gate injection

A small generator runs in the existing hooks. Its job is to produce
**`additionalContext`** that names, for the active skill and scope:

1. The active skill (name + perspective + fidelity, parsed from the skill's YAML front matter).
2. The required upstream perspectives (looked up in the taxonomy).
3. The specific upstream nodes (resolved via context-graph edges, when the graph exists).
4. The file paths and semantic pointers to load.
5. The required failure mode if any of the above is missing: **flag a gap, do not fabricate** — reference `practices/story-driven-delivery/reference/handling-incomplete-context.md`.
6. The content of `cdd-context-index.md` so non-canonical paths are visible from the first turn.
7. The corrections-pending check (the only thing the current hook does).

The author of a new skill does **nothing extra** to opt in. The skill's existing YAML front matter is the input; the taxonomy + context graph supply the rest.

---

## Generated instruction — template

The hook emits this `additionalContext` (filled per turn):

```
You are in a Context-Driven Delivery session.

## Read-gate for this turn

Active skill: {active_skill_name}
  context-perspective: {perspective}
  context-fidelity: {fidelity_level} ({mode})

Required upstream perspectives (from common/context-taxonomy.md):
  {ordered_list_of_upstream_perspectives}

Required upstream artifacts for the current scope:
{upstream_artifact_table}

Mandatory pre-step BEFORE generating any output this turn:
  1. Load every file listed under "Required upstream artifacts".
  2. If any file is missing, OR any required pointer does not resolve, OR
     scope cannot be determined: stop. Flag the gap in chat using the
     "flag a gap" protocol in
     practices/story-driven-delivery/reference/handling-incomplete-context.md.
     Do not fabricate names, columns, table headings, or scenarios.
  3. Only after upstream is loaded, proceed with the user's request.

## Non-canonical paths (from cdd-context-index.md)

{verbatim_contents_of_cdd_context_index_or_"none"}

## Pending corrections

{contents_of_corrections_pending_or_"none"}
```

The `{upstream_artifact_table}` is the **dependency-derived list**, e.g.:

```
| Perspective   | File                                            | Pointer / scope                                      | Rule                                                         |
|---------------|-------------------------------------------------|------------------------------------------------------|--------------------------------------------------------------|
| domain        | docs/domain/model/domain-graph.json             | modules/Catalog                                       | Use attribute names verbatim in example-table columns        |
| domain        | docs/domain/model/domain-graph.json             | modules/Catalog/classes/Product                       | Table NAMES must match concept names; cells must be atomic   |
| stories       | docs/stories/story-map/story-graph.json         | epics/Shop in store                                   | Spec `## Story:` headings must match graph story names       |
| (path index)  | docs/cdd-context-index.md                        | n/a                                                   | Use overrides listed there before falling back to scaffold   |
```

A skill consuming this **cannot plausibly claim "I didn't know which domain concepts to use"** — they are listed by file and pointer in the same context that the user's prompt arrives in.

---

## Generator inputs and lookups

### 1. Detect the active skill

| Source | How |
|---|---|
| Attached skills on the latest user message | The hook payload (`detect-cdd-corrections.json` already receives `$data` from stdin) — extend to read attached skill list when present |
| Latest `## Skill: X` header in the session journal | Fall-back when no skill is attached |
| Active checklist row in `cdd-session-checklist.md` | Final fall-back — pick the unchecked row in the rightmost-stage column |

If none of the above resolve, the generator emits a **degraded** instruction:
"No active skill detected. Before any generation, read the orchestrator skill at `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` and run its `### 1. Assess entry point` step."

### 2. Parse the active skill's front matter

```yaml
context-perspective: stories
context-fidelity:
  - level: specification
    mode: scenario
```

Already standardized in `common/context-taxonomy.md` lines 64–80. A short YAML reader (a dozen lines of PowerShell / Python) returns `{perspective, fidelity_level, mode}`.

### 3. Resolve upstream perspectives from the taxonomy

`common/context-taxonomy.md` line 22 declares the order:
`domain → stories → ux → architecture`

Rule: for perspective `P`, all perspectives left of `P` in this order are **mandatory upstream**. Stage skills (`perspective = stage`) inherit the upstream of the perspective they currently serve, determined from the active skill's parent practice in the journal.

### 4. Resolve scope-specific upstream nodes from the context graph

When `docs/context/context-graph.json` exists (delivery-graph Phase 1+):

1. Determine current scope node id from the kanban / session checklist / user prompt.
2. Filter edges where `source` or `target` is the scope node and `type` is in the perspective-specific set:
   - `perspective=stories` → require edges of type `exercises` (→ domain) and `surfaces-through` (→ ux).
   - `perspective=ux` → require edges of type `presents` (→ domain) and `enables` (→ stories).
   - `perspective=architecture` → require `implements` (→ stories, ux) and `realizes` (→ domain).
   - `perspective=domain` → no required cross-view upstream (but still requires fidelity-ladder upstream from the previous stage).
3. For each resolved upstream node, look up `path` + `pointer` from the graph's node registry.

When `context-graph.json` does not exist yet, the generator falls back to listing the canonical files for upstream perspectives from `common/folder-conventions.md` (e.g. domain → `docs/domain/model/domain-model.md` + `docs/domain/model/domain.json`).

### 5. Always append `cdd-context-index.md`

Verbatim. Single shell read. If the file is empty (header only), emit `"none"` so the agent knows there are no overrides — versus the file being missing entirely (which is itself a gap).

### 6. Always include pending corrections

This is the only behavior the existing `session-setup.ps1` covers today (lines 14–22 of that script). Keep that block; prepend the read-gate above it.

---

## Hook script sketch — `session-setup.ps1` (rewritten)

```powershell
# session-setup.ps1 — sessionStart hook
# Emits a generated read-gate instruction + cdd-context-index + pending corrections.

$raw = $input | Out-String
if (-not $raw) { $raw = [Console]::In.ReadToEnd() }
try { $data = $raw | ConvertFrom-Json } catch { exit 0 }

$cwd = if ($data.cwd) { $data.cwd } else { (Get-Location).Path }

# 1. Detect active skill
$activeSkill = & "$PSScriptRoot/detect-active-skill.ps1" -SessionData $data -Cwd $cwd

# 2. Parse front matter
$frontMatter = if ($activeSkill) {
    & "$PSScriptRoot/read-skill-frontmatter.ps1" -SkillPath $activeSkill.path
} else { $null }

# 3. Resolve upstream perspectives from taxonomy
$upstreamPerspectives = & "$PSScriptRoot/resolve-upstream-perspectives.ps1" `
    -Perspective $frontMatter.perspective `
    -Fidelity $frontMatter.fidelity

# 4. Resolve scope-specific upstream nodes from context graph (if present)
$upstreamArtifacts = & "$PSScriptRoot/resolve-upstream-artifacts.ps1" `
    -Perspectives $upstreamPerspectives `
    -Cwd $cwd `
    -ScopeHint $data.prompt

# 5. Load cdd-context-index.md
$contextIndex = & "$PSScriptRoot/load-context-index.ps1" -Cwd $cwd

# 6. Load corrections-pending.md
$pendingCorrections = & "$PSScriptRoot/load-pending-corrections.ps1" -Cwd $cwd

# 7. Render instruction from template
$additionalContext = & "$PSScriptRoot/render-read-gate.ps1" `
    -ActiveSkill $activeSkill `
    -FrontMatter $frontMatter `
    -UpstreamPerspectives $upstreamPerspectives `
    -UpstreamArtifacts $upstreamArtifacts `
    -ContextIndex $contextIndex `
    -PendingCorrections $pendingCorrections

@{ additionalContext = $additionalContext } | ConvertTo-Json -Compress
```

`detect-correction.ps1` keeps its current job (append to `corrections-pending.md` when correction phrases are detected) and additionally **regenerates** the read-gate so it appears on the **next** turn with the new correction included in the pending block.

A Bash twin lives next to each script for non-PowerShell environments
(mirrors the existing `session-setup.sh` / `detect-correction.sh` pattern).

---

## Helper scripts to add

All under `practices/context-driven-delivery/scripts/`:

| Script | Input | Output |
|---|---|---|
| `detect-active-skill.ps1` / `.sh` | session payload + cwd | `{name, path, source: "attached"|"journal"|"checklist"|"none"}` |
| `read-skill-frontmatter.ps1` / `.sh` | skill path | `{perspective, fidelity: {level, mode}}` |
| `resolve-upstream-perspectives.ps1` / `.sh` | perspective, fidelity | ordered list `[domain, stories, …]` |
| `resolve-upstream-artifacts.ps1` / `.sh` | perspectives, cwd, scope hint | list `[{perspective, file, pointer, rule}]` |
| `load-context-index.ps1` / `.sh` | cwd | verbatim contents of `cdd-context-index.md` or `"none"` |
| `load-pending-corrections.ps1` / `.sh` | cwd | verbatim contents of `corrections-pending.md` or `"none"` |
| `render-read-gate.ps1` / `.sh` | all of the above | string for `additionalContext` |

Each helper is small, single-purpose, testable in isolation, and replaceable by a Python/TypeScript implementation later without touching the hook contract.

The graph query (`resolve-upstream-artifacts`) is the only one that depends on the delivery-graph being live. Until it is, it returns the canonical-folder fallback list and a marker like `# graph not yet available — falling back to folder-conventions.md`.

---

## How a skill author opts in

**They don't.** Opt-in is automatic for any skill that already follows
`common/context-taxonomy.md` lines 64–80 (every practice skill in `abd-skills` today). The skill author writes the skill the same way; the hook does the rest.

Two things a skill *should* do to take fullest advantage:

1. Keep front matter accurate. A skill mislabeled `context-perspective: domain` when it really authors story artifacts will get the wrong upstream list injected. The lint already exists implicitly (front matter is required) — adding a single scanner that checks every `SKILL.md` parses cleanly closes the loop.
2. Emit and read `id` / `pointer` consistently in the graphs. Phase 1 of the delivery-graph plan already requires this for `story-graph`; extending to `domain-graph` / `ux-graph` / `arch-graph` happens in Phases 3–5.

---

## How this composes with `handling-incomplete-context.md`

`practices/story-driven-delivery/reference/handling-incomplete-context.md` already specifies:
- "Assess context coverage before producing anything."
- "Don't fabricate to fill gaps."
- "Capture what is missing, state the assumption, recommend the validation action."

That document defines the **policy**. Today it is referenced by skill prose
that agents skim past. The injected read-gate makes the policy
**operational**: the upstream list is enumerated, the failure mode is named,
and the link to the policy doc is in the same paragraph. The policy file
remains the canonical reference; the hook makes it impossible to ignore.

---

## How this fixes the themed problems

| Theme | Mechanism |
|---|---|
| **C1 — single source of truth violated** | Generator's upstream list is mechanically derived from the same single sources (taxonomy + context graph + folder conventions). Discrepancy becomes a generator bug, not a per-skill discipline failure. |
| **C2 — gate, not cleanup** | The read-gate is in `sessionStart` and `userPromptSubmitted` — i.e. **before** the agent composes any reply. It cannot be deferred to a cleanup pass. |
| **Theme 1 — entry-point detection** | `detect-active-skill.ps1` honors attached skills as a strong signal. When `abd-context-app-sandbox` is attached, the generator emits a Context-phase read-gate, regardless of what later-stage artifacts exist. |
| **Theme 2 — grill: read first, ask later** | Grill turns get the same injection. The "Required upstream" list IS the list the grill skill must search before asking the user a single question. Failure mode is the same: flag gap, don't ask. |
| **Theme 5 — spec tables drift from domain** | `abd-story-specification` turns inject a row pointing at `docs/domain/model/domain-graph.json` plus the specific module pointer. The rule line says "table NAMES must match concept names; column names must match attribute names; cells must be atomic." |
| **Theme 7 — fixtures hand-typed** | Generator includes canonical fixture file paths (and once the graph is live, the specific fixture nodes) as required upstream for any `engineering`-fidelity skill that touches scenarios. |
| **Theme 8 — multi-layer code map drift** | All layers share the same generator output: one canonical `domain-graph.json` is named, regardless of which layer's code map is being authored. |
| **Theme 9 — story map ↔ graph ↔ spec drift** | Generator points spec authoring at `story-graph.json` as the only allowed source of `## Story:` headings; fallback path is `story-map.md`. Headings invented from route analysis become visibly inconsistent with the injected list. |
| **Theme 11 — semantic drift** | "Pending corrections" block includes journal-noted semantic gaps that are explicitly carried forward (a small journal convention adds them automatically). |

Themes 3 (folder drift), 4 (proxy semantics), 6 (scanner gaps), and 10
(template HTML entities) are independent — they need scanner / tool fixes,
not injection.

---

## Failure modes the generator must handle gracefully

| Condition | Generator behavior |
|---|---|
| No active skill detectable | Emit degraded "load the orchestrator skill first" instruction (see Detect 1 above). Do not fail the hook. |
| Active skill has no front matter | Emit the degraded instruction + name the missing front matter as a defect. |
| `cdd-context-index.md` missing | Emit `"none"` under that section. The orchestrator's job is to scaffold the file; do not fail. |
| `context-graph.json` missing | Fall back to folder-conventions canonical paths; mark the table with `# graph not yet live`. |
| Scope unresolvable | Emit the full perspective-level upstream list (no scope filter). Agent still gets pointed at the right files; just not at the specific node. |
| Hook script error | Hook contract already permits silent `exit 0`. Log to a sibling file (`.cursor/logs/hook-errors.log`) so failures are recoverable. |

Every failure mode degrades to *more* injected context, never less. The
worst case is the current behavior (static paragraph).

---

## Phasing within delivery-graph-solution.md

Slot under existing Phase 6. Re-read the original plan's Phase 6:
> "Read-gates on pilot skills (`abd-story-specification`, `abd-ux-mockup`, `abd-architecture-specification`) — Index-first context"

This proposal makes Phase 6 a runtime mechanism, not a per-skill prose edit:

| Step | Deliverable | Notes |
|---|---|---|
| **6a** | Rewritten `session-setup.{ps1,sh}` + 7 helper scripts (folder-conventions fallback only) | Works even before `context-graph.json` exists |
| **6b** | `cdd-context-index.md` autoload + `corrections-pending.md` autoload | Cheapest win; closes the "non-canonical path is invisible" gap |
| **6c** | `resolve-upstream-artifacts.ps1` graph-aware path | Lights up after delivery-graph Phase 2 (context-graph-ops CLI) |
| **6d** | Front-matter lint scanner | Per `common/context-taxonomy.md`; prevents silent generator misbehavior |
| **6e** | Eval fixture: "ignored upstream link" | Per delivery-graph Phase 7. A test prompt where the upstream is present but the agent must demonstrate it was read (e.g. by quoting a node pointer). |

6a + 6b are deliverable in isolation against the current state of
`abd-skills` — no new graph required. They convert the static paragraph
into a generated, dependency-aware one and close the cdd-context-index
"silent override" gap immediately.

---

## Open questions

1. **Active-skill detection signal strength.** Is the attached-skill list reliably available in `userPromptSubmitted` payloads in Cursor? If yes, that's the strongest signal. If not, the journal-based detection is the working fallback. (Either way, the orchestrator skill should explicitly write the active skill name to the journal at the start of each turn — separate small scope.)
2. **Scope hint extraction.** A naive parser of `$data.prompt` for epic / story names is fragile. Better: the orchestrator pins the active scope into a `cdd-active-scope.md` next to the journal. The generator reads that file. Simpler and explicit.
3. **Token budget.** Injecting the full `cdd-context-index.md` + corrections-pending + an upstream table can grow. Cap at a known size (e.g. 4 KB total injected context) and degrade to "see X for full list" when over.
4. **Multi-skill turns.** A turn may run two skills (e.g. story-map then drawio-story-sync). The generator emits the read-gate of the **first** skill in the chain; subsequent skills produce their own gate when the orchestrator transitions.
5. **Symmetry with `cdd-resume.prompt.md`.** The resume prompt should run the same generator (statically expanded into the resume message) so resumed sessions see the same read-gate as a fresh sessionStart.

---

## What this is not

- **Not a replacement for the skills themselves.** Each skill's `## Build` step still exists; the injection adds a precondition.
- **Not a substitute for the context graph.** The generator works with folder-conventions fallback today, but it gets much sharper once `context-graph.json` exists.
- **Not a way to skip grilling.** Grill turns receive the same upstream list — the grill skill's first job becomes "search the listed upstream for an answer before asking the user."
- **Not a code-gen of skill prose.** Authors still write skill prose. The injection complements it; it does not replace `SKILL.md`.

---

## References

| Piece | Path |
|---|---|
| Delivery graph solution (the parent design) | `c:\dev\abd-skills\docs\delivery-graph-solution.md` |
| Context taxonomy (perspective + fidelity dependencies) | `c:\dev\abd-skills\common\context-taxonomy.md` |
| Folder conventions (canonical paths fallback) | `c:\dev\abd-skills\common\folder-conventions.md` |
| Context index scaffold | `c:\dev\abd-skills\common\context-scaffold\cdd-context-index.md` |
| Existing sessionStart hook | `c:\dev\abd-skills\practices\context-driven-delivery\scripts\session-setup.ps1` |
| Existing userPromptSubmitted hook | `c:\dev\abd-skills\practices\context-driven-delivery\scripts\detect-correction.ps1` |
| Hook wiring file | `c:\dev\abd-skills\practices\context-driven-delivery\hooks\detect-cdd-corrections.json` |
| Incomplete-context policy | `c:\dev\abd-skills\practices\story-driven-delivery\reference\handling-incomplete-context.md` |
| abd-skills domain model (terms used in this doc) | `c:\dev\abd-skills\docs\domain\abd-skills-domain-model.md` |
| Themed problems this addresses | `./themed-problems.md` |
| Self-grill + per-theme countermeasures | `./self-grill-and-countermeasures.md` |
