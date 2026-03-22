---
type: strategy
status: in-progress
tags: [seo, marketing, content, local, ai-crawlers]
---

# 🔍 SEO Master Plan — Porta D'irta

## Audit Snapshot — Existing State (2026-03-22)

### Already in place ✅
- `sitemap.xml` (10 pages, static — must be replaced with dynamic generation before multilingual)
- `robots.txt` (basic allow-all + sitemap pointer)
- Canonical URLs on every page via `Layout.astro`
- JSON-LD: `LodgingBusiness` on `/hotel`, `Restaurant` on `/restaurante`, `Event` per package on `/experiencias`
- Open Graph + Twitter Card meta on every page
- CSP + HSTS + security headers in `public/_headers`
- NAP consistent across Footer + JSON-LD: Camí del Pebret s/n · 12598 Peñíscola · +34 644 026 066
- `hero-poster.jpg` compressed: 882KB → 115KB
- `width`/`height` on in-flow images (hotel room cards, restaurant philosophy image)

### Confirmed gaps ⚠️
- `ogImage` default is `https://picsum.photos/1200/630` — every page without an explicit prop shows a random photo on social share
- `og:url` missing from `<head>` entirely — breaks Facebook/LinkedIn previews
- `og:image:width` / `og:image:height` missing — validators complain
- Room content only exists inside the Beds24 iframe — **Google cannot index any room information**
- Restaurant menu is styled HTML cards with no dish-level text — unindexable
- No `<link rel="preload">` for hero-poster.jpg (LCP element)
- Google Fonts loaded via `<link>` — render-blocking, kills mobile PageSpeed
- JSON-LD missing: `numberOfRooms`, `checkinTime`, `checkoutTime` (hotel); `menu`, `acceptsReservations` (restaurant)
- No `BreadcrumbList` JSON-LD on interior pages
- No `FAQPage` JSON-LD on `/hotel`
- No AI crawler directives in `robots.txt`
- No Google Business Profile
- No Google Search Console
- No Google Analytics 4
- No hreflang tags (needed before multilingual launch)
- Static `sitemap.xml` will go out of sync when multilingual routes are added

---

## Priority 1 — This Week

### Code changes
- [ ] Create branded `og-default.jpg` (1200×630) — property exterior + Porta D'irta wordmark
- [ ] Replace `picsum.photos` default `ogImage` in `Layout.astro` with `/assets/images/og-default.jpg`
- [ ] Add `og:url`, `og:image:width`, `og:image:height` to `Layout.astro` `<head>`
- [ ] Add `<link rel="preload" as="image">` for hero-poster.jpg (conditionally from `index.astro`)
- [ ] Add Google Site Verification meta tag slot in `Layout.astro`
- [ ] Update `robots.txt` with AI crawler rules (see section below)
- [ ] Add indexable HTML room content to `/hotel` **outside the iframe** (name, description, price, amenities per room)
  - **Future improvement (blocked on Beds24 token):** Once `BEDS24_API_KEY` is set in Cloudflare Pages env vars, replace manual HTML with a build-time SSG fetch via `src/lib/beds24.ts` in `hotel.astro` frontmatter. This keeps room names/descriptions/prices automatically in sync with the booking engine with no manual double-entry.
- [ ] Add HTML menu content to `/restaurante` (section headings + representative dishes — not a PDF)
- [ ] Expand `LodgingBusiness` JSON-LD: add `numberOfRooms: 3`, `checkinTime`, `checkoutTime`, `acceptsReservations`, `currenciesAccepted`, `hasMap`
- [ ] Expand `Restaurant` JSON-LD: add `acceptsReservations: true`, `menu` URL, `servesCuisine` array, `currenciesAccepted`
- [ ] **Dual-entity schema linking** — add `containsPlace` to `LodgingBusiness` pointing at the Restaurant entity, and `isContainedInPlace` on the Restaurant pointing back at the Hotel. Google treats these as separate local entities — this helps the restaurant rank independently in "restaurants near me" searches without being diluted by the hotel profile.
- [ ] Add `BreadcrumbList` JSON-LD to all interior pages
- [ ] Add `FAQPage` JSON-LD to `/hotel` with common guest questions
- [ ] **`prefers-reduced-motion` for video hero** — if user has this accessibility setting enabled, skip the `<video>` element entirely and display only the poster image. Implement via CSS media query on the `<video>` tag (`@media (prefers-reduced-motion: reduce) { video { display: none; } }`) combined with ensuring the poster `<img>` is always rendered in the DOM (not just as a video attribute).

