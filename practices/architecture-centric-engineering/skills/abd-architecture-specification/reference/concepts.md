# Architecture Specification — Concepts

## What is an architecture specification?

An **architecture specification** is a **specification directory** — doc, runnable template slice, rules, and scanners — that defines how domain concepts and stories instantiate as code in a chosen stack. Where the directory lives does not matter; the shape does:

```
<spec>/
├── architecture-specification.md   ← the doc
├── template/                       ← runnable code + domain artifacts + tests
├── templates/                      ← parameterized scaffold (peer to template/)
├── rules/                          ← what generated code must satisfy
└── scanners/                       ← automated checks against those rules
```

The markdown doc details one or more cross-cutting **mechanisms** the system needs and defines how each is realized across the architecture's layers. A finished spec lets a reviewer answer three questions in one read:

- **What is the principle?** — the one-line rule that, if you violated it, your code would no longer be "in this architecture".
- **What is the pattern?** — the named, repeatable shape that implements the principle.
- **How does it actually run?** — the participants, the file layout, the call sequence, and the test approach.

---

## Mechanism

**Architecture mechanism** is a family-level concept — see [`reference/architecture-mechanism.md`](../../../reference/architecture-mechanism.md) for the definition and the canonical categories. The specification document devotes one section (or file) to each mechanism the project has actually decided, and is the deepest-fidelity treatment: it gives each mechanism the full five-part shape below.

**Document once, assign later.** After discovery (or the first run that creates a mechanism), later exploration, specification, and engineering **assign** the existing section. Only **create** when the scope needs a mechanism that has no complete section yet.

---

## Assign vs create

Assignment is recorded on the **story map**, not in a separate mechanism table. Each node — **system**, **epic**, or **sub-epic** — carries an **`architecture-spec`** field: a list of specification directory paths. **More than one spec may be assigned to the same node** (e.g. stack baseline + scoped companion).

| Node level | Assign when | Create when |
| --- | --- | --- |
| **System** | Complete spec directory exists for this stack | Bootstrapping a new architecture |
| **Epic** | Spec(s) already document this epic's mechanisms and patterns | Epic needs a new spec directory or mechanisms not in any assigned spec |
| **Sub-epic** | Assigned spec(s) already cover this sub-epic's stories | Sub-epic needs new mechanism sections or template slices |

Before writing anything, **discover** existing specification directories — skills repo (`specs/<arch>/`), project workspace, or `mechanism-registry.json`.

**Workflow:**

1. **Locate the story map node** for this run and read its current `architecture-spec` list.
2. **Assign** — add paths to existing complete spec directories; cite them on the node; do not rewrite their content.
3. **Create** — when no assigned spec covers the node, author a new spec directory or extend an assigned spec with missing mechanism sections only.
4. **Inside each assigned spec** — each mechanism is documented once: assign existing `## Mechanism: <Name>` sections; create only what is missing.

| Situation | Action |
| --- | --- |
| Spec directory exists and covers this node | **Assign** — add path to node's `architecture-spec` |
| Node needs a second, scoped spec (integration, increment) | **Assign** — add second path; node holds multiple specs |
| No spec covers this node | **Create** — new spec directory; add path to `architecture-spec` |
| Mechanism missing inside an assigned spec | **Create** — add or finish that section only |

**Avoid:** regenerating a full `architecture-specification.md` when only new mechanisms are needed; duplicating a mechanism under a different heading when an equivalent section exists; forking a full spec copy per epic when a companion spec suffices.

**Example:** Epic *Wire Payment* assigns `specs/mern/` (stack) and `docs/architecture/wire-transfer/` (companion). Sub-epic *Refund Processing* adds `docs/architecture/refunds/` (create). Mechanisms Error Handling and Persistence are assigned inside `specs/mern/`; Refund validation is created in the refunds companion.

---

## Kanban ticket run (quick pass vs long pass)

When pulled from a kanban board, **always run this skill** — kanban does not auto-skip.

1. **Locate the story map node** and read its `architecture-spec` field.
2. **Check** assigned spec directories and mechanism sections inside them; consult `mechanism-registry.json` when present.
3. **Quick pass** — every needed spec is already assigned on the node and every mechanism inside those specs is complete → update story map links only; mark skill done.
4. **Long pass** — node needs a new spec path and/or mechanisms missing inside assigned specs → create only what is missing; add paths to `architecture-spec`; register creates in `mechanism-registry.json` when used.

---

## Run modes

| Mode | Produces | When to use |
| --- | --- | --- |
| **document** | `architecture-specification.md` | Mechanism sections only; `template/` already exists on the assigned spec |
| **template** | `template/` runnable code, spec `templates/` scaffold, `rules/`, `scanners/` | Code-first; doc assigned separately or refreshed later |
| **both** (default) | Full specification directory | New spec or full refresh — template slice first, then doc |

**Document** — write or update mechanism sections, diagrams, and walkthroughs. Walkthrough steps reference files under `template/` when present; otherwise use parameterized pattern comments pointing at `templates/`. Do not edit `template/` unless the user asks.

