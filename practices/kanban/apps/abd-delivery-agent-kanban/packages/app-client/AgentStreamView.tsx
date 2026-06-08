import { useEffect, useRef } from 'react';
import { useAgentStream } from '@deliveryforge/kanban-client';
import { Heartbeat } from '@deliveryforge/kanban-client';
import type { AgentRole } from '@deliveryforge/kanban-shared';

/**
 * AgentStreamView — displays live agent output beside the active ticket stage column.
 *
 * Connects to GET /api/board/agent/:role/stream (SSE) and renders:
 *   - Text message bubbles (like IDE chat)
 *   - Thinking indicator animation while the model is processing
 *   - Completion / error status banners
 *   - A close button to collapse the view
 */
export function AgentStreamView({
  role,
  onClose,
}: {
  role: AgentRole;
  onClose: () => void;
}) {
  const { messages, isThinking, sessionState, clearMessages } = useAgentStream(role);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isThinking]);

  const label = Heartbeat.roleFullName(role);

  return (
    <div className="kb-stream-panel" data-role={role}>
      <div className="kb-stream-panel-header">
        <span className="kb-stream-panel-title">{label}</span>
        <div className="kb-stream-panel-actions">
          <button
            className="kb-stream-panel-btn"
            onClick={clearMessages}
            title="Clear messages"
          >
            ⌫
          </button>
          <button
            className="kb-stream-panel-close"
            onClick={onClose}
            title="Close stream view"
          >
            ✕
          </button>
        </div>
      </div>

      <div className="kb-stream-panel-body">
        {messages.length === 0 && !isThinking && sessionState === 'idle' && (
          <div className="kb-stream-empty">No active session</div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className="kb-stream-bubble">
            {msg.content}
          </div>
        ))}

        {isThinking && (
          <div className="kb-stream-thinking">
            <span className="kb-stream-dot" />
            <span className="kb-stream-dot" />
            <span className="kb-stream-dot" />
          </div>
        )}

        {sessionState === 'completed' && (
          <div className="kb-stream-status kb-stream-status--done">Session complete</div>
        )}
        {sessionState === 'failed' && (
          <div className="kb-stream-status kb-stream-status--error">Session failed</div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
