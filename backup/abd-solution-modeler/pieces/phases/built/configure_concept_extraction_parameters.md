# Phase 2 — Configure Concept Extraction Parameters

**Actor:** AI

## Purpose

Calibrate extraction parameters for twelve evidence-signal techniques. Outputs `extraction_config.json`. Phase 3 runs extraction with this config and loops back here if signals fail.

**Principle:** AI calibrates, code extracts (Phase 3), AI evaluates, repeat. Same config yields same extraction. When extraction is wrong, re-calibrate config — not prompts.

## Trigger

configure extraction, calibrate extraction, extraction parameters, concept extraction config

## Inputs

- `context/context_chunks.json` — normalized chunks from Phase 1

## Sampling Strategy

Read **15% of chunks, doubled** (i.e., 30% of the corpus), spread evenly across the corpus. Take chunks from the beginning, middle, and end of the file. If the corpus has 200 chunks, read 60. If it has 500, read 150.

**Why 30%:** This is instrument calibration — you need enough to see the document's structural patterns, definition syntax, and verb usage across all sections. 15% risks missing patterns that only appear in specific chapters. Doubling to 30% catches section-specific language.

**How to sample:** Divide `context_chunks.json` into thirds (beginning, middle, end). Read 10% of chunks from each third. This ensures coverage of introductory definitions, core rules, and specialized sections.

## Three Focused Scans

This phase runs as **three separate AI prompts**, each focused on a group of related signals. Each scan reads the same chunk sample but looks for different things.

---

### Scan A — Structure Calibration

**Signals:** 1 (TF weights), 2 (definition patterns), 6 (table mining), 7 (enumeration patterns)

**What the AI looks at:** How is this document formatted? What structural cues carry concept signal?

**For each signal, observe and propose:** See [concept_extraction.md](concept_extraction.md) Scan A section for full signal details and default JSON.

**Scan A output:** `tf_weights`, `definition_patterns`, `table_mining`, `enumeration_patterns` fields.

---

### Scan B — Behavior Calibration

**Signals:** 3 (dependency verbs), 4 (noun phrase mining), 8 (contrast patterns), 9 (actor detection), 12 (verb interaction)

**What the AI looks at:** What happens in this domain and who does it? What verbs and noun structures carry behavioral signal?

**For each signal, observe and propose:** See [concept_extraction.md](concept_extraction.md) Scan B section for full signal details and default JSON.

**Scan B output:** `dependency_verbs`, `np_mining`, `contrast_patterns`, `actor_detection`, `verb_interaction` fields.

---

### Scan C — Tuning Review

**Signals:** 5 (co-occurrence), 10 (topic modeling), 11 (centrality) + noise filters

**What the AI looks at:** Corpus-level characteristics — size, density, structure. These signals are code-computed; the AI just picks reasonable parameters.

**For each signal, observe and propose:** See [concept_extraction.md](concept_extraction.md) Scan C section for full signal details and default JSON.

**Scan C output:** `cooccurrence`, `topic_modeling`, `centrality`, `noise_filters` fields.

---

## Outputs

- `generated/extraction_config.json` — calibrated parameters for all 12 signals

## extraction_config.json shape

After all three scans, merge results into `generated/extraction_config.json`:

```json
{
  "tf_weights": {},
  "definition_patterns": [],
  "dependency_verbs": [],
  "np_mining": {},
  "cooccurrence": {},
  "table_mining": {},
  "enumeration_patterns": [],
  "contrast_patterns": [],
  "actor_detection": {},
  "topic_modeling": {},
  "centrality": {},
  "verb_interaction": {},
  "noise_filters": []
}
```

## Next step

After writing extraction_config.json, run **Phase 3 (concept_extraction)**. Phase 3 runs extraction, evaluates, and loops back to this phase if signals fail.

## Run

```bash
python scripts/pipeline.py generate configure_concept_extraction_parameters
```
