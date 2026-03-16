# Phase 4 — Evidence Graph

**Actor:** Code | 
## Purpose

Build rule dependency structure.

## Trigger

build evidence graph, evidence graph, rule dependency

## Inputs

`evidence/` — extraction outputs (terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json)

## Instructions

Create graph relations:

```
Concept → performs → Action
Action → produces → State
Concept → modifies → Concept
```

## Outputs

`evidence/evidence_graph.json`

## Run

```bash
python scripts/pipeline.py run evidence_graph
```

Script: `scripts/evidence_graph.py`

## Checkpoint 2

Human validates rule coverage before proceeding.
