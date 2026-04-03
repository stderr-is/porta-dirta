---
type: design-system
project: Peñíscola Off-Grid Retreat
status: active
tags: [ui, ux, cro, astro, sustainability]
---

# 🎨 Hospitality UI/UX & Conversion Design System (2026)

## 1. The Core Philosophy: "Transparent Sustainability"
The digital presence must mirror the physical property: highly efficient, completely independent (Astro + self-hosted backend), and radically transparent.
* **Zero UI Bloat:** No loading screens, no heavy JavaScript animations. The site must load instantly, reflecting the efficiency of the 4800W + 5000W solar arrays powering the property.
* **The "Functional Glass" Aesthetic:** UI overlays (like booking modals or navigation bars) use CSS backdrop-blur (`backdrop-filter: blur(10px)`). This creates a modern, premium feel while keeping the focus on the high-resolution background imagery of the farm, the food, and the coast.

## 2. The Visual Language
* **Color Palette:**
  * **Primary (The Land):** Terracotta and Sun-baked clay to reflect the Peñíscola environment.
  * **Secondary (The Farm):** Sage Green and Olive, representing the agricultural aspect (goats, chickens, mushroom cultivation).
  * **Base/Surface:** Clean off-whites for maximum readability.
  * **Action/CTA:** Deep Charcoal or a stark, high-contrast hue for booking buttons.
* **Typography:**
  * **Headings:** An elegant, modern Serif (communicates luxury, heritage, and the culinary quality of the brother-in-law's restaurant).
  * **Body:** A highly readable, geometric Sans-Serif (ensures WCAG 3.0 compliance and perfect mobile legibility).
* **Imagery Directive:** STRICTLY NO STOCK PHOTOS. Authenticity is the ultimate luxury. Use real photos of the 4 lithium batteries, the SmartLife automation dashboards, the farm-hacked incubation systems, and the plated food. 

## 3. Conversion Architecture (Sequential Upselling)
Based on 2026 hospitality CRO data, we must avoid cognitive overload. The user journey flows strictly in one direction:
1. **The Hook:** The homepage focuses 100% on the 4 rooms and the off-grid experience.
2. **The Primary CTA:** A sticky "Book Your Stay" button remains at the bottom of the viewport on all mobile devices.
3. **The Sequential Catch:** * *First:* Secure the room via the Beds24 widget.
   * *Second:* ONLY AFTER the room is confirmed (e.g., on the success page or via automated email), present the TastyIgniter integration: *"Reserve your table for our farm-to-table dinner."*
   * *Third:* Present the Hi.Events integration: *"Join Saturday's cheese-making or mushroom cultivation workshop."*

## 4. Technical UI Constraints
* **Mobile-First Touch Targets:** All interactive elements must be easily tap-able via one-handed thumb reach, optimized for high-DPI screens.
* **Data-Driven Transparency:** Create a specific UI component (a "Live Tech" card) that can eventually pull real-time data from the Easun inverter or SmartLife system, displaying live solar generation or battery capacity to the guest.

## 2026-04-03 UI i18n Note

- The multilingual table hub (`/[lang]/mesa`) now follows per-locale labels for all user-visible card titles (breakfast, taperia, special menu, drinks, street food) while preserving existing visual component structure and spacing.
