# Object model critique — `map-model-spec.json` (fixture-specific)

**Scope:** This note reviews **one** `map-model-spec.json` produced by the skill against a **single test corpus** in `test/mm3/`. It uses that corpus’s vocabulary on purpose to show *where* the pipeline broke down. For **domain-neutral** analysis of the skill itself (any story-map + OO modeling use case), see `docs/pipeline-deep-dive.md`.

Expert review of the inheritance-heavy scaffold: naive OO mistakes, alignment with `abd-maps-models-specs` rules (concepts, domains, scaffolding — not evidence/chunks), and reconciliation across modules.

**Sources reviewed:** `map-model-spec.json`, module `depends_on`, rules (`concept-layering-scaffold`, `classify-variants-before-modeling`, `module-depends-on`, `no-junk-concepts`, `no-anemia`, `no-over-centralization`), and `parts/domain.md` composition vs `extends`.

---

## Dependency order (how to read this)

In **`depends_on`**, **consumers** list **providers**:

| Module | Outgoing `depends_on` |
|--------|------------------------|
| **Ranks and measures** | none in spec |
| **Abilities** | none in spec |
| **Checks and tasks** | → Ranks and measures |
| **Skills** | → Abilities, Checks and tasks |
| **Powers** | → Abilities, Checks and tasks |
| **Combat resolution** | → Abilities, Checks and tasks |

**Most wired-in consumers** (each with two provider links): **Skills**, **Powers**, **Combat resolution**.

**Most depended-upon providers** (three consumers each): **Abilities**, **Checks and tasks**.

A sound refactor review starts from **Ranks** and **Abilities**, then **Checks**, then the three dependents.

---

## 1. Ranks and measures

### Naive mistake: `MeasurementTable` as superclass for unrelated “row” and “rule” concepts

`TimeMeasureRow`, `AthleticsJumpDistanceFromCheck`, `MaterialToughnessOrdinalScale`, `CombatRoundDurationEstimate`, `EnvironmentalHazardIntensityExamples` all **`extend MeasurementTable`**. In OO terms, a **table** is one cohesive abstraction (rows/columns, lookup). Jump-distance-from-Athletics, fall damage, hazard examples, and “~6 seconds per round” are **different mechanisms**: some are **lookup tables**, some are **formulas**, some are **narrative timing**. Inheritance here is mostly **“we needed a parent string in JSON”**, not **is-a** in the domain.

**`FallDamageRankFromDistanceRank` extends `Rank`** while siblings extend `MeasurementTable` — the tree is **inconsistent** (rank-based formula vs “table” family).

**`VehicleSizeCategoryPointCost` extends `Rank`** — vehicle sizing cost is a **build/purchase rule** that *uses* ranks; it is not a *kind of* abstract rank value. Classic **implementation inheritance for convenience** instead of **composition** (e.g. `Rank` + `PointCostRule`).

### Rule tie-in

- **`classify-variants-before-modeling`** — these mix **pipelines** (formula vs table vs flavor scale).
- **`concept-layering-scaffold`** — base → category → implementation is blurred: everything is flattened under `MeasurementTable`.

---

## 2. Abilities

### Naive mistake: subtyping `Ability` / `AbilityRank` for processes, gates, and derived rules

- **`AbilityRankPurchase` extends `AbilityRank`** — spending PP for +1 rank is a **purchase transaction** (or `CharacterBuild` operation), not a specialization of “a rank value.”
- **`InteractionTargetMentalThreshold` extends `AbilityRank`** — owns **DC/threshold behavior** keyed by Int; that is a **rule object** or **modifier policy**, not “a rank.”
- **`ConstructAdvantageAbilityGate` extends `Ability`** — acceptable as a **constraint** on constructs, but it is **cross-cutting** (Abilities × Advantages); burying it only under `Ability` hides **collaboration** (guidelines prefer **composition** or explicit relationships).

**`StaminaBreathHoldRoundBudget` extends `Stamina`** — breath-hold duration is a **derived rule** from Stamina in a specific chapter; **is-a Stamina** overstates the relationship: it is **behavior that references** Stamina, not a subtype of the ability “Stamina.”

