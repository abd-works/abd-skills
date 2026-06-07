import { z } from 'zod';

export const TeamSchema = z
  .object({
    'product-owner': z.number().int().min(0).default(1),
    'business-expert': z.number().int().min(0).default(1),
    'ux-designer': z.number().int().min(0).default(1),
    engineer: z.number().int().min(0).default(1),
  })
  .optional();

export type Team = z.infer<typeof TeamSchema>;
