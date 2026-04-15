# Phase 3 — Concept Extraction

**Actor:** AI + Code loop

## Purpose

Run code extraction with `extraction_config.json` (from Phase 2), evaluate signal quality, and **loop back to Phase 2** when signals fail. Outputs `concept_signals/concept_signals.json`.

**Principle:** AI calibrates (Phase 2), code extracts (Phase 3), AI evaluates. When extraction is wrong, go back to Phase 2 — adjust `extraction_config.json`, then run Phase 3 again. Loop between Phase 2 and Phase 3 until all 12 signals pass.

## Trigger

concept extraction, concept signals, term candidates, definition candidates, run extraction

## Inputs

- `context/context_chunks.json` — normalized chunks from Phase 1
- `generated/extraction_config.json` — from Phase 2 (configure_concept_extraction_parameters)

## Signal Reference (for Phase 2 and evaluation)

Phase 2 uses these signal definitions when calibrating. Phase 3 uses the evaluation checklist below. Full details:

This phase runs as **three separate AI prompts**, each focused on a group of related signals. Each scan reads the same chunk sample but looks for different things.

---

### Scan A — Structure Calibration

**Signals:** 1 (TF weights), 2 (definition patterns), 6 (table mining), 7 (enumeration patterns)

**What the AI looks at:** How is this document formatted? What structural cues carry concept signal?

**For each signal, observe and propose:**

#### Signal 1 — TF Weights

*Summary:* Weight terms by where they appear (heading, table, definition, etc.). High-weighted terms surface before the AI guesses them.

Look at where concepts appear in the document structure.

- Are headings concept names (high weight) or just chapter titles (lower weight)?
- Are bold terms domain concepts or emphasis?
- Are tables core rule definitions (high weight) or just formatting?
- Are list items led by concept names?

**Defaults to adjust:**

```json
"tf_weights": {
  "heading": 5,
  "table_header": 4,
  "definition_sentence": 3,
  "capitalized_noun": 2,
  "regular": 1,
  "bold_term": 3,
  "list_item_lead": 2
}
```

#### Signal 2 — Definition Patterns

*Summary:* Rulebooks and specs use explicit definition patterns (X is a..., X represents...). One of the highest-signal concept extractors.

Look at how this corpus defines things. Not just "X is a..." — what syntax does it actually use?

- Does it use "X is a..."? "X represents..."? "X: a type of..."?
- Does it use behavioral definitions? "X alters Y", "X imposes Y", "X resists Y"?
- Are behavioral patterns more revealing than static "is a" definitions?

**Defaults to adjust:**

```json
"definition_patterns": [
  "^([A-Z][a-zA-Z ]+) (is|represents|refers to|describes|means)\\s+"
]
```

Add domain-specific patterns you observe. Rank them — which patterns produce the strongest concept signal in this corpus?

#### Signal 6 — Table Mining

*Summary:* Tables contain enormous signal. Extract table name, column headers, row labels → clean domain vocabularies.

Look at how tables are used.

- Are tables markdown (`|...|`) or HTML?
- Do headers contain concept names or just column labels like "Name", "Value"?
- Are row labels concepts?

**Defaults to adjust:**

```json
"table_mining": {
  "header_pattern": "^\\s*\\|([^|]+)\\|",
  "concept_columns": ["header", "row_label"],
  "ignore_patterns": ["page", "chapter", "table of contents"]
}
```

#### Signal 7 — Enumeration Patterns

*Summary:* Patterns like "types of X include", "X may be" reveal parent concepts and children (e.g., Condition + Dazed, Stunned, Paralyzed).

Look at how this corpus lists variants or types.

- "Effects include: Damage, Affliction..."
- "The following modifiers apply:"
- "Available options: X, Y, Z"

**Defaults to adjust:**

```json
"enumeration_patterns": [
  "types of ([A-Z][a-zA-Z ]+) include",
  "([A-Z][a-zA-Z ]+) may be",
  "([A-Z][a-zA-Z ]+) categories are",
  "([A-Z][a-zA-Z ]+) can be one of",
  "forms of ([A-Z][a-zA-Z ]+)"
]
```

Add domain-specific enumeration syntax you observe.

**Scan A output:** `tf_weights`, `definition_patterns`, `table_mining`, `enumeration_patterns` fields.

---

### Scan B — Behavior Calibration

**Signals:** 3 (dependency verbs), 4 (noun phrase mining), 8 (contrast patterns), 9 (actor detection), 12 (verb interaction)

