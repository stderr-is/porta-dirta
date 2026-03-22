// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import node from '@astrojs/node';

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

  ...(isNode && {
    adapter: node({ mode: 'standalone' }),
  }),

  // i18n routing — Spanish is the default with no URL prefix.
  // English, French, and German will be served at /en/, /fr/, /de/ respectively.
  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en', 'fr', 'de'],
    routing: {
      prefixDefaultLocale: false,
    },
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
