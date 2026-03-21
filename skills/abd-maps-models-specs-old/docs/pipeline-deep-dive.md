# abd-maps-models-specs — pipeline deep dive: mistakes, root causes, and a better approach

This document analyzes the **designed process** (Stages 1–3, rows 4–11), the **artifacts** (chunks → scaffold → classification → deepen → integrate), and **why** end-to-end runs can produce object models that fail basic OO discipline (over-broad supertypes, spurious `extends`, noun explosion)—the same failure modes an expert review would flag on **any** domain where the skill is used for story mapping plus OO-oriented solution modeling.

It does **not** assume the current pipeline is correct. It separates **what is structurally sound** from **what systematically steers the model wrong**. **No particular subject matter** (payments, compliance, games, etc.) is required for the argument; where an **example artifact** is useful, it lives under `test/` and is **illustrative**, not normative.

---

## 1. What the pipeline actually optimizes for

On paper, the skill optimizes for:

- **Traceability** — every bold concept name and many fields tie to `chunk_id`s (`chunks_must_be_referenced`).
- **Narrative alignment** — epics and confirming stories use the **same spellings** as `concepts[].name` (`scaffold-concept-story-name-alignment`).
- **Breadth without reading everything** — foundational spine, then **K ≈ 30%** of chunks fully read for scaffold.
- **Layered discovery** — base → categories → implementations (`concept-layering-scaffold`), variant families classified before modeling (`classify-variants-before-modeling`).

What it **does not** mechanically enforce:

- **Semantic substitutability** (Liskov) for `extends`.
- **Separation of modeling roles** — in any domain, at least these **categories** should stay distinguishable until promoted deliberately (names are illustrative, not domain-specific):
  - **Domain types** — stateful abstractions you intend to implement as classes or equivalents.
  - **Documentation artifacts** — section structure, examples, introductory prose, non-normative notes.
  - **Tabular or matrix material** — lookup data, matrices, scoring grids (often *data* or *policies*, not subtypes of one “table” class).
  - **Procedural or scheduling constructs** — turn order, phase rules, allocation of attention or resources in time (often *policies* or *interpreters*, not subclasses of a single “check” or “action” type unless the source truly unifies them).
- **Distinguishing** “mentioned in this chunk” from “this chunk **defines** a class.”

So the **optimand** is *document-faithful, citation-heavy JSON*, not *a minimal, behaviorally coherent OO model*. Those two diverge quickly on **large, heterogeneous sources** (regulations, handbooks, multi-chapter specs).

---

## 2. Stage 1 — Extract context (steps 1–3)

### 2.1 What works

- **Chunking with intent** — `evidence_type`, `document_region`, merge rules for PDF tables, definition runs, and exclusions are the right *shape* of problem for downstream modeling.
- **Per-chunk metadata** — `candidate_concepts`, `modeling_priority`, `retrieval_tags` are the right *hooks* for routing chunks to modules **without** forcing every mention into `concepts[]` yet.
- **`parts/context.md` “Prompt for study”** — asking *why* we are extracting and which sections are useless is underused in automation but **correct**: scope drives curation.

### 2.2 Mistakes / failure modes

| Issue | What goes wrong |
|--------|------------------|
| **Chunks are syntactic, not semantic** | A “chunk” is often *one rule block* or *one table*. The model later treats **each chunk as permission to mint one concept**, especially when classification lists `primary_concepts` per chunk. |
| **No “ontology layer” in Stage 1** | `candidate_concepts` are string hints. There is no persisted **non-class** taxonomy: *term*, *role*, *mechanism*, *table row*, *worked example*, *sidebar*. Everything collapses toward “concept candidate.” |
| **Evidence type ≠ modeling kind** | `example` vs `domain-rule` is recorded, but **later steps barely use it** to block subclassing. An **example** paragraph still becomes a **subtype** if the LLM needs a noun for alignment. |
| **Volume vs. signal** | Fine-grained chunking increases **N**; **K = 0.3N** scales, but **stratified lexical sampling** does not prioritize high-`modeling_priority` chunks. Breadth can miss the *defining* section while reading lots of marginal mentions. |

### 2.3 Root mistake

**Stage 1 produces a corpus optimized for retrieval and citation, not for stable class discovery.** That is acceptable **if** later stages *refuse* to elevate every retrieved mention to a type. Today, later stages *don’t refuse strongly enough*.

---

## 3. Stage 2 — Row 4: Foundational mechanisms (spine)