**What the AI looks at:** What happens in this domain and who does it? What verbs and noun structures carry behavioral signal?

**For each signal, observe and propose:**

#### Signal 3 — Dependency Verbs

*Summary:* Subject→verb→object patterns (Attack targets Defense, Character uses Power). Produces concept candidates through behavior, not just noun frequency.

Look at what verbs express relationships between concepts.

- Domain-specific relationship verbs: "resists", "imposes", "grants", "inflicts"?
- Business verbs: "approves", "submits", "escalates"?
- API verbs: "returns", "accepts", "validates"?

**Defaults to adjust:**

```json
"dependency_verbs": [
  "has", "have", "contains", "includes", "uses", "requires",
  "applies", "targets", "modifies", "affects"
]
```

Add domain-specific verbs. Remove generic ones that produce noise in this corpus.

#### Signal 4 — Noun Phrase Mining

*Summary:* Extract noun phrases (attack check, damage effect, character condition). Cluster to derive core nouns.

Look at how concepts are expressed as phrases.

- Single nouns ("Attack") or compound phrases ("Area Effect Attack", "Damage Resistance Check")?
- What's the typical phrase length?
- What's a reasonable minimum frequency to filter noise?

**Defaults to adjust:**

```json
"np_mining": {
  "min_frequency": 2,
  "max_words": 4,
  "prioritize_compound": true
}
```

#### Signal 8 — Contrast Patterns

*Summary:* When text compares things (Unlike X, Y does...), both X and Y are strong concept indicators, often siblings.

Look at how this corpus compares or contrasts concepts.

- "Unlike X, Y does..."
- "X differs from Y in..."
- Domain-specific comparison language?

**Defaults to adjust:**

```json
"contrast_patterns": [
  "unlike ([A-Z][a-zA-Z ]+),\\s+([A-Z][a-zA-Z ]+)",
  "([A-Z][a-zA-Z ]+) differs from ([A-Z][a-zA-Z ]+)",
  "while ([A-Z][a-zA-Z ]+).*,\\s+([A-Z][a-zA-Z ]+)",
  "in contrast to ([A-Z][a-zA-Z ]+)",
  "as opposed to ([A-Z][a-zA-Z ]+)"
]
```

#### Signal 9 — Actor Detection

*Summary:* Entities that initiate or trigger actions (Triggering-Actor / Responding-Actor). *Not* every concept that appears as the subject of a verb — those are covered by dependency (Signal 3) and verb-interaction (Signal 12) signals.

- Who are the actors in this domain? (character, player, system, gamemaster?)
- What verbs do actors use? (rolls, selects, activates, submits?)

**Defaults to adjust:**

```json
"actor_detection": {
  "actor_verbs": ["rolls", "selects", "chooses", "determines", "decides", "assigns", "activates", "initiates", "creates", "submits"],
  "known_actors": [],
  "actor_noun_pattern": "(character|player|user|system|gamemaster|admin|manager|operator)"
}
```

Replace defaults with domain-specific actors and verbs.

#### Signal 12 — Verb Interaction

*Summary:* The strongest signal. Verbs applied to nouns repeatedly (attack targets defense, effect causes condition). Concepts in many verb structures are almost always real domain objects.

Look at what action verbs recur with domain nouns.

- What are the key domain action verbs?
- Which generic verbs should be excluded because they produce noise? (e.g., "check", "roll" might be too generic in a rulebook)
- What verb patterns express rules?

**Defaults to adjust:**

```json
"verb_interaction": {
  "min_verb_frequency": 3,
  "verb_patterns": [],
  "exclude_verbs": ["is", "are", "was", "were", "has", "have", "can", "may", "should", "would", "could"],
  "prioritize_domain_verbs": true
}
```

**Scan B output:** `dependency_verbs`, `np_mining`, `contrast_patterns`, `actor_detection`, `verb_interaction` fields.

---

### Scan C — Tuning Review

**Signals:** 5 (co-occurrence), 10 (topic modeling), 11 (centrality) + noise filters

**What the AI looks at:** Corpus-level characteristics — size, density, structure. These signals are code-computed; the AI just picks reasonable parameters.

#### Signal 5 — Co-occurrence

*Summary:* Build co-occurrence matrix (term A appears near term B). Highest-degree nodes are often core domain concepts.

- How large are the chunks? (chunk-level window or sentence-level?)
- How tightly co-located are concepts?

