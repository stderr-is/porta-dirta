# Claude Memory Index — Porta D'irta Project

## Feedback / How-To
- [feedback_n8n_http_body.md](feedback_n8n_http_body.md) — How to correctly send a JSON body from an n8n HTTP Request node v4 (the `jsonBody` fix)
- [feedback_n8n_tastyigniter_proxy.md](feedback_n8n_tastyigniter_proxy.md) — TastyIgniter PHP proxy pattern to bypass n8n body encoding bugs
- [feedback_n8n_task_runner.md](feedback_n8n_task_runner.md) — ⚠️ Code nodes: `$helpers`/`fetch` don't work in webhook mode (task runner sandbox) — use HTTP Request nodes instead
- [feedback_n8n_workflow_patching.md](feedback_n8n_workflow_patching.md) — DB patches get overwritten by UI Publish — always reload via API deactivate/activate cycle
- [feedback_n8n_imap_fields.md](feedback_n8n_imap_fields.md) — ⚠️ IMAP trigger uses `textPlain`/`textHtml`/`metadata` NOT `text`/`html`/`headers` — wrong names = silent empty body
- [feedback_telegram_restart_window.md](feedback_telegram_restart_window.md) — Button taps lost during n8n restart window; TELEGRAM_BOT_TOKEN env var can be empty after restart

## Credentials & Tokens
- [reference_credentials.md](reference_credentials.md) — ⭐ MASTER credentials file: all logins, passwords, tokens, ports for every service
- [reference_beds24_tokens.md](reference_beds24_tokens.md) — Beds24 API V2 refresh token, room IDs, and how to get an access token

## Project Context
- [project_portadirta.md](project_portadirta.md) — High-level project overview and working directory
- [project_cunyado_pending_info.md](project_cunyado_pending_info.md) — ⚠️ CRITICAL: Missing info from brother-in-law blocking go-live (legal placeholders, eventos content, email addresses, social handles)
