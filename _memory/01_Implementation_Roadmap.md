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
- [x] Workflow B end-to-end price update — FIXED (2026-03-21): n8n HTTP Request v4 body encoding bug resolved. Root cause: `body.parameters` is silently ignored; must use `jsonBody` with `JSON.stringify(...)`. TastyIgniter PHP proxy at `/api/internal/beds24/calendar` bypasses the n8n body encoding entirely — accepts flat JSON, builds Beds24 nested array in PHP, forwards via curl. Bot command "Sube Torre Badum a 150€ hasta el final del mes" → `💰 Precio actualizado` confirmed working.
- [x] **Configure `BEDS24_API_TOKEN`**: moved all secrets to `backend/.env` and updated `docker-compose.yml`. Restarted n8n. (2026-03-24)
- [x] **Email Enrichment**: emails now first classify intent, then fetch live restaurant availability + live hotel availability (Beds24), then draft informed replies. (2026-03-25)
- [x] **Menú Especial Semana Santa**: Integrated editorial redesign on `/restaurante` page + synchronized `menu.json` for AI/dynamic page. (2026-03-25)
- [ ] Test Workflow C: trigger manually, verify pricing recommendation appears in Telegram
- [ ] Verify Identity Router blocks unauthorized Telegram IDs
- [x] Workflow B — Full command suite (2026-03-22): 10 new bot commands added + tested:
  - `beds24.getArrivals` / `beds24.getDepartures` / `beds24.getDailySummary` — via `/api/internal/daily-summary` PHP proxy
  - `beds24.getGuestInfo` — via `/api/internal/guest-info` PHP proxy (who is in room X)
  - `beds24.getRevenue` — sum confirmed bookings for a period
  - `beds24.getOccupancyRate` — occupancy % over a date range
  - `tastyigniter.createReservation` — create restaurant booking from natural language
  - `tastyigniter.cancelReservation` — cancel by guest name via `/api/internal/reservations/cancel`
  - `maintenance.addNote` / `maintenance.listNotes` — persistent static data notes (no API call path: Has API Call? → Direct Action Handler)
  - Updated help menu in Schema Validator
  - `Prepare Claude Prompt` updated with all new action rules + extended payload schema (nombre, email, telefono, hora, name, note)
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
- [x] Upload cover images to 4 demo events via Hi.Events API (2026-03-21)
  - Correct route: POST /api/events/{event_id}/images (multipart, field `image` + `type=EVENT_COVER`)
  - NOT /api/v1/ — Hi.Events uses /api/ (no version prefix) for authenticated routes
  - Images uploaded: sierra-tower-wide.jpg → event 1, sierra-tower-sea.jpg → event 2, food-paella-wine.jpg → event 3, food-paella-close.jpg → event 4
  - Images served from: https://events.hobbitonranch.com/storage/event_cover/
- [x] Add `"Nuestros Paquetes"` dynamic section to `experiencias.astro` (2026-03-21)
  - Section id="paquetes", inserted between Intro section and Sierra de Irta section
  - Fetches from /api/public/organizers/1/events at build time (no auth)
  - Filters: status=LIVE only; sorts UPCOMING first
  - Card states: UPCOMING → full card + cover image + price badge + "Reservar" CTA → Hi.Events booking page, PAST → greyed + grayscale + "Finalizado" badge overlay
  - Empty state: "Próximamente nuevas experiencias" with contact link
  - Cover image from event.images[0].url, SVG placeholder fallback
  - GarlandDivider inserted between paquetes section and Sierra de Irta
