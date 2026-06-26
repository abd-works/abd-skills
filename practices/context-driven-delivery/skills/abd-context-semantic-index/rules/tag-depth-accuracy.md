# Rule: Tag depth accuracy

This is a **tagging exercise, not full modeling**. Tags should stay at an orientation level — broad enough to classify and locate content, not so deep that the tagger is doing the work of downstream analysis. Passing means tags identify the right area (epic, module, platform, screen) without decomposing into individual stories, structured terms, component interactions, or UI controls. Failing means the tagger either over-structures content that should be left for later analysis, or speculates on details the content does not contain.

## DO

- Tag at the **orientation level** for each view — the level that answers "what area is this about?" not "what is the detailed structure?"

  **Example (pass):** The chunk discusses order processing workflows and validation. Tags include:

  ```yaml
  story:
    epic: Manage Orders
    actor: user
  domain:
    module: Order Management
    key_abstraction: Order
  ```

  The tagger identifies the capability area and the key abstraction — enough to locate this content. Decomposing into individual stories, specific terms like `Order Line`, or stereotypes like `aggregate` is downstream work.

- Tag `arch.provenance` for architecture content so it is clear what is custom-built versus platform-provided.

  **Example (pass):** The chunk says "Authentication uses AWS Cognito with custom token enrichment middleware." Tags include:

  ```yaml
  architecture:
    mechanism: security
    platform: AWS Cognito
    provenance: extended
  ```

  Cognito is out-of-box but the custom middleware makes this `extended`.

- Leave deeper tag levels empty — partial depth is expected and correct for a tagging pass.

  **Example (pass):** The chunk says "The system handles order management." Tags include:

  ```yaml
  domain:
    module: Order Management
  ```

  The content names the module but no specific abstractions — stopping at `module` is accurate.

## DO NOT

- Over-structure content by tagging at levels that belong to downstream analysis — individual stories, domain terms, DDD stereotypes, UI controls, or component interactions.

  **Example (fail):** The chunk discusses order processing. Tags include:

  ```yaml
  domain:
    module: Order Management
    key_abstraction: Order
    term: Order Line
    stereotype: aggregate
  story:
    epic: Manage Orders
    sub_epic: Process Order
    story: Submit Order
  ```

  The tagger decomposed into stories and domain terms — that is story mapping and domain modeling work, not tagging.

- Speculate on tag values the content does not actually contain — do not infer details from assumptions or external knowledge.

  **Example (fail):** The chunk says "The system processes customer orders." Tags include:

  ```yaml
  domain:
    module: Order Management
    key_abstraction: Order
    term: Order Line
    stereotype: aggregate
  ```

  The content never mentions `Order Line` or aggregate boundaries. The tagger guessed from general e-commerce knowledge instead of reading the text.

- Assign `arch.provenance` without evidence from the content about whether the component is custom or platform-provided.

  **Example (fail):** The chunk describes "a caching layer for product queries" with no mention of Redis, Memcached, or any platform. Tags include `arch.provenance: ootb`. There is no basis for the `ootb` claim — omit `provenance` or note it as unknown in the report.
