import type { KanbanBoard } from '@deliveryforge/kanban-server';
import { LeadScanService } from '@deliveryforge/kanban-server';

/**
 * Adapts the TypeScript LeadScanService to the app-server layer.
 *
 * Previously this class shelled out to the Python run_kanban_lead_tick.py.
 * The Python domain layer is now fully ported to TypeScript in packages/kanban/server.
 * Python scripts are kept but the app no longer depends on them.
 */
export class KanbanLeadService {
  /**
   * Run the lead-scan and return its JSON report.
   * Always executes regardless of board mode.
   */
  async runLeadScan(engagementRoot: string): Promise<Record<string, unknown>> {
    const service = new LeadScanService(engagementRoot);
    return service.runTick() as unknown as Promise<Record<string, unknown>>;
  }

  /**
   * Run the lead scan only when the board is NOT in fixture+manual mode.
   * In fixture+manual mode the scan is skipped to avoid auto-claiming roles
   * that violate manual drop intent ownership.
   *
   * Returns the scan result, or null when skipped.
   */
  async maybeRunLeadScan(
    engagementRoot: string,
    isFixtureWorkspace: boolean,
    board: KanbanBoard,
  ): Promise<Record<string, unknown> | null> {
    const isManual = board.boardMode === 'manual';
    if (isFixtureWorkspace && isManual) return null;
    try {
      return await this.runLeadScan(engagementRoot);
    } catch {
      return null;
    }
  }
}
