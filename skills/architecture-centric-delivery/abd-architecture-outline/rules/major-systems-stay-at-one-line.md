# Rule: Major systems stay at one line

The Major Systems section of the outline lists each subsystem the architecture distinguishes and gives each one **one line of description**. Internal components, mechanisms, data models, and patterns are out of scope — they belong in the blueprint and reference documents. The catalogue exists so a reader can map any feature request or operations alert to a named owner-system in seconds. Failing means a system has a multi-paragraph description, a component list, code references, or an interface contract embedded in the outline.

## DO

- Render the major systems as a table with three columns: System, One-line description, Primary owner/module.

  **Example (pass):**

  | System | One-line description | Primary owner / module |
  |---|---|---|
  | **Identity** | Authenticates users and issues tokens; thin wrapper over Auth0. | `packages/identity` |
  | **Orders** | Order lifecycle from cart to fulfilment; canonical source of revenue events. | `packages/orders` |

- Make the one-line description a *role-in-the-system* statement, not a feature list.

  **Example (pass):** "Read-mostly product catalogue with strong cache reliance." — names the role and a defining trait.

- Defer all "how" questions about a system to the blueprint or reference document linked from the outline.

  **Example (pass):** The Orders row above says nothing about *how* orders flow through the system; that lives in `architecture-blueprint.md`.

## DO NOT

- Expand a major system's description into a paragraph about its internal components.

  **Example (fail):**

  | System | Description |
  |---|---|
  | Orders | The Orders system contains an `OrderService`, an `OrderRepository`, an `OrderEventPublisher`, and integrates with the Catalogue system to validate line items. It uses the Saga pattern for distributed transactions and stores events in an outbox table for at-least-once delivery. |

  This is blueprint-level content invading the outline.

- List endpoints, classes, database tables, or message topics in the outline.

  **Example (fail):** A "Notifications" row that lists six event-bus topics and four database tables. The outline should name the system; the blueprint owns the contract.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the outline is deliberately shallow, the blueprint owns components.
