import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tests/**/*.test.ts', 'tests/**/*.test.tsx'],
    exclude: ['tests/**/*_e2e.spec.ts', 'tests/e2e/**', 'node_modules/**'],
    globals: true,
    environment: 'jsdom',
  },
});