### Manual actions (no code)
- [ ] **Create Google Business Profile** — business.google.com — START NOW (postcard verification takes 2 weeks)
  - Category: "Boutique Hotel" + "Restaurant" (dual)
  - Upload 25+ photos: exterior, all 3 rooms, restaurant, terrace, food, pool, sierra views
  - Set hours: hotel 24h, restaurant Tue–Sun 13–16h + 20–22h
  - Add attributes: WiFi, Piscina, Restaurante en el hotel, Admite reservas
  - Link to https://www.portadirta.com
- [ ] **Google Search Console** — verify portadirta.com, submit sitemap (needs GSC verification meta tag)
- [ ] **TripAdvisor** — create hotel + restaurant listings separately (hoteliers.tripadvisor.com)
- [ ] **Booking.com** — create property listing (partner.booking.com) — takes 3–7 days
- [ ] **El Tenedor / TheFork** — restaurant listing (tenedor.es)

---

## Priority 2 — Month 1

### Code changes
- [ ] Self-host Google Fonts (WOFF2 files in `/public/assets/fonts/`) — eliminates render-blocking 3rd-party request, +10–15 PageSpeed points on mobile
- [ ] Replace static `sitemap.xml` with `@astrojs/sitemap` integration — needed before multilingual launch
- [ ] Add Google Analytics 4 — production-only script in `Layout.astro` (gated by `import.meta.env.PROD`)
  - Track: form submissions, `tel:` link clicks, booking widget interactions, experience inquiries
- [ ] Add `aggregateRating` to `LodgingBusiness` JSON-LD once first reviews arrive (enables star ratings in SERPs)

### n8n automation
- [ ] Post-checkout review request workflow: 24h after checkout → email guest with Google review link
  - Use short redirect: `portadirta.com/opiniones` → Google review URL
  - Also request TripAdvisor review as secondary option

### Manual actions
- [ ] **Bing Webmaster Tools** — bing.com/webmaster + submit sitemap (covers Bing + Copilot AI)
- [ ] **Bing Places** — bing.com/business (feeds Microsoft Maps + Copilot local answers)
- [ ] **Apple Maps Connect** — maps.apple.com/place-registration (critical for UK/DE iPhone users → Siri)
- [ ] **HolidayCheck.de** — critical for German market
- [ ] **Expedia / Hotels.com** — expediapartnercentral.com
- [ ] **Turisme Comunitat Valenciana** — turismecv.com — apply for accommodation directory listing (high-authority regional backlink)
- [ ] **Ayuntamiento de Peñíscola** — email turismo@peniscola.org for official listing (`.peniscola.es` backlink = gold)
- [ ] **Patronat de Turisme de la Diputació de Castelló** — castellonturisme.com
- [ ] **Guía Repsol** — guiarepsol.com (Spanish equivalent of Michelin — very high authority)
- [ ] Physical QR review cards on restaurant tables → direct link to Google review form

---

## Priority 3 — Month 3

### Code changes
- [ ] Launch `/en/` multilingual routes
- [ ] Add `hreflang` tags to `Layout.astro` for es / en / fr / de + `x-default`
- [ ] Configure `@astrojs/sitemap` with i18n locale map for multilingual sitemap entries
- [ ] Set up Astro Content Collections `blog` with MDX schema

### Content
- [ ] First blog post: "La Sierra de Irta: guía completa para senderistas en Peñíscola" — targets `senderismo Peñíscola`, `Sierra de Irta rutas`
- [ ] Second post: "Los mejores arroces de la Costa del Azahar" — food tourism, cites restaurant