### 3.1 What works

- **Concept-first spine** — “Module + epic without `concepts[]` is decoration” is the right anti-pattern to name.
- **Human checkpoint** before breadth — correct **gate**.
- **3–7 mechanisms** — forces prioritization.

### 3.2 Mistakes / failure modes

| Issue | What goes wrong |
|--------|------------------|
| **`extends` allowed at spine** | `modules-epics-foundational-spine.md` invites `extends` when a concept is “clearly a subtype.” At skim depth, **everything** looks like a subtype of a few large umbrellas the model already introduced (whatever the source’s chapter headings suggest). |
| **Epic pressure** | ≥2 `confirming_stories` and **Verb Noun** epics push the model to **invent story-shaped nouns** that then **must** become `concepts[]` rows to pass alignment — a **noun explosion** before the domain is understood. |
| **Scanners don’t see OO** | `chunks_must_be_referenced`, `no_duplicates`, `epic_requires_confirming_stories`, `no_junk_concepts` — none detect **wrong `extends`**. |

### 3.3 Root mistake

The spine optimizes for **naming + citation + story linkage**, not for **behavioral cores**. You get a **label graph** that *looks* validated because scanners pass.

---

## 4. Stage 2 — Row 5: Modules / epics scaffold (K-read breadth)

### 4.1 What works

- **Concepts before epics** (step order) — stated repeatedly; when followed, it helps.
- **`depends_on`** — forcing explicit provider/consumer edges is valuable for ordering deepen passes.
- **`evidence_stage: hypothesis → scaffolded`** — good *idea* for gating detail.

### 4.2 Mistakes / failure modes

| Issue | What goes wrong |
|--------|------------------|
| **K reads ≠ representative** | Lexical spread across chunk IDs favors **even coverage of file ids**, not **conceptual coverage** of each module. Different modules often need different *shapes* of reading; one stratified list doesn’t guarantee each **mechanism** is hit. |
| **`extends` + `properties` in one breath** | Breadth tells the model to add `extends` for is-a and properties for has-a, but **without a mandatory variant-classification pass per module**, the default LLM behavior is **inheritance** because it’s fewer JSON fields than composing roles. |
| **Concept layering rule is soft** | `concept-layering-scaffold` says “defer exhaustive enumeration to deepen” — but Pass 1 classification and story pressure **already** add dozens of names in practice (see below). |
| **Alignment rule side effect** | `scaffold-concept-story-name-alignment` (100% match) **punishes** leaving a proper noun only in story text. The **cheap fix** is **add a concept row**, not **fix the story**. |

### 4.3 Root mistake

Breadth is framed as **“expand concepts and cite chunks”** but not **“prove behavioral families before naming subtypes.”** So the scaffold **fills in** before the hard **classify-variants** decisions are made **per mechanism**.

---

## 5. Stage 2 — Rows 6 / 6a: Concept classification (AI + code)

This is where many runs **lock onto** “every chunk evidences concepts” and **coarse supertypes** **accumulate children**—regardless of industry.

### 5.1 Documented behavior (honest)

`parts/steps/concept-classification.md` **admits**:

- Pass 1 returns **coarse** umbrella names, not full subtype enumerations for every family.
- Finer subtypes appear when **Concept Classes and Stories** re-harvests — **if** coverage is there.

So classification **by design under-produces** fine types in Pass 1, then **later steps over-produce** concrete rows to close gaps.

### 5.2 Code-driven mistakes (`classify_chunks.py`)

The implementation includes **hardcoded string patterns** that, when substrings co-occur in a chunk, append **relationship** rows (including labels like **`inherits`**) between **named concepts** drawn from a fixed illustrative list. That is **not** a proof of substitutability; it is **heuristic co-occurrence**.

**Effect:** Pass 2 (code) can **inject inheritance-flavored relationships** before any careful reading of whether the **child** type is substitutable for the **parent** everywhere the source cares. That **reinforces** the failure mode of **over-broad parents + default inheritance.**

**`MODULE_COOCCURRENCE`**-style lists also **prime** the AI pass with **tight coupling** between module labels that may reflect **documentation co-location**, not **valid generalization** in your target model.

*Remediation is domain-agnostic:* ship **suggested** edges with confidence / provenance, or **omit** regex-driven inheritance until Integrate.

### 5.3 AI-driven mistakes

