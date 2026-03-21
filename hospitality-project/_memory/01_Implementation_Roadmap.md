---
type: roadmap
status: in-progress
tags: [wbs, planning, execution]
---

# 🗺️ Implementation Roadmap

## Phase 1: Initiation (Architecture & Infrastructure)
*Goal: Establish the foundation before a single line of code is written.*
- [ ] Procure the Cloud PaaS (Platform as a Service) environment. *(using Cloudflare Tunnel as interim)*
- [x] Initialize GitHub repository and define Astro project structure.
- [ ] Register Beds24 account and initiate Booking.com XML authorization.
- [x] Set up DNS records — Cloudflare Tunnel CNAMEs on hobbitonranch.com (testing).
**Tech Stack:** Plane.so (PM), GitHub (VCS), Coolify/Railway (Hosting).
**Automation:** GitHub Action to auto-create tasks in Plane from a markdown "Ideas" folder.

## Phase 2: Planning (Prototyping & Database Prep)
*Goal: Lock in the exact layout, container limits, and data flow.*
- [x] Deploy TastyIgniter and Hi.Events Docker containers — running locally, exposed via Cloudflare Tunnel.
- [x] Map the physical restaurant floor plan digitally within TastyIgniter — 2 areas (Terraza + Interior), 30 tables via DB.
- [x] Generate Beds24 API V2 tokens and configure webhook endpoints.
- [x] Prototype the Astro `/experiences` page — built and live, fetches real Hi.Events prices at build time.
**Tech Stack:** Figma (UI), Docker Compose (Containers), Swagger UI (API Testing).
**Automation:** CI/CD pipeline in GitHub to auto-deploy the Astro static site in under 60 seconds.

## Phase 3: Execution (The Build & Integration)
*Goal: Wire systems together, focusing on layout stability and zero cross-system friction.*
- [x] Embed the Beds24 booking widget into the Astro frontend.
- [x] Build restaurant reservation API endpoint (TastyIgniter `/api/public/reservations`).
- [x] Build experience inquiry API endpoint (TastyIgniter `/api/public/contact`).
- [x] Create 4 live experiences in Hi.Events (Sierra de Irta, Kayak, Cata de Vinos, Castillo Papal).
- [x] Deploy Hi.Events full UI (all-in-one: nginx + PHP-FPM + React SSR).
- [x] TastyIgniter configured via DB: location, hours (Tue–Sun, lunch 13–16h + dinner 20–22h), 2 dining areas (Terraza + Interior), 30 tables.
- [x] Hi.Events admin: info@portadirta.com / Portadirta2026! — log in at https://events.hobbitonranch.com to set up check-in lists.
- [x] n8n: SMTP credential added, "Check-in Tomorrow" welcome email workflow created (Beds24 → guest email with restaurant + experiences links). Activate at https://n8n.hobbitonranch.com (stderr.is@gmail.com / Portadirta2026!)
- [x] Uptime Kuma monitoring added → https://monitor.hobbitonranch.com (first-run setup required in browser).
- [x] Replace all picsum placeholders with 17 real property photos (rooms, food, aerials, sierra).
- [x] Compress drone video → hero.mp4 (2.6MB, 20s, 1280p) with poster frame.
- [x] Serve logos locally (logo-negativo.png, logo-positivo.png) — removed WP URL dependency.
- [x] Correct brand palette → warm earthy Mediterranean (sandy taupe, linen, charcoal, terracotta).
- [x] Fix Nav/Footer: correct address (Camí del Pebret, s/n) and phone (+34 644 026 066).
- [ ] Configure Beds24 "Auto Actions" to send "Book a Table" email upon room confirmation.
- [x] Append URL parameters to restaurant link to pre-fill guest details in TastyIgniter. (Script in restaurante.astro reads `?fecha`, `personas`, `nombre`, `email`, `telefono` from URL and pre-fills form.)
- [x] Build Astro content collections for local collaboration events. (`src/content.config.ts` — two collections: `colaboradores` (4 partners) + `eventos-locales` (3 events). Wired into experiencias.astro partner tiles + eventos.astro upcoming events section.)
**Tech Stack:** Astro (Frontend HTML), n8n (Workflow Automation).
**Automation:** n8n listens for "Check-in Tomorrow" trigger to WhatsApp the guest their Hi.Events ticket QR code.

