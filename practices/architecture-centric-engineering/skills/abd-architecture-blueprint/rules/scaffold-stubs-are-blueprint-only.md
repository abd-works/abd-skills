# Rule: Scaffold stubs carry blueprint-fidelity content only

When `abd-architecture-blueprint` runs in `mode: scaffold` and seeds a per-folder `architecture-context.md`, the stub **must** carry only blueprint-fidelity (and inherited outline-fidelity) content. Spec-fidelity slots — File Structure, Participants, Class Specification, Rules, Canonical Patterns, Across the Codebase, and the package-tier Public Surface — must be left empty with `<!-- spec to fill -->` markers for `abd-architecture-specification` to author later. The blueprint must not invent file structures, participant lists, code patterns, or enforceable rules at scaffold time, because the blueprint does not yet know them and inventing them creates content that `abd-architecture-specification` will silently override or that drifts out of sync with the eventual code. Passing means a fresh scaffold run produces stubs whose only filled sections are the blueprint-fidelity headers (Outline context, Blueprint context, owning module, mechanism code-shape, technology, ADR links, dependencies, test tier) and every spec-fidelity section is an empty marker. Failing means a stub ships with a fabricated file tree, a guessed Class Specification, or a rules list that has no source in the blueprint document.

## DO

- Fill blueprint-fidelity slots from the blueprint document verbatim.

  **Example (pass):** the blueprint's Modules section records `Orders` as a module with mechanisms `[common set] + Idempotency`, test tier `Domain`, and dependency `Customers`. The scaffolded `src/orders/architecture-context.md` carries:

  ```markdown
  **Owning module** -- `Orders`
  **Mechanisms used** -- common set + Idempotency
  **Test tier** -- Domain
  **Dependencies** -- Customers
  ```

  No invented surface, no invented participants — every spec-fidelity section is `<!-- spec to fill -->`.

- Fill outline-fidelity slots from the outline document verbatim.

  **Example (pass):** the outline's Architecture Mechanisms section records `Caching` with technology `Redis 7.x` and NFR justification `sub-10ms read latency for hot-path catalog queries`, linked to ADR-005. The scaffolded `src/cache/architecture-context.md` (mechanism-host folder) carries:

  ```markdown
  **Technology choice** -- Redis 7.x
  **NFR justification** -- sub-10ms read latency for hot-path catalog queries
  **ADR** -- [ADR-005](../../docs/architecture/decisions/ADR-005-caching.md)
  ```

- Mark every spec-fidelity section with `<!-- spec to fill -->` (or an equivalent comment marker) and keep the section heading. This lets `abd-architecture-specification` detect which sections it owns without having to parse prose.

  **Example (pass):**

  ```markdown
  ### Canonical Patterns

  <!-- spec to fill: ```code blocks showing the canonical shape per non-trivial file in the skeleton, using {placeholders}``` -->
  ```

## DO NOT

- Invent a File Structure tree at scaffold time.

  **Example (fail):** the blueprint says nothing about how `Caching` lays out files inside `src/cache/`. The scaffold step fabricates a tree (`src/cache/{key-builder.ts, redis-client.ts, invalidation.ts}`) because "it seemed plausible". `abd-architecture-specification` will later discover the real layout differs; the fabricated tree was misleading from the moment it was written.

- Invent Rules.

  **Example (fail):** the blueprint records the Caching mechanism's code shape as "every cache miss falls through to the source-of-truth repository". The scaffold step expands this into a Rules list with three additional bullets ("must use SHA-256 for key hashes", "must set TTL to 300s", "must wrap reads in a circuit breaker") that have no source in the blueprint or outline. These rules will conflict with whatever `abd-architecture-specification` actually discovers.

- Invent Class Specification or Canonical Patterns.

  **Example (fail):** the scaffold step writes a draft Class Specification for `CacheClient` with three methods (`get`, `set`, `invalidate`) and pseudo-code for each. None of this is grounded in code that exists. `abd-architecture-specification` will write the real spec from real code; the draft is noise that the spec author has to delete first.

- Overwrite existing content in a context file that was authored by `abd-architecture-specification`.

  **Example (fail):** re-running scaffold mode after the spec skill has filled `src/orders/architecture-context.md` truncates the file and reseeds it from the blueprint stub, wiping the spec-fidelity sections. Scaffold mode must be idempotent: skip existing files (except to append new blueprint-fidelity content under a dated "Blueprint updates" subsection, per [`generate.md` § Step 3c](../reference/generate.md#step-3c-stub-seeding)).

- Fill in placeholders the blueprint did not record.

  **Example (fail):** the blueprint records the Orders module's `Mechanisms used` as `common set`, with no module-specific mechanisms. The scaffold step infers `Idempotency` from "feels right for an orders module" and seeds it into the stub. `Idempotency` was never declared in the blueprint; this is a fabricated vocabulary violation that breaks the `vocabulary-matches-source-of-truth` rule downstream.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint, mode: scaffold). Scaffold mode is a handoff aid — it puts the right folders and the right blueprint-level metadata on disk so `abd-architecture-specification` can do its job — not a shortcut that lets the blueprint pre-empt the spec.
