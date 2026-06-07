import { test } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Scale Agent Pool Up or Down', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test.skip('Scenario 1: Delivery Lead adds an executor', async () => {
    // TODO: implement — Scenario 1: Delivery Lead adds an executor
  });

  test.skip('Scenario 2: Delivery Lead removes an executor', async () => {
    // TODO: implement — Scenario 2: Delivery Lead removes an executor
  });

  test.skip('Scenario 3: Cannot reduce below zero', async () => {
    // TODO: implement — Scenario 3: Cannot reduce below zero
  });
});
