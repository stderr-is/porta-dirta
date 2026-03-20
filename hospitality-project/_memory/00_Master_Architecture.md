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

## The Critical Path
1. Beds24 Booking.com API Authorization
2. ~~Cloudify/Railway Docker Deployment~~ → **Cloudflare Tunnel (testing phase)**
3. Astro Frontend Integration

> [!warning] The Booking.com Bottleneck
> If Booking.com delays the XML connection approval by one day, the entire public launch is delayed by one day. We **cannot** launch the site manually without OTA sync protection.

## Infrastructure (Testing Phase — as of 2026-03-20)

### Hosting Strategy
- **Testing:** Cloudflare Tunnel (`porta-dirta-backend`) exposes local Docker containers to the public internet via `hobbitonranch.com` subdomains. No public IP or port forwarding required.
- **Production:** Final server TBD. Tunnel config + docker-compose will be updated to point to `portadirta.com`.
- **Frontend:** Astro static site deployed to Cloudflare Pages at `https://porta-dirta.hobbitonranch.com`.

### Services & Public URLs (Testing)
| Service | Container Port | Public URL | Purpose |
|---------|---------------|------------|---------|
| TastyIgniter | 8081 | https://restaurant.hobbitonranch.com | Restaurant admin + API |
| Hi.Events | 8082 | https://events.hobbitonranch.com | Ticketing admin + booking UI + API |
| n8n | 5678 | https://n8n.hobbitonranch.com | Workflow automation UI |

### Cloudflare Tunnel
- **Tunnel name:** `porta-dirta-backend`
- **Tunnel ID:** `bc2e8520-0371-4583-80f2-4f5b1f107990`
- **Credentials:** `~/.cloudflared/bc2e8520-0371-4583-80f2-4f5b1f107990.json`
- **Config:** `~/.cloudflared/config.yml`
- **Runs as:** systemd user service (`systemctl --user status cloudflared`)

### Hi.Events Container
- Uses `Dockerfile.all-in-one` (nginx + PHP-FPM + Node.js SSR + queue workers in one container)
- The simple `Dockerfile` only served the backend API ("Congratulations" page). The all-in-one includes the full React frontend UI.

### Domain Migration Path
When moving to the final server:
1. Update `APP_URL` in `backend/tastyigniter/.env` → `https://restaurante.portadirta.com`
2. Update `APP_URL` + `APP_FRONTEND_URL` in `backend/hi.events/backend/.env` → `https://events.portadirta.com`
3. Update `VITE_API_URL_CLIENT` + `VITE_FRONTEND_URL` in `docker-compose.yml` events environment
4. Update `PUBLIC_TASTYIGNITER_URL` + `PUBLIC_HIEVENTS_URL` in `frontend/.env`
5. Rebuild the `events` container (`docker compose build events`)
6. Delete or repurpose the Cloudflare Tunnel
