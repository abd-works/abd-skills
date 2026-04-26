# Process — abd-ooad

**Pipeline:** **Stage 0 — Orient** → **Stage 1 — Scaffold** → **Stage 2 — Model** → **Stage 3 — DDD patterns** → **Stage 4 — Behaviour**.

**Validators** (`check-single-responsibility`, `check-hidden-roles`) run at defined gates — after p5 and after p7.

**Practices** (`iterative-refinement`, `tension-as-a-signal`, `refine-names`) are continuous — they apply within every phase.

---

## Outcome

You finish with an **object-oriented domain model** that maps domain behaviour to classes, responsibilities, properties, operations, relationships, stereotypes, invariants, and lifecycle. The model is validated by walking real scenarios. `term-registry.md` carries the full evidence trail with phase tags; `domain-model.md` is the canonical model artifact.

---

## Stage 0 — Orient

**Purpose:** Confirm workspace configuration; scan source material for anchors, tensions, and module boundaries.

| # | Phase ID | Description |
|---|----------|-------------|
| 0a | workspace-and-config` | Set `skill_path`, `active_skill_workspace`, confirm `skill-config.json` |
| 0b | domain-scan` | Scan source, identify anchors and tensions, sketch initial module boundaries, seed nbhjjjjjjjjbloterm-registry.md` |

---

## Stage 1 — Scaffold

**Purpose:** Settle domain language and produce named class stubs for each module slice. No structure, no DDD stereotypes — English only.

| # | Phase ID | Description |
|---|----------|-------------|
| p1 | nouns-verbs-rules-and-states` | Extract nouns, verbs, rules, and states per module slice |
| p2 | candidate-classes` | Cluster nouns aond verbs into named class stubs (`<< Kind? >>`) |
| p3 | thing-vs-data-about-a-thing` | For each stub: does it have identity? Entity candidate or property/VO |

---

## Stage 2 — Model

**Purpose:** Build full OO structure — responsibilities, properties, operations, relationships, and structural mechanisms (inherit / interface / compose). No DDD stereotypes or context seams yet.

| # | Phase ID | Description |
|---|----------|-------------|
| p4 | responsibilities-and-collaborators | CRC pass: one responsibility sentence per class, named collaborators |
| p5 | properties-methods-and-relationships | Three-pass: properties → operations → relationships and cardinality |
| — | **Validator:** `check-single-responsibility` | Run after p5 — does any class have more than one reason to change? |
| p6 | `inherit-interface-or-compose` | For each relationship: is-a → inherit; shared contract → interface; has-a → compose |

---

## Stage 3 — DDD patterns

**Purpose:** Apply **tactical** DDD (stereotypes per class) then **strategic** DDD (bounded contexts, aggregates, seams). *Classify* before *design bounded contexts* so aggregate and context boundaries rest on stable roles.

| # | Phase ID | Description |
|---|----------|-------------|
| p7 | `classify-stereotypes` | Assign one DDD stereotype per class; replace `<< Kind? >>` stubs |
| — | **Validator:** `check-hidden-roles` | Run after p7 — does any generic noun cover more than one role? |
| p8 | `design-bounded-contexts` | Name bounded contexts and seams; confirm aggregates — what changes atomically per operation |

---

## Stage 4 — Behaviour

**Purpose:** Define the rules and dynamic behaviour the model must enforce.

| # | Phase ID | Description |
|---|----------|-------------|
| p9 | invariants | Identify and attach domain constraints; express as guard conditions |
| p10 | state-and-lifecycle | Full lifecycle: states, transitions, guards mapped to invariants, domain events |
| p11 | scenario-validation | Walk real scenarios step by step; every step must map to a class and operation |

---

## Practices (continuous)

These are not phases or gates. They apply within every phase pass.

| Practice ID | When it applies |
|-------------|----------------|
| `iterative-refinement` | Any phase — if this pass contradicts a prior decision, fix it before continuing |
| `tension-as-a-signal` | Any phase — ambiguity, conflict, or contested ownership → record a `Tension` note |
| `refine-names` | Any phase — names are hypotheses; refine when the model reveals a better name |

See `practices/` for detail on each.

---

## Stage map

| Stage | Name | Phase IDs |
|-------|------|-----------|
| 0 | Orient | `workspace-and-config`, `domain-scan` |
| 1 | Scaffold | `nouns-verbs-rules-and-states`, `candidate-classes`, `thing-vs-data-about-a-thing` |
| 2 | Model | `responsibilities-and-collaborators`, `properties-methods-and-relationships`, `inherit-interface-or-compose` |
| 3 | DDD patterns | `classify-stereotypes`, `design-bounded-contexts` |
| 4 | Behaviour | `invariants`, `state-and-lifecycle`, `scenario-validation` |
| — | Validators | `check-single-responsibility`, `check-hidden-roles` |

---

## Phase chronicle

| Phase ID | Purpose | Stage |
|----------|---------|-------|
| `workspace-and-config` | Set workspace and config | 0 · Orient |
| `domain-scan` | Scan, anchors, tensions, sketch | 0 · Orient |
| `nouns-verbs-rules-and-states` | Extract nouns, verbs, rules, states | 1 · Scaffold |
| `candidate-classes` | Cluster into named class stubs | 1 · Scaffold |
| `thing-vs-data-about-a-thing` | Identity question: entity or property/VO | 1 · Scaffold |
| `responsibilities-and-collaborators` | CRC pass | 2 · Model |
| `properties-methods-and-relationships` | Properties → operations → relationships | 2 · Model |
| `inherit-interface-or-compose` | Structural mechanism per relationship | 2 · Model |
| `classify-stereotypes` | DDD stereotype per class | 3 · DDD patterns |
| `design-bounded-contexts` | Bounded contexts, seams, aggregate boundaries | 3 · DDD patterns |
| `invariants` | Domain constraint guard conditions | 4 · Behaviour |
| `state-and-lifecycle` | States, transitions, events | 4 · Behaviour |
| `scenario-validation` | Scenario walkthrough; gap resolution | 4 · Behaviour |
| `check-single-responsibility` | Validator — class has one reason to change | Gate after p5 / p8 |
| `check-hidden-roles` | Validator — no smashed abstractions | Gate after p7 |

**Optional:** `model-in-layers` — not part of the default pipeline. Run with `--phase model-in-layers`.

---

## Build and generate

- **One phase:** `python scripts/base/generate.py --phase <phase-id>`
- **One stage group:** `python scripts/base/generate.py --stage <key>` (keys in `skill-config.json → process_stages`)
- **Build:** `python scripts/base/build.py`
- **List:** `python scripts/base/generate.py --list-stages` / `--list-phases`

---

## Implementation notes

**Strategy before deep runs:** After `domain-scan`, fill `strategy.md` from `templates/strategy.md` — slices, coverage, phase-id execution plan. See `library/strategy-led-generation.md`.

**Stage boundaries:** After completing a stage, confirm direction before heavy rework in the next. Revisits are new rows on `strategy-run-checklist.md` — not a separate rerun document.

**Artifact hygiene:** Analysis in `domain-model.md`; long verbatim evidence in `terms.md` per module; `term-registry.md` = Term + Targets + Notes with `[pN]` phase tags. After markdown stabilizes, render `*.drawio`.
