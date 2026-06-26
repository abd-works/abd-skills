# Rule: stub-inventory-format

**Artifact:** `docs/stubs/stub-inventory.md`

The stub inventory is the canonical record of every stub introduced by this skill. It must be complete enough that a reviewer — or a future AI working on BDD test steps — can identify every hardcoded value, trace it to its boundary point, and know which test step phrases cite it.

## DO

- Open the file with a YAML front-matter block containing `app`, `surface`, `tool`, and `stubbed_at` fields.

  **Example (pass):**
  ```yaml
  ---
  app: pml-vouchera
  surface: web
  tool: playwright
  stubbed_at: 2026-06-25
  ---
  ```

- Include a `## Classification` section before the stub table. One row per candidate dependency, with columns `Dependency`, `Classification`, and `Reason`.

  **Example (pass):**
  ```markdown
  ## Classification
  | Dependency | Classification | Reason |
  |------------|----------------|--------|
  | Stripe     | external — stubbed | live API key unavailable in CI |
  | PostgreSQL | in-scope — skipped | declared in docker-compose.test.yml |
  | pml-harmony | in-scope — skipped | peer-repo e2e participant |
  ```

- Include a `## Stubs` section with columns `Service`, `Boundary Point`, `Hardcoded Values`, and `BDD Step References`. One row per stubbed external dependency.

  **Example (pass):**
  ```markdown
  ## Stubs
  | Service | Boundary Point | Hardcoded Values | BDD Step References |
  |---------|----------------|------------------|---------------------|
  | Stripe  | src/__stubs__/stripe.ts → createStripeClient | payment_intent_id: pi_stub_001, status: succeeded | When the payment completes / Then the order status is "succeeded" |
  | SendGrid | src/__stubs__/email.ts → emailService | messageId: stub-msg-001 | Then a confirmation email is sent |
  ```

- Include a `## Smoke Test Results` section. One row per significant screen with columns `Slug`, `Result` (PASS / FAIL / WARN), and `Note`.

  **Example (pass):**
  ```markdown
  ## Smoke Test Results
  | Slug | Result | Note |
  |------|--------|------|
  | 01-login | PASS | email and password inputs visible |
  | 02-dashboard | PASS | nav, usage widget, billing summary present |
  | 03-campaigns | WARN | spinner visible on first load; passed on retry with longer wait |
  ```

- Include a `## Hardcoded Value Notice` section — a flat table of every literal value introduced by stubs, the service it belongs to, and the BDD step phrase that references it. This table is copied to the AI session prompt after inventory completion.

  **Example (pass):**
  ```markdown
  ## Hardcoded Value Notice
  | Literal | Service | Step phrase |
  |---------|---------|-------------|
  | pi_stub_001 | Stripe | When the payment intent id is "pi_stub_001" |
  | succeeded | Stripe | Then the order status is "succeeded" |
  | stub-msg-001 | SendGrid | Then a confirmation email is sent with id "stub-msg-001" |
  ```

- List every stub in the inventory, including stubs added to workers, queue consumers, cron jobs, and event handlers.

  **Example (pass):** The Stripe stub (API controller) and the SES email stub (Bull worker) both appear in the `## Stubs` table.

## DO NOT

- Omit any stub from the `## Stubs` table even if the stub is only active in a non-HTTP code path.

  **Example (fail):** The stub table lists Stripe but omits the SES stub added to the email worker because "it's not part of the web flow". Every external stub must appear.

- Leave `BDD Step References` blank when existing Gherkin steps already reference the hardcoded value. Write `none yet` only when no steps exist for that service at all.

  **Example (fail):** `payment.feature` contains `Then the order status is "succeeded"` but the Stripe row's `BDD Step References` column says `none yet`.

- Use the `## Hardcoded Value Notice` table to introduce new test data not already in the `## Stubs` table. The notice table flattens the stubs table — it does not add new values.

  **Example (fail):** The notice table lists `payment_intent_id: pi_real_005` — a value not present in any stub. New values must come from the stubs themselves, not be invented in the notice.

**Source:** Engagement convention (abd-stub-external-dependencies authoring, 2026-06-25).
