---
name: Porta D'irta project overview
description: High-level project overview and working directory for Porta D'irta hospitality project
type: project
---

Porta D'irta is a boutique hotel + restaurant in Peñíscola, Spain.

**Working directory:** `/home/stderr/hospitality-project/` (local) | `/opt/portadirta/` (VPS)
**VPS is now the source of truth.** Use `gitpush "message"` on VPS to backup to GitHub.

## Stack
- **Frontend:** Astro SSR (portadirta.com)
- **Restaurant:** TastyIgniter (restaurante.portadirta.com)
- **Events:** Hi.Events (eventos.portadirta.com)
- **Automation:** n8n (n8n.portadirta.com)
- **Hotel booking:** Beds24 API V2
- **Monitoring:** Uptime Kuma (monitor.portadirta.com)

## Key automation (Workflow B)
Email → IMAP trigger → Claude classifies → Telegram preview → admin taps ✅/❌ → auto-reply or restaurant booking created
