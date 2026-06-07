---
scanner: layer_purity_scanner.py
---

# Rule: Maintain Layer Purity

Dependencies point inward toward the domain core. The `shared/` package contains **plain TypeScript only** — no framework imports. The `server/` package never imports from `client/`, and vice versa. Both `client/` and `server/` depend on `shared/`, but `shared/` depends on neither.

## DO

- Keep `shared/` free of Express, React, MongoDB, Mongoose, and any infrastructure framework.
- Use only plain TypeScript, Zod (validation), and standard library in `shared/`.
- Import domain logic from `shared/` into both `client/` and `server/`.
- Place HTTP/Express concerns exclusively in `server/`.
- Place React/UI concerns exclusively in `client/`.

```typescript
// packages/recipients/shared/RecipientStatus.ts — CORRECT: plain TypeScript only
export type RecipientStatusType = 'Active' | 'Pending' | 'Inactive';

export class RecipientStatus {
  constructor(
    public readonly status: RecipientStatusType,
    public readonly createdAt: Date
  ) {}

  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }
}
```

```typescript
// packages/recipients/server/recipients.service.ts — CORRECT: imports from shared
import { Recipients } from '@project/recipients/shared';
import { RecipientsRepository } from './recipients.repository';

export class RecipientsService {
  constructor(private repo: RecipientsRepository) {}

  async getRecipients(enterpriseId: string) {
    const all = await this.repo.findByEnterprise(enterpriseId);
    return new Recipients(all).filterByStatus('Active').toArray();
  }
}
```

```typescript
// packages/recipients/server/recipients.service.ts — CORRECT: depends on interface, not concrete class
import { RecipientsRepositoryInterface } from './recipients.repository';

export class RecipientsService {
  constructor(private repo: RecipientsRepositoryInterface) {}  // interface — not the concrete MongoRepo
}
```

## DON'T

- Import Express, React, MongoDB, or any framework/infrastructure library in `shared/`.
- Import `client/` code from `server/` or `server/` code from `client/`.
- Place React components or hooks in `shared/`.
- Place Express middleware or route handlers in `shared/`.
- Depend on the concrete repository class in the service layer — services must accept the repository **interface** so they can work with any implementation (MongoDB, in-memory, test fake).

```typescript
// packages/recipients/shared/Recipient.ts — WRONG: framework import in shared
import { Schema, model } from 'mongoose';  // VIOLATION: infrastructure in domain core
import express from 'express';              // VIOLATION: server framework in shared

export const RecipientSchema = new Schema({ ... });
```

```typescript
// packages/recipients/server/recipients.service.ts — WRONG: importing from client
import { useRecipients } from '@project/recipients/client';  // VIOLATION: server imports client
```

```typescript
// packages/recipients/server/recipients.service.ts — WRONG: depends on concrete class
import { RecipientsRepository } from './recipients.repository';  // VIOLATION: concrete class, not interface

export class RecipientsService {
  constructor(private repo: RecipientsRepository) {}  // breaks when swapping implementations
}
```
