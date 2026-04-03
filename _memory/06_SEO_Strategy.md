---
type: strategy
status: active
last-audited: 2026-03-23
tags: [seo, marketing, content, local, ai-crawlers, structured-data, multilingual]
---

# 🔍 SEO Master Plan — Porta D'irta
*Full audit + implementation roadmap. Last updated 2026-03-23.*

---

## 1. Audit Snapshot — Current Technical State

### ✅ Already Correct
- Canonical URLs on every page via `Layout.astro` (generated from `Astro.url.pathname` + `site: portadirta.com`)
- Open Graph + Twitter Card meta on every page (title, description, image)
- JSON-LD `LodgingBusiness` on `/hotel` · `Restaurant` on `/restaurante` · `Event` per package on `/experiencias`
- `BreadcrumbList` JSON-LD on `/hotel`, `/restaurante`, `/experiencias`, `/eventos`, `/contacto`, `/reservar`
- `FAQPage` JSON-LD on `/hotel`
- NAP consistent: Camí del Pebret s/n · 12598 Peñíscola · +34 644 026 066 (Footer + JSON-LD)
- Hero poster preload hint in `index.astro`
- AI crawler directives in `robots.txt` — GPTBot/ClaudeBot/PerplexityBot allowed; CCBot/omgili blocked
- SEO crawler rate-limiting — AhrefsBot/SemrushBot `Crawl-delay: 10`
- `sitemap.xml` declared in `robots.txt`
- Google Fonts loaded with `preconnect` + `display=swap` (FOIT prevention)
- `loading="lazy"` + `decoding="async"` on all content images
- Descriptive alt text on all content images; decorative images `aria-hidden="true"`
- Legal pages present: `/legal`, `/privacidad`, `/cookies` — GDPR compliant
- Security headers in `public/_headers` (CSP, HSTS)
- i18n routing configured in `astro.config.mjs`: default=`es`, subdirectory strategy for en/fr/de
- `trailingSlash: 'never'` prevents duplicate-URL issues
- `site: 'https://www.portadirta.com'` set in `astro.config.mjs`
- GDPR consent checkboxes on all 4 forms

### 🔴 CRITICAL — Fix Before Launch

| # | Issue | File | Line(s) | Impact |
|---|-------|------|---------|--------|
| C1 | `hobbitonranch.com` hardcoded in event content files | `src/content/eventos-locales/cena-maridaje.md`, `noche-jazz-terraza.md` | `ticketsUrl` field | Broken links post-launch |
| C2 | `hobbitonranch.com` fallback URL in experiencias | `src/pages/experiencias.astro` | ~78 | If env var unset, tickets go to wrong domain |
| C3 | `hobbitonranch.com` in `SustainabilityStatus.astro` | `src/components/SustainabilityStatus.astro` | commented section | Will break when uncommented |
| C4 | No `hreflang` tags declared anywhere | `src/layouts/Layout.astro` | missing from `<head>` | Google duplicate content penalty across language versions |
| C5 | Language pages (`/en/`, `/fr/`, `/de/`) missing from `sitemap.xml` | `public/sitemap.xml` | all entries | Multilingual pages not discovered by crawlers |
| C6 | Static `sitemap.xml` will go out of sync | `public/sitemap.xml` | — | Must migrate to `@astrojs/sitemap` before multilingual launch |
| C7 | `og:url` missing from `<head>` entirely | `src/layouts/Layout.astro` | `<head>` block | Breaks Facebook/LinkedIn Open Graph previews |
| C8 | `og:image:width` / `og:image:height` missing | `src/layouts/Layout.astro` | `<head>` block | OG validators warn; some social cards won't render |

### 🟠 HIGH — Fix in First Week After Launch

