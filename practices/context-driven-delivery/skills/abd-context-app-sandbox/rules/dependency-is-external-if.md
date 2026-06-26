# Rule: dependency-is-external-if

**Artifact:** The `## Classification` table in `docs/stubs/stub-inventory.md`.

A dependency is **external** — and must be stubbed — when it points to a service that is neither part of the same repository nor a declared participant in a peer-repo e2e test suite. In-repo services and peer-repo e2e participants already run under controlled conditions; stubbing them would duplicate isolation already provided by the test environment and produce misleading stubs.

## DO

- Mark a dependency as **external — stubbed** when its endpoint is configured via an environment variable that resolves to a third-party SaaS URL not present in any docker-compose or equivalent orchestration file.

  **Example (pass):** `STRIPE_BASE_URL=https://api.stripe.com` is in `.env.example` but not in `docker-compose.test.yml`. The Stripe client is classified `external — stubbed`.

- Mark a dependency as **external — stubbed** when its SDK is initialised with a key sourced from a vault, secret manager, or CI secret that is not populated during local dev or CI stub runs.

  **Example (pass):** `new SendGrid({ apiKey: process.env.SENDGRID_API_KEY })` where `SENDGRID_API_KEY` is absent from the `.env.example` and `.env.test`. Classified `external — stubbed`.

- Mark a dependency as **in-scope — skipped** when its service is declared as a named container in a `docker-compose.yml`, `docker-compose.test.yml`, `docker-compose.e2e.yml`, or equivalent file that is started as part of the test or dev run.

  **Example (pass):** `postgres` and `redis` are services in `docker-compose.test.yml`. Both are classified `in-scope — skipped — declared in docker-compose.test.yml`.

- Mark a dependency as **in-scope — skipped** when its service lives in a sibling or peer repository that is explicitly started as a container in the root e2e compose file or test setup script.

  **Example (pass):** `pml-harmony` identity service is started by `docker-compose.e2e.yml` via `../pml-harmony/docker-compose.yml`. It is classified `in-scope — skipped — peer-repo e2e participant`.

- Classify every call site — including those in background workers, queue consumers, cron jobs, and event handlers — not only those in the main HTTP request path.

  **Example (pass):** An SES email client called from a Bull worker appears in the classification table alongside the Stripe client called from the API controller.

## DO NOT

- Mark a third-party API as **in-scope** because a Jest fixture or Nock interceptor provides sample responses for it. Fixture data does not make the live endpoint in-scope.

  **Example (fail):** Stripe responses are mocked in Jest fixtures, so Stripe is classified `in-scope — skipped`. Wrong — the live Stripe endpoint is still external. The classification must be `external — stubbed` and a proper boundary stub must replace the Jest fixture for the smoke-test run.

- Classify only the dependencies visible in the main app entry point. Scan all modules, workers, and services in the repository.

  **Example (fail):** The classification table lists Stripe (API controller) but omits Twilio (SMS worker) and S3 (file upload service). All three are external and must be classified.

- Leave the `Reason` column blank for any **in-scope — skipped** row.

  **Example (fail):** A row reads `PostgreSQL | in-scope — skipped |` with no reason. Must state why: `declared in docker-compose.test.yml`.

**Source:** Engagement convention (abd-stub-external-dependencies authoring, 2026-06-25).
