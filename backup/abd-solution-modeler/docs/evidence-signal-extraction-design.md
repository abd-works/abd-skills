# Design: Evidence-Signal Extraction — Concept Triangulation

## The Problem

LLM-assisted domain extraction has a critical failure mode:

**If Concept v1 is weak, the rest of the pipeline becomes confirmation bias over bad anchors.**

Phase 2 (Hypothesize / Concept Guidance v1) currently asks the AI to guess concepts from chunks. Phase 3 (Extract) then does *guided* extraction — it mines evidence *guided by* those concepts. When the initial concept list is poor:

- Extraction is biased toward what the AI guessed
- Evidence analysis reinforces the bad anchors
- The resulting model is lacking because the foundation was wrong

The solution is not "improve the prompt." It is **concept triangulation**: multiple orthogonal concept discovery signals *before* creating Concept v1.

---

## Core Insight: Let the Text Speak First

**Current flow (problematic):**

```
concepts → evidence
```

The AI guesses concepts, then extraction looks for evidence that supports them.

**Target flow:**

```
evidence → concept clusters → concepts
```

Let the text speak first. Derive concept clusters from evidence signals. *Then* name and structure concepts.

---

## Three Jobs, Three Actors

The pipeline mixes three distinct jobs. Separating them makes the system stable and debuggable.

| Job | What it does | Best actor | Why |
|-----|--------------|------------|-----|
| **1. Signal detection** | Detect terms, patterns, structures in text | **Code** | Deterministic, fast, stable across runs |
| **2. Pattern discovery** | Discover what patterns matter for this corpus | **AI** | Recognizes domain-specific language usage |
| **3. Semantic interpretation** | Turn signals into domain concepts and behaviors | **AI** | Requires understanding and synthesis |

**Current mistake:** AI does all three. Extraction output changes every run. When it's wrong, you rewrite prompts.

**Correct architecture:** AI configures the extractor. Code runs extraction. AI consolidates.

---

## AI Configures, Code Extracts

AI should *design the rules* of the extractor, not *perform* the extraction.

| AI role | Output | Code role |
|---------|--------|-----------|
| Propose TF weights by structural position | `weights.json` | Apply weights deterministically |
| Propose definition/rule/comparison patterns | `patterns.json` | Run regex/parsers against corpus |
| Propose grammatical structures (SVO, etc.) | `grammar_rules.json` | Search for those patterns |

**Benefits:**

- **Reproducibility** — same config → same extraction
- **Debugging** — adjust `patterns.json` instead of prompts
- **Speed** — code scans large corpora; AI does not
- **Stability** — extraction output is deterministic

---

## Twelve Evidence-Signal Techniques

These techniques are used in NLP and knowledge extraction systems. They produce orthogonal signals that triangulate domain concepts.

### 1. Term Frequency + Structural Weighting

Not raw TF. Weight terms by *where* they appear.

| Location | Weight | Example |
|----------|--------|---------|
| Heading | +5 | `## Attack Resolution` → Attack |
| Table header | +4 | `\| Effect \| Resistance \|` → Effect, Resistance |
| Definition sentence | +3 | "An attack is..." → Attack |
| Capitalized domain noun | +2 | "The Character rolls..." → Character |
| Regular occurrence | +1 | — |

Aggregate. High-weighted terms (Attack, Effect, Defense, Condition, Power) surface before the AI guesses them.

**Implementation:** Code. AI can propose domain-specific weights (e.g., rulebooks vs API specs).

---

### 2. Definition Sentence Detection

Rulebooks and specs use explicit definition patterns:

- *X is a ...*
- *X represents ...*
- *X refers to ...*
- *X describes ...*

**Regex example:** `^([A-Z][a-zA-Z ]+) (is|represents|refers to|describes)`

**Example:** "A Damage effect represents physical harm." → `DamageEffect`

One of the highest-signal concept extractors.

---

### 3. Dependency Pattern Mining (Relationship Discovery)

Detect grammatical patterns, not just nouns.

- *Attack targets Defense*
- *Effect applies Condition*
- *Character uses Power*

Using dependency parsing: `subject → verb → object`

