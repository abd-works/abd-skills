---
name: abd-architecture-reference
description: >-
  Produce an architecture reference document for a specified architecture —
  one mechanism (e.g. error handling, caching, persistence, auth) at a time —
  so a downstream implementation skill can build code that matches. Each
  mechanism section names its principles and patterns, draws participants as
  a class diagram, flows through a sequence diagram plus a step-by-step
  walkthrough, shows file structure, gives example code that follows the
  project's coding standards (defaulting to abd-clean-code when it is in
  scope) and test snippets that follow the project's testing standards
  (defaulting to abd-acceptance-test-driven-development when it is in
  scope), and explains how the mechanism is tested. Use this skill when you have a layered architecture from
  abd-architecture-description and a list of mechanisms from
  abd-architecture-mechanisms, and you need the reference document the
  implementation skill (built by abd-build-architecture-skill) will consume.
---
# abd-architecture-reference

## Purpose

Architecture decisions usually live in someone's head, a deck, or a wiki page that nobody opens twice. This skill packages those decisions into a **single reference document** for the chosen architecture so that any team member can implement the same mechanism the same way the next person did, and the one after that. The reference is the contract: it names the principles the architecture refuses to break, fixes the patterns that satisfy them, draws the participants, shows the flow, and gives code samples a reviewer can compare against. When the reference is done, "how do we do caching here?" has one answer, "where does error handling live?" has one answer, and the team stops re-litigating those questions every sprint.

## When to use this skill

Load this skill when **any** of the following apply:

- A team needs **one canonical answer** for a mechanism such as error handling, caching, persistence, authentication, validation, messaging, or observability — instead of three competing patterns scattered across the codebase.
- A new architecture is being adopted (MERN, hexagonal, event-driven, layered Python, Clean Architecture, microservices) and you want to **lock both the design and implementation constraints / guidance** before any production code is written.
- An existing system has drifted; two recent features solved the same cross-cutting concern in two different ways, and the team wants to **agree on one**.
- A new engineer joining the project keeps asking "where does X live and what shape does it take?" and you want a **single document** to point at instead of pairing on the same answer every time.
- A code review keeps surfacing the same "this isn't how we do it here" comments, and the team wants those expectations **written down** so they apply before review, not during.
- You are documenting the architecture **as it actually is** in a working system so future changes can stay consistent with what already shipped.

---

## Agent Instructions

1. **Gather the architecture context first.** Before drafting anything, make sure you have two pieces of context in front of you:

   - A **layered description** of the target architecture — the set of layers it uses (presentation, application, domain, infrastructure, or whatever names this architecture chooses), the tech that sits in each, and what each layer is responsible for.
   - A **list of mechanisms** to cover, each with a one-line statement of intent (what error handling is *for* in this architecture, what caching is for, what authorization is for, and so on).

   That context might come from a prior decision document, an ADR, a wiki page, a slide deck, an existing reference in another repo, a working system you are documenting after the fact, or — when present — sibling skills that produce these outputs. The format of the source does not matter; the two pieces of information do. If either piece is missing, stop and gather it before generating the reference. Invented layers and ad-hoc mechanism lists are the failure modes this step prevents.

   For shape and tone, the filled illustrative example block at the bottom of [`templates/architecture-reference.md`](templates/architecture-reference.md) is a worked example of what one mechanism section should look like when complete. Read it once before generating new sections.

2. **Choose how mechanisms are sectioned inside the file.** The reference is **always a single file** (`architecture-reference.md`). The only choice is how the mechanisms inside it are organized.
   - **Combined section** — when the reference covers only **2–3 mechanisms** and they are tightly related (e.g. error handling + retries, caching + memoization, auth + authorization), use **one `## Mechanisms` section** that covers them together, weaving the five-part shape (Principles & Patterns, File Structure, Participants, Flow, Walkthrough Example) across all of them.
   - **One section per mechanism** (the default for 4+ mechanisms, and always allowed) — each mechanism gets its own `## Mechanism: <Name>` section with the five-part shape as `###` subsections.
   The user may override either way; honour an explicit choice.

3. **Template.** Always produce one file from the single template:

   | Template | What to produce |
   | --- | --- |
   | `templates/architecture-reference.md` | The whole reference file — title, TOC, Architecture Layers, the mechanisms (combined or per-mechanism, depending on count), Testing Architecture, References. The template carries both section modes inline; choose the one that matches your mechanism count and delete the other. The template also includes a filled illustrative example block at the bottom — mirror it for tone and depth, then delete it before shipping. |

