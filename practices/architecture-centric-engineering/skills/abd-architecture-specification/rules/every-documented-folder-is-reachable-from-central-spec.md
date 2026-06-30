---
scanner: every-documented-folder-reachable
---

### Rule: Every folder with a context file appears in the central spec's index

If a folder has an `architecture-context.md`, the central spec MUST list it under Package Context (in the right category) and link to it. A documented folder absent from the index is invisible: a developer searching the central spec for the right unit will never find it, and the documentation effort is wasted. The inverse also holds: every link in Package Context MUST point at a context file that exists. Passing means the set of entries under Package Context matches the set of `architecture-context.md` files on disk exactly. Failing means an authored context file is missing from the index OR the index links a folder that has no context file (a 404 from the spec).

#### DO

- Index every documented folder under the right category.

  **Example (pass):** `find . -name architecture-context.md` returns 9 files; Package Context lists 9 entries across the Mechanisms / Services / Utilities & Legacy / Testing categories.

- Place each entry under the category that matches its tier and role.

  **Example (pass):** Mechanism-tier context files appear under **Mechanisms**; third-party SDK wrappers appear under **Services**; grab-bags and legacy folders appear under **Utilities & Legacy**; test helpers appear under **Testing**.

- When a new context file is authored, add the index entry in the same change.

  **Example (pass):** Adding `/tests/integration-helpers/architecture-context.md` includes a corresponding `- **Integration helpers** — ...` entry under **Testing** in the central spec.

#### DO NOT

- Author a context file the central spec does not link.

  **Example (fail):** `/tests/test-helpers/architecture-context.md` exists; the Testing category in the central spec is empty. A developer reading the central spec never learns that file exists.

- List a folder under Package Context that has no context file.

  **Example (fail):** Package Context says `- **SmsGateway** — ... [/src/adapters/SmsGateway/](/src/adapters/SmsGateway/architecture-context.md)` but no such file exists on disk. The link 404s; the reader gives up.

- Categorise a context file by its folder name rather than its role.

  **Example (fail):** `tests/domain-helpers/architecture-context.md` is filed under **Utilities & Legacy** because the file path contains "helpers". Test helpers belong under **Testing**.

**Source:** Documentation that cannot be navigated cannot be used; the central spec's index is the contract that every authored context file is discoverable.
