---
name: TastyIgniter PHP proxy pattern
description: TastyIgniter PHP proxy pattern to bypass n8n body encoding bugs
type: feedback
---

When n8n's HTTP Request node can't send the correct body format for TastyIgniter, use a PHP proxy endpoint at `POST /api/internal/*` that accepts a flat JSON object and builds the correct nested structure.

Internal endpoints require header: `X-Internal-Token: ${INTERNAL_API_TOKEN}`
