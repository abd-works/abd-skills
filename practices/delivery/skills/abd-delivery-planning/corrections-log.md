# abd-delivery-planning — corrections log

## Entry 1 — routine template instead of explicit slot plan

| Field | Content |
| --- | --- |
| **Context** | PawPlace `agile-delivery-plan.md` Runs 3–10 authored as "routine template" with offset table and estimated slot ranges |
| **Status** | confirmed |
| **DO / DO NOT** | **DO** list every run (3–10) and every slot row in saved multi-increment plans. **DO NOT** substitute offset/skill-pattern templates or estimated slot maps for explicit slot schedules. |
| **Example (wrong)** | `## Runs 3–10 — Increments 2–9 (routine template)` with `\| Offset \| Phase \|` and `\| 3 \| 2 \| 43 \| ~68 \|` only |
| **Example (correct)** | `## Run 3 — Increment 2: …` with `\| Slot \| Phase \| Role \| Skill(s) \| Deliverable \|` rows 43–68 |
| **Likely source** | `prompt gap` — SKILL.md §2c described runs but not mandatory per-slot expansion; no scanner for template anti-patterns |
