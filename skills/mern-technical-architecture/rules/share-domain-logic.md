---
scanner: domain_structure_scanner.py
---

# Rule: Share Domain Logic

Define domain entities, value objects, Zod validation schemas, and business rule methods **once** in the `shared/` package. Both `client/` and `server/` import from `shared/` — never duplicate validation, type definitions, or business logic across tiers. This eliminates drift between frontend and backend validation, ensures consistent behavior, and creates a single source of truth for domain rules.

## DO

- Place all Zod schemas in `shared/` so both tiers validate identically.
- Define domain entity classes with business methods in `shared/`.
- Export collection/aggregate classes (e.g., `Recipients`) from `shared/` for reuse in both tiers.
- Use the shared schema in the repository layer to validate raw DB documents into typed entities.
- Use the same shared schema in the client for form validation before HTTP calls.

```typescript
// packages/recipients/shared/recipient.schema.ts — CORRECT: single source of truth
import { z } from 'zod';

export const RecipientSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(140),
  status: z.enum(['Active', 'Pending', 'Inactive']),
  beneficiaryBank: BeneficiaryBankSchema,
});

export type RecipientDTO = z.infer<typeof RecipientSchema>;
```

```typescript
// packages/recipients/server/recipients.repository.ts — CORRECT: validates with shared schema
import { RecipientSchema } from '@project/recipients/shared';

async findAll(): Promise<Recipient[]> {
  const docs = await this.collection.find().toArray();
  return docs.map(doc => RecipientSchema.parse(doc));  // shared validation
}
```

```typescript
// packages/recipients/client/RecipientForm.tsx — CORRECT: same schema for client validation
import { RecipientSchema } from '@project/recipients/shared';

const result = RecipientSchema.safeParse(formData);
if (!result.success) { setErrors(result.error.issues); }
```

## DON'T

- Duplicate Zod schemas or validation logic between `client/` and `server/`.
- Redefine TypeScript interfaces that already exist in `shared/`.
- Place business rule methods (e.g., eligibility checks) in only one tier.
- Create separate "client types" and "server types" for the same domain concept.

```typescript
// packages/recipients/server/validation.ts — WRONG: duplicated schema
import { z } from 'zod';
export const ServerRecipientSchema = z.object({  // DUPLICATE of shared schema
  id: z.string().uuid(),
  name: z.string().min(1).max(140),
  status: z.enum(['Active', 'Pending', 'Inactive']),
});
```

```typescript
// packages/recipients/client/types.ts — WRONG: separate type definition
export interface ClientRecipient {  // DUPLICATE: already defined in shared
  id: string;
  name: string;
  status: 'Active' | 'Pending' | 'Inactive';
}
```
