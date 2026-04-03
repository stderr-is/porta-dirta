# Plan: Menu Auto-Update Pipeline — VPS Direct Implementation

## Git Status — RESOLVED ✅
The 2 local commits have just been successfully pushed to GitHub (`bfb1d5d..c6a3c11`).
The VPS can now `git pull` in `/opt/portadirta-repo/` to get all the new frontend files.

## What the VPS needs

### Frontend — Just needs a git pull + Docker rebuild
The 2 pushed commits add to `/opt/portadirta-repo/`:
```
frontend/src/pages/[lang]/taperia.astro   ← NEW
frontend/src/pages/[lang]/menu.astro      ← NEW
frontend/src/pages/[lang]/bebidas.astro   ← NEW
frontend/src/pages/[lang]/desayuno.astro  ← NEW
frontend/src/pages/[lang]/streetfood.astro← NEW
frontend/src/pages/[lang]/carta.astro     ← NEW (redirect)
frontend/src/pages/[lang]/mesa.astro      ← NEW
frontend/src/pages/[lang]/test_mesa.astro ← NEW (redirect)
frontend/src/i18n/translations.ts         ← UPDATED (DE fix)
frontend/public/_redirects               ← UPDATED
```
After pull: copy/sync these into `/opt/portadirta/frontend/` then rebuild Docker.

### Backend — Config + code fixes only (no git)
| Item | Issue | Fix |
|---|---|---|
| `.env` | Wrong doc IDs (carta vs taperia mix-up, bebidas not set) | Replace with 5 correct IDs |
| `docker-compose.yml` | References 3 old env vars | Replace with 5 new refs |
| `api.php` | Whitelist is `['carta','menu','bebidas']` | Expand to `['taperia','menu','bebidas','desayuno','streetfood']` |
| `workflow-b` | 3 commands, no translations in Claude prompts | 5 commands + EN/FR/DE translations |

### Frontend pages — Need SSR conversion
The `[lang]/` restaurant pages we pushed are currently `prerender=true` (static). On the VPS (SSR mode) they'll still work as prerendered, but they WON'T read from the menu volume at request time. To get dynamic translation updates:
- Remove `export const prerender = true`
- Remove `getStaticPaths()`
- Add runtime lang validation
- Add `fs.readFileSync` from `MENU_DATA_PATH` 
- Use `data.translations?.[lang]?.sections` with Spanish fallback

---

## Current State (confirmed by SSH to 72.62.180.39)

### VPS Stack — All Running ✅
- `backend-frontend-1` — SSR Astro, port 4321
- `backend-n8n-1` — n8n, port 5678
- `backend-restaurant-1` — TastyIgniter, port 8081

### VPS dirs
- `/opt/portadirta/` — production files Docker uses (NOT a git repo)
- `/opt/portadirta-repo/` — git clone (will pull latest here, then sync)

### VPS menu-data volume — All 5 files exist but NO TRANSLATIONS
```
taperia.json    → sections=['Tapas']
menu.json       → sections=[Aperitivos, Entrantes, Platos, Postres]
bebidas.json    → sections=[Aperitivos, Cervezas, Bodega, Coctelería, ...]
desayuno.json   → sections=['Desayuno']
streetfood.json → sections=[Para Picar, Burgers, Pizzas, Postres]
```
Data is correct but no EN/FR/DE translations yet — workflow-b hasn't run with correct config.

### Correct Doc ID mapping (confirmed from Google Docs)
```
MENU_TAPERIA_DOC_ID    = 1a9wPRqGnud31JwCJANRFrXewJlQKOkK-AfKCXdW5djI
MENU_MENU_DOC_ID       = 12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE
MENU_BEBIDAS_DOC_ID    = 14A3S1EAhKBmcBGDXE8wka1kVVpe8V1fzIuP5PFUi0Ek
MENU_DESAYUNO_DOC_ID   = 1HGDUzyf2FhzN1uahdV6A1vk_L7FqRUe-eDZZNe09nss
MENU_STREETFOOD_DOC_ID = 14sxH4RfnDLc2XmrJhqM8rBaz0riJW5qetpiT29DHzDY
```

---

## Implementation Steps (all via SSH to 72.62.180.39)

### Step 1 — Git pull on VPS + sync to production
```bash
cd /opt/portadirta-repo && git pull
# Sync new/updated frontend files to production:
rsync -av frontend/src/pages/\[lang\]/ /opt/portadirta/frontend/src/pages/\[lang\]/
rsync -av frontend/src/i18n/translations.ts /opt/portadirta/frontend/src/i18n/
rsync -av frontend/public/_redirects /opt/portadirta/frontend/public/
```

### Step 2 — Convert [lang]/ menu pages from static → SSR
Modify 5 files in `/opt/portadirta/frontend/src/pages/[lang]/` (taperia, menu, bebidas, desayuno, streetfood):
1. **Remove** `export const prerender = true`
2. **Remove** `getStaticPaths()` function (entire export)
3. **Add** runtime lang validation + JSON file reading pattern
4. **Add** translation-aware section reading with Spanish fallback

Example transformation (taperia):
```typescript
// REMOVE:
export const prerender = true;
export function getStaticPaths() { return [{params:{lang:'en'}},{params:{lang:'fr'}},{params:{lang:'de'}}]; }

// ADD at top of frontmatter:
import fs from 'node:fs';  // (already imported in Spanish version)
const { lang } = Astro.params;
if (!lang || !['en', 'fr', 'de'].includes(lang)) {
  return new Response(null, { status: 404 });
}
// ... existing JSON read pattern ...
const langData = (taperia as any).translations?.[lang];
const sections = langData?.sections?.length ? langData.sections : taperia.sections;
```

### Step 3 — Update bundled fallback JSON files
Add empty translations to 5 files in `/opt/portadirta/frontend/src/data/`:
```json
"translations": { "en": { "sections": [] }, "fr": { "sections": [] }, "de": { "sections": [] } }
```

### Step 4 — Fix `.env`
`/opt/portadirta/backend/.env`:
- Remove `MENU_CARTA_DOC_ID`
- Add 5 correct doc IDs

### Step 5 — Fix docker-compose.yml
`/opt/portadirta/backend/docker-compose.yml`:
- Replace 3 old MENU_ vars with 5 new ones

