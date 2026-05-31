import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

export default defineConfig({
  root: path.resolve(__dirname),
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://127.0.0.1:3001',
      '/health': 'http://127.0.0.1:3001',
    },
  },
  resolve: {
    alias: {
      '@deliveryforge/delivery-board-shared': path.resolve(__dirname, '../delivery-board/shared/index.ts'),
      '@deliveryforge/delivery-board-client': path.resolve(__dirname, '../delivery-board/client/index.ts'),
    },
  },
});