| # | Issue | File | Line(s) | Impact |
|---|-------|------|---------|--------|
| H1 | `ogImage` default is `picsum.photos` random placeholder | `src/layouts/Layout.astro` | ~39 | Every page without explicit `ogImage` shows random photo on social share |
| H2 | Missing custom `ogImage` on `/experiencias`, `/contacto`, `/reservar` | `src/pages/experiencias.astro`, `contacto.astro`, `reservar.astro` | front matter | Social shares look unbranded |
| H3 | `/reservar` has `noindex={true}` | `src/pages/reservar.astro` | ~18 | Page excluded from organic search; won't rank for "reservar hotel Peñíscola" |
| H4 | Room content only inside Beds24 iframe | `src/pages/hotel.astro` | iframe section | Google cannot crawl/index any room information — biggest content gap |
| H5 | Restaurant menu is styled cards with no indexable text | `src/pages/restaurante.astro` | menu section | Dish names/prices unindexable; misses "arroz caldoso Peñíscola" etc. |
| H6 | Weak H1 on language placeholder pages | `src/pages/en/index.astro`:27, `fr/index.astro`:24, `de/index.astro`:24 | Describes page status, not property | Weak keyword signal for the locale |
| H7 | JSON-LD `description` fields too short/marketing-y | `hotel.astro`, `restaurante.astro` | JSON-LD blocks | AI tools (Perplexity, ChatGPT) quote these verbatim — need factual 200+ char sentences |
| H8 | `LodgingBusiness` JSON-LD missing `numberOfRooms`, `checkinTime`, `checkoutTime` | `src/pages/hotel.astro` | JSON-LD block | Incomplete hotel schema; Google Hotels integration weakened |
| H9 | `Restaurant` JSON-LD missing `acceptsReservations`, `menu`, `servesCuisine` | `src/pages/restaurante.astro` | JSON-LD block | Incomplete restaurant schema; TheFork/Google integration weakened |
| H10 | No analytics — blind to which pages/keywords drive bookings | — | — | Cannot measure or improve anything |

### 🟡 MEDIUM — Month 1

| # | Issue | File | Impact |
|---|-------|------|--------|
| M1 | Google Fonts loaded via external `<link>` — render-blocking | `Layout.astro` ~91 | −10–15 PageSpeed on mobile |
| M2 | Images missing explicit `width`/`height` on several pages | Various | CLS (layout shift) |
| M3 | No `aggregateRating` in JSON-LD (need reviews first) | `hotel.astro`, `restaurante.astro` | No star ratings in SERPs |
| M4 | Internal linking opportunities missed | Page body text | PageRank distribution, crawl budget |
| M5 | No `prefers-reduced-motion` CSS on hero `<video>` | `index.astro` | Accessibility + performance on low-motion devices |
| M6 | Experiencias page title/description too generic | `experiencias.astro` front matter | Misses "kayak Peñíscola", "senderismo Sierra de Irta" etc. |
| M7 | No Google Site Verification meta slot | `Layout.astro` | Can't verify GSC until this is added |

### 🟢 LOW — Ongoing / Nice-to-Have

| # | Issue | Impact |
|---|--------|--------|
| L1 | 404 page has no helpful internal links | Lost users don't recover |
| L2 | No blog/content section | Missing long-tail organic acquisition channel |
| L3 | No Wikidata entity for Porta D'irta | AI tools have no structured machine-readable anchor |
| L4 | No `Event` schema on `/eventos` page for actual events | Missed event rich results |
| L5 | No `FAQ` schema on `/experiencias` | Missed FAQ rich results for activity questions |

---

## 2. Implementation Roadmap

### Wave 0 — Critical Fixes (Before Go-Live)

#### Code changes

- [ ] **C1/C2/C3 — Fix hobbitonranch.com URLs**
  - `src/content/eventos-locales/*.md` → change `ticketsUrl` to `https://events.portadirta.com` (or whatever production URL will be)
  - `src/pages/experiencias.astro:78` → change fallback from `events.hobbitonranch.com` to `events.portadirta.com`
  - `SustainabilityStatus.astro` → update commented URL for when it goes live