### Step 6 — Expand PHP proxy
`/opt/portadirta/backend/tastyigniter/routes/api.php`:
- `foreach (['taperia', 'menu', 'bebidas', 'desayuno', 'streetfood']`
- Validation: all 5 require `sections`; `menu` also requires `price`

### Step 7 — Update workflow-b (largest change)
Modify `/opt/portadirta/backend/n8n-workflows/workflow-b-command-center.json` via Python JSON patching:

**4 nodes to update:**

**"Menu Command?" IF node:**
Update condition string to detect 5 commands: `/carta|/taperia|/menu|/bebidas|/desayuno|/streetfood`

**"Route Menu Command" Code node:**
```javascript
if (lower.startsWith('/taperia') || lower.startsWith('/carta')) {
  menuType = 'taperia'; docId = $env.MENU_TAPERIA_DOC_ID || '';
} else if (lower.startsWith('/menu')) {
  menuType = 'menu'; docId = $env.MENU_MENU_DOC_ID || '';
} else if (lower.startsWith('/bebidas')) {
  menuType = 'bebidas'; docId = $env.MENU_BEBIDAS_DOC_ID || '';
} else if (lower.startsWith('/desayuno')) {
  menuType = 'desayuno'; docId = $env.MENU_DESAYUNO_DOC_ID || '';
} else if (lower.startsWith('/streetfood')) {
  menuType = 'streetfood'; docId = $env.MENU_STREETFOOD_DOC_ID || '';
}
```

**"Build Menu Prompt" Code node:**
Add 2 new prompts (desayuno, streetfood) + add translations to ALL 5 schemas:

```
taperia schema:   { updated, sections:[{name,items:[{name,desc,price,allergens}]}], translations:{en:{sections:[]},fr:{...},de:{...}} }
menu schema:      { updated, name, price, priceNote, available, sections:[...], translations:{en:{name,priceNote,available,sections:[]}, fr, de} }
bebidas schema:   { updated, sections:[{name,items:[{name,desc,price,unit}]}], translations:{en:{sections:[]},fr,de} }
desayuno schema:  { updated, sections:[{name,note,items:[{name,description,price}]}], translations:{en:{sections:[]},fr,de} }
streetfood schema:{ updated, sections:[{name,items:[{name,price,allergens}]}], translations:{en:{sections:[]},fr,de} }
```

Prompts include instruction: "Translate section names and item names/descriptions to EN, FR, DE. Keep prices as numbers. Allergen keys remain in Spanish (gluten, lácteos, etc.)."

**Schema Validator Code node (help menu):**
Replace `/carta` → `/taperia`, add `/desayuno` and `/streetfood` lines.

**After JSON is patched** — update n8n via PostgreSQL (troubleshooting note: must update BOTH tables):
```python
# Connect to n8n-db postgres container
# UPDATE workflow_entity SET nodes=<new_json> WHERE id='av9R2wseN47PQZ8S'
# Also insert into workflow_history
```

### Step 8 — Restart services
```bash
cd /opt/portadirta/backend

# Rebuild frontend (new pages + SSR changes)
docker compose build frontend && docker compose up -d frontend

# Restart n8n with new env vars
docker compose up -d n8n

# Re-register Telegram webhook (CRITICAL — n8n clears it on restart)
sleep 15
curl -s -X POST \
  "https://api.telegram.org/bot8348668157:AAEMAD_F37GNJJZxOd4C5krZg4OnPaZ_MD4/setWebhook" \
  -d "url=https://n8n.portadirta.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook"

# Restart TastyIgniter (PHP changes)
docker restart backend-restaurant-1
```

### Step 9 — End-to-end test
1. Send `/taperia` to Telegram → expect `✅ Taperia actualizada` + section count
2. Check `taperia.json` in volume has translations keys
3. Visit `https://www.portadirta.com/en/taperia` → English tapas names
4. Visit `https://www.portadirta.com/fr/taperia` → French
5. Repeat for all 5 menus

---

## Files changed summary

| File on VPS | Change |
|---|---|
| `/opt/portadirta-repo/` + `/opt/portadirta/frontend/` | git pull + rsync |
| `frontend/src/pages/[lang]/{5 pages}` | Remove prerender, add SSR JSON reading |
| `frontend/src/data/{5 files}.json` | Add empty translations field |
| `backend/.env` | 5 correct doc IDs |
| `backend/docker-compose.yml` | 5 env var refs |
| `backend/tastyigniter/routes/api.php` | whitelist 3→5 |
| `backend/n8n-workflows/workflow-b-command-center.json` | 5 commands + translations |

## What is behind and what isn't

### Frontend — Behind by 2 commits (frontend-only changes)
The 2 local commits that were **never pushed to GitHub** touch ONLY frontend files:
```
frontend/public/_redirects
frontend/src/i18n/translations.ts
frontend/src/pages/[lang]/taperia.astro   ← NEW
frontend/src/pages/[lang]/menu.astro      ← NEW
frontend/src/pages/[lang]/bebidas.astro   ← NEW
frontend/src/pages/[lang]/desayuno.astro  ← NEW
frontend/src/pages/[lang]/streetfood.astro← NEW
frontend/src/pages/[lang]/carta.astro     ← NEW (redirect)
frontend/src/pages/[lang]/mesa.astro      ← NEW
frontend/src/pages/[lang]/test_mesa.astro ← NEW (redirect artifact)
```
The VPS production frontend source is at `/opt/portadirta/frontend/` (NOT a git repo — Docker builds from it directly). It's missing all 10 of those files.

### Backend — Same version, wrong config only
The backend code (PHP proxy, workflow-b JSON) is identical between local and VPS. **No code changes needed**, just config corrections.

### VPS structure
- `/opt/portadirta/` — production files Docker uses (NOT a git repo)
  - `/opt/portadirta/frontend/` — Astro source, rebuilt into Docker container
  - `/opt/portadirta/backend/` — n8n, PHP, docker-compose
- `/opt/portadirta-repo/` — git clone (separate, for version control)

---

## Current State (confirmed by SSH to 72.62.180.39)

### VPS Stack — All Running ✅
- `backend-frontend-1` — SSR Astro, port 4321, built today (Apr 2)
- `backend-n8n-1` — n8n, port 5678, up 7 days
- `backend-restaurant-1` — TastyIgniter, port 8081, up 7 days

