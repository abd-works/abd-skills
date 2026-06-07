import { z } from 'zod';

export const SkillProgressSchema = z.object({
  execution_status: z
    .preprocess(
      (v) => (v === 'pending' ? 'not_started' : v),
      z.enum(['not_started', 'in_progress', 'done']),
    )
    .default('not_started'),
  agent: z.string().nullable().optional(),
  start: z.string().nullable().optional(),
  end: z.string().nullable().optional(),
  review_status: z
    .enum(['not_started', 'in_progress', 'done', 'failed'])
    .nullable()
    .optional()
    .transform((v) => (v === 'not_started' ? null : v)),
  reviewer: z.string().nullable().optional(),
  review_start: z.string().nullable().optional(),
  review_end: z.string().nullable().optional(),
});

export type SkillProgress = z.infer<typeof SkillProgressSchema>;
