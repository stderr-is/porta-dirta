---
type: architecture
status: active
tags: [ai, n8n, gemini, telegram, automation]
---

# 🤖 AI Automation & Orchestration Blueprint — Porta D'irta

## Architecture Overview

```
Beds24 webhook / Email IMAP / Telegram voice+text / Cron
        ↓
  n8n (Orchestrator) ← all logic lives here
        ↓
  [Identity Router] → drop unauthorized immediately (zero Gemini cost)
        ↓
  Gemini 1.5 Flash (HTTP) ← reasoning + JSON generation + audio transcription
        ↓
  [Schema Validator] ← never execute raw LLM output against an API
        ↓
  [Confirmation gate] ← human-in-the-loop for all destructive actions
        ↓
  Beds24 API / TastyIgniter API / Hi.Events API / SMTP / Telegram
        ↓
  [Audit Log] ← every AI-triggered mutation is recorded
```

## Core Components

| Component | Tool | Purpose |
|---|---|---|
| Orchestrator | n8n (self-hosted, already running at n8n.hobbitonranch.com) | Webhooks, routing, scheduling, API calls |
| LLM Brain | Anthropic Claude Haiku 4.5 | Language detection, intent parsing, JSON generation (switched from Gemini — free tier quota issues) |
| Primary Interface | Telegram Bot API | Mobile-first command center for admin + collaborators |
| Secondary Interface | IMAP/SMTP in n8n | Guest email inbox monitoring and auto-draft replies |

## Security: Telegram Identity Router

**First node in every Telegram workflow is the Identity Router. No Gemini call is made before it passes.**

| Tier | Persona | Access | n8n Env Var |
|---|---|---|---|
| Master Admin | Ricardo | Full R/W: Beds24 pricing, room blocks, restaurant, all queries | `TELEGRAM_ADMIN_ID` |
| Collaborator | Restaurant partner | Read-only: table availability, ticket counts. Router blocks all write endpoints. | `TELEGRAM_COLLAB_ID` |
| Unauthorized | Anyone else | Payload dropped. Zero cost. No Gemini call. | — |

**User IDs are stored as n8n environment variables, never hardcoded in workflow JSON.**

## n8n Environment Variables (add to docker-compose.yml)

```yaml
- ANTHROPIC_API_KEY=your_anthropic_api_key   # replaces GEMINI_API_KEY
- TELEGRAM_BOT_TOKEN=your_bot_token
- TELEGRAM_ADMIN_ID=your_telegram_numeric_id
- TELEGRAM_COLLAB_ID=collaborator_telegram_numeric_id
- BEDS24_API_TOKEN=your_beds24_v2_long_lived_token
- BEDS24_PROP_ID=318433
```

---

## Workflow A: Silent Concierge

**Files:** `workflow-a-silent-concierge.json` + `workflow-a2-callback-handler.json`

### Flow
1. IMAP polls `info@portadirta.com` every 60s for new messages
2. Code node extracts sender, subject, body; generates `messageKey` from `Message-ID` header for idempotency (duplicate emails are skipped)
3. HTTP → Gemini with Silent Concierge system prompt
4. Gemini returns: `{ language, intent, draftSubject, draftBody }`
5. Draft stored in workflow static data keyed by `messageKey` (TTL: 24h)
6. Telegram sends Ricardo a formatted preview with inline buttons:
   - `[✅ Approve & Send]` → callback_data: `approve_{messageKey}`
   - `[✏️ Edit]` → callback_data: `edit_{messageKey}`

### Approve flow (Workflow A2)
- Load draft from static data → send via SMTP → Telegram "✅ Sent to {email}"
- Mark `messageKey` as processed to prevent duplicate sends

### Edit flow (Workflow A2)
- Send Telegram message with `force_reply: true` containing the original draft
- Store `{messageKey, forceReplyMsgId}` in static data
- When Ricardo replies (detected by `reply_to_message.message_id` match) → update draft body → re-present with `[✅ Approve & Send]`

