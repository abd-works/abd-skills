# Rule: Outline leads with system context diagram

The outline answers "what is this system?" through the system context diagram first and prose second. The first numbered section of `architecture-outline.md` is the **system context diagram**, followed by the mechanisms and principles sections. Failing means the document opens with paragraphs of prose before the diagram appears, has no diagram, or has a caption that runs to half a page.

## DO

- The first numbered section of `architecture-outline.md` is `## 1. System Context`. Sections 2+ are mechanisms, principles, tech stack, systems, ADRs.

  **Example (pass):** `architecture-outline.md` heading 1 is exactly `## 1. System Context`. Section 2 is `## 2. Architecture Mechanisms`.

- The system context diagram caption is three sentences or fewer and names what the reader should see.

  **Example (pass):** Caption: "PawPlace connects three actors — Pet Owners, Vets, and Admins — to the core platform over HTTPS. Two external systems integrate: Auth0 for identity and Stripe for payments. All synchronous calls use REST; async notifications use AMQP."

- The diagram uses a `.drawio` source paired with an exported PNG referenced in the outline.

  **Example (pass):** Section 1 embeds `![System Context](./diagrams/system-context.png)` with a link to `system-context.drawio` and `system-context-elements.md`.

## DO NOT

- Open the outline with a prose-only section before the system context diagram appears.

  **Example (fail):** Section 1 is `## Introduction` with five paragraphs of project history. The diagram does not appear until section 4.

- Include a layered architecture, platform architecture, or deployment topology diagram in the outline. Those live in the blueprint.

  **Example (fail):** Outline has `## 1. Layered Architecture` and `## 2. System Context`. The layered diagram is blueprint-level content and does not belong at this level.

- Caption the diagram with a multi-paragraph rationale.

  **Example (fail):** System context caption is six paragraphs explaining why a microservices split was chosen. That rationale belongs in an ADR, not the caption.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the outline is "the one-page picture of the system" and the system context diagram is its load-bearing content.
