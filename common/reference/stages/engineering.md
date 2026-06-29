# Engineering

**Pull:** When a ticket is `stage: engineering` and active, agents pull skills from `kanban.json` for this stage.
**Prior:** [specification.md](specification.md)

Bootcamp stage **5 · Engineering**. **Multiple roles** across four skills in fixed order. Plans may use one slot for the whole stage or **one slot per skill** — keep this order either way.

Role ↔ skill index: [team-roles.md](../roles/team-roles.md)

## Purpose

Deliver working software for the slice: typed domain code, failing then passing acceptance tests, and clean production implementation (including production UI when in scope) — honoring specification artifacts (scenarios, clickable UX prototype, domain specification, architecture reference).

## Outcomes

- system code
- business code
- interface code
- architecture code

## Team role

Assign **`team-role` per skill**, not one role for the whole stage:

| Step | Executor | Review at checkpoint |
| --- | --- | --- |
| 1 · `abd-domain-code` | **Business Expert** | Reviewer |
| 2 · `abd-story-acceptance-test` | **Product Owner** | Reviewer |
| 3 · `abd-architecture-code` | **Engineer** | Reviewer |

`abd-clean-code` and `abd-secure-code` live under **`stages/engineering/`** — shown in the stage supplemental strip on the board, not in a practice column.

## Practice skills (required order)

Run skills **top to bottom**. Skip only when the engagement plan explicitly waives a step.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-code` | Business Expert | Domain tests + production code TDD from domain specification |
| 1b | **Domain-driven design** | `drawio-domain-sync` | Business Expert | **Background** after domain code — `domain-specification.drawio` |
| 2 | **Story-driven delivery** | `abd-story-acceptance-test` | Product Owner | Acceptance tests from scenarios; example data from domain code; test layout per architecture reference |
| 3 | **Architecture-centric engineering** | `abd-architecture-code` | Engineer | Production code from named architecture spec — templates, file layout, and rules for the story; **production UI** honours the clickable prototype and `ux-specification.md` from [Specification](specification.md) |

**Architecture spec** (`abd-architecture-specification`) is produced in [Exploration](exploration.md) (document) and [Specification](specification.md) (template). In Engineering, use `abd-architecture-code` to generate from it — do not re-run `abd-architecture-specification` unless the spec itself is incomplete.

**UX prototype** (`abd-ux-specification`) runs only in [Specification](specification.md). Engineering implements production behaviour; it does not re-run the prototype skill.

## Entry conditions

- [Specification](specification.md) exit gate passed — including clickable prototype + `ux-specification.md` when UX skill was assigned, domain specification from `abd-domain-specification`, and architecture reference when in scope.
- Scenarios, prototype spec, domain specification, and architecture reference (when in scope) available.

## Expected outputs

Docs under **`docs/increments/<n>-<slug>/engineering/`**; code in **`src/`**. See [artifact-layout.md](../artifact-layout.md).

1. Production code and tests in `src/` (domain, acceptance, app/UI per architecture reference).
2. Typed domain code + tests (Business Expert).
3. Acceptance tests then production implementation (Product Owner writes tests; Engineer implements).

**When increment fully archived** — kanban lead merges `increments/<n>-<slug>/engineering/` into `docs/end-to-end/engineering/`.

## Exit gate

1. Scanners green for **each assigned skill** in order (`run_scanners.py` for `abd-domain-code`, `abd-story-acceptance-test`, `abd-clean-code`, `abd-architecture-code` as applicable).
2. Domain code aligns with domain specification when `abd-domain-code` ran.
3. Step 2: acceptance tests exist and **fail** before step 3 implementation (when ATDD ran).
4. Tests trace to scenarios; example data matches domain code; test structure matches architecture reference when `abd-architecture-code` ran.
5. Production UI and behaviour honour the clickable prototype and `ux-specification.md` when `abd-architecture-code` was assigned.
6. **Ripple check**.
7. User confirmed at checkpoint.

## Handoff

Final stage for the increment. Pass to kanban lead:

- Stories delivered, tests green, deploy status.
- Technical debt and ripple items for next increment or [discovery.md](discovery.md) refresh.
