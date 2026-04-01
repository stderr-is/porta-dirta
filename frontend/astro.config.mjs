// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import node from '@astrojs/node';
import sitemap from '@astrojs/sitemap';

// BUILD_TARGET=node → SSR for Hostinger VPS (output: 'server' + node adapter)
// default           → SSG for Cloudflare Pages (output: 'static', no adapter)
const isNode = process.env.BUILD_TARGET === 'node';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.portadirta.com',
  output: isNode ? 'server' : 'static',
  trailingSlash: 'never',

  // Output flat .html files (hotel.html) instead of directories (hotel/index.html).
  // This prevents Cloudflare Pages from auto-redirecting /hotel → /hotel/ (308 loop).
  // SSR (Hostinger) ignores this — the node adapter handles routing itself.
  build: {
    format: 'file',
  },

  integrations: [sitemap()],

  ...(isNode && {
    adapter: node({ mode: 'standalone' }),
  }),

  // No Astro i18n routing — translations are handled client-side via
  // src/scripts/i18n-client.ts and data-i18n attributes.

  vite: {
    plugins: [tailwindcss()],
  },
});