- [ ] **C4 — Add hreflang tags to `Layout.astro`**
  ```html
  <!-- In <head>, after canonical tag -->
  <link rel="alternate" hreflang="es" href={`https://www.portadirta.com${Astro.url.pathname}`} />
  <link rel="alternate" hreflang="en" href={`https://www.portadirta.com/en${Astro.url.pathname}`} />
  <link rel="alternate" hreflang="fr" href={`https://www.portadirta.com/fr${Astro.url.pathname}`} />
  <link rel="alternate" hreflang="de" href={`https://www.portadirta.com/de${Astro.url.pathname}`} />
  <link rel="alternate" hreflang="x-default" href={`https://www.portadirta.com${Astro.url.pathname}`} />
  ```
  Note: Only add when the language page actually exists. Until /en/, /fr/, /de/ are fully translated, add only the es + x-default entries.

- [ ] **C5/C6 — Migrate to `@astrojs/sitemap`**
  ```bash
  npm install @astrojs/sitemap
  ```
  In `astro.config.mjs`:
  ```js
  import sitemap from '@astrojs/sitemap';
  export default defineConfig({
    site: 'https://www.portadirta.com',
    integrations: [sitemap({ i18n: { defaultLocale: 'es', locales: { es: 'es-ES', en: 'en-GB', fr: 'fr-FR', de: 'de-DE' } } })],
  })
  ```
  Delete `public/sitemap.xml` after confirming `@astrojs/sitemap` generates it at build time.

- [ ] **C7/C8 — Fix OG tags in `Layout.astro`**
  Add to `<head>`:
  ```html
  <meta property="og:url" content={canonicalUrl} />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  ```

- [ ] **H1 — Replace picsum OG default**
  - Design a 1200×630 branded image: property exterior shot + "Porta D'irta" wordmark in bottom-left
  - Save as `/public/assets/images/og-default.jpg`
  - In `Layout.astro`: change default ogImage from `picsum.photos/1200/630` to `/assets/images/og-default.jpg`

- [ ] **M7 — Add Google Site Verification slot**
  In `Layout.astro` `<head>`:
  ```html
  {googleSiteVerification && <meta name="google-site-verification" content={googleSiteVerification} />}
  ```
  Pass `googleSiteVerification` as a Layout prop (or read from env var) so it can be set without code changes.

#### Manual actions (no code)

- [ ] **Create Google Business Profile** — business.google.com — START NOW (postcard verification takes 2 weeks)
  - Category: "Hotel de lujo" (primary) + "Restaurante" (secondary)
  - Photos: 25+ images — exterior, all 3 rooms, restaurant, terrace, food dishes, pool, Sierra de Irta views
  - Hours: Hotel 24h / Restaurant 13–16h + 20–22h every day
  - Attributes: WiFi, Piscina, Restaurante propio, Admite reservas
  - Q&A: pre-seed with 5 common questions (check-in time, parking, pets, restaurant opening, nearest beach)
  - Link to `https://www.portadirta.com`

- [ ] **Google Search Console** — verify portadirta.com, submit sitemap URL

---

### Wave 1 — High Priority (First 2 Weeks After Launch)

#### Code changes

- [ ] **H2 — Add custom ogImage to missing pages**
  - `experiencias.astro` front matter → `ogImage: '/assets/images/sierra-tower-wide.jpg'`
  - `contacto.astro` front matter → `ogImage: '/assets/images/property-aerial-pool.jpg'`
  - `reservar.astro` front matter → `ogImage: '/assets/images/room-1.jpg'` (or best room photo)

- [ ] **H3 — Fix noindex on /reservar**
  Remove `noindex={true}` from `src/pages/reservar.astro`.
  Instead add: `<link rel="canonical" href="https://www.portadirta.com/reservar" />` (already done via Layout).
  The concern was URL params creating duplicates — Astro's canonical handles this since it uses `Astro.url.pathname` (no query string).

- [ ] **H4 — Add indexable room content to /hotel**
  Outside the Beds24 iframe, add an HTML section with:
  ```html
  <!-- ONE section per room, Google can index this -->
  <section id="torre-badum">
    <h2>Suite Torre Badum</h2>
    <p>Suite de 45m² con terraza privada y vistas al Castillo Papal de Peñíscola y al Mediterráneo.
       Cama king size, baño con ducha de lluvia, AC, WiFi, minibar. Capacidad: 2 personas.
       Precio desde 180€/noche. Desayuno no incluido.</p>
    <!-- key amenities as <ul> -->
  </section>
  ```
  **Future:** Once `BEDS24_API_TOKEN` is set in Cloudflare Pages env vars, replace with build-time SSG fetch via `src/lib/beds24.ts` to keep names/prices in sync automatically.

