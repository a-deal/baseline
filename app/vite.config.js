import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  base: '/baseline/app/',
  build: {
    outDir: 'dist',
  },
  server: {
    port: 8787,
  },
});
