---
type: architecture
status: active
tags: [strategy, beds24, data-flow]
---

# 🧠 Master Architecture & Parameters — Porta D'irta

## The "Single Source of Truth"
**Beds24** is the absolute master database for guest identity and dates.
* **TastyIgniter** (Restaurant) and **Hi.Events** (Collabs/Ticketing) are downstream dependents.
* Data flows strictly in **one direction**: from the room reservation to the experience upsell. Never the reverse.

## AI Orchestration Layer (updated 2026-03-20)
**n8n** is the central nervous system for all automation. **Claude Haiku 4.5** is the reasoning engine called via HTTP (switched from Gemini — free tier quota issues; Anthropic API key in n8n env). **Telegram Bot** is the mobile command interface for the admin.

### Critical n8n v2.12 Bug — IF Node typeVersion 2
All IF nodes in workflow JSONs must use the **new n8n v2 condition format** — the old format is silently ignored (always fires output[0]):
```json
{
  "conditions": {
    "options": {"caseSensitive": true, "leftValue": "", "typeValidation": "strict"},
    "conditions": [{"id": "uuid", "leftValue": "={{ $json.field }}", "rightValue": "value",
      "operator": {"type": "string", "operation": "notEquals", "singleValue": false}}],
    "combinator": "and"
  },
  "options": {}
}
```
Boolean conditions use `"type": "boolean", "operation": "equals"`. All 5 IF nodes in Workflow B fixed on 2026-03-20.

### Critical n8n v4 Bug — HTTP Request Node Body Encoding (fixed 2026-03-21)
`body.parameters` is silently ignored when `specifyBody: "json"`. The correct parameter is `jsonBody`:
```json
{
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={{ JSON.stringify({ key: $json.value }) }}"
}
```
`specifyBody: "string"` also broken — URL-form-encodes the entire JSON string as a key with empty value.
**Workaround for complex payloads:** TastyIgniter PHP proxy at `POST /api/internal/beds24/calendar` accepts flat JSON, builds nested Beds24 structure in real PHP, forwards via curl. Auth header: `X-Internal-Token: ${INTERNAL_API_TOKEN}`.

### n8n REST API (for scripted workflow updates)
- Login: `POST /rest/login` with `{"emailOrLdapLoginId":"...", "password":"..."}` + `browser-id` header → session cookie
- Update workflow: `PATCH /rest/workflows/{id}` (PUT returns 404)
- Workflow B ID: `i87KV1SQXuhTCYxt`

Full blueprint: `_memory/05_AI_Automation.md`
Workflow files: `backend/n8n-workflows/`

Data flow with AI layer:
```
OTA/Guest → Beds24 → n8n webhook → [Identity Router] → Gemini → [Schema Validator] → [Confirmation] → API → Audit Log
Email → IMAP → n8n → Gemini → Telegram draft → [Approve/Edit] → SMTP
Telegram voice/text → n8n → [Identity Router] → Gemini → [Schema Validator] → API
Cron 02:00 → n8n → Beds24 occupancy → Gemini yield analysis → Telegram approval → Beds24 price update
```

## The Critical Path
1. Beds24 Booking.com API Authorization
2. ~~Cloudify/Railway Docker Deployment~~ → **Cloudflare Tunnel (testing phase)**
3. Astro Frontend Integration

> [!warning] The Booking.com Bottleneck
> If Booking.com delays the XML connection approval by one day, the entire public launch is delayed by one day. We **cannot** launch the site manually without OTA sync protection.

## Infrastructure (Testing Phase — as of 2026-03-20)

### Hosting Strategy (CONFIRMED 2026-03-21)
- **Testing:** Cloudflare Tunnel (`porta-dirta-backend`) exposes local Docker containers to the public internet via `hobbitonranch.com` subdomains. No public IP or port forwarding required.
- **Frontend (Production):** Astro site will be hosted on **Hostinger**.
- **Backend (Production):** All backoffice services (TastyIgniter, Hi.Events, n8n, Uptime Kuma) will run on a **Hostinger VPS running Debian + Docker**. Same docker-compose stack, moved to the VPS.
- **Beds24:** External cloud service — NOT self-hosted, no migration needed.
- **Cloudflare:** Stays in front as CDN + SSL + DDoS protection (proxy mode), even on Hostinger.
- **Current temp frontend:** Astro static site on Cloudflare Pages (will move to Hostinger at launch).

### Implications for Astro SSR
- Since backend runs on a Debian VPS (not Cloudflare Workers), use `@astrojs/node` adapter (not `@astrojs/cloudflare`) for any SSR pages.
- SSR Astro container runs alongside other Docker services on the same VPS.
- Cloudflare sits in front for caching and SSL — no need for Cloudflare Pages at production.

### Astro Build Modes (configured 2026-03-21)
- `npm run build` → static SSG output (Cloudflare Pages, current)
- `npm run build:hostinger` → SSR server output (Hostinger VPS, `BUILD_TARGET=node`)
- Controlled by `BUILD_TARGET` env var in `astro.config.mjs` — no code changes needed to switch
- SSR entry point: `dist/server/entry.mjs` (standalone node server on port 4321)
- Frontend Docker files: `frontend/Dockerfile` + `frontend/docker-compose.yml` + `frontend/.env.example`

### Transitional Hosting Phase (frontend on Hostinger, backends still local)
- Hostinger VPS runs ONLY the Astro SSR container (`portadirta.com`)
- Backends (TastyIgniter, Hi.Events, n8n) stay on local machine via Cloudflare Tunnel
- Astro calls backends via `hobbitonranch.com` tunnel URLs (set in `frontend/.env`)
- When backends migrate to Hostinger: update 2 env vars + `docker compose up -d --build` — done