## Phase 3.5: AI Automation Layer
*Goal: Deploy AI orchestration so the property runs with minimal manual intervention.*
- [x] Add Anthropic API key + Telegram Bot credentials to n8n environment variables in `docker-compose.yml` (switched from Gemini — free tier quota issues)
- [x] Create Telegram Bot via @BotFather, get `TELEGRAM_BOT_TOKEN`, find admin `TELEGRAM_ADMIN_ID`
- [x] Uptime Kuma fully configured: 5 monitors + Telegram alerts (portadirta / Portadirta2026!)
- [x] TastyIgniter admin email changed to info@portadirta.com (was diogojorgepinto86@gmail.com — changed via DB)
- [x] Nature redesign approved and merged to master: sage-tinted bg, GarlandDivider, forest overlay on photos
- [x] Cloudflare Pages production branch confirmed as master
- [ ] Cloudflare Pages env vars still need setting in dashboard: PUBLIC_TASTYIGNITER_URL + PUBLIC_HIEVENTS_URL
- [ ] Import `workflow-a-silent-concierge.json` into n8n, wire IMAP credential
- [ ] Import `workflow-a2-callback-handler.json` into n8n, wire Telegram credential
- [x] Import `workflow-b-command-center.json` into n8n — ACTIVE at https://n8n.hobbitonranch.com (id: i87KV1SQXuhTCYxt)
- [ ] Import `workflow-c-yield-management.json` into n8n, wire Beds24 + Telegram + SMTP credentials
- [ ] Activate all 4 workflows, test Workflow A with a real test email to info@portadirta.com
- [x] Test Workflow B routing — FIXED (2026-03-20): n8n v2 IF node typeVersion 2 requires new condition format; all 5 IF nodes migrated. Bot now correctly routes text → Claude → API.
- [ ] **Configure `BEDS24_API_TOKEN`**: replace `REPLACE_WITH_BEDS24_V2_TOKEN` in `docker-compose.yml` then `docker compose up -d n8n` — bot returns 401 until this is set
- [ ] Test Workflow C: trigger manually, verify pricing recommendation appears in Telegram
- [ ] Verify Identity Router blocks unauthorized Telegram IDs
**Tech Stack:** Claude Haiku 4.5 API, Telegram Bot API, n8n (running at n8n.hobbitonranch.com).
**Reference:** `_memory/05_AI_Automation.md` — full blueprint with gap analysis.

## Phase 3.6: Hi.Events → Experiences Page Dynamic Integration
*Goal: Experiences page automatically reflects packages published in Hi.Events — no code changes needed to add/remove experiences.*

### Architecture
- **Flag system:** Hi.Events category `"Experiencias Porta D'irta"` (slug: `portadirta-featured`). Only events tagged with this category appear on the site.
- **Data fetch:** Build-time SSG fetch from Hi.Events public API — no CORS issues, great SEO.
- **Rebuild trigger:** n8n webhook (Hi.Events event published/updated/deleted) → POST to Cloudflare Pages deploy hook → automatic rebuild in ~30s.
- **Future (Hostinger VPS):** Swap to `@astrojs/node` SSR — same logic, fresh data per request, no rebuild needed.

### Event card states
- **Upcoming** (start_date > today): full card, photo, price, gold "Reservar" CTA → Hi.Events booking page
- **Past** (start_date < today): same card, desaturated, `"Finalizado"` badge, no CTA
- **Empty** (0 events in category): elegant fallback — "Próximamente nuevas experiencias"

