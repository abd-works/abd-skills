# What Counts as External

A dependency is **external** when it connects the application to a service that runs outside the repository boundary and is not orchestrated by the e2e test environment.

## The boundary question

Ask three questions in order:

1. **Is the service code in this repository?**
   If yes → **in-scope**. The service starts with the app and is already under test.

2. **Is the service declared in a compose file that runs as part of the e2e or integration test suite?**
   Check `docker-compose.yml`, `docker-compose.test.yml`, `docker-compose.e2e.yml`, and any equivalent in peer repositories that the root test setup references. If yes → **in-scope**.

3. **Is the service started by a peer-repo test script that is part of the same e2e run?**
   Common pattern: a root `Makefile` or `package.json` script runs `docker compose -f ../pml-harmony/docker-compose.yml up -d` before the e2e suite. If yes → **in-scope**.

If none of the above — **external**. It must be stubbed.

## Common external services

These are almost always external in a typical web or mobile backend:

| Category | Examples |
|----------|---------|
| Payment gateways | Stripe, Braintree, Adyen, PayPal |
| Email delivery | SendGrid, Mailgun, Amazon SES, Postmark |
| SMS / voice | Twilio, Vonage, MessageBird |
| Push notifications | Firebase FCM, APNs, OneSignal |
| Identity providers | Auth0, Okta, Cognito (when used as SaaS, not self-hosted) |
| Blob / object storage | AWS S3, Azure Blob, GCS (when not emulated locally) |
| Analytics / observability | Segment, Mixpanel, Datadog, Sentry |
| AI / ML APIs | OpenAI, Anthropic, Google Vertex |
| Search | Algolia, Elasticsearch Cloud (when not run locally) |
| CRM / ERP | Salesforce, HubSpot |

## The e2e-participant exception explained

A peer service that runs in the same e2e test suite is **not** external for the purposes of this skill because:

- It is already started and stopped by the test orchestration.
- Its behaviour is under the team's control (same org, same deploy pipeline).
- Stubbing it would create a fake seam that the real e2e test already covers.

**Example:** `pml-harmony` handles identity in the Paradise Mobile ecosystem. When the e2e suite starts `pml-harmony` as a container alongside `pml-vouchera`, the identity calls from `pml-vouchera` to `pml-harmony` are **in-scope**. Do not stub them; let the real service respond.

## Environment variable heuristic

If you see an environment variable whose value is a fully-qualified third-party URL (e.g. `https://api.stripe.com`, `https://api.sendgrid.com`, `https://management.twilio.com`), and that URL does not appear in any compose file's service definition, the dependency is **external**.

If the environment variable holds a `localhost` or container-network hostname (e.g. `http://harmony:3000`, `postgres://db:5432`), check whether that hostname is defined in a compose file before classifying.
