import { Ticket as DomainTicket } from '@deliveryforge/kanban-shared';
import type { KanbanColumn } from '@deliveryforge/kanban-shared';
import type { RawTicket } from '@deliveryforge/kanban-shared';
import {
  KanbanBoard,
  type KanbanConfiguration,
  type StageId,
} from '@deliveryforge/kanban-shared';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

// ── Scatter types ──────────────────────────────────────────────────────────

export type ScatterChildSpec = {
  id: string;
  name: string;
  priority: number;
};

export type ScatterResolveContext = {
  /** Scope of children at the boundary stage (e.g. increment, sprint). */
  childScope: string;
  ticketScopeLevel?: string;
};

/**
 * Server-side Ticket — extends domain Ticket with planning-artifact I/O.
 * Owns scatter child resolution: reading thin-slicing.md and sprint-groupings.md
 * from the engagement workspace to produce the scatter child specs that the
 * KanbanBoard needs when advancing a parent ticket through a scope boundary.
 */
export class Ticket extends DomainTicket {
  constructor(raw: RawTicket, column: KanbanColumn) {
    super(raw, column);
  }

  // ── Instance: scatter child resolution ───────────────────────────────────

  /**
   * Resolve scatter children from planning artifacts for this ticket.
   * Reads thin-slicing.md or sprint-groupings.md from the engagement workspace.
   * Throws if no artifact is found.
   */
  resolveScatterChildren(
    engagementRoot: string,
    context?: ScatterResolveContext,
  ): ScatterChildSpec[] {
    return Ticket.resolveScatterChildren(engagementRoot, this.ticketId, context);
  }

  /**
   * Try to resolve scatter children — returns null if planning artifacts
   * are missing instead of throwing, allowing the board to advance without scatter.
   */
  tryResolveScatterChildren(
    engagementRoot: string,
    context?: ScatterResolveContext,
  ): ScatterChildSpec[] | null {
    return Ticket.tryResolveScatterChildren(engagementRoot, this.ticketId, context);
  }

  // ── Instance: scatter boundary helper ────────────────────────────────────

  /**
   * Determine whether this ticket sits at a scatter boundary on the path
   * from its current stage to the target stage.
   */
  scatterBoundary(
    board: KanbanBoard,
    config: KanbanConfiguration,
    definitionName: string | null | undefined,
    targetStage: StageId,
  ): { boundaryStage: StageId; childStage: StageId; childScope: string } | null {
    if (!this.stage) return null;
    return board.scatterBoundaryOnPath(
      config,
      definitionName,
      this.scopeLevel,
      this.stage as StageId,
      targetStage,
    );
  }

  // ── Static: scatter child resolution (used by KanbanBoard) ───────────────

  /**
   * Resolve scatter children for any ticket ID from planning artifacts.
   * - all/project → increment: thin-slicing.md
   * - increment → sprint: sprint-groupings.md
   */
  static resolveScatterChildren(
    workspaceRoot: string,
    parentTicketId: string,
    context?: ScatterResolveContext,
  ): ScatterChildSpec[] {
    const childScope = context?.childScope;
    if (childScope === 'sprint' || Ticket.isIncrementScatterParent(parentTicketId)) {
      return Ticket.resolveFromSprintGroupings(workspaceRoot, parentTicketId);
    }
    return Ticket.resolveFromThinSlicing(workspaceRoot, parentTicketId);
  }

  /** Returns null when scatter artifacts for this boundary are missing. */
  static tryResolveScatterChildren(
    engagementRoot: string,
    parentTicketId: string,
    context?: ScatterResolveContext,
  ): ScatterChildSpec[] | null {
    try {
      return Ticket.resolveScatterChildren(engagementRoot, parentTicketId, context);
    } catch {
      return null;
    }
  }

  // ── Private: ID helpers ───────────────────────────────────────────────────