### Regenerate flow (Workflow A2)
- `[🔄 Regenerate]` button added alongside `[✅ Approve & Send]` and `[✏️ Edit]`
- callback_data: `regenerate_{messageKey}`
- Re-calls Claude with the same input but `temperature: 0.9` (vs. 0.3 default) for a varied tone
- Overwrites the stored draft, re-presents the three buttons
- Use case: first draft is too formal, too short, or missed the guest's tone

### Idempotency
- `messageKey` derived from email `Message-ID` header (base64, first 20 chars)
- Processed keys stored in static data with timestamp; ignored on re-trigger

---

## Workflow B: Mobile Command Center

**File:** `workflow-b-command-center.json`

### Flow
1. Telegram Trigger: `message` + `callback_query` updates
2. **Identity Router** (Switch node on `from.id`):
   - Admin → full branch
   - Collaborator → read-only branch (same flow, restricted action allowlist)
   - Unknown → immediate stop, no response
3. **Voice detection:** `message.voice` exists → download OGG URL → send as base64 to Gemini multimodal (Gemini 1.5 Flash transcribes + interprets in one API call — no separate STT service needed)
4. Text path → send directly to Gemini with Command Center system prompt
5. Gemini returns strict JSON: `{ action, endpoint, method, payload, isDestructive, confirmationMessage, humanReadableSummary }`
6. **Schema Validator** Code node:
   - Action is in allowed list for user's tier
   - Required payload fields present and correct type
   - Numeric values within safe bounds
   - Dates in YYYY-MM-DD format
   - On failure → Telegram error message, stop
7. **Destructive gate:** `isDestructive === true` → Telegram sends `confirmationMessage` with `[✅ Confirm]` / `[❌ Cancel]` → wait for callback before executing
8. **API Executor** HTTP node calls Beds24 / TastyIgniter / Hi.Events
9. **Audit Log** Code node records entry
10. Telegram sends `humanReadableSummary` back to user
11. **API Executor error branch:** if HTTP node fails (Beds24 down, 401 expired token, 5xx) →
    - Immediate high-priority Telegram alert to Admin: "🔴 API ERROR: {endpoint} failed — {status}. Check Beds24 token or service status."
    - Write to Audit Log with `result: "error"`
    - Do NOT silently fail — booking-path failures are critical

### Destructive actions (require confirmation)
- Beds24: block room, update price, cancel booking
- TastyIgniter: delete reservation
- Hi.Events: cancel event

### Read-only actions (execute immediately)
- Beds24: get occupancy, list bookings, get revenue
- TastyIgniter: check table availability, list reservations
- Hi.Events: get ticket counts

---

## Workflow C: Yield Management & Cross-Selling

**File:** `workflow-c-yield-management.json`

### C1 — Cross-sell (Beds24 booking confirmed webhook)
1. Beds24 webhook → extract guest name, email, check-in date, adult count
2. **Last-minute logic** (IF node on time delta):
   - Check-in < 48h away → **1h wait** (guest is in active planning mode right now)
   - Check-in ≥ 48h away → **24h wait** (standard — guest settles before upsell hits)
3. Compose personalized email:
   - Restaurant link pre-filled: `/restaurante?fecha={checkin}&personas={adults}&nombre={name}&email={email}`
   - Hi.Events link for experiences
4. Send via SMTP — no Claude needed, pure rule-based

### C3 — Flash Sale Anomaly Detector (daily cron 16:00)
1. Beds24 API → check occupancy for **tonight** only
2. IF any room is still unbooked → calculate flash sale price (floor price from `pricing-rules.json`)
3. Telegram to Ricardo:
   > "🚨 *Suite Panorámica* sigue vacía esta noche. Precio flash sugerido: **€200**. ¿Aplicar?"
   > `[💰 Aplicar precio flash]` `[🙈 Ignorar]`
4. `[Aplicar]` callback → Beds24 price update → confirmation sent
5. No action needed if all rooms are booked (workflow exits silently)

