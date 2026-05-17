### Rule: Mechanism section has all five parts

Every mechanism in the produced reference document must contain the **same five-part shape** so the implementation skill can generalize across mechanisms. The five parts are **Principles & Patterns**, **File Structure**, **Participants** (class diagram or table), **Flow** (sequence diagram), and **Walkthrough Example**, followed by a **Testing the Mechanism** subsection. A reviewer should be able to land on any one mechanism and find every part without scrolling away. Passing means each mechanism reads as a self-contained recipe. Failing means a mechanism is missing a part, or parts are merged into prose that hides whether the structure is there.

#### DO

- Give **every** mechanism the heading sequence `Principles & Patterns`, `File Structure`, `Participants`, `Flow`, `Walkthrough Example`, `Testing the Mechanism` (in that order).

  **Example (pass):** `## Mechanism: Caching` is followed by `### Principles & Patterns`, `### File Structure`, `### Participants`, `### Flow`, `### Walkthrough Example`, `### Testing the Mechanism` in that exact order.

- Use **fenced code blocks** for the **File Structure** tree so it renders as a tree, not as prose with slashes.

- Make each mechanism section **self-contained**: someone arriving via deep link can implement it without reading other mechanisms.

- In `### Testing the Mechanism`, state which tier tests this mechanism and which test doubles / mocks are used. Cross-reference `## Testing Architecture` for full examples but do not duplicate them inline.

  **Example (pass):** `### Testing the Mechanism` says "Domain tier — inject `Mock<IPaymentGateway>` via constructor; assert `gateway.Charge()` called once. See Testing Architecture for the `[AssemblyInitialize]` wiring."

#### DO NOT

- Create a standalone **`## Mechanism: Test Tiers`** or **`## Mechanism: Test Strategy`** or any mechanism whose entire purpose is describing how tests are organised. That content belongs in `## Testing Architecture`, not in a mechanism section. Mechanisms are cross-cutting concerns of the production architecture (error handling, caching, auth, game bridge seam, etc.).

  **Example (fail):** `## Mechanism: Test Tiers` with Principles & Patterns describing Tier 1 vs Tier 2 isolation. This is a testing strategy, not an architecture mechanism.

- Merge `Participants` and `Flow` into a single prose paragraph that mentions classes and sequence in the same sentence.

  **Example (fail):** `### How it works: the controller calls the service, which calls the repository...` with no class table, no class diagram, and no sequence diagram.

- Skip `### Testing the Mechanism` because "testing is covered in the Testing Architecture section."

  **Example (fail):** Mechanism `Authorization` ends after `Walkthrough Example` with no testing sub-section. The reader has no idea which tier owns the verification or which helper to extend.

- Reorder the parts so that, for example, `Walkthrough Example` comes before `Participants`.

**Source:** Practice-skill authoring convention (abd-architecture-reference). The five-part shape is the contract between this skill and `abd-build-architecture-skill`.
