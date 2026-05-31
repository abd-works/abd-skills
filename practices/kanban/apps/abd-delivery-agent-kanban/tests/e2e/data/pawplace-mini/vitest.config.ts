import react from '@vitejs/plugin-react';
import path from 'node:path';
import { defineConfig } from 'vitest/config';

const root = __dirname;

export default defineConfig({
  plugins: [react()],
  test: {
    include: [
      'tests/**/*_server.test.ts',
      'tests/**/*_client.test.tsx',
      'packages/**/tests/**/*_domain.test.ts',
    ],
    exclude: ['**/*_e2e.spec.ts'],
    environment: 'jsdom',
    globals: true,
    setupFiles: [path.join(root, 'vitest.setup.ts')],
  },
  resolve: {
    alias: {
      '@pawplace-mini/cart-shared': path.join(root, 'packages/cart/shared/src/index.ts'),
      '@pawplace-mini/cart-server': path.join(root, 'packages/cart/server/index.ts'),
      '@pawplace-mini/cart-client': path.join(root, 'packages/cart/client/index.ts'),
      '@pawplace-mini/catalog-client': path.join(root, 'packages/catalog/client/index.ts'),
      '@pawplace-mini/catalog-shared': path.join(root, 'packages/catalog/shared/src/index.ts'),
      '@pawplace-mini/catalog-server': path.join(root, 'packages/catalog/server/index.ts'),
      '@pawplace-mini/inventory-client': path.join(root, 'packages/inventory/client/index.ts'),
      '@pawplace-mini/app-server': path.join(root, 'packages/app-server/index.ts'),
      '@pawplace-mini/store-shared': path.join(root, 'packages/store/shared/index.ts'),
      '@pawplace-mini/store-server': path.join(root, 'packages/store/server/index.ts'),
      '@pawplace-mini/store-shared/mockStores': path.join(root, 'packages/store/shared/mockStores.ts'),
      '@pawplace-mini/store-shared/types': path.join(root, 'packages/store/shared/types.ts'),
      '@pawplace-mini/store-client': path.join(root, 'packages/store/client/index.ts'),
      '@pawplace-mini/store-client/store.api': path.join(root, 'packages/store/client/store.api.ts'),
      '@pawplace-mini/store-client/FindStoreLayout': path.join(root, 'packages/store/client/FindStoreLayout.tsx'),
      '@pawplace-mini/store-client/SelectedStoreContext': path.join(root, 'packages/store/client/SelectedStoreContext.tsx'),
      '@pawplace-mini/store-client/StoreListView': path.join(root, 'packages/store/client/StoreListView.tsx'),
      '@pawplace-mini/store-client/StoreMapView': path.join(root, 'packages/store/client/StoreMapView.tsx'),
      '@pawplace-mini/checkout-client': path.join(root, 'packages/checkout/client/index.ts'),
      '@pawplace-mini/checkout-shared': path.join(root, 'packages/checkout/shared/src/index.ts'),
      '@pawplace-mini/checkout-server': path.join(root, 'packages/checkout/server/index.ts'),
      '@pawplace-mini/fulfillment-client': path.join(root, 'packages/fulfillment/client/index.ts'),
      '@pawplace-mini/fulfillment-shared': path.join(root, 'packages/fulfillment/shared/src/index.ts'),
      '@pawplace-mini/fulfillment-server': path.join(root, 'packages/fulfillment/server/index.ts'),
    },
  },
});