### VPS Frontend — SSR mode ✅
- Built with `BUILD_TARGET=node` → `output: 'server'` → Node.js adapter
- Serves dynamically from `node ./dist/server/entry.mjs`
- Source: `/opt/portadirta/frontend/`
- Menu JSON volume mounted at `/app/data`

### VPS menu-data volume — All 5 files exist but NO TRANSLATIONS
```
taperia.json    — sections=['Tapas']            no translations
menu.json       — sections=[Aperitivos, Entrantes, Platos, Postres]  no translations
bebidas.json    — sections=[Aperitivos, Cervezas, ...]  no translations
desayuno.json   — sections=['Desayuno']         no translations
streetfood.json — sections=[Para Picar, Burgers, Pizzas, Postres]  no translations
```
Good news: the data is already there from a previous manual run. Just needs translations added.

### VPS n8n env vars — WRONG Doc IDs
```
MENU_CARTA_DOC_ID=12tEHjkxxkt...   ← WRONG: this is actually the Menú Especial doc
MENU_MENU_DOC_ID=1WYJCS8m5wN...   ← WRONG: unknown/unused doc
MENU_BEBIDAS_DOC_ID=REPLACE_...   ← NOT SET
```

### Correct Doc ID mapping (confirmed from Google Docs)
```
MENU_TAPERIA_DOC_ID   = 1a9wPRqGnud31JwCJANRFrXewJlQKOkK-AfKCXdW5djI
MENU_MENU_DOC_ID      = 12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE
MENU_BEBIDAS_DOC_ID   = 14A3S1EAhKBmcBGDXE8wka1kVVpe8V1fzIuP5PFUi0Ek
MENU_DESAYUNO_DOC_ID  = 1HGDUzyf2FhzN1uahdV6A1vk_L7FqRUe-eDZZNe09nss
MENU_STREETFOOD_DOC_ID= 14sxH4RfnDLc2XmrJhqM8rBaz0riJW5qetpiT29DHzDY
```

---

## Implementation — Executing Directly on VPS via SSH

### Step 1 — Copy missing frontend files to VPS
Upload via SFTP (paramiko) to `/opt/portadirta/frontend/`:
- `src/pages/[lang]/taperia.astro`
- `src/pages/[lang]/menu.astro`
- `src/pages/[lang]/bebidas.astro`
- `src/pages/[lang]/desayuno.astro`
- `src/pages/[lang]/streetfood.astro`
- `src/pages/[lang]/carta.astro`
- `src/pages/[lang]/mesa.astro`
- `src/pages/[lang]/test_mesa.astro`
- `src/i18n/translations.ts`
- `public/_redirects`

Then modify the 5 restaurant menu pages to add SSR JSON translation reading (see Step 5).

### Step 2 — Update 5 bundled fallback JSON files
**Files:** `/opt/portadirta/frontend/src/data/{taperia,menu,bebidas,desayuno,streetfood}.json`
Add empty translations field to each (so TypeScript type is correct):
```json
{
  "updated": "...",
  "sections": [...],
  "translations": {
    "en": { "sections": [] },
    "fr": { "sections": [] },
    "de": { "sections": [] }
  }
}
```

### Step 3 — Convert [lang]/ menu pages to SSR + JSON translation reading
For each of the 5 pages we just copied (taperia, menu, bebidas, desayuno, streetfood):
1. **Remove** `export const prerender = true` (not needed in full SSR mode)
2. **Remove** `getStaticPaths()` (not needed in SSR mode)
3. **Add** runtime lang validation at top of frontmatter:
   ```typescript
   const { lang } = Astro.params;
   if (!lang || !['en', 'fr', 'de'].includes(lang)) {
     return new Response(null, { status: 404 });
   }
   ```
4. **Add** JSON file reading from volume:
   ```typescript
   import fs from 'node:fs';
   import fallback from '../../data/taperia.json';
   let data: typeof fallback = fallback;
   const menuDataPath = process.env.MENU_DATA_PATH;
   if (menuDataPath) {
     try { data = JSON.parse(fs.readFileSync(`${menuDataPath}/taperia.json`, 'utf-8')); } catch {}
   }
   ```
5. **Add** translation-aware section reading:
   ```typescript
   const langData = (data as any).translations?.[lang];
   const sections = langData?.sections?.length ? langData.sections : data.sections;
   ```
6. Keep all hardcoded `ui` objects (page titles, allergen labels, CTA buttons) — they don't change when menus update.

### Step 4 — Fix `.env` doc IDs
**File:** `/opt/portadirta/backend/.env`
- Remove `MENU_CARTA_DOC_ID`
- Add 5 correct variables (see mapping above)

### Step 5 — Fix docker-compose.yml n8n env var references
**File:** `/opt/portadirta/backend/docker-compose.yml`
Replace the 3 old vars with 5 new ones.

### Step 6 — Expand PHP proxy to 5 menu types
**File:** `/opt/portadirta/backend/tastyigniter/routes/api.php` (line ~544)
```php
foreach (['taperia', 'menu', 'bebidas', 'desayuno', 'streetfood'] as $menuType) {
```
Update validation: all non-menu types require `sections`; `menu` requires `price` + `sections`.

### Step 7 — Update n8n workflow-b
**File:** `/opt/portadirta/backend/n8n-workflows/workflow-b-command-center.json`

Use Python to parse the JSON, patch 3 code nodes, write back:

**Node "Route Menu Command":** 5 commands (taperia/carta alias, menu, bebidas, desayuno, streetfood)

**Node "Build Menu Prompt":** 5 Claude prompts, all with translations schema:
- taperia: parse tapas list → JSON + EN/FR/DE translations
- menu: parse set menu → JSON + translations for root fields (name, priceNote, available) + sections
- bebidas: parse drinks → JSON + EN/FR/DE translations
- desayuno: parse breakfast description → JSON + EN/FR/DE translations
- streetfood: parse street food items → JSON + EN/FR/DE translations

**Node help text (Schema Validator):** Update `/carta` → `/taperia`, add `/desayuno` and `/streetfood`

**Node "Menu Command?" IF condition:** Add `/taperia`, `/desayuno`, `/streetfood` detection

After patching JSON file → update n8n via database (both `workflow_entity` and `workflow_history` tables per troubleshooting notes).