- [ ] **H5 — Add indexable menu text to /restaurante**
  Add an HTML `<section id="carta">` with:
  - Section headings (Entrantes, Arroces, Carnes, Postres)
  - 3–4 representative dishes per section as `<p>` or `<ul>` — no need for full menu, enough for indexing
  - Mention allergens once confirmed by brother-in-law (see cuñado pending)

- [ ] **H6 — Rewrite H1 on language placeholder pages**
  - `en/index.astro` H1: `"Porta D'irta — Boutique Hotel & Restaurant in Peñíscola, Spain"`
  - `fr/index.astro` H1: `"Porta D'irta — Hôtel Boutique & Restaurant à Peñíscola, Espagne"`
  - `de/index.astro` H1: `"Porta D'irta — Boutique-Hotel & Restaurant in Peñíscola, Spanien"`

- [ ] **H7 — Rewrite JSON-LD `description` fields for AI SEO**
  Target: 200+ characters, factual, no marketing fluff.
  Example for LodgingBusiness:
  > "Porta D'irta is a 3-room boutique hotel in Peñíscola, Castellón, Spain, situated on the Costa del Azahar next to the Parque Natural Sierra de Irta. It offers a sea-view suite (Torre Badum), a garden suite, and a panoramic room, with rates from €120/night. The property includes a full-service Mediterranean restaurant serving lunch and dinner daily."

- [ ] **H8 — Expand LodgingBusiness JSON-LD** (`src/pages/hotel.astro`)
  Add these fields:
  ```json
  "numberOfRooms": 3,
  "checkinTime": "15:00",
  "checkoutTime": "11:00",
  "amenityFeature": [
    {"@type": "LocationFeatureSpecification", "name": "WiFi gratuito", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Piscina exterior", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Restaurante", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Aparcamiento gratuito", "value": true}
  ],
  "currenciesAccepted": "EUR",
  "acceptsReservations": true,
  "hasMap": "https://maps.google.com/?q=Porta+D'irta+Peñíscola",
  "containsPlace": { "@type": "Restaurant", "name": "Porta D'irta Restaurante", "@id": "https://www.portadirta.com/restaurante" }
  ```

- [ ] **H9 — Expand Restaurant JSON-LD** (`src/pages/restaurante.astro`)
  Add:
  ```json
  "acceptsReservations": true,
  "menu": "https://www.portadirta.com/restaurante#carta",
  "servesCuisine": ["Mediterránea", "Valenciana", "De temporada"],
  "currenciesAccepted": "EUR",
  "paymentAccepted": "Cash, Credit Card",
  "isContainedInPlace": { "@type": "LodgingBusiness", "name": "Porta D'irta", "@id": "https://www.portadirta.com/hotel" },
  "priceRange": "€€"
  ```

- [ ] **H10 — Install Google Analytics 4**
  In `Layout.astro`, inside `<head>`, gated by `import.meta.env.PROD`:
  ```astro
  {import.meta.env.PROD && (
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>
  )}
  ```
  Track conversion events: form submissions (restaurant, contact, events, experiences), `tel:` link clicks, Beds24 widget interactions.

- [ ] **M6 — Improve weak page titles/descriptions**

  | Page | Current | Better |
  |------|---------|--------|
  | `/experiencias` | "Experiencias" / generic | Title: "Experiencias en Peñíscola — Kayak, Senderismo & Catas de Vino · Porta D'irta" · Desc: "Rutas guiadas por la Sierra de Irta, kayak en la Costa del Azahar, catas de vinos valencianos y visitas al Castillo Papal. Reserva tu experiencia en Peñíscola con Porta D'irta." |
  | `/reservar` | "Reservar Habitación" / thin | Title: "Reservar Habitación — Mejor Precio Garantizado · Porta D'irta Peñíscola" · Desc: "Reserva directamente tu habitación o suite en Porta D'irta, Peñíscola. Precio mínimo garantizado, confirmación inmediata. Sin intermediarios." |

