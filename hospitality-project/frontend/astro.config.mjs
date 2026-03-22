// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import node from '@astrojs/node';

// BUILD_TARGET=node → SSR for Hostinger VPS (output: 'server' + node adapter)
// default           → SSG for Cloudflare Pages (output: 'static', no adapter)
const isNode = process.env.BUILD_TARGET === 'node';

// https://astro.build/config
export default defineConfig({
  output: isNode ? 'server' : 'static',
  trailingSlash: 'never',

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
