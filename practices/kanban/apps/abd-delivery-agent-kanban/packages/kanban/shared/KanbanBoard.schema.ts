import { z } from 'zod';
import { TicketSchema } from './Ticket.schema';
import { TeamSchema } from './TeamMembership.schema';

export const KanbanBoardSchema = z.object({
  schema: z.literal('abd-delivery-kanban/v2'),
  synced_at: z.string().nullable().optional(),
  stage_configuration: z.string().nullable().optional(),
  board_mode: z.enum(['automatic', 'manual']).default('automatic'),
  backlog: z.array(TicketSchema).default([]),
  active: z.array(TicketSchema).default([]),
  done: z.array(TicketSchema).default([]),
  archived: z.array(TicketSchema).default([]),
  team: TeamSchema,
});

export type KanbanBoardData = z.infer<typeof KanbanBoardSchema>;

export function parseKanbanBoard(raw: unknown): KanbanBoardData {
  return KanbanBoardSchema.parse(raw);
}
