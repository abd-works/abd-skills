# Generate — abd-domain-model

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — domain model format: class blocks, constructor, properties, methods, collaborators, invariants, subtypes, and the consistent file shape.
- **`../../references/domain-model-json.md`** — `domain-model.json` schema, containment hierarchy, and upstream mapping from glossary terms and domain-language bullets.
- **`../supporting/domain-ops/SKILL.md`** — validate/read/write `domain-model.json` on disk (`domain_graph_cli.py`, `domain_map`).
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/domain-model-template.md` | Human-readable domain model with typed class blocks under each KA. |
| `../../references/domain-model-template.json` | Machine-readable graph (`abd-domain-model/v1`) — Module → KA → Class → Property/Operation. |
| `templates/domain.json` | Flat scanner vocabulary — class names, property names (camelCase), inheritance — derived from `domain-model.json`. |

**Canonical paths** (see `common/reference/folder-conventions.md`):

- `docs/domain/model/domain-model.md`
- `docs/domain/model/domain-model.json`
- `docs/domain/model/domain.json`

Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `modules/<module-name>-domain-model.md` (and matching `.json`).

The files are **not** an in-place enrichment of the domain-language file. They are fresh artifacts in the same flat heading shape every other DDD phase skill uses.

## After write — validate with domain-ops

```bash
export PYTHONPATH="practices/domain-driven-design/skills/supporting/domain-ops/scripts"
python3 practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py read --file docs/domain/model/domain-model.json
```

## Quality bar

Every behavior bullet from the Domain Language maps to at least one property or method. Properties are typed — never raw `String`; use domain types, constrained enums, or typed primitives. Methods use type-only params (no param names). Hidden collaborators (not in params or return) listed underneath methods, indented, before invariants. No `+` prefix. No stereotypes. No `List<T>` or `Dictionary<K,V>`. No `Interaction:` blocks. Subtype blocks carry only deltas. State marker set to `domain-model`.
