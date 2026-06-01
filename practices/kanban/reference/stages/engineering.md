# Engineering

**Pull:** When a ticket is `stage: engineering` and active, agents pull skills from `kanban.json` for this stage — same [pull-model](../../agents/reference/pull-model.md) as all stages.
**Prior:** [specification.md](specification.md) · **Index:** [README.md](README.md)

Bootcamp stage **5 — Engineering**. **Multiple roles** across four skills in fixed order. Plans may use one slot for the whole stage or **one slot per skill** — keep this order either way.

Role × skill index: [team-roles.md](../roles/team-roles.md)

## Purpose

Deliver working software for the slice: runnable UI from `abd-interface-design`, domain types in code, failing then passing tests, and clean production implementation — honoring specification artifacts (scenarios, interface spec, CRC, architecture reference).

## Team role

Assign **`team-role` per skill**, not one role for the whole stage:

| Step | Executor | Review at checkpoint |
| --- | --- | --- |
| 1 — `abd-interface-design` (implementation pass) | **UX Designer** | Reviewer |
| 2 — `abd-object-model` | **Business Expert** | Reviewer |
| 3 — `abd-acceptance-test-driven-development` | **Product Owner** | Reviewer |
| 4 — `abd-clean-code` (+ stack/arch skill) | **Engineer** | Reviewer |

## Practice skills (required order)

Run skills **top to bottom**. Skip only when the engagement plan explicitly waives a step.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **User experience design** | `abd-interface-design` | UX Designer | **Implementation pass** — runnable UI from `interface-design.md` (spec pass ran in [Specification](specification.md)) |
| 2 | **Domain-driven design** | `abd-object-model` | Business Expert | Typed domain surface aligned with CRC / UL |
| 2b | **Domain-driven design** | `drawio-domain-sync` | Business Expert | **Background** after object-model — `object-model-class-diagram.drawio` |
| 3 | **Story-driven delivery** | `abd-acceptance-test-driven-development` | Product Owner | Acceptance tests from scenarios; example data from object model; test layout per architecture reference |
| 4 | **Architecture-centric engineering** | `abd-clean-code` **+** stack / arch skill **if provided** (e.g. `mern-technical-architecture`, `hero-vtt-technical-architecture`) | Engineer | Production code to pass tests; implementation patterns from architecture reference |

**Architecture reference** (`abd-architecture-reference`) is produced in [Specification](specification.md). In this stage, **use** it — do not re-run the reference skill unless specification was incomplete. Step 3: testing patterns and folder layout. Step 4: implementation patterns.

## Entry conditions

- [Specification](specification.md) exit gate passed — including `interface-design.md` from `abd-interface-design` **spec pass** when UI is in scope.
- Scenarios, interface spec, CRC, and architecture reference (when in scope) available.

## Expected outputs

Docs under **`docs/increments/<n>-<slug>/engineering/`**; code in **`src/`**. See [artifact-layout.md](../artifact-layout.md).

1. Runnable UI in `src/`; spec in `increments/<n>-<slug>/specification/interface-design.md`.
2. `increments/<n>-<slug>/engineering/object-model.md` + domain code (Business Expert).
3. Acceptance tests then production code (Product Owner writes tests; Engineer implements).

**When increment fully archived** → kanban lead merges `increments/<n>-<slug>/engineering/` into `docs/end-to-end/engineering/`.

## Exit gate

1. Scanners green for **each assigned skill** in order (`run_scanners.py` for `abd-interface-design`, `abd-object-model`, `abd-acceptance-test-driven-development`, `abd-clean-code` as applicable).
2. Step 3: acceptance tests exist and **fail** before step 4 implementation (when ATDD ran).
3. Object model in code matches CRC / UL when step 2 ran.
4. Tests trace to scenarios; example data matches object model; test structure matches architecture reference when stack skill ran.
5. Implementation honors architecture reference and interface spec when stack skill was assigned.
6. **Ripple check** per [README.md](README.md).
7. User confirmed at checkpoint.

## Handoff

Final stage for the increment. Pass to kanban lead:

- Stories delivered, tests green, deploy status.
- Technical debt and ripple items for next increment or [discovery.md](discovery.md) refresh.
