import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: '*.test.js',
  timeout: 15000,
  use: {
    baseURL: 'https://mybaseline.health',
  },
});
