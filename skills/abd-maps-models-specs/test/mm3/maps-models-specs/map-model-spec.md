# MM3 map / model / spec (stub — orchestrator + critic alignment)

This file exists so **`critic_mm3_domain.py`** can score **model_keywords** against `rules/mm3_domain_critic.json`.

It is **not** an extracted truth from the handbook — replace with promoted concepts as the pipeline matures.

## Core resolution

- **Check** — base resolution object; specializations include **AttackCheck**, **DefenseCheck**, **OpposedCheck**, **SkillCheck**, **AbilityCheck** (and routine checks vs resistance).
- **Trait** — durable character capabilities (**Skill**, **Ability**, **Defense**) that provide bonuses and participate in checks. **Power** is a container, not a trait, but powers apply **Effect** instances.

## Powers vs effects

- **Power** aggregates one or more **Effect** (ranked, with **extras** and **flaws**).
- **Effect** categories (sensory, attack, movement, …) are **not** the same as book table-of-contents lines.

## Attack-style effects

- **Damage** and **Affliction** specialize a common **AttackEffect** shape (resistance paths differ).

## Modifiers

- **Modifier** / **Extra** / **Flaw** — cross-cutting; categorize by behavior, not only by TOC.
