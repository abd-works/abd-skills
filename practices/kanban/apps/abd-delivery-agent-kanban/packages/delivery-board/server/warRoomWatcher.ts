import { watch, type FSWatcher } from 'node:fs';
import path from 'node:path';
import { resolvePlanningPaths } from '@deliveryforge/delivery-board-shared';
import type { KanbanBoardService } from './kanbanBoard.service';

const WATCHED_PATTERN =
  /(?:board\.json|kanban\.json|metrics-log\.jsonl|heartbeat-[\w-]+\.json)$/i;
const DEBOUNCE_MS = 600;

export class WarRoomWatcher {
  private watcher: FSWatcher | null = null;
  private debounceTimer: ReturnType<typeof setTimeout> | null = null;
  private currentRoot: string | null = null;

  constructor(private readonly service: KanbanBoardService) {}

  watch(planningRoot: string): void {
    if (this.currentRoot === planningRoot) return;
    this.stop();

    const paths = resolvePlanningPaths(planningRoot);
    const kanbanDir = paths.kanbanDir.replace(/\//g, path.sep);

    this.currentRoot = planningRoot;

    try {
      this.watcher = watch(kanbanDir, { persistent: false, recursive: true }, (_eventType, filename) => {
        if (!filename || !WATCHED_PATTERN.test(filename.replace(/\\/g, '/'))) return;
        this.scheduleInvalidate(filename);
      });

      this.watcher.on('error', (err) => {
        console.warn('[kanban-watcher] watch error: ' + (err as Error).message);
      });

      console.log('[kanban-watcher] watching ' + kanbanDir);
    } catch (err) {
      console.warn('[kanban-watcher] could not watch ' + kanbanDir + ': ' + (err as Error).message);
    }
  }

  stop(): void {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    this.watcher?.close();
    this.watcher = null;
    this.currentRoot = null;
  }

  private scheduleInvalidate(trigger: string): void {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
      this.service.invalidateSnapshotCache();
      console.log('[kanban-watcher] ' + trigger + ' changed');
    }, DEBOUNCE_MS);
  }
}