4. **Code and test examples follow whatever standards the project has agreed.** Any production-code sample in a mechanism section must follow the **coding standard in scope for the project** — a style guide, a clean-code skill, an ESLint config, a `CLAUDE.md` block, whatever the team has agreed. Any test snippet must follow the **testing standard in scope for the project** — a testing skill, a test-style guide, the team's existing test patterns. When the project is using **abd-clean-code** and **abd-acceptance-test-driven-development**, those *are* the standards; default to them. When the project uses something else (project-specific guide, language-idiomatic style, a corporate standard), use that instead. Cite whichever standards apply at the bottom of each mechanism section so a reviewer can find them.

5. **Rules.** Generate content following the rules attached to this skill (bundled below). After writing, take on the role of a *Peer Reviewer* and walk each rule's **DO** / **DO NOT** / **Examples** against the produced document. Be strict.


---

## Core concepts

### Architecture Reference?

An **architecture reference** details one or more cross-cutting mechanisms the system needs and defines how that mechanism is realized across the architecture's layers. "Mechanism" is the verbed concern — *how the architecture handles errors*, *how it caches*, *how it persists*, *how it authorizes*, *how it observes*. A reference is the design and working implementaton of one or more mechanisms, saying which layers participate and what each one does.

A finished reference lets a reviewer answer three questions in one read:

- **What is the principle?** — the one-line rule that, if you violated it, your code would no longer be "in this architecture" (e.g., "domain layer never imports from infrastructure", "errors raised at the boundary, never swallowed mid-pipeline").
- **What is the pattern?** — the named, repeatable shape that implements the principle (Repository, Result-or-throw, Side-car Cache, Saga, Outbox, Specification, Resource owner, etc.).
- **How does it actually run?** — the participants, the file layout, the call sequence, and the test approach, so an implementer can recognize the pattern in code on sight.

### Mechanism

A **mechanism** is one cross-cutting concern the architecture has a fixed answer for: error handling, caching, persistence, authentication, authorization, validation, messaging, logging, observability, configuration, feature flags, idempotency, transactions, rate limiting. Mechanisms come from the **abd-architecture-mechanisms** output. The reference document devotes one section (or file) to each mechanism the project has actually decided.

### Principle vs. pattern

A **principle** is a one-liner stance the architecture takes — a constraint the team is not allowed to break. It is technology-agnostic, fits in a sentence, and survives in a corridor conversation. Examples: "Domain First", "Micro Front-End / Micro-Service Alignment", "Event-Based Orchestration for Cross-Domain Service Calls", "MVVM in the presentation layer", "REST for synchronous API boundaries". One principle can be satisfied by many different patterns.

A **pattern** is the full description of how the team has chosen to satisfy that principle in this project: the named shape, its structural options, its benefits, and its trade-offs. Patterns are concrete and have a name the team can use in a pull-request comment ("use the Result pattern here", "this violates the side-car cache pattern"). A mechanism section names the pattern the team has committed to and explains *why that pattern over the alternatives* — that trade-off reasoning is what makes the reference trustworthy rather than just a style guide.

### Layered description vs. mechanism reference

**abd-architecture-description** answers *what are the layers and what tech sits in each*. **This skill** answers *for each mechanism, which of those layers participate and in what order*. The layered description is the map; the mechanism reference is the route through that map for one concern.

### Sections inside one mechanism

Every mechanism section, whether it lives in a single document or its own file, has the same five-part shape so the document reads predictably:

1. **Principles & Patterns** — one-liner principle(s) stating the architectural stance, followed by a named pattern description per principle that covers the chosen shape, its options, its benefits, and its trade-offs.
2. **File Structure** — where the mechanism's code lives in the project's folder layout (a fenced tree).
3. **Participants** — the classes / modules involved, presented as a class diagram (Mermaid or Markdown table). This is the *who*.
4. **Flow** — a sequence diagram (Mermaid) of one representative scenario. This is the *when*.
5. **Walkthrough Example** — a step-by-step narration of the same scenario through the participants, plus example production code that follows the project's coding standard and a test snippet that follows the project's testing standard. This is the *how*.

A short **Testing the mechanism** subsection at the end of each mechanism (or one consolidated **Testing Architecture** section after the combined mechanisms block) explains which of the project's test tiers owns the verification and which test doubles or helpers are used. The tier names come from whatever the project has agreed (e.g. Domain / ViewModel+Domain / E2E / Game Bridge for WPF; Server / Client / E2E for MERN; Unit / Integration / E2E for most web stacks). The Testing Architecture section is the canonical definition of those tiers for this project.

### Section organization

The reference is **always one file**: `architecture-reference.md`. What changes with mechanism count is how the mechanisms are sectioned **inside** that file.