### Implementation tasks
- [x] Save plan to memory
- [x] Hi.Events API token obtained: POST /api/auth/login (NOT /api/v1/auth/login) → JWT valid 7 days
- [x] Confirmed 4 demo events exist: ruta-guiada-sierra-de-irta, kayak-y-snorkel-en-la-costa, cata-de-vinos-y-gastronomia, visita-guiada-al-castillo-papal — all LIVE/UPCOMING, 0 images
- [x] FLAG DECISION: Use Hi.Events `status` field as flag — LIVE=appears on site, DRAFT=hidden. No custom category needed since instance is Porta D'irta exclusive.
- [x] LIFECYCLE: Use `lifecycle_status` field — UPCOMING=full card+CTA, PAST=faded+Finalizado badge
- [ ] **RESUME HERE: Upload cover images to 4 demo events via Hi.Events API**
  - Correct image upload route NOT YET FOUND — tried /api/auth/events/{id}/images (404)
  - Need to find correct route: check inside Docker container routes or Hi.Events docs
  - Image mapping: event 1 (sierra) → sierra-tower-wide.jpg, event 2 (kayak) → sierra-tower-sea.jpg, event 3 (vinos) → food-paella-wine.jpg, event 4 (castle) → food-paella-close.jpg
  - All images at: /home/stderr/hospitality-project/frontend/public/assets/images/
  - Hi.Events admin JWT (expires ~7 days from 2026-03-21): obtain fresh one with POST /api/auth/login {"email":"info@portadirta.com","password":"Portadirta2026!"}
- [ ] Add `"Nuestros Paquetes"` dynamic section to `experiencias.astro` (between Intro and Sierra de Irta sections)
  - Fetch from: GET /api/public/organizers/1/events (no auth needed)
  - Filter: only status=LIVE events
  - Card states: UPCOMING → full card + "Reservar" → https://events.hobbitonranch.com/e/{slug}, PAST → greyed + "Finalizado" badge
  - Empty state: "Próximamente nuevas experiencias"
  - Cover image: first item in event.images array, fallback to placeholder
- [ ] JSON-LD Event structured data in `<head>` for upcoming events (Google rich results)
- [ ] n8n workflow: Hi.Events webhook → Cloudflare Pages deploy hook (rebuild trigger)
  - Cloudflare Pages deploy hook URL must be created manually in dashboard first

### Hosting note
- Current: Cloudflare Pages SSG (build-time fetch) — working now
- Production: Hostinger VPS Docker — switch to `@astrojs/node` adapter + SSR for `/experiencias`

## Phase 4: Monitoring (Testing & QA)
*Goal: Break the system now so staff won't face catastrophic failure during a shift.*
- [ ] Execute simulated double-booking attempt across Booking.com and local site.
- [ ] Verify credit card hold releases for "no-show" restaurant bookings.
- [ ] Test off-grid mobile access: staff log into Beds24 via 4G.
- [ ] Verify idempotency (prevent double-charging on multiple "Pay" clicks).
**Tech Stack:** Uptime Kuma (Monitoring), Playwright (E2E Testing).
**Automation:** Cron job for nightly encrypted PostgreSQL dumps of TastyIgniter/Hi.Events to a separate drive.

## Phase 5: Closing (Handover & Launch)
*Goal: Prepare the human operators for the technical system.*
- [ ] Execute final live transactions with real credit cards, then refund.
- [ ] Switch DNS entirely to the production environment (portadirta.com).
- [ ] Migrate from Cloudflare Tunnel to final server — update all APP_URLs and rebuild events container.
- [ ] Conduct a 15-minute operational walkthrough with staff using a tablet.
- [ ] Establish maintenance schedule (e.g., Ubuntu/Docker updates on Tuesday mornings).
**Tech Stack:** OBS Studio (Screen recording for SOPs).
