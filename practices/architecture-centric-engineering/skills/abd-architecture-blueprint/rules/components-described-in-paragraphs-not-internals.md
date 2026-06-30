# Rule: Components described in paragraphs, not internals

A component in the blueprint is described in **one to two short paragraphs** covering **purpose**, **dependencies**, and **interactions** — no internal class lists, no method tables, no file trees, no code snippets. The blueprint sits between the outline (one-liner) and the reference (full walkthrough); internal structure belongs in the reference, not here. Failing means a component description bullets out every class in the package, lists every public method, embeds a file tree, or runs to multiple pages.

## DO

- Write each component as 1–2 paragraphs with the three named subheadings (Purpose, Dependencies, Interactions) or three sentence-shaped beats in a single paragraph.

  **Example (pass):**

  > #### OrderService
  >
  > **Purpose.** Owns the order lifecycle from cart to fulfilment; canonical source of revenue events.
  >
  > **Dependencies.** `IOrderRepository`, `ICatalogueClient`, `IEventPublisher`, `IClock`.
  >
  > **Interactions.** Called from the orders API; calls into the Catalogue system on validation; emits domain events consumed by Notifications.

- Name dependencies as interface symbols, not implementation classes. The component's job in the blueprint is what it *uses*, not what it *contains*.

  **Example (pass):** "Depends on `IPaymentProvider`" rather than "uses `StripePaymentProvider`".

- Defer "how does it do X?" to the architecture reference by explicit forward link when the question naturally arises.

  **Example (pass):** "Implements the outbox pattern for cross-component event delivery — see the Persistence mechanism's `architecture-context.md` for the full transactional shape."

## DO NOT

- List every public method or property of the component.

  **Example (fail):**
  > **OrderService methods:** `createCart()`, `addLineItem()`, `removeLineItem()`, `applyDiscount()`, `submit()`, `cancel()`, `fulfil()`, `refund()`, `archive()`.

  The method list is reference-level content and changes every sprint; in the blueprint it adds noise without adding clarity.

- Embed code or pseudo-code inside a component description.

  **Example (fail):** A `OrderService` paragraph followed by a 30-line TypeScript snippet showing the `createCart` implementation. That is reference content.

- Drop a file tree under each component.

  **Example (fail):**
  > **OrderService files:**
  > ```
  > packages/orders/
  > ├── order-service.ts
  > ├── order-repository.ts
  > ├── order-event-publisher.ts
  > └── ...
  > ```
  > File structure of a component is reference-level content (the reference's File Structure section). Keep the blueprint at paragraphs.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); blueprint is "components in paragraphs", reference owns internals.