### Services & Public URLs (Testing)
| Service | Container Port | Public URL | Credentials | Purpose |
|---------|---------------|------------|-------------|---------|
| TastyIgniter | 8081 | https://restaurant.hobbitonranch.com | `TASTYIGNITER_ADMIN_EMAIL` / `${TASTYIGNITER_ADMIN_PASSWORD}` | Restaurant admin + API |
| Hi.Events | 8082 | https://events.hobbitonranch.com | `HIEVENTS_ADMIN_EMAIL` / `${HIEVENTS_ADMIN_PASSWORD}` | Ticketing admin + booking UI + API |
| n8n | 5678 | https://n8n.hobbitonranch.com | `N8N_ADMIN_EMAIL` / `${N8N_ADMIN_PASSWORD}` | Workflow automation UI |
| Uptime Kuma | 3001 | https://monitor.hobbitonranch.com | (first-run setup in browser) | Service uptime monitoring + alerts |

### Cloudflare Tunnel
- **Tunnel name:** `porta-dirta-backend`
- **Tunnel ID:** `bc2e8520-0371-4583-80f2-4f5b1f107990`
- **Credentials:** `~/.cloudflared/bc2e8520-0371-4583-80f2-4f5b1f107990.json`
- **Config:** `~/.cloudflared/config.yml`
- **Runs as:** systemd user service (`systemctl --user status cloudflared`)

### Hi.Events Container
- Uses `Dockerfile.all-in-one` (nginx + PHP-FPM + Node.js SSR + queue workers in one container)
- The simple `Dockerfile` only served the backend API ("Congratulations" page). The all-in-one includes the full React frontend UI.
- **API route prefix:** `/api/` (NOT `/api/v1/`). Auth routes under `/api/auth/`. Authenticated admin routes directly under `/api/`. Public routes under `/api/public/`.
- **Image upload (admin):** `POST /api/events/{id}/images` — multipart form, fields: `image` (file) + `type=EVENT_COVER`. Requires `Authorization: Bearer <JWT>`.
- **Image URL pattern:** `https://events.hobbitonranch.com/storage/event_cover/{filename}`
- **Public events feed:** `GET /api/public/organizers/1/events` — returns all LIVE events with images array, product_categories (for pricing), lifecycle_status (UPCOMING/PAST).

### Uptime Kuma (configured 2026-03-21)
- **URL:** https://monitor.hobbitonranch.com
- **Login:** `UPTIME_KUMA_ADMIN_USER` / `${UPTIME_KUMA_ADMIN_PASSWORD}`
- **5 monitors:** Porta D'irta Web, Restaurante, Hi.Events, n8n Automation, Beds24 API
- **Notifications:** Telegram alerts to admin (bot token in n8n env, chat ID: 1330098629)
- **Beds24 monitor** accepts HTTP 401 as "UP" (auth required endpoint — 401 means server alive)

### TastyIgniter Admin (configured 2026-03-21)
- **URL:** https://restaurant.hobbitonranch.com/admin
- **Login:** `TASTYIGNITER_ADMIN_EMAIL` / `${TASTYIGNITER_ADMIN_PASSWORD}`
- Note: install created account as diogojorgepinto86@gmail.com — already changed to info@portadirta.com via DB

### Cloudflare Pages (frontend)
- **Project:** porta-dirta
- **Production branch:** master (was briefly set to nature-test during design test — now back to master)
- **Env vars needed:** PUBLIC_TASTYIGNITER_URL=https://restaurant.hobbitonranch.com and PUBLIC_HIEVENTS_URL=https://events.hobbitonranch.com — must be set manually in dashboard → Settings → Environment variables

### Domain Migration Path (to Hostinger VPS)
When moving to the final Hostinger VPS:
1. Copy `backend/` docker-compose stack to the Hostinger Debian VPS
2. Update `APP_URL` in `backend/tastyigniter/.env` → `https://restaurante.portadirta.com`
3. Update `APP_URL` + `APP_FRONTEND_URL` in `backend/hi.events/backend/.env` → `https://events.portadirta.com`
4. Update `VITE_API_URL_CLIENT` + `VITE_FRONTEND_URL` in `docker-compose.yml` events environment
5. Update `PUBLIC_TASTYIGNITER_URL` + `PUBLIC_HIEVENTS_URL` in `frontend/.env`
6. Rebuild the `events` container (`docker compose build events`)
7. Deploy Astro frontend to Hostinger (static export or Node.js Docker container for SSR)
8. Point Cloudflare DNS to Hostinger IP (proxy mode ON for CDN + SSL)
9. Decommission Cloudflare Tunnel + Cloudflare Pages

## 2026-04-03 Update (Menu + i18n stabilization)

- n8n menu updates were stabilized end-to-end (`/bebidas`, `/taperia`) with strict deployment protocol on each workflow change: `workflow_history` insert -> `workflow_entity` (`versionId` + `activeVersionId`) update -> n8n restart -> Telegram webhook re-register.
- Runtime config alignment completed: `MENU_CARTA_DOC_ID` passthrough added in `backend/docker-compose.yml` for n8n service to avoid wrong source-doc fallback behavior.
- Frontend multilingual menu pages now use translation overlays that preserve numeric/non-text fields (prices, allergens, units) instead of replacing full objects.
- Localized table hub routes are live at `/en/mesa`, `/fr/mesa`, `/de/mesa` after moving `[lang]/mesa` to dynamic-compatible behavior and deploying updated container image.
