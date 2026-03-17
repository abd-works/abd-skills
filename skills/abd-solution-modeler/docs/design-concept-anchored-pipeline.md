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
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": ["act_0042", "rel_0012"]
    },
    {
      "id": "Attack",
      "module": "Core",
      "kind": "entity",
      "inherits": null,
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": []
    },
    {
      "id": "AreaEffectAttack",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack",
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_area_effect_attack"],
      "evidence_refs": []
    },
    {
      "id": "PerceptionAttack",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack",
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_perception_attack"],
      "evidence_refs": []
    },
    {
      "id": "Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": null,
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": []
    },
    {
      "id": "Attack Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Effect",
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": []
    },
    {
      "id": "Damage Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack Effect",
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_apply_damage_effect"],
      "evidence_refs": []
    },
    {
      "id": "Weakening Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack Effect",
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_apply_weakening_effect"],
      "evidence_refs": []
    },
    {
      "id": "Afflicting Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack Effect",
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_apply_afflicting_effect"],
      "evidence_refs": []
    }
  ],
  "behaviors": [
    {
      "id": "beh_activate",
      "name": "activate",
      "owner": "Character",
      "collaborators": ["Attack"],
      "preconditions": [],
      "results": [],
      "linked_steps": ["step_activate_attack"]
    },
    {
      "id": "beh_resolve_hit",
      "name": "resolve hit",
      "owner": "Character",
      "collaborators": ["Attack", "Effect"],
      "preconditions": [],
      "results": [],
      "linked_steps": ["step_attack_hits"]
    },
    {
      "id": "beh_resolve_miss",
      "name": "resolve miss",
      "owner": "Character",
      "collaborators": ["Attack"],
      "preconditions": [],
      "results": [],
      "linked_steps": ["step_attack_misses"]
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
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {
                    "id": "step_activate_attack",
                    "name": "User activates attack",
                    "linked_behaviors": ["beh_activate"],
                    "trigger": "Player",
                    "response": "Character",
                    "when_then": "When user selects attack from character sheet, Character activates that attack"
                  },
                  {
                    "id": "step_attack_hits",
                    "name": "Attack hits",
                    "linked_behaviors": ["beh_resolve_hit"],
                    "trigger": "Character",
                    "response": "Effect",
                    "when_then": "When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)"
                  },
                  {
                    "id": "step_attack_misses",
                    "name": "Attack misses",
                    "linked_behaviors": ["beh_resolve_miss"],
                    "trigger": "Character",
                    "response": "Character",
                    "when_then": "When attack resolves as miss, no effect applied"
                  }
                ],
                "scenarios": [
                  {"id": "scenario_attack_hits", "name": "Attack hits", "step_refs": ["step_activate_attack", "step_attack_hits"]},
                  {"id": "scenario_attack_misses", "name": "Attack misses", "step_refs": ["step_activate_attack", "step_attack_misses"]}
                ]
              },
              {
                "id": "story_resolve_area_effect_attack",
                "name": "Resolve Area Effect Attack",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_activate_area_attack", "name": "User activates area attack", "linked_behaviors": ["beh_activate"], "trigger": "Player", "response": "Character", "when_then": "When user selects area attack, Character activates it"},
                  {"id": "step_area_hits", "name": "Area attack hits targets in area", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Effect", "when_then": "When area resolves, Effect applies to each target in area (Damage Effect, Weakening Effect, or Afflicting Effect depending on power); dodge for half"}
                ]
              },
              {
                "id": "story_resolve_perception_attack",
                "name": "Resolve Perception Attack",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_activate_perception_attack", "name": "User activates perception attack", "linked_behaviors": ["beh_activate"], "trigger": "Player", "response": "Character", "when_then": "When user selects perception attack, Character activates it"},
                  {"id": "step_perception_hits", "name": "Perception attack hits target in range", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Effect", "when_then": "When target in perception range, Effect applies (e.g. Damage Effect, Weakening Effect, Afflicting Effect); no attack check"}
                ]
              },
              {
                "id": "story_apply_damage_effect",
                "name": "Apply Damage Effect",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_damage_applies", "name": "Damage Effect applies to target", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Damage Effect", "when_then": "When attack hits, Damage Effect applies; resistance check — each degree of failure adds damage (injuries, bruises)"}
                ]
              },
              {
                "id": "story_apply_weakening_effect",
                "name": "Apply Weakening Effect",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_weakening_applies", "name": "Weakening Effect applies to target", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Weakening Effect", "when_then": "When attack hits, Weakening Effect reduces target resistance (Toughness)"}
                ]
              },
              {
                "id": "story_apply_afflicting_effect",
                "name": "Apply Afflicting Effect",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_afflicting_applies", "name": "Afflicting Effect applies to target", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Afflicting Effect", "when_then": "When attack hits, Afflicting Effect imposes condition; resistance check to avoid"}
                ]
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
- **Behaviors** are separate because they genuinely cross concepts. A behavior like "activate" involves Character and Attack — storing it inside one concept distorts it.
- **Interaction tree** is separate because stories cross concepts. A story goes directly to steps (ordered list). Each step exercises at least one behavior.
- **Scenarios are groupings, not hierarchy.** Scenarios sit alongside steps and have `step_refs` — they group steps for organization (e.g. "Attack hits" vs "Attack misses"). When there are many steps, scenarios slice them. Steps are the primary content; scenarios are optional views.
- **Step ↔ behavior is the tight link.** Each step has `linked_behaviors` (at least one). Each behavior has `linked_steps`. The distinction is not UI vs domain — it is whether the user interaction creates a reaction. Selecting an attack from a character sheet to activate it is trigger context for the `activate` behavior; the selection itself does not create a reaction. By contrast, a user opening a power to see details, or selecting a payment type that causes the system to display different payment details — those create reactions and are behaviors. If the interaction triggers a state change or system response, it is a behavior.
- **Everything links back.** Concepts point to behaviors and stories. Behaviors point to concepts and steps. Steps point to behaviors. No scattering without cross-references.

### Story vs. Scenario: When Subtypes Become Separate Stories

The more types you have for a concept, the less it makes sense to bundle them into one story. **Subtype with different resolution mechanics → different story.** This is the safer default.

**Rule:** When a subtype changes the flow (different mechanics, different steps, different collaborators), give it its own story. Use scenarios only for small variations within the same flow (e.g. hit vs miss).

**Heuristic:**


| Variation type                       | Same story?                           | Example                                                                                                                           |
| ------------------------------------ | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Type field** (melee vs ranged)     | Yes — parameterized examples in steps | Punch (melee), Bow shot (ranged)                                                                                                  |
| **Subtype with different mechanics** | No — separate story                   | AreaEffectAttack → "Resolve Area Effect Attack"; PerceptionAttack → "Resolve Perception Attack"                                   |
| **Effect subtype**                   | No — separate story                   | Damage Effect → "Apply Damage Effect"; Weakening Effect → "Apply Weakening Effect"; Afflicting Effect → "Apply Afflicting Effect" |


**When to resolve:** Subtype *concepts* must exist from Phase 2 (hypothesis) and Phase 6 (structure assigns `inherits`). During interaction-tree construction (Phases 5–6, 8), the tree decides whether a subtype is a scenario (same story) or a separate story. Phase 8 splits stories for subtypes that already exist — it does not discover new subtypes.

**How to encode:**

- **Story naming:** Base story "Resolve Attack"; subtype stories "Resolve Area Effect Attack", "Resolve Perception Attack", "Apply Damage Effect", "Apply Weakening Effect", "Apply Afflicting Effect".
- **Story grouping:** Group under a sub-epic (e.g. "Attack Resolution") so the hierarchy is visible.
- **Step reuse:** Shared steps (e.g. "User activates attack") can be referenced by multiple stories; subtype-specific steps live in the subtype story.
- **Concept → story_refs:** Each subtype concept links to its own story, not the base story.

## Pipeline


