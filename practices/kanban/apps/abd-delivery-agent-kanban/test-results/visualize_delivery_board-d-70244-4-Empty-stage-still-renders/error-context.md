# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visualize_delivery_board\display_board_layout\organize_tickets_into_stage_groups_by_delivery_phase_e2e.spec.ts >> Organize Tickets into Stage Groups by Delivery Phase >> Scenario 4: Empty stage still renders
- Location: tests\e2e\visualize_delivery_board\display_board_layout\organize_tickets_into_stage_groups_by_delivery_phase_e2e.spec.ts:174:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.kb-stage-group[data-stage="shaping"]')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('.kb-stage-group[data-stage="shaping"]')

```

```yaml
- banner:
  - text: Agentic Agile Delivery
  - heading "Kanban Board — …" [level=1]
  - group "Display mode":
    - button "Executive"
    - button "Engineering"
  - link "home":
    - /url: /
- text: Planning folder
- textbox "Planning folder":
  - /placeholder: C:/dev/.../docs/planning
  - text: C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning
- button "Connect"
- button "Use stubs"
- button "Refresh"
- text: "Polled Unexpected token ' ', \" { \"sch\"... is not valid JSON"
```

# Test source

```ts
  102 |           stage_history: [],
  103 |           scatter_from: null,
  104 |           scatter_to: [],
  105 |           notes: '',
  106 |           skill_progress: {
  107 |             'abd-domain-model': {
  108 |               execution_status: 'done',
  109 |               review_status: 'done',
  110 |               agent: 'business-expert',
  111 |               reviewer: 'business-expert',
  112 |             },
  113 |           },
  114 |         },
  115 |       ];
  116 |       next.backlog = [
  117 |         {
  118 |           ticket_id: 'inc-sprint-a',
  119 |           lineage: ['PawPlace', 'Sprint A'],
  120 |           scope_level: 'sprint',
  121 |           stage: 'specification',
  122 |           priority: 1,
  123 |           entered_stage: '2026-06-01T12:00:00Z',
  124 |           completed_stage: null,
  125 |           stage_history: [],
  126 |           scatter_from: null,
  127 |           scatter_to: [],
  128 |           notes: '',
  129 |           skill_progress: {},
  130 |         },
  131 |       ];
  132 |       next.archived = [];
  133 |       return next;
  134 |     });
  135 | 
  136 |     await goToBoard(page);
  137 |     const specification = stageColumn(page, 'specification');
  138 |     await expect(specification.getByText('In Progress', { exact: true })).toBeVisible();
  139 |     await expect(specification.getByText('Done', { exact: true })).toBeVisible();
  140 |     await expect(stageDoneColumn(page, 'specification').getByText('Queued', { exact: true })).toHaveCount(0);
  141 |     await expect(specification.locator('[data-ticket="inc-sprint-a"]')).toHaveCount(0);
  142 |     await expect(specification.locator('[data-ticket="inc-sprint-b"]')).toBeVisible();
  143 |     await expect(specification.locator('[data-ticket="inc-sprint-c"]')).toBeVisible();
  144 |     await expectTicketNotInGlobalBacklog(page, 'inc-sprint-a');
  145 |   });
  146 | 
  147 |   test('Scenario 3: Stage queue tickets do not appear in global Backlog', async ({ page }) => {
  148 |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  149 |       const next = { ...board };
  150 |       next.backlog = [
  151 |         {
  152 |           ticket_id: 'inc-sprint-a',
  153 |           lineage: ['PawPlace', 'Sprint A'],
  154 |           scope_level: 'sprint',
  155 |           stage: 'specification',
  156 |           priority: 1,
  157 |           entered_stage: '2026-06-01T12:00:00Z',
  158 |           completed_stage: null,
  159 |           stage_history: [],
  160 |           scatter_from: null,
  161 |           scatter_to: [],
  162 |           notes: '',
  163 |           skill_progress: {},
  164 |         },
  165 |       ];
  166 |       return next;
  167 |     });
  168 | 
  169 |     await goToBoard(page);
  170 |     await expect(stageColumn(page, 'specification').locator('[data-ticket="inc-sprint-a"]')).toHaveCount(0);
  171 |     await expectTicketNotInGlobalBacklog(page, 'inc-sprint-a');
  172 |   });
  173 | 
  174 |   test('Scenario 4: Empty stage still renders', async ({ page }) => {
  175 |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  176 |       const next = { ...board };
  177 |       next.active = [
  178 |         {
  179 |           ticket_id: '200',
  180 |           lineage: ['PawPlace', 'Exploration Story'],
  181 |           scope_level: 'increment',
  182 |           stage: 'exploration',
  183 |           priority: 1,
  184 |           entered_stage: '2026-06-01T12:00:00Z',
  185 |           completed_stage: null,
  186 |           stage_history: [],
  187 |           scatter_from: null,
  188 |           scatter_to: [],
  189 |           notes: '',
  190 |           skill_progress: {},
  191 |           hold_in_progress: true,
  192 |         },
  193 |       ];
  194 |       next.backlog = [];
  195 |       next.done = [];
  196 |       next.archived = [];
  197 |       return next;
  198 |     });
  199 | 
  200 |     await goToBoard(page);
  201 |     const shaping = stageColumn(page, 'shaping');
> 202 |     await expect(shaping).toBeVisible();
      |                           ^ Error: expect(locator).toBeVisible() failed
  203 |     await expect(shaping.locator('[data-ticket]')).toHaveCount(0);
  204 |   });
  205 | });
  206 | 
```