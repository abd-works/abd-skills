# Rule: Introduce a collection class when the collection has unique behavior

**Scanner:** Manual review

When an entity owns multiple related objects and managing that collection requires unique behavior beyond simple holding — such as supersession logic, sequential processing, end-of-turn checks, or constraint enforcement — introduce a named collection class that owns that behavior.

## DO

- Introduce a collection class and give it the management responsibilities.

  **Example (pass):** `Imposed Conditions` owns `apply new condition` with supersession invariants. `Character` simply holds `imposed conditions | Imposed Conditions`.

  **Example (pass):** `Ongoing Effects` owns `make resistance check` and `end effect`. `Character` simply holds `ongoing effects | Ongoing Effects`.

## DO NOT

- Put collection management behavior directly on the entity.

  **Example (fail):** `Character` owns `apply new condition` with all supersession logic — the character class becomes bloated with condition-management concerns.

- Leave collection management implied without a named owner.

  **Example (fail):** Domain Language says "character tracks ongoing effects" with no named class to own the tracking and end-of-turn check.

- Create a collection class when the collection has no behavior beyond holding.

  **Example:** If `Character` simply holds a list of traits with no management logic, `traits | Trait` on `Character` is sufficient — no `Traits` collection class is needed.

**Source:** Engagement convention (class-responsibility-collaborator skill).
