### Rule: Reference document includes a Table of Contents

A reference is no use if a reviewer cannot jump to the mechanism they need. `architecture-specification.md` must begin with a `## Table of Contents` immediately after the title, listing **Overview**, **Architecture Flow**, **Instantiating the Domain**, the mechanisms section(s) (a single **Mechanisms** entry in combined mode, or every **Mechanism: \<Name\>** as a sub-bullet in per-mechanism mode), **Testing Architecture**, and **References**, with anchor links to the corresponding headings. Passing means a reviewer who opens the file can reach any mechanism in one click. Failing means the file opens with the `Overview` and no navigation block, or the TOC is a wall of unlinked plain text.

#### DO

- Place `## Table of Contents` immediately under the H1 title, with anchor links for every H2 in the document.

  **Example (pass):**
  ```markdown
  # Sample Architecture Reference

  ## Table of Contents
  - [Overview](#overview)
  - [Architecture Flow](#architecture-flow)
  - [Instantiating the Domain](#instantiating-the-domain)
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
  - [Architecture Flow](#architecture-flow)
  - [Instantiating the Domain](#instantiating-the-domain)
  - [Mechanisms](#mechanisms)
    - [Error Handling](#error-handling)
    - [Retries](#retries)
    - [Idempotency](#idempotency)
  - [Testing Architecture](#testing-architecture)
  - [References](#references)
  ```

- Keep anchor IDs in sync with heading text after edits (rename a mechanism ? update the TOC link).

  **Example (pass):** Renaming `Mechanism: Persistence` to `Mechanism: Data Persistence` also updates the TOC entry and anchor `#mechanism-data-persistence`.

#### DO NOT

- Open the document with `## Overview` and jump straight into prose with no navigation block.

  **Example (fail):** Reference has H1 then `## Overview` then mechanism sections; no TOC anywhere. Reviewers must scroll to find anything.

- Use a TOC of plain text (no anchor links) so clicking does nothing.

  **Example (fail):**
  ```markdown
  ## Table of Contents
  - Overview
  - Architecture Flow
  - Instantiating the Domain
  - Mechanism: Caching
  ```
  No `[label](#anchor)` syntax — useless on rendered Markdown.

- Leave stale TOC entries pointing at deleted mechanisms.

  **Example (fail):** `Mechanism: Messaging` was removed from the document; the TOC still has a link to `#mechanism-messaging` that 404s the reader.

**Source:** Practice-skill authoring convention (abd-architecture-specification).