- **Combined section** — when there are only **2–3 mechanisms** and they are tightly related, the reference can use **one `## Mechanisms` section** that weaves the five-part shape across all of them. Smaller systems and tightly-coupled concerns benefit from this — fewer headings to maintain.
- **One section per mechanism** — the default for **4+ mechanisms**, and always allowed. Each mechanism gets its own `## Mechanism: <Name>` section with the five-part shape as `###` subsections.

Either way, the five-part shape is preserved so a downstream implementation skill (or a human reviewer) can find every part of every mechanism consistently.

### Sections and rules

**`SKILL.md`** carries teaching and workflow order. **`rules/*.md`** validate the **produced reference document** — required sections, diagram presence, code style sources, TOC, layout choice — independently of the skill's narrative.

---

## Example

For an architecture with layers **Presentation / Application / Domain / Infrastructure** and mechanisms **Error Handling, Caching, Persistence**, the single-document reference reads:

```
# <ArchitectureName> Architecture Reference

## Table of Contents
- Overview
- Architecture Layers (from abd-architecture-description)
- Mechanism: Error Handling
- Mechanism: Caching
- Mechanism: Persistence
- Testing Architecture
- References

## Overview
One paragraph: name the architecture, name the four guiding principles,
name the three mechanisms covered.

## Architecture Layers
Reuse the layer block from abd-architecture-description verbatim.

## Mechanism: Error Handling
### Principles & Patterns
- Principle: errors raised at the boundary, never swallowed.
- Pattern: Result<T, DomainException> from application services;
  controller maps to HTTP status.
### File Structure
packages/<domain>/shared/Errors.ts
packages/<domain>/server/error-mapper.ts
### Participants  (class diagram)
[Mermaid classDiagram]
### Flow  (sequence diagram)
[Mermaid sequenceDiagram]
### Walkthrough Example
1. Repository fails to parse a Mongo doc...
2. Service catches with .mapErr(...)
3. Controller maps DomainException -> 422
   (code sample follows the project's coding standard)
   (test sample follows the project's testing standard)
### Testing the mechanism
- Domain tier: every application-service method has one failure scenario.
- ViewModel tier: form displays the mapped error message.

## Mechanism: Caching
... same shape ...
```

For more than five mechanisms, the same content splits into `mechanisms/error-handling.md`, `mechanisms/caching.md`, etc., and `architecture-reference.md` becomes a table of contents with one-line summaries and links.

---

## The shape of a good mechanism section

