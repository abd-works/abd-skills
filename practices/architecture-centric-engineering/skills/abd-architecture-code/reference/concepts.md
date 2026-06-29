# Concepts — abd-architecture-code

## `<spec-root>`

The architecture spec **directory path resolved in step 0** (user path, story-map node, or project default). **Not hardcoded in this skill.** Every file name, folder, test tier, helper layout, and production layer placement is read from **`<spec-root>`** — `architecture-specification.md`, `rules/`, `templates/tests/`, and `example/tests/` when present.

## Orchestration

| Phase | Skill | Output |
| --- | --- | --- |
| Setup | **`track_task`** | **`progress/`** checklists — one row per spec testing tier and production layer |
| RED | **`abd-story-acceptance-test`** | Acceptance tests per **`<spec-root>`** Testing Architecture |
| GREEN | **`abd-clean-code`** | Production code per **`<spec-root>`** `template/` patterns |

**`<spec-root>` overrides** generic paths in downstream skills (e.g. when `abd-story-acceptance-test` says "follow host project conventions").

## Per-scenario increment

Work **one scenario at a time** within each layer: write test → run RED → write code → run GREEN → fix → next scenario. Do not batch all tests then all code.

**Layer order** — read from **`<spec-root>` Testing Architecture** first. When the spec is silent, default: domain → server → client → E2E (or spec-equivalent tier names).

Continue through deploy and verify until the story works end-to-end in a running solution — not when unit tests alone pass.

The companion **abd-architecture-specification** skill shows the *parameterized template shape*; this skill shows *filled-in output* — see **`reference/example.ts`** for a concrete Recipients module merged from `mern-domain-first-specification`.
