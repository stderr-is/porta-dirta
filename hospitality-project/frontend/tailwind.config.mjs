// tailwind.config.mjs
// NOTE: This project uses Tailwind CSS v4, which uses CSS-based configuration
// via @theme directives in src/styles/global.css rather than this JS config file.
// This file is kept as a reference for the design system tokens.
// The authoritative token definitions live in src/styles/global.css.

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],

  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#0D2B45',        // Deep Mediterranean Blue — primary background
          'blue-light': '#1A4A6E', // Lighter blue for hover states
          gold: '#C9A84C',         // CTA / primary action colour
          coral: '#E07B5A',        // Alternative CTA
          sand: '#C4A882',         // Sandy neutral accent
          stone: '#8B7355',        // Warm stone accent
          white: '#FFFFFF',
          cream: '#FAF8F5',        // Off-white page background
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