```
## Mechanism: <Name>

### Principles & Patterns
- Principle: <one sentence the architecture refuses to break>
- Pattern: <named, repeatable shape that satisfies the principle>

### File Structure
<fenced folder tree showing where this mechanism's code lives>

### Participants
<Mermaid classDiagram OR a Markdown table>
| Class / Module | Layer | Responsibility | Collaborators |

### Flow
<Mermaid sequenceDiagram for ONE representative scenario>

### Walkthrough Example
1. <step naming participant>
2. <step naming participant>
...
```code (follows the project's coding standard)```
```test (follows the project's testing standard)```

### Testing the mechanism
- Tier: <project's tier name — e.g. Domain / ViewModel+Domain for WPF, Server / Client for MERN, Unit / Integration for web stacks>
- Doubles / helpers: <which test doubles or Given/When/Then helpers verify it>
```

Each mechanism section must be self-contained: a reader who jumps directly to it (via the TOC or a deep link) has enough to implement that mechanism without flipping back to other sections.

---

## Build

**Goal:** Produce a reference document for one architecture that any implementer can read once and reproduce.

- **Outputs:** A single file at `inputs/architecture-reference.md` in the target project's skill or repository (not under this skill).
- **Per format:** The file always includes a Table of Contents. Mechanisms are organized inside the file in one of the two modes (combined section, or one section per mechanism) per the section-organization rule.
- **While writing:** Every mechanism (whether in a combined section or its own section) follows the five-part shape — Principles & Patterns, File Structure, Participants, Flow, Walkthrough Example — plus a Testing subsection. Code in walkthroughs follows the project's coding standard; test snippets follow the project's testing standard.

**Build steps:**

1. **Load the layered description.** Take the layer set you gathered in *Agent Instructions step 1* and copy or summarize the layer block faithfully into the reference's *Architecture Layers* section. Cite whatever source it came from (ADR number, wiki page, sibling-skill output) so a reviewer can trace the names back.

2. **Load the mechanism list.** Take the mechanisms and their intents you gathered in *Agent Instructions step 1*. Each entry becomes one section (or one file) in the reference. If a mechanism the project actually needs is missing from the list, do not invent it here — pause, agree the mechanism upstream wherever the source of truth lives, then come back.

3. **Decide section organization.** Count mechanisms. **2–3** tightly-related mechanisms → one combined `## Mechanisms` section that weaves the five-part shape across them. **4+ mechanisms (or any non-tightly-related set)** → one `## Mechanism: <Name>` section per mechanism, each with the five-part shape as `###` subsections. Use `templates/architecture-reference.md` either way — it carries both modes inline; delete the one you do not pick. Honour an explicit user override.

4. **Author each mechanism** using the five-part shape. State the **principle in one sentence** (the stance the architecture takes; technology-agnostic). Describe the **pattern** in full — name it, lay out any options, state the benefits and the trade-offs so a reviewer knows *why this pattern over the alternatives*. Draw the participants as a Mermaid `classDiagram` (or a participants table when a diagram is overkill), draw the flow as a Mermaid `sequenceDiagram`, walk one scenario step-by-step, and include a code sample and a test snippet that obey the project's coding standard and testing standard (defaulting to **abd-clean-code** and **abd-acceptance-test-driven-development** when those are in scope).

5. **Add a Testing Architecture section.** Either a short Testing subsection per mechanism (per-mechanism mode) or one consolidated Testing Architecture section after the combined block (combined mode) explaining which tier verifies each mechanism and which helper pattern is used.

6. **Insert the Table of Contents.** Always required at the top of `architecture-reference.md`, with anchor links to every H2 (Overview, Architecture Layers, Mechanism: \<Name\> or Mechanisms, Testing Architecture, References).

7. **Peer-review against bundled rules.** Walk the rules block at the bottom of this file against the produced document and fix violations.

8. **Bundle.** After any change to `rules/*.md`, run:

   ```bash
   python skills/skill-builder/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root skills/engineering/abd-architecture-reference
   ```

---

## Validate

**Goal:** Inspect the produced reference document as a reviewer — not as a second author.

- **Who is checking:** Software Architect (layer assignments, principle phrasing), Tech Lead (pattern names are real and match team vocabulary), Domain Expert (mechanism intent matches actual product needs), Engineer-About-To-Implement (every section is implementable from the file alone).
- **Cross-artifact parity:** Layers and mechanism names in the reference match exactly the architecture's agreed source of truth (ADR, wiki, decision doc, or sibling-skill output, whichever the team uses).

Walk the checklist against the produced document:

- **Required sections** — every mechanism (whether in a combined section or its own section) has Principles & Patterns, File Structure, Participants (class diagram or table), Flow (sequence diagram), Walkthrough Example, and a Testing subsection.
- **TOC** — the file opens with a Table of Contents whose anchor links reach every H2 in the document.
- **Diagrams present** — every mechanism has a class diagram (Mermaid `classDiagram` or a Markdown participants table) AND a sequence diagram (Mermaid `sequenceDiagram`).
- **Walkthroughs are step-numbered** — not prose paragraphs. Each step names the participant doing the work.
- **Code follows the project's coding standard** — whichever guide is in scope (defaulting to `abd-clean-code` when present): no `Manager`, `Handler`, `Service` (in the anemic sense), no swallowed exceptions, no anemic data bags. Domain entities carry behaviour.
- **Tests follow the project's testing standard** — whichever guide is in scope (defaulting to `abd-acceptance-test-driven-development` when present): Given / When / Then helpers; no defensive checks; story-driven names.
- **Grounded in source of truth** — layer names and mechanism names match the architecture's source of truth (ADR, wiki, sibling-skill output, etc.); the source is cited.
- **Section organization matches mechanism count** — 2–3 tightly-related mechanisms may share one combined `## Mechanisms` section; 4+ → one `## Mechanism: <Name>` section each. Any override is noted at the top of the file.
- **Self-contained mechanisms** — a reader who jumps directly to one mechanism (via the TOC) has enough to implement it without scrolling away.

---

<!-- execute_rules:bundle_rules:begin -->
##### Rule: Code examples follow the project's coding and testing standards

Every code block inside a `Walkthrough Example` must obey the **coding standard the project has agreed** for production code and the **testing standard the project has agreed** for test code. The reference document does not invent style — it inherits the team's existing guide. When the project uses **abd-clean-code** and **abd-acceptance-test-driven-development**, those are the standards and the samples must follow them. When the project uses a different style guide, project-specific patterns, or a corporate standard, the samples must follow *that*. The reference cites whichever standards apply at the bottom of each mechanism section so a reviewer can find them. Passing means a snippet would survive review under the standard the project actually uses. Failing means a snippet violates the chosen standard, contradicts an in-scope guide, or invents conventions that do not match any agreed source.

###### DO

- Identify the **coding standard in scope** before writing the production-code sample. In an agilebydesign-skills-anchored project this is usually `abd-clean-code` (domain language, small functions, constructor injection, no anemic data bags); in another project it may be a different guide.

  **Example (pass):** The project's `agents/coding-standards.md` says "no service-with-anemic-bag patterns" and the project loads `abd-clean-code`. The Walkthrough Example ships an `InvoiceService` that delegates to entity methods on `Invoice` — no `Manager`, no `process()`, dependencies in the constructor.

- Identify the **testing standard in scope** before writing the test snippet. Default is `abd-acceptance-test-driven-development` (class per story, method per scenario, Given/When/Then helpers, no defensive checks) when the project has it in scope.

  **Example (pass):**
  ```typescript
  class TestInvoiceCreationFailures {
    helper = new InvoiceServerHelper();
    async test_invalid_invoice_returns_422_with_validation_message() {
      await this.helper.givenUserLoggedIn();
      await this.helper.whenUserSubmitsInvoiceWithMissingAmount();
      await this.helper.thenResponseIs422WithMessage('amount is required');
    }
  }
  ```

- Cite the standards used at the bottom of the mechanism section so the reader can find them.

  **Example (pass):** End-of-mechanism line: `Code follows the project's coding standard (abd-clean-code in scope here); tests follow the project's testing standard (abd-acceptance-test-driven-development in scope here).`

- If the project's standard differs from the agilebydesign defaults, **say so explicitly** at the top of the reference so readers know which guide the samples obey.

  **Example (pass):** Below the title: `> Coding standard: company-python-style.md. Testing standard: in-house pytest patterns.`

###### DO NOT

- Ship a code sample that violates the in-scope standard because "this is just an illustration".

  **Example (fail):** Project uses `abd-clean-code`; the sample is
  ```typescript
  export class RecipientManager {
    process(data: any) { /* ... */ }
  }
  ```
  — `Manager` class, `process` method, `any` parameter, no constructor dependencies. Whatever the project's standard is, this violates a clean-code guide.

- Ship a test snippet with defensive `try/catch` or branching assertions when the project's testing standard forbids them.

  **Example (fail):**
  ```typescript
  try {
    const r = await svc.createInvoice(input);
    if (r.ok) expect(r.value).toBeDefined();
  } catch (e) { /* ignore */ }
  ```
  — defensive try, conditional assertion, swallowed exception. Violates `abd-acceptance-test-driven-development` (and any sensible testing guide).

- Pick conventions out of thin air when the project has no documented standard yet.

  **Example (fail):** The project has no coding-standards document and no clean-code skill. The reference's samples use a `Service` + anemic `Recipient` interface and rationalize it as "industry standard". The team has no way to peer-review against an agreed source — pause and agree a coding standard before authoring code samples.

**Source:** Practice-skill authoring convention (abd-architecture-reference). The reference document inherits the team's existing code-style and test-style decisions rather than imposing new ones.

##### Rule: Reference is grounded in abd-architecture-description and abd-architecture-mechanisms

The **layer names** in the reference document must match the output of **abd-architecture-description** for the same architecture, and the **mechanism names** must match the output of **abd-architecture-mechanisms**. The reference document is the join of those two skills; it does not invent layers, rename them, or add mechanisms the mechanisms skill never listed. When the reference needs a layer or mechanism that the upstream skills do not contain, the upstream skill is updated first and the reference is regenerated. Passing means a reviewer can hold the abd-architecture-description output, the abd-architecture-mechanisms output, and the reference side-by-side and see the same vocabulary in all three. Failing means the reference uses a synonym (`Persistence layer` vs `Infrastructure`), drops a layer, or introduces a mechanism that nobody else has heard of.

###### DO

- Copy or summarize the layer block from **abd-architecture-description** into the **Architecture Layers** section of the reference, keeping layer names byte-for-byte identical.

  **Example (pass):** `abd-architecture-description` names four layers `Presentation`, `Interface Adapters`, `Application`, `Domain Core`, `Infrastructure`. The reference's `Architecture Layers` section lists the same five names in the same order.

- For each mechanism, cite the **abd-architecture-mechanisms** entry that it implements, near the mechanism heading.

  **Example (pass):** `## Mechanism: Caching` is followed by the line `> Source intent: abd-architecture-mechanisms entry for Caching.`

- When a mechanism is missing from **abd-architecture-mechanisms**, **stop and add it there first** before adding it to the reference.

  **Example (pass):** The team realizes `Idempotency` is needed; the reference author updates `abd-architecture-mechanisms` first, regenerates its output, then adds the `Idempotency` section to the reference.

###### DO NOT

- Rename a layer to suit the mechanism (e.g. call it `Storage` in the caching section and `Infrastructure` in the persistence section).

  **Example (fail):** Mechanism `Caching` describes a `Storage layer` while `Persistence` describes an `Infrastructure layer` — same code lives in the same folder; the reference invented two names.

- Add a mechanism that does not appear in **abd-architecture-mechanisms**.

  **Example (fail):** The reference includes `Mechanism: Multi-tenancy` but the `abd-architecture-mechanisms` output for this architecture has no Multi-tenancy entry — the reference has gone off-piste.

- Reorder or merge layers in a way that contradicts **abd-architecture-description**.

  **Example (fail):** `abd-architecture-description` lists `Domain Core` between `Application` and `Infrastructure`; the reference puts `Domain Core` at the top and merges `Application` into `Interface Adapters`.

**Source:** Practice-skill authoring convention (abd-architecture-reference); preserves the contract with **abd-architecture-description** and **abd-architecture-mechanisms** that downstream tooling depends on.

##### Rule: Include class and sequence diagrams for every mechanism

Every mechanism must show its **participants** as either a Mermaid `classDiagram` block **or** a Markdown participants table (Class / Layer / Responsibility / Collaborators), and must show its **flow** as a Mermaid `sequenceDiagram` block. The flow diagram is mandatory because the implementation skill renders timing from it. The class view may be a table when the relationships are simple enough that a diagram adds no signal, but the **classes-and-layers information must be present** in some structured form — never just a paragraph of prose. Passing means a reader who only opens the Participants block and the Flow block already knows who the actors are and the order of calls. Failing means either block is missing, both are prose, or the sequence diagram is an ASCII sketch rather than Mermaid.

###### DO

- Use ` ```mermaid\nsequenceDiagram\n... ``` ` for the **Flow** section. Mermaid is required so downstream tools can render it.

  **Example (pass):** `### Flow` is followed by a fenced block starting with `\`\`\`mermaid\nsequenceDiagram\n    participant Controller\n    Controller->>Service: createInvoice(input)`.

- For **Participants**, use either ` ```mermaid\nclassDiagram\n...``` ` **or** a four-column Markdown table with headers `Class / Module | Layer | Responsibility | Collaborators` (or both).

  **Example (pass):** `### Participants` contains a Markdown table listing `CachingRecipientsRepository | Infrastructure | LRU + TTL side-car | MongoRecipientsRepository`.

- When a mechanism has more than five participants, **prefer the table** for readability and add a small Mermaid class diagram only for the central trio.

  **Example (pass):** A `Persistence` mechanism with eight classes ships a full participants table plus a three-class Mermaid diagram showing only `Repository`, `Entity`, `Schema`.

###### DO NOT

- Use ASCII art (e.g. `Controller -> Service -> Repository`) in place of a Mermaid sequence diagram.

  **Example (fail):** `### Flow` body is the line `Controller -> Service -> Repository -> Mongo` with no fenced Mermaid block — the implementation skill cannot parse the call order.

- Replace **Participants** with a paragraph of prose like "The mechanism involves the controller, the service, and the repository."

  **Example (fail):** `### Participants` body is one sentence; no table, no diagram. The reader has no idea which layer each participant lives in.

- Mix Mermaid syntax with non-Mermaid (e.g. PlantUML) inside the same fenced block.

  **Example (fail):** A fence opens with `\`\`\`mermaid` but the body uses `@startuml`/`@enduml` syntax — neither renderer will accept it.

**Source:** Practice-skill authoring convention (abd-architecture-reference); the Mermaid diagrams are how the downstream implementation skill renders timing and structure from this document.

##### Rule: Reference document includes a Table of Contents

A reference is no use if a reviewer cannot jump to the mechanism they need. `architecture-reference.md` must begin with a `## Table of Contents` immediately after the title, listing **Overview**, **Architecture Layers**, the mechanisms section(s) (a single **Mechanisms** entry in combined mode, or every **Mechanism: \<Name\>** as a sub-bullet in per-mechanism mode), **Testing Architecture**, and **References**, with anchor links to the corresponding headings. Passing means a reviewer who opens the file can reach any mechanism in one click. Failing means the file opens with the `Overview` and no navigation block, or the TOC is a wall of unlinked plain text.

###### DO

- Place `## Table of Contents` immediately under the H1 title, with anchor links for every H2 in the document.

  **Example (pass):**
  ```markdown
  # Sample Architecture Reference

  ## Table of Contents
  - [Overview](#overview)
  - [Architecture Layers](#architecture-layers)
  - [Mechanism: Error Handling](#mechanism-error-handling)
  - [Mechanism: Caching](#mechanism-caching)
  - [Mechanism: Persistence](#mechanism-persistence)
  - [Testing Architecture](#testing-architecture)
  - [References](#references)
  ```

- In combined-section mode, link to the single `## Mechanisms` H2 and (optionally) to each mechanism's `###` heading within it.

  **Example (pass):**
  ```markdown
  ## Table of Contents
  - [Overview](#overview)
  - [Architecture Layers](#architecture-layers)
  - [Mechanisms](#mechanisms)
    - [Error Handling](#error-handling)
    - [Retries](#retries)
    - [Idempotency](#idempotency)
  - [Testing Architecture](#testing-architecture)
  - [References](#references)
  ```

- Keep anchor IDs in sync with heading text after edits (rename a mechanism → update the TOC link).

  **Example (pass):** Renaming `Mechanism: Persistence` to `Mechanism: Data Persistence` also updates the TOC entry and anchor `#mechanism-data-persistence`.

###### DO NOT

- Open the document with `## Overview` and jump straight into prose with no navigation block.

  **Example (fail):** Reference has H1 then `## Overview` then mechanism sections; no TOC anywhere. Reviewers must scroll to find anything.

- Use a TOC of plain text (no anchor links) so clicking does nothing.

  **Example (fail):**
  ```markdown
  ## Table of Contents
  - Overview
  - Architecture Layers
  - Mechanism: Caching
  ```
  No `[label](#anchor)` syntax — useless on rendered Markdown.

- Leave stale TOC entries pointing at deleted mechanisms.

  **Example (fail):** `Mechanism: Messaging` was removed from the document; the TOC still has a link to `#mechanism-messaging` that 404s the reader.

**Source:** Practice-skill authoring convention (abd-architecture-reference).

##### Rule: Mechanism section has all five parts

Every mechanism in the produced reference document must contain the **same five-part shape** so the implementation skill can generalize across mechanisms. The five parts are **Principles & Patterns**, **File Structure**, **Participants** (class diagram or table), **Flow** (sequence diagram), and **Walkthrough Example**, followed by a **Testing the Mechanism** subsection. A reviewer should be able to land on any one mechanism and find every part without scrolling away. Passing means each mechanism reads as a self-contained recipe. Failing means a mechanism is missing a part, or parts are merged into prose that hides whether the structure is there.

###### DO

- Give **every** mechanism the heading sequence `Principles & Patterns`, `File Structure`, `Participants`, `Flow`, `Walkthrough Example`, `Testing the Mechanism` (in that order).

  **Example (pass):** `## Mechanism: Caching` is followed by `### Principles & Patterns`, `### File Structure`, `### Participants`, `### Flow`, `### Walkthrough Example`, `### Testing the Mechanism` in that exact order.

- Use **fenced code blocks** for the **File Structure** tree so it renders as a tree, not as prose with slashes.

- Make each mechanism section **self-contained**: someone arriving via deep link can implement it without reading other mechanisms.

- In `### Testing the Mechanism`, state which tier tests this mechanism and which test doubles / mocks are used. Cross-reference `## Testing Architecture` for full examples but do not duplicate them inline.

  **Example (pass):** `### Testing the Mechanism` says "Domain tier — inject `Mock<IPaymentGateway>` via constructor; assert `gateway.Charge()` called once. See Testing Architecture for the `[AssemblyInitialize]` wiring."

###### DO NOT

- Create a standalone **`## Mechanism: Test Tiers`** or **`## Mechanism: Test Strategy`** or any mechanism whose entire purpose is describing how tests are organised. That content belongs in `## Testing Architecture`, not in a mechanism section. Mechanisms are cross-cutting concerns of the production architecture (error handling, caching, auth, game bridge seam, etc.).

  **Example (fail):** `## Mechanism: Test Tiers` with Principles & Patterns describing Tier 1 vs Tier 2 isolation. This is a testing strategy, not an architecture mechanism.

- Merge `Participants` and `Flow` into a single prose paragraph that mentions classes and sequence in the same sentence.

  **Example (fail):** `### How it works: the controller calls the service, which calls the repository...` with no class table, no class diagram, and no sequence diagram.

- Skip `### Testing the Mechanism` because "testing is covered in the Testing Architecture section."

  **Example (fail):** Mechanism `Authorization` ends after `Walkthrough Example` with no testing sub-section. The reader has no idea which tier owns the verification or which helper to extend.

- Reorder the parts so that, for example, `Walkthrough Example` comes before `Participants`.

**Source:** Practice-skill authoring convention (abd-architecture-reference). The five-part shape is the contract between this skill and `abd-build-architecture-skill`.

##### Rule: Section organization matches mechanism count

The reference is **always one file** (`architecture-reference.md`). What varies is how the mechanisms inside that file are organized — and the choice is **decidable from the mechanism count**, not author taste. With **2–3 mechanisms that are tightly related**, the reference can use **one combined `## Mechanisms` section** that weaves the five-part shape (Principles & Patterns, File Structure, Participants, Flow, Walkthrough Example) across all of them. With **4+ mechanisms** (or any set whose mechanisms are not tightly related), each mechanism gets its own `## Mechanism: <Name>` section with the five-part shape as `###` subsections. The rule has one explicit override: if the user (or an enclosing skill) **states a section organization**, that choice wins and the reference includes a one-line note at the top saying so. Passing means the organization matches the count, or the override is documented. Failing means the file splits into multiple files, or a 10-mechanism architecture is crammed into one combined section, or the five-part shape is dropped to "save space".

###### DO

- Count the mechanisms first; pick the section organization from the count using the rule above. Always produce one file at `inputs/architecture-reference.md`.

  **Example (pass):** Three tightly-related mechanisms (`Error Handling`, `Retries`, `Idempotency`) → one `## Mechanisms` section in `architecture-reference.md` that weaves Principles & Patterns, File Structure, Participants, Flow, and a Walkthrough across all three.

- For 4+ mechanisms (or non-tightly-related sets), give each mechanism its own `## Mechanism: <Name>` H2 with the five-part shape as `###` subsections.

  **Example (pass):** Six mechanisms (`Error Handling`, `Caching`, `Persistence`, `Authorization`, `Validation`, `Observability`) → six H2 sections in the same `architecture-reference.md`, each with the same `### Principles & Patterns` / `### File Structure` / `### Participants` / `### Flow` / `### Walkthrough Example` / `### Testing the mechanism` shape.

- Honour an explicit user override and document it at the top of the file.

  **Example (pass):** Five mechanisms but the user asks for the combined section. Below the title: `> Organization: combined (user override; default for 5 mechanisms would be per-mechanism sections).`

###### DO NOT

- Split the reference across multiple files (e.g. a `mechanisms/` folder with `mechanisms/caching.md`, `mechanisms/error-handling.md`).

  **Example (fail):** The skill ships `architecture-reference.md` plus three files under `mechanisms/`. Multi-file is not a layout this skill produces — the contract with downstream consumers (a build skill, a reviewer) is one file.

- Cram 10 mechanisms into one combined `## Mechanisms` section to "keep it tight".

  **Example (fail):** A combined section runs 2000 lines because the author refused to give each mechanism its own H2. Readers cannot scan; the TOC cannot help.

- Drop the five-part shape to make the combined section shorter.

  **Example (fail):** The combined section has Principles & Patterns and Walkthrough but skips Participants and Flow because "the diagrams take too much space". The downstream implementation skill now has nothing to render the participants from.

**Source:** Practice-skill authoring convention (abd-architecture-reference). One-file rule keeps the contract simple for downstream consumers; section-organization rule keeps the file scannable as the mechanism set grows.

##### Rule: Walkthrough Example is numbered steps that name participants

The **Walkthrough Example** subsection must be an **ordered list** of steps, with each step naming the participant doing the work and the action taken — not a prose paragraph and not a bullet list. The walkthrough renders the same scenario as the sequence diagram, but in language a reviewer can read aloud while pointing at the diagram. Passing means a reader can pair each numbered step with a `participant` in the sequence diagram. Failing means the walkthrough is one block of paragraphs, uses unordered bullets, or describes "the system" / "the code" instead of naming a participant.

###### DO

- Start each step with the **participant name** in bold or as the subject of the sentence, then the action.

  **Example (pass):** `1. **Controller** validates the request body and calls service.createInvoice(input).`

- Match the number of steps to the messages in the sequence diagram (give or take one for the precondition / outcome).

  **Example (pass):** Sequence diagram has 5 messages; walkthrough has 5 numbered steps plus a 6th line for the user-visible outcome.

- Use an **ordered list** (`1.`, `2.`, `3.`), not an unordered list (`-`, `*`).

  **Example (pass):** Steps are numbered `1.` ... `4.` in markdown source.

###### DO NOT

- Write the walkthrough as a paragraph: "The controller calls the service which then calls the repository, and finally the response is mapped...".

  **Example (fail):** `### Walkthrough Example` body is two paragraphs with no list markers — the reviewer cannot map prose to diagram messages.

- Use the passive voice that hides the actor: "A request is received, validation is performed, and a response is sent".

  **Example (fail):** Step 1 reads "A request is received and validated." — which participant did the receiving? Which did the validating?

- Use bullets (`-`) instead of numbers; bullets imply a set, the walkthrough is a sequence.

  **Example (fail):** `- Controller receives the request` / `- Service is called` — no ordering, no alignment with the sequence diagram.

**Source:** Practice-skill authoring convention (abd-architecture-reference); numbered walkthroughs let a reviewer pair each step against the sequence-diagram message.
<!-- execute_rules:bundle_rules:end -->
