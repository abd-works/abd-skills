# drawio-domain-sync — Concepts

## Source types

Three domain model artifacts can feed this skill. Each expresses domain concepts at a different fidelity level. All three render with the same card-rows-collaborators shape; the only difference is where rows and collaborators come from.

- **Domain Language** (`abd-domain-language`) — plain-English concept blocks with verb-led behavior bullets, `*italicized*` cross-concept references, and invariants. Output file: `domain-language.md` or `<name>-domain-language.md`. The diagram represents each `### concept` as a class card; each behavior bullet becomes one row with the bullet's italicized terms as the collaborator column (`<bullet text> : Collaborator, Collaborator`); each unique cross-concept italicized reference becomes one folded association edge. `### Subtype *is a type of* Base` drives an inheritance edge. `### term *(boundary)*` scoped stubs render as imported cards with a `«boundary: OwningModule»` stereotype. Property/instance stubs become property rows on the parent or lightweight stub cards. Invariants appear in the third compartment. This is the second pass after a completed Domain Language file — analogous to how the Domain Model's collaborator column feeds the diagram. See `rules/class-diagram-domain-language-bullets-become-rows.md`.
- **Domain Model** (`abd-domain-model`) — typed class blocks with constructors, typed properties, method signatures, hidden collaborators, and invariants. Output file: `domain-model.md` or `<name>-domain-model.md`. The diagram shows class boxes with responsibilities as rows, each annotated with its collaborator types using `name : Collaborator` notation (e.g., `modifier : Character, Imposed Conditions`). Collaborator names also drive association edges between classes. Invariants appear in the class compartment.
- **Domain Specification** (`abd-domain-specification`) — full typed Class Model with typed properties (`+ name: Type`), typed method signatures, ownership semantics. Output file: `class-model.md` or `<name>-class-model.md`. The diagram is a full UML class diagram with typed property and operation compartments.

The agent reads whichever source type is present and maps its content to class diagram elements. Domain Specifications produce the richest diagrams; Domain Models produce slightly leaner cards with the same row+collaborator shape; Domain Language files produce the leanest cards by reading rows from prose bullets and collaborators from italicized term references.

**Picking the source.** When multiple source artifacts exist for the same scope, prefer the highest-fidelity one available (Domain Specification > Domain Model > Domain Language). The Domain Language render is the right choice when only the Domain Language file has been written — typically the first time the team wants a visual of the domain, before the Domain Model has been run.

## Page per Key Abstraction

A Key Abstraction is a named grouping in the source file, introduced with a `## **KA Name**` heading. Each KA gets **one Draw.io page**. The page name matches the KA name exactly. All concepts that belong to that KA appear as classes on its page. When a concept from one KA extends or uses a concept from another KA, that external concept appears on the page as an imported ghost class — see **cross-model ancestors** below.

## AI-driven layout

Positioning is a judgment call, not a script output. The agent reads the source, identifies which class is the base, which are children, which are collaborators, and then places them so the diagram reads naturally. The rules in `rules/` — base classes above derived classes, cross-model ancestors visible at the page top, distinct anchor points when multiple edges leave the same class side — are applied as reasoning constraints, not as CLI flags.

## Sync back

When a user edits a diagram in Draw.io, the `sync-to-model` command reads the diagram and produces a diff against the source model file. The agent reviews the diff with the user and applies confirmed changes to the source model. The source model remains the authoritative text; the diagram is a derived view.

**Domain Language sync caveat.** When the source is a Domain Language file (`*-domain-language.md`), sync-back is **one-way for new/deleted concepts only**. Card additions, card deletions, and inheritance-edge additions round-trip back to the Domain Language file as new/deleted `### concept` headings and `### Subtype *is a type of* Base` headings. Row edits, collaborator-list edits, and free-text bullet rewrites do **not** round-trip — the Domain Language file's prose form is the authoritative record, and bullet-level changes must be made in the markdown directly. Domain Model and Domain Specification sources do not have this asymmetry.

## Incremental vs full rendering

**Prefer incremental edits when the diagram already exists.** If a `.drawio` file is present and the source model has changed, use `update-class`, `add-class`, `delete-class`, and edge commands to apply only the changes — do not regenerate the entire file from scratch. Full regeneration destroys any manual repositioning the user has done in Draw.io. Only use full rendering when creating a diagram for the first time.

## Persisting module build scripts

When a full render produces a bespoke Python script that builds the diagram programmatically, **keep the script in the destination repo** at `<repo-root>/scripts/build_<name>_diagram.py`. These scripts are re-runnable, extendable, and auditable — a readable record of every layout decision. When the model changes incrementally, prefer editing the existing build script over writing a new one.

Each script should:
1. Import `drawio_tools` from the skill's `scripts/` directory.
2. Build the entire diagram atomically — load/create the mxfile, add all pages, classes, and edges, save once.
3. Run `audit_diagram_report()` at the end and print the result.
4. Be runnable standalone: `python scripts/build_<name>_diagram.py`.

## CLI reference

The full CLI command reference — `add-class`, `update-class`, `delete-class`, `move`, all relationship commands, `inspect`, and `sync-to-model` — is documented in [`diagrams.md`](../drawio-domain-sync/diagrams.md) alongside detailed layout guidelines, UML relationship selection, and cross-model import conventions. Read that file during rendering; SKILL.md does not duplicate those mechanics.
