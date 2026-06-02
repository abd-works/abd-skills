/** Must match config.default.json planningRoot (pawplace-stubs). */
export const DEFAULT_PLANNING_ROOT =
  import.meta.env.VITE_PLANNING_ROOT ??
  'C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning';

const OVERRIDE_KEY = 'planningRootOverride';

/** User override from Connect — not the old `planningRoot` key (ignored). */
export function readPlanningRootOverride(): string | null {
  return localStorage.getItem(OVERRIDE_KEY);
}

export function savePlanningRootOverride(root: string): void {
  localStorage.setItem(OVERRIDE_KEY, root);
}

export function resolvePlanningRoot(): string {
  if (import.meta.env.VITE_PLANNING_ROOT) {
    return import.meta.env.VITE_PLANNING_ROOT;
  }
  return readPlanningRootOverride() ?? DEFAULT_PLANNING_ROOT;
}
