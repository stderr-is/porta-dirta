// tailwind.config.mjs
// NOTE: This project uses Tailwind CSS v4, which uses CSS-based configuration
// via @theme directives in src/styles/global.css rather than this JS config file.
// This file is kept as a reference for the design system tokens and for tools
// that do not yet support CSS-only configuration.
// The authoritative token definitions live in src/styles/global.css.

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],

  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#0D2B45',         // Deep nav/overlay dark
          'blue-light': '#1A4A6E', // Hover state
          earth: '#B8A490',        // Warm sandy taupe
          linen: '#EDE8DF',        // Light linen
          cream: '#F5F0E8',        // Warm cream page background
          gold: '#C9A84C',         // CTA / primary action
          terracotta: '#C05A3A',   // Accent
          sand: '#C4A882',         // Sandy neutral accent
          stone: '#8B7355',        // Warm stone (body text)
          charcoal: '#2C2018',     // Dark charcoal-brown
          white: '#FFFFFF',
          olive: '#4A5E2A',        // Deep olive
          sage:  '#7A8F52',        // Sage green
          forest: '#2C4A3C',       // Muted sage-teal
          'sage-light': '#c8deb0', // Light sage
        },
      },

      fontFamily: {
        display: ['Cormorant Garamond', 'serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },

  plugins: [],
};
