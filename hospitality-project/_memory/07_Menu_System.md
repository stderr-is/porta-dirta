# 07 — Menu System: Carta & Menú Especial

## Overview

Two distinct menu types exist at Porta D'irta:
- **La Carta** — full à la carte menu. Changes seasonally (new dishes, price updates).
- **El Menú** — fixed-price set menu (e.g. €35pp, changes per event or weekly).

There is **no "menú del día"**.

---

## Architecture

### Data Flow

```
Staff edits Google Doc
    ↓
Sends /carta or /menu to Telegram bot
    ↓
n8n fetches the relevant Google Doc (Google Drive node)
    ↓
Claude 4.5 parses text → structured JSON + ES/EN/FR/DE translations
    ↓
n8n POSTs to PHP proxy on TastyIgniter (VPS)
    ↓
PHP writes to shared Docker volume:
  /data/carta.json
  /data/menu.json
    ↓
Astro SSR reads files on each request → renders fresh HTML + JSON-LD
```

### Why SSR (not SSG + rebuild)
The site runs on Hostinger VPS via Coolify/Docker with `output: 'server'` (Node adapter).
No build trigger needed — Astro reads the JSON files at request time, so updates are instant.

---

## Google Docs

| Doc | Name | Updated |
|---|---|---|
| Carta | `Carta — Porta D'irta` | Seasonally |
| Menú | `Menú — Porta D'irta` | Weekly / per event |

---

## JSON Schemas

### `carta.json`
```json
{
  "updated": "2025-03-23",
  "sections": [
    {
      "name": "Tapas",
      "items": [
        {
          "name": "Aceitunas aliñadas",
          "description": "...",
          "price": 3.50,
          "allergens": []
        }
      ]
    },
    { "name": "Arroces", "items": [] },
    { "name": "Platos principales", "items": [] },
    { "name": "Postres caseros", "items": [] }
  ],
  "translations": {
    "en": { "sections": [] },
    "fr": { "sections": [] },
    "de": { "sections": [] }
  }
}
```

### `menu.json`
```json
{
  "updated": "2025-03-23",
  "name": "Menú Especial",
  "price": 35.00,
  "priceNote": "por persona — pan y agua incluidos",
  "available": "Sábados y domingos",
  "sections": [
    { "name": "Aperitivos", "items": [] },
    { "name": "Entrantes", "items": [] },
    {
      "name": "Segundos",
      "items": [],
      "note": "Mín. 2 personas para arroces"
    },
    { "name": "Postres", "items": [] }
  ],
  "translations": {
    "en": {},
    "fr": {},
    "de": {}
  }
}
```

---

## Frontend Pages

### `/carta` — `src/pages/carta.astro`
- SSR, reads `carta.json` at request time
- Mobile-first, content-first (no hero — jumps straight to menu)
- Large readable text (scanned from phone at table)
- Sections: Tapas · Arroces · Platos · Postres
- "Reservar mesa" CTA at bottom
- JSON-LD: `Schema.org/Menu` with `MenuItem` entries
- QR code destination for table QR codes

### `/menu` — `src/pages/menu.astro`
- SSR, reads `menu.json` at request time
- Shows fixed price, available days, all courses
- Same mobile-first treatment
- "Reservar mesa" CTA at bottom
- JSON-LD: `Schema.org/Menu` with fixed price `Offer`
- QR code destination (separate QR or same as carta if only one active)

### `/restaurante` updates
- Remove current static menu section
- Add two prominent CTA cards: "Ver La Carta →" and "Ver El Menú →"
- Both cards link to `/carta` and `/menu` respectively

---

## Backend (VPS / TastyIgniter)

### PHP Proxy Endpoints
- `POST /api/save-carta` → writes `/data/carta.json`
- `POST /api/save-menu` → writes `/data/menu.json`
- Protected by a shared secret token (set in n8n + PHP)

---

## n8n Workflow B — New Branches

### `/carta` command
1. Telegram trigger: message text starts with `/carta`
2. Google Drive node: fetch `Carta — Porta D'irta` doc as plain text
3. Claude node: parse into `carta.json` structure + translate to EN/FR/DE
4. HTTP Request: POST to TastyIgniter PHP proxy
5. Telegram reply: `✅ Carta actualizada en portadirta.com/carta`

### `/menu` command
1. Telegram trigger: message text starts with `/menu`
2. Google Drive node: fetch `Menú — Porta D'irta` doc as plain text
3. Claude node: parse into `menu.json` structure + translate to EN/FR/DE
4. HTTP Request: POST to TastyIgniter PHP proxy
5. Telegram reply: `✅ Menú actualizado en portadirta.com/menu`

---

## Claude Parsing Prompts

### Carta prompt
```
You are a structured data extractor for a Spanish restaurant menu.

Convert the following raw text (from a Google Doc) into a valid JSON object
matching this exact schema: [carta.json schema]

Rules:
- Prices are always numbers (no € symbol)
- If no description exists, use ""
- Allergens: identify from dish name/ingredients where possible
- Keep original Spanish names exactly as written
- Add translations object with EN/FR/DE versions of name and description only
- Return ONLY the JSON, no explanation
```