### Step 8 — Restart services
```bash
# Rebuild frontend with new pages
cd /opt/portadirta/backend && docker compose build frontend && docker compose up -d frontend

# Restart n8n to pick up new env vars
docker compose up -d n8n

# Re-register Telegram webhook (n8n clears it on restart)
sleep 10
curl -s -X POST "https://api.telegram.org/bot{TOKEN}/setWebhook" \
  -d "url=https://n8n.portadirta.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook"

# Restart TastyIgniter for PHP changes
docker restart backend-restaurant-1
```

### Step 9 — End-to-end test
1. Send `/taperia` → Telegram replies `✅ Taperia actualizada`
2. Check volume: `taperia.json` now has translations
3. Visit `https://www.portadirta.com/en/taperia` → English tapas
4. Visit `https://www.portadirta.com/fr/taperia` → French
5. Repeat for `/menu`, `/bebidas`, `/desayuno`, `/streetfood`

### Step 10 — Push local commits to GitHub (via VPS git key)
```bash
# On VPS: sync portadirta-repo with portadirta/ changes
cd /opt/portadirta-repo
git add frontend/src/pages/\[lang\]/ frontend/src/i18n/ frontend/public/_redirects
git add backend/n8n-workflows/workflow-b-command-center.json
git add backend/tastyigniter/routes/api.php backend/docker-compose.yml
git commit -m "feat: menu auto-update pipeline with EN/FR/DE translations"
git push  # uses /root/.ssh/github_vps
```

---

## Files Changed on VPS

| File | Change |
|---|---|
| `/opt/portadirta/backend/.env` | 5 correct doc IDs |
| `/opt/portadirta/backend/docker-compose.yml` | 5 env var references |
| `/opt/portadirta/backend/tastyigniter/routes/api.php` | whitelist 3→5 types |
| `/opt/portadirta/backend/n8n-workflows/workflow-b-command-center.json` | 5 commands + translations |
| `/opt/portadirta/frontend/src/pages/[lang]/taperia.astro` | NEW + SSR |
| `/opt/portadirta/frontend/src/pages/[lang]/menu.astro` | NEW + SSR |
| `/opt/portadirta/frontend/src/pages/[lang]/bebidas.astro` | NEW + SSR |
| `/opt/portadirta/frontend/src/pages/[lang]/desayuno.astro` | NEW + SSR |
| `/opt/portadirta/frontend/src/pages/[lang]/streetfood.astro` | NEW + SSR |
| `/opt/portadirta/frontend/src/pages/[lang]/carta.astro` | NEW (copy) |
| `/opt/portadirta/frontend/src/pages/[lang]/mesa.astro` | NEW (copy) |
| `/opt/portadirta/frontend/src/i18n/translations.ts` | Updated DE fix |
| `/opt/portadirta/frontend/public/_redirects` | Updated redirects |
| `/opt/portadirta/frontend/src/data/{5 files}.json` | Empty translations field |

## Current State (confirmed by SSH to 72.62.180.39)

### VPS Stack — All Running ✅
- `backend-frontend-1` — SSR Astro, port 4321, up 9h
- `backend-n8n-1` — n8n, port 5678, up 7 days
- `backend-restaurant-1` — TastyIgniter, port 8081, up 7 days
- `backend-events-1` — Hi.Events, up 7 days

### VPS Frontend — SSR mode ✅
- Built with `BUILD_TARGET=node` → `output: 'server'` → Node.js adapter
- Serves dynamically from `node ./dist/server/entry.mjs`
- Source: `/opt/portadirta/frontend/`
- Menu JSON volume mounted at `/app/data` (reads `MENU_DATA_PATH=/app/data`)

### VPS menu-data volume — All 5 files exist but NO TRANSLATIONS
```
taperia.json   — sections=['Tapas']                                          no translations
menu.json      — sections=['Aperitivos de bienvenida', 'Entrantes al centro', 'Platos a elegir', 'Postres caseros a elegir']  no translations
bebidas.json   — sections=['Aperitivos & Vermuts', 'Cervezas', ...]          no translations
desayuno.json  — sections=['Desayuno']                                       no translations
streetfood.json— sections=['Para Picar', 'Burgers', 'Pizzas', 'Postres']    no translations
carta.json     — sections=old bundled data                                   no translations
```

### VPS [lang]/ pages — MISSING 5 restaurant sub-menu pages
`/opt/portadirta/frontend/src/pages/[lang]/` only has:
`contacto.astro, eventos.astro, experiencias.astro, hotel.astro, index.astro, reservar.astro, restaurante.astro`
**MISSING:** taperia, menu, bebidas, desayuno, streetfood

### VPS git repo — 2 commits BEHIND local
VPS latest: `bfb1d5d fix: nav links, language switcher URLs, and hotel page i18n`
Local latest: `c6a3c11 feat: add [lang]/menu, fix DE translations, update redirects`
**The restaurant i18n pages (5acd2d4 + c6a3c11) were NEVER pushed to GitHub / deployed to VPS.**

### VPS n8n env vars — WRONG Doc IDs
```
MENU_CARTA_DOC_ID=12tEHjkxxkt...   ← this is actually the Menú Especial!
MENU_MENU_DOC_ID=1WYJCS8m5wN...   ← unknown / wrong doc
MENU_BEBIDAS_DOC_ID=REPLACE_WITH_BEBIDAS_DOC_ID  ← not set
```

### Correct Doc ID mapping (from user's Google Docs)
```
MENU_TAPERIA_DOC_ID   = 1a9wPRqGnud31JwCJANRFrXewJlQKOkK-AfKCXdW5djI
MENU_MENU_DOC_ID      = 12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE  (Menú Especial)
MENU_BEBIDAS_DOC_ID   = 14A3S1EAhKBmcBGDXE8wka1kVVpe8V1fzIuP5PFUi0Ek
MENU_DESAYUNO_DOC_ID  = 1HGDUzyf2FhzN1uahdV6A1vk_L7FqRUe-eDZZNe09nss
MENU_STREETFOOD_DOC_ID= 14sxH4RfnDLc2XmrJhqM8rBaz0riJW5qetpiT29DHzDY
```

---

## Implementation — Executing Directly on VPS via SSH

All changes are made directly on the VPS. The frontend Docker container will be rebuilt with the updated source. No `git push` required from the local machine.

