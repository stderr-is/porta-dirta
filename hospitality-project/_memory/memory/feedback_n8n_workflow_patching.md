---
name: n8n workflow patching — DB patches rules
description: Critical rules for patching n8n workflows in PostgreSQL — versionId/activeVersionId, FK order, webhook_entity, SMTP data loss after HTTP nodes
type: feedback
---

## Rule 1: Always update BOTH `versionId` AND `activeVersionId`

n8n v2 has two version fields in `workflow_entity`. If `activeVersionId` is NULL or doesn't match `versionId`, n8n **silently skips the workflow on startup** — webhook not registered, IMAP not polling.

**Every patch SQL must include:**
```sql
INSERT INTO workflow_history ("versionId","workflowId","nodes","connections","authors","createdAt","updatedAt")
VALUES ('<new-uuid>', 'av9R2wseN47PQZ8S', '<nodes>', '<conns>', 'Ricardo Leite', NOW(), NOW());

UPDATE workflow_entity
SET nodes='<nodes>', connections='<conns>',
    "versionId"='<new-uuid>',
    "activeVersionId"='<new-uuid>',
    "updatedAt"=NOW()
WHERE id='av9R2wseN47PQZ8S';
```

Quick fix if diverged: `UPDATE workflow_entity SET "activeVersionId"="versionId" WHERE id='av9R2wseN47PQZ8S';`

## Rule 2: INSERT workflow_history BEFORE UPDATE workflow_entity

FK constraint: `workflow_entity.activeVersionId → workflow_history.versionId`. INSERT first or you get FK violation.

## Rule 3: After restart, manually insert webhook_entity if Telegram rate-limits

```sql
INSERT INTO webhook_entity ("webhookPath",method,node,"webhookId","pathLength","workflowId")
VALUES ('475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook','POST','Telegram Trigger',
        '475cd6ce-bb05-46ee-aea8-663b6e9d8433',2,'av9R2wseN47PQZ8S')
ON CONFLICT DO NOTHING;
```

## Rule 4: After HTTP Request nodes, $json loses upstream data

Reference upstream nodes by name: `$('Email Callback Handler').first().json.body`

## Rule 5: Always restart n8n after DB patch + re-register webhook

```bash
docker restart backend-n8n-1
sleep 22
BOT="8348668157:AAEMAD_F37GNJJZxOd4C5krZg4OnPaZ_MD4"
curl -s -X POST "https://api.telegram.org/bot${BOT}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://n8n.portadirta.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook","allowed_updates":["message","callback_query"]}'
```
