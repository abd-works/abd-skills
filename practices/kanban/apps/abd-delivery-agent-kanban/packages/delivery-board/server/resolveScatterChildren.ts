import { readFileSync, existsSync } from 'node:fs';

import { join } from 'node:path';



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



function slugify(title: string): string {

  return title

    .toLowerCase()

    .trim()

    .replace(/[^a-z0-9]+/g, '-')

    .replace(/^-+|-+$/g, '');

}



function incrementNumberFromTicketId(ticketId: string): number | null {

  const inc = ticketId.match(/-inc-(\d+)-/i);

  if (inc) return Number(inc[1]);

  const head = ticketId.split('-', 1)[0]!;

  if (/^\d+$/.test(head)) return Number(head);

  return null;

}



function isIncrementScatterParent(ticketId: string): boolean {

  return /-inc-\d+-/i.test(ticketId);

}



function parseIncrementsFromText(text: string, parentId: string): ScatterChildSpec[] {

  const children: ScatterChildSpec[] = [];

  const re = /### Increment (\d+): (.+)/g;

  let m: RegExpExecArray | null;

  while ((m = re.exec(text)) !== null) {

    const incNum = Number(m[1]);

    const title = m[2]!.trim();

    children.push({

      id: `${parentId}-inc-${incNum}-${slugify(title)}`,

      name: title,

      priority: incNum,

    });

  }

  if (children.length === 0) {

    throw new Error('No increments found in thin-slicing document');

  }

  return children;

}



function parseIncrementsFromModuleSection(

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

  return parseIncrementsFromText(section[0], parentId);

}



function moduleNumberFromTicketId(ticketId: string): number | null {

  const head = ticketId.split('-', 1)[0]!;

  if (!/^\d+$/.test(head)) return null;

  return Number(head);

}



function resolveFromThinSlicing(workspaceRoot: string, parentTicketId: string): ScatterChildSpec[] {

  const mod = moduleNumberFromTicketId(parentTicketId);



  const discoveryThin = join(workspaceRoot, 'docs/end-to-end/discovery/stories/thin-slicing.md');

  if (existsSync(discoveryThin)) {

    const text = readFileSync(discoveryThin, 'utf8');

    if (mod !== null) {

      return parseIncrementsFromModuleSection(text, mod, parentTicketId);

    }

    return parseIncrementsFromText(text, parentTicketId);

  }



  const shapingThin = join(workspaceRoot, 'docs/end-to-end/shaping/thin-slicing.md');

  if (existsSync(shapingThin)) {

    const text = readFileSync(shapingThin, 'utf8');

    if (mod !== null) {

      try {

        return parseIncrementsFromModuleSection(text, mod, parentTicketId);

      } catch {

        // single-project boards: whole-file increments

      }

    }

    return parseIncrementsFromText(text, parentTicketId);

  }



  const dash = parentTicketId.indexOf('-');

  const slug = dash >= 0 ? parentTicketId.slice(dash + 1) : parentTicketId;

  const perModule = join(

    workspaceRoot,

    `docs/end-to-end/discovery/stories/${slug}-thin-slicing.md`,

  );

  if (existsSync(perModule)) {

    const text = readFileSync(perModule, 'utf8');

    return parseIncrementsFromText(text, parentTicketId);

  }



  throw new Error(

    `No thin-slicing for scatter from ${parentTicketId}: tried discovery/stories/thin-slicing.md, shaping/thin-slicing.md, and ${perModule}`,

  );

}



function parseSprintsFromGroupingsSection(

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



function resolveFromSprintGroupings(

  workspaceRoot: string,

  parentTicketId: string,

): ScatterChildSpec[] {

  const path = join(workspaceRoot, 'docs/end-to-end/discovery/stories/sprint-groupings.md');

  if (!existsSync(path)) {

    throw new Error(`No sprint-groupings.md for scatter from ${parentTicketId}`);

  }



  const incNum = incrementNumberFromTicketId(parentTicketId);

  if (incNum === null) {

    throw new Error(`Cannot infer increment number from ticket_id: ${parentTicketId}`);

  }



  const text = readFileSync(path, 'utf8');

  const section = text.match(

    new RegExp(`## Increment ${incNum}:.*?(?=\\n## Increment \\d+:|$)`, 's'),

  );

  if (!section) {

    throw new Error(`No Increment ${incNum} section in sprint-groupings.md`);

  }



  const slugMatch = section[0].match(/`([^`]+)`/);

  const incrementSlug = slugMatch?.[1] ?? `inc-${incNum}`;

  return parseSprintsFromGroupingsSection(section[0], incrementSlug);

}



/**

 * Resolve scatter children from planning artifacts.

 * - all/project → increment: thin-slicing only (never re-parse thin-slicing for increment parents).

 * - increment → sprint: sprint-groupings.md only; missing file → caller advances ticket without scatter.

 */

export function resolveScatterChildren(

  workspaceRoot: string,

  parentTicketId: string,

  context?: ScatterResolveContext,

): ScatterChildSpec[] {

  const childScope = context?.childScope;

  if (childScope === 'sprint' || isIncrementScatterParent(parentTicketId)) {

    return resolveFromSprintGroupings(workspaceRoot, parentTicketId);

  }

  return resolveFromThinSlicing(workspaceRoot, parentTicketId);

}



/** Returns null when scatter artifacts for this boundary are missing. */

export function tryResolveScatterChildren(

  engagementRoot: string,

  parentTicketId: string,

  context?: ScatterResolveContext,

): ScatterChildSpec[] | null {

  try {

    return resolveScatterChildren(engagementRoot, parentTicketId, context);

  } catch {

    return null;

  }

}

