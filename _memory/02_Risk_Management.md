---
type: risk-assessment
status: active
tags: [black-swan, mitigation, security]
---

# 🦢 "Black Swan" Failures & Mitigations

| Phase | Identified Risk | The "Plan B" Mitigation |
| :--- | :--- | :--- |
| **Initiation** | Booking.com rejects Beds24 connection due to extranet conflicts. | Initiate mapping 14 days early. Use Beds24 iCal sync as fallback; monitor local capacity heavily. |
| **Initiation** | Domain propagation locks PaaS SSL cert, leaving site insecure. | Pre-verify domain TXT records and use a temporary Cloudflare tunnel. |
| **Initiation** | Stripe flags account as "high risk" due to event ticketing. | Have PayPal Business or Square pre-approved as a secondary gateway. |
| **Planning** | ~~PaaS memory limits exceeded by multiple Docker containers (silent crash).~~ | ✅ **MITIGATED (2026-03-20):** `mem_limit` + `mem_reservation` set on all 7 services in `docker-compose.yml`. restaurant 512m, events 1g (all-in-one), DBs 256–512m, n8n 512m, kuma 256m. |
| **Planning** | ~~Beds24 API V2 rate limits (1 call at a time) block bulk scripts.~~ | ✅ **MITIGATED (2026-03-20):** Exponential backoff implemented in `apiFetch` in `frontend/src/lib/beds24.ts`. 429 → retry up to 5×, 500ms→1s→2s→4s→8s, max 30s cap. |
| **Planning** | TastyIgniter auto-assignment fails for odd-numbered parties. | Set strict combination rules (e.g., party of 5 always locks two 4-top tables). |
| **Execution** | ~~Beds24 widget injects raw CSS, breaking Astro mobile view.~~ | ✅ **MITIGATED (2026-03-20):** Both widget wrapper divs in `hotel.astro` now have `contain: layout style; isolation: isolate` — prevents injected styles from escaping the widget boundary. |
| **Execution** | ~~CORS policies block TastyIgniter widget on public Astro domain.~~ | ✅ **MITIGATED (2026-03-20):** CORS headers added to TastyIgniter Apache config (via `cors.conf` + `a2enmod headers` in Dockerfile) and Hi.Events nginx `/api/` location block. Allows `porta-dirta.hobbitonranch.com` + `portadirta.com`. |
| **Execution** | Guests ignore automated upsell email. | Embed restaurant booking link directly onto the Astro "Payment Successful" redirect page. |
| **Monitoring** | Docker container silently drops, killing restaurant bookings. | Uptime Kuma triggers immediate email/SMS alert if specific port dies. |
| **Monitoring** | Staff locked out of backend via 2FA during high network latency. | Generate and securely store static offline backup codes for admin accounts. |
| **Monitoring** | Webhooks misfire, sending 3 duplicate confirmation emails. | Implement idempotency keys in n8n to ignore duplicate payloads. |
| **Closing** | Staff revert to pen-and-paper because interface feels "too technical". | Restrict raw DB access. Provide a heavily restricted, bookmark-only calendar view. |
| **Closing** | Final DNS switch triggers a 12-hour email blackout. | Validate MX records independently before routing A records to new PaaS IP. |
| **Closing** | Beds24 API long-life token expires silently after 6 months. | Add a calendar alert for token rotation at the 5-month mark. |
| **AI Layer** | Gemini returns malformed JSON, n8n executes partial API payload corrupting Beds24 data. | Schema Validator Code node runs before every API call. Invalid JSON → Telegram alert, workflow stops. Never pass raw LLM output to an API. |
| **AI Layer** | Admin clicks `[Approve & Send]` twice, guest receives duplicate email. | `messageKey` idempotency: processed keys stored in n8n static data. Second Approve on same key is a no-op. |
| **AI Layer** | Runaway n8n workflow loop hammers Gemini API, unexpected cost spike. | Set Gemini API budget alert at $5/month. Workflow execution limits in n8n settings. |
| **AI Layer** | Unauthorized Telegram user reverse-engineers bot token and sends commands. | Identity Router drops all unknown `from.id` values before any processing. Bot token stored as n8n env var, never in workflow JSON. Set bot privacy mode via @BotFather (disable group adds). |
| **AI Layer** | Yield management autonomously sets price below break-even. | Hard floor prices in `pricing-rules.json`. Schema validator rejects any recommended price below floor. Human approval required before any Beds24 price write. |
| **AI Layer** | Voice note misheard by Gemini, executes wrong destructive action. | All destructive actions (room block, price change, cancel) require explicit `[✅ Confirm]` in Telegram before API call. Read-only actions execute immediately. |
