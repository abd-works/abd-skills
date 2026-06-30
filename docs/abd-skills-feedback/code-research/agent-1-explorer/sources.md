# Code Research — Pass 1 Explorer: raw source notes

All excerpts are verbatim from `c:\dev\abd-skills` as read this session. File paths are relative to the abd-skills repo root. Line numbers are inclusive ranges.

---

## Path: CDD Orchestrator Entry Point — Source notes

### practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md  lines 39–54

```markdown
### 1. Assess entry point

1. Scan the workspace for existing skill outputs.
   - **First:** check `cdd-context-index.md` at the workspace root — it lists every artifact at a non-standard path. If a path is listed there, use it directly without searching.
   - **Then:** use the scaffold tree in `folder-conventions.md` — look under `docs/domain/`, `docs/stories/`, `docs/ux/`, `docs/architecture/`, and `docs/sessions/`.
   - **Also:** use the output filenames in `skill-index.md` as a second cross-reference.
   - Time-box this — if not obvious, ask the user where outputs live.
2. Review what exists against the current ask. At each fidelity level (see common/context-taxonomy.md`), does the existing artifact cover the ask?
3. Recommend an entry point:
   - No workspace memory or source material needs ingesting → context
   - Memory exists, nothing shaped → shaping
   - Scope defined but interactions are not → discovery
   - Stories exist but need refinement → exploration
   - Stories refined, concrete behaviour missing → specification
   - Specification done, code needed → engineering
4. Present and confirm with the user. Do not proceed until confirmed.
```

Observations:
1. Line 43 uses the legacy `docs/sessions/` path — duplicate evidence for the folder-conventions path below.
2. The entry-point conditions (lines 47–53) do not include "existing running application + no `docs/external/app-extraction/` artifacts → context (run abd-context-app-sandbox + abd-context-app-extractor)".
3. The step does not say "read any skills attached to the user's opening message — treat them as routing signals".

### practices/context-driven-delivery/skills/cdd-handoff/SKILL.md  lines 19–25

```markdown
## Output

No new file. Append a `## ↓ RESUME POINT` block to the bottom of:

```text
<workspace>/docs/cdd-sessions/<YYYY-MM-DD>-<topic>/cdd-session-checklist.md
```
```

Observation: uses the new canonical `docs/cdd-sessions/` path. Inconsistent with `abd-context-driven-delivery/SKILL.md` line 43.

### practices/context-driven-delivery/prompts/cdd-resume.prompt.md  lines 60–67

```markdown
## 5. Session state management

- Update the checklist after each completed cell.
- Append to the journal with `Ran` lines and any new grill Q→A.
- If the user provides corrections, add them to the journal `## Corrections` section and re-run the affected cell.
```

Observation: corrections are mentioned as something the user newly provides. Nothing in this prompt instructs the agent to enumerate **existing** journal corrections as a mandatory preflight before any other work.

### practices/context-driven-delivery/instructions/cdd-self-correction.instructions.md  lines 14–34

```markdown
## Non-negotiable order

1. **Write the correction first.** Append to `## Corrections` in the active
   `docs/cdd-sessions/<date>-<topic>/cdd-session-journal.md`. Use this format:

   ```markdown
   - **DO NOT** [rule]
     - Example (wrong): [what you did]
     - Example (correct): [what should have happened]
   ```

2. **Then** fix the output or answer the user.
```

Observation: correctly enforces logging when a new correction is signaled in the current turn. Does not address how a *fresh agent* on resume should load and apply existing corrections.

---

## Path: Grill Skill — Source notes

### common/grill-me-with-practice-skill.md  lines 11–22

```markdown
When a skill is invoked **without** "grill me", it generates directly. Grill mode is opt-in. **If "grill me" was not in the invocation — stop reading this file and proceed with generation.**

---

## Purpose

You are grilling to establish shared understanding at the **current fidelity level**. Your questions are shaped by what the practice skill at this perspective and fidelity needs as input. You validate that understanding by running the skill — the generated output confirms or reveals gaps. Stay focused at one fidelity level until it's resolved before moving deeper.

You must ask questions **one at a time**, waiting for feedback before continuing.

If a question can be answered by reading existing skill outputs or the codebase, read them instead of asking. Use `common/skill-index.md` output filenames to know what to look for.
```

Observations:
1. Line 11 says grill mode is opt-in — a signal that contradicts the CDD orchestrator's instruction to grill at each cell.
2. Line 19 says "ask one at a time" — but no detection or self-check enforces it.
3. Lines 21–22 hint at "read first, ask later" but stops short of a procedure.

### common/grill-me-with-practice-skill.md  lines 60–66

```markdown
## Where your questions come from

The gap between what the ask needs and what already exists. Also:

