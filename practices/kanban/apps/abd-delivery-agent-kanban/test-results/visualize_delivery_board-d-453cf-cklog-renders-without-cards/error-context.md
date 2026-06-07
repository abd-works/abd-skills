# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visualize_delivery_board\display_board_layout\display_backlog_tickets_e2e.spec.ts >> Display Backlog Tickets >> Scenario 3: Empty backlog renders without cards
- Location: tests\e2e\visualize_delivery_board\display_board_layout\display_backlog_tickets_e2e.spec.ts:96:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[data-end-col="backlog"]')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('[data-end-col="backlog"]')

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
  8   |   updateJsonFile,
  9   | } from '../../e2e_support';
  10  | 
  11  | test.describe('Display Backlog Tickets', () => {
  12  |   test.beforeEach(() => {
  13  |     resetPawPlaceStubsFixture();
  14  |   });
  15  | 
  16  |   test('Scenario 1: Backlog tickets ordered by priority', async ({ page }) => {
  17  |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  18  |       const next = { ...board };
  19  |       next.done = [];
  20  |       next.archived = [];
  21  |       next.active = [
  22  |         {
  23  |           ticket_id: 'STORY-007',
  24  |           lineage: ['PetStore', 'Sprint 1', 'List Pets'],
  25  |           scope_level: 'sprint',
  26  |           stage: 'discovery',
  27  |           priority: 2,
  28  |           entered_stage: '2026-06-01T12:01:00Z',
  29  |           completed_stage: null,
  30  |           stage_history: [],
  31  |           scatter_from: null,
  32  |           scatter_to: [],
  33  |           notes: '',
  34  |           skill_progress: {},
  35  |           hold_in_progress: true,
  36  |         },
  37  |         {
  38  |           ticket_id: 'STORY-003',
  39  |           lineage: ['PetStore', 'Sprint 1', 'Add Pet'],
  40  |           scope_level: 'sprint',
  41  |           stage: 'discovery',
  42  |           priority: 1,
  43  |           entered_stage: '2026-06-01T12:00:00Z',
  44  |           completed_stage: null,
  45  |           stage_history: [],
  46  |           scatter_from: null,
  47  |           scatter_to: [],
  48  |           notes: '',
  49  |           skill_progress: {},
  50  |           hold_in_progress: true,
  51  |         },
  52  |       ];
  53  |       next.backlog = [];
  54  |       return next;
  55  |     });
  56  | 
  57  |     await goToBoard(page);
  58  |     const stageTickets = stageInProgressColumn(page, 'discovery');
  59  |     const story3 = stageTickets.locator('[data-ticket="STORY-003"]');
  60  |     const story7 = stageTickets.locator('[data-ticket="STORY-007"]');
  61  |     await expect(story3.getByText('Add Pet', { exact: true })).toBeVisible();
  62  |     await expect(story7.getByText('List Pets', { exact: true })).toBeVisible();
  63  |     await expect(stageTickets.locator('[data-ticket="STORY-003"], [data-ticket="STORY-007"]')).toHaveCount(2);
  64  |   });
  65  | 
  66  |   test('Scenario 2: Hovering backlog ticket shows full lineage', async ({ page }) => {
  67  |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  68  |       const next = { ...board };
  69  |       next.active = [
  70  |         {
  71  |           ticket_id: 'STORY-003',
  72  |           lineage: ['PetStore', 'Sprint 1', 'Add Pet'],
  73  |           scope_level: 'sprint',
  74  |           stage: 'discovery',
  75  |           priority: 1,
  76  |           entered_stage: '2026-06-01T12:00:00Z',
  77  |           completed_stage: null,
  78  |           stage_history: [],
  79  |           scatter_from: null,
  80  |           scatter_to: [],
  81  |           notes: '',
  82  |           skill_progress: {},
  83  |           hold_in_progress: true,
  84  |         },
  85  |       ];
  86  |       next.backlog = [];
  87  |       next.done = [];
  88  |       next.archived = [];
  89  |       return next;
  90  |     });
  91  | 
  92  |     await goToBoard(page);
  93  |     await expect(ticketCard(page, 'STORY-003')).toHaveAttribute('title', /PetStore > Sprint 1 > Add Pet/);
  94  |   });
  95  | 
  96  |   test('Scenario 3: Empty backlog renders without cards', async ({ page }) => {
  97  |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  98  |       const next = { ...board };
  99  |       next.active = [];
  100 |       next.backlog = [];
  101 |       next.done = [];
  102 |       next.archived = [];
  103 |       return next;
  104 |     });
  105 | 
  106 |     await goToBoard(page);
  107 |     const backlog = page.locator('[data-end-col="backlog"]');
> 108 |     await expect(backlog).toBeVisible();
      |                           ^ Error: expect(locator).toBeVisible() failed
  109 |     await expect(backlog.locator('[data-ticket]')).toHaveCount(0);
  110 |   });
  111 | });
  112 | 
```