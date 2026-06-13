# Rule: Each diagram has a companion element-inventory file with a 1–2 sentence description per element

The outline diagram has a companion `system-context-elements.md` file under `docs/architecture/diagrams/`. The file lists every element that appears in the diagram — actors, systems, relationships — and gives each one a 1–2 sentence description stating what it is and the role it plays. No element in the diagram is undescribed; no described element is absent from the diagram. Failing means the element file is missing, contains unfilled placeholders, has descriptions shorter than a meaningful statement, has descriptions longer than two sentences, or lists elements that do not match the diagram.

## DO

- Give each element its own named entry with the element type in parentheses and a 1–2 sentence description that states what it is and its role.

  **Example (pass):**
  ```markdown
  ### Customer (Person)
  The primary end user who browses the catalogue, adds items to a cart, and submits orders
  through the web browser. Authenticated by the identity provider before any order operation
  is accepted.

  ### Stripe (External System)
  Processes card payments on behalf of the platform; the system sends a charge request and
  receives a synchronous success/failure response plus asynchronous webhook confirmations.
  ```

- Cover every element type the system context notation requires: the system itself (with a **Major functions** list of 4–7 bullets and a **Platform technology** block), every Person (actor/role), every External Software System, and every Relationship (with a **Protocol** line).

  **Example (pass):** `system-context-elements.md` has sections `Systems in Scope` (each with a Major functions list and Platform technology block), `Persons`, `External Systems`, and `Relationships` — no section missing and no element within a section blank.

- Keep the element file and the diagram in sync — every element in the `.drawio` source corresponds to an entry in the element file, and vice versa.

  **Example (pass):** `system-context-elements.md` lists `Auth0 (External System)`. The matching `system-context.drawio` contains an Auth0 box. Neither has an extra element the other lacks.

## DO NOT

- Leave description text as an unfilled template token.

  **Example (fail):** `system-context-elements.md` has an entry `### SendGrid (External System)` with the body `{one-sentence description}`. That is a placeholder, not a description; the file fails the quality bar until real prose is written.

- Write a description longer than two sentences.

  **Example (fail):** The `Orders API (Software System)` entry runs to a paragraph explaining idempotency keys, the Saga pattern, and retry logic. Descriptions beyond two sentences are blueprint-level content; they do not belong in the element file.

- List an element in the file that does not appear in the diagram, or draw an element without a matching entry in the file.

  **Example (fail):** `system-context-elements.md` lists `Datadog (External System)` but `system-context.drawio` has no Datadog box. Alternatively, the `.drawio` has a `WAF` box with no corresponding entry in the element file. Both cases mean the file and the diagram have drifted.

- Omit the element type from the entry heading.

  **Example (fail):** Entry heading reads `### Customer` with no `(Person)` qualifier. Without the type, a reviewer cannot tell whether this is a human actor or an external software system without reading the diagram.

**Source:** Architecture outline practice; describing every element before drawing forces explicit decisions about what belongs in the diagram and produces an auditable inventory that keeps the diagram maintainable across releases.