- **Skill grill prompts** in the active skill's `## Grill prompts` section — input traps specific to this skill at this perspective and fidelity level.
- **Skill rules** — each FAIL example in a skill's `rules/*.md` implies a question.
```

Observation: the *sources* of questions are listed, but the ordered procedure "for each candidate question, publicly answer from these sources first; only surface to the user what cannot be answered" is not stated.

---

## Path: Folder Conventions & Session Paths — Source notes

### Grep "docs/sessions/" c:\dev\abd-skills — files with matches

```
practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md
practices/context-driven-delivery/scripts/session-setup.ps1
practices/context-driven-delivery/scripts/session-setup.sh
practices/context-driven-delivery/scripts/detect-correction.ps1
practices/context-driven-delivery/scripts/detect-correction.sh
common/decision-record.md
docs/eval-loop-planning.md
catalog/doc/skill/abd-context-driven-delivery/SKILL.html
```

Observation: 8 files still reference the legacy path; `cdd-handoff/SKILL.md` and the session journal template appear to use the new path. The rename is partly complete.

---

## Path: Story Specification — Rules & Scanners — Source notes

### practices/story-driven-delivery/skills/abd-story-specification/SKILL.md  lines 49–63

```markdown
### 1. Read context

Read these files:
- **`reference/concepts.md`** — what specification by example is, Given/When/Then, scenarios vs outlines, domain concept grounding, quick checklist.
- **`reference/examples.md`** — worked examples showing plain Scenarios, Scenario Outlines with relationship-based tables, and Background.

**Default input — domain model outline:** Always read the domain model before writing any scenario. The domain model outline is the structural spine for all scenarios: concept names, relationships, invariants, and constraints come from there verbatim.

Read in this priority order:
- **Class Model** (`domain-specification.md`) — typed classes with invariants and typed relationships. Use first when present.
- **Domain model** (`domain-model.md`) — concepts with responsibilities and collaborators. **Default source** when no Class Model exists.
- **Domain language** (`domain-language.md`) — defined terms and key abstractions. Use for term verification and when no model file exists.
```

Observations:
1. No mandatory read of `story-map.md` or `story-graph.json`.
2. No mandatory read of per-service domain-model modules (`docs/domain/model/modules/{service}-domain-model.md`).

### practices/story-driven-delivery/skills/abd-story-specification/rules/example-tables-use-domain-language.md  lines 15–24

```markdown
## Grounded mode (domain model exists)

When an Class Model, domain model, or domain language glossary is available in the workspace or has been provided as context:

- **Table names** MUST correspond to a concept in the domain model (Class Model class, domain model card, or domain-language term). The match is case-insensitive.
- **Column names** MUST correspond to attributes or fields of that concept as defined in the domain model. The match normalizes casing and underscores (`purchased_rank` matches `purchasedRank`).
- **Inheritance applies** — if concept B inherits from concept A, a table named B may use any attribute from both B and A (resolved transitively up the chain).
- **Cross-references** — a column that references another concept by name (e.g. a foreign key) is valid if that concept exists in the domain model.
- The `scenario` column is a universal row-label alias and always passes validation.
```

Observation: rule **text** explicitly requires table names and column names to match. The scanner implements only the column check (see next excerpt).

### practices/story-driven-delivery/skills/abd-story-specification/scanners/example-tables-domain-scanner.py  lines 207–252

```python
def scan_story_node(self, node: Any) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if not isinstance(node, Story):
        return violations

    for scenario in node.scenarios:
        if not scenario.has_examples:
            continue

        cols = scenario.examples_columns

        # --- Denormalization heuristic (always runs, even without vocab) ---

        numbered = _detect_numbered_suffix_columns(cols)
        if numbered:
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=(
                        f'Story "{node.name}" outline "{scenario.name}": '
                        f"columns {numbered} look like numbered denormalization "
                        f"(e.g. owner_1_name, owner_2_name). One-to-many "
                        f"relationships belong in a separate table, not as "
                        f"extra columns."
                    ),
                    severity="error",
                ).to_dict()
            )

        example_tables = scenario.examples or []
        table_count = len(example_tables)

        if table_count <= 1 and len(cols) > DENORM_COLUMN_THRESHOLD:
            violations.append( ... ) # column-count check