| #   | Phase                 | Actor    | What it does                                                                                                                                                                       | Output                                                                  |
| --- | --------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 1   | **Normalize**         | Code     | Chunk and clean raw source into uniform text segments.                                                                                                                             | `context_chunks.json`                                                   |
| 2   | **Hypothesize**       | AI       | Scan chunks to identify candidate concepts, modules, mechanisms, actors, and broad epic areas.                                                                                     | `hypothesis.json` + interaction tree skeleton (epics only)              |
| 3   | **Extract**           | Code     | Mine chunks for actions, decisions, states, relationships guided by hypothesis.                                                                                                    | `evidence/*.json` (six files)                                           |
| 4   | **Index**             | Code     | Aggregate evidence into a concept-anchored index so each concept knows its actions, states, and relationships.                                                                     | `evidence_index.json`                                                   |
| 5   | **Revise Hypothesis** | AI       | Merge duplicates, discover missing concepts, refine modules and epics using indexed evidence.                                                                                      | `solution_model.json` v1 (concepts + epics/sub-epics + initial stories) |
|     | **Checkpoint 1**      | Human    | Verify concept framing and interaction skeleton.                                                                                                                                   |                                                                         |
| 6   | **Structure**         | AI       | Assign properties, composition, inheritance, aggregate boundaries; add steps to stories from evidence; assign actors and pre-conditions. Concepts and interaction tree gain structure in parallel. | `solution_model.json` v2                                                |
| 7   | **Behavior**          | AI       | Assign operations to concepts by decision ownership; link each behavior to the step(s) that exercise it; group steps into scenarios (e.g. hit vs miss). Each step has at least one linked behavior. | `solution_model.json` v3                                                |
|     | **Checkpoint 2**      | Human    | Verify behavior ownership and step-to-behavior links.                                                                                                                              |                                                                         |
| 8   | **Variation**         | AI       | Split stories by subtype when mechanics differ (per *Story vs. Scenario* rule); add failure modes. Subtype concepts already exist from Phase 2/6 — Phase 8 does not discover them. | `solution_model.json` v4                                                |
| 9   | **Consolidate**       | AI       | Detect anemia, over-centralization, orphans; fix anti-patterns; add examples to stories.                                                                                           | `solution_model.json` v5                                                |
|     | **Checkpoint 3**      | Human    | Verify model quality and completeness.                                                                                                                                             |                                                                         |
| 10  | **Assess**           | AI+Human | Produce model assessment: consistency, coverage, completeness, **type field vs subtype** (mechanical difference test). No late "walkthrough" — verification happens incrementally in Phases 6–7. | `assessment.json`                                                       |
| 11  | **Finalize**          | AI       | Apply assessment fixes; produce validated model with full traceability.                                                                                                            | `solution_model.json` final                                             |


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
    "actions": {},
    "decisions": {},
    "states": {},
    "relationships": {}
  }
}
```

Same data, different organization. Registries hold the actual evidence sentences (from extraction `raw`), keyed by ID. Full example with populated registries: see **Appendix — Phase 4**.

**Origin of the evidence buckets.** Phase 3 (Extract) produces six flat files from `evidence_extraction_guided.py`. These buckets are grounded in established NLP and knowledge-extraction research:


| Phase 3 output       | What it extracts                                                                                                                                       | Research grounding                                                                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `actions.json`       | Subject–predicate–object triples (e.g. "Effect applies damage", "Effect applies weakening", "Effect applies afflicting", "Character activates Attack") | **Event extraction** (ACE 2005: trigger + arguments); **SVO triple extraction** (textacy, dependency parsing); **Semantic role labeling** (PropBank, FrameNet: agent/theme/patient → performs/receives) |
| `decisions.json`     | Conditionals (if/when/unless + condition)                                                                                                              | **Conditional extraction** (LexNLP `lexnlp.extract.en.conditions`: if, when, unless, until, provided that, etc.); rule-based pattern matching for legal/contract text                                   |
| `states.json`        | Entity + state description (state, becomes, transitions to, gains, loses)                                                                              | **Entity state tracking** (ProPara, OpenPI: entity attributes and state changes in procedural text); **VerbNet semantic parsing** for state extraction                                                  |
| `relationships.json` | From-entity, type, to-entity (has, contains, uses, belongs to)                                                                                         | **Relation extraction** (ACE2005: PHYS, ORG-AFF, PER-SOC; OpenIE; DocRED); binary entity–relation–entity triples                                                                                        |
| `terms.json`         | Domain term candidates                                                                                                                                 | **Terminology extraction** (Wikipedia: subtask of IE; noun phrase chunking, termhood/unithood; C-value/NC-value; supports ontology learning)                                                            |


**Removed: `modifiers.json`.** The modifiers bucket (variation descriptions, variation axes) has been deprecated. It was domain-specific, poorly standardized, and never performed well. Future work: research better approaches — see *Subtype vs type-field discrimination* below.

**Subtype vs type-field discrimination.** A major weakness: the system conflates **real subtypes** (inheritance — extra data and behavior) with **type fields** (e.g. red vs blue — same flow, different value). Research is documented in [subtype-vs-type-field-research.md](./subtype-vs-type-field-research.md). Summary:

- **Feature modeling:** Mechanical difference test — does switching variant change which *rules* apply? Yes → subtype; no → type field.
- **Ontology learning:** Taxonomic ("is-a", "such as") vs attribute ("has", "of type") patterns. Inheritance = vertical; attributes = horizontal.
- **DDD heuristics:** Behavior differences → subtype. Same flow, different value → type field.
- **Proposed strategy:** Pattern-based pre-filter + mechanical difference test + behavioral evidence (do variants have different actions/decisions?). See research doc for heuristics table and extraction strategy.

**Alignment with CRC / OO design.** CRC cards (Beck & Cunningham, OOPSLA'89) use **Class**, **Responsibility** (verb phrases), and **Collaborator**. Our buckets map: actions → responsibilities; relationships → collaborators; states → entity attributes. Terminology extraction feeds concept naming. Decisions feed when/how behaviors apply. See References below.

**Human-readable rendered view.** The index is optimized for AI lookup (IDs only). For human review at Checkpoint 2, render an expanded view that inlines the relevant details for each ID. Example:

```markdown
## Effect

**performs**
- act_0003 — applies damage to target
- act_0017 — modifies target's resistance

**receives**
- act_0088 — receives trigger from Character when attack resolves

**states**
- st_0012 — applied (effect has been applied to target)