### Rule tie-in

- **`no-junk-concepts` / duplicate decision** — several rows are **the same “rule about abilities”** sliced by topic; without **`properties`/`operations`/`relationships`**, the model risks **anemic siblings** (**`no-anemia`**).

---

## 3. Checks and tasks (largest structural problems)

### Severe mistake: `extends Check` as a dump for “anything in the chapter that mentions a check or a number”

Examples that are **not** “a kind of check” in an OO sense:

- **`StandardAndMoveActionPerCombatRound`** and **`ReactionVersusFreeActionTiming`** — **action economy / timing**; they do not specialize the **check** protocol (roll + modifiers vs DC). Violates **`classify-variants-before-modeling`**: different **pipeline** than `Check`.

**`ClimbCircumstanceModifierTable` extends `Check`** — a **modifier table** is normally **composition** (`Check` has `circumstanceModifiers: ModifierTable`) or a **`CircumstanceModifier` aggregate**, not a subtype of check.

**`AcrobaticsTaskMenu` extends `Check`** — a **menu of named tasks** is **taxonomy/metadata**, not a check instance.

**`UltimateEffortFixedResult` extends `Check`** — hero-point spend that **fixes die result** is a **metarule / spend** on a check, not a check subtype (strategy pattern, or `CheckResolution` + `HeroPointOverride`).

**`OpposedEffectCheck`** has **`foundational: false`** and **no `extends`** — sits awkwardly next to **`OpposedCheck` extends `Check`**. Unclear **is-a vs related mechanism**.

### Rule tie-in

- **`concept-layering-scaffold`** — **Check** is overloaded: **resolution**, **DC construction**, **circumstance tables**, **action economy**, **hero point overrides** — **`no-over-centralization`** risk on `Check` as a **god-ish** superclass by accident.

---

## 4. Skills

### Naive mistakes

- **`SkillCatalog extends Skill`** — a **catalog/index** is **not** a skill; it is **metadata** or a **`SkillRegistry`**. Textbook **wrong is-a** (**`no-junk-concepts`** if it duplicates “thing named in the index”).
- **`OpposedSkillPairing extends SkillCheck`** — **pairings** are **relationships** between skills (graph/lookup), not a **kind of** skill check roll.
- **`InvestigationVersusPerceptionSearch` extends `Skill`** — the *distinction between two skills’ use* is **procedural guidance**, often modeled as **methods on a context** or **`SkillUseCase`**, not inheritance from `Skill`.

### Rule tie-in

- **`classify-variants-before-modeling`** — “which skill when” is often **enum / role** on a unified **`SkillCheck`**, not dozens of **`extends Skill`**.

---

## 5. Powers (breadth + deep `extends PowerEffect` chain)

### Core mistake: `PowerEffect` as universal superclass for mechanics, metadata, samples, and catalogs

- **`Advantage extends PowerEffect`** — in M&M, **advantages** and **powers** share PP economy but are **different design constructs**; forcing **is-a** conflates **purchase categories** (**`classify-variants-before-modeling`** would often use a **sibling under `Trait`/`Purchasable`** or **composition**).
- **`Descriptor extends PowerEffect`** — descriptors are **annotations on** effects, not **subtypes of** effect. Prefer **composition** (`PowerEffect` **has** `DescriptorSet`).
- **`PowerLevel extends PowerPoints`** — **series limit** vs **point budget** are related but **not** “PL is a kind of PP.”
- **`AlternateVehicleEquipmentPointPricing` extends `PowerPoints`** — again a **pricing pattern**, not a type of points.
- **`PowerEffectNameTableFragment`, `PowerExtraSection`, `SamplePowerWriteupSchema` extend `PowerEffect`** — **documentation/layout artifacts** or **schemas**, not domain subtypes; **`no-junk-concepts`** territory (handbook structure mistaken for mechanics).
- **Concrete samples** (`BlastRangedDamageEffect`, `CommunicationLimitedFlaw`, `CreateEffectExtras`, …) **`extend PowerEffect`** — risks **confusing instances / build examples with taxonomic types**. Often **`PowerEffect`** + **`effectType` enum** + **`extras[]`**, or **`PowerTemplate`** **aggregating** `PowerEffect`, is cleaner.

