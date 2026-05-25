# Rule: Outline leads with the four diagrams

The outline answers "what is this system?" through diagrams first and prose second. The first four numbered sections of the outline document must be the **platform diagram**, the **layered architecture diagram**, the **system context diagram**, and the **deployment topology diagram**, in that order, each followed by a caption of three sentences or fewer. Failing means the document opens with paragraphs of prose, has fewer than four diagrams, reorders the four into something else, or ships a diagram with a caption that runs to half a page.

## DO

- Put the platform diagram, layered diagram, system context diagram, and deployment topology diagram as the first four numbered sections of the outline, each with its own heading.

  **Example (pass):** `architecture-outline.md` headings 1–4 are `## 1. Platform Diagram`, `## 2. Layered Architecture`, `## 3. System Context`, `## 4. Deployment Topology`. Sections 5+ are principles, tech stack, systems, ADRs.

- Limit every caption under a diagram to three sentences or fewer, naming what the reader should see.

  **Example (pass):** Layered diagram caption: "Dependencies point one way only: Presentation depends on Application, Application on Domain, Domain on Infrastructure interfaces (never their implementations). The Domain layer never imports from Infrastructure assemblies."

- Pick one diagram notation and stay consistent inside one outline (all mermaid, or all drawio links, or all PNGs).

  **Example (pass):** All four diagrams are mermaid fenced blocks. Switching is fine across outlines, not within one.

## DO NOT

- Open the outline with a prose-only "Introduction" or "Background" section before the diagrams appear.

  **Example (fail):** Section 1 of the outline is `## Introduction` with five paragraphs of history. The platform diagram does not appear until section 6.

- Ship the outline with three diagrams (e.g. missing the deployment topology) on the grounds that "we will add it later".

  **Example (fail):** Outline has Platform, Layered, and Context diagrams but no Deployment Topology — readers cannot answer "where does this run?" from the page.

- Caption a diagram with a multi-paragraph essay about the history of the choice.

  **Example (fail):** Layered diagram caption is six paragraphs explaining how we tried hexagonal first; the rationale belongs in an ADR, not the caption.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the outline is "the one-page picture of the system" and four diagrams are its load-bearing content.
