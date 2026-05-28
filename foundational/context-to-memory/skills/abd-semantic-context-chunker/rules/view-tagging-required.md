# Rule: View tagging required

Every chunk and every pass-through file must be tagged with at least one primary view and the corresponding hierarchical tags from the taxonomy reference. Passing means no chunk exists without a `primary_views` list and at least one view's tag hierarchy filled in. Failing means chunks are left untagged, or tags are invented outside the vocabulary in `references/four-view-taxonomy.md`.

## DO

- Assign at least one entry in `primary_views` (story, domain, architecture, ux) to every chunk and every pass-through file.

  **Example (pass):**

  ```yaml
  primary_views: [domain, architecture]
  tags:
    domain:
      module: Order Management
      key_abstraction: Order
    architecture:
      component: Order Service
      provenance: custom
  ```

  The chunk describes order data and the service that manages it — both views are tagged with hierarchical detail.

- Tag content that legitimately informs multiple views with all applicable views — do not force a single assignment.

  **Example (pass):** A paragraph about "users cancel orders from the order detail screen if status is Pending" is tagged `primary_views: [story, ux, domain]` because it describes a user action (story), names a screen (ux), and references a status constraint (domain).

- Use only tag names and enum values defined in `references/four-view-taxonomy.md`.

  **Example (pass):** `story.actor: user` — the value `user` is in the taxonomy's enum for `story.actor`.

## DO NOT

- Leave any chunk or pass-through file with an empty or missing `primary_views` list.

  **Example (fail):**

  ```yaml
  chunk_id: requirements__chunk_04
  primary_views: []
  tags: {}
  ```

  The chunk has no view assignment and no tags — a reviewer cannot tell which practice this content informs.

- Invent tag names or values that do not appear in the taxonomy reference.

  **Example (fail):** `domain.category: business_logic` — the taxonomy defines `domain.module_kind` with specific enum values, not `domain.category`. The tagger invented a field.

- Tag a chunk with all four views when its content clearly serves only one or two.

  **Example (fail):** A paragraph that only lists database column definitions is tagged `primary_views: [story, domain, architecture, ux]`. It should be `[domain]` or at most `[domain, architecture]` — there is no story behavior, no screen layout.
