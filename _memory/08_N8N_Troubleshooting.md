# 08 — n8n Troubleshooting & Hard-Won Lessons

## ⚠️ READ THIS BEFORE TOUCHING ANY n8n WORKFLOW

---

## 0. THE ONLY CORRECT WAY TO PATCH AN n8n WORKFLOW

> This is the single most important section. Every other approach we tried first failed. Follow this exactly every time.

### Why everything else fails

| What you might try | Why it doesn't work |
|---|---|
| Patch `workflow_entity.nodes` in SQL | n8n does NOT execute from this table |
| `deactivate` then `activate` via API | Does not reload code from DB |
| `PUT /api/v1/workflows/{id}` via API | Updates DB but runtime keeps old in-memory code |
| Tell user to click "Publish" in UI | UI sends browser-cached (old) state back to DB, erasing all patches |
| Manual "Execute Workflow" in UI | Runs inline (not task runner) — works differently than real webhooks |

**n8n executes from `workflow_history` (keyed by `versionId`), not `workflow_entity.nodes`.**
**The only way to make n8n use new code after a DB patch is: patch `workflow_history` + `docker compose restart n8n`.**

### The correct procedure

```bash
# ── STEP 1: get the active versionId ────────────────────────────────────────
VERID=$(docker exec backend-n8n-db-1 psql -U n8n -d n8n -t -A -c \
  "SELECT \"versionId\" FROM workflow_entity WHERE id='WORKFLOW_ID';")
echo "Active version: $VERID"

# ── STEP 2: extract nodes from workflow_history ──────────────────────────────
docker exec backend-n8n-db-1 psql -U n8n -d n8n -t -A -c \
  "SELECT nodes FROM workflow_history WHERE \"versionId\"='$VERID';" > /tmp/wh_nodes.json

# ── STEP 3: apply your patch in Python ───────────────────────────────────────
python3 << 'PYEOF'
import json
with open('/tmp/wh_nodes.json') as f:
    nodes = json.load(f)
# ... make changes to nodes ...
with open('/tmp/wh_patched.json', 'w') as f:
    json.dump(nodes, f)
PYEOF

# ── STEP 4: write to BOTH tables ─────────────────────────────────────────────
docker cp /tmp/wh_patched.json backend-n8n-db-1:/tmp/wh_patched.json
docker exec backend-n8n-db-1 psql -U n8n -d n8n -c "
  UPDATE workflow_history
    SET nodes = (SELECT nodes::jsonb FROM (SELECT pg_read_file('/tmp/wh_patched.json') AS nodes) t)
    WHERE \"versionId\" = '$VERID';
  UPDATE workflow_entity
    SET nodes = (SELECT nodes::jsonb FROM (SELECT pg_read_file('/tmp/wh_patched.json') AS nodes) t)
    WHERE id = 'WORKFLOW_ID';"

# ── STEP 5: restart n8n ──────────────────────────────────────────────────────
cd /home/stderr/hospitality-project/backend && docker compose restart n8n
sleep 8

# ── STEP 6: re-register Telegram webhook (ALWAYS needed after restart) ───────
BOT=$(docker exec backend-n8n-1 sh -c 'echo $TELEGRAM_BOT_TOKEN')
curl -s "https://api.telegram.org/bot${BOT}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://n8n.hobbitonranch.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook","allowed_updates":["message","callback_query"]}' \
  | python3 -m json.tool

# ── STEP 7: verify by sending a real message in Telegram ─────────────────────
# Do NOT test with "Execute Workflow" in the n8n UI — it runs in a different mode
# and does NOT reflect real webhook behaviour.
```

### How to verify the patch actually took effect

After restarting, always verify by checking the LATEST execution in the DB:

```bash
# Get the latest execution ID
docker exec backend-n8n-db-1 psql -U n8n -d n8n -c \
  "SELECT id, mode, status FROM execution_entity WHERE \"workflowId\"='WORKFLOW_ID' ORDER BY id DESC LIMIT 3;"

# Check the workflowData snapshot used in that execution
# (n8n writes this from workflow_history at execution time)
EID=<latest id>
docker exec backend-n8n-db-1 psql -U n8n -d n8n -c \
  "COPY (SELECT \"workflowData\" FROM execution_data WHERE \"executionId\"=$EID) TO '/tmp/check.json';"
docker cp backend-n8n-db-1:/tmp/check.json /tmp/check.json
python3 -c "
with open('/tmp/check.json') as f: s = f.read()
print('your_patch_string in snapshot:', 'your_patch_string' in s)
"
```

If your patch string is NOT in the snapshot of the latest execution, the fix did not take effect.

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

## 2. ⚠️ n8n executes from `workflow_history`, NOT `workflow_entity.nodes`

### The problem
n8n stores the live execution code in the **`workflow_history`** table, keyed by `versionId`. The `workflow_entity.nodes` column is NOT what n8n actually runs — it is only a convenience/display copy. Patching `workflow_entity` alone has zero effect on what executes.

Additionally:
- `deactivate/activate` does NOT reload code from the DB — it just toggles active state
- `PUT /api/v1/workflows/{id}` updates DB but n8n's runtime still uses its in-memory copy until restart
- The only way to make n8n use new code is: **patch `workflow_history` + restart n8n**

### The fix

```bash
# Step 1: get the active versionId
VERID=$(docker exec backend-n8n-db-1 psql -U n8n -d n8n -t -A -c \
  "SELECT \"versionId\" FROM workflow_entity WHERE id='WORKFLOW_ID';")

# Step 2: extract nodes from workflow_history
docker exec backend-n8n-db-1 psql -U n8n -d n8n -t -A -c \
  "SELECT nodes FROM workflow_history WHERE \"versionId\"='$VERID';" > /tmp/wh_nodes.json

# Step 3: patch /tmp/wh_nodes.json with python, save to /tmp/wh_patched.json

# Step 4: write back to BOTH tables
docker cp /tmp/wh_patched.json backend-n8n-db-1:/tmp/wh_patched.json
docker exec backend-n8n-db-1 psql -U n8n -d n8n -c "
  UPDATE workflow_history SET nodes = (SELECT nodes::jsonb FROM (SELECT pg_read_file('/tmp/wh_patched.json') AS nodes) t) WHERE \"versionId\"='$VERID';
  UPDATE workflow_entity SET nodes = (SELECT nodes::jsonb FROM (SELECT pg_read_file('/tmp/wh_patched.json') AS nodes) t) WHERE id='WORKFLOW_ID';"

# Step 5: restart n8n (required to reload from DB)
cd /home/stderr/hospitality-project/backend && docker compose restart n8n
sleep 8

# Step 6: re-register Telegram webhook (always needed after n8n restart)
BOT=$(docker exec backend-n8n-1 sh -c 'echo $TELEGRAM_BOT_TOKEN')
curl -s "https://api.telegram.org/bot${BOT}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://n8n.hobbitonranch.com/webhook/475cd6ce-bb05-46ee-aea8-663b6e9d8433/webhook","allowed_updates":["message","callback_query"]}'
```

The API key `n8n_api_activation_key_portadirta_2026` is stored in the `user_api_keys` table.

### Consequences
- Never patch only `workflow_entity` — always patch `workflow_history` too
- Never tell the user to "click Publish" — that overwrites both tables with the browser's stale cache
- `deactivate/activate` and `PUT` API calls do NOT reload code — only restart works
- If Publish was clicked: re-apply all patches to both tables, then restart

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
