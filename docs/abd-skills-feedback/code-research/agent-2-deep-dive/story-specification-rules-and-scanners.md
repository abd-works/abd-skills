# Deep Dive: Story Specification — Rules & Scanners

## Principles & Patterns

- **Rule-text-and-scanner pairing**: each rule under `abd-story-specification/rules/` has a markdown body that defines the rule and (often) a Python scanner under `scanners/` that enforces it mechanically. The pattern is sound but the scanners check only a subset of what the rules declare.
- **Domain grounding via `domain.json`**: the scanners walk a schema file produced as a side-effect of the domain skills. The schema names concepts and their attributes; the scanners validate **columns** against it.
- **Step-text-as-truth assumption**: the `then-asserts-concrete-output-scanner.py` treats `scenario.steps` as the sole source of assertable values. Example-table cell contents are not inspected.
- **Single-WHEN stub pattern**: `stub-service-interaction-structure.md` defines a single `When` block with `And` continuations for system-forwards / service-returns. This is **not** the two-phase **When → Then → When → Then** pattern that midtier proxies require.

## File Structure

```
practices/story-driven-delivery/skills/abd-story-specification/
├── SKILL.md
├── reference/                                          ← worked examples and concepts
├── rules/
│   ├── background-vs-scenario-setup.md
│   ├── emphasize-domain-significant-terms-scenarios.md
│   ├── example-tables-use-domain-language.md          ← rule text says BOTH table+columns
│   ├── given-describes-state-not-actions.md
│   ├── ground-scenarios-in-ddd-outputs.md
│   ├── keep-scenarios-consistent-across-connected-domains.md
│   ├── map-table-columns-to-scenario-parameters.md
│   ├── mention-domain-concept-beside-placeholder.md
│   ├── prefer-key-examples-over-exhaustive-enumeration.md
│   ├── scenario-language-matches-domain.md
│   ├── scenarios-cover-all-cases.md
│   ├── scenarios-on-story-graph.md
│   ├── stub-service-interaction-structure.md          ← single-WHEN partition
│   ├── then-asserts-concrete-output.md
│   ├── trailing-spaces-for-line-breaks.md
│   ├── use-real-data-over-invented-examples.md
│   ├── use-scenario-outline-when-needed.md
│   ├── validate-scenario-values-against-schema.md
│   └── write-concrete-scenarios.md
├── scanners/
│   ├── emphasize-domain-terms-scenario-scanner.py
│   ├── example-tables-domain-scanner.py               ← columns only
│   ├── then-asserts-concrete-output-scanner.py        ← step text only
│   └── __init__.py
└── templates/specification-by-example.md
```

## Participants

| Rule | Body says | Scanner enforces |
|---|---|---|
| `example-tables-use-domain-language.md` | Table names AND columns match `domain.json` | Columns only (and a denormalization heuristic) |
| `then-asserts-concrete-output.md` | Then steps contain at least one assertable value | Step text only; cell contents ignored |
| `stub-service-interaction-structure.md` | Single `When` with `system-forwards` / `service-returns` as `And` continuations; outcome in `Then` | (no scanner found) |
| `given-describes-state-not-actions.md` | Given is state, not actions | (no scanner found) |
| *missing — boundary-step-system-and-operation* | n/a (rule does not exist) | n/a |
| *missing — example-cells-are-atomic-data* | n/a (rule does not exist) | n/a |
| *missing — table-name-matches-concept* | rule text covers it; scanner doesn't | n/a |

## Flow

1. Author writes a `specification-by-example.md` file using Scenario Outline.
2. Author runs the skill's `## Validate` step — scanners walk the file.
3. Scanners emit `Violation` objects against rules.
4. Author iterates until scanners are clean.
5. **Gap:** an author who clears scanners assumes the spec passes all rules — but several rules (table-name match, cell content, boundary system/op, two-phase proxy) are not actually checked.

## Walkthrough Example — pml-midtier session

The midtier spec author produced a Scenario Outline with this Examples table:

```
| scenario   | bundle_stub_id    | mavenir_stub_behavior                                                    |
| Scenario 1 | bundle_stub_001   | respond HTTP 201 with **MavenirCart** { id: cart_stub_001 }              |
```

- The **column** `bundle_stub_id` is not in `domain.json` → `example-tables-domain-scanner.py` would flag it.
- The **column** `mavenir_stub_behavior` is not in `domain.json` → also flagged.
- The **table name** (`CartCreationSetup`) does not match any concept → **scanner does not check this**; it passes silently.
- The **cell** `respond HTTP 201 with **MavenirCart** { id: cart_stub_001 }` is a sentence → **scanner does not check cell content**; it passes silently.
- The corrected version uses table name `CartItemPayload` (a `domain.json` concept), columns `http_status`, `cartId`, and atomic cell values `201`, `cart_stub_001`. Every value in the corrected version is an atom; every name is a concept.

The session also produced ACs/specs with steps like:

```
Then the midtier fetches **MavenirCustomer** and detects **MavenirCharacteristic** { name: done } is set
```

- The verb `fetches` is vague; no target system is named; no operation is named.
- The corrected version:
  `Then the midtier sends GET customer(cus_stub_001) to **Mavenir** and detects **MavenirCharacteristic** { name: done } is set`
- No existing rule or scanner catches the original; the fix relies entirely on AI re-reading the journal correction.
