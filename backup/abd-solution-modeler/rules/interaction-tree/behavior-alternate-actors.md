---
title: Alternate actors in steps
impact: HIGH
---

## Alternate actors in steps

Alternate between actors every 1–2 steps. Scenarios should show back-and-forth interaction between user and system.

**DO** alternate actors every 1–2 steps to show interaction flow.
- Actor acts, system responds: `User submits order → System validates payment`
- System completes, actor reacts: `System displays confirmation → User reviews details`
- System can chain 1–2 sequential actions before returning to actor: `User submits form → System validates input → System saves data → System displays result → User confirms`

**DO NOT** have more than 2 consecutive steps from the same actor without switching.
- Example (wrong): `System validates → System processes → System stores → System notifies` — too many consecutive system steps
- Example (wrong): `User enters name → User enters email → User enters password → User clicks submit` — should have system validation between steps
