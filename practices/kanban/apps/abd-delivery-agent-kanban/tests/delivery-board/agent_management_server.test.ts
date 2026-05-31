/**

 * Agent Management Tests

 *

 * Stories: Indicate Agent Liveness from Heartbeat,

 *          Show Role Engagement in Agent Pool,

 *          Scale Agent Pool Up or Down

 */

import { describe, it, expect } from 'vitest';

import {

  resolvePoolAvatarState,

  HEARTBEAT_STALE_SECS,

} from '@deliveryforge/delivery-board-shared';



// ============================================================================

// HELPER FUNCTIONS — Pool avatar state (mirrors specification scenarios)

// ============================================================================



function when_board_resolves_pool_avatar(

  slotIndex: number,

  engagedCount: number,

  heartbeatAgeSeconds: number | null,

): 'idle' | 'working' | 'inactive' {

  return resolvePoolAvatarState(

    slotIndex,

    engagedCount,

    heartbeatAgeSeconds,

    HEARTBEAT_STALE_SECS,

  );

}



// ============================================================================

// HELPER FUNCTIONS — Scale Agent Pool (domain model stub)

// ============================================================================



interface Team {

  pool: Record<string, { executor_count: number; reviewer_count: number }>;

}



interface AgentPoolGroup {

  agent_role: string;

  executor_count: number;

  can_increment: boolean;

  can_decrement: boolean;

}



function given_team_with_executors(agent_role: string, executor_count: number): Team {

  return {

    pool: {

      [agent_role]: { executor_count, reviewer_count: 1 },

    },

  };

}



function when_delivery_lead_adds_executor(team: Team, agent_role: string): Team {

  const current = team.pool[agent_role] ?? { executor_count: 0, reviewer_count: 1 };

  return {

    pool: {

      ...team.pool,

      [agent_role]: {

        ...current,

        executor_count: current.executor_count + 1,

      },

    },

  };

}



function when_delivery_lead_removes_executor(team: Team, agent_role: string): Team {

  const current = team.pool[agent_role] ?? { executor_count: 0, reviewer_count: 1 };

  const new_count = Math.max(0, current.executor_count - 1);

  return {

    pool: {

      ...team.pool,

      [agent_role]: {

        ...current,

        executor_count: new_count,

      },

    },

  };

}



function when_delivery_lead_views_pool_group(

  team: Team,

  agent_role: string,

): AgentPoolGroup {

  const entry = team.pool[agent_role] ?? { executor_count: 0, reviewer_count: 1 };

  return {

    agent_role,

    executor_count: entry.executor_count,

    can_increment: true,

    can_decrement: entry.executor_count > 0,

  };

}



function then_team_shows_executors(

  team: Team,

  agent_role: string,

  expected_count: number,

): void {

  const entry = team.pool[agent_role];

  expect(entry).toBeDefined();

  expect(entry!.executor_count).toBe(expected_count);

}



function then_decrement_button_is_disabled(group: AgentPoolGroup): void {

  expect(group.can_decrement).toBe(false);

}



function then_increment_button_is_available(group: AgentPoolGroup): void {

  expect(group.can_increment).toBe(true);

}



// ============================================================================

// STORY: Indicate Agent Liveness from Heartbeat

// ============================================================================



describe('Indicate Agent Liveness from Heartbeat', () => {

  it('agent alive — heartbeat recent', () => {

    expect(when_board_resolves_pool_avatar(0, 0, 30)).toBe('idle');

    expect(when_board_resolves_pool_avatar(0, 1, 30)).toBe('working');

  });



  it('agent inactive — heartbeat stale with no engagement', () => {

    expect(when_board_resolves_pool_avatar(0, 0, 180)).toBe('inactive');

  });



  it('agent idle — no heartbeat file and no engagement', () => {

    expect(when_board_resolves_pool_avatar(0, 0, null)).toBe('idle');

  });

});



// ============================================================================

// STORY: Show Role Engagement in Agent Pool

// ============================================================================



describe('Show Role Engagement in Agent Pool', () => {

  it('engaged slot working without heartbeat', () => {

    expect(when_board_resolves_pool_avatar(0, 1, null)).toBe('working');

  });



  it('engaged slot working despite stale heartbeat', () => {

    expect(when_board_resolves_pool_avatar(0, 1, 180)).toBe('working');

  });



  it('unengaged slot inactive when heartbeat stale', () => {

    expect(when_board_resolves_pool_avatar(1, 1, 180)).toBe('inactive');

  });

});



// ============================================================================

// STORY: Scale Agent Pool Up or Down

// ============================================================================



describe('Scale Agent Pool Up or Down', () => {

  it('delivery lead adds an executor', () => {

    const team = given_team_with_executors('engineer', 2);

    const updated_team = when_delivery_lead_adds_executor(team, 'engineer');

    then_team_shows_executors(updated_team, 'engineer', 3);

  });



  it('delivery lead removes an executor', () => {

    const team = given_team_with_executors('business-expert', 2);

    const updated_team = when_delivery_lead_removes_executor(team, 'business-expert');

    then_team_shows_executors(updated_team, 'business-expert', 1);

  });



  it('cannot reduce below zero', () => {

    const team = given_team_with_executors('ux-designer', 0);

    const group = when_delivery_lead_views_pool_group(team, 'ux-designer');

    then_decrement_button_is_disabled(group);

    then_increment_button_is_available(group);

  });

});