**Defaults to adjust:**

```json
"cooccurrence": {
  "window_size": "chunk",
  "min_count": 2,
  "max_edges": 300
}
```

#### Signal 10 — Topic Modeling

*Summary:* Cluster chunks by topic. Extract representative nouns from each cluster. Domain modules emerge automatically.

- How many distinct topic areas does the corpus cover?
- What domain-specific words appear everywhere but carry no concept signal? (these are domain stop words)

**Defaults to adjust:**

```json
"topic_modeling": {
  "n_clusters": 8,
  "min_cluster_size": 3,
  "stop_words": ["the", "a", "an", "is", "are", "was", "were", "be", "been", "being"],
  "domain_stop_words": []
}
```

#### Signal 11 — Centrality

*Summary:* After building the term/relationship graph, run degree/PageRank/betweenness. Top nodes are usually foundation concepts.

- Is the domain tightly connected (use betweenness) or hub-and-spoke (use degree)?

**Defaults to adjust:**

```json
"centrality": {
  "metric": "degree",
  "top_n": 20,
  "threshold": 0.02
}
```

#### Noise Filters

*Summary:* Exclude chunks that carry no concept signal (chapter headers, title page, section separators, flavor text).

- What repeated junk appears in chunks? Chapter headers, title page text, section separators, flavor text?

**Defaults to adjust:**

```json
"noise_filters": [
  "table of contents", "appendix", "index", "license",
  "copyright", "acknowledgments", "foreword", "preface"
]
```

**Scan C output:** `cooccurrence`, `topic_modeling`, `centrality`, `noise_filters` fields.

---

## Outputs

- `concept_signals/concept_signals.json` — extracted signals

## Loop: Phase 2 ↔ Phase 3

Phase 3 runs extraction and evaluation. When signals fail, **go back to Phase 2** to adjust config, then run Phase 3 again. Loop until all 12 pass.

**CRITICAL: AI MUST verify.** Phase 3 is not complete until Step 2 (evaluate with subagent) has been run. Do not skip evaluation — extraction output often contains junk (pronouns, headers, generic verbs). The evaluation catches this and drives config fixes.

### Step 1 — Run extraction

Run: `python scripts/extract_concepts.py -i <context_chunks.json> -o <concept_signals_dir> -c <extraction_config.json>`

If extraction crashes (regex error, missing capture group), **go to Phase 2** — fix the offending pattern in `extraction_config.json`, then run Phase 3 again.

### Step 2 — Evaluate with subagent

Launch a subagent to read `concept_signals/concept_signals.json` and run this checklist:

| # | Signal | Check | Fail threshold |
|---|--------|-------|----------------|
| 1 | tf_weights | Term count reasonable for corpus size | < 50 terms |
| 2 | definition_patterns | Definitions are real concepts, not pronouns/headers | > 50% junk |
| 3 | dependency_verbs | Dependency count reflects domain verb richness | < 200 in a rule-heavy corpus |
| 4 | np_mining | Noun phrases are domain-relevant, not structural junk | > 30% structural headers |
| 5 | cooccurrence | Edge count non-trivial | < 100 edges |
| 6 | table_mining | Tables found if corpus has tables | 0 when corpus has tables |
| 7 | enumeration_patterns | Enumerations found for type/subtype structures | < 20 in a rich domain |
| 8 | contrast_patterns | Non-zero if corpus compares concepts | 0 when corpus uses "unlike/whereas" |
| 9 | actor_detection | Actors are real actors, not section headers | > 30% junk actors |
| 10 | topic_modeling | Clusters map to real domain areas | Clusters are generic words |
| 11 | centrality | Top-ranked concepts are real domain concepts | Top 5 are structural junk |
| 12 | verb_interaction | Domain verbs dominate, not generic verbs | Top verbs are "make/get/take" |

The subagent should read a sample of actual signal entries (not just counts) and report:
- PASS/FAIL per signal with reason
- For each FAIL: what config change would fix it

### Step 3 — If any FAIL: go back to Phase 2

**Do not fix config from Phase 3.** For each FAIL, run **Phase 2 (configure_concept_extraction_parameters)** again. Adjust the relevant section in `extraction_config.json` based on the subagent's suggestions. Then run Phase 3 again.

### Step 4 — Stop condition

Stop when all 12 signals pass or when remaining failures are inherent to the corpus (e.g. no tables exist to mine).

## Run

```bash
python scripts/pipeline.py generate concept_extraction
```
