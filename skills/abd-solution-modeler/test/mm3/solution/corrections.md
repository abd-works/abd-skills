# Corrections

## Phase 2 (concept_guidance_v1) — Validation Pass 2025-03-16

### Rule: Verb-noun format (no technical implementation terms)
- **DO** use behavioral language; **DO NOT** use method names, class.method() style
- **Example (wrong):** "validates via **Power Level**.validate_rank() and **Power Point**.spend()"; "**Power**.add_effect()"; "**Resistance**.roll_vs_affliction()"
- **Example (correct):** "validates rank against **Power Level** caps and spends **Power Point**"; "adds **Effect** to **Power**"; "rolls **Resistance** check"

### Fixes applied
- Replaced all method-style references in interaction_tree.md Steps with behavioral descriptions
- interaction_tree.md now uses outcome/behavioral language throughout

---

## Systemic Issues — Model Quality 2025-03-16

### 1. Arbitrarily missing steps in stories
- **Issue:** Many stories have steps omitted arbitrarily.
- **Fix:** Audit all stories against evidence; ensure complete step coverage per scenario.

### 2. Examples at story level are broken
- **Issue:** Epic-level Examples look correct, but story-level Examples reference concepts with no actual data. Sometimes correct (when referring to higher-level table); often wrong. Appears random.
- **Example (wrong):** "Player has chosen power level" — not cleanly mapped to any Example in the Defined Character epic.
- **Fix:** Ensure every story-level Example either (a) references a concrete epic-level Example with explicit mapping, or (b) provides its own complete Example data. No orphaned concept references.

### 3. "Create power" as one story is too coarse
- **Issue:** Power creation is a single story; it should be decomposed into multiple stories reflecting the real complexity.
- **Fix:** Decompose into sub-epics/stories: Power structure, Effect selection, Modifiers (Extras/Flaws), Descriptors, Array management, etc.

### 4. Power use in combat is not an effective story
- **Issue:** Power use in combat ignores the rules. Not grounded in source mechanics.
- **Fix:** Re-derive from rules; run validation checks per three-stage process.

### 5. Validation process not applied
- **Issue:** Unclear whether scan/validate were run per AGENTS.md three-stage process on generated artifacts.
- **Fix:** Run `pipeline.py scan` and `pipeline.py validate` on all phases; fix violations; re-validate until clean.

### 6. Power Use interaction (interaction_tree.md 166–172) — mixed stories
- **Issue:** Steps 1–7 are different stories with different conditions, randomly concatenated. Not a coherent story.
- **Example (wrong):** "Check Complication", "Check Descriptor conditions", "Check Action cost", "If Attack Effect...", "If Defense Effect...", "If area effect..." — each is a distinct story with distinct conditions.
- **Fix:** Split into separate stories: Power Use (Attack), Power Use (Defense), Power Use (Area), Power Use (Descriptor-gated), etc. Each story has its own conditions and steps.

### 7. Effect subtypes incompletely modeled (final_domain_model.md 119–132)
- **Issue:** Subtypes imply different classes with different data and behavior. Only Attack and Defense were modeled; Affliction, Control, Sensory, stat-altering effects were not.
- **Example (wrong):** Listing "Subtypes: Attack Effect, Defense Effect, Affliction, Control Effect, General Effect" without modeling each subtype's data and behavior.
- **Fix:** For each subtype (Attack, Defense, Affliction, Control, Sensory, stat-altering, etc.): define distinct properties, operations, and mechanics. No table-of-contents categorization without underlying mechanics.

### 8. Flaws and Extras completely missed
- **Issue:** Flaws and Extras are probably an entire epic with several sub-epics and 20–30 stories. High complexity: types of flaws, types of extras, application rules.
- **Fix:** Add epic: Modifiers (Extras and Flaws). Decompose into sub-epics and stories from concept_guidance and source rules.

### 9. Advantages missed
- **Issue:** Many ways of applying Advantages; complexity completely missed.
- **Fix:** Model Advantages as first-class; capture application variants from source.

### 10. Model not grounded in concept_guidance and source
- **Issue:** Concept guide and original source contain these concepts and mechanics; model lacks the will or wit to go back and create a robust model from that source.
- **Fix:** Re-anchor all phases to concept_guidance and source documents; regenerate models from evidence, not from shallow categorization.

---

## Solution — Critical Quality Steps (abd-solution-modeler only) 2025-03-16

**Problem:** The three-stage process was not enforced for every AI step; no mandatory deep scan of evidence before generation.

**Solution implemented (within abd-solution-modeler only):**

1. **Created `pieces/critical_quality_steps.md`** — Replaces/extends validation with:
   - **Step 0 — Deep Scan (REQUIRED FIRST):** Before generating, you MUST do a deep scan of evidence and concept_guidance; understand nuance at a detailed level.
   - **Three-Stage Process:** Generate → Scan → Validate (all required for every AI step).

