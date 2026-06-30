# Rule: Cross-cutting concerns are named as typed architecture mechanisms

Every cross-cutting concern the system commits to appears in the blueprint as a **typed, named architecture mechanism** with its own subsection under section 3. The standard mechanism vocabulary covers Security, Error Handling & Resilience, Logging & Observability, Validation, Configuration, Caching, Communication, and Persistence; projects may add or rename mechanisms as needed but each must be a named subsection. Failing means a cross-cutting concern exists in code but has no blueprint section, two unrelated concerns are merged into one subsection, or a section title is generic ("Other patterns", "Implementation notes") instead of naming the mechanism.

## DO

- Give every committed cross-cutting concern its own `### 3.X {Mechanism Name}` subsection inside section 3.

  **Example (pass):**

  ```
  ## 3. Architecture Mechanisms
  ### 3.1 Security
  ### 3.2 Error Handling & Resilience
  ### 3.3 Logging & Observability
  ### 3.4 Validation
  ### 3.5 Configuration
  ### 3.6 Caching
  ### 3.7 Persistence
  ```

- Describe each mechanism in 1–2 paragraphs: what concern it addresses, which components depend on it, how they interact with it; then explicitly defer deep walkthroughs to the reference.

  **Example (pass):** "Caching — Catalogue data is cached in Redis with a write-through pattern; admin writes invalidate the keys they touch. Identity data is cached at the API edge with a 60-second TTL. *See the Caching mechanism's `architecture-context.md` for the full cache-key convention and invalidation strategy.*"

- Add project-specific mechanisms when the canonical list does not cover something material (e.g. **Multi-tenancy Isolation**, **Game Bridge Seam**, **GPU Workload Dispatch**).

  **Example (pass):** A WPF/COH project blueprint with a `### 3.8 COH Game Bridge Seam` subsection — same shape as the standard ones.

## DO NOT

- Fold security and validation together under a single "Cross-cutting" heading.

  **Example (fail):** Section 3 has one subsection called "Cross-cutting concerns" with five paragraphs that drift across auth, error handling, logging, and validation. Readers cannot find the security mechanism without scanning.

- Use a generic subsection title like "Patterns" or "Implementation notes" instead of naming the mechanism.

  **Example (fail):** `### 3.4 Implementation patterns` with content that is in fact about logging and observability. Rename to `### 3.4 Logging & Observability`.

- Drop a mechanism into the document as a single sentence because "we'll fill it in later".

  **Example (fail):** "### 3.5 Configuration. TBD." Either describe the mechanism in 1–2 paragraphs, omit the section because the concern is not yet a real commitment, or call out the deferral in writing with a reason.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); each mechanism named here becomes a mechanism-tier `architecture-context.md` (and a one-line entry in the central spec) under `abd-architecture-specification`.
