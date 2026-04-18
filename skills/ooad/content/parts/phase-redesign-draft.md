# Phase redesign draft

## Old → New mapping

| Old # | Old phase | → | New # | New phase | New stage |
|-------|-----------|---|-------|-----------|-----------|
| 0 | workspace-and-config | → | **p0a** | workspace-and-config | Stage 0 — Orient |
| 1 | domain-scan | → | **p0b** | domain-scan | Stage 0 — Orient |
| 2 | nouns-verbs-rules-and-states | → | **p1** | nouns-verbs-rules-and-states | Stage 1 — Scaffold |
| 3 | raw-candidates | → | **p2** | candidate-classes *(cluster only — no DDD stereotypes)* | Stage 1 — Scaffold |
| 4 | thing-vs-data-about-a-thing | → | **p3** | thing-vs-data-about-a-thing *(first-class object or property? confirm or demote)* | Stage 1 — Scaffold |
| 5 | responsibilities-and-collaborators | → | **p4** | responsibilities-and-collaborators *(CRC pass — English only)* | Stage 2 — Model |
| 6 + 7 | properties-and-operations + relationships-and-cardinality | → | **p5** | properties-methods-and-relationships *(properties → operations → relationships + cardinality; one pass)* | Stage 2 — Model |
| 12 + 13 + 14 | inheritance-when-behavior-generalizes + abstract-classes-and-interfaces + prefer-composition | → | **p6** | inherit-interface-or-compose *(one phase, three lenses: is-a → inherit; shared contract → interface; has-a → compose; evaluated simultaneously)* | Stage 2 — Model |
| — | *(no equivalent — was premature in raw-candidates)* | → | **p7** | classify-stereotypes *(Entity, ValueObject, Policy, Role, Event, Process — confirmed after model shape is known)* | Stage 3 — DDD patterns |
| 18 | what-changes-together | → | **p8** | design-bounded-contexts *(bounded contexts, seams, aggregates — what changes atomically)* | Stage 3 — DDD patterns |
| 8 | invariants-in-the-model | → | **p9** | invariants | Stage 4 — Behaviour |
| 15 | model-state-transitions | → | **p10** | state-and-lifecycle *(states, transitions, guards, birth → retirement arc)* | Stage 4 — Behaviour |
| 19 | validate-with-scenarios | → | **p11** | scenario-validation | Stage 4 — Behaviour |
| 10 | watch-for-bloated-classes | → | **check-single-responsibility** | validator — does this class have more than one reason to change? | Gate after p5 / p8 |
| 11 | smashed-abstractions-and-hidden-roles | → | **check-hidden-roles** | validator — is this name doing double duty? | After p7 |

| 16 | iterative-refinement | → | dropped | practice within every phase | — |
| 17 | tension-as-a-signal | → | dropped | term-registry at point of discovery | — |
| 20 | refine-names | → | dropped | naming within each phase | — |

---

## New phase list (clean)

### Stage 0 — Orient
- p0a `workspace-and-config`
- p0b `domain-scan`

### Stage 1 — Scaffold
- p1 `nouns-verbs-rules-and-states` — per module; raw vocabulary, no classification
- p2 `candidate-classes` — cluster nouns and verbs into named stubs; English only, no stereotypes
- p3 `thing-vs-data-about-a-thing` — first-class object or property on another class? confirm or demote each stub

### Stage 2 — Model
- p4 `responsibilities-and-collaborators` — CRC pass; one responsibility sentence, exclusions, collaborator names; English only
- p5 `properties-methods-and-relationships` — properties → operations → relationships + cardinality; one pass in that order
- p6 `inherit-interface-or-compose` — for each relationship: is-a → inherit; shared contract → interface; has-a/uses-a → compose; evaluated simultaneously

### Stage 3 — DDD patterns
- p7 `classify-stereotypes` — Entity, ValueObject, Policy, Role, Event, Process; confirmed after model shape and relationships are known; no `?` carries past this phase
- p8 `design-bounded-contexts` — name bounded contexts and seams; confirm aggregates (what changes atomically per operation)

### Stage 4 — Behaviour
- p9 `invariants` — rules that must always hold; guard clauses attached to operations
- p10 `state-and-lifecycle` — states, transitions, guards, birth → retirement arc
- p11 `scenario-validation` — walk real scenarios through the model; find gaps, wrong owners, missing operations

---

## Validators (not phases)

These are **checks**, not design steps. They can run as a checker after every phase or as a gate at the end of Stage 2 and Stage 3 — decision TBD.

| Old phase | Renamed validator | Question it asks |
|-----------|-------------------|-----------------|
| `watch-for-bloated-classes` | `check-single-responsibility` | Does this class have more than one reason to change? |
| `smashed-abstractions-and-hidden-roles` | `check-hidden-roles` | Is this name doing double duty? Is there a hidden role that should be its own type? |

**When to run — options:**
- After every phase (continuous) — catches problems early but adds overhead
- Gate at end of Stage 2 (Model complete) — before Behaviour begins
- Gate at end of Stage 3 (Behaviour complete) — before treating the run as done
- Both Stage 2 and Stage 3 gates — recommended; model shape is stable enough at each point

---

## Practices (not phases — apply continuously inside every phase)

| Old phase | Practice | When it applies |
|-----------|----------|-----------------|
| `iterative-refinement` | If this pass contradicts a prior decision, fix it before continuing forward | Every phase |
| `tension-as-a-signal` | Record in term-registry (`Tension` note) at the moment it surfaces | Every phase |
| `refine-names` | Naming is corrected in term-registry at the phase where the name is first stabilised | Every phase |

---

## Net result

| | Old | New |
|-|-----|-----|
| Phases | 19 (+ 1 deferred) | 11 (p0a–p11) |
| Validators | 0 | 2 (`check-single-responsibility`, `check-hidden-roles`) |
| Stages | 6 | 3 (Orient, Scaffold, Model, Behaviour) |
| Dropped | 0 | 3 (`iterative-refinement`, `tension-as-a-signal`, `refine-names`) |