2. **Injection into every AI phase** (`assemble_agents.py`):
   - `critical_quality_steps.md` is prepended to every built phase file (concept_guidance_v1/v2, concept_model, structural_model, behavior_model, variation_model, refined_domain_model, model_assessment, final_domain_model).
   - Fallback to `validation.md` if critical_quality_steps.md is missing.

3. **AGENTS.md assembly:** `_CONTENT_ORDER` now uses `critical_quality_steps.md` (with `validation.md` fallback).

---

## Phase 7 (structural_model) — Process Violation 2025-03-16

### Rule: Follow three-layer validation process (AGENTS.md 78–91)
- **DO** regenerate structural_model from concept_model when concept_model changes; run scan and validate after generation.
- **Example (wrong):** Structural model was not regenerated after concept_model was updated; scan and validate were not run for structural_model.
- **Example (correct):** After concept_model changes, regenerate structural_model to align modules and concept headings; run `pipeline.py scan structural_model`; run `pipeline.py validate structural_model`; fix violations; re-validate until clean.

### Fixes applied
- Regenerated structural_model from updated concept_model
- Aligned module structure (Character Definition, Powers and Effects, Combat and Conflict, Materials and Objects, Narrative Mechanics)
- Used **Concept** format for headings to match concept_model
- Added missing concepts: Advantage, Power Level, Defense Effect, Descriptor, Flaw, Power Stunt, Material, Extra Effort, Circumstance Modifier, Charges, Attitude
- Ran scan: 0 violations
- Ran validate: adversarial review against 7 rules — no remaining violations

---

## Phase 6 (concept_model) — Validation Pass 2025-03-16

### Rule: Standard Types for Properties
- **DO** use standard types (String, Number, List<T>, EnumType)
- **Example (wrong):** `- abilities — eight abilities...` (no type)
- **Example (correct):** `List<Ability> abilities` with evidence citation

### Rule: Format
- **DO** use `**Concept** : BaseConcept` for concept headings
- **Example (wrong):** `### Character`
- **Example (correct):** `**Character**` (top-level) or `**Ability** : Character collaborator`

### Rule: EnumType for constrained values
- **DO** use EnumType for fixed sets
- **Example (wrong):** `- type — standard, move, free` (implied string)
- **Example (correct):** `ActionType type {standard, move, free}`

### Fixes applied
- Reformatted concept headings to **Concept** : BaseConcept
- Added standard types to properties (List<**Ability**>, Number, String, Boolean, etc.)
- Added EnumType for ActionType, DefenseType, ModifierType, AbilityName, DurationType, RangeType, DamageType, ConditionName, CheckType, AttitudeStep, PowerStuntCost, ExtraEffortCost where applicable
- Re-ran scan: 0 violations
- Re-ran validate: adversarial review against 3 rules — no remaining violations

---

## Phase 12 (final_domain_model) — Format and Integration 2025-03-16

### Rule: Domain Model Format (pieces/domain.md)
- **DO** use `**ConceptName** : <BaseConcept>` with properties (`- <type> property`), operations (`- operation(params) → return`), Invariants under specific property/operation, Interactions, examples
- **Example (wrong):** Prose summary with "**Composition:** Ability, Skill...", "**Operations:** add_ability, add_skill...", collapsed concepts, no example tables
- **Example (correct):** One concept per heading; full property types; full operation signatures with params and return; Invariant under each; Interactions list; examples with columns matching concept properties

### Rule: Integration of all models
- **DO** integrate concept_model (properties), structural_model (composition/aggregation), behavior_model (operation signatures), variation_model (invariants)
- **Example (wrong):** Final model as standalone summary; ignores concept_model property types and structural relationships
- **Example (correct):** Final model = concept + structural + behavior + variation merged; each concept has complete property/operation/invariant set

### Rule: Example tables match Domain Model (validated-examples-match-domain-model.md)
- **DO** add example tables to interaction tree; columns match concept properties; every **Concept** in labels has corresponding table
- **Example (wrong):** No example tables in interaction tree; final model lists "examples:" with no actual tables
- **Example (correct):** Epic-level Examples with tables (Campaign Power Level, Character in Creation, etc.); columns = concept property names

### Fixes applied
- Rebuilt final_domain_model in correct format: one concept per heading, full properties with types, full operations with signatures, Invariants under property/operation, Interactions, examples
- Integrated concept_model (properties), structural_model (composition/aggregation), behavior_model (operation signatures), variation_model (invariants)
- Added example tables to interaction_tree: Campaign Power Level, Campaign Power Point Budget, Character in Creation, Allocated Ability, Allocated Skill, Created Power, Resolved Attack, Target Defense, Applied Condition, Resistance Check Result, Effect to Modify, Applied Extra, Applied Flaw
