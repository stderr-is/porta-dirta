---
name: n8n Code node sandbox limitations
description: ⚠️ $helpers/fetch don't work in webhook mode (task runner sandbox) — use HTTP Request nodes instead
type: feedback
---

In n8n's task runner sandbox (webhook-triggered workflows), Code nodes cannot:
- Use `$helpers.httpRequest()`
- Use `fetch()`
- Access external URLs directly

**Fix:** Replace any HTTP calls in Code nodes with dedicated HTTP Request nodes.

**Why:** The task runner runs Code nodes in an isolated sandbox without network access helpers.