  private static slugify(title: string): string {
    return title
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  private static incrementNumberFromTicketId(ticketId: string): number | null {
    const inc = ticketId.match(/-inc-(\d+)-/i);
    if (inc) return Number(inc[1]);
    const head = ticketId.split('-', 1)[0]!;
    if (/^\d+$/.test(head)) return Number(head);
    return null;
  }

  private static isIncrementScatterParent(ticketId: string): boolean {
    return /-inc-\d+-/i.test(ticketId);
  }

  private static moduleNumberFromTicketId(ticketId: string): number | null {
    const head = ticketId.split('-', 1)[0]!;
    if (!/^\d+$/.test(head)) return null;
    return Number(head);
  }

  // ── Private: thin-slicing parsers ─────────────────────────────────────────

  private static parseIncrementsFromText(text: string, parentId: string): ScatterChildSpec[] {
    const children: ScatterChildSpec[] = [];
    const re = /### Increment (\d+): (.+)/g;
    let m: RegExpExecArray | null;
    while ((m = re.exec(text)) !== null) {
      const incNum = Number(m[1]);
      const title = m[2]!.trim();
      children.push({
        id: `${parentId}-inc-${incNum}-${Ticket.slugify(title)}`,
        name: title,
        priority: incNum,
      });
    }
    if (children.length === 0) {
      throw new Error('No increments found in thin-slicing document');
    }
    return children;
  }

  private static parseIncrementsFromModuleSection(
    text: string,
    moduleNum: number,
    parentId: string,
  ): ScatterChildSpec[] {
    const section = text.match(
      new RegExp(`## Module ${moduleNum}:.*?(?=\\n## Module \\d+:|$)`, 's'),
    );
    if (!section) {
      throw new Error(`No Module ${moduleNum} section in thin-slicing document`);
    }
    return Ticket.parseIncrementsFromText(section[0], parentId);
  }

  private static resolveFromThinSlicing(
    workspaceRoot: string,
    parentTicketId: string,
  ): ScatterChildSpec[] {
    const mod = Ticket.moduleNumberFromTicketId(parentTicketId);

    const discoveryThin = join(workspaceRoot, 'docs/end-to-end/discovery/stories/thin-slicing.md');
    if (existsSync(discoveryThin)) {
      const text = readFileSync(discoveryThin, 'utf8');
      if (mod !== null) {
        return Ticket.parseIncrementsFromModuleSection(text, mod, parentTicketId);
      }
      return Ticket.parseIncrementsFromText(text, parentTicketId);
    }

    const shapingThin = join(workspaceRoot, 'docs/end-to-end/shaping/thin-slicing.md');
    if (existsSync(shapingThin)) {
      const text = readFileSync(shapingThin, 'utf8');
      if (mod !== null) {
        try {
          return Ticket.parseIncrementsFromModuleSection(text, mod, parentTicketId);
        } catch {
          // single-project boards: whole-file increments
        }
      }
      return Ticket.parseIncrementsFromText(text, parentTicketId);
    }

    const dash = parentTicketId.indexOf('-');
    const slug = dash >= 0 ? parentTicketId.slice(dash + 1) : parentTicketId;
    const perModule = join(
      workspaceRoot,
      `docs/end-to-end/discovery/stories/${slug}-thin-slicing.md`,
    );
    if (existsSync(perModule)) {
      const text = readFileSync(perModule, 'utf8');
      return Ticket.parseIncrementsFromText(text, parentTicketId);
    }

    throw new Error(
      `No thin-slicing for scatter from ${parentTicketId}: tried discovery/stories/thin-slicing.md, shaping/thin-slicing.md, and ${perModule}`,
    );
  }

  // ── Private: sprint-groupings parsers ────────────────────────────────────

  private static parseSprintsFromGroupingsSection(
    sectionText: string,
    incrementSlug: string,
  ): ScatterChildSpec[] {
    const children: ScatterChildSpec[] = [];
    const rowRe = /^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|/gm;
    let m: RegExpExecArray | null;
    while ((m = rowRe.exec(sectionText)) !== null) {
      const sprintNum = Number(m[1]);
      const label = m[2]!.trim();
      if (!label || label.toLowerCase() === 'label') continue;
      children.push({
        id: `${incrementSlug}-sprint-${sprintNum}`,
        name: label,
        priority: sprintNum,
      });
    }
    if (children.length === 0) {
      throw new Error(`No sprint rows in sprint-groupings for ${incrementSlug}`);
    }
    return children;
  }

  private static resolveFromSprintGroupings(
    workspaceRoot: string,
    parentTicketId: string,
  ): ScatterChildSpec[] {
    const filePath = join(workspaceRoot, 'docs/end-to-end/discovery/stories/sprint-groupings.md');
    if (!existsSync(filePath)) {
      throw new Error(`No sprint-groupings.md for scatter from ${parentTicketId}`);
    }

    const incNum = Ticket.incrementNumberFromTicketId(parentTicketId);
    if (incNum === null) {
      throw new Error(`Cannot infer increment number from ticket_id: ${parentTicketId}`);
    }

    const text = readFileSync(filePath, 'utf8');
    const section = text.match(
      new RegExp(`## Increment ${incNum}:.*?(?=\\n## Increment \\d+:|$)`, 's'),
    );
    if (!section) {
      throw new Error(`No Increment ${incNum} section in sprint-groupings.md`);
    }

    const slugMatch = section[0].match(/`([^`]+)`/);
    const incrementSlug = slugMatch?.[1] ?? `inc-${incNum}`;
    return Ticket.parseSprintsFromGroupingsSection(section[0], incrementSlug);
  }
}