### Manual
- [ ] **Create Wikidata entity** for Porta D'irta (instance of: boutique hotel, location: Peñíscola, coordinates, website) — feeds ChatGPT, Perplexity, Copilot citations
- [ ] **Press trips** — pitch UK/FR/DE travel writers with destination angle ("undiscovered Mediterranean") not commercial pitch
- [ ] **Spanish travel bloggers** — approach 3 bloggers covering Valencia/Castellón for comped stays
- [ ] **Parque Natural Sierra de Irta** — check if park has accommodation directory near its boundaries
- [ ] **Gastroranking** — gastroranking.com (restaurant)

---

## Keyword Strategy by Page

| Page | Primary (ES) | Primary (EN) | Long-tail |
|---|---|---|---|
| `/` | hotel boutique Peñíscola | boutique hotel Peniscola | hotel con restaurante Peñíscola |
| `/hotel` | habitaciones Peñíscola | sea view suite Peniscola | suite panorámica Peñíscola precio |
| `/restaurante` | restaurante Peñíscola mediterráneo | Mediterranean restaurant Peniscola | arroz caldoso Peñíscola · restaurante terraza |
| `/experiencias` | actividades Peñíscola turismo | kayak Peniscola coast | senderismo Sierra de Irta guiado |
| `/eventos` | eventos Peñíscola 2026 | jazz night Peniscola | cena maridaje Castellón |
| `/contacto` | contacto hotel Peñíscola | contact boutique hotel Peniscola | — |

**Rule:** "Peñíscola" must appear at least 3× naturally on every page. It is the primary local keyword.

---

## AI / LLM SEO (ChatGPT · Perplexity · Copilot · Claude)

Answer engines are increasingly the first touchpoint for "best boutique hotel in Peñíscola" queries.

### robots.txt AI crawler rules
```
# Answer engines — ALLOW (these cite your site in responses)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# Training scrapers — BLOCK (no referral value)
User-agent: CCBot
Disallow: /

User-agent: omgili
Disallow: /

# SEO tools — rate limit (prevent server load)
User-agent: AhrefsBot
Crawl-delay: 10

User-agent: SemrushBot
Crawl-delay: 10
```

### LLM content principles
- JSON-LD `description` fields must be 200+ chars of factual content (not marketing copy) — AI tools quote these verbatim
- Write sentences that are complete without context: "Porta D'irta is a 3-room boutique hotel in Peñíscola, on the Costa del Azahar (Castellón, Spain), with rooms from €120/night"
- Use `<h2>`/`<h3>` as standalone questions or facts: "How far is Porta D'irta from Peñíscola castle?"
- TripAdvisor reviews + Reddit r/Spain threads are primary Perplexity sources — genuine guest reviews on both platforms
- Wikidata entry = machine-readable anchor for all major AI tools

---

## Review Strategy

| Platform | Target | Notes |
|---|---|---|
| Google | 50+ reviews, 4.7+ avg | Primary local pack ranking signal |
| TripAdvisor | 40+ reviews, 4.5+ avg | Travellers' Choice badge eligibility |
| Booking.com | 8.5+ score | Feeds Google Hotels score |
| El Tenedor | 4.5+ | Restaurant-specific |

### Mechanics
- **n8n automation:** 24h post-checkout email with Google review link (direct write-a-review URL, not just GBP profile)
- **Restaurant tables:** Physical QR card → review link
- **Post-experience:** Hi.Events follow-up 3 days after event date
- **Respond to every review within 24h** — include property name + location naturally (Google indexes review responses)

### Response formula
> "Muchas gracias, [Name]. Nos alegra que la [Room Name] superara sus expectativas y que pudieran disfrutar de [specific experience]. Les esperamos en Porta D'irta en su próxima visita a la Costa del Azahar."

Contains 3 keyword-rich phrases, the room name, and the location — all indexed.

---

## Link Building Strategy

### Tier 1 — Booking platforms (do immediately — each creates a backlink)
- Booking.com · Expedia/Hotels.com · TripAdvisor · El Tenedor/TheFork · HolidayCheck.de · Trivago (auto-populated)

### Tier 2 — Regional/governmental authority links
- Turisme Comunitat Valenciana (turismecv.com)
- Ayuntamiento de Peñíscola (turismo@peniscola.org)
- Patronat de Turisme de la Diputació de Castelló (castellonturisme.com)
- Parque Natural Sierra de Irta (if accommodation directory exists)
- Guía Repsol (guiarepsol.com)