| Issue | What goes wrong |
|--------|------------------|
| **Primary concepts per chunk** | The natural output is **nouns the chunk talks about**, not **types whose instances share state/behavior**. |
| **Seed spec bias** | Doc says: if the incoming `map-model-spec.json` is **sparse**, Pass 1 stays coarse; if **rich**, it proliferates names. The scaffold **seed** therefore **steers** classification toward either under- or over-modeling. |
| **Merge strategy** | AI evidence + code gap-fill **union** evidence onto concepts. There is no **“demote to mention / not a class”** pass. |

### 5.4 Root mistake

**Classification merges “mentioned in text” with “is-a domain class” and sometimes adds inheritance-like edges from patterns.** That is **actively hostile** to good OO. The step is **evidence attachment**, not **taxonomy discipline**.

---

## 6. Stage 2 — Row 7: Concept classes and stories (deepen)

### 6.1 What works

- **Topological order by `depends_on`** — correct.
- **Pass 1 exhaustive harvest** — “add every evidenced concept not yet in module” is **right for completeness** if **class** is the only representation — see below.
- **Explicit** `extends` vs composition in `parts/domain.md` and deepen text — **right vocabulary**.

### 6.2 Mistakes / failure modes

| Issue | What goes wrong |
|--------|------------------|
| **Harvest = classify every noun** | Pass 1 says: scan **full text** of all chunks bound to the pair and add **every** domain concept evidenced. On a **large normative corpus**, that is **many** proper nouns **as classes** unless a human or a **strong classifier** rejects them. |
| **No staged typing** | There is no mandatory intermediate artifact: **Glossary term** → **Mechanism** → **Class** → **Subtype**. The JSON jumps straight to **Class**. |
| **Story hierarchy 4–9** | Forces **regrouping** that may **duplicate** conceptual material under sub-epics, increasing **surface area** for new concept names. |
| **Integrate deferred** | `classify-variants-before-modeling` says **defer** subtypes until harmonize — but **deepen Pass 1** **adds** subtypes eagerly. **Rules conflict.** |

### 6.3 Root mistake

**Deepen optimizes for completeness of `concepts[]` per module**, not **minimality of types**. **Completeness without a reject gate** on a dense source yields an unmaintainable type list.

---

## 7. Stage 2 — Row 8: Integrate and harmonize

### 7.1 What works

- Synonym merge, `extends` repointing, enum vs subtype decisions — **necessary**.

### 7.2 Mistakes / failure modes

| Issue | What goes wrong |
|--------|------------------|
| **Comes too late** | If **hundreds** of bad rows exist, “finalize subtypes/enums” becomes **merge theater**, not **design**. |
| **Scanners still not semantic** | `no_duplicates` / `domain_interaction_sync` don’t answer “should this exist?” |

---

## 8. Cross-cutting meta-mistakes (the real list)

1. **Citation pressure → reification pressure** — Chunks must be referenced; alignment must match; the **cheapest** fix is **more concept rows**.
2. **Inheritance is easier than composition in JSON** — One `extends` string vs. many `properties` with typed collaborators.
3. **Rules conflict in time** — Layering and “classify variants first” **defer** detail; **classification + deepen harvest** **add** detail early.
4. **Code suggests inheritance** — Pattern-matched `inherits`-style edges **bias** the model before disciplined review.
5. **No “not a class” outcome** — Nothing in the pipeline **strongly labels** a mention as **non-class** (e.g. narrative aside, worked example, tabular layout, process label).
6. **Story map and domain modeled in one JSON** — Coupling **narrative verification** to **type taxonomy** **via** simple **noun** (or surface-string) **concept classification**—and alignment that treats story words as **type** candidates—**amplifies** noun explosion. (A single artifact is not inherently wrong if references are **typed** and verification is **behavioral**; the failure mode is **noun-for-name** coupling.)
7. **30% breadth** — Good for **coverage sampling**, weak as **sole** input to **global** `extends` trees without a **second opinion** pass (human or batch classifier).

---

## 9. What would a *right* approach look like?

Think in **four layers**, **persisted explicitly**, before most rows become `concepts[]`:

| Layer | Question it answers | Stored as |
|--------|---------------------|-----------|
| **A. Mention / term** | What nouns appear? | Glossary / term index (could extend `context_index` or a `terms.json`) |
| **B. Mechanism / pipeline** | What **named processes** does the source describe (workflows, resolution pipelines, lifecycles)? | Small set of **mechanism** nodes with **steps**, not classes—unless you later prove one mechanism *is* a class |
| **C. Domain type** | What **stateful things** participate with **distinct** state/lifecycles? | **`concepts[]`** — **sparingly** |
| **D. Subtype / enum** | For each family in C, did we run **classify-variants** and choose enum vs extends? | Decision log + **then** `extends` / `EnumType` |

