# 08 — n8n Troubleshooting & Hard-Won Lessons

## ⚠️ READ THIS BEFORE TOUCHING ANY n8n WORKFLOW

---

## 1. Task Runner: `$helpers` and `fetch` DON'T WORK in webhook mode

### The problem
n8n 2.x runs Code nodes in a separate sandboxed process called the **task runner**.
- **Manual execution** (clicking "Execute Workflow" in UI): Code nodes run inline in the main process → `$helpers`, `fetch`, `require('node-fetch')` ALL work.
- **Webhook/production execution** (real Telegram message, activated workflow): Code nodes run in the task runner sandbox → `$helpers` and `fetch` are **NOT defined**.

This means a Code node that works perfectly in manual test will **silently fail** in production.

### The fix
**Never use `$helpers.httpRequest()` or `fetch()` in Code nodes that need to work in production.**

If a Code node needs to make an HTTP call (e.g. send a Telegram message), convert it to an **HTTP Request node** instead. HTTP Request nodes run in the main process and have no sandbox restrictions.

Available in Code nodes in both modes:
- `$json`, `$input`, `$env`, `items`
- `$('NodeName').first().json` — referencing other nodes
- `$getWorkflowStaticData('global')` — persistent storage
- Standard JS (no network calls, no require)

### Specific nodes affected (Workflow B — Command Center)
The following nodes were originally Code type and caused `$helpers is not defined` in production. They were converted to HTTP Request nodes (2026-03-24):
- `Telegram — Menu Updated` → httpRequest
- `Telegram — Menu Error` → httpRequest
- `Telegram — Fetch Error` → httpRequest
- `Telegram — Claude Error` → httpRequest
- `Telegram — Proxy Error` → httpRequest
- `Telegram — Route Error` → httpRequest

---

## 2. "Publish" in the n8n UI overwrites DB patches

### The problem
When Claude patches a workflow by writing directly to the PostgreSQL `workflow_entity` table, those patches are **lost** the next time someone clicks "Save" or "Publish" in the n8n UI. The UI saves its cached (old) state back to the DB.

### The fix
After patching the DB, use the n8n API `PUT` endpoint to flush n8n's internal runtime state. **`deactivate/activate` alone is NOT enough** — it only toggles the active flag and re-registers webhooks, it does NOT reload the workflow code from the DB.

```bash
# Step 1: fetch (reads from DB — has your patch)
curl -s "http://localhost:5678/api/v1/workflows/WORKFLOW_ID" \
  -H "X-N8N-API-KEY: n8n_api_activation_key_portadirta_2026" > /tmp/wf.json

# Step 2: PUT back (flushes n8n's internal state)
# IMPORTANT: settings must only contain 'executionOrder' — other keys cause 400 error
python3 -c "
import json
with open('/tmp/wf.json') as f: wf = json.load(f)
body = {'name': wf['name'], 'nodes': wf['nodes'], 'connections': wf['connections'],
        'settings': {'executionOrder': wf['settings'].get('executionOrder','v1')},
        'staticData': wf.get('staticData')}
print(json.dumps(body))
" | curl -s -X PUT "http://localhost:5678/api/v1/workflows/WORKFLOW_ID" \
  -H "X-N8N-API-KEY: n8n_api_activation_key_portadirta_2026" \
  -H "Content-Type: application/json" -d @-

# Step 3: re-activate (PUT deactivates it)
curl -s -X POST "http://localhost:5678/api/v1/workflows/WORKFLOW_ID/activate" \
  -H "X-N8N-API-KEY: n8n_api_activation_key_portadirta_2026"
```

The API key `n8n_api_activation_key_portadirta_2026` is stored in the `user_api_keys` table.

### Consequences
- Never tell the user to "click Publish" after a DB patch
- `deactivate/activate` is insufficient — must use `PUT` to actually flush runtime state
- If the user clicks Publish, patches disappear — re-apply the patch and use PUT to reload

---

## 3. Telegram webhook clears on n8n restart

### The problem
After `docker compose restart n8n`, the Telegram webhook URL is unregistered. Messages sent to the bot are not forwarded to n8n. Executions show `mode: webhook` but never fire.

The `Identity Router` node has a self-heal mechanism that re-registers the webhook — but it uses `$helpers.httpRequest` which **doesn't work in webhook mode** (see issue #1). It's a catch-22: the self-heal only runs when a message is received, but messages aren't received because the webhook isn't registered.

### The fix
After any n8n restart, re-register the webhook manually:

```bash
BOT=$(docker exec backend-n8n-1 sh -c 'echo $TELEGRAM_BOT_TOKEN')
curl -s "https://api.telegram.org/bot${BOT}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://n8n.hobbitonranch.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook","allowed_updates":["message","callback_query"]}'
```

