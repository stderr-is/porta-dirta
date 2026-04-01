---
type: roadmap
status: completed
tags: [wbs, planning, execution]
---

# 🗺️ Implementation Roadmap

## Phase 1: Initiation (Architecture & Infrastructure)
*Goal: Establish the foundation before a single line of code is written.*
- [x] **Finalize Architecture:** Document core systems (e.g., Backend API, Frontend framework, DB schema) in `_memory/00_Master_Architecture.md`. (Done 2026-03-15)
- [x] **Design System:** Create initial design tokens, components, and patterns in `_memory/04_Hospitality_Design_System.md`. (Done 2026-03-18)
- [x] **i18n Strategy:** Define translation file structure and dynamic routing approach. (Done 2026-03-28)

## Phase 2: MVP Core (Content & Infrastructure)
*Goal: Launch a basic, functional site covering the core user journeys (booking intent pages).*
- [x] **i18n Infrastructure:** Set up `ui.ts` and `utils.ts` for multi-locale support. (Done 2026-03-31)
- [x] **i18n Wave 1 (EN):** Full translation of core pages (`index`, `hotel`, `restaurante`, `reservar`, `contacto`). (Done 2026-03-31)
- [x] **SEO Priority 1:** Implement OG tags, robots.txt, and indexable HTML content. (Done 2026-03-20)
- [x] **i18n Wave 1 (FR/DE):** Add placeholder pages and basic `hreflang` tags. (Done 2026-03-31)
- [x] **Sitemap Migration:** Automate sitemap generation using `@astrojs/sitemap`. (Done 2026-03-31)

## Phase 3: Feature Expansion (Content & Integrations)
*Goal: Add rich content and key integrations.*
- [ ] **i18n Wave 2 (FR/DE):** Full translation of core pages.
- [ ] **Blog:** Implement blog content and structure.
- [ ] **Restaurant Sub-menus:** Add detail pages for specific menu sections.
- [ ] **Experiencias/Eventos:** Detail pages for unique offerings.
- [ ] **AI Automation:** Integrate n8n workflows for automated tasks (e.g., event processing, customer support).
- [ ] **SEO Priority 2:** Implement `hreflang` tags across all pages.

## Phase 4: Optimization (SEO & Conversion)
*Goal: Ensure the site is found by the right guests and converts visitors into bookings.*
- [x] **Mobile UX:** Add sticky "Book Now" bar and WhatsApp FAB for CRO.
- [x] **Transparency:** Add live sustainability status component (mocked).
- [ ] **AI Crawler directives** — GPTBot/ClaudeBot/PerplexityBot allowed; CCBot/omgili blocked in robots.txt.

## Phase 5: Maintenance & Operations
*Goal: Keep the site running smoothly and securely.*
- [ ] **Testing:** Add end-to-end tests for core booking flows.
- [ ] **Monitoring:** Set up uptime monitoring for critical services.
- [ ] **Infrastructure:** Establish maintenance schedule (e.g., Ubuntu/Docker updates on Tuesday mornings).
**Tech Stack:** OBS Studio (Screen recording for SOPs).
