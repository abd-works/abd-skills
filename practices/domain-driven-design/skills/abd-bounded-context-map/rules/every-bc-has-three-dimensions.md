# Rule: Every dependency has three dimensions — domain mapping, integration mechanism, team engagement

Every dependency arc in `bounded-context-map.md` must record all three dimensions: what domain concepts cross the boundary, how the systems communicate, and how the teams collaborate. A complete dependency means no reviewer has to guess at any of the three. Failure is a dependency row with one or more dimensions missing, blank, or filled with only a placeholder.

## DO

- Fill all three dimension fields for every dependency arc: **Domain mapping**, **Integration mechanism**, and **Team engagement model**.

  **Example (pass):**

  ```
  ### Trading → DCF — Front Page
  - Direction: Trading is upstream; Front Page is downstream
  - Domain mapping: Deal information and counterparty details flow into Front Page for case aggregation
  - Integration mechanism: REST/API (via Filing and Communications Service)
  - Team engagement model: Anticorruption Layer — Service Provider
  ```

- When a dimension is genuinely undecided, write a specific follow-up action with an owner and target date rather than leaving the field blank.

  **Example (pass):**

  ```
  - Integration mechanism: TBD — decision pending POC results from API team. Owner: Sarah. Target: Sprint 12.
  ```

## DO NOT

- Leave any of the three dimension fields blank or missing from a dependency arc.

  **Example (fail):**

  ```
  ### Trading → Front Page
  - Direction: upstream/downstream
  - Domain mapping: deal data
  ```

  Integration mechanism and team engagement model are absent — the arc is incomplete.

- Use generic placeholders like "TBD" or "various" without a named owner and resolution date.

  **Example (fail):**

  ```
  - Integration mechanism: TBD
  - Team engagement model: TBD
  ```

  No owner, no target date — the placeholder will never be resolved.

**Source:** Kept chunk #7 in `inputs/abd-answers-retrieval.md` — ABD three-dimension dependency model (DDD Training slide 66, EWMA slide 6).