Also ensure n8n's webhook routing table is populated:
```sql
INSERT INTO webhook_entity ("webhookPath", method, node, "webhookId", "pathLength", "workflowId")
VALUES ('475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook','POST','Telegram Trigger',
        '475cd6ce-bb05-46ee-aea8-663b6e9d8433',1,'av9R2wseN47PQZ8S')
ON CONFLICT DO NOTHING;
```

Verify with:
```bash
curl -s "https://api.telegram.org/bot${BOT}/getWebhookInfo" | python3 -m json.tool
```

---

## 4. n8n workflow activation: DB flag alone is not enough

### The problem
Setting `active=true` in `workflow_entity` via SQL does NOT make n8n start processing webhooks for that workflow. n8n has an in-memory registry of active workflows that is separate from the DB.

### The fix
Always activate via the n8n API (see issue #2 above). The API call properly registers the workflow in n8n's runtime AND registers the Telegram webhook in one step.

---

## 5. Docker volume permissions: named volumes initialize as root

### The problem
When `docker compose up` creates a named volume and mounts it into a container for the first time, the mount point directory is owned by `root:root`. PHP (running as `www-data`) cannot write to it → 500 errors from the menu proxy.

### The fix
Add a custom Docker entrypoint to the TastyIgniter container that runs `chown` before starting Apache:

`backend/tastyigniter/docker-entrypoint.sh`:
```sh
#!/bin/sh
mkdir -p /var/www/data
chown www-data:www-data /var/www/data
exec /usr/local/bin/docker-php-entrypoint apache2-foreground
```

`Dockerfile`:
```dockerfile
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
```

**Important**: do NOT use `ENTRYPOINT [..., "$@"]` with no CMD — the container will exit with code 0. Must explicitly pass `apache2-foreground`.

---

## 6. Dockerfile: `printf '%{...}'` breaks in modern sh/dash

### The problem
The TastyIgniter `Dockerfile` had:
```dockerfile
RUN printf '...%{CORS_ORIGIN}e...' > /etc/apache2/conf-enabled/cors.conf
```
This worked for months because the Docker layer was cached. When the cache was invalidated (build context changed), the layer re-ran and failed: `printf: %{: invalid directive`.

Modern Debian containers use `dash` as `/bin/sh`, which interprets `%{` as an invalid printf format specifier.

### The fix
Replace `RUN printf` with a `COPY` of a pre-made file:
```dockerfile
COPY cors.conf /etc/apache2/conf-enabled/cors.conf
```

---

## 7. n8n execution data format (for debugging)

n8n 2.x stores execution data in a compressed deduplication format in the `execution_data` table. The `data` column is a JSON array where `arr[0]` has string indices that reference values elsewhere in the array.

To read the actual error from a failed execution:
```bash
docker exec backend-n8n-db-1 psql -U n8n -d n8n -c \
  "COPY (SELECT data FROM execution_data WHERE \"executionId\"=NNN) TO '/tmp/execNNN.json';"
docker cp backend-n8n-db-1:/tmp/execNNN.json /tmp/execNNN.json
```
Then `grep -o '"is not defined"' /tmp/execNNN.json` etc. — or look for `"lastNodeExecuted"` references.

To distinguish manual vs webhook executions:
```sql
SELECT id, mode, status, "startedAt" FROM execution_entity
WHERE "workflowId" = 'WORKFLOW_ID' ORDER BY id DESC LIMIT 10;
```

---

## 8. Adding error handling to n8n nodes

### For HTTP Request nodes
Set `"onError": "continueErrorOutput"` in the node JSON. This adds a second output port (index 1) that fires when the node returns an HTTP error or DNS failure. Wire it to a Telegram notification node.

```json
{
  "name": "Fetch Google Doc",
  "type": "n8n-nodes-base.httpRequest",
  "onError": "continueErrorOutput",
  ...
}
```

In connections:
```json
"Fetch Google Doc": {
  "main": [
    [{"node": "Next Node", "type": "main", "index": 0}],
    [{"node": "Telegram — Error Node", "type": "main", "index": 0}]
  ]
}
```

### For IF routing on isError flag
When a Code node outputs `{isError: true, error: '...', chatId: '...'}` on the same port as success, add an IF node immediately after:
- Condition: `$json.isError !== true`
- True branch → happy path
- False branch → Telegram error node

---

## 9. Workflow IDs (Workflow B)

| Workflow | ID | Status |
|---|---|---|
| B: Mobile Command Center | `av9R2wseN47PQZ8S` | ACTIVE |
| Telegram webhook path | `475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook` | registered |

---

## 10. n8n execution data: manual vs webhook

When debugging, always check the `mode` column in `execution_entity`:
- `manual` = triggered from n8n UI "Execute Workflow" button — Code nodes run inline (no task runner)
- `webhook` = triggered by real Telegram message — Code nodes run in task runner sandbox

If a workflow works in `manual` mode but fails in `webhook` mode, the cause is almost always the **task runner sandbox** (issue #1 above).