**`PowerModifierCatalog`, `AlternateEffectArray`, `DescriptorLayer`** — **`foundational: false`**, **no `extends`** — the model admits they are **different beasts** but has not integrated them into a **layered** tree (**`concept-layering-scaffold`** gap).

---

## 6. Combat resolution

### Naive mistakes

- **`InitiativeCheck extends Check`** — reasonable **is-a** check.
- **`FightingStyleAdvantageBundleExamples extends Advantage`** — **examples** as a **class** is a **modeling smell** (documentation as type).
- **`ImperviousSkipsUnneededAttackRoll extends ResistanceCheck`** — rule is about **whether you roll to hit** when damage cannot penetrate; that is **attack pipeline / immunity**, not **resistance saving throws**. Wrong **parent** breaks **substitutability**.
- **`MinionCombatResolutionPackage extends Condition`** — minion **combat options** are **not** character **conditions** (dazed, staggered, etc.). Wrong **bounded context**.
- **`CoveringAttack`** — **no `extends`** while related ideas use `Check`; incomplete layering.

**Cross-module:** **`AreaAndPerceptionAutomaticEffectResolution` extends `Check`** — lives under **Combat resolution** but describes **attack types skipping** checks; **tight coupling** of **Power/Attack** to **Check** without a named **AttackResolution** umbrella (**`module-depends-on`** lists Checks but **concept placement** is fuzzy).

---

## Reconciliation: themes across modules

| Theme | What went wrong | Better direction (conceptual) |
|--------|------------------|-------------------------------|
| **Table / formula / narrative** | All hung under `MeasurementTable` or `Check` | Split **LookupTable**, **Formula**, **TimingRule**, **ModifierTable**; **compose** into tasks |
| **Purchase / pricing / PP** | `extends Rank`, `extends PowerPoints`, `extends AbilityRank` | **`SpendBudget`**, **`TraitPurchase`**, **`PricingRule`** composed with traits |
| **Descriptors & extras** | `extends PowerEffect` | **`Descriptor`**, **`Extra`**, **`Flaw`** as **parts of** or **policies on** `PowerEffect` |
| **Action economy** | `extends Check` | **`TurnStructure`**, **`Action`**, **`Reaction`** — not checks |
| **Examples & fragments** | Named concepts extending core types | **`DocumentationFragment`** or fold into **evidence**, not **is-a** |

---

## Rules (concepts / scaffolding / domains)

- **`classify-variants-before-modeling`**: The spec often **flattens different pipelines** into one parent (`Check`, `PowerEffect`, `MeasurementTable`).
- **`concept-layering-scaffold`**: **Base → categories → implementations** is weak; many lists are **flat siblings** with `extends` pointing at the same parent.
- **`module-depends-on`**: Declared edges are **minimal**; **cross-cutting** rules (constructs, vehicles, HQ) are **forced into** the nearest module, which **masks real dependencies** (many honest gaps live in `open_questions`).

---

## Bottom line

The model reads like **evidence-first tagging**: each chunk became a **new class** with **`extends` chosen from the nearest chapter noun** (`Check`, `PowerEffect`, `MeasurementTable`). That produces **naive OO**: **God-adjacent** parents (**especially `Check` and `PowerEffect`**), **wrong is-a** (catalogs, examples, timing, pricing), and **inconsistent roots** (e.g. `Rank` vs `MeasurementTable`, `ResistanceCheck` for attack-skip). Your own **`parts/domain.md`** preference — **composition for has-a, inheritance only for true substitutability** — is the standard the spec should be held to next; the **`extends`** field in JSON would need a **systematic pass** to separate **type hierarchy** from **“this rule references that concept.”**

### Highest-leverage first refactor

**Checks and tasks** — detaching **action economy**, **modifier tables**, and **hero-point overrides** from **`Check`** will clarify **Skills**, **Powers**, and **Combat resolution** downstream.

---

*Generated as a readable companion to the scaffold in `map-model-spec.json`.*
