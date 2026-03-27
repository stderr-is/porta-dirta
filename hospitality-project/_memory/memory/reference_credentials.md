---
name: Porta D'irta — All Credentials & Access
description: Master credentials reference for all services in the Porta D'irta stack. Read this when any password, token, or login is needed.
type: reference
---

## VPS (Hostinger)
- **IP:** 72.62.180.39
- **SSH:** `ssh root@72.62.180.39` (password auth)
- **OS:** Debian 13 | Docker 29.3.1 | Compose v5.1.1
- **Files:** `/opt/portadirta/backend/`
- **Git repo:** `/opt/portadirta-repo/` — run `gitpush "message"` to backup to GitHub

## Domain & DNS
- **Domain:** portadirta.com
- **DNS managed at:** Hostinger hPanel (ns1/ns2.dns-parking.com)

## Email — info@portadirta.com
- **Provider:** Hostinger mail (mx1/mx2.hostinger.com)
- **SMTP:** smtp.hostinger.com:465 (SSL)
- **IMAP:** imap.hostinger.com:993 (SSL)
- **Username:** info@portadirta.com
- **Password:** Portadirta2026!

## TastyIgniter (Restaurant backend)
- **URL:** https://restaurante.portadirta.com/admin
- **Login:** info@portadirta.com
- **Password:** Portadirta2026!
- **DB:** MySQL — user: `tasty` / pass: `tasty_pass` / db: `tastyigniter`
- **Internal API token:** `portadirta-n8n-2026` (X-Internal-Token header)

## n8n (Automation)
- **URL:** https://n8n.portadirta.com
- **Encryption key:** in `/opt/portadirta/backend/.env` → `N8N_ENCRYPTION_KEY`
- **DB:** PostgreSQL — user: `n8n` / pass: `n8n_pass` / db: `n8n`
- **Workflow B ID:** `av9R2wseN47PQZ8S`
- **Telegram webhook path:** `475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook`

## Telegram Bot
- **Bot token:** `8348668157:AAEMAD_F37GNJJZxOd4C5krZg4OnPaZ_MD4`
- **Admin/Collab IDs:** in `/opt/portadirta/backend/.env`

## Hi.Events (Ticketing)
- **URL:** https://eventos.portadirta.com
- **DB:** PostgreSQL — user: `hievents` / pass: `hievents_pass` / db: `hievents`

## Uptime Kuma (Monitoring)
- **URL:** https://monitor.portadirta.com

## Beds24 (Hotel booking)
- **Property ID:** 318433
- **Room IDs:** 662792 Torre Badum | 662793 Cala El Pebret | 662794 Cala Aljub | 662795 Ermita Sant Antoni
- **V1 API key:** `portadirta2026xK9mR4vL`
- **V2 Refresh token:** ⚠️ EXPIRED — regenerate at beds24.com → Account → API → Refresh Tokens

## Docker internal ports
| Service | Container | Port |
|---|---|---|
| TastyIgniter | backend-restaurant-1 | 8081 |
| Hi.Events | backend-events-1 | 8082 |
| n8n | backend-n8n-1 | 5678 |
| Uptime Kuma | backend-uptime-kuma-1 | 3001 |
| Astro frontend | backend-frontend-1 | 4321 |
