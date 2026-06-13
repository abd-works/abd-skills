# Rule: Major systems stay at one line

The Major Systems section of the outline lists each subsystem the architecture distinguishes and gives each one **one line of description**. Internal components, mechanisms, data models, and patterns are out of scope — they belong in the blueprint and reference. The catalogue exists so a reader can map any feature request or operations alert to a named owner-system in seconds. Failing means a system has a multi-paragraph description, a component list, code references, or an interface contract embedded in the outline.

## DO

- The Major Systems section is a table with three columns: System, One-line description, Primary owner/module.

  **Example (pass):**

  | System | One-line description | Primary owner / module |
  |---|---|---|
  | **Identity** | Authenticates users and issues tokens; thin wrapper over Auth0. | `packages/identity` |
  | **Orders** | Order lifecycle from cart to fulfilment; canonical source of revenue events. | `packages/orders` |

- Every one-line description is a role-in-the-system statement — what the system does and a defining trait — not a feature list.

  **Example (pass):** "Read-mostly product catalogue with strong cache reliance." Names the role and one defining trait; nothing about how it is built.

- All "how" detail — internal mechanisms, component lists, interfaces, code references — is absent from the table.

  **Example (pass):** The Orders row says nothing about how orders flow; that lives in `architecture-blueprint.md`.

## DO NOT

- Expand a major system's description into a paragraph about its internal components.

  **Example (fail):**

  | System | Description |
  |---|---|
  | Orders | The Orders system contains an `OrderService`, an `OrderRepository`, an `OrderEventPublisher`, and integrates with the Catalogue system to validate line items. It uses the Saga pattern for distributed transactions and stores events in an outbox table for at-least-once delivery. |

  This is blueprint-level content.

- List endpoints, classes, database tables, or message topics in the outline.

  **Example (fail):** A "Notifications" row that names six event-bus topics and four database tables. The outline names the system; the blueprint owns the contract.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the outline is deliberately shallow — the blueprint owns components.
