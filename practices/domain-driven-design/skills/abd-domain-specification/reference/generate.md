# Generate — abd-domain-specification

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — typed notation: properties, operations, object initialisation, relationships (aggregation/composition/association), collections, inheritance, invariants, interactions, entities and value objects. **The `## Code format` section is authoritative for the code shape** — read it in full before touching any code.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

## Discover the target format

Before writing anything, figure out **what channel is the source of truth for this engagement**:

1. **Code already exists** at `<deliverables-folder>/` or in the project's domain source folder (`src/**/*.ts`, `src/**/*.py`, `src/**/*.java`, etc.)
   → **The AI edits code directly.** No CLI. No markdown. Load [`../templates/domain-specification.<ext>`](../templates/) for the shape, walk the existing files, add or refine classes, properties, operations, invariant methods, interaction methods. Keep the same file per KA — do not split (D26).

2. **Markdown or JSON source exists but no code yet** (typical: earlier phases produced `domain-model.md` or `domain-model.json`; this phase upgrades to specification fidelity in code)
   → **Bootstrap once with the CLI**, then edit code:
     ```bash
     python domain_graph_cli.py generate \
         --input <deliverables-folder>/domain-model.json \
         --out <src-folder>/ \
         --language typescript
     ```
     After bootstrap, the CLI is done. All further edits are in the code files. Never re-run `generate` against a folder that already has code — the command refuses to overwrite existing files.

3. **Nothing exists yet** (greenfield discovery)
   → **Emit the markdown shape first** ([`../templates/domain-specification-scaffold.md`](../templates/domain-specification-scaffold.md)) to give humans a low-fidelity surface to argue over, then move to code as soon as the shape stabilises. Markdown is a *stepping stone*, not the destination.

## Output shape

| Source-of-truth channel        | Deliverable                                                     |
| ------------------------------ | --------------------------------------------------------------- |
| Code (default target)          | One `<ka-slug>.<ext>` per KA under the module folder            |
| Markdown (early exploration)   | `<deliverables-folder>/[<name>-]domain-specification.md`        |
| JSON (diagram / scanner cache) | `<deliverables-folder>/domain-model.json` — produced by CLI derive from code, not authored by the AI |

The **code file is not** an in-place enrichment of the domain model file. It is a fresh artifact per KA in the folder layout described in `concepts.md` § `File / folder granularity`.

## Quality bar

Every property is typed and justified by a domain responsibility. Every operation is a fully typed signature. Every class has object initialisation decided (marked with `@initialisation`). Composition / aggregation properties carry the corresponding tag. Subtype classes carry only deltas. Every non-trivial operation has a matching `@interaction` empty method whose name summarises the coordination. Every operation with an inherent rule has a matching `@invariant` empty method whose name IS the rule. No free-text step-by-step narrative lives in doc comments — it lives in the method body of concrete implementations or in `domain-context.md`. Variable names in interaction bodies use domain language. State marker (in `<deliverables-folder>/state.json` or equivalent) set to `domain-specification`.
