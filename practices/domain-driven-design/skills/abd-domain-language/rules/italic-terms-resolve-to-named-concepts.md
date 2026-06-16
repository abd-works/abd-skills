# Rule: Every italicized term resolves to a named concept, stub, or primitive

**Scanner:** Manual review (optional companion scanner — see `scanners/italic-terms-resolve-scanner.py` when present)

Every `*italicized*` term that appears in a behavior bullet, invariant, KA intro paragraph, or boundary stub must resolve to one of:

1. a `### concept_name` heading in this file (under any KA, including the KA's own concept),
2. a `### Subtype *is a type of* Base` subtype heading,
3. a property / instance / type-property stub heading (e.g. `### rank` with a first bullet `is a property of *trait*`),
4. a `### boundary_term *(boundary)*` scoped stub under the KA, OR
5. a primitive description in **parentheses** when no concept fits (e.g. *(integer)*, *(true or false)*, *(0–40)*) — in that case the parenthetical itself is **not** italicized, only the surrounding domain term.

This makes the file deterministically diagram-parseable: every italicized term in a bullet is a connector to another card. Failing means an italicized term has no matching heading and no primitive form — so a downstream diagram render cannot draw an edge for it without inventing a target.

This rule complements `domain-terms-italicized-in-prose-and-bullets.md` (which enforces *that* terms are italicized) by enforcing *that* italicized terms refer to something the file actually defines.

## DO

- Italicize a term only when a matching `### term` block, subtype heading, stub heading, or `*(boundary)*` stub exists in this file.

  **Example (pass):**
  ```
  ### check
  - is made *using* the *trait* of a *character*
  ```
  …and the same file has `### trait` under `## Trait`, and `### character *(boundary)*` (or a `### character` block) under this KA or the file's Boundary Domain.

- Promote an inline italicized noun to its own stub when it has no matching heading yet but the source treats it as a named domain idea.

  **Example (pass):** Behavior bullet on `check` mentions *roll total*; add `### roll total` with one bullet `is a property of *check* — the d20 face value plus all modifiers`.

- Use parenthetical primitive descriptions when no concept is appropriate.

  **Example (pass):**
  ```
  - has exactly one *rank* — a single numeric value (*integer 0 and up*)
  ```
  Here `*rank*` resolves to `### rank`; the value range is a primitive description, not a separate concept.

- Bring a boundary term in as a scoped stub when bullets on a KA's concepts reference it.

  **Example (pass):** Behavior bullets on the Check KA mention *power effect*. Add `### power effect *(boundary)*` under `## Check` with the one scoped bullet that explains what this KA depends on (`sets the *DC* for *resistance checks*`). The canonical `## Effect / power effect` entry remains under `# Boundary Domain`.

## DO NOT

- Leave an italicized term with no matching heading anywhere in the file.

  **Example (fail):** `### condition` has bullet `- is imposed by a *condition source*`, but no `### condition source` block, no subtype heading, no stub, and no boundary entry resolves *condition source*. A diagram renderer cannot draw an edge from `condition` to *condition source*.

- Italicize a primitive value description that should be parenthetical instead.

  **Example (fail):** `- has a *circumstance modifier* of *between -5 and +5*` — the range is not a concept; write `(between -5 and +5)` plainly.

- Italicize prose-only words that have no domain status.

  **Example (fail):** `- *resolves* the *check* *immediately*` — `immediately` is not a domain term; only `*check*` should stay italicized (and `*resolves*` should be plain verb).

## Why this matters

This is the rule that makes a Domain Language a **second-pass input to drawio-domain-sync** — analogous to how domain model's collaborator column makes domain model a diagram-ready source. When every italicized term resolves to a card on the page, the renderer can draw one association edge per unique cross-concept reference without guessing.

**Source:** Engagement convention — added so the Domain Language can be rendered as a class diagram with concepts as cards, behavior bullets as rows, and italicized terms as collaborators (mirroring the domain model pass).
