# Deep Dive: Domain Code Map Absence

## Principles & Patterns

- **Domain artifacts assume a greenfield context**: `abd-domain-language`, `abd-domain-glossary`, and `abd-domain-model` produce concepts, terms, and ownership tables — none of which point to existing source files.
- **No standard "concept → file path" artifact**: there is no `domain-code-map.md` template or skill that ties each domain Key Abstraction or operation to the file/function in the codebase that implements it.
- **Story specifications use domain language abstractly**: `abd-story-specification` requires example tables to use domain concepts as column names, but never requires that those concepts be linked to specific service modules or files.
- **In a brownfield/reverse-engineering context this gap is acute**: when the goal is "reverse-engineer from existing code to story specs," the missing link from domain concept → existing service module → existing route is exactly what the session needed and didn't have.

## File Structure

```
practices/domain-driven-design/skills/
├── abd-domain-language/         ← produces terms, KAs, concept sketches
├── abd-domain-glossary/         ← produces grouped glossary
├── abd-domain-model/            ← produces ownership table per concept
├── abd-domain-specification/    ← produces typed surface (types, invariants)
├── abd-domain-walk/             ← validates model with scenarios
└── supporting/
    └── drawio-domain-sync/      ← renders domain model to draw.io

(missing) abd-domain-code-map/   ← no such skill exists
```

## Participants

| Existing artifact | What it produces | Does it map to code? |
|---|---|---|
| `domain.json` / `domain-model.md` | Key Abstractions, operations, invariants | No file paths |
| Glossary | Term → definition | No file paths |
| Ownership table | Who creates/mutates/guards each concept | Conceptual ownership only, not file ownership |
| `abd-domain-specification` typed surface | TypeScript types, validators | No anchor to existing implementation |

| Missing artifact | What it would produce |
|---|---|
| `domain-code-map.md` | Per Key Abstraction or operation: `file path` + `function/class name` + `line range` |
| `abd-domain-code-map` skill | Read existing codebase, walk domain model, produce the map |
| Scanner: `domain-code-map-completeness` | Assert every operation in `domain.json` has an entry in the code map |

## Flow

**Greenfield flow (currently supported):**
1. Domain Language → Domain Glossary → Domain Model → Domain Specification.
2. Story Specification consumes Domain Model abstractly.
3. Implementation comes later; correspondence to domain is enforced by `abd-clean-code` review.

**Brownfield flow (missing — required by this session):**
1. Code Research (Explorer + Deep Dive) → file evidence per concern.
2. Domain Language → Domain Glossary → Domain Model.
3. **Domain Code Map**: for each concept and operation, name the file path + function that implements it today.
4. Story Specification consumes Domain Model + Domain Code Map — so example tables can reference specific service modules without guessing.
5. Acceptance tests can call the specific functions named in the code map.

## Walkthrough Example — pml-midtier session

The midtier exposes proxy routes under `/mv/customer/cart` (and similar). The session needed to:
- Reverse-engineer routes from the existing controllers.
- Identify which "cart operations" the routes implement.
- Produce a story map and specifications that reference both abstract operations (e.g. *add item to cart*) and concrete routes (e.g. `POST /mv/customer/cart`).

There was no skill that said: "Walk `src/cart/cart.controller.ts`, list each route, attach each route to a domain operation in `domain.json`, write `domain-code-map.md`." The agent had to invent this step. The journal documents the failure mode:

> Spec example tables referenced cart "items" abstractly without naming the specific midtier route or downstream service that the test would exercise, leaving the test scaffold ambiguous about what to invoke.

A `domain-code-map.md` artifact, generated from code research and tied back to the domain model, would have closed this loop. The shape would be:

```markdown
## Concept: Cart

| Operation        | Domain method  | File                          | Function           | Route                |
|---|---|---|---|---|
| Add item         | Cart.addItem   | src/cart/cart.controller.ts   | addItem            | POST /mv/customer/cart |
| Remove item      | Cart.removeItem| src/cart/cart.controller.ts   | removeItem         | DELETE /mv/customer/cart/:id |
| ...              | ...            | ...                           | ...                | ... |
```

With this map in place, story specs can use the operation name (`add item`) for human-readability and the route+function for test scaffolding, without inventing either at spec time.
