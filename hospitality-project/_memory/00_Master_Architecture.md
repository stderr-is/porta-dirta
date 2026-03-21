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

### Services & Public URLs (Testing)
| Service | Container Port | Public URL | Credentials | Purpose |
|---------|---------------|------------|-------------|---------|
| TastyIgniter | 8081 | https://restaurant.hobbitonranch.com | info@portadirta.com / Portadirta2026! | Restaurant admin + API |
| Hi.Events | 8082 | https://events.hobbitonranch.com | info@portadirta.com / Portadirta2026! | Ticketing admin + booking UI + API |
| n8n | 5678 | https://n8n.hobbitonranch.com | stderr.is@gmail.com / Portadirta2026! | Workflow automation UI |
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

### Uptime Kuma (configured 2026-03-21)
- **URL:** https://monitor.hobbitonranch.com
- **Login:** portadirta / Portadirta2026!
- **5 monitors:** Porta D'irta Web, Restaurante, Hi.Events, n8n Automation, Beds24 API
- **Notifications:** Telegram alerts to admin (bot token in n8n env, chat ID: 1330098629)
- **Beds24 monitor** accepts HTTP 401 as "UP" (auth required endpoint — 401 means server alive)

### TastyIgniter Admin (configured 2026-03-21)
- **URL:** https://restaurant.hobbitonranch.com/admin
- **Login:** info@portadirta.com / Portadirta2026!
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
