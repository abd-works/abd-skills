# Exploration

## Purpose

Deepen each story's definition by writing behavioral acceptance criteria — concrete WHEN/THEN statements that describe how the system responds to user actions. Bridge the gap between story-level intent and testable expectations.

Acceptance criteria are story-level behavioral statements that answer four questions: **When** does the behavior apply? **Then** what is observable? **And** what else happens in sequence? **But** what must not happen? They sit above BDD scenarios (which come in the next stage) and below the story-map level of intent.

A good AC set can be read by a product owner, a tester, and a developer — all at once — and describes observable outcomes, not implementation details.

## Why this stage matters

- **Shared understanding:** AC force the team to articulate what "done" looks like for each story before a line of code is written or a test designed.
- **Behavioral language:** By stating outcomes in user/system interaction terms (not database columns or API endpoints), AC stay useful across roles and survive design changes.
- **Gap detection:** Writing AC exposes missing business rules, unclear edge cases, and assumptions that would otherwise surface late. Unknowns surfaced early are more valuable than plausible-sounding requirements that turn out to be wrong.
- **Downstream traceability:** Every scenario, test, and line of production code traces back to an AC. If it is not in the AC, it should not be in the test; if it is not in the test, it should not be in the code.

## Team role

**Analyst**

## Practice skill

`abd-acceptance-criteria` — Exploration-phase AC: WHEN/THEN/AND/BUT, behavioral language, per-story domain terms, atomic AC, actor alternation, channel-specific detail.

## Entry conditions

- Prioritization exit gate passed.
- `story-graph.json` contains stories with slice assignments.
- A target slice or set of stories is identified for exploration (typically the first/spine slice from prioritization).

## Expected outputs

- Updated `story-graph.json` with AC arrays on explored stories.
- Rendered acceptance-criteria artifacts per the practice skill templates (`acceptance-criteria.md` and `acceptance-criteria.txt`).

## Key questions (is this stage done?)

1. Does every explored story have at least one WHEN/THEN AC that a product owner can read and confirm?
2. Do the AC cover the happy path, error paths, and boundary conditions — or only the sunny day?
3. Is the language behavioral (observable triggers and outcomes) rather than technical (class names, table schemas)?
4. Are domain terms used consistently across AC and aligned with the vocabulary established during discovery?
5. Does each AC describe a delta from the general case, or are there repeated blocks of near-identical text?
6. Are there flagged unknowns — business rules, system behaviors, or edge cases where context was missing — rather than invented AC filling the gap?
7. Do AC alternate between user-visible and system-visible emphasis, avoiding long runs of the same actor?

## Conditions of success

- AC are **atomic**: the general case is stated once, and follow-on AC describe only what differs (error paths, edge cases).
- AC use **WHEN/THEN/AND/BUT** structure — no Given (that is reserved for scenarios in the next stage).
- **Domain terms** are explicit per story: things, state, actions, and rules are named and consistent with the story map.
- AC cover **all important permutations**: validation paths, calculation branches, happy path, errors, boundaries.
- Where the product has distinct surfaces (CLI, UI, API), AC include **channel-specific detail** so testers know where to look.
- **No fabrication**: where context is incomplete, unknowns are captured explicitly rather than papered over with plausible-sounding AC.

## Exit gate

1. `story-graph.json` passes structural validation.
2. Practice skill scanners pass: `run_scanners.py --skill-root <abd-acceptance-criteria> --workspace <workspace>` exits 0.
3. Every explored story has at least one AC in WHEN/THEN format.
4. AC use behavioral language — describe system response to user action, not implementation.
5. AC reference only stories that exist in the graph (traceability).
6. Domain vocabulary is consistent with discovery-stage naming.
7. The user has confirmed the AC at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Updated `story-graph.json` with AC.
- Which stories/slices have been explored (scope for scenarios stage).
- Any open questions, edge cases flagged but not yet resolved, and gaps in business logic.