#### Manual actions

- [ ] **TripAdvisor** — create hotel + restaurant listings (hoteliers.tripadvisor.com)
- [ ] **El Tenedor / TheFork** — restaurant listing (tenedor.es)
- [ ] **Booking.com** — create property listing (partner.booking.com) — takes 3–7 days
- [ ] **Expedia / Hotels.com** — expediapartnercentral.com (feeds Trivago automatically)
- [ ] **Bing Webmaster Tools** — bing.com/webmaster + submit sitemap (covers Bing + Copilot AI)
- [ ] **Bing Places** — bing.com/business (feeds Microsoft Maps + Copilot local answers)
- [ ] **Apple Maps Connect** — maps.apple.com/place-registration (critical for UK/DE iPhone users → Siri)

---

### Wave 2 — Month 1

#### Code changes

- [ ] **M1 — Self-host Google Fonts**
  - Download WOFF2 for Cormorant Garamond (300/400/600/700 + italic variants) + Inter (300/400/500)
  - Place in `/public/assets/fonts/`
  - In `Layout.astro` replace `<link href="https://fonts.googleapis.com/...">` with `@font-face` in `global.css`
  - Expected gain: +10–15 PageSpeed Mobile points (eliminates render-blocking 3rd-party DNS + download)

- [ ] **M2 — Add width/height to images missing them**
  Grep for `<img` tags without both `width=` and `height=`. Add to prevent CLS.
  At minimum: hero poster, room card images, restaurant food images.

- [ ] **M4 — Internal linking improvements**
  - `index.astro` hero section: add text link to `/experiencias` and `/eventos` in body copy
  - `experiencias.astro`: add CTA linking to `/reservar` ("¿Te quedas a dormir? Reserva tu habitación")
  - `restaurante.astro`: link to `/reservar` ("Alójate con nosotros")

