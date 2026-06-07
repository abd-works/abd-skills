# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: manage_agent_lifecycle_via_cursor_sdk\bootstrap_agent_from_role_definition\resolve_agent_definition_from_role_e2e.spec.ts >> Resolve Agent Definition from Role >> Scenario 1: Role "engineer" resolves to its agent definition
- Location: tests\e2e\manage_agent_lifecycle_via_cursor_sdk\bootstrap_agent_from_role_definition\resolve_agent_definition_from_role_e2e.spec.ts:9:7

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import { resetPawPlaceStubsFixture } from '../../e2e_support';
  3  | 
  4  | test.describe('Resolve Agent Definition from Role', () => {
  5  |   test.beforeEach(() => {
  6  |     resetPawPlaceStubsFixture();
  7  |   });
  8  | 
  9  |   test('Scenario 1: Role "engineer" resolves to its agent definition', async ({ request }) => {
  10 |     const response = await request.get('http://127.0.0.1:3001/api/board/agent/engineer/definition');
> 11 |     expect(response.ok()).toBe(true);
     |                           ^ Error: expect(received).toBe(expected) // Object.is equality
  12 |     const payload = (await response.json()) as { role: string; path?: string };
  13 |     expect(payload.role).toBe('engineer');
  14 |   });
  15 | 
  16 |   test('Scenario 2: Role "kanban-lead" resolves to its agent definition', async ({ request }) => {
  17 |     const response = await request.get('http://127.0.0.1:3001/api/board/agent/kanban-lead/definition');
  18 |     expect(response.ok()).toBe(true);
  19 |     const payload = (await response.json()) as { role: string; path?: string };
  20 |     expect(payload.role).toBe('kanban-lead');
  21 |   });
  22 | 
  23 |   test.skip('Scenario 3: Unknown role returns error', async () => {
  24 |     // TODO: implement — Scenario 3: Unknown role returns error
  25 |   });
  26 | });
  27 | 
```