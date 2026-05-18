### Rule: Include class and sequence diagrams for every mechanism

Every mechanism must show its **participants** as either a Mermaid `classDiagram` block **or** a Markdown participants table (Class / Layer / Responsibility / Collaborators), and must show its **flow** as a Mermaid `sequenceDiagram` block. The flow diagram is mandatory because the implementation skill renders timing from it. The class view may be a table when the relationships are simple enough that a diagram adds no signal, but the **classes-and-layers information must be present** in some structured form — never just a paragraph of prose. Passing means a reader who only opens the Participants block and the Flow block already knows who the actors are and the order of calls. Failing means either block is missing, both are prose, or the sequence diagram is an ASCII sketch rather than Mermaid.

#### DO

- Use ` ```mermaid\nsequenceDiagram\n... ``` ` for the **Flow** section. Mermaid is required so downstream tools can render it.

  **Example (pass):** `### Flow` is followed by a fenced block starting with `\`\`\`mermaid\nsequenceDiagram\n    participant Controller\n    Controller->>Service: createInvoice(input)`.

- For **Participants**, use either ` ```mermaid\nclassDiagram\n...``` ` **or** a four-column Markdown table with headers `Class / Module | Layer | Responsibility | Collaborators` (or both).

  **Example (pass):** `### Participants` contains a Markdown table listing `CachingRecipientsRepository | Infrastructure | LRU + TTL side-car | MongoRecipientsRepository`.

- When a mechanism has more than five participants, **prefer the table** for readability and add a small Mermaid class diagram only for the central trio.

  **Example (pass):** A `Persistence` mechanism with eight classes ships a full participants table plus a three-class Mermaid diagram showing only `Repository`, `Entity`, `Schema`.

#### DO NOT

- Use ASCII art (e.g. `Controller -> Service -> Repository`) in place of a Mermaid sequence diagram.

  **Example (fail):** `### Flow` body is the line `Controller -> Service -> Repository -> Mongo` with no fenced Mermaid block — the implementation skill cannot parse the call order.

- Replace **Participants** with a paragraph of prose like "The mechanism involves the controller, the service, and the repository."

  **Example (fail):** `### Participants` body is one sentence; no table, no diagram. The reader has no idea which layer each participant lives in.

- Mix Mermaid syntax with non-Mermaid (e.g. PlantUML) inside the same fenced block.

  **Example (fail):** A fence opens with `\`\`\`mermaid` but the body uses `@startuml`/`@enduml` syntax — neither renderer will accept it.

**Source:** Practice-skill authoring convention (abd-architecture-template); the Mermaid diagrams are how the downstream implementation skill renders timing and structure from this document.