### Step 1 — Fix `.env` doc IDs
**File:** `/opt/portadirta/backend/.env`
- Remove `MENU_CARTA_DOC_ID`
- Add 5 correct variables:
  ```
  MENU_TAPERIA_DOC_ID=1a9wPRqGnud31JwCJANRFrXewJlQKOkK-AfKCXdW5djI
  MENU_MENU_DOC_ID=12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE
  MENU_BEBIDAS_DOC_ID=14A3S1EAhKBmcBGDXE8wka1kVVpe8V1fzIuP5PFUi0Ek
  MENU_DESAYUNO_DOC_ID=1HGDUzyf2FhzN1uahdV6A1vk_L7FqRUe-eDZZNe09nss
  MENU_STREETFOOD_DOC_ID=14sxH4RfnDLc2XmrJhqM8rBaz0riJW5qetpiT29DHzDY
  ```

### Step 2 — Fix docker-compose.yml n8n env var references
**File:** `/opt/portadirta/backend/docker-compose.yml`
Replace:
```yaml
- MENU_CARTA_DOC_ID=${MENU_CARTA_DOC_ID}
- MENU_MENU_DOC_ID=${MENU_MENU_DOC_ID}
- MENU_BEBIDAS_DOC_ID=${MENU_BEBIDAS_DOC_ID}
```
With:
```yaml
- MENU_TAPERIA_DOC_ID=${MENU_TAPERIA_DOC_ID}
- MENU_MENU_DOC_ID=${MENU_MENU_DOC_ID}
- MENU_BEBIDAS_DOC_ID=${MENU_BEBIDAS_DOC_ID}
- MENU_DESAYUNO_DOC_ID=${MENU_DESAYUNO_DOC_ID}
- MENU_STREETFOOD_DOC_ID=${MENU_STREETFOOD_DOC_ID}
```

### Step 3 — Expand PHP proxy to 5 menu types
**File:** `/opt/portadirta/backend/tastyigniter/routes/api.php` (line ~544)
Change:
```php
foreach (['carta', 'menu', 'bebidas'] as $menuType) {
```
To:
```php
foreach (['taperia', 'menu', 'bebidas', 'desayuno', 'streetfood'] as $menuType) {
```
Update validation: remove the `carta`/`bebidas` grouping, add `desayuno` and `streetfood` to the `sections`-required group.

### Step 4 — Update n8n workflow-b (biggest change)
**File:** `/opt/portadirta/backend/n8n-workflows/workflow-b-command-center.json`
Use Python+paramiko to read the JSON, patch specific code nodes, then write back.

**Node: "Menu Command?" (IF node)**
Update condition to also detect `/taperia`, `/desayuno`, `/streetfood`:
```javascript
text.startsWith('/carta') || text.startsWith('/taperia') ||
text.startsWith('/menu') || text.startsWith('/bebidas') ||
text.startsWith('/desayuno') || text.startsWith('/streetfood')
```

**Node: "Route Menu Command" (Code node)**
Replace 3-command routing with 5:
```javascript
const lower = (text || '').toLowerCase().trim();
let menuType = '', docId = '';

if (lower.startsWith('/taperia') || lower.startsWith('/carta')) {
  menuType = 'taperia'; docId = $env.MENU_TAPERIA_DOC_ID || '';
} else if (lower.startsWith('/menu')) {
  menuType = 'menu'; docId = $env.MENU_MENU_DOC_ID || '';
} else if (lower.startsWith('/bebidas')) {
  menuType = 'bebidas'; docId = $env.MENU_BEBIDAS_DOC_ID || '';
} else if (lower.startsWith('/desayuno')) {
  menuType = 'desayuno'; docId = $env.MENU_DESAYUNO_DOC_ID || '';
} else if (lower.startsWith('/streetfood')) {
  menuType = 'streetfood'; docId = $env.MENU_STREETFOOD_DOC_ID || '';
}
if (!docId || docId.startsWith('REPLACE_')) {
  return [{ json: { error: `⚠️ No configurado: añade MENU_${menuType.toUpperCase()}_DOC_ID`, chatId, menuType, isError: true }}];
}
return [{ json: { menuType, docId, chatId, tier, isError: false } }];
```

**Node: "Build Menu Prompt" (Code node)**
This is the most critical change. Add EN/FR/DE translations to ALL 5 prompts:

All 5 schemas must include a `translations` field:
```json
"translations": {
  "en": { "sections": [ /* same structure as sections, all text translated to English */ ] },
  "fr": { "sections": [ /* French */ ] },
  "de": { "sections": [ /* German */ ] }
}
```

The `/menu` schema also needs translation for root fields:
```json
"translations": {
  "en": { "name": "Special Menu", "priceNote": "per person — bread and water included", "available": "Saturdays and Sundays", "sections": [...] },
  "fr": { ... },
  "de": { ... }
}
```

5 prompts needed:
1. **taperia**: tapas with prices, allergens → EN/FR/DE translations of section + item names/descriptions
2. **menu**: set menu with price, courses, supplements → EN/FR/DE of name, priceNote, available, sections
3. **bebidas**: drinks grouped by category → EN/FR/DE of section + item names
4. **desayuno**: breakfast description + price → EN/FR/DE of section name and item description
5. **streetfood**: burgers/pizzas/snacks with prices → EN/FR/DE of section + item names

**Node: Schema Validator help menu text**
Update the help section from:
```
'• /carta — Actualiza la carta desde Google Docs',
'• /menu — Actualiza el menú del día',
'• /bebidas — Actualiza la carta de bebidas',
```
To:
```
'• /taperia — Actualiza la carta de tapas',
'• /menu — Actualiza el menú especial',
'• /bebidas — Actualiza la carta de bebidas',
'• /desayuno — Actualiza el menú de desayuno',
'• /streetfood — Actualiza el street food',
```

**After patching the JSON file:**
Import into n8n via database patch (per troubleshooting notes — must update BOTH `workflow_entity` AND `workflow_history` tables, then restart n8n):
```python
# Connect to n8n postgres
# UPDATE workflow_entity SET nodes = <new nodes json> WHERE id = 'av9R2wseN47PQZ8S'
# INSERT into workflow_history ... 
# docker restart backend-n8n-1
```

### Step 5 — Create 5 new [lang]/ Astro pages (SSR)
**Directory:** `/opt/portadirta/frontend/src/pages/[lang]/`

These pages don't exist on VPS yet. Create them with SSR + JSON translation reading:

Pattern for all 5 pages (using taperia as example):
```typescript
---
import fs from 'node:fs';
import Layout from '../../layouts/Layout.astro';
// ... other imports

// SSR: validate lang param
const { lang } = Astro.params;
if (!lang || !['en', 'fr', 'de'].includes(lang)) {
  return new Response(null, { status: 404 });
}

// SSR: read from shared volume, fallback to bundled
import fallback from '../../data/taperia.json';
let data: typeof fallback = fallback;
const menuDataPath = process.env.MENU_DATA_PATH;
if (menuDataPath) {
  try { data = JSON.parse(fs.readFileSync(`${menuDataPath}/taperia.json`, 'utf-8')); } catch {}
}

// Use JSON translations if available, else fall back to Spanish sections
const langSections = (data as any).translations?.[lang]?.sections;
const sections = langSections?.length ? langSections : data.sections;

// Hardcoded UI chrome (titles, allergen labels, CTA buttons)
const ui = {
  en: { title: "La Tapería", subtitle: "...", /* etc */ },
  fr: { ... },
  de: { ... },
} as const;
const t = ui[lang as keyof typeof ui];
---
```

Each page keeps its existing hardcoded `ui` object for:
- Page title, subtitle, description
- Allergen labels dictionary
- CTA button text, schedule text
- Any other non-menu-item text

Only the menu SECTIONS (item names, descriptions, prices) come from the JSON.

Pages to create: `taperia.astro`, `menu.astro`, `bebidas.astro`, `desayuno.astro`, `streetfood.astro`

Note: `getStaticPaths` is OMITTED — in full SSR mode it's not needed.

### Step 6 — Update bundled fallback JSON files
**Files:** `/opt/portadirta/frontend/src/data/{taperia,menu,bebidas,desayuno,streetfood}.json`

Add empty translations field (so the TypeScript type inference works):
```json
{
  "updated": "...",
  "sections": [...],
  "translations": {
    "en": { "sections": [] },
    "fr": { "sections": [] },
    "de": { "sections": [] }
  }
}
```

### Step 7 — Rebuild + restart frontend container
```bash
cd /opt/portadirta/backend
docker compose build frontend
docker compose up -d frontend
```

### Step 8 — Restart n8n with new env vars
```bash
cd /opt/portadirta/backend
docker compose up -d n8n
# Re-register Telegram webhook (n8n clears it on restart):
sleep 10
curl -s -X POST \
  "https://api.telegram.org/bot8348668157:AAEMAD_F37GNJJZxOd4C5krZg4OnPaZ_MD4/setWebhook" \
  -d "url=https://n8n.portadirta.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook"
```

### Step 9 — Restart TastyIgniter for PHP changes
```bash
docker restart backend-restaurant-1
```

### Step 10 — Verify the pipeline
1. Send `/taperia` to Telegram bot → expect `✅ Taperia actualizada` reply
2. Check `cat /var/lib/docker/volumes/backend_menu-data/_data/taperia.json | python3 -c "import sys,json;d=json.load(sys.stdin);print(list(d.get('translations',{}).keys()))"`
3. Visit `https://www.portadirta.com/en/taperia` → should show English tapas
4. Visit `https://www.portadirta.com/fr/taperia` → French
5. Repeat for `/menu`, `/bebidas`, `/desayuno`, `/streetfood`

### Step 11 — Push changes to git (for version control)
```bash
cd /opt/portadirta-repo
git add -A
git commit -m "feat: menu auto-update pipeline with i18n support"
git push  # uses /root/.ssh/github_vps
```

---

## Execution Order (with dependencies)

```
Step 1 (env) ─┐
Step 2 (yml) ──┤── Step 8 (restart n8n) ─── Step 10 (test)
Step 3 (php) ──┴── Step 9 (restart TI)    /
Step 4 (workflow-b) ─── import n8n ──────/
Step 5 (new pages) ─┬── Step 7 (rebuild) ─/
Step 6 (fallback) ──┘
```

Steps 1–6 can be done in parallel. Steps 7–10 are sequential.

---

## Files Changed on VPS

| File | Type | Change |
|---|---|---|
| `/opt/portadirta/backend/.env` | Config | 5 correct doc IDs |
| `/opt/portadirta/backend/docker-compose.yml` | Config | 5 env var references |
| `/opt/portadirta/backend/tastyigniter/routes/api.php` | PHP | whitelist + validation |
| `/opt/portadirta/backend/n8n-workflows/workflow-b-command-center.json` | JSON | 5 commands + translations |
| `/opt/portadirta/frontend/src/pages/[lang]/taperia.astro` | Astro | NEW — SSR + JSON translations |
| `/opt/portadirta/frontend/src/pages/[lang]/menu.astro` | Astro | NEW — SSR + JSON translations |
| `/opt/portadirta/frontend/src/pages/[lang]/bebidas.astro` | Astro | NEW — SSR + JSON translations |
| `/opt/portadirta/frontend/src/pages/[lang]/desayuno.astro` | Astro | NEW — SSR + JSON translations |
| `/opt/portadirta/frontend/src/pages/[lang]/streetfood.astro` | Astro | NEW — SSR + JSON translations |
| `/opt/portadirta/frontend/src/data/taperia.json` | JSON | add translations field |
| `/opt/portadirta/frontend/src/data/menu.json` | JSON | add translations field |
| `/opt/portadirta/frontend/src/data/bebidas.json` | JSON | add translations field |
| `/opt/portadirta/frontend/src/data/desayuno.json` | JSON | add translations field |
| `/opt/portadirta/frontend/src/data/streetfood.json` | JSON | add translations field |

## Current State Audit

### What IS working ✅
- **n8n running locally** (`backend-n8n-1`, up 2 days) exposed via Cloudflare Tunnel at `n8n.hobbitonranch.com`
- **Workflow-b imported** — `/carta` command has been tested at least once
- **carta.json in shared Docker volume** (16KB, 2026-03-24) WITH EN/FR/DE translations
- **PHP proxy functional** at `http://restaurant/api/internal/menu/{type}` (auth: `X-Internal-Token: portadirta-n8n-2026`)
- **Spanish root pages are SSR** — read from `MENU_DATA_PATH` at request time with fallback to bundled JSON
- **5 Google Docs** exist — one per sub-menu, all shared publicly

### What is NOT working ❌

