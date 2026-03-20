---
type: design-system
project: Porta D'irta
status: active
tags: [ui, ux, cro, astro, events]
---

# 🎨 Hospitality UI/UX & Conversion Design System — Porta D'irta

## 0. Brand Identity
* **Name:** Porta D'irta
* **Logo:** Two local files — never use the old WP URL
  * `frontend/public/assets/logos/logo-negativo.png` — white on transparent, used on dark/blurred backgrounds (nav, footer, hero)
  * `frontend/public/assets/logos/logo-positivo.png` — dark on light background (print, email templates)
  * Public paths: `/assets/logos/logo-negativo.png` and `/assets/logos/logo-positivo.png`
* **Contact (from business card):** Camí del Pebret, s/n · 12598 Peñíscola · +34 644 026 066 · +34 632 460 981 · info@portadirta.com

## 0b. Real Media Assets (2026-03-20 session)
All assets in `frontend/public/assets/`:
* **Video:** `video/hero.mp4` — 20s drone composite, 2.6MB, 1280p, no audio. Poster: `video/hero-poster.jpg`
* **Room interiors:** `images/room-1.jpg` through `room-4.jpg` — actual guest bedrooms
* **Food/Restaurant:** `food-paella-close.jpg`, `food-paella-table.jpg`, `food-paella-wine.jpg`, `food-paella-serving.jpg`
* **Aerial/Property:** `property-aerial-twilight.jpg`, `property-aerial-pool.jpg`, `property-aerial-dusk.jpg`
* **Restaurant settings:** `restaurant-aerial.jpg`, `restaurant-terrace.jpg`
* **Sierra/Landscape:** `sierra-tower-sea.jpg`, `sierra-tower-wide.jpg`, `sierra-trail-vertical.jpg`, `terrace-breakfast.jpg`

## 1. The Core Philosophy: "Guided Mediterranean Elegance"
The digital presence must mirror the physical property: spacious, elegant, and perfectly situated by the sea.
* **The "Functional Glass" Aesthetic:** UI overlays (like navigation and booking modules) use CSS backdrop-blur to maintain visibility of the stunning property photography and video, creating depth without clutter.
* **The Scroll Journey:** Pages are not endless dumps of text. They are curated journeys. The user scrolls through distinct, visually arresting sections (Rooms → Dining → Events → Local Collabs) that naturally funnel down to a final booking widget.

## 2. The Visual Language
* **Color Palette (CORRECTED 2026-03-20 — warm earthy Mediterranean, not deep navy):**
  * **Background:** `#F5F0E8` warm cream — page bg
  * **Primary text:** `#2C2018` dark charcoal-brown
  * **Brand earth:** `#B8A490` sandy taupe — brand primary surface
  * **Linen:** `#EDE8DF` — card backgrounds
  * **Gold CTA:** `#C9A84C` — all primary CTAs and accent lines
  * **Terracotta:** `#C05A3A` — accent (from roof tiles in photos)
  * **Stone:** `#8B7355` — secondary text / hover state for CTAs
  * **Deep navy:** `#0D2B45` — dark sections (footer, hero overlays) only — NOT primary brand colour
* **Imagery Directive:** Hero = drone video (`hero.mp4`). Each page has real property photography. No more picsum placeholders.

## 3. The Conversion Architecture
* **The Hotel (Main Hub):** Aggressive cross-selling. The booking engine (Beds24) must be configured to offer Restaurant meals (Breakfast/Lunch/Dinner) and local collaborations (Sierra de Irta trips, beach services) as **direct add-ons at the time of room reservation**.
* **The Entry Point:** A hero video background overlaid immediately with the Beds24 availability widget. Zero friction to start the booking process.
* **The Restaurant (Standalone Focus):** Targeted at locals and walk-ins. Features Fixed, Weekly, and Seasonal menus. Links back to the hotel/events are present in the functional header, but there are no aggressive room-booking popups.
* **The Events Space:** Dedicated sections for Weddings, Communions, and Birthdays, highlighting the gardens and tennis court, utilizing inquiry forms and Hi.Events where applicable.
