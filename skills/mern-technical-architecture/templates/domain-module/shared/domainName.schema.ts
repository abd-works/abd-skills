/**
 * domainName.schema.ts — Zod validation schema for the domain entity.
 *
 * Used at repository boundary (.parse()) to validate raw DB documents,
 * and at API/form boundary (.safeParse()) for user input validation.
 * Both client/ and server/ import this — single source of truth.
 */
import { z } from 'zod';

export const DomainNameSchema = z.object({
  id: z.string().uuid(),
  enterpriseId: z.string().uuid(),
  name: z.string().min(1, 'DomainName name is required').max(140),
  status: z.enum(['Active', 'Pending', 'Inactive']),
  createdAt: z.coerce.date(),
});

/** Raw DTO shape from Zod parse — status is a string enum, not a class instance. */
export type DomainNameDTO = {
  id: string;
  enterpriseId: string;
  name: string;
  status: 'Active' | 'Pending' | 'Inactive';
  createdAt: Date;
};
