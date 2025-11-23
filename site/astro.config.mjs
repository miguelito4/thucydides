import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel/static';

export default defineConfig({
  site: 'https://thucydides.caseyjr.org',
  output: 'static',
  adapter: vercel({
    webAnalytics: { enabled: true }
  }),
  build: {
    inlineStylesheets: 'auto',
  }, 
  vite: {
    server: {
      fs: {
        allow: ['..'],
      },
    },
  },
});