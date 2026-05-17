# Rule: Decision records are named and live on disk

Every architectural decision visible at the outline level (platform, architectural style, deployment model, major external integration) is captured as its own ADR file under `docs/architecture/decisions/ADR-NNN-{slug}.md`. The outline itself lists each ADR with a one-line consequence and a link to the file. Failing means an outline references decisions without files behind them, embeds a multi-paragraph rationale in the outline itself, or names decisions in prose without an ADR number.

## DO

- List ADRs in the outline as a table or numbered list with ID, decision, and a one-line consequence; each ID links to the actual ADR file.

  **Example (pass):**

  | ID | Decision | One-line consequence |
  |---|---|---|
  | [ADR-001](../decisions/ADR-001-spa-plus-rest-api-platform.md) | SPA + REST API platform | No server rendering, no GraphQL surface. |
  | [ADR-003](../decisions/ADR-003-aws-fargate-deployment.md) | AWS ECS Fargate, single region, multi-AZ | No Kubernetes operations cost; region failure is a DR scenario. |

- Use the `decision-record.md` template in this skill's `templates/` folder for every ADR file.

  **Example (pass):** `ADR-001-spa-plus-rest-api-platform.md` has Status / Date / Deciders / Context / Decision / Options considered / Consequences / Compliance — same shape as the template.

- Keep the ADR list in the outline to outline-level decisions only (platform, style, deployment, major external integrations).

  **Example (pass):** "How error handling is structured" is an architectural decision but a *blueprint-level* one — its ADR is listed in the blueprint, not the outline.

## DO NOT

- Embed a multi-paragraph rationale for a decision directly in the outline.

  **Example (fail):** A section 8 heading reads `## Decision Records — Why we chose AWS over Azure` followed by three paragraphs comparing services. The detail belongs in `ADR-003`, not the outline.

- Reference an ADR by name without an actual file existing under `docs/architecture/decisions/`.

  **Example (fail):** Outline lists "ADR-004: Auth0 identity" but `docs/architecture/decisions/` has no file with that ID.

- Number ADRs inconsistently or restart numbering per document.

  **Example (fail):** Outline cites `ADR-001` for the platform decision and `ADR-001` again for an unrelated networking decision in the blueprint. ADR numbers are project-wide and monotonic.

**Source:** Practice-skill authoring convention (abd-architecture-outline); ADRs are decisions-on-disk, the outline only summarises.