```

Observation: the scanner reads `scenario.examples_columns` and `scenario.examples` (the table objects) but only validates **column** names. There is no reference to a `table_name` attribute against domain concepts.

### practices/story-driven-delivery/skills/abd-story-specification/scanners/then-asserts-concrete-output-scanner.py  lines 76–121

```python
class ThenAssertsConcreteOutputScanner(StoryScanner):

    def scan_story_node(self, node: Any) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        if not isinstance(node, Story):
            return violations

        for scenario in node.scenarios:
            if not scenario.has_examples:
                continue

            in_then_block = False
            for step in scenario.steps:
                stripped = step.strip()
                lower = stripped.lower()

                if lower.startswith("then "):
                    in_then_block = True
                elif lower.startswith("when ") or lower.startswith("given "):
                    in_then_block = False
                    continue

                if not in_then_block:
                    continue

                if not _is_then_or_continuation(stripped):
                    continue

                if _is_navigation_only(stripped):
                    continue

                if not _has_assertable_value(stripped):
                    ...
```

Observation: the scanner iterates `scenario.steps` only. Example-table **cells** are never inspected. Cell content like `respond HTTP 409 Conflict (cart already exists)` could never be flagged by this scanner.

### practices/story-driven-delivery/skills/abd-story-specification/rules/stub-service-interaction-structure.md  lines 6–25

```markdown
## Pattern

**GIVEN** — declare the stub: the service name, the hardcoded request it expects, and the hardcoded response it returns. This is configuration state, not behavior.

**WHEN** — express the full observable interaction as a sequence:
- the system captures or receives the triggering input
- the system forwards or invokes the stubbed service with the fixed request
- the stubbed service returns the fixed response

**THEN** — assert the business outcome only. Never assert what a stubbed service returns; that is already fixed in GIVEN.

## DO

```gherkin
Given *PaymentGateway* is stubbed to receive charge request for *$120.00 AUD* and return *transaction-id: TXN-9912, status: approved*
When the *Checkout* captures *order #4471* with total *$120.00 AUD*
  And the *Checkout* forwards the charge request to *PaymentGateway*
  And *PaymentGateway* returns *transaction-id: TXN-9912, status: approved*
Then the *Order #4471* status is *Paid*
```

Observation: the rule defines a single WHEN block containing `system forwards` and `service returns` as `And` continuations. This is **not** the two-phase **When → Then → When → Then** pattern that midtier proxies require according to the session journal (lines 231–234). The rule covers stub partitioning but not proxy two-phase flow.

---

## Path: Story Graph Operations & MD ↔ JSON Sync — Source notes

### practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md  lines 162–215

```markdown
## Converting Markdown to story-graph.json

| `md_story_map_to_story_graph.py` | abd-story-mapping | `story-map.md` tree → epics, sub-epics, stories |

…

```bash
python scripts/md_story_map_to_story_graph.py <input-story-map.md> <output-story-graph.json>

python scripts/story_graph_cli.py read  --file <output-story-graph.json>
python scripts/story_graph_cli.py names --file <output-story-graph.json>
```

Merges acceptance criteria from an `acceptance-criteria.md` file into an **existing** `story-graph.json`. Matches by story name; injects numbered AC strings (preserving WHEN/THEN/AND/Evidence format) without disturbing scenarios or other fields.
```

Observations:
1. Pipeline is unidirectional: MD → JSON.
2. There is no `--check-parity` or `--verify-md-matches-json` flag in `story_graph_cli.py` shown in the SKILL body.
3. A patch script that mutates the JSON directly does not get caught — the JSON is the only artifact under CLI guardianship.

### practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md  lines 286–303

```markdown
`story-graph.json` is **shared mutable state** across the delivery flow — every stage mutates the same file. The planning skill allows **parallel runs** when outputs are independent (e.g. story definition for one slice while discovery continues for another). The policy and the mechanical safeguards are:

…

    SHA=$(python scripts/story_graph_cli.py sha --file story-graph.json)

    python scripts/story_graph_cli.py write --file story-graph.json --expect-sha $SHA --input new.json
```

Observation: the conflict-avoidance mechanism (SHA-stamped writes) protects against concurrent edits but does nothing about MD ↔ JSON parity.

---

## Path: Diagram Sync & Template Writing — Source notes

### Observation, not file excerpt

`Grep "verify_no_placeholders|placeholder" c:\dev\abd-skills\common` returned no helper script for post-write placeholder verification. The two diagram-sync skill folders (`drawio-story-sync`, `drawio-domain-sync`) have their own `scripts/` and `## Validate` blocks; in this pass I did not open them line-by-line, but the absence of a common helper means each skill would either re-implement the check or omit it. The session journal documents the silent-no-op failure mode (lines 135–139).

---

## Path: Domain Code Map Absence — Source notes

### Grep "domain-code-map|code map" c:\dev\abd-skills\practices\domain-driven-design — no matches

```
(no files)
```

Observation: the artifact `domain-code-map.md` and any skill that produces it do not exist in the DDD practice. The catalog (`common/skill-index.md`) does not list a code-map skill. The orchestrator's Specification stage (`abd-context-driven-delivery/SKILL.md` line 174) calls for `abd-domain-specification + abd-domain-walk` only.
