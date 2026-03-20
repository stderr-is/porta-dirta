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
2. **24h wait** (guests settle before upsell hits)
3. Compose personalized email:
   - Restaurant link pre-filled: `/restaurante?fecha={checkin}&personas={adults}&nombre={name}&email={email}`
   - Hi.Events link for experiences
4. Send via SMTP — no Gemini needed, pure rule-based

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