- [x] JSON-LD Event structured data in `<head>` for upcoming events (2026-03-21)
  - Layout.astro got `<slot name="head" />` for per-page head injections
  - experiencias.astro fills that slot with `<script type="application/ld+json" set:html={...} />`
  - Emits one `schema.org/Event` object per UPCOMING package: name, description, startDate, location (Porta D'irta, Peñíscola), organizer, Offer (price+currency+bookingUrl), image URL
- [~] n8n workflow: Hi.Events webhook → Cloudflare Pages deploy hook (rebuild trigger)
  - **INTERIM ONLY** — only needed while hosted on Cloudflare Pages (SSG)
  - On Hostinger VPS with `@astrojs/node` SSR, every request re-fetches live → no rebuild needed
  - If Cloudflare Pages interim phase breaks (stale events showing), implement this as a stopgap
  - Cloudflare Pages deploy hook URL must be created manually in dashboard first

### Hosting note
- Current: Cloudflare Pages SSG (build-time fetch) — working now
- Production: Hostinger VPS Docker — switch to `@astrojs/node` adapter + SSR for `/experiencias`

## Phase 3.8: Menu Automation Pipeline
*Goal: Staff update menus by editing a Google Doc and sending one Telegram message — site updates instantly, no rebuild, no developer needed.*

### ✅ FULLY OPERATIONAL (2026-03-24)
- [x] **Frontend pages**: `/carta`, `/menu`, `/bebidas`, `/mesa` — mobile-first, allergen pills, QR-ready
- [x] **Astro SSR reading**: all 4 pages read from `MENU_DATA_PATH` volume at request time; fall back to bundled JSON on Cloudflare Pages build
- [x] **PHP proxy** (`routes/api.php`): `POST /api/internal/menu/carta|menu|bebidas` — validates + writes JSON to shared Docker volume
- [x] **Docker**: `menu-data` named volume + custom entrypoint `chown www-data` on startup (volume initialises as root — see n8n troubleshooting notes)
- [x] **Dockerfile fix**: replaced broken `printf '%{CORS_ORIGIN}e'` with `COPY cors.conf` (printf interprets `%{` as format directive in modern sh/dash)
- [x] **n8n Workflow B**: menu pipeline LIVE in production webhook mode — full error handling on every step:
  - Route OK? IF gate (env var missing → Telegram error)
  - Fetch Google Doc (DNS/network failure → Telegram error)
  - Claude — Parse Menu (Anthropic API failure → Telegram error)
  - Extract Menu JSON (bad JSON from Claude → Telegram error)
  - Save Menu to Proxy (proxy down → Telegram error)
  - Telegram — Menu Updated (success confirmation)
- [x] Fill `MENU_CARTA_DOC_ID` + `MENU_MENU_DOC_ID` in `docker-compose.yml` (done 2026-03-23)
- [x] Share Google Docs as "anyone with the link can view" (confirmed by owner)

### Still needed to go live on portadirta.com
- [ ] Uncomment `frontend` service in `docker-compose.yml` (VPS deployment — currently Cloudflare Pages serves static fallback)
- [ ] Real bebidas list from owner → `MENU_BEBIDAS_DOC_ID`
- [ ] Generate + print QR code for `portadirta.com/mesa`

### Full details + troubleshooting
See `_memory/07_Menu_System.md` — activation checklist, JSON schemas, Claude prompts.
See `_memory/08_N8N_Troubleshooting.md` — **CRITICAL: read before touching n8n workflows**.

## Phase 3.7: /eventos Page — Final Polish
*Blocked on input from brother-in-law (content owner) before proceeding.*
- [ ] Wire inquiry form to TastyIgniter contact API or n8n webhook — **awaiting decision on form fields / destination email**
- [ ] Replace venue mosaic placeholder photos with real event/garden photography
- [ ] Replace `property-aerial-pool.jpg` in Mercado Artesanal content with a proper image
- [ ] Confirm final event lineup for summer 2026 (Jazz, Cena Maridaje, Mercado — are these real or demo?)

## Phase 4: Optimization (SEO & Conversion)
*Goal: Ensure the site is found by the right guests and converts visitors into bookings.*
*Full plan in `_memory/06_SEO_Strategy.md`. Items below are the actionable checklist.*
- [x] **SEO Priority 1:** Implement OG tags, robots.txt, and indexable HTML room content (Done 2026-03-20).
- [x] **Mobile UX:** Add sticky "Book Now" bar and WhatsApp FAB for CRO.
- [x] **Transparency:** Add live sustainability status component (mocked).
- [x] **Fix Language Switcher:** Add placeholders for EN/FR/DE to prevent 404s.
- [x] **AI Crawler directives** — GPTBot/ClaudeBot/PerplexityBot allowed; CCBot/omgili blocked in robots.txt.
- [x] **JSON-LD structured data** — LodgingBusiness, Restaurant, BreadcrumbList, FAQPage, Event on key pages.

### SEO Wave 0 — Critical (Before Go-Live)
- [ ] Fix `hobbitonranch.com` hardcoded in `eventos-locales/*.md` ticketsUrl + `experiencias.astro:78` fallback
- [ ] Add `og:url`, `og:image:width`, `og:image:height` to `Layout.astro`
- [ ] Create branded `og-default.jpg` (1200×630) and replace picsum.photos default in `Layout.astro`
- [ ] Add Google Site Verification meta slot to `Layout.astro`
- [ ] Migrate static `public/sitemap.xml` → `@astrojs/sitemap` integration
- [ ] Add hreflang tags to `Layout.astro` (es + x-default for now; full 4-locale when translations ready)
- [ ] **Create Google Business Profile** — START NOW (postcard verification = 2 weeks)
- [ ] **Google Search Console** — verify portadirta.com, submit sitemap

### SEO Wave 1 — High Priority (First 2 Weeks After Launch)
- [ ] Remove `noindex={true}` from `reservar.astro` (canonical URL already prevents duplicate issues)
- [ ] Add indexable HTML room content to `/hotel` outside the Beds24 iframe (name, description, price, amenities)
- [ ] Add indexable menu section to `/restaurante` (section headings + representative dishes)
- [ ] Rewrite H1 on en/fr/de placeholder pages to name the property (not the "coming soon" status)
- [ ] Rewrite JSON-LD `description` fields to 200+ chars factual text (for AI citation)
- [ ] Expand LodgingBusiness JSON-LD: numberOfRooms, checkinTime, checkoutTime, amenities, containsPlace
- [ ] Expand Restaurant JSON-LD: acceptsReservations, menu URL, servesCuisine, isContainedInPlace
- [ ] Install Google Analytics 4 (production-only, gated by `import.meta.env.PROD`)
- [ ] Improve title/description for `/experiencias` and `/reservar` (see `06_SEO_Strategy.md` §2 Wave 1)
- [ ] TripAdvisor + El Tenedor + Booking.com + Bing Webmaster + Apple Maps listings

### SEO Wave 2 — Month 1
- [ ] Self-host Google Fonts (WOFF2 in `/public/assets/fonts/`) — eliminates render-blocking 3rd-party request
- [ ] Add Event JSON-LD to `/eventos` (once brother-in-law confirms real event lineup + dates)
- [ ] Add FAQ schema to `/experiencias`
- [ ] n8n review request workflow (24h post-checkout → Google review link)
- [ ] Physical QR review cards for restaurant tables → `portadirta.com/opiniones`
- [ ] Regional directory listings: turismecv.com, Ayuntamiento Peñíscola, Patronat Castelló, Guía Repsol

### SEO Wave 3 — Month 3+
- [ ] Launch `/en/` full multilingual routes with translations
- [ ] Blog content section (Astro Content Collections MDX)
- [ ] Wikidata entity for Porta D'irta
- [ ] Press trip pitches (UK/FR/DE travel media)
- [ ] Spanish travel blogger outreach (comped stays)

## Phase 5: Monitoring (Testing & QA)
*Goal: Break the system now so staff won't face catastrophic failure during a shift.*
- [ ] Execute simulated double-booking attempt across Booking.com and local site.
- [ ] Verify credit card hold releases for "no-show" restaurant bookings.
- [ ] Test off-grid mobile access: staff log into Beds24 via 4G.
- [ ] Verify idempotency (prevent double-charging on multiple "Pay" clicks).
**Tech Stack:** Uptime Kuma (Monitoring), Playwright (E2E Testing).
**Automation:** Cron job for nightly encrypted PostgreSQL dumps of TastyIgniter/Hi.Events to a separate drive.

## Pre-Launch Checklist (before going live)
- [x] **Fill legal page placeholders**: replaced all `[NOMBRE TITULAR]` and `[NIF/CIF]` with real data in `legal.astro`, `privacidad.astro`, and `cookies.astro`. (2026-03-25)
- [ ] **Remove beta disclaimer banners** from 3 pages — search `TODO: REMOVE BEFORE LAUNCH`:
  - `frontend/src/pages/hotel.astro` — above Beds24 hero widget AND above booking anchor widget
  - `frontend/src/pages/restaurante.astro` — above reservation form
  - `frontend/src/pages/experiencias.astro` — above Nuestros Paquetes section
- [ ] **Remove beta disclaimer from TastyIgniter email templates** — run in DB:
  ```sql
  UPDATE mail_templates SET body = '', plain_body = '', is_custom = 0
  WHERE template_id IN (10, 12, 13);
  ```
  Templates affected: 10 (reservation confirmation), 12 (reservation update), 13 (reservation reminder)
- [ ] **Remove beta disclaimer from Beds24 email templates** — done manually in Beds24 dashboard → Templates
- [ ] **Remove beta disclaimer from n8n "Check-in Tomorrow" workflow** — edit the SMTP send node body
- [ ] Set Cloudflare Pages env vars to production URLs (replace `hobbitonranch.com` → `portadirta.com` subdomains)
- [x] **Legal pages created** — `/legal` (Aviso Legal LSSI-CE), `/privacidad` (GDPR privacy policy), `/cookies` (EU Cookie Directive). All 3 footer links now resolve.
- [x] **GDPR consent checkboxes** — added to all 4 forms: contacto, restaurante, eventos, experiencias. Each links to /privacidad. Required field (HTML5 `required`).
- [x] **CSP fixed** — added Google Maps to `frame-src` and `connect-src` (was blocked, causing broken map embed in contacto page).

## Phase 5: Closing (Handover & Launch)
*Goal: Prepare the human operators for the technical system.*
- [ ] Execute final live transactions with real credit cards, then refund.
- [ ] Switch DNS entirely to the production environment (portadirta.com).
- [ ] Migrate from Cloudflare Tunnel to final server — update all APP_URLs and rebuild events container.
- [ ] Conduct a 15-minute operational walkthrough with staff using a tablet.
- [ ] Establish maintenance schedule (e.g., Ubuntu/Docker updates on Tuesday mornings).
**Tech Stack:** OBS Studio (Screen recording for SOPs).