#### 1. Wrong Doc ID mapping (CRITICAL CONFIG BUG)
Current env vars are WRONG:
- `MENU_CARTA_DOC_ID=12tEHjkxxkt...` → This is actually the **Menú Especial**, not the carta/taperia!
- `MENU_MENU_DOC_ID=1WYJCS8m5wN...` → Unknown doc, not in the user's current list
So `/carta` has been parsing the SET MENU document and writing it as `carta.json` — wrong data entirely.

#### 2. File naming mismatch
- n8n `/carta` writes `carta.json` to shared volume
- Astro `taperia.astro` reads `taperia.json` — NEVER finds the n8n-written file
- Only `carta.json` exists in the volume; no `taperia.json`, `menu.json`, `bebidas.json`, etc.

#### 3. Only 3 of 5 menus have Telegram commands
- n8n supports: `/carta`, `/menu`, `/bebidas`
- Missing: `/taperia` (or rename `/carta`), `/desayuno`, `/streetfood`
- No env vars for the 2 new doc IDs

#### 4. Translation schema missing from `/menu` and `/bebidas` prompts
- `/carta` prompt includes `translations: { en, fr, de }` ✅
- `/menu` prompt → NO translations field ❌
- `/bebidas` prompt → NO translations field ❌
- No prompts exist for desayuno or streetfood

#### 5. [lang]/ pages are static — don't read JSON translations
- All 5 `[lang]/*.astro` pages have `export const prerender = true`
- Menu items are read from JSON at BUILD TIME only
- All UI text is hardcoded per-page
- Even if JSON had translations, these pages wouldn't serve them dynamically

#### 6. PHP proxy only accepts 3 menu types
- Whitelist: `['carta', 'menu', 'bebidas']`
- Missing: `taperia`, `desayuno`, `streetfood`

#### 7. Frontend Docker container not running
- No `backend-frontend-1` container
- Site served from Cloudflare Pages (static SSG) — all "SSR" reading from MENU_DATA_PATH is dead code

---

## Google Doc → File → Page Mapping (Corrected)

| Google Doc | Doc ID | Telegram Cmd | Env Var | JSON File | Astro Page |
|---|---|---|---|---|---|
| Menú Especial | `12tEHjkxxkt...` | `/menu` | `MENU_MENU_DOC_ID` | `menu.json` | `/menu` |
| La Taperia | `1a9wPRqGnud...` | `/taperia` | `MENU_TAPERIA_DOC_ID` | `taperia.json` | `/taperia` |
| Bebidas y Bodega | `14A3S1EAhKB...` | `/bebidas` | `MENU_BEBIDAS_DOC_ID` | `bebidas.json` | `/bebidas` |
| Desayuno | `1HGDUzyf2Fh...` | `/desayuno` | `MENU_DESAYUNO_DOC_ID` | `desayuno.json` | `/desayuno` |
| Street Food | `14sxH4RfnDL...` | `/streetfood` | `MENU_STREETFOOD_DOC_ID` | `streetfood.json` | `/streetfood` |

Full Doc IDs:
- MENU_MENU_DOC_ID=12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE
- MENU_TAPERIA_DOC_ID=1a9wPRqGnud31JwCJANRFrXewJlQKOkK-AfKCXdW5djI
- MENU_BEBIDAS_DOC_ID=14A3S1EAhKBmcBGDXE8wka1kVVpe8V1fzIuP5PFUi0Ek
- MENU_DESAYUNO_DOC_ID=1HGDUzyf2FhzN1uahdV6A1vk_L7FqRUe-eDZZNe09nss
- MENU_STREETFOOD_DOC_ID=14sxH4RfnDLc2XmrJhqM8rBaz0riJW5qetpiT29DHzDY

---

## Implementation Plan

### Phase 1: Fix n8n Workflow-B (the brain)

**File:** `backend/n8n-workflows/workflow-b-command-center.json`

#### 1A. Update Route Menu Command node
Replace 3-command routing with 5-command routing:
```javascript
if (lower.startsWith('/taperia') || lower.startsWith('/carta')) {
  menuType = 'taperia';
  docId = $env.MENU_TAPERIA_DOC_ID || '';
} else if (lower.startsWith('/menu')) {
  menuType = 'menu';
  docId = $env.MENU_MENU_DOC_ID || '';
} else if (lower.startsWith('/bebidas')) {
  menuType = 'bebidas';
  docId = $env.MENU_BEBIDAS_DOC_ID || '';
} else if (lower.startsWith('/desayuno')) {
  menuType = 'desayuno';
  docId = $env.MENU_DESAYUNO_DOC_ID || '';
} else if (lower.startsWith('/streetfood')) {
  menuType = 'streetfood';
  docId = $env.MENU_STREETFOOD_DOC_ID || '';
}
```

#### 1B. Update Menu Command? detection node
Add `/taperia`, `/desayuno`, `/streetfood` to the regex/startsWith check.

#### 1C. Update Build Menu Prompt node — add/fix ALL 5 prompts

**Every prompt must include this translations schema:**
```json
"translations": {
  "en": { "sections": [/*same structure as sections, translated*/] },
  "fr": { "sections": [/*...*/] },
  "de": { "sections": [/*...*/] }
}
```

**5 Claude prompts needed:**

1. **taperia** (replaces carta): Parse tapas with prices, allergens, EN/FR/DE translations
2. **menu**: Parse set menu with price, courses, supplements, allergens, EN/FR/DE translations
   - Also translate: `name`, `priceNote`, `available` fields
3. **bebidas**: Parse drinks by section (bodega, coctelería), EN/FR/DE translations
4. **desayuno** (NEW): Parse breakfast description + price, EN/FR/DE translations
5. **streetfood** (NEW): Parse street food items with prices, allergens, EN/FR/DE translations

#### 1D. Update help menu in Schema Validator
Replace `/carta` with `/taperia` in the help text, add `/desayuno` and `/streetfood`.

---

### Phase 2: Fix PHP Proxy (the writer)

**File:** `backend/tastyigniter/routes/api.php`

#### 2A. Expand menu type whitelist
```php
foreach (['taperia', 'menu', 'bebidas', 'desayuno', 'streetfood'] as $menuType) {
```

#### 2B. Update validation rules
- `taperia`, `bebidas`, `streetfood`, `desayuno`: require `sections` array
- `menu`: require `price` + `sections`

---

