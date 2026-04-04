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
- [x] **Restaurant Sub-menus:** Add detail pages for specific menu sections. (Done 2026-04-03)
- [ ] **Experiencias/Eventos:** Detail pages for unique offerings.
- [x] **AI Automation:** Integrate n8n workflows for automated tasks (e.g., event processing, customer support). (Done 2026-04-03)
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

## 2026-04-03 Progress Notes
- [x] Menu bot command pipeline stabilized for `/bebidas` and `/taperia` with production deployment protocol enforced after each n8n workflow change.
- [x] Multilingual menu rendering fixed on `[lang]` pages (`menu`, `taperia`, `bebidas`, `desayuno`, `streetfood`) with safe merge of translated text over base structured menu data.
- [x] Localized table hub routes `/en/mesa`, `/fr/mesa`, `/de/mesa` fixed and fully translated labels deployed.
- [x] Security hardening baseline: docker secrets externalized from compose, internal token moved to env vars, n8n/uptime images pinned, tracked memory credentials sanitized. (Done 2026-04-04)
- [x] Performance/SEO/a11y/infra hardening pass: self-hosted fonts, hero video compressed + WebM source, JSON-LD added to home/hotel/event pages, accessible mobile nav toggle state, legal CIF surfaced in footer, Docker DB healthchecks + service_healthy dependencies, and shared volume permissions tightened. (Done 2026-04-04)
