# Stub Patterns

Stubs replace the outermost interface of each external dependency. The pattern you use depends on whether the codebase uses dependency injection, module aliases, or neither. Choose the lightest pattern that puts the stub at the earliest calling point without touching protocol internals.

## Finding the earliest calling point

Scan the codebase in this order:

1. **DI container registrations** — look for provider registrations (`useClass`, `useFactory`, `useValue` in NestJS; provider arrays in Angular; context providers in React). The registered token is the boundary point.
2. **Module-level factory exports** — look for `export function createXxxClient(...)` or `export const xxxService = ...` at the top of a service module. This is the boundary point.
3. **Direct SDK construction** — look for `new Stripe(...)`, `new SendGrid(...)`, `SESClient.from(...)`. If there is no DI seam, add a thin adapter around the construction and stub the adapter.
4. **Environment variable access** — look for `process.env.EXTERNAL_URL` or equivalent. The first point that reads the env-var and constructs a client is the boundary.

## Pattern A — NestJS / DI provider override

Use when the codebase registers external clients as NestJS providers.

```typescript
// src/__stubs__/stripe.stub.ts
import { STRIPE_CLIENT } from '@/payments/payments.tokens';

export const stripeStubProvider = {
  provide: STRIPE_CLIENT,
  useValue: {
    paymentIntents: {
      create: vi.fn().mockResolvedValue({ id: 'pi_stub_001', status: 'succeeded' }),
      retrieve: vi.fn().mockResolvedValue({ id: 'pi_stub_001', status: 'succeeded' }),
    },
    customers: {
      create: vi.fn().mockResolvedValue({ id: 'cus_stub_001' }),
    },
  },
};

// In your AppModule override for smoke-test / stub environment:
// providers: [stripeStubProvider]
```

**Boundary point:** `src/__stubs__/stripe.stub.ts → stripeStubProvider` (replaces `STRIPE_CLIENT` token)

## Pattern B — Module alias / path alias replacement

Use when the app imports from a fixed module path and the test environment supports path aliases (Vite, Jest `moduleNameMapper`, TypeScript path aliases).

```typescript
// src/__stubs__/email.ts
// Replaces @/services/email in test/stub environments

export const emailService = {
  send: vi.fn().mockResolvedValue({ messageId: 'stub-msg-001' }),
  sendTemplate: vi.fn().mockResolvedValue({ messageId: 'stub-tpl-001' }),
};
```

In `vitest.config.ts` or `jest.config.ts`:
```typescript
resolve: {
  alias: {
    '@/services/email': path.resolve(__dirname, 'src/__stubs__/email.ts'),
  },
}
```

**Boundary point:** `src/__stubs__/email.ts → emailService` (replaces `@/services/email`)

## Pattern C — Thin adapter extraction (no DI seam)

Use when external calls are made directly in controllers or services without a DI seam or module alias.

Step 1 — Extract the adapter (application code change):
```typescript
// src/adapters/payments.adapter.ts
export interface IPaymentsAdapter {
  chargeCard(amount: number, currency: string): Promise<{ transactionId: string }>;
}

export class StripePaymentsAdapter implements IPaymentsAdapter {
  async chargeCard(amount: number, currency: string) {
    const intent = await stripeClient.paymentIntents.create({ amount, currency });
    return { transactionId: intent.id };
  }
}
```

Step 2 — Create the stub:
```typescript
// src/__stubs__/payments.adapter.stub.ts
export class StubPaymentsAdapter implements IPaymentsAdapter {
  async chargeCard(_amount: number, _currency: string) {
    return { transactionId: 'txn_stub_001' };
  }
}
```

Step 3 — Bind in the test/stub environment:
```typescript
// AppModule override
{ provide: IPaymentsAdapter, useClass: StubPaymentsAdapter }
```

**Boundary point:** `src/__stubs__/payments.adapter.stub.ts → StubPaymentsAdapter` (replaces `IPaymentsAdapter`)

## Pattern D — Environment variable override (HTTP-level boundary)

Use only when the external service communicates over plain HTTP and the client is configurable via base URL — intercept at the URL level with a local HTTP stub server, not at the transport layer.

```typescript
// In stub environment setup: point STRIPE_BASE_URL at a local stub server
process.env.STRIPE_BASE_URL = 'http://localhost:9999';

// Local stub server (e.g. using msw, nock, or a minimal Express app)
// Responds to POST /v1/payment_intents with { id: 'pi_stub_001', status: 'succeeded' }
```

**Boundary point:** `process.env.STRIPE_BASE_URL` override; stub server at `http://localhost:9999`

**When to avoid:** Do not use this pattern to intercept OAuth token endpoints, refresh flows, or protocol-level authentication. Use Pattern A or B to stub the entire authenticated client instead.

## Hardcoded values — naming convention

Use a consistent prefix so stub values are easy to identify in test output and BDD steps:

| Category | Convention | Example |
|----------|-----------|---------|
| IDs | `<service>_stub_<sequence>` | `pi_stub_001`, `cus_stub_001` |
| Tokens | `stub-token-<sequence>` | `stub-token-001` |
| Message IDs | `stub-msg-<sequence>` | `stub-msg-001` |
| Transaction IDs | `txn_stub_<sequence>` | `txn_stub_001` |

Using a prefix makes it immediately obvious in logs and test output that a value is a stub value, not a real one that leaked into the test environment.
