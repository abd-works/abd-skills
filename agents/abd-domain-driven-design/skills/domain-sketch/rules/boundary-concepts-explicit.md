# Rule: Boundary concepts are explicit about who defines and who enforces

**Scanner:** AI review

When a concept in this module defines something that another module enforces or consumes, both sides of the relationship must be stated. Passing means every boundary term names who defines, who enforces, and what crosses the boundary. Failing means a boundary term says only "owned by X" without capturing the define/enforce relationship.

## DO

- State what this module defines and what the consuming module enforces.

  **Example (pass):** "*game modifier* — *conditions* define them (action restrictions, check penalties, defense reductions); enforcement is owned by the consuming module (Combat for action restrictions, this module for check penalties)."

- Name boundary terms in the `#### Boundary terms` section with both sides of the relationship.

  **Example (pass):** "*action round structure* — defined by Combat; consumed by this module when restricting what a conditioned character may do in a round."

## DO NOT

- Write boundary terms as bare ownership claims with no relationship detail.

  **Example (fail):** "*action round structure* — owned by Combat." — doesn't say what this module sends to Combat or what Combat enforces on behalf of this module.

- Dismiss cross-module mechanics with "another module handles it" and no further detail.

  **Example (fail):** "Condition enforcement is handled elsewhere." — which module? What mechanism? What crosses the boundary?

**Source:** Correction 24 (mm3e-online-holistic engagement).