### Menú prompt
```
You are a structured data extractor for a Spanish restaurant set menu.

Convert the following raw text into a valid JSON object matching this schema: [menu.json schema]

Rules:
- Extract the fixed price (number only)
- Extract available days/times from the text if present
- Identify what is included (bread, water, wine, etc.) for priceNote
- Keep course sections in order as they appear
- Add translations for EN/FR/DE
- Return ONLY the JSON, no explanation
```

---

## Pages

| Page | Purpose | noindex |
|---|---|---|
| `/mesa` | QR code table landing — links to all 3 menus + reservar | yes |
| `/carta` | Full à la carte with allergen icons | no |
| `/menu` | Fixed-price set menu | no |
| `/bebidas` | Drinks & wine list | no |

Single QR per table → `portadirta.com/mesa`

---

## ⚠️ Pending: Real Drinks List

`src/data/bebidas.json` is currently a **mockup**.
Need from owner:
- Full wine list (whites, reds, rosés) with real names, origins, prices per glass/bottle
- Beer selection
- Spirits / cocktails (if any)
- Soft drinks and water prices
- Coffee menu

Once received, update `bebidas.json` and send `/bebidas` to the Telegram bot (when n8n pipeline is built).

---

## Allergen Icon System

Allergens shown as small circular badges (not text) on `/carta` and `/bebidas`.
Defined in `carta.astro` as `ALLERGENS` map — 14 EU major allergens, each with:
- Short code (G, L, H, CR, MO…)
- Label for tooltip / `aria-label`
- Colour pair (bg + text)
A legend is shown at the bottom of each menu page.

---

## SEO Targets

| Page | Primary keyword (ES) | Secondary |
|---|---|---|
| `/carta` | carta restaurante Peñíscola | menú à la carte Costa Azahar |
| `/menu` | menú especial Peñíscola | menú fin de semana Peñíscola |
| `/bebidas` | carta vinos restaurante Peñíscola | vinos Costa del Azahar |

---

## QR Codes

- **One QR per table** pointing to `https://www.portadirta.com/mesa`
- Style to match brand (gold on dark blue, with logo)
- Print and laminate for tables

---

## Build Order

- [x] Write plan to `_memory/07_Menu_System.md`
- [x] Build `src/pages/carta.astro` — allergen full-name coloured pills, mobile-first
- [x] Build `src/pages/menu.astro` — fixed-price, course sections, allergen pills
- [x] Build `src/pages/bebidas.astro` — mockup data
- [x] Build `src/pages/mesa.astro` — QR landing page (noindex, live price from menu.json)
- [x] Update `restaurante.astro` — editorial photo cards → /carta and /menu
- [x] Write `src/data/carta.json` — real data from Google Doc (with allergens)
- [x] Write `src/data/menu.json` — real Menú Especial data (with allergens)
- [x] Write `src/data/bebidas.json` — ⚠️ MOCKUP, needs real data
- [x] PHP proxy: `POST /api/internal/menu/carta|menu|bebidas` in `routes/api.php` — validates JSON, writes to shared Docker volume
- [x] n8n Workflow B: `/carta`, `/menu`, `/bebidas` command pipeline (10 new nodes — see Architecture section)
- [x] Astro pages: SSR file-system reading from `MENU_DATA_PATH` with static fallback for Cloudflare
- [x] Docker: `menu-data` named volume + commented `frontend` service in `docker-compose.yml`
- [x] **ACTIVATE**: fill `MENU_CARTA_DOC_ID` + `MENU_MENU_DOC_ID` in n8n env vars — done 2026-03-23
  - Carta: `12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE`
  - Menú: `1WYJCS8m5wN7XIL17Wpl9hfSKvBkdTVElszs12cCdV0Q`
- [x] **ACTIVATE**: Google Docs shared as "anyone with the link can view" — confirmed by user
- [ ] **ACTIVATE**: reimport `workflow-b-command-center.json` into n8n (or update in-place via n8n UI)
- [ ] **ACTIVATE**: uncomment `frontend` service in `docker-compose.yml` when deploying Astro on VPS
- [ ] Real bebidas list from owner → update `bebidas.json`, then fill `MENU_BEBIDAS_DOC_ID`
- [ ] Generate single QR code for `portadirta.com/mesa` + print for tables

---

## Activation Checklist (what still needs to happen on the VPS)

1. Open `docker-compose.yml` on the VPS
2. Set `MENU_CARTA_DOC_ID=` the ID from `docs.google.com/document/d/**THIS_PART**/edit`
3. Set `MENU_MENU_DOC_ID=` same for the menú doc
4. Share both Google Docs → Share → "Anyone with the link" → Viewer
5. `docker compose up -d n8n` to pick up new env vars
6. In n8n UI: delete old Workflow B, import `workflow-b-command-center.json`
7. Test: send `/carta` to the Telegram bot → should reply `✅ Carta actualizada`
