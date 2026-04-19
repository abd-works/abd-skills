# Story Definition

## Purpose

Define each story completely through concrete specification-by-example scenarios — Given/When/Then with real domain values. This is where a story goes from "described" to "defined": the scenarios are the story's full behavioral specification, unambiguous enough to review with stakeholders and translate directly into executable tests.

Specification by example is a practice where the team creates specifications through concrete scenarios demonstrated through examples. These are not throwaway analysis artifacts — they become **executable requirements**, testable without translation, captured in **living documentation** that stays current as the system evolves.

## Why this stage matters

- **Concreteness removes ambiguity:** AC say "the payment is validated"; a scenario says "Given **Account** *Acme Operating* with **Transactional Limit** *$500,000.00 USD*, When the **User** *Jane Doe* enters a **Payment Amount** of *$10,000.00 USD*, Then the **Wire Payment** is marked as *successful*." There is no room for misinterpretation.
- **Multiple perspectives, not solo work:** Specifications written from a single viewpoint produce gaps that surface late. Good scenarios require business logic, technical constraints, and testing concerns to converge.
- **Direct input to tests:** The scenarios written here are the direct input to acceptance tests in the next stage. If a scenario is unclear, the test will be unclear; if the scenario is concrete, the test writes itself.
- **Living documentation:** Unlike traditional specs that rot, scenarios tied to automated tests stay current — when behavior changes, the scenario changes, and the test enforces it.

## Team role

**Analyst**

## Practice skill

`abd-specification-by-example` — Concrete Given/When/Then steps with real domain values, bold concept names, italic values. Plain scenarios (inline values) and outline (multiple data rows).

## Entry conditions

- Exploration exit gate passed.
- `story-graph.json` contains stories with AC in WHEN/THEN format.
- Target stories for scenario writing are identified (typically those explored in the previous stage).

## Expected outputs

- Scenario files in the workspace (per the practice skill's template format).
- Updated `story-graph.json` with scenario references on stories where applicable.

## Key questions (is this stage done?)

1. Does every explored story have at least one scenario with **real domain values** — not abstract placeholders like "customer A" or "order 123"?
2. Are Given steps describing **state** (preconditions) and When steps describing **actions** — or are actions hiding in Given?
3. Is there at least one happy path, one failure/rejection, and edge cases where the story implies them?
4. Where the same steps apply across multiple data rows (calculations, boundaries), are Scenario Outlines used instead of duplicated plain scenarios?
5. Do scenarios trace back to AC — can a reviewer see which AC each scenario exercises?
6. Are domain terms consistent with earlier stages, using the same vocabulary established in discovery and exploration?
7. Has Background been used only where three or more scenarios share identical starting state?

## Conditions of success

- Scenarios use **real or realistic domain data** — not invented placeholders that hide inconsistencies real data would expose.
- **Given** describes state, **When** describes actions, **Then** asserts outcomes — no mixing.
- The main-flow AC from exploration serves as the scenario spine; remaining AC become additional scenarios for failures, edges, and alternate flows.
- **Key examples over exhaustive enumeration:** a few well-chosen examples that illustrate the rule beat thirty rows that restate it.
- Scenarios are persisted in `story-graph.json` (the canonical source), not in competing standalone markdown files.
- Domain language matches the model — entities, value objects, and collaborations read naturally in the steps.

## Exit gate

1. `story-graph.json` passes structural validation.
2. Practice skill scanners pass (if `abd-specification-by-example` ships scanners): `run_scanners.py --skill-root <abd-specification-by-example> --workspace <workspace>`.
3. Every explored story has at least one scenario with concrete values (not abstract placeholders).
4. Scenarios use Given/When/Then structure with real domain data.
5. Scenarios trace back to AC — every scenario exercises at least one AC.
6. Domain terms and actor names are consistent with upstream stages.
7. The user has confirmed the scenarios at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Scenario files and their paths.
- Updated `story-graph.json`.
- Mapping of scenarios to stories and AC for test traceability.
- Any ambiguities discovered during scenario writing that may need upstream revision.