**Template** — produce the runnable slice under `template/` (domain spec, spec-by-example, tests, production code), mirror it in `templates/`, and bootstrap or update `rules/` and `scanners/`. Skip `architecture-specification.md`.

**Both** — run template pass first (with human review before the document pass), then author the doc and validate both passes.

When pulled from kanban without an explicit mode, default to **both**. When the ticket or user names only one deliverable ("doc only", "template only"), honor that mode.

**Kanban stage defaults:** Exploration → **document**; Specification → **template**.

---

## Principle vs. pattern

A **principle** is a one-liner stance the architecture takes — a constraint the team is not allowed to break. It is technology-agnostic, fits in a sentence, and survives in a corridor conversation.

A **pattern** is the full description of how the team has chosen to satisfy that principle in this project: the named shape, its structural options, its benefits, and its trade-offs.

---

## Layered description vs. mechanism reference

**Instantiating the Domain** is the common section of every architecture reference. It has four sub-sections: **Principles** (naming rules, layer qualifiers), **Architecture Flow** (how one interaction traverses the tech stack — diagram + table), **Module Layout** (folder tree + shared artefact table), and **Participants** (class diagram showing inheritance, interface implementation, and delegation across tiers). **Mechanisms** cover each runtime concern (web client, app server, persistence, …) — content differs by stack.

---

## Reference document structure

Every `architecture-specification.md` follows the skeleton in **`templates/architecture-specification.md`**. Summary:

| Section | Scope |
|---------|-------|
| Overview | Architecture name, mechanism list, sources |
| **Instantiating the Domain** | **Common** — four sub-sections: **Principles** (naming rules, layer qualifiers), **Architecture Flow** (diagram + `\| Tech \| File \| Instantiates from domain \|` table), **Module Layout** (folder tree), **Participants** (class diagram — inheritance, interface, delegation) |
| Mechanisms | Tech-specific — one section per runtime concern; five-part shape each (no testing subsection inside mechanisms) |
| **Testing Architecture** | **Common** — four sub-sections: **Principles** (story instantiates tests; stub at tier boundary only), **Testing Scope** (4-layer diagram — domain unit / HTTP adapter / React adapter / browser; entry point, real, stubbed, asserts), **Module Layout** (domain unit tests beside domain classes; lowest sub-epic = file; story = `describe`; scenario = `it`), **Participants** (base helper = scenario vocabulary; tier helpers = adapter implementations; class diagram) |
| Example | `template/` pointer — runnable code, `specification-by-example.md`, `domain-spec.md`, tests |
| Rules and Validation | `rules/` + `scanners/` — one-row-per-rule table + run command |
| References | Worked example path, normative patterns, standards |

**Architecture Flow** is a sub-section of Instantiating the Domain — not a standalone top-level section.

**Named spec directories** (e.g. `specs/<arch>/`) are authoritative for their architecture. Assign; do not recreate.

---

## The five-part shape

Every mechanism section has the same five-part shape:

1. **Principles & Patterns** — one-liner principle(s) followed by a named pattern description per principle.
2. **File Structure** — where the mechanism's code lives (a fenced tree).
3. **Participants** — the classes/modules involved, as a class diagram or table.
4. **Flow** — a sequence diagram of one representative scenario.
5. **Walkthrough Example** — a step-by-step narration of the same scenario with example code.

Testing content belongs in the top-level **Testing Architecture** section — not inside individual mechanism sections.

---

## Section organization

The reference is **always one file**: `architecture-specification.md`.

- **Combined section** — when there are only **2–3 mechanisms** and they are tightly related, use one `## Mechanisms` section that weaves the five-part shape across all of them.
- **One section per mechanism** — the default for **4+ mechanisms**, and always allowed. Each mechanism gets its own `## Mechanism: <Name>` section.

---

## Code and test standards

Code in walkthroughs follows the project's coding standard (defaulting to `abd-clean-code` when in scope). Test snippets follow the project's testing standard (defaulting to `abd-story-acceptance-test` when in scope).

---

## Template code conventions

Every run that includes **template** mode produces a **runnable template slice** under `template/` alongside the reference doc (when mode is **both**). The template slice and the doc are a single artifact — they must stay in sync.

### Template domain artifacts

Alongside template code, produce two domain artifacts in the **same folder**:

| File | Produced per |
|------|--------------|
| `specification-by-example.md` | `abd-story-specification` — scenarios for the story the template implements |
| `domain-spec.md` | `abd-domain-specification` — typed domain specification |

**Template layout** (`template/`):