Produces early candidates for Attack, Defense, Effect, Condition, Power through *behavior*, not just noun frequency.

---

### 4. Noun Phrase Mining (NP Chunking)

Use an NLP parser to extract noun phrases:

- attack check
- resistance check
- affliction effect
- damage effect
- character condition

Cluster. Derive core nouns: Attack, Check, Effect, Condition, Character.

Common in knowledge extraction systems.

---

### 5. Co-occurrence Graphs

Build a co-occurrence matrix: term A appears near term B.

| A | B |
|---|---|
| Attack | Defense |
| Effect | Resistance |
| Effect | Condition |
| Character | Power |

Cluster the graph. Highest-degree nodes are often core domain concepts.

---

### 6. Table Mining

Tables in rulebooks contain enormous signal.

Extract:

- Table name
- Column headers
- Row labels

**Examples:** Condition Table, Power Effect Table, Attack Difficulty Table → clean domain vocabularies.

Heavily used in rule system extraction.

---

### 7. Enumeration Pattern Detection

Look for patterns:

- *types of X include:*
- *X may be:*
- *X categories are:*

**Example:** "Conditions include: Dazed, Stunned, Paralyzed" → Condition + children.

---

### 8. Contrast Detection

When text compares things: *Unlike X, Y does...*

**Example:** "Unlike Dodge resistance, Toughness represents durability." → Dodge, Toughness (sibling concepts).

Strong concept indicators.

---

### 9. Actor Detection

Extract entities that initiate actions:

- *character rolls*
- *player selects*
- *system determines*

→ Character, Player, System. Anchors interaction modeling.

---

### 10. Topic Modeling (LDA / Clustering)

Cluster chunks by topic. Example clusters:

- attack resolution
- character abilities
- conditions
- power effects

Extract representative nouns from each cluster. Domain modules emerge automatically.

---

### 11. Graph Centrality

After building the term/relationship graph, run:

- Degree centrality
- PageRank
- Betweenness

Top nodes are usually foundation concepts: Character, Effect, Attack, Condition, Power.

---

### 12. Verb-Centered Interaction Graph (Strongest Signal)

**The single strongest signal for domain concepts:** verbs applied to nouns repeatedly.

- *attack targets defense*
- *attack check compares defense*
- *attack effect causes condition*

Concepts that appear in many verb structures are almost always real domain objects.

Used in compilers and ontology mining. More powerful than TF-IDF for rule-system domains.

---

## Recommended Architecture

### Current (Problematic)

```
Phase 1: Chunk extraction
Phase 2: AI guesses concepts        ← weak anchor
Phase 3: Code extracts (guided)      ← biased by bad concepts
Phase 4: Index
Phase 5: AI revises
```

### Target

```
Phase 1:     Chunk extraction
Phase 1.5:   Evidence signal extraction (code)
             - term frequency + structural weighting
             - definition detection
             - NP mining
             - dependency triples
             - table mining
             - co-occurrence graph
             - (optional) AI corpus analysis → extraction config
Phase 2:     AI concept synthesis (merges signals, names concepts, groups modules)
Phase 3:     Code extracts (guided by synthesized concepts)
Phase 4:     Index
Phase 5:     AI revises
```

---

## Phase 1.5 Outputs

Pure code. Outputs:

| File | Contents |
|------|----------|
| `term_candidates.json` | Weighted terms from TF + structural position |
| `definition_candidates.json` | Concepts from definition sentences |
| `dependency_actions.json` | Subject–verb–object triples |
| `cooccurrence_graph.json` | Term co-occurrence edges |
| `topic_clusters.json` | Chunk clusters + representative terms |
| `table_vocabularies.json` | Table names, headers, row labels |

Optional (AI-configured):

| File | Contents |
|------|----------|
| `weights.json` | TF weights by structural position (AI-proposed) |
| `patterns.json` | Definition/rule/comparison patterns (AI-proposed) |
| `grammar_rules.json` | SVO patterns to search (AI-proposed) |

---

## AI Corpus Analysis (Optional Phase 1.4)

Before Phase 1.5, AI can scan the corpus and propose extraction configuration:

