import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';

export type AgentOutputEvent =
  | { type: 'text'; content: string }
  | { type: 'thinking' };

/**
 * CursorCliAdapter — drives the Cursor headless agent CLI instead of @cursor/sdk.
 *
 * Spawns: agent -p --output-format stream-json --force --workspace <workspace> <prompt>
 *
 * Parses the NDJSON stream to extract text events and tool-call indicators,
 * then broadcasts them to registered listeners. No native modules required.
 */

export type SdkSessionState = 'running' | 'completed' | 'failed';

export interface SdkStreamListener {
  (event: AgentOutputEvent): void;
}

export interface SdkSessionStatus {
  state: SdkSessionState;
  messageCount: number;
  lastActivitySec: number;
  finalMessage?: string;
  errorDetail?: string;
}

const AGENT_BIN = process.env['CURSOR_AGENT_BIN'] || 'agent';

export class CursorSdkAdapter {
  readonly role: string;
  readonly workspace: string;
  private _state: SdkSessionState = 'running';
  private _messageCount = 0;
  private _lastActivityTs: number = Date.now();
  private _finalMessage: string | null = null;
  private _errorDetail: string | null = null;
  private readonly _listeners = new Set<SdkStreamListener>();
  private _proc: ReturnType<typeof spawn> | null = null;

  constructor(role: string, workspace: string) {
    this.role = role;
    this.workspace = workspace;
  }

  // ─── Lifecycle ─────────────────────────────────────────────────────────────

  async start(bootstrapPrompt: string): Promise<void> {
    const apiKey = process.env['CURSOR_API_KEY'];
    if (!apiKey) {
      this._state = 'failed';
      this._errorDetail = 'CURSOR_API_KEY environment variable not set';
      this._broadcast({ type: 'text', content: `[error] ${this._errorDetail}` });
      return;
    }

    return new Promise<void>((resolve) => {
      this._proc = spawn(
        AGENT_BIN,
        ['-p', '--output-format', 'stream-json', '--force', '--workspace', this.workspace, bootstrapPrompt],
        {
          env: { ...process.env, CURSOR_API_KEY: apiKey },
          stdio: ['ignore', 'pipe', 'pipe'],
          shell: true,
        },
      );

      const rl = createInterface({ input: this._proc.stdout! });
      rl.on('line', (line) => {
        if (!line.trim()) return;
        try {
          const event = JSON.parse(line) as Record<string, unknown>;
          this._handleCliEvent(event);
        } catch {
          // non-JSON line — treat as raw text
          if (line.trim()) {
            this._messageCount++;
            this._lastActivityTs = Date.now();
            this._broadcast({ type: 'text', content: line });
          }
        }
      });

      const stderrChunks: Buffer[] = [];
      this._proc.stderr!.on('data', (chunk: Buffer) => stderrChunks.push(chunk));

      this._proc.on('close', (code) => {
        rl.close();
        if (this._state === 'running') {
          if (code === 0) {
            this._state = 'completed';
            this._finalMessage = `${this.role} session complete`;
            this._broadcast({ type: 'text', content: `[done] ${this.role} session complete` });
          } else {
            this._state = 'failed';
            const stderr = Buffer.concat(stderrChunks).toString().trim();
            this._errorDetail = stderr || `agent exited with code ${code}`;
            this._broadcast({ type: 'text', content: `[error] ${this._errorDetail}` });
          }
        }
        this._proc = null;
        resolve();
      });

      this._proc.on('error', (err) => {
        this._state = 'failed';
        this._errorDetail = err.message;
        this._broadcast({ type: 'text', content: `[error] ${err.message}` });
        this._proc = null;
        resolve();
      });
    });
  }

  stop(): void {
    if (this._proc) {
      this._proc.kill();
      this._proc = null;
    }
    this._state = 'completed';
  }

  // ─── CLI event parsing ─────────────────────────────────────────────────────

  private _handleCliEvent(event: Record<string, unknown>): void {
    const type = event['type'] as string | undefined;

    if (type === 'assistant') {
      // Both streaming deltas (has timestamp_ms, no model_call_id) and
      // buffered flushes (has model_call_id) carry text blocks.
      const msg = event['message'] as Record<string, unknown> | undefined;
      const content = (msg?.['content'] as Array<Record<string, unknown>>) ?? [];
      for (const block of content) {
        if (block['type'] === 'text' && typeof block['text'] === 'string') {
          this._messageCount++;
          this._lastActivityTs = Date.now();
          this._broadcast({ type: 'text', content: block['text'] });
        }
      }
    } else if (type === 'tool_call') {
      const subtype = event['subtype'] as string | undefined;
      if (subtype === 'started') {
        this._lastActivityTs = Date.now();
        this._broadcast({ type: 'thinking' });
      }
    } else if (type === 'result') {
      this._state = 'completed';
      this._finalMessage = `${this.role} session complete`;
    }
  }

  // ─── Streaming ─────────────────────────────────────────────────────────────

  addListener(fn: SdkStreamListener): void {
    this._listeners.add(fn);
  }

  removeListener(fn: SdkStreamListener): void {
    this._listeners.delete(fn);
  }

  private _broadcast(event: AgentOutputEvent): void {
    for (const fn of this._listeners) {
      fn(event);
    }
  }

  // ─── Status ────────────────────────────────────────────────────────────────

  getStatus(): SdkSessionStatus {
    const status: SdkSessionStatus = {
      state: this._state,
      messageCount: this._messageCount,
      lastActivitySec: Math.round((Date.now() - this._lastActivityTs) / 1000),
    };
    if (this._finalMessage) status.finalMessage = this._finalMessage;
    if (this._errorDetail) status.errorDetail = this._errorDetail;
    return status;
  }

  get state(): SdkSessionState {
    return this._state;
  }
}
