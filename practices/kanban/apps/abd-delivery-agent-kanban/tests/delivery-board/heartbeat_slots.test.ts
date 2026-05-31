import { describe, it, expect } from 'vitest';
import {
  buildHeartbeatSlots,
  parseHeartbeatFileName,
} from '@deliveryforge/delivery-board-shared';

describe('parseHeartbeatFileName', () => {
  it('parses primary and suffixed instance files', () => {
    expect(parseHeartbeatFileName('heartbeat-business-expert.json')).toEqual({
      role: 'business-expert',
      slotKey: '',
    });
    expect(parseHeartbeatFileName('heartbeat-business-expert-be2.json')).toEqual({
      role: 'business-expert',
      slotKey: 'be2',
    });
    expect(parseHeartbeatFileName('heartbeat-kanban-lead.json')).toEqual({
      role: 'kanban-lead',
      slotKey: '',
    });
  });
});

describe('buildHeartbeatSlots', () => {
  const now = Date.parse('2026-05-30T23:20:00Z');

  it('orders primary slot before suffixed instances', () => {
    const slots = buildHeartbeatSlots(
      [
        {
          fileName: 'heartbeat-business-expert-be2.json',
          raw: { ts: '2026-05-30T23:18:00Z', status: 'ready' },
        },
        {
          fileName: 'heartbeat-business-expert.json',
          raw: { ts: '2026-05-30T23:19:00Z', status: 'ready' },
        },
      ],
      now,
    );

    expect(slots['business-expert']).toHaveLength(2);
    expect(slots['business-expert']![0].status).toBe('ready');
    expect(slots['business-expert']![1].status).toBe('ready');
    expect(slots['business-expert']![0].ageSeconds).toBe(60);
    expect(slots['business-expert']![1].ageSeconds).toBe(120);
  });
});
