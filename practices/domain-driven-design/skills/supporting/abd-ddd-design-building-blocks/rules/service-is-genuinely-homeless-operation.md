---
scanner:
---
# Rule: Service is genuinely homeless operation

A Service stereotype is only valid when the operation **does not naturally belong** to any single Entity or Value Object. If the operation could coherently live on one concept without distorting it, it should be a method on that concept — not a Service. Passing means every Service entry explains why placement on any existing concept would distort that concept. Failing means Services are used as a dumping ground for behavior that has a clear owner.

## DO

- Explain which concepts the operation spans and why none of them can own it alone.

  **Example (pass):** "**Spans:** Customer (preferences), Pet (availability), Breed (standards). **Rationale:** Matching logic requires inputs from three aggregates — placing it on Customer makes Customer a search engine; placing it on Pet makes Pet responsible for customer preferences."

- Confirm the Service is stateless (or explain why state is domain-justified if it is not).

  **Example (pass):** "**Stateless:** Yes — accepts inputs, returns results, holds nothing between calls."

- Name the Service using domain language — the operation it performs, not a technical pattern name.

  **Example (pass):** `PetMatchingService`, `TransferAuthorizationService` — named for what the domain expert would call the action.

## DO NOT

- Create a Service for an operation that clearly belongs on one Entity just because "services are easier to test."

  **Example (fail):** `OrderTotalCalculationService` when the Order aggregate already owns its lines and the total invariant — this is naturally `Order.recalculateTotal()`.

- Use Service as a catch-all for "I don't know where this goes."

  **Example (fail):** "**Rationale:** Didn't fit anywhere else." — that is not a rationale; ask which concept the operation's inputs and outputs most naturally belong to.

- Name Services with infrastructure terms instead of domain language.

  **Example (fail):** `DataProcessingService`, `HelperService`, `UtilityService` — these are not domain operations.

**Source:** Kept chunks #1, #3, #9 in `inputs/abd-answers-retrieval.md`
