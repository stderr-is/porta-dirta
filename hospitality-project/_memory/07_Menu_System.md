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

## SEO Targets

| Page | Primary keyword (ES) | Secondary |
|---|---|---|
| `/carta` | carta restaurante Peñíscola | menú à la carte Costa Azahar |
| `/menu` | menú especial Peñíscola | menú degustación Peñíscola |

---

## QR Codes

- Generate two QR codes pointing to:
  - `https://www.portadirta.com/carta`
  - `https://www.portadirta.com/menu`
- Style to match brand (gold on dark blue, with logo)
- Print and laminate for tables

---

## Build Order

- [x] Write plan to `_memory/07_Menu_System.md`
- [ ] Build `src/pages/carta.astro` (static placeholder data)
- [ ] Build `src/pages/menu.astro` (static placeholder data)
- [ ] Build `CartaSection.astro` component
- [ ] Build `MenuEspecial.astro` component
- [ ] Update `restaurante.astro` — replace menu section with CTA cards
- [ ] Write `src/data/carta.json` placeholder
- [ ] Write `src/data/menu.json` placeholder
- [ ] PHP proxy: `save_carta.php` + `save_menu.php`
- [ ] n8n: `/carta` branch on Workflow B
- [ ] n8n: `/menu` branch on Workflow B
- [ ] Generate and print QR codes
