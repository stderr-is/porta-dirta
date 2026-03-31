---
name: Telegram bot restart window
description: Button taps lost during n8n restart; TELEGRAM_BOT_TOKEN env var can be empty after restart
type: feedback
---

- Button taps (callback_query) sent while n8n is restarting are lost — Telegram doesn't retry them
- After `docker restart backend-n8n-1`, wait 22s before testing
- `TELEGRAM_BOT_TOKEN` env var can appear empty in Code nodes right after restart — use HTTP Request nodes to read `$env` values instead
