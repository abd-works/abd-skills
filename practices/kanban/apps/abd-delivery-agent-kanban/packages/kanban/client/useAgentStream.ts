import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Streamed message from an agent session via GET /api/board/agent/:role/stream (SSE).
 */
export interface AgentStreamMessage {
  type: 'text' | 'thinking' | 'status';
  content?: string;
  state?: string;
}

/**
 * View model for a single agent stream panel.
 */
export interface AgentStreamPanelView {
  role: string;
  anchoredStage: string | null;
  messages: AgentStreamMessage[];
  isThinking: boolean;
  sessionState: 'running' | 'completed' | 'failed' | 'idle';
}

/**
 * useAgentStream — subscribes to the SSE stream for one agent role.
 *
 * Opens GET /api/board/agent/:role/stream and maps events to typed messages.
 * Cleans up the EventSource on unmount or when the role changes.
 */
export function useAgentStream(role: string | null): {
  messages: AgentStreamMessage[];
  isThinking: boolean;
  sessionState: AgentStreamPanelView['sessionState'];
  clearMessages: () => void;
} {
  const [messages, setMessages] = useState<AgentStreamMessage[]>([]);
  const [isThinking, setIsThinking] = useState(false);
  const [sessionState, setSessionState] = useState<AgentStreamPanelView['sessionState']>('idle');
  const esRef = useRef<EventSource | null>(null);

  const clearMessages = useCallback(() => setMessages([]), []);

  useEffect(() => {
    if (!role) return;

    const es = new EventSource(`/api/board/agent/${role}/stream`);
    esRef.current = es;

    es.onmessage = (e: MessageEvent<string>) => {
      try {
        const event = JSON.parse(e.data) as AgentStreamMessage;
        if (event.type === 'thinking') {
          setIsThinking(true);
        } else if (event.type === 'text') {
          setIsThinking(false);
          setMessages((prev) => [...prev, event]);
        } else if (event.type === 'status') {
          const st = event.state as AgentStreamPanelView['sessionState'];
          setSessionState(st ?? 'idle');
          if (st !== 'running') setIsThinking(false);
        }
      } catch {
        // ignore malformed events
      }
    };

    es.onerror = () => {
      setSessionState('idle');
      es.close();
    };

    return () => {
      es.close();
      esRef.current = null;
    };
  }, [role]);

  return { messages, isThinking, sessionState, clearMessages };
}
