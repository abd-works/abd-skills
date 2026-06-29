# Engineering

**Prior:** [specification.md](specification.md) · **Index:** [README.md](README.md)

Bootcamp stage **5 — Engineering**. **Multiple roles** across four skills in fixed order. Plans may use one slot for the whole stage or **one slot per skill** — keep this order either way.

Role × skill index: [team-roles.md](../roles/team-roles.md)

## Purpose

Deliver working software for the slice: runnable UI from `abd-interface-design`, domain types in code, failing then passing tests, and clean production implementation — honoring specification artifacts (scenarios, interface spec, domain model, architecture reference).

## Team role

Assign **`team-role` per skill**, not one role for the whole stage:

| Step | Executor | Review at checkpoint |
| --- | --- | --- |
| 1 — `abd-interface-design` (implementation pass) | **UX Designer** | Reviewer |
| 2 — `abd-domain-code` | **Engineer** | **Business Expert** + Reviewer |
| 3 — `abd-acceptance-test-driven-development` | **Engineer** | Reviewer |
| 4 — `abd-clean-code` (+ stack/arch skill) | **Engineer** | Reviewer |

## Practice skills (required order)

Run skills **top to bottom**. Skip only when the engagement plan explicitly waives a step.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **User experience design** | `abd-interface-design` | UX Designer | **Implementation pass** — runnable UI from `interface-design.md` (spec pass ran in [Specification](specification.md)) |
| 2 | **Domain-driven design** | `abd-domain-code` | Engineer | Typed domain surface aligned with domain model / domain language; Business Expert validates at checkpoint |
| 3 | **Story-driven delivery** | `abd-acceptance-test-driven-development` | Engineer | Acceptance tests from scenarios; example data from domain specification; test layout per architecture reference |
| 4 | **Architecture-centric engineering** | `abd-clean-code` **+** stack / arch skill **if provided** (e.g. `mern-technical-architecture`, `hero-vtt-technical-architecture`) | Engineer | Production code to pass tests; implementation patterns from architecture reference |

**Architecture reference** (`abd-architecture-reference`) is produced in [Specification](specification.md). In this stage, **use** it — do not re-run the reference skill unless specification was incomplete. Step 3: testing patterns and folder layout. Step 4: implementation patterns.

## Entry conditions

- [Specification](specification.md) exit gate passed — including `interface-design.md` from `abd-interface-design` **spec pass** when UI is in scope.
- Scenarios, interface spec, domain model, and architecture reference (when in scope) available.

## Expected outputs

1. Runnable UI from `abd-interface-design` implementation pass (UX Designer, when assigned).
2. Domain modules / types from domain specification (Engineer).
3. Failing acceptance test suite (Engineer); passing after clean-code implementation.
4. Production code passing all tests (Engineer).

## Exit gate

1. Scanners green for **each assigned skill** in order (`run_scanners.py` for `abd-interface-design`, `abd-domain-code`, `abd-acceptance-test-driven-development`, `abd-clean-code` as applicable).
2. Step 3: acceptance tests exist and **fail** before step 4 implementation (when ATDD ran).
3. Domain code matches domain model / domain language when step 2 ran; Business Expert signed off at checkpoint.
4. Tests trace to scenarios; example data matches domain specification; test structure matches architecture reference when stack skill ran.
5. Implementation honors architecture reference and interface spec when stack skill was assigned.
6. **Ripple check** per [README.md](README.md).
7. User confirmed at checkpoint.

## Handoff

Final stage for the increment. Pass to kanban lead:

- Stories delivered, tests green, deploy status.
- Technical debt and ripple items for next increment or [discovery.md](discovery.md) refresh.
