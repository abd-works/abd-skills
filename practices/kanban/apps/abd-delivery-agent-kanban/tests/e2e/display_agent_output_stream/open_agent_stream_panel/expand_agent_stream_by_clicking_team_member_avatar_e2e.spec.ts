import { test } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Expand Agent Stream by Clicking Team Member Avatar', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test.skip('Scenario 1: User clicks engineer avatar with active ticket — stream panel opens beside stage column', async () => {
    // TODO: implement — Scenario 1: User clicks engineer avatar with active ticket — stream panel opens beside stage column
  });

  test.skip('Scenario 2: User clicks avatar with no active session — panel shows "No active session"', async () => {
    // TODO: implement — Scenario 2: User clicks avatar with no active session — panel shows "No active session"
  });
});