### Phase 3: Fix Docker configuration

**File:** `backend/docker-compose.yml`

#### 3A. Update env vars for n8n service
Remove old `MENU_CARTA_DOC_ID`, add all 5:
```yaml
- MENU_TAPERIA_DOC_ID=${MENU_TAPERIA_DOC_ID}
- MENU_MENU_DOC_ID=${MENU_MENU_DOC_ID}
- MENU_BEBIDAS_DOC_ID=${MENU_BEBIDAS_DOC_ID}
- MENU_DESAYUNO_DOC_ID=${MENU_DESAYUNO_DOC_ID}
- MENU_STREETFOOD_DOC_ID=${MENU_STREETFOOD_DOC_ID}
```

#### 3B. Create/update `.env` file with actual doc IDs
```
MENU_MENU_DOC_ID=12tEHjkxxktMUzgj1Wq006gL56Qor9xButJ9JR-VKXeE
MENU_TAPERIA_DOC_ID=1a9wPRqGnud31JwCJANRFrXewJlQKOkK-AfKCXdW5djI
MENU_BEBIDAS_DOC_ID=14A3S1EAhKBmcBGDXE8wka1kVVpe8V1fzIuP5PFUi0Ek
MENU_DESAYUNO_DOC_ID=1HGDUzyf2FhzN1uahdV6A1vk_L7FqRUe-eDZZNe09nss
MENU_STREETFOOD_DOC_ID=14sxH4RfnDLc2XmrJhqM8rBaz0riJW5qetpiT29DHzDY
```

---

### Phase 4: Convert [lang]/ pages to SSR + JSON translations

**Files:** `frontend/src/pages/[lang]/{taperia,menu,bebidas,desayuno,streetfood}.astro`

For each page:

#### 4A. Remove static prerendering
```diff
- export const prerender = true;
```
Keep `getStaticPaths()` for Cloudflare Pages compatibility (ignored in server mode).

#### 4B. Add SSR JSON reading (same pattern as Spanish pages)
```typescript
import fs from 'node:fs';
import fallbackData from '../../data/taperia.json';

let data = fallbackData;
const menuDataPath = process.env.MENU_DATA_PATH;
if (menuDataPath) {
  try { data = JSON.parse(fs.readFileSync(`${menuDataPath}/taperia.json`, 'utf-8')); } catch {}
}
```

#### 4C. Read translated sections from JSON, fallback to hardcoded
```typescript
const langSections = data.translations?.[lang]?.sections;
const sections = langSections?.length ? langSections : data.sections;
// If langSections empty (n8n hasn't run yet), show Spanish with translated UI chrome
```

#### 4D. Keep hardcoded UI chrome
Page titles, allergen labels, CTA buttons, schedule text — these don't change when menus update and are already translated in the hardcoded `ui` objects.

#### 4E. Add runtime lang validation
```typescript
const { lang } = Astro.params;
if (!['en', 'fr', 'de'].includes(lang!)) {
  return new Response(null, { status: 404 });
}
```

---

### Phase 5: Update bundled fallback JSON files

**Files:** `frontend/src/data/{taperia,menu,bebidas,desayuno,streetfood}.json`

Add empty translations field to each:
```json
{
  "updated": "...",
  "sections": [...],
  "translations": {
    "en": { "sections": [] },
    "fr": { "sections": [] },
    "de": { "sections": [] }
  }
}
```

Also update `carta.json` (though it's mostly unused after renaming).

---

### Phase 6: Test locally

1. Restart n8n with new env vars: `docker compose up -d n8n`
2. Re-import workflow-b (or update via n8n API)
3. Re-register Telegram webhook
4. Send `/taperia` → verify `taperia.json` written with translations
5. Send `/menu` → verify `menu.json` with translations
6. Send `/bebidas`, `/desayuno`, `/streetfood` → verify all
7. Start frontend container: `docker compose up -d frontend`
8. Check all pages render correctly in all 4 languages

### Phase 7: Deploy to VPS

1. `git push` (user runs manually)
2. SSH to VPS → pull latest → `docker compose up -d`
3. Import updated workflow-b in n8n UI
4. Re-register Telegram webhook
5. Full end-to-end test

---

## Files Changed Summary

| File | Change Type |
|---|---|
| `backend/n8n-workflows/workflow-b-command-center.json` | Major: 5 commands, 5 prompts, all with translations |
| `backend/tastyigniter/routes/api.php` | Minor: expand whitelist to 5 types |
| `backend/docker-compose.yml` | Minor: 5 env vars instead of 3 |
| `backend/.env` | Minor: actual doc IDs |
| `frontend/src/pages/[lang]/taperia.astro` | Medium: SSR + JSON translation reading |
| `frontend/src/pages/[lang]/menu.astro` | Medium: SSR + JSON translation reading |
| `frontend/src/pages/[lang]/bebidas.astro` | Medium: SSR + JSON translation reading |
| `frontend/src/pages/[lang]/desayuno.astro` | Medium: SSR + JSON translation reading |
| `frontend/src/pages/[lang]/streetfood.astro` | Medium: SSR + JSON translation reading |
| `frontend/src/data/{5 files}.json` | Minor: add empty translations field |

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Current `carta.json` in volume is wrong data (Menú parsed as Carta) | Will be overwritten on first `/taperia` run |
| Claude produces inconsistent translations | Validate section count matches ES; alert on mismatch |
| [lang]/ pages slower as SSR | Menu QR pages — latency acceptable, not SEO-critical |
| Cloudflare Pages static build breaks | `getStaticPaths` kept; pages prerender with bundled fallback |
| n8n restart clears Telegram webhook | Document re-registration command in deployment checklist |
| Desayuno doc is very short (1 item) | Claude prompt still works; produces valid JSON for 1-item menu |

---

## 2026-04-03 Closure Snapshot

- Menu command pipeline stabilized in production with live confirmations for `/bebidas` and `/taperia`.
- Translation rendering bug on `[lang]` menu pages resolved by merge-based strategy preserving non-translated structured fields.
- Localized mesa pages restored and translated (`/en/mesa`, `/fr/mesa`, `/de/mesa`) after route/runtime alignment and frontend image redeploy.
- Runtime parity issue between compose and n8n container env fixed (`MENU_CARTA_DOC_ID` passthrough).
- Restaurant API internal write endpoints expanded for all menu targets used by bot automation.
