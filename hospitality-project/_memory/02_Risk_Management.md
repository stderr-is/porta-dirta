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
| **Planning** | PaaS memory limits exceeded by multiple Docker containers (silent crash). | Hardcode RAM limits in `docker-compose.yml`; prioritize DB over frontend apps. |
| **Planning** | Beds24 API V2 rate limits (1 call at a time) block bulk scripts. | Implement exponential backoff script to space out API calls. |
| **Planning** | TastyIgniter auto-assignment fails for odd-numbered parties. | Set strict combination rules (e.g., party of 5 always locks two 4-top tables). |
| **Execution** | Beds24 widget injects raw CSS, breaking Astro mobile view. | Isolate widget inside a Shadow DOM or iframe to strip external styling. |
| **Execution** | CORS policies block TastyIgniter widget on public Astro domain. | Strictly define CORS headers in the PaaS reverse proxy settings. |
| **Execution** | Guests ignore automated upsell email. | Embed restaurant booking link directly onto the Astro "Payment Successful" redirect page. |
| **Monitoring** | Docker container silently drops, killing restaurant bookings. | Uptime Kuma triggers immediate email/SMS alert if specific port dies. |
| **Monitoring** | Staff locked out of backend via 2FA during high network latency. | Generate and securely store static offline backup codes for admin accounts. |
| **Monitoring** | Webhooks misfire, sending 3 duplicate confirmation emails. | Implement idempotency keys in n8n to ignore duplicate payloads. |
| **Closing** | Staff revert to pen-and-paper because interface feels "too technical". | Restrict raw DB access. Provide a heavily restricted, bookmark-only calendar view. |
| **Closing** | Final DNS switch triggers a 12-hour email blackout. | Validate MX records independently before routing A records to new PaaS IP. |
| **Closing** | Beds24 API long-life token expires silently after 6 months. | Add a calendar alert for token rotation at the 5-month mark. |