- [ ] **M5 — prefers-reduced-motion for hero video**
  In `index.astro` or `global.css`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .hero-video { display: none; }
  }
  ```
  Ensure the poster `<img>` is always in the DOM (not just a video attribute) so low-motion users still see the hero.

- [ ] **L4 — Add Event JSON-LD to `/eventos`**
  For each confirmed event (Jazz, Cena Maridaje, Mercado Artesanal — pending from brother-in-law):
  ```json
  {
    "@type": "Event",
    "name": "Noche de Jazz en la Terraza",
    "startDate": "2026-07-15T20:00",
    "location": { "@type": "Place", "name": "Porta D'irta", "address": "Camí del Pebret s/n, 12598 Peñíscola" },
    "organizer": { "@type": "Organization", "name": "Porta D'irta" },
    "offers": { "@type": "Offer", "price": "35", "priceCurrency": "EUR", "url": "..." }
  }
  ```

- [ ] **L5 — Add FAQ schema to /experiencias**
  Common questions: "¿Hace falta experiencia previa para el kayak?", "¿Cuándo salen las rutas de senderismo?", "¿Están incluidas las experiencias en el precio de la habitación?" etc.

- [ ] n8n automation: post-checkout review request
  - 24h after checkout date: send email to guest with direct Google review link
  - Short redirect: `portadirta.com/opiniones` → Google review URL (easy to put on physical cards too)
  - Secondary: TripAdvisor review link

#### Manual actions

- [ ] **HolidayCheck.de** — critical for German drive market
- [ ] **Turisme Comunitat Valenciana** — turismecv.com — apply for accommodation directory (high-authority regional backlink)
- [ ] **Ayuntamiento de Peñíscola** — email turismo@peniscola.org for official tourism listing (`.peniscola.es` backlink = gold for local SEO)
- [ ] **Patronat de Turisme de la Diputació de Castelló** — castellonturisme.com
- [ ] **Guía Repsol** — guiarepsol.com (Spanish equivalent of Michelin — very high DA)
- [ ] Physical QR review cards printed for restaurant tables → `portadirta.com/opiniones` redirect
- [ ] Once first 10+ reviews arrive: add `aggregateRating` to LodgingBusiness + Restaurant JSON-LD (enables star ratings in SERPs)

---

### Wave 3 — Month 3+

#### Code changes

- [ ] Launch `/en/` multilingual routes with full translations
  - Priority order: `/en/` → `/de/` → `/fr/`
  - Use DeepL Pro for first-pass, native speaker review on all booking/pricing/cancellation copy
- [ ] Activate hreflang tags in `Layout.astro` for all 4 locales once translations exist
- [ ] Configure `@astrojs/sitemap` with i18n locale map (if not done in Wave 0)
- [ ] Set up Astro Content Collections `blog` with MDX schema
- [ ] Create `/opiniones` redirect page → Google review URL (for physical cards)

#### Content

- [ ] First blog post: "La Sierra de Irta: guía completa para senderistas en Peñíscola" → targets `senderismo Peñíscola`, `Sierra de Irta rutas`
- [ ] Second: "Los mejores arroces de la Costa del Azahar" → food tourism, cites restaurant
- [ ] Third: "Escapada romántica en Peñíscola: guía completa" → `escapada romántica Peñíscola` (high intent)

#### Manual actions

- [ ] **Create Wikidata entity** for Porta D'irta (instance of: boutique hotel, location: Peñíscola, coordinates, website, year opened) — feeds ChatGPT, Perplexity, Copilot citations
- [ ] **Parque Natural Sierra de Irta** — check if park has accommodation directory for nearby properties
- [ ] **Press trips** — pitch UK/FR/DE travel writers with destination angle ("undiscovered Mediterranean") not commercial pitch
- [ ] Spanish travel bloggers: Con Mochila y en Tren · The Foodie Studies · 101 Lugares Increíbles — offer comped stay in exchange for review article + social

---

## 3. Keyword Strategy by Page

| Page | Primary ES | Primary EN | Long-tail (high intent) |
|------|-----------|-----------|------------------------|
| `/` | hotel boutique Peñíscola | boutique hotel Peniscola | hotel con restaurante Peñíscola · villa boutique Costa del Azahar |
| `/hotel` | habitaciones Peñíscola | sea view room Peniscola | suite panorámica Peñíscola precio · suite con terraza Castellón |
| `/restaurante` | restaurante Peñíscola mediterráneo | Mediterranean restaurant Peniscola | arroz caldoso Peñíscola · restaurante terraza vistas al mar |
| `/experiencias` | actividades Peñíscola turismo | kayak Peniscola coast | senderismo Sierra de Irta guiado · cata de vinos Castellón |
| `/eventos` | eventos Peñíscola 2026 | jazz night Peniscola | cena maridaje Castellón · mercado artesanal Costa del Azahar |
| `/reservar` | reservar hotel Peñíscola | book hotel Peniscola | mejor precio Peñíscola habitación · reserva directa hotel Castellón |
| `/contacto` | contacto hotel Peñíscola | contact boutique hotel Peniscola | — |

**Rule:** "Peñíscola" must appear at least 3× naturally on every page. It is the primary local keyword.
"Costa del Azahar" is the secondary geographic keyword — use on `/`, `/hotel`, `/restaurante`.
"Castillo de Peñíscola", "Sierra de Irta" are tertiary landmark keywords — use on `/experiencias`, `/blog`.

---

## 4. AI / LLM SEO (ChatGPT · Perplexity · Copilot · Claude)

Answer engines are increasingly the first touchpoint for "best boutique hotel in Peñíscola" queries. This section is distinct from classic SEO — it's about being cited, not ranked.

### What answer engines use as sources
1. **Official website JSON-LD** — the most machine-readable signal
2. **Wikidata** — structured fact database used by all major LLMs
3. **TripAdvisor, Booking.com** — scraped at corpus-build time
4. **Travel press articles** — Guardian, Lonely Planet, etc.
5. **Reddit r/Spain, r/travel** — Perplexity scrapes heavily
6. **Google Business Profile** — Copilot uses GBP data for local answers

### Principles for AI-citeable content

- JSON-LD `description` fields must be **200+ chars of factual content** (not marketing copy). AI tools quote these verbatim. Bad: "Un refugio de ensueño con vistas al mar". Good: "Porta D'irta is a 3-room boutique hotel in Peñíscola, Castellón, Spain, with rates from €120/night, a restaurant serving Mediterranean cuisine, and direct access to the Parque Natural Sierra de Irta."
- Use `<h2>`/`<h3>` as **standalone facts or questions**: "How far is Porta D'irta from the Castillo Papal?" / "Distance from Valencia: 130km (1h 45min by car)"
- Write sentences that are **complete without context** — don't rely on page layout for meaning
- **FAQ sections** are prime AI-quotation targets — add to `/hotel` and `/experiencias`
- `@id` fields on JSON-LD entities create canonical machine-readable identity: `"@id": "https://www.portadirta.com/hotel"` — use consistently across all JSON-LD

### robots.txt AI configuration (already done ✅)
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Disallow: /
```

