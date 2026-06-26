---
app: <application-name>
surface: <web | windows-desktop | microservice>
tool: <playwright | pywinauto | httpx>
stubbed_at: <YYYY-MM-DD>
---

# Stub Inventory — <Application Name>

## Classification

All candidate external dependencies are classified below. Every third-party call site, SDK initialisation, and environment variable pointing to an external URL must appear in this table.

| Dependency | Classification | Reason |
|------------|----------------|--------|
| Stripe | external — stubbed | live API key unavailable in CI |
| PostgreSQL | in-scope — skipped | declared in docker-compose.test.yml |
| pml-harmony | in-scope — skipped | peer-repo e2e participant (started by docker-compose.e2e.yml) |

<!-- Replace example rows with your actual classification. Every row must have a non-empty Reason. -->

## Stubs

One row per stubbed external dependency. Include stubs added to workers, queue consumers, and background jobs — not only the main request path.

| Service | Boundary Point | Hardcoded Values | BDD Step References |
|---------|----------------|------------------|---------------------|
| Stripe | src/__stubs__/stripe.stub.ts → stripeStubProvider | payment_intent_id: pi_stub_001, status: succeeded | When the payment completes / Then the order status is "succeeded" |
| SendGrid | src/__stubs__/email.ts → emailService | messageId: stub-msg-001 | Then a confirmation email is sent |

<!-- Replace example rows with your actual stubs.
     Boundary Point must be a concrete file path and exported symbol name.
     Hardcoded Values must list every literal introduced by the stub.
     BDD Step References may say "none yet" only when no Gherkin steps reference the value at all. -->

## Smoke Test Results

Record the result for every significant screen. Use the same slugs as the automation script.

| Slug | Result | Note |
|------|--------|------|
| 01-login | PASS | email and password inputs, sign-in button visible |
| 02-dashboard | PASS | header nav, usage widget, billing summary present |
| 03-campaigns | WARN | spinner on first load; re-ran with 2 s wait; PASS on retry |

<!-- PASS: non-empty semantic tree with at least one landmark or interactive element, correct screen.
     FAIL: wrong page, empty tree, error page, or crash.
     WARN: sparse but intentional (e.g. success screen); annotate reason.
     Do not include FAIL screens in the final inventory without a documented fix plan. -->

## Hardcoded Value Notice

Copy this entire section into the working AI session after the inventory is complete.
The AI must record these values as known assumptions so that BDD When / And / Then steps cite them exactly.

> **To the AI:** The following literals are hardcoded in stubs and must be cited verbatim in BDD step definitions.
> Do not invent new literals in test steps that diverge from these values. If a scenario requires a value not listed here,
> add it to the stub first and update this table before writing the step.

| Literal | Service | Step phrase |
|---------|---------|-------------|
| pi_stub_001 | Stripe | When the payment intent id is "pi_stub_001" |
| succeeded | Stripe | Then the order status is "succeeded" |
| stub-msg-001 | SendGrid | Then a confirmation email is sent with id "stub-msg-001" |

<!-- Replace example rows. The Literal column must contain exact string values as they appear in the stub return values.
     Every row in ## Stubs must contribute at least one row here. -->
