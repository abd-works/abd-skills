# Rule: Ubiquitous Language bullets become card rows; italicized terms become collaborators

**Scanner:** Manual review

When the source is a Ubiquitous Language file (`*-ubiquitous-language.md` with `state: ubiquitous-language` in the front matter), the renderer produces a class diagram with the same shape it produces for a CRC source — cards with rows and collaborators — but reads its structure from the ULL's prose form rather than from CRC tables.

Mapping:

| ULL element | Diagram element |
|---|---|
| `## KAName` | One page named exactly `KAName` |
| `### concept_name` (KA's own first) | One class card on the KA's page |
| Each verb-led behavior bullet on a concept | One row on that card, formatted `<bullet text> : <Collaborator>, <Collaborator>` |
| `*italicized*` terms inside a bullet | The collaborator list on that row, comma-separated |
| `**Invariant:** …` bullet | One row in the invariant compartment |
| `### Subtype *is a type of* Base` | Inheritance edge child → parent |
| `### stub` whose first bullet says `is a property of *parent*` | Property row on the parent's card, OR a lightweight stub card with a `«property of: Parent»` stereotype (agent's call based on how many stubs the parent has) |
| `### boundary_term *(boundary)*` under a KA | Imported card on that KA's page with a `«boundary: OwningModule»` stereotype, dashed border (same visual treatment as `«from: KA Name»`) |
| Parenthetical primitive description (e.g. `(integer)`, `(0–40)`) | Inline value description on the row, no separate card |

A passing diagram contains one card per `### concept`, one row per bullet, one association edge per unique cross-concept italicized reference (folded — multiple bullets pointing at the same target produce one edge, not many), one inheritance edge per `*is a type of*` heading, and no dropped bullets, terms, or invariants.

A failing diagram drops bullets, drops italicized terms, invents type annotations the source does not contain, or draws one edge per bullet-reference instead of folding duplicates.

## DO

- Emit one row per behavior bullet, label = the bullet's text with italic markers stripped, collaborator column = the bullet's italicized terms.

  **Example (pass):**

  ULL:
  ```
  ### check
  - is made *using* the *trait* of a *character*
  - is resolved by *rolling* a *d20*, comparing the *roll total* to the *difficulty class*, producing a *check result*
  - **Invariant:** shape is always *roll total* versus *difficulty class*
  ```

  Renders to card `check` with rows:
  ```
  is made using the trait of a character          : Trait, Character
  is resolved by rolling a d20, comparing the roll total to the difficulty class, producing a check result : D20, Roll Total, Difficulty Class, Check Result
  ─────────────────────────────────────────────────
  Invariant: shape is always roll total versus difficulty class
  ```

  …and association edges `check → Trait`, `check → Character`, `check → D20`, `check → Roll Total`, `check → Difficulty Class`, `check → Check Result`.

- Fold duplicate cross-concept references into a single edge.

  **Example (pass):** Three different bullets on `check` mention `*trait*`. The diagram has exactly **one** `check → Trait` association edge, not three.

- Draw inheritance from `### Subtype *is a type of* Base` headings, not from association edges.

  **Example (pass):** `### opposed check *is a type of* check` produces a hollow-triangle inheritance edge `opposed check → check`. The italicized `*check*` references inside the bullets of `opposed check` do **not** also produce an association edge — inheritance subsumes them.

- Render `### term *(boundary)*` stubs as imported cards with `«boundary: OwningModule»` stereotype and a dashed border.

  **Example (pass):** `### power effect *(boundary)*` under the Check KA renders as a dashed-border card titled `power effect` with stereotype `«boundary: Power»` above the name. The owning module name comes from the `# Boundary Domain` canonical entry's `Owned by: …` line.

- Render property/instance stubs as either a property row on the parent or a lightweight stub card with a `«property of: Parent»` stereotype.

  **Example (pass):** `### roll total` with first bullet `is a property of *check* — the d20 face value plus all modifiers` becomes either a row on the `check` card (`roll total : (integer)`) when `check` has few properties, or a small stub card titled `roll total` with stereotype `«property of: check»` when the parent already has many properties.

## DO NOT

- Drop bullets, italicized terms, or invariants during rendering.

  **Example (fail):** ULL bullet `- supplies its *rank* as the primary *modifier* for any *check*` rendered as a row with only `Check` in the collaborator column, dropping `Rank` and `Modifier`. The reader cannot see which collaborators the row depends on.

- Invent type annotations the source does not contain.

  **Example (fail):** Adding `+ name: String` or `+ rank: Integer` to a card whose ULL source uses no types. Object-model fidelity is only appropriate when the source is an object model.

- Emit one edge per bullet reference instead of folding duplicates.

  **Example (fail):** `check` mentions `*trait*` in three bullets; diagram has three parallel `check → Trait` edges, all stacked on the same anchor. Should be one folded edge.

- Treat italicized terms inside `**Invariant:**` lines as new association edges.

  **Example (fail):** `**Invariant:** *ranks* must never be added directly` renders an association edge `rank → rank` because the renderer scanned the invariant text for italicized terms. Invariants do not produce edges; only behavior bullets do. (The italicized terms inside invariants still must resolve per `italic-terms-resolve-to-named-concepts.md` in the upstream skill.)

- Draw association edges from a subtype to its base for behaviors that are already inherited.

  **Example (fail):** `### opposed check *is a type of* check` plus an association edge `opposed check → check` because a bullet says `is made against another *check's* result`. The inheritance edge already carries that relationship.

## Notes

- This rule depends on the upstream rule `italic-terms-resolve-to-named-concepts.md` in `abd-ubiquitous-language`. If italicized terms in the source do not resolve, this renderer cannot draw their edges without inventing cards — fix the ULL first.
- For first-time full renders of large ULLs, persist a `build_<name>_ull_diagram.py` in the destination repo per the existing build-script convention.
- ULL `sync-to-model` (diagram → source) is one-way for new/deleted concepts only. Bullet text rewrites do not round-trip back to the file — the ULL prose is the authoritative form, and bullet edits should be made in the markdown, not in Draw.io.
