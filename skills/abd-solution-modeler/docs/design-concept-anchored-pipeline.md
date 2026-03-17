# Design: Concept-Anchored Pipeline

## Problem

The current pipeline fragments concept identity between extraction and modeling:

- Evidence extraction (Phase 3) produces six flat files with 7,000+ entries
- The evidence graph (Phase 4) derives edges as flat triples (`from → relation → to`)
- AI modeling phases (6–12) receive markdown and must reconstruct concept identity from scattered edges and prose

This causes:

- **Scattering**: a concept's actions, states, relationships, and evidence live in separate files with no cross-index
- **Re-parsing**: every AI phase re-reads markdown to understand what the previous phase produced
- **Drift**: domain model and interaction tree are separate markdown files that evolve independently and can diverge

## Design Principles

1. **Concepts are the anchor** — every artifact organizes around concepts, not around edge types
2. **Behaviors are first-class** — because they cross multiple concepts, they get their own registry linked back to concepts
3. **Interaction tree is first-class** — because stories cross concepts, the tree is a peer structure linked to concepts and behaviors
4. **One artifact from modeling onward** — domain model and interaction tree are sections of the same JSON, co-versioned
5. **Structured JSON is the source of truth** — markdown is a rendered view, not the working format between phases

## The Artifact: `solution_model.json`

From Phase 5 onward, every phase reads and writes a single structured file:

```json
{
  "concepts": [
    {
      "id": "Character",
      "module": "Core",
      "kind": "aggregate_root",
      "inherits": null,
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [
        {"type": "owns", "target": "AbilityScore", "cardinality": "1..*"}
      ],
      "behavior_refs": ["beh_001", "beh_003"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": ["act_0042", "rel_0012"]
    }
  ],
  "behaviors": [
    {
      "id": "beh_001",
      "name": "resolve attack",
      "owner": "Character",
      "collaborators": ["Attack", "Defense", "Effect"],
      "preconditions": [],
      "results": [],
      "linked_stories": ["story_resolve_attack"]
    }
  ],
  "interaction_tree": {
    "epics": [
      {
        "name": "Combat Resolution",
        "sub_epics": [
          {
            "name": "Attack Flow",
            "stories": [
              {
                "id": "story_resolve_attack",
                "name": "Resolve Attack",
                "linked_behaviors": ["beh_001"],
                "actors": ["Player", "Gamemaster"],
                "scenarios": []
              }
            ]
          }
        ]
      }
    ]
  },
  "evidence_refs": {
    "actions": [],
    "decisions": [],
    "states": [],
    "relationships": []
  }
}
```

**Why this shape:**

- **Concepts** anchor everything. Inspect one concept and see its properties, operations, relationships, linked behaviors, and linked stories.
- **Behaviors** are separate because they genuinely cross concepts. A behavior like "resolve attack" involves Character, Attack, Defense, Effect — storing it inside one concept distorts it.
- **Interaction tree** is separate because stories cross concepts. A story like "Resolve Attack" exercises multiple concepts and behaviors.
- **Everything links back.** Concepts point to behaviors and stories. Behaviors point to concepts and stories. Stories point to behaviors. No scattering without cross-references.

## Pipeline

