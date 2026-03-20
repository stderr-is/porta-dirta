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
- [ ] Map the physical restaurant floor plan digitally within TastyIgniter.
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
- [ ] Configure Beds24 "Auto Actions" to send "Book a Table" email upon room confirmation.
- [ ] Append URL parameters to restaurant link to pre-fill guest details in TastyIgniter.
- [ ] Build Astro content collections for local collaboration events.
**Tech Stack:** Astro (Frontend HTML), n8n (Workflow Automation).
**Automation:** n8n listens for "Check-in Tomorrow" trigger to WhatsApp the guest their Hi.Events ticket QR code.

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
