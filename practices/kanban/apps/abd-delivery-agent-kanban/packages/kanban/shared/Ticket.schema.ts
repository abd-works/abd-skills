import { z } from 'zod';
import { SkillProgressSchema } from './SkillProgress.schema';

function normalizeTicketNotes(value: unknown): string {
  if (value == null) return '';
  if (Array.isArray(value)) {
    return value.filter((n): n is string => typeof n === 'string').join('\n');
  }
  if (typeof value === 'string') return value;
  return String(value);
}

export const TicketSchema = z.object({
  ticket_id: z.string(),
  lineage: z.array(z.string()).default([]),
  scope_level: z.string().default('all'),
  stage: z.string(),
  priority: z.number().default(1),
  skill_progress: z.record(SkillProgressSchema).default({}),
  entered_stage: z.string().nullable().optional(),
  completed_stage: z.string().nullable().optional(),
  scatter_from: z.string().nullable().optional(),
  scatter_to: z.array(z.string()).default([]),
  notes: z.preprocess(normalizeTicketNotes, z.string()).default(''),
  stage_history: z
    .array(
      z.object({
        stage: z.string(),
        entered: z.string().nullable().optional(),
        completed: z.string().nullable().optional(),
        skipped: z.boolean().optional(),
      }),
    )
    .default([]),
  hold_in_progress: z.boolean().optional(),
});

export type RawTicket = z.infer<typeof TicketSchema>;
