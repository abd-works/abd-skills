# Generate — abd-domain-model

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — domain model format: class blocks, constructor, properties, methods, collaborators, invariants, subtypes. **The `## Code format` section is authoritative for the code shape** — read it in full before touching any code.
- **`../../references/domain-model-json.md`** — `domain-model.json` schema, containment hierarchy, and upstream mapping from glossary terms and domain-language bullets.
- **`../supporting/domain-ops/SKILL.md`** — validate/read/write `domain-model.json` on disk (`domain_graph_cli.py`, `domain_map`).
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

## Discover the target format

Before writing anything, figure out **what channel is the source of truth for this engagement**:

1. **Code already exists** at `<deliverables-folder>/` or in the project's domain source folder (`src/**/*.ts`, `src/**/*.py`, `src/**/*.java`, etc.)
   → **The AI edits code directly.** No CLI. No markdown. Load [`../templates/domain-model.<ext>`](../templates/) for the shape, walk the existing files, add or refine classes, properties, and operation signatures. Keep the same file per KA — do not split (D26).

2. **Markdown or JSON source exists but no code yet**
   → **Bootstrap once with the CLI**, then edit code:
     ```bash
     python domain_graph_cli.py generate \
         --input <deliverables-folder>/domain-model.json \
         --out <src-folder>/ \
         --language typescript \
         --fidelity model
     ```
     After bootstrap, the CLI is done. All further edits are in the code files. Never re-run `generate` against a folder that already has code — the command refuses to overwrite existing files.

3. **Nothing exists yet** (greenfield discovery)
   → **Emit the markdown shape first** ([`../templates/domain-model-template.md`](../templates/domain-model-template.md)) to give humans a low-fidelity surface to argue over, then move to code as soon as the shape stabilises. Markdown is a *stepping stone*, not the destination.

## Output shape

| Source-of-truth channel        | Deliverable                                                     |
| ------------------------------ | --------------------------------------------------------------- |
| Code (default target)          | One `<ka-slug>.<ext>` per KA under the module folder            |
| Markdown (early exploration)   | `docs/domain/model/domain-model.md`                             |
| JSON (diagram / scanner cache) | `docs/domain/model/domain-model.json` — produced by CLI derive from code, not authored by the AI |

**Canonical markdown/JSON paths** (see `common/reference/folder-conventions.md`):

- `docs/domain/model/domain-model.md`
- `docs/domain/model/domain-model.json`
- `docs/domain/model/domain.json`

Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `modules/<module-name>-domain-model.md` (and matching `.json`).

## After write — validate with domain-ops

When code is the source of truth, derive JSON back with:

```bash
export PYTHONPATH="practices/domain-driven-design/skills/supporting/domain-ops/scripts"
python3 practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py \
    derive-from-fs --source <src-folder>/ --out docs/domain/model/domain-model.json
python3 practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py \
    read --file docs/domain/model/domain-model.json
```

When markdown is the source of truth (early exploration), validate the JSON that mirrors it:

```bash
python3 practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py \
    read --file docs/domain/model/domain-model.json
```

## Quality bar

Every behavior bullet from the Domain Language maps to at least one property or operation. Properties are typed — never raw `String`; use domain types, constrained enums, or typed primitives. Operations have typed parameters and return types (or `void`). Subtype classes carry only deltas. No stereotypes, no relationship flavour, no invariant methods, no interaction methods — those belong at specification fidelity. State marker set to `domain-model`.
