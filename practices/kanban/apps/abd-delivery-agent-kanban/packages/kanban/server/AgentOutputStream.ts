/**
 * domain model: AgentOutputStream — carries a single streamed event from an agent session.
 *      Emitted by AgentSession.emit(); consumed by the server relay and the
 *      client stream panel.
 */

export type AgentOutputEvent =
  | { type: 'text'; content: string }
  | { type: 'thinking' };

export class AgentOutputStream {
  private readonly _event: AgentOutputEvent;

  constructor(event: AgentOutputEvent) {
    this._event = event;
  }

  lastMessage(): string {
    return this._event.type === 'text' ? this._event.content : '';
  }

  isThinking(): boolean {
    return this._event.type === 'thinking';
  }

  get event(): AgentOutputEvent {
    return this._event;
  }
}