```
template/
├── specification-by-example.md      # Given/When/Then scenarios for the story
├── domain-spec.md                   # Typed domain spec for the example module
├── packages/
│   ├── app-server/                  # Composition root — mounts routers, injects repos
│   ├── app-client/                  # Composition root — React app, routes
│   └── <domain>/
│       ├── shared/
│       │   ├── <Entity>.ts
│       │   ├── <Entity>s.ts
│       │   ├── <entity>.schema.ts
│       │   ├── <Entity>Repository.ts
│       │   └── <entity>s.test.ts    ← domain unit tests — live here, next to the classes
│       ├── server/
│       │   ├── <Entity>sServer.ts
│       │   ├── <Entity>Router.ts
│       │   └── <Entity>RepositoryServer.ts
│       └── client/
│           ├── <Entity>Client.ts
│           ├── <Entity>sClient.ts
│           ├── <Entity>.api.ts
│           ├── use<Entity>s.ts
│           ├── <Entity>ListView.tsx
│           └── <Entity>CardView.tsx
└── tests/
    └── <epic>/                           # Epic → folder
        ├── <sub-epic>_server.test.ts     # Sub-epic → file | Story → describe | Scenario → it
        ├── <sub-epic>_client.test.tsx
        ├── <sub-epic>_e2e.spec.ts
        └── helpers/
            ├── <sub-epic>.base.ts        # scenario vocabulary + test data constants
            ├── <sub-epic>.server.ts      # seeds DB; Supertest HTTP
            ├── <sub-epic>.client.ts      # vi.mock at API boundary; Testing Library
            └── <sub-epic>.e2e.ts         # Playwright page navigation
```

**File naming** (real-story examples — all names derive from domain classes):

| Layer | Pattern | Example |
|-------|---------|---------|
| Shared entity | `<Entity>.ts` | `Recipient.ts` |
| Shared collection | `<Entity>s.ts` | `Recipients.ts` |
| Shared schema | `<entity>.schema.ts` | `recipient.schema.ts` |
| Shared repository interface | `<Entity>Repository.ts` | `RecipientRepository.ts` |
| Domain unit tests | `<entity>s.test.ts` in `shared/` | `recipients.test.ts` |
| Server collection | `<Entity>sServer.ts` | `RecipientsServer.ts` |
| Server router | `<Entity>Router.ts` | `RecipientRouter.ts` |
| Server repository impl | `<Entity>RepositoryServer.ts` | `RecipientRepositoryServer.ts` |
| Client entity | `<Entity>Client.ts` | `RecipientClient.ts` |
| Client collection | `<Entity>sClient.ts` | `RecipientsClient.ts` |
| Client API | `<Entity>.api.ts` | `Recipient.api.ts` |
| Client hook | `use<Entity>s.ts` | `useRecipients.ts` |
| Test file | `<sub-epic>_<tier>.test.ts` | `select-recipient_server.test.ts` |
| Base helper | `<sub-epic>.base.ts` | `select-recipient.base.ts` |
| Tier helper | `<sub-epic>.<tier>.ts` | `select-recipient.server.ts` |

When assigning from a named spec, assign all three together — code, spec-by-example, and domain spec.

### Template validation (mandatory)

Every run that **creates or edits** template code (modes **template** or **both**) must validate it against the **architecture spec's** rules and scanners — not only this skill's document rules.

| Pass | `--skill-root` | `--workspace` | What it checks |
|------|----------------|---------------|----------------|
| **Doc** | `abd-architecture-specification/` | `architecture-specification.md` | Mechanism shape, TOC, diagrams, walkthroughs |
| **Template** | `specs/<arch>/` (or project's spec copy) | `specs/<arch>/template/` or `template/` | Tier extensions, layer purity, tests, package layout |

Workflow per **`execute-skill-using-skills-rules`:**

1. Read `specs/<arch>/rules/` before writing template code.
2. After authoring — AI pass: per-rule verdict on template code.
3. Run `run_scanners.py` with `--language` when applicable; fix all failures; re-run until green.

Named spec reference command (MERN):

```bash
python foundational/skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root practices/architecture-centric-engineering/specs/mern \
  --workspace practices/architecture-centric-engineering/specs/mern/template \
  --language typescript
```

Do not declare the template slice complete while any scanner fails.

### Folder layout

```
template/
├── <mechanism-name>/        # kebab-case, matches mechanism heading in the doc
│   ├── <domain>.<ext>
│   ├── <presentation>.<ext>
│   └── tests/
│       └── test_<scenario>.<ext>
└── <next-mechanism>/
    └── ...
```

One sub-folder per mechanism in the reference. Folder name must match the mechanism heading exactly (kebab-case, lower-case).

### Two template domain modes

**Toy / hello-world** — use when no real project context exists or when isolating the mechanism is clearest. Pick a simple domain (Calculator, Pet Store, Library) and keep the three-layer shape (Domain → Presentation → Tests).

**Real story** — draw class and file names from the actual domain model and stories in the engagement. Follow the file naming table above.

### Non-negotiable rules

- Every file runs immediately — no stubs, no placeholder bodies, no missing imports.
- Every Walkthrough step in the doc references a specific file by path (e.g. `template/error-handling/calculator.py`).
- When the doc changes, the template code changes in the **same edit**. When template code is fixed, the corresponding Walkthrough step is updated in the **same edit**.
- Tests are named after story scenarios or user-facing behaviors, not implementation details.