**relationships**
- rel_0005 — belongs to Character (effect is owned by the attacking character)
```

Same concept-anchored structure, but each ID is expanded with its human-readable description from the registries. Supports human verification of rule coverage without cross-referencing raw JSON.

### One artifact from Phase 5 onward

Today, domain model lives in `domain.md` and interaction tree lives in `interaction_tree.md`. They are separate files maintained by separate instructions. When Phase 7 assigns an operation to a concept, it must separately remember to update the interaction tree markdown.

With `solution_model.json`, when Phase 7 adds a behavior, it simultaneously links that behavior to the step(s) that exercise it in the same file. Step and behavior cannot diverge.

### Structured JSON throughout

Today, Phases 6–12 produce markdown only. Every subsequent phase re-parses prose to understand the model. With structured JSON, each phase reads the previous version, enriches specific sections, and writes the next version. Markdown is rendered from the JSON for human review, not used as the source of truth between phases.

### Fewer phases (11 vs 12)

The current split between `concept_model` and `structural_model` can merge into one "Structure" phase. With concept-anchored evidence from Phase 4, the AI doesn't need a separate pass to "discover" relationships — they're already indexed.

## Phase Sequence Rationale

The intellectual progression is unchanged and correct:

**Hypothesis → Extract → Structure → Behavior → Variation → Assess**

This sequence works because each phase depends on what the previous one established:

- **Structure** before **Behavior**: you need to know what exists and how things compose before you can assign who owns which operation
- **Behavior** before **Variation**: you need baseline operations before you can split stories by subtype and add failure modes
- **Variation** before **Assess**: you need the full model including subtype stories and edge cases before assessment is meaningful

The change is not the sequence. The change is **what flows between the phases** — concept-anchored structured JSON instead of flat edge lists and markdown.

## Co-Evolution Mechanism

Every AI phase (5–9, 11) receives the full `solution_model.json` and must update both the domain sections (concepts, behaviors) and the interaction tree sections (stories, scenarios, steps) in the same pass.

Phase instructions enforce this:

- Phase 6 (Structure): "For each property or relationship you add to a concept, verify the concept appears in at least one story. If not, either add a story or flag the concept as structural-only. For each story, add steps from evidence — steps are the primary flow; scenarios come in Phase 7."
- Phase 7 (Behavior): "For each behavior you create, link it to the step(s) that exercise it. Each step must have at least one linked behavior. If no step exists, create one. After linking, verify: owner concept has that operation; collaborators appear in the step flow. Group steps into scenarios (e.g. hit vs miss) — scenarios are optional but add clarity when steps form natural paths."
- Phase 8 (Variation): "For each subtype with different mechanics, ensure a separate story exists. Add failure-mode scenarios where appropriate."

**Verification is incremental, not deferred.** Phase 6 verifies concept↔story; Phase 7 verifies step↔behavior↔concept. Phase 10 (Assess) produces a cross-cutting report — it does not redo scenario walkthroughs that were already enforced during build.

### Parallel Detail Progression

Concepts and the interaction tree evolve in lockstep. Each phase adds comparable detail to both:

| Phase | Concepts gain | Interaction tree gains |
|-------|---------------|------------------------|
| 5     | story_refs, evidence_refs | stories (epics, sub-epics), empty steps |
| 6     | properties, relationships, inheritance, kind | steps (with actors, pre-conditions), empty linked_behaviors |
| 7     | operations, behavior_refs | linked_behaviors, when_then, scenarios (step groupings) |
| 8     | (unchanged — subtypes already exist) | subtype stories, failure-mode scenarios |
| 9     | examples | examples on steps |

Scenarios appear in Phase 7 (basic groupings like hit vs miss) and Phase 8 (failure modes, subtype-specific). No phase defers "scenario work" to a later phase — steps and scenarios are built as behaviors are assigned.

---

## Appendix: Phase-by-Phase Evolution

For each phase, this section shows the output — both the AI version (JSON) and the human version (rendered markdown). Phase 2 produces `hypothesis.json` and `concept_guidance.json`; Phase 3 produces `evidence/*.json`; Phase 4 produces `evidence_index.json`; Phases 5–9 and 11 produce `solution_model.json`; Phase 10 (Assess) produces `assessment.json`.

---

### Phase 2 — Hypothesize

Phase 2 produces the initial domain hypothesis — candidate concepts, modules, mechanisms, actors, and epics. Outputs: `hypothesis.json` and `concept_guidance.json` (or merged). The interaction tree skeleton has epics only; no stories yet.

**Nested hierarchy.** Many domains need inheritance beyond one level. Effect is a prime example: base Effect → Attack Effect (parent of damage, weakening, afflicting, healing) and Sensory Effect (sibling branch). Attack Effect → Damage Effect, Weakening Effect, Afflicting Effect, Healing Effect. A flat list collapses this. The concept value is directly the next level: `{ "ChildName": { ... } }` — no `subtypes` wrapper. Keys are subtype names; values are `{}` (leaf) or nested objects (branch). Reserved key `related` holds non-hierarchy links.

**Type field vs subtype.** Not every variation is a subtype. Melee vs ranged attack — same resolution flow (attack check), different parameters (range, reach vs ammunition) — are **type fields**; they appear as parameterized examples in steps, not in the concept hierarchy. **True subtypes** have different mechanics: e.g. AreaEffectAttack uses area targeting and dodge-for-half, implying a different concept (AreaEffectCheck), different behavior, possibly a different story. The hierarchy holds only real subtypes.

**Subtype discovery must happen upstream.** If extraction (Phase 3) and hypothesis (Phase 2) do not surface subtypes (AreaEffectAttack, PerceptionAttack, Damage Effect, etc.) as distinct concepts or evidence clusters, you never recover them. The evidence is biased toward whatever buckets extraction produced. Phase 8 does not discover subtypes — it works with concepts that already exist. Phase 2 must include subtype candidates in `priority_concepts` and `concept_hierarchy`; Phase 3 extraction must be guided to find evidence for them. Phase 6 assigns `inherits` when structuring. No `variations` field on concepts — the hierarchy is the source of truth; derive subtypes by querying `concepts.where(inherits === parentId)`.

**Concept guidance (AI / JSON)**

```json
{
  "priority_concepts": ["Character", "Ability", "Power", "Effect", "Attack Effect", "Damage Effect", "Weakening Effect", "Afflicting Effect", "Healing Effect", "Sensory Effect", "Defense", "Attack", "AreaEffectAttack", "PerceptionAttack", "Check", "Resistance Check", "Player", "Gamemaster"],
  "concept_aliases": {
    "Character": ["character", "hero", "character sheet"],
    "Effect": ["effect", "power effect", "effect type"],
    "Attack Effect": ["attack effect", "attack-type effect"],
    "Damage Effect": ["damage", "damage effect", "damage rank"],
    "Weakening Effect": ["weaken", "weaken effect", "weakened"],
    "Afflicting Effect": ["affliction", "affliction effect", "condition"],
    "Healing Effect": ["healing", "healing effect", "heal"],
    "Sensory Effect": ["sensory effect", "senses", "concealment", "invisibility"],
    "Attack": ["attack", "attack check", "attack roll"],
    "AreaEffectAttack": ["area effect attack", "area attack", "burst", "blast"],
    "PerceptionAttack": ["perception attack", "perception range attack"]
  },
  "concept_hierarchy": {
    "Power": {
      "Device": {},
      "Power Array": {},
      "related": ["Effect", "Modifier", "Power Point"]
    },
    "Attack": {
      "AreaEffectAttack": {},
      "PerceptionAttack": {},
      "related": ["Effect", "Check"]
    },
    "Effect": {
      "Attack Effects": {
        "Damage Effect": {},
        "Affliction Effect": {},
        "Weaken Effect": {},
        "Healing Effect": {}
      },
      "Sensory Effects": {
        "Senses": {},
        "Concealment": {},
        "Invisibility": {}
      },
      "Adjustment Effects": {
        "Weaken Effect": {},
        "Enhance Effect": {}
      },
      "related": ["Modifier", "Resistance Check", "Condition"]
    },
    "Defense": {
      "Dodge": {},
      "Parry": {},
      "Fortitude": {},
      "Will": {},
      "Toughness": {},
      "related": ["Resistance Check", "Ability"]
    }
  },
  "priority_mechanisms": ["Check Resolution", "Resistance", "Power Cost", "Action Economy"],
  "priority_actors": ["Player", "Gamemaster"],
  "noise_filters": ["table of contents", "appendix", "index", "license"],
  "focus_sections": ["CHAPTER 6: POWERS", "CHAPTER 1: THE BASICS", "CHAPTER 4: SKILLS"]
}
```

**Hierarchy depth.** The same pattern applies elsewhere: e.g. Account → Joint Account, Family Account → more specific account types with individualized behavior. Any `{}` can be expanded to `{ "Child": {}, ... }` for another level.

**Interaction tree skeleton (epics only)** — rendered markdown or JSON; stories added in Phase 5.

---

### Phase 4 — Index

Phase 4 produces `evidence_index.json` — evidence grouped by concept. No concepts or interaction tree yet; this is the indexed evidence that feeds Phase 5. The index is keyed by concepts from the hierarchy (Phase 2); subtypes (AreaEffectAttack, PerceptionAttack; Attack Effect, Damage Effect, Weakening Effect, Afflicting Effect, Healing Effect, Sensory Effect) get their own entries when rule text distinguishes them.

**Evidence index (AI / JSON)**

```json
{
  "concepts": {
    "Character": {
      "term_ids": ["term_0001"],
      "performs": ["act_0042", "act_0043"],
      "receives": ["act_0088"],
      "states": ["st_0001"],
      "relationships": ["rel_0012", "rel_0013"]
    },
    "Attack": {
      "term_ids": ["term_0022"],
      "performs": [],
      "receives": ["act_0042"],
      "states": ["st_0022"],
      "relationships": ["rel_0013"]
    },
    "AreaEffectAttack": {
      "term_ids": ["term_0023"],
      "performs": [],
      "receives": ["act_0044"],
      "states": [],
      "relationships": []
    },
    "PerceptionAttack": {
      "term_ids": ["term_0024"],
      "performs": [],
      "receives": [],
      "states": [],
      "relationships": []
    },
    "Effect": {
      "term_ids": ["term_0042"],
      "performs": [],
      "receives": ["act_0088"],
      "states": ["st_0012"],
      "relationships": ["rel_0005"]
    },
    "Attack Effect": {
      "term_ids": ["term_0043"],
      "performs": [],
      "receives": [],
      "states": [],
      "relationships": []
    },
    "Damage Effect": {
      "term_ids": ["term_0044"],
      "performs": ["act_0003"],
      "receives": [],
      "states": [],
      "relationships": []
    },
    "Weakening Effect": {
      "term_ids": ["term_0045"],
      "performs": ["act_0017"],
      "receives": [],
      "states": [],
      "relationships": []
    },
    "Afflicting Effect": {
      "term_ids": ["term_0046"],
      "performs": [],
      "receives": [],
      "states": [],
      "relationships": []
    },
    "Healing Effect": {
      "term_ids": ["term_0047"],
      "performs": [],
      "receives": [],
      "states": [],
      "relationships": []
    },
    "Sensory Effect": {
      "term_ids": ["term_0048"],
      "performs": [],
      "receives": [],
      "states": [],
      "relationships": []
    }
  },
  "registries": {
    "actions": {
      "act_0042": {
        "subject": "Character",
        "predicate": "activates",
        "object": "Attack",
        "raw": "The character activates an attack from their character sheet when they choose to use a power or weapon."
      },
      "act_0043": {
        "subject": "Character",
        "predicate": "resolves",
        "object": "Attack",
        "raw": "The character resolves the attack outcome by rolling the check and comparing the result to the target's defense."
      },
      "act_0003": {
        "subject": "Effect",
        "predicate": "applies",
        "object": "damage",
        "raw": "The effect applies damage to the target when the attack hits and the effect is a damage type."
      },
      "act_0017": {
        "subject": "Effect",
        "predicate": "modifies",
        "object": "resistance",
        "raw": "The effect modifies the target's resistance, adding to or reducing their Toughness for the attack."
      },
      "act_0088": {
        "subject": "Character",
        "predicate": "triggers",
        "object": "Effect",
        "raw": "When the attack resolves, the character's effect receives the trigger and applies to the target."
      },
      "act_0044": {
        "subject": "Character",
        "predicate": "resolves",
        "object": "AreaEffectAttack",
        "raw": "For area effect attacks, targets in the area may attempt a dodge check for half damage."
      }
    },
    "decisions": {
      "dec_0001": {
        "trigger": "when",
        "condition": "the attack check exceeds the target's defense, the effect is applied",
        "raw": "When the attack check exceeds the target's defense, the effect is applied to the target."
      }
    },
    "states": {
      "st_0001": {
        "entity": "Character",
        "state_description": "The character has an active attack in progress.",
        "raw": "The character has an active attack in progress until it is resolved."
      },
      "st_0022": {
        "entity": "Attack",
        "state_description": "The attack has been resolved as a hit or miss.",
        "raw": "The attack has been resolved as a hit or miss based on the check result."
      },
      "st_0012": {
        "entity": "Effect",
        "state_description": "The effect has been applied to the target.",
        "raw": "The effect has been applied to the target and may modify their condition or resistance."
      }
    },
    "relationships": {
      "rel_0012": {
        "from_entity": "Character",
        "type": "owns"
        "to_entity": "AbilityScore",
        "raw": "The character owns ability scores that contribute modifiers to checks."
      },
      "rel_0013": {
        "from_entity": "Character",
        "type": "owns",
        "to_entity": "Attack",
        "raw": "The character owns the attack they activate from their powers or equipment."
      },
      "rel_0005": {
        "from_entity": "Effect",
        "type": "belongs to",
        "to_entity": "Character",
        "raw": "The effect belongs to the attacking character and is applied when their attack resolves."
      }
    }
  }
}
```

**Evidence index (Markdown)**

```markdown
## Character

**performs**
- act_0042 — activates attack from character sheet
- act_0043 — resolves attack outcome (hit or miss)

**receives**
- act_0088 — receives trigger when attack resolves

**states**
- st_0001 — has active attack

**relationships**
- rel_0012 — owns AbilityScore
- rel_0013 — owns Attack

---

## Attack

**receives**
- act_0042 — receives activate from Character

**states**
- st_0022 — resolved (hit or miss)

**relationships**
- rel_0013 — belongs to Character

---

## Effect

**receives**
- act_0088 — receives trigger from Character when attack resolves

**states**
- st_0012 — applied (effect has been applied to target)

**relationships**
- rel_0005 — belongs to Character (effect is owned by the attacking character)

---

## Attack Effect

*(parent of damage, weakening, afflicting, healing; inherits from Effect)*

---

## Damage Effect

**performs**
- act_0003 — applies damage to target

---

## Weakening Effect

**performs**
- act_0017 — modifies target's resistance (reduces Toughness)

---

## Afflicting Effect

*(no evidence in example; rule text would index condition-imposing effects here)*

---

## Healing Effect

*(no evidence in example; rule text would index healing effects here)*

---

## Sensory Effect

*(inherits from Effect; sibling to Attack Effect; senses, concealment, invisibility)*
```

---

### Phase 5 — Revise Hypothesis

Phase 5 produces the first version of `solution_model.json` — concepts discovered from the evidence index, plus stories added to the interaction tree. Properties, operations, behaviors, and steps are empty at this phase; they are filled in by Phases 6–9. The artifact structure is complete; the content is intentionally minimal.

**solution_model.json v1 (AI / JSON)**

```json
{
  "concepts": [
  {
    "id": "Character",
    "module": "Core",
    "kind": null,
    "inherits": null,
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": ["act_0042", "rel_0012"]
  },
  {
    "id": "Attack",
    "module": "Core",
    "kind": null,
    "inherits": null,
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "AreaEffectAttack",
    "module": "Core",
    "kind": null,
    "inherits": "Attack",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_area_effect_attack"],
    "evidence_refs": ["act_0044"]
  },
  {
    "id": "PerceptionAttack",
    "module": "Core",
    "kind": null,
    "inherits": "Attack",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_perception_attack"],
    "evidence_refs": []
  },
  {
    "id": "Effect",
    "module": "Core",
    "kind": null,
    "inherits": null,
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": ["act_0088", "st_0012", "rel_0005"]
  },
  {
    "id": "Attack Effect",
    "module": "Core",
    "kind": null,
    "inherits": "Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Damage Effect",
    "module": "Core",
    "kind": null,
    "inherits": "Attack Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_apply_damage_effect"],
    "evidence_refs": ["act_0003"]
  },
  {
    "id": "Weakening Effect",
    "module": "Core",
    "kind": null,
    "inherits": "Attack Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_apply_weakening_effect"],
    "evidence_refs": ["act_0017"]
  },
  {
    "id": "Afflicting Effect",
    "module": "Core",
    "kind": null,
    "inherits": "Attack Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_apply_afflicting_effect"],
    "evidence_refs": []
  },
  {
    "id": "Healing Effect",
    "module": "Core",
    "kind": null,
    "inherits": "Attack Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Sensory Effect",
    "module": "Core",
    "kind": null,
    "inherits": "Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  }
  ],
  "behaviors": [],
  "interaction_tree": {
    "epics": [
      {
        "name": "Combat Resolution",
        "sub_epics": [
          {
            "name": "Attack Flow",
            "stories": [
              {"id": "story_resolve_attack", "name": "Resolve Attack", "actors": [], "steps": [], "scenarios": []},
              {"id": "story_resolve_area_effect_attack", "name": "Resolve Area Effect Attack", "actors": [], "steps": [], "scenarios": []},
              {"id": "story_resolve_perception_attack", "name": "Resolve Perception Attack", "actors": [], "steps": [], "scenarios": []},
              {"id": "story_apply_damage_effect", "name": "Apply Damage Effect", "actors": [], "steps": [], "scenarios": []},
              {"id": "story_apply_weakening_effect", "name": "Apply Weakening Effect", "actors": [], "steps": [], "scenarios": []},
              {"id": "story_apply_afflicting_effect", "name": "Apply Afflicting Effect", "actors": [], "steps": [], "scenarios": []}
            ]
          }
        ]
      }
    ]
  }
}
```

**solution_model v1 (Markdown)**

```markdown
## Module: Core

### Character
Candidate concept from hypothesis. Participates in story_resolve_attack.
Evidence: act_0042, rel_0012.

### Attack
Candidate concept from hypothesis. Participates in story_resolve_attack.

### AreaEffectAttack : inherits Attack
Candidate concept from hypothesis. Participates in story_resolve_area_effect_attack. Evidence: act_0044.

### PerceptionAttack : inherits Attack
Candidate concept from hypothesis. Participates in story_resolve_perception_attack.

### Effect
Candidate concept from hypothesis. Participates in story_resolve_attack. Evidence: act_0088, st_0012, rel_0005.

### Attack Effect : inherits Effect
Candidate concept from hypothesis. Participates in story_resolve_attack.

### Damage Effect : inherits Attack Effect
Candidate concept from hypothesis. Participates in story_apply_damage_effect. Evidence: act_0003.

### Weakening Effect : inherits Attack Effect
Candidate concept from hypothesis. Participates in story_apply_weakening_effect. Evidence: act_0017.

### Afflicting Effect : inherits Attack Effect
Candidate concept from hypothesis. Participates in story_apply_afflicting_effect.

### Healing Effect : inherits Attack Effect
Candidate concept from hypothesis. Participates in story_resolve_attack.

### Sensory Effect : inherits Effect
Candidate concept from hypothesis. Participates in story_resolve_attack.

---

# Epic: Combat Resolution

## Sub-Epic: Attack Flow

### Story: Resolve Attack
(No steps yet. Story identified from evidence.)

### Story: Resolve Area Effect Attack
(No steps yet. Subtype story for AreaEffectAttack.)

### Story: Resolve Perception Attack
(No steps yet. Subtype story for PerceptionAttack.)

### Story: Apply Damage Effect
(No steps yet. Subtype story for Damage Effect.)

### Story: Apply Weakening Effect
(No steps yet. Subtype story for Weakening Effect.)

### Story: Apply Afflicting Effect
(No steps yet. Subtype story for Afflicting Effect.)
```

---

### Phase 6 — Structure

Phase 6 adds structure to both concepts and the interaction tree in parallel: concepts get properties, relationships, inheritance, and kind; stories get steps (from evidence), actors, and pre-conditions. Steps have empty `linked_behaviors` until Phase 7.

**Concepts (AI / JSON)**

```json
"concepts": [
  {
    "id": "Character",
    "module": "Core",
    "kind": "aggregate_root",
    "inherits": null,
    "properties": [
      {"name": "name", "type": "String"},
      {"name": "ability_scores", "type": "List<AbilityScore>"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "owns", "target": "AbilityScore", "cardinality": "1..*"},
      {"type": "owns", "target": "Attack", "cardinality": "0..*"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": ["act_0042", "rel_0012"]
  },
  {
    "id": "Attack",
    "module": "Core",
    "kind": "entity",
    "inherits": null,
    "properties": [
      {"name": "targets", "type": "List<Character>"},
      {"name": "resolved", "type": "Boolean"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "AreaEffectAttack",
    "module": "Core",
    "kind": "entity",
    "inherits": "Attack",
    "properties": [
      {"name": "area", "type": "Area"},
      {"name": "dodge_for_half", "type": "Boolean"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": ["act_0044"]
  },
  {
    "id": "PerceptionAttack",
    "module": "Core",
    "kind": "entity",
    "inherits": "Attack",
    "properties": [
      {"name": "perception_range", "type": "Boolean"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": null,
    "properties": [
      {"name": "applied", "type": "Boolean"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Attack Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": "Effect",
    "properties": [],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Damage Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": "Attack Effect",
    "properties": [
      {"name": "damage_rank", "type": "Integer"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": ["act_0003"]
  },
  {
    "id": "Weakening Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": "Attack Effect",
    "properties": [
      {"name": "weaken_rank", "type": "Integer"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": ["act_0017"]
  },
  {
    "id": "Afflicting Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": "Attack Effect",
    "properties": [
      {"name": "condition", "type": "Condition"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Healing Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": "Attack Effect",
    "properties": [
      {"name": "healing_rank", "type": "Integer"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  },
  {
    "id": "Sensory Effect",
    "module": "Core",
    "kind": "entity",
    "inherits": "Effect",
    "properties": [
      {"name": "sense_type", "type": "String"}
    ],
    "operations": [],
    "invariants": [],
    "relationships": [
      {"type": "belongs_to", "target": "Character", "cardinality": "1"}
    ],
    "behavior_refs": [],
    "story_refs": ["story_resolve_attack"],
    "evidence_refs": []
  }
]
```

**Concepts (Markdown)**

```markdown
## Module: Core

### Character : aggregate_root
- String name
- List<AbilityScore> ability_scores
- owns AbilityScore (1..*)
- owns Attack (0..*)

### Attack : entity
- List<Character> targets
- Boolean resolved
- belongs_to Character (1)

### AreaEffectAttack : entity, inherits Attack
- Area area
- Boolean dodge_for_half
- belongs_to Character (1)

### PerceptionAttack : entity, inherits Attack
- Boolean perception_range
- belongs_to Character (1)

### Effect : entity
- Boolean applied
- belongs_to Character (1)

### Attack Effect : entity, inherits Effect
- belongs_to Character (1)

### Damage Effect : entity, inherits Attack Effect
- Integer damage_rank
- belongs_to Character (1)

### Weakening Effect : entity, inherits Attack Effect
- Integer weaken_rank
- belongs_to Character (1)

### Afflicting Effect : entity, inherits Attack Effect
- Condition condition
- belongs_to Character (1)

### Healing Effect : entity, inherits Attack Effect
- Integer healing_rank
- belongs_to Character (1)

### Sensory Effect : entity, inherits Effect
- String sense_type
- belongs_to Character (1)
```

**Interaction tree (AI / JSON)**

```json
"stories": [
  {
    "id": "story_resolve_attack",
    "name": "Resolve Attack",
    "actors": ["Player", "Gamemaster"],
    "steps": [
      {"id": "step_activate_attack", "name": "User activates attack", "linked_behaviors": [], "trigger": "Player", "response": "Character", "when_then": ""},
      {"id": "step_attack_hits", "name": "Attack hits", "linked_behaviors": [], "trigger": "Character", "response": null, "when_then": ""},
      {"id": "step_attack_misses", "name": "Attack misses", "linked_behaviors": [], "trigger": "Character", "response": null, "when_then": ""}
    ],
    "scenarios": []
  }
]
```

**Interaction tree (Markdown)**

```markdown
### Story: Resolve Attack
- Triggering-Actor: Player
- Responding-Actor: Gamemaster

**Steps**
1. User activates attack (Player → Character)
2. Attack hits (Character → ?)
3. Attack misses (Character → ?)
```

---

### Phase 7 — Behavior

Phase 7 assigns operations to concepts, creates behaviors, links each behavior to the step(s) that exercise it, and groups steps into scenarios (e.g. hit vs miss). Verification: owner has that operation; collaborators appear in the flow.

**Concepts (AI / JSON)**

```json
"concepts": [
  {
    "id": "Character",
    "module": "Core",
    "kind": "aggregate_root",
    "properties": [...],
    "operations": [
      {"name": "activate", "params": ["Attack"], "returns": "void"},
      {"name": "resolve_hit", "params": ["Attack", "Effect"], "returns": "void"},
      {"name": "resolve_miss", "params": ["Attack"], "returns": "void"}
    ],
    "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Attack",
    "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "AreaEffectAttack",
    "inherits": "Attack",
    "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "PerceptionAttack",
    "inherits": "Attack",
    "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Attack Effect",
    "inherits": "Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Damage Effect",
    "inherits": "Attack Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Weakening Effect",
    "inherits": "Attack Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Afflicting Effect",
    "inherits": "Attack Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Healing Effect",
    "inherits": "Attack Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  },
  {
    "id": "Sensory Effect",
    "inherits": "Effect",
    "behavior_refs": ["beh_resolve_hit"],
    "story_refs": ["story_resolve_attack"]
  }
],
"behaviors": [
  {"id": "beh_activate", "name": "activate", "owner": "Character", "collaborators": ["Attack"], "linked_steps": ["step_activate_attack"]},
  {"id": "beh_resolve_hit", "name": "resolve hit", "owner": "Character", "collaborators": ["Attack", "Effect"], "linked_steps": ["step_attack_hits"]},
  {"id": "beh_resolve_miss", "name": "resolve miss", "owner": "Character", "collaborators": ["Attack"], "linked_steps": ["step_attack_misses"]}
]
```

**Concepts (Markdown)**

```markdown
### Character : aggregate_root
- activate(Attack) → void
  Collaborators: Attack
  Interactions: step_activate_attack
- resolve_hit(Attack, Effect) → void
  Collaborators: Attack, Effect
  Interactions: step_attack_hits
- resolve_miss(Attack) → void
  Collaborators: Attack
  Interactions: step_attack_misses

### Attack
Participates in: beh_activate, beh_resolve_hit, beh_resolve_miss

### AreaEffectAttack : inherits Attack
Participates in: beh_activate, beh_resolve_hit, beh_resolve_miss

### PerceptionAttack : inherits Attack
Participates in: beh_activate, beh_resolve_hit, beh_resolve_miss

### Effect
Participates in: beh_resolve_hit

### Attack Effect : inherits Effect
Participates in: beh_resolve_hit

### Damage Effect : inherits Attack Effect
Participates in: beh_resolve_hit

### Weakening Effect : inherits Attack Effect
Participates in: beh_resolve_hit

### Afflicting Effect : inherits Attack Effect
Participates in: beh_resolve_hit

### Healing Effect : inherits Attack Effect
Participates in: beh_resolve_hit

### Sensory Effect : inherits Effect
Participates in: beh_resolve_hit
```

**Interaction tree (AI / JSON)** — Phase 7 adds scenarios when steps form natural paths (hit vs miss)

```json
"steps": [
  {
    "id": "step_activate_attack",
    "name": "User activates attack",
    "linked_behaviors": ["beh_activate"],
    "trigger": "Player",
    "response": "Character",
    "when_then": "When user selects attack from character sheet, Character activates that attack"
  },
  {
    "id": "step_attack_hits",
    "name": "Attack hits",
    "linked_behaviors": ["beh_resolve_hit"],
    "trigger": "Character",
    "response": "Effect",
    "when_then": "When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)"
  },
  {
    "id": "step_attack_misses",
    "name": "Attack misses",
    "linked_behaviors": ["beh_resolve_miss"],
    "trigger": "Character",
    "response": "Character",
    "when_then": "When attack resolves as miss, no effect applied"
  }
],
"scenarios": [
  {"id": "scenario_attack_hits", "name": "Attack hits", "step_refs": ["step_activate_attack", "step_attack_hits"]},
  {"id": "scenario_attack_misses", "name": "Attack misses", "step_refs": ["step_activate_attack", "step_attack_misses"]}
]
```

**Interaction tree (Markdown)**

```markdown
### Story: Resolve Attack

**Steps**
1. User activates attack — beh_activate
   When user selects attack from character sheet, Character activates that attack
   (Player → Character)
2. Attack hits — beh_resolve_hit
   When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)
   (Character → Effect)
3. Attack misses — beh_resolve_miss
   When attack resolves as miss, no effect applied
   (Character → Character)

**Scenarios**
- Attack hits | Attack misses
```

---

### Phase 8 — Variation

Phase 8 splits stories by subtype when mechanics differ and adds **failure-mode scenarios**. Basic scenarios (e.g. hit vs miss) are added in Phase 7 when behaviors are linked. **Subtype concepts (AreaEffectAttack, PerceptionAttack, Damage Effect, etc.) are not discovered here** — they must already exist from Phase 2 (hypothesis) and Phase 6 (structure assigns `inherits`). If extraction and hypothesis did not surface them upfront, Phase 8 cannot recover them; the evidence is biased. Per the *Story vs. Scenario* rule: subtypes with different mechanics get **separate stories** — "Resolve Attack" (base), "Resolve Area Effect Attack", "Resolve Perception Attack", "Apply Damage Effect", "Apply Weakening Effect", "Apply Afflicting Effect". Melee/ranged are **type fields** and appear as parameterized examples in steps, not as subtypes. Phase 8 adds failure-mode scenarios (e.g. "Melee out of reach", "Area effect hits in area") and subtype-specific scenario groupings. The hierarchy is expressed by `inherits` on child concepts; no `variations` field — derive subtypes by querying `concepts.where(inherits === parentId)`.

**solution_model.json v4 (AI / JSON)**

```json
{
  "concepts": [
    {
      "id": "Character",
      "module": "Core",
      "kind": "aggregate_root",
      "inherits": null,
      "properties": [
        {"name": "name", "type": "String"},
        {"name": "ability_scores", "type": "List<AbilityScore>"}
      ],
      "operations": [
        {"name": "activate", "params": ["Attack"], "returns": "void"},
        {"name": "resolve_hit", "params": ["Attack", "Effect"], "returns": "void"},
        {"name": "resolve_miss", "params": ["Attack"], "returns": "void"}
      ],
      "invariants": [],
      "relationships": [
        {"type": "owns", "target": "AbilityScore", "cardinality": "1..*"},
        {"type": "owns", "target": "Attack", "cardinality": "0..*"}
      ],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": ["act_0042", "rel_0012"]
    },
    {
      "id": "Attack",
      "module": "Core",
      "kind": "entity",
      "inherits": null,
      "properties": [
        {"name": "targets", "type": "List<Character>"},
        {"name": "resolved", "type": "Boolean"}
      ],
      "operations": [],
      "invariants": [],
      "relationships": [
        {"type": "belongs_to", "target": "Character", "cardinality": "1"}
      ],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": []
    },
    {
      "id": "AreaEffectAttack",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack",
      "properties": [{"name": "area", "type": "Area"}, {"name": "dodge_for_half", "type": "Boolean"}],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_area_effect_attack"],
      "evidence_refs": []
    },
    {
      "id": "PerceptionAttack",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack",
      "properties": [{"name": "perception_range", "type": "Integer"}],
      "behavior_refs": ["beh_activate", "beh_resolve_hit", "beh_resolve_miss"],
      "story_refs": ["story_resolve_perception_attack"],
      "evidence_refs": []
    },
    {
      "id": "Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": null,
      "properties": [],
      "operations": [],
      "invariants": [],
      "relationships": [
        {"type": "belongs_to", "target": "Character", "cardinality": "1"}
      ],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_resolve_attack"],
      "evidence_refs": []
    },
    {
      "id": "Damage Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack Effect",
      "properties": [{"name": "damage_rank", "type": "Integer"}],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_apply_damage_effect"],
      "evidence_refs": []
    },
    {
      "id": "Weakening Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack Effect",
      "properties": [{"name": "weaken_rank", "type": "Integer"}],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_apply_weakening_effect"],
      "evidence_refs": []
    },
    {
      "id": "Afflicting Effect",
      "module": "Core",
      "kind": "entity",
      "inherits": "Attack Effect",
      "properties": [{"name": "condition", "type": "String"}],
      "behavior_refs": ["beh_resolve_hit"],
      "story_refs": ["story_apply_afflicting_effect"],
      "evidence_refs": []
    }
  ],
  "behaviors": [
    {"id": "beh_activate", "name": "activate", "owner": "Character", "collaborators": ["Attack"], "linked_steps": ["step_activate_attack"]},
    {"id": "beh_resolve_hit", "name": "resolve hit", "owner": "Character", "collaborators": ["Attack", "Effect"], "linked_steps": ["step_attack_hits"]},
    {"id": "beh_resolve_miss", "name": "resolve miss", "owner": "Character", "collaborators": ["Attack"], "linked_steps": ["step_attack_misses"]}
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
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {
                    "id": "step_activate_attack",
                    "name": "User activates attack",
                    "linked_behaviors": ["beh_activate"],
                    "trigger": "Player",
                    "response": "Character",
                    "when_then": "When user selects attack from character sheet, Character activates that attack",
                    "parameterized_examples": ["Punch (melee)", "Bow shot (ranged)"]
                  },
                  {
                    "id": "step_attack_hits",
                    "name": "Attack hits",
                    "linked_behaviors": ["beh_resolve_hit"],
                    "trigger": "Character",
                    "response": "Effect",
                    "when_then": "When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)"
                  },
                  {
                    "id": "step_attack_misses",
                    "name": "Attack misses",
                    "linked_behaviors": ["beh_resolve_miss"],
                    "trigger": "Character",
                    "response": "Character",
                    "when_then": "When attack resolves as miss, no effect applied"
                  }
                ],
                "scenarios": [
                  {"id": "scenario_attack_hits", "name": "Attack hits", "step_refs": ["step_activate_attack", "step_attack_hits"]},
                  {"id": "scenario_attack_misses", "name": "Attack misses", "step_refs": ["step_activate_attack", "step_attack_misses"]},
                  {"id": "scenario_melee_reach", "name": "Melee attack out of reach", "step_refs": ["step_activate_attack", "step_attack_misses"]}
                ]
              },
              {
                "id": "story_resolve_area_effect_attack",
                "name": "Resolve Area Effect Attack",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_activate_area_attack", "name": "User activates area attack", "linked_behaviors": ["beh_activate"], "trigger": "Player", "response": "Character", "when_then": "When user selects area attack, Character activates it"},
                  {"id": "step_area_hits", "name": "Area attack hits targets in area", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Effect", "when_then": "When area resolves, Effect applies to each target (Damage Effect, Weakening Effect, or Afflicting Effect depending on power); dodge for half"}
                ]
              },
              {
                "id": "story_resolve_perception_attack",
                "name": "Resolve Perception Attack",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_activate_perception_attack", "name": "User activates perception attack", "linked_behaviors": ["beh_activate"], "trigger": "Player", "response": "Character", "when_then": "When user selects perception attack, Character activates it"},
                  {"id": "step_perception_hits", "name": "Perception attack hits target in range", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Effect", "when_then": "When target in perception range, Effect applies (e.g. Damage Effect, Weakening Effect, Afflicting Effect); no attack check"}
                ]
              },
              {
                "id": "story_apply_damage_effect",
                "name": "Apply Damage Effect",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_damage_applies", "name": "Damage Effect applies to target", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Damage Effect", "when_then": "When attack hits, Damage Effect applies; resistance check — each degree of failure adds damage (injuries, bruises)"}
                ]
              },
              {
                "id": "story_apply_weakening_effect",
                "name": "Apply Weakening Effect",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_weakening_applies", "name": "Weakening Effect applies to target", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Weakening Effect", "when_then": "When attack hits, Weakening Effect reduces target ability / effect"}
                ]
              },
              {
                "id": "story_apply_afflicting_effect",
                "name": "Apply Afflicting Effect",
                "actors": ["Player", "Gamemaster"],
                "steps": [
                  {"id": "step_afflicting_applies", "name": "Afflicting Effect applies to target", "linked_behaviors": ["beh_resolve_hit"], "trigger": "Character", "response": "Afflicting Effect", "when_then": "When attack hits, Afflicting Effect imposes condition; resistance check to avoid"}
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**solution_model v4 (Markdown)**

```markdown
## Module: Core

### Character : aggregate_root
- String name
- List<AbilityScore> ability_scores
- owns AbilityScore (1..*)
- owns Attack (0..*)
- activate(Attack) → void — beh_activate
- resolve_hit(Attack, Effect) → void — beh_resolve_hit
- resolve_miss(Attack) → void — beh_resolve_miss

### Attack : entity
- List<Character> targets
- Boolean resolved
- belongs_to Character (1)
**Variations**
- AreaEffectAttack — adds area, dodge_for_half (different resolution: area targeting, dodge for half) — separate story
- PerceptionAttack — adds perception_range (different resolution: perception range, no attack check) — separate story

### AreaEffectAttack : entity (inherits Attack)
- Area area
- Boolean dodge_for_half
- story_refs: story_resolve_area_effect_attack

### PerceptionAttack : entity (inherits Attack)
- Integer perception_range
- story_refs: story_resolve_perception_attack

### Effect : entity
- belongs_to Character (1)
**Subtypes** (derived from concepts where inherits → Effect)
- Attack Effect — inherits Effect (parent of damage/weakening/afflicting/healing effects)
- Sensory Effect — inherits Effect, adds sense_type (produces sensory output)
- Damage Effect — inherits Attack Effect, adds damage_rank (resistance check; each degree of failure adds damage) — separate story
- Weakening Effect — inherits Attack Effect, adds weaken_rank (reduces target's resistance) — separate story
- Afflicting Effect — inherits Attack Effect, adds condition (imposes condition; resistance check to avoid) — separate story
- Healing Effect — inherits Attack Effect, adds healing_rank (restores damage or conditions) — separate story

---

# Epic: Combat Resolution

## Sub-Epic: Attack Flow

### Story: Resolve Attack
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. User activates attack — beh_activate
   When user selects attack from character sheet, Character activates that attack
   Examples (type fields): Punch (melee), Bow shot (ranged)
2. Attack hits — beh_resolve_hit
   When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)
3. Attack misses — beh_resolve_miss
   When attack resolves as miss, no effect applied

**Scenarios**
- Attack hits: step_activate_attack → step_attack_hits
- Attack misses: step_activate_attack → step_attack_misses
- Melee attack out of reach: step_activate_attack → step_attack_misses (type-field scenario)

### Story: Resolve Area Effect Attack
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. User activates area attack — beh_activate
2. Area attack hits targets in area — beh_resolve_hit
   When area resolves, Effect applies to each target (Damage Effect, Weakening Effect, or Afflicting Effect depending on power); dodge for half

### Story: Resolve Perception Attack
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. User activates perception attack — beh_activate
2. Perception attack hits target in range — beh_resolve_hit
   When target in perception range, Effect applies (e.g. Damage Effect, Weakening Effect, Afflicting Effect); no attack check

### Story: Apply Damage Effect
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. Damage Effect applies to target — beh_resolve_hit
   When attack hits, Damage Effect applies; resistance check — each degree of failure adds damage (injuries, bruises)

### Story: Apply Weakening Effect
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. Weakening Effect applies to target — beh_resolve_hit
   When attack hits, Weakening Effect reduces target resistance (Toughness)

### Story: Apply Afflicting Effect
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. Afflicting Effect applies to target — beh_resolve_hit
   When attack hits, Afflicting Effect imposes condition; resistance check to avoid
```

---

### Phase 9 — Consolidate

**Concepts (Markdown)** — adds examples, anti-pattern fixes

```markdown
### Character : aggregate_root
- activate(Attack) → void
  Collaborators: Attack
  Interactions: step_activate_attack

**Examples**
| scenario | name | ability_scores |
|----------|------|----------------|
| resolve_attack.player | Fighter | Str 16, Dex 12 |
| resolve_attack.target | Goblin | Str 8, Dex 14 |
```

**Interaction tree (Markdown)** — adds examples to steps

```markdown
**Steps**
1. User activates attack — beh_activate
   When user selects attack from character sheet, Character activates that attack
   Examples: [Player selects Punch from character sheet]
2. Attack hits — beh_resolve_hit
   When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)
   Examples: [Punch hits Goblin, Damage Effect applies 5 damage]; [Weakening Touch hits Goblin, Weakening Effect reduces Toughness]; [Paralyzing gaze hits target, Afflicting Effect imposes Vulnerable]
```

---

### Phase 10 — Assess

Phase 10 produces `assessment.json` — a cross-cutting model assessment. **It does not redo scenario walkthroughs.** Verification of step↔behavior↔concept consistency happens incrementally in Phases 6–7. Phase 10 assesses:

1. **Consistency** — Step-behavior-concept traceability: every step has linked behaviors; every behavior has an owner with that operation; collaborators appear in the flow. (Mostly pass/fail — issues should have been caught in Phase 7.)
2. **Coverage** — Evidence assigned: concepts with evidence_refs; behaviors grounded in evidence. Gaps: evidence not yet assigned to concepts or behaviors.
3. **Completeness** — Orphan concepts (no story_refs), anemia (concepts with no behaviors), over-centralization (one concept doing too much). Phase 9 already fixes anti-patterns; Phase 10 reports any remaining issues.
4. **Type field vs subtype** — For each concept with `inherits`: does it have different mechanics (different behaviors, rules, or resolution) from siblings? If it shares the same operations with only different parameters → flag as possible type-field misclassification (should be parameterized examples in steps, not a hierarchy node). For parameterized examples in steps (e.g. melee vs ranged): if they imply different rules or behaviors → flag as possible subtype misclassification (should be in hierarchy). Per [subtype-vs-type-field-research.md](./subtype-vs-type-field-research.md): mechanical difference test — does switching variant change which *rules* apply? Yes → subtype; no → type field. Aligns with similar discrimination logic in story synchronizers (e.g. hierarchical vs simple cell IDs for sub-epics — tool-generated vs user-created).
5. **Human sign-off** — Checklist for human review: concept framing, behavior ownership, step-to-behavior links, type-field vs subtype, model quality.

**assessment.json (AI / JSON)**

```json
{
  "consistency": {
    "step_behavior_links": "pass",
    "owner_operations": "pass",
    "collaborator_flow": "pass"
  },
  "coverage": {
    "evidence_assigned": 0.92,
    "gaps": ["act_0123 not assigned to any concept", "dec_0045 not linked to behavior"]
  },
  "completeness": {
    "orphans": [],
    "anemia": [],
    "over_centralization": []
  },
  "type_field_vs_subtype": {
    "possible_type_field_misclassified": ["MeleeAttack", "RangedAttack"],
    "possible_subtype_misclassified": [],
    "notes": "MeleeAttack and RangedAttack share same beh_resolve_hit; differ only by range parameter → consider type field on Attack"
  },
  "human_checklist": {
    "concept_framing": "pending",
    "behavior_ownership": "pending",
    "step_behavior_links": "pending",
    "type_field_vs_subtype": "pending",
    "model_quality": "pending"
  }
}
```

Phase 11 (Finalize) applies fixes from the assessment; human resolves checklist items before sign-off.

---

### Phase 11 — Finalize

**Concepts (AI / JSON)** — validated, no structural changes from v5

**Concepts (Markdown)** — assessment fixes applied; full traceability

```markdown
## Module: Core

### Character : aggregate_root
- String name
- List<AbilityScore> ability_scores
- owns AbilityScore (1..*)
- owns Attack (0..*)
- activate(Attack) → void — beh_activate
- resolve_hit(Attack, Effect) → void — beh_resolve_hit
- resolve_miss(Attack) → void — beh_resolve_miss

Stories: Resolve Attack
```

**Interaction tree (Markdown)** — validated, examples complete

```markdown
# Epic: Combat Resolution

## Sub-Epic: Attack Flow

### Story: Resolve Attack
Triggering-Actor: Player | Responding-Actor: Gamemaster

**Steps**
1. User activates attack — beh_activate
   When user selects attack from character sheet, Character activates that attack
   Examples: [Player selects Punch from character sheet]
2. Attack hits — beh_resolve_hit
   When attack resolves as hit, Effect applies (e.g. Damage Effect, Weakening Effect, or Afflicting Effect depending on power)
   Examples: [Punch hits Goblin, Damage Effect applies 5 damage]; [Weakening Touch hits Goblin, Weakening Effect reduces Toughness]; [Paralyzing gaze hits target, Afflicting Effect imposes Vulnerable]
3. Attack misses — beh_resolve_miss
   When attack resolves as miss, no effect applied
   Examples: [Punch misses, Goblin dodges]

**Scenarios**
- Attack hits | Attack misses | Melee out of reach | Area effect hits in area | Perception attack hits in range
```

---

## References (Phase 3 Evidence Buckets)

**Event extraction & semantic roles**

- ACE (Automatic Content Extraction): event trigger + arguments; LDC annotation guidelines. [ACE structures](https://cs.nyu.edu/~grishman/jet/guide/ACEstructures.html)
- PropBank: verb-oriented semantic role labeling; Arg0–Arg5 map to agent/theme/patient. Palmer et al. [PropBank](https://en.wikipedia.org/wiki/PropBank)
- FrameNet: frame-based semantic roles; generalizes across verbs/nouns. [FrameNet](https://framenet.icsi.berkeley.edu/)
- SVO triple extraction: dependency parsing → subject–verb–object; textacy, TakeFive (frame-oriented knowledge graphs). Springer: [Semantic role labeling for knowledge graph extraction](https://link.springer.com/article/10.1007/s13748-021-00241-7)

**Relation extraction**

- Relationship extraction: binary entity–relation–entity; MUC 1998; ACE2005 (PHYS, ORG-AFF, PER-SOC); OpenIE; DocRED. [Wikipedia: Relationship extraction](https://en.wikipedia.org/wiki/Relationship_extraction)
- ACM Survey: [Relation Extraction: Recent Advances and New Frontiers](https://dl.acm.org/doi/full/10.1145/3674501)

**Entity state extraction**

- ProPara, OpenPI: entity state tracking in procedural text; discrete/continuous state models. ACL: [Tracking Discrete and Continuous Entity State](https://aclanthology.org/W19-1502/)
- VerbNet semantic parser for automatic entity state annotation. ACL: [Automatic Entity State Annotation using VerbNet](https://aclanthology.org/2021.law-1.13.pdf)

**Conditional extraction**

- LexNLP `lexnlp.extract.en.conditions`: if, when, unless, until, provided that, conditioned on, etc. [LexNLP conditions](https://lexpredict-lexnlp.readthedocs.io/en/latest/modules/extract/en/conditions.html)

**Terminology extraction**

- Wikipedia: subtask of information extraction; noun phrase chunking; termhood/unithood; C-value/NC-value. [Wikipedia: Terminology extraction](https://en.wikipedia.org/wiki/Terminology_extraction)
- Supports ontology learning, knowledge graph construction, domain modeling.

**CRC / OO design**

- Beck, K. & Cunningham, W. (1989). "A Laboratory For Teaching Object-Oriented Thinking." OOPSLA'89. [CRC paper](https://www.cs.unc.edu/~stotts/COMP145/CRC/papers/beck.html)
- CRC: Class, Responsibility (verb phrases), Collaborator. [Wikipedia: CRC card](https://en.wikipedia.org/wiki/Class-responsibility-collaboration_card)

**Internal**

- [evidence-signal-extraction-design.md](./evidence-signal-extraction-design.md) — twelve evidence-signal techniques, concept triangulation

