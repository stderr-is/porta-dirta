---
type: design-system
project: Porta D'irta
status: active
tags: [ui, ux, cro, astro, events]
---

# 🎨 Hospitality UI/UX & Conversion Design System — Porta D'irta

## 0. Brand Identity
* **Name:** Porta D'irta
* **Logo:** Negative (white) version on transparent background — `https://portadirta.com/wp-content/uploads/2026/02/LOGO-negativo.png`
  * Always used on dark or blurred backgrounds (hero, nav overlays, footers)
  * Never place on white/light backgrounds without a dark backing layer


## 1. The Core Philosophy: "Guided Mediterranean Elegance"
The digital presence must mirror the physical property: spacious, elegant, and perfectly situated by the sea. 
* **The "Functional Glass" Aesthetic:** UI overlays (like navigation and booking modules) use CSS backdrop-blur to maintain visibility of the stunning property photography and video, creating depth without clutter.
* **The Scroll Journey:** Pages are not endless dumps of text. They are curated journeys. The user scrolls through distinct, visually arresting sections (Rooms → Dining → Events → Local Collabs) that naturally funnel down to a final booking widget.

## 2. The Visual Language
* **Color Palette:**
  * **Primary:** Deep Mediterranean Blue and crisp Whites.
  * **Secondary:** Sandy neutrals and warm stone colors.
  * **Action/CTA:** A refined, high-contrast gold or warm coral to draw the eye to booking widgets.
* **Imagery Directive:** The primary asset is motion. The entry point must feature a high-quality, auto-playing video of the villa, the pool, the gardens, and the beach proximity. 

## 3. The Conversion Architecture
* **The Hotel (Main Hub):** Aggressive cross-selling. The booking engine (Beds24) must be configured to offer Restaurant meals (Breakfast/Lunch/Dinner) and local collaborations (Sierra de Irta trips, beach services) as **direct add-ons at the time of room reservation**.
* **The Entry Point:** A hero video background overlaid immediately with the Beds24 availability widget. Zero friction to start the booking process.
* **The Restaurant (Standalone Focus):** Targeted at locals and walk-ins. Features Fixed, Weekly, and Seasonal menus. Links back to the hotel/events are present in the functional header, but there are no aggressive room-booking popups.
* **The Events Space:** Dedicated sections for Weddings, Communions, and Birthdays, highlighting the gardens and tennis court, utilizing inquiry forms and Hi.Events where applicable.
