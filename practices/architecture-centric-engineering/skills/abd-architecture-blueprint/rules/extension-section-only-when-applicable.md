# Rule: Extension & Evolution section appears only when there is a real extension point

Section 6 of the blueprint (Extension & Evolution) is included **only** when the system has a *real, documented* extension seam: a named adapter contract, an extension registry, a documented plug-in mechanism, a multi-tenancy isolation boundary, or a similar concrete plug-in point. A blueprint with no such seams should **omit** the section entirely. A "TBD" or "not applicable yet" placeholder is the failing case — empty sections create noise and signal documentation drift. Failing means shipping the section with no content, listing speculative future extension ideas, or describing a feature that is not actually pluggable.

## DO

- Include section 6 only when at least one extension point exists in code, with a named contract and a registration mechanism.

  **Example (pass):** "The architecture has one documented extension seam: notification channels. New channels implement `INotificationChannel` and register through `ChannelRegistry.register()` at startup."

- Describe each extension point in one paragraph naming the contract, the registration mechanism, and where the contract is documented in detail.

  **Example (pass):** "Theme plug-ins — load JSON theme manifests at startup through `IThemeProvider`; the contract lives in the Theme mechanism's `architecture-context.md` (Class Specification → `IThemeProvider`)."

- Omit the section entirely when there are no real extension points. State explicitly in the Build/Validate step that section 6 was omitted because nothing is pluggable; reviewers know it was a considered decision.

  **Example (pass):** A blueprint with sections 1–5 and 7 (no 6). The Validate step note: "Extension & Evolution omitted; no extension seams exist in the current architecture."

## DO NOT

- Ship the section with "TBD" or "To be defined" as content.

  **Example (fail):** "### 6. Extension & Evolution\nTBD — we'll define plug-in points once the system grows."

- Use the section to list speculative future ideas that are not implemented.

  **Example (fail):** "Future plug-in points may include theme packs, alternative payment providers, and custom reporting. Architecture support to be added."

- Describe a feature as "pluggable" when it is hard-coded in source.

  **Example (fail):** "Payment providers are pluggable" when the codebase has a `switch(provider)` statement enumerating Stripe and PayPal with no contract or registry. Either the seam is real (named contract + registry) or the section omits payment providers.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); empty sections are documentation rot.