### C2 — Yield analysis (daily cron 02:00)
1. Beds24 API → forward occupancy for next 30 days
2. Code node loads `pricing-rules.json`, computes rule-recommended price per date
3. Build list of dates where current price ≠ recommended price
4. If adjustments exist → Gemini generates natural-language summary of recommendations
5. **Schema validator** checks prices are numeric, within floor/ceiling bounds
6. Telegram to Ricardo: "📊 5 price adjustments for next 2 weeks — [Review & Apply] [Dismiss]"
7. `[Review & Apply]` callback → execute Beds24 price updates sequentially with exponential backoff
8. Audit log written, Telegram confirmation sent

---

## Pricing Rules (backend/n8n-workflows/pricing-rules.json)

```json
{
  "basePrice": { "habitacion-mediterranea": 120, "suite-junior": 180, "suite-panoramica": 250 },
  "floor":     { "habitacion-mediterranea": 90,  "suite-junior": 140, "suite-panoramica": 200 },
  "ceiling":   { "habitacion-mediterranea": 200, "suite-junior": 300, "suite-panoramica": 420 },
  "tiers": [
    { "occupancyMin": 0,  "occupancyMax": 50, "multiplier": 1.0,  "minStayNights": 1 },
    { "occupancyMin": 51, "occupancyMax": 70, "multiplier": 1.10, "minStayNights": 1 },
    { "occupancyMin": 71, "occupancyMax": 85, "multiplier": 1.25, "minStayNights": 2 },
    { "occupancyMin": 86, "occupancyMax": 100,"multiplier": 1.40, "minStayNights": 2 }
  ]
}
```

---

## Claude API Call Pattern (n8n HTTP Request node)

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  anthropic-version: 2023-06-01
  content-type: application/json

Body:
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 512,
  "messages": [{ "role": "user", "content": "{systemPrompt}\n\nINPUT:\n{userInput}" }]
}
```

Response text extracted in Code node: `geminiRaw.content?.[0]?.text || '{}'`
Models used: `claude-haiku-4-5-20251001` for all workflows. Email concierge uses `max_tokens: 2048`.
Voice transcription not supported — voice messages get a "please use text" Telegram reply.

## Beds24 Rate Limit Mitigation

Beds24 API V2 allows only 1 concurrent request per token. If multiple n8n workflows trigger simultaneously (e.g. booking webhook + yield cron), 429 errors occur.

**Mitigation (simple approach — no global queue needed):**
- Add a **2-second Wait node** at the start of every workflow that calls Beds24
- Exponential backoff already exists in `beds24.ts` for the frontend side
- Workflow C (yield cron) runs at 02:00 — low collision risk with webhooks
- If 429 is received in any n8n HTTP node → retry after 5s, max 3 retries → if still failing, send Telegram alert (same error branch as above)

**Note:** n8n does not have a native global queue. A full queue implementation would require Redis + n8n Queue Mode — not justified at current scale (3 rooms). Revisit if volume increases significantly.

---

## Audit Log Format

Every AI-triggered API mutation is appended to n8n workflow static data:
```json
{
  "ts": "2026-07-15T14:23:00Z",
  "user": "admin",
  "action": "beds24.updatePrice",
  "payload": { "roomId": "2", "date": "2026-07-20", "price": 185 },
  "result": "success | error",
  "n8nExecutionId": "12345"
}
```

## Workflow Files

| File | Import into n8n | Status |
|---|---|---|
| `workflow-a-silent-concierge.json` | Settings → Import workflow | Ready to import |
| `workflow-a2-callback-handler.json` | Settings → Import workflow | Ready to import |
| `workflow-b-command-center.json` | Settings → Import workflow | Ready to import |
| `workflow-c-yield-management.json` | Settings → Import workflow | Ready to import |

**After import:** Update credential IDs for Telegram Bot, IMAP, and SMTP credentials in each workflow node.

## 2026-04-03 Operational Update (Workflow B)

- Workflow B menu command path was hardened for production:
  - stronger JSON-shape enforcement and parse diagnostics in menu extraction path,
  - safer Telegram error messaging path (avoids formatting/entity failures),
  - doc-ID fallback compatibility for `/taperia` route selection.
- Production deployment pattern used repeatedly and confirmed:
  1. insert new `workflow_history` row,
  2. set `workflow_entity.versionId` and `workflow_entity.activeVersionId` to same new UUID,
  3. restart n8n,
  4. re-register Telegram webhook.