---

## 5. Review Strategy

### Targets
| Platform | Target | Notes |
|----------|--------|-------|
| Google | 50+ reviews, 4.7+ avg | Primary local pack ranking signal |
| TripAdvisor | 40+ reviews, 4.5+ avg | Travellers' Choice badge eligibility; primary Perplexity source |
| Booking.com | 8.5+ score | Feeds Google Hotels score |
| El Tenedor | 4.5+ | Restaurant-specific |

### Collection mechanics
- **n8n automation:** 24h post-checkout email with direct Google review link (deep-link to write form, not just GBP profile)
- **Restaurant:** Physical QR card on every table → `portadirta.com/opiniones` redirect
- **Post-experience:** Hi.Events follow-up email 3 days after event date
- **Respond to every review within 24h** — include property name + location naturally (Google indexes review responses)

### Review response formula
> "Muchas gracias, [Name]. Nos alegra que la [Suite/Habitación X] superara sus expectativas y que pudieran disfrutar de [specific experience mentioned]. Les esperamos de nuevo en Porta D'irta en su próxima visita a la Costa del Azahar."
*Contains property name + room name + location keyword — all indexed by Google.*

---

## 6. Link Building Strategy

### Tier 1 — Booking platforms (do immediately — each creates a backlink + citation)
- Booking.com · Expedia/Hotels.com · TripAdvisor · El Tenedor/TheFork · HolidayCheck.de · Trivago (auto-populated from Expedia)

### Tier 2 — Regional/governmental authority links
- Turisme Comunitat Valenciana (turismecv.com) — apply for accommodation listing
- Ayuntamiento de Peñíscola (turismo@peniscola.org) — official tourism directory
- Patronat de Turisme de la Diputació de Castelló (castellonturisme.com)
- Parque Natural Sierra de Irta — check for nearby accommodation directory
- Guía Repsol (guiarepsol.com) — highest DA food/travel site in Spain

### Tier 3 — Travel press (pitch at Month 2–3)
| Publication | Market | Angle |
|------------|--------|-------|
| The Guardian Travel | UK | "Hidden gems of the Costa del Azahar" |
| Condé Nast Traveller UK | UK | Boutique hotel feature |
| Lonely Planet | All | Spain boutique hotel guide update |
| Le Figaro Voyages | FR | Costa Azahar destination guide |
| Stern / Geo | DE | Spanish coastal travel feature |
| National Geographic España | ES | Sierra de Irta nature + accommodation |

**Pitch rule:** Never pitch the hotel directly. Pitch the **destination story** and include Porta D'irta as the recommended base.

### Tier 4 — Spanish travel bloggers (Valencia/Castellón focus)
- Con Mochila y en Tren (conmochilayentren.com) — high DA travel blog
- The Foodie Studies — food/restaurant angle
- 101 Lugares Increíbles (101lugaresincreibles.com)
- Offer: 1–2 night comped stay in exchange for review article + social post (2 links minimum: homepage + restaurant)

---

## 7. Analytics & Monitoring

