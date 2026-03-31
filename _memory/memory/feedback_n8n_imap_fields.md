---
name: n8n IMAP trigger field names
description: ⚠️ IMAP trigger uses textPlain/textHtml/metadata NOT text/html/headers — wrong names = silent empty body
type: feedback
---

IMAP Email Trigger node outputs:
- `$json.textPlain` — plain text body (NOT `$json.text`)
- `$json.textHtml` — HTML body (NOT `$json.html`)
- `$json.metadata.subject` — subject (NOT `$json.headers.subject`)
- `$json.metadata.from` — sender

**Why:** n8n's IMAP node uses a different output schema than you'd expect. Using the wrong field names silently returns empty strings — no error thrown.