### Tier 3 — Travel press (pitch at month 2–3)
| Publication | Market | Angle |
|---|---|---|
| The Guardian Travel | UK | "Hidden gems of the Costa del Azahar" |
| Condé Nast Traveller UK | UK | Boutique hotel feature |
| Lonely Planet | All | Spain boutique hotel guide |
| Le Figaro Voyages | FR | Costa Azahar destination guide |
| Stern / Geo | DE | Spanish coastal travel feature |
| National Geographic España | ES | Sierra de Irta nature angle |

**Pitch rule:** Never pitch the hotel directly. Pitch the destination story and include Porta D'irta as the recommended place to stay.

### Tier 4 — Spanish travel bloggers (Valencia/Castellón focus)
- Con mochila y en tren (conmochilayentren.com)
- The Foodie Studies (restaurant angle)
- 101 Lugares Increíbles (101lugaresincreibles.com)
- Offer: 1–2 night comped stay in exchange for review article + social post

---

## Analytics & Monitoring

| Tool | Purpose | Status |
|---|---|---|
| Google Search Console | Indexing, coverage, Core Web Vitals, query performance | ⬜ Not set up |
| Google Analytics 4 | Conversion tracking, traffic sources, user behaviour | ⬜ Not set up |
| Bing Webmaster Tools | Bing indexing, site scan | ⬜ Not set up |
| Google Business Profile Insights | Local search impressions, direction requests, calls | ⬜ Not set up |
| PageSpeed Insights | Core Web Vitals per deploy | Manual (run after each deploy) |
| Uptime Kuma | Uptime monitoring | ✅ Running at monitor.hobbitonranch.com |

### PageSpeed targets
- Mobile Performance: 80+
- LCP: < 2.5s (hero poster preload is the main lever)
- CLS: < 0.1 (explicit width/height on all images — partially done)
- INP: < 200ms (Astro SSG has minimal JS — should be naturally excellent)

---

## Content Calendar — Blog (from Month 3)

| Post | Target keyword | Market | Priority |
|---|---|---|---|
| La Sierra de Irta: guía completa para senderistas | senderismo Peñíscola · Sierra de Irta rutas | ES | High |
| Los mejores arroces de la Costa del Azahar | arroz Costa del Azahar · gastronomía Castellón | ES | High |
| Escapada romántica en Peñíscola: guía completa | escapada romántica Peñíscola | ES | High (high competition) |
| Peñíscola con niños: qué hacer en familia | Peñíscola familia · turismo familiar Castellón | ES | Medium |
| Cata de vinos en Castellón: bodegas de la DO | cata de vinos Castellón | ES | Low competition |
| El Castillo Papal de Peñíscola: historia y visita | castillo Peñíscola visita · historia Peñíscola | ES | Informational / AI SEO |

---

## Multilingual Roadmap

Route structure (subdirectory, not subdomain — preserves domain authority):
- `portadirta.com/` — ES default
- `portadirta.com/en/` — EN (British market first — highest non-ES LTV)
- `portadirta.com/de/` — DE (high LTV, drive-market)
- `portadirta.com/fr/` — FR (drive-market: Lyon 6h, Montpellier 4h)

Translation priority: `/en/hotel` + `/en/` first → then `/de/` → then `/fr/`

Use DeepL Pro for first-pass translation, then native speaker review on all booking/pricing/cancellation copy.

---

## Ongoing Monthly Checklist

- [ ] Respond to all new reviews within 24h
- [ ] Post 1 Google Business Profile update (event, seasonal menu, photo)
- [ ] Check GSC: crawl errors, impressions, CTR underperformers
- [ ] Run PageSpeed Insights after any major deploy
- [ ] Publish 1 blog post
- [ ] Monitor "hotel boutique Peñíscola" rankings (Ahrefs / Semrush free tier)
- [ ] Verify NAP consistency across all directories (quarterly)
- [ ] Refresh og:image for seasonal promotions (summer / Easter / Christmas)
- [ ] Update room pricing on HTML `/hotel` page whenever Beds24 prices change