1. **TF weights** — domain-specific (rulebooks: high weight on rules, tables; API specs: high weight on method definitions, schema)
2. **Definition patterns** — "X is a", "X represents", plus domain-specific variants
3. **Grammatical patterns** — SVO structures that express rules (e.g., "X targets Y", "X applies Y")

Output: `extraction_config.json`. Phase 1.5 code uses this config.

---

## Phase 2 Becomes Concept Synthesis

Phase 2 is no longer "AI guesses concepts." It is **concept synthesis**:

- Merge signals from term_candidates, definitions, dependency triples, co-occurrence, tables, clusters
- Name concepts (normalize "damage effect" → DamageEffect)
- Group into modules
- Identify mechanisms and actors

The AI is consolidating evidence, not hallucinating concepts.

---

## When Extraction Is Wrong

**Current:** Rewrite prompts. Re-run. Hope.

**With this design:** Adjust config files.

- `patterns.json` — add/remove definition patterns
- `weights.json` — tune structural weights
- `grammar_rules.json` — add SVO patterns

Re-run extraction. Deterministic. Debuggable.

---

## Summary

| Principle | Implication |
|-----------|-------------|
| **Concept triangulation** | Multiple orthogonal signals before Concept v1 |
| **Evidence first** | evidence → clusters → concepts (not concepts → evidence) |
| **AI configures, code extracts** | AI proposes rules; code runs them |
| **Three jobs, three actors** | Signal detection (code), pattern discovery (AI), semantic interpretation (AI) |
| **Phase 1.5 is pure code** | Deterministic, fast, stable |
| **Phase 2 is synthesis** | AI merges signals, does not guess |

---

## Subtype vs type-field discrimination (research complete)

The modifiers bucket has been deprecated. A core weakness remains: the system conflates **subtypes** (inheritance — extra data/behavior) with **type fields** (e.g. red vs blue — same flow, different value).

**Research findings:** See [subtype-vs-type-field-research.md](./subtype-vs-type-field-research.md) for full analysis. Key takeaways:

| Source | Actionable insight |
|--------|--------------------|
| **Feature modeling** | Mechanical difference test: does switching variant change which rules apply? |
| **Ontology learning** | Hearst patterns ("such as", "is a") → subtype candidates; attribute patterns ("has", "of type") → type field candidates |
| **DDD heuristics** | Behavior differences → subtype; same flow, different value → type field |
| **Proposed strategy** | Pattern pre-filter + mechanical difference test + behavioral evidence (different actions/decisions per variant?) |

**Linguistic modification** (adjectives/adverbs): Syntactic only; weak signal for rule-mechanics. Not sufficient alone.

---

## References

**Design & phases**

- Design: [design-concept-anchored-pipeline.md](./design-concept-anchored-pipeline.md) — artifact shape, phase sequence, research grounding for evidence buckets
- Phases: `phases/built/configure_concept_extraction_parameters.md` — current Phase 2 behavior
- Evidence: `evidence/` — current extraction outputs

**Research grounding for the twelve techniques**

- Term frequency + structural weighting: standard in information retrieval; domain-specific weighting used in ontology learning (Wong et al., AusDM 2007)
- Definition detection: common in ontology learning from text (Navigli & Velardi, Computational Linguistics 2004)
- Dependency / SVO triples: PropBank, FrameNet, textacy; semantic role labeling for knowledge graph extraction (TakeFive, Springer 2021)
- NP chunking: standard NLP; terminology extraction uses noun phrases (Wikipedia: Terminology extraction)
- Co-occurrence graphs: used in ontology learning, topic modeling, knowledge extraction
- Table mining: rule-system extraction (evidence-signal doc §6)
- Enumeration patterns: ontology learning, taxonomy induction
- Contrast detection: concept differentiation in ontology learning
- Actor detection: semantic role labeling (agent/theme); event extraction (ACE)
- Topic modeling (LDA): standard; domain clustering
- Graph centrality: knowledge graph analysis; concept importance
- Verb-centered interaction graph: "strongest signal" — used in compilers, ontology mining; more powerful than TF-IDF for rule-system domains (evidence-signal doc §12)