| # | Phase | Actor | What it does | Output |
|---|-------|-------|--------------|--------|
| 1 | **Normalize** | Code | Chunk and clean raw source into uniform text segments. | `context_chunks.json` |
| 2 | **Hypothesize** | AI | Scan chunks to identify candidate concepts, modules, mechanisms, actors, and broad epic areas. | `hypothesis.json` + interaction tree skeleton (epics only) |
| 3 | **Extract** | Code | Mine chunks for actions, decisions, states, relationships guided by hypothesis. | `evidence/*.json` (six files) |
| 4 | **Index** | Code | Aggregate evidence into a concept-anchored index so each concept knows its actions, states, and relationships. | `evidence_index.json` |
| 5 | **Revise Hypothesis** | AI | Merge duplicates, discover missing concepts, refine modules and epics using indexed evidence. | `solution_model.json` v1 (concepts + epics/sub-epics + initial stories) |
| | **Checkpoint 1** | Human | Verify concept framing and interaction skeleton. | |
| 6 | **Structure** | AI | Assign properties, composition, inheritance, aggregate boundaries; assign actors and pre-conditions to stories. | `solution_model.json` v2 |
| 7 | **Behavior** | AI | Assign operations to concepts by decision ownership; link each operation to the story step that exercises it. | `solution_model.json` v3 |
| | **Checkpoint 2** | Human | Verify behavior ownership and story-to-operation links. | |
| 8 | **Variation** | AI | Add specialization, polymorphism, failure modes; add variation scenarios to stories. | `solution_model.json` v4 |
| 9 | **Consolidate** | AI | Detect anemia, over-centralization, orphans; fix anti-patterns; add examples to stories. | `solution_model.json` v5 |
| | **Checkpoint 3** | Human | Verify model quality and completeness. | |
| 10 | **Validate** | AI+Human | Walk key scenarios through the model — verify operations, state changes, and concept interactions match the interaction tree. | `assessment.json` |
| 11 | **Finalize** | AI | Apply assessment fixes; produce validated model with full traceability. | `solution_model.json` final |

## Key Changes from Current Pipeline

### Phase 4 (Index) is new

Today `evidence_graph.py` builds a flat edge list:

```json
{"from": "Effect", "relation": "performs", "to": "Checks", "action_id": "act_0003"}
```

The new Phase 4 flips this — it groups evidence *around concepts*:

```json
{
  "concepts": {
    "Effect": {
      "term_ids": ["term_0042"],
      "performs": ["act_0003", "act_0017"],
      "receives": ["act_0088"],
      "states": ["st_0012"],
      "relationships": ["rel_0005"]
    }
  },
  "registries": {
    "actions": [],
    "decisions": [],
    "states": [],
    "relationships": []
  }
}
```

Same data, different organization. Now the AI can ask "what does Effect do?" without scanning 7,000 edges.

### One artifact from Phase 5 onward

Today, domain model lives in `domain.md` and interaction tree lives in `interaction_tree.md`. They are separate files maintained by separate instructions. When Phase 7 assigns an operation to a concept, it must separately remember to update the interaction tree markdown.

With `solution_model.json`, when Phase 7 adds an operation to a concept, it simultaneously links that operation to a story step in the same file. They cannot diverge.

### Structured JSON throughout

Today, Phases 6–12 produce markdown only. Every subsequent phase re-parses prose to understand the model. With structured JSON, each phase reads the previous version, enriches specific sections, and writes the next version. Markdown is rendered from the JSON for human review, not used as the source of truth between phases.

### Fewer phases (11 vs 12)

The current split between `concept_model` and `structural_model` can merge into one "Structure" phase. With concept-anchored evidence from Phase 4, the AI doesn't need a separate pass to "discover" relationships — they're already indexed.

## Phase Sequence Rationale

The intellectual progression is unchanged and correct:

**Hypothesis → Extract → Structure → Behavior → Variation → Validate**

This sequence works because each phase depends on what the previous one established:

- **Structure** before **Behavior**: you need to know what exists and how things compose before you can assign who owns which operation
- **Behavior** before **Variation**: you need baseline operations before you can specialize them
- **Variation** before **Validate**: you need the full model including edge cases before walkthrough validation is meaningful

The change is not the sequence. The change is **what flows between the phases** — concept-anchored structured JSON instead of flat edge lists and markdown.

## Co-Evolution Mechanism

Every AI phase (5–9, 11) receives the full `solution_model.json` and must update both the domain sections (concepts, behaviors) and the interaction tree sections (stories, scenarios, steps) in the same pass.

Phase instructions enforce this:

- Phase 6 (Structure): "For each property or relationship you add to a concept, verify the concept appears in at least one story. If not, either add a story or flag the concept as structural-only."
- Phase 7 (Behavior): "For each operation you assign to a concept, link it to the story step that exercises it. If no step exists, create one."
- Phase 8 (Variation): "For each specialization you add, create a variation scenario in the linked story."

This makes co-evolution a structural constraint, not a hope.
