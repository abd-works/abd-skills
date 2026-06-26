# Rule: stub-at-boundary-not-internals

**Artifact:** Each stub file and the `Boundary Point` column in `docs/stubs/stub-inventory.md`.

A stub replaces the **entire interface** at the **earliest calling point** — the outermost adapter, SDK factory, or module export that the application's own code directly imports or instantiates. It does not intercept protocol-layer internals such as token exchange, TLS handshake, HTTP transport, or SDK retry loops. Stubbing internals creates fragile tests that break when the SDK's internal structure changes; stubbing the earliest interface is robust, honest, and easy to locate.

## DO

- Stub the outermost HTTP adapter or SDK factory. If the application imports and calls `stripeClient.paymentIntents.create(...)`, stub the entire `stripeClient` object returned by the factory — not the underlying `https.request` or transport call.

  **Example (pass):** `src/__stubs__/stripe.ts` exports `createStripeClient` that returns `{ paymentIntents: { create: vi.fn().mockResolvedValue({ id: 'pi_stub_001', status: 'succeeded' }) } }`. The DI container binds this factory to the `STRIPE_CLIENT` token for test and smoke-test environments.

- Stub at the module boundary that the application's own code imports. If the app does `import { emailService } from '@/services/email'`, the stub replaces the `email` module's export — not the SendGrid transport inside it.

  **Example (pass):** `src/__stubs__/email.ts` exports `emailService = { send: vi.fn().mockResolvedValue({ messageId: 'stub-msg-001' }) }`. The test environment resolves `@/services/email` to this stub via a Vite/Jest module alias or NestJS provider override.

- Record the **exact file path and exported symbol name** in `stub-inventory.md` as the `Boundary Point`.

  **Example (pass):** `src/__stubs__/stripe.ts → createStripeClient`

- When no dependency injection mechanism exists, wrap the external call in a thin adapter in the application code first, then stub the adapter — do not stub the third-party import directly.

  **Example (pass):** `src/adapters/payments.adapter.ts` exports `IPaymentsAdapter`. The stub implements `IPaymentsAdapter` with hardcoded return values. Application code already imports from `adapters/payments.adapter`, making the boundary explicit and testable.

## DO NOT

- Intercept OAuth token exchange, TLS handshake, session refresh, or any protocol-layer mechanism to simulate an authenticated session.

  **Example (fail):** A Nock interceptor overrides `https.request` to return a fake OAuth token for `https://oauth.stripe.com/token`. This stubs a protocol internal; the Stripe client's own token management is untested, the stub silently breaks on SDK version changes, and the approach cannot scale to other OAuth providers without separate interceptors.

- Mock individual private or protected methods deep inside an SDK's class hierarchy when the top-level factory or constructor is accessible.

  **Example (fail):** `jest.spyOn(Stripe.prototype._requestSender, 'send')` intercepts a private method. The earliest calling point is `new Stripe(apiKey)` — stub the constructor injection or factory, not the internal sender.

- Leave the `Boundary Point` column blank or write a prose description instead of a concrete file path and symbol.

  **Example (fail):** `Boundary Point: "somewhere in the payments service"` — must be `src/__stubs__/stripe.ts → createStripeClient`.

- Place the stub at a lower level than the outermost import just to avoid modifying existing application code. Refactor the thin adapter if needed.

  **Example (fail):** The Stripe call is buried in a controller method with no DI seam. Rather than adding a transport-level interceptor, extract `stripeClient` into a provider the controller receives via constructor injection, then stub the provider.

**Source:** Engagement convention (abd-stub-external-dependencies authoring, 2026-06-25).