| Tool | Purpose | Status |
|------|---------|--------|
| Google Search Console | Indexing, coverage, Core Web Vitals, query performance | ⬜ Not set up |
| Google Analytics 4 | Conversion tracking, traffic sources, user behaviour | ⬜ Not set up |
| Bing Webmaster Tools | Bing indexing, site scan | ⬜ Not set up |
| Google Business Profile Insights | Local search impressions, direction requests, calls | ⬜ Not set up (pending GBP creation) |
| PageSpeed Insights | Core Web Vitals per deploy | Run manually after each deploy |
| Uptime Kuma | Uptime monitoring | ✅ Running at monitor.hobbitonranch.com |

### PageSpeed targets
- Mobile Performance: **80+**
- LCP: **< 2.5s** (hero poster preload is the main lever; self-hosted fonts = biggest remaining gain)
- CLS: **< 0.1** (explicit width/height on all images — partially done)
- INP: **< 200ms** (Astro SSG has minimal JS — should be naturally excellent)

---

## 8. Multilingual Roadmap

Route structure: **subdirectory** (not subdomain) — preserves domain authority.

```
portadirta.com/          → ES (default, no prefix)
portadirta.com/en/       → EN
portadirta.com/de/       → DE
portadirta.com/fr/       → FR
```

**Priority order:** `/en/` first (UK = highest non-ES LTV, best English-speaker ROI) → `/de/` (drive market, high spend) → `/fr/` (Lyon 6h, Montpellier 4h)

**Translation workflow:**
1. DeepL Pro first-pass
2. Native speaker review on all: pricing copy, cancellation policy, booking process, legal pages
3. Hreflang tags activated only once a locale has **all main pages** translated (partial = Google confusion)

**Pages to translate per locale (minimum viable):**
`/` · `/hotel` · `/restaurante` · `/reservar` · `/contacto` — these 5 cover >90% of booking intent traffic.

---

## 9. Content Calendar — Blog (from Month 3)

| Post | Target keyword | Intent | Priority |
|------|---------------|--------|----------|
| La Sierra de Irta: guía completa para senderistas | senderismo Peñíscola · Sierra de Irta rutas | Informational / AI SEO | High |
| Los mejores arroces de la Costa del Azahar | arroz Costa del Azahar · gastronomía Castellón | Informational | High |
| Escapada romántica en Peñíscola: guía completa | escapada romántica Peñíscola | Navigational → booking | High |
| Peñíscola con niños: qué hacer en familia | Peñíscola familia · turismo familiar Castellón | Informational | Medium |
| Cata de vinos en Castellón: bodegas de la DO | cata de vinos Castellón | Informational / low competition | Medium |
| El Castillo Papal de Peñíscola: historia y visita | castillo Peñíscola · historia Peñíscola | Informational / AI SEO | Medium |
| Guía de bodas en Peñíscola: venues y celebraciones | boda Peñíscola · salón bodas Castellón | High commercial intent | Low (need event infrastructure first) |

**Content rule:** Every post must have a natural conversion path to a booking, reservation, or experience inquiry at the bottom. The goal of blog content is commercial, not purely editorial.

---

## 10. Monthly Maintenance Checklist

- [ ] Respond to all new reviews within 24h (include property name + location naturally)
- [ ] Post 1 Google Business Profile update (event, seasonal dish, photo, special offer)
- [ ] Check GSC: crawl errors, impressions, CTR underperformers
- [ ] Run PageSpeed Insights after any major deploy (target: 80+ mobile)
- [ ] Verify NAP consistency across all directories (quarterly)
- [ ] Refresh `og:image` for seasonal promotions (summer / Easter / Christmas)
- [ ] Update indexable room pricing on `/hotel` whenever Beds24 prices change
- [ ] Publish 1 blog post (from Month 3 onwards)
- [ ] Monitor "hotel boutique Peñíscola" rank weekly (Google Incognito / Ahrefs free tier)

## 2026-04-03 Technical SEO / Routing Update

- Localized restaurant table hub routes now resolve correctly:
  - `/en/mesa`
  - `/fr/mesa`
  - `/de/mesa`
- This removes avoidable 404 leakage on translated internal entry points and improves crawl consistency for localized hospitality navigation.
