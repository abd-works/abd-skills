# Rule: page-slug-naming

**Artifact:** `pages/<slug>/` folder names inside `docs/extracted-context/app-extraction/`.

Each page folder name is a **slug** — a short, human-readable identifier that encodes traversal order and a meaningful label. This rule checks that slugs conform to that convention and are inspectable at a glance in any file explorer.

## DO

- Use the format `<NN>-<kebab-description>` for every page folder, where `<NN>` is a zero-padded two-digit sequence and `<kebab-description>` is a short, lowercase, hyphen-separated label.

  **Example (pass):** Folders named `01-login`, `02-dashboard`, `03-campaigns-list` — the sequence gives sort order; the label gives instant meaning.

- For modals, drawers, or overlays that belong to a parent page, append a lowercase letter suffix to the parent sequence number.

  **Example (pass):** Parent page is `03-campaigns-list`; the create modal becomes `03b-campaign-create-modal` and the delete confirmation becomes `03c-campaign-delete-confirm`. Both sort directly after the parent.

## DO NOT

- Use a sequence-only slug with no meaningful label.

  **Example (fail):** Folders named `step-001`, `step-002`, `page-1`, `view-003` — reading the folder tree gives no information about what each page contains.

- Use a label without a sequence prefix.

  **Example (fail):** Folder named `campaigns-list` with no numeric prefix — lost sort order; reviewer cannot tell where this view falls in the application flow.

- Use inconsistent casing or spaces in folder names.

  **Example (fail):** `03-Campaigns List` or `03-Campaigns_List` — uppercase and spaces break file-system portability and make glob patterns fragile.

**Source:** Engagement convention (abd-context-app-extractor authoring, 2026-06-25).