**Operational rules:**

1. **Nothing becomes a `concept` until it passes** “owns state or distinct operations **not** reducible to a property on a broader type.” **Reject gate** (AI or checklist) **before** JSON row.
2. **Stage 1** (or a new **Stage 1b**): tag chunks with **`modeling_kind`** (domain-agnostic values such as: definition, rule, table, example, narrative aside, structural/layout). **Classification and deepen must not** subclass from **example** or **layout** rows without promotion.
3. **Kill or quarantine regex inheritance** in `classify_chunks.py`. Replace with **candidate** relationships **`suggested_relationship`** with **low confidence**, or drop entirely until Integrate.
4. **Breadth K**: **stratify by** `modeling_priority` and **`evidence_type`**, not only **chunk id** — e.g. ensure each module gets **top-N** high-signal chunks, then fill spread.
5. **Foundational spine**: **forbid `extends`** except where **two** chunk anchors show **behavioral** specialization. **Spine = mechanisms + cores**, not **trees**.
6. **Concept classification**: rename mentally to **“attach evidence to existing concepts; propose new terms as *candidates*”** — **merge** into `concepts[]` only in Integrate or a **typed** sub-step.
7. **Deepen Pass 1**: replace **“every noun”** with **“every term in B/C layers not yet mapped”** — map **terms** to **mechanisms** first, **types** second.
8. **Align scaffold-concept-story-name-alignment** with **aliases**: allow story-only nouns if they map to **`term_id`** or **`[see Glossary: X]`** without minting **Concept X** class.

**Confirming story (behavioral definition).** A **story** in the sense that matters for OO alignment is **not** a domain phrase, policy label, or noun cluster in isolation (those may be **terms**, **rules**, or **parts of acceptance criteria**). A **valid** confirming story is at minimum: a **primary actor** executes a **behavior** (operation) **on** a **domain concept**, producing a **meaningful change of state** (or other defined outcome) **on** that concept; optionally, a **supporting actor** reacts with a **behavior** **on** another **concept**. **Verbs name operations**, not extra concept rows named after the verb. If text cannot be resolved to **concept + operation + state change**, it is not a confirming story—treat it as **noise** or **reframe** before it drives `concepts[]` or alignment. Scanners and alignment rules should **not** assume “every story word is a concept candidate”; they should privilege **behavioral coverage** and **interaction** over **surface noun** parity with `concepts[].name`.

---

## 10. Concrete recommendations (priority order)

1. **Remove or neutralize inheritance injection from code** (`RELATIONSHIP_PATTERNS` / any `inherits` from string match). This is the **highest-leverage** code fix.
2. **Add a “candidate concepts” queue** (JSON array or separate file) **written by** classification, **merged into** `concepts[]` only in **Integrate** after variant rules — **breaks** the chunk→class reflex.
3. **Make `classify-variants-before-modeling` a gate** between **Row 5** and **Row 6** (per module): **enum vs extends** written down **before** full corpus classification.
4. **Tighten foundational spine**: **no `extends`** in row 4; **only** named cores + citations + epics.
5. **Change K selection** to **priority-stratified** + lexical spread, not **only** lexical spread.
6. **Deepen Pass 1**: split into **Term harvest** (glossary) vs **Type harvest** (concepts) with **explicit promotion** criteria.
7. **Optional**: split **story map** validation from **domain** validation — e.g. stories may reference **terms**; only **interaction** steps must reference **Concept** names — reduces forced noun explosion.

---

## 11. Closing

The skill’s **written philosophy** (composition over inheritance, layering, variant classification, evidence stages) is **aligned with good OO**. The **as-run pipeline** rewards **citation density** and **name alignment** and **allows** early, cheap **`extends`**, while **code** sometimes **suggests inheritance** from patterns. **That combination** produces bad incentives on **any** large, heterogeneous corpus—not a single subject matter.

Fix the **incentives and gates**, not just the prompt wording.

---

*For a **concrete** illustration of failure modes on one fixture (same skill, one test corpus), see the artifact critique next to that fixture’s `map-model-spec.json` under `test/`. This document stays **skill-level** and **domain-neutral**.*
