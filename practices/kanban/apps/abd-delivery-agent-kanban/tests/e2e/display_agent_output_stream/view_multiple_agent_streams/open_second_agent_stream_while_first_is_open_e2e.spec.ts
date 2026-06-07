import { test } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Open Second Agent Stream While First Is Open', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test.skip('Scenario 1: Business-expert panel open, user clicks engineer — both panels visible', async () => {
    // TODO: implement — Scenario 1: Business-expert panel open, user clicks engineer — both panels visible
  });

  test.skip('Scenario 2: Three panels open — all three stack horizontally', async () => {
    // TODO: implement — Scenario 2: Three panels open — all three stack horizontally
  });
});
