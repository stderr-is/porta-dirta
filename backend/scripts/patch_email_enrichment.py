import json
import copy
import os

# Define paths
BACKUP_FILE = 'backend/n8n-workflows/backups/workflow-b-command-center-PRE-ENRICHMENT.json'
OUTPUT_NODES = '/tmp/wf_b_patched_nodes.json'
OUTPUT_CONNS = '/tmp/wf_b_patched_conns.json'

print(f"Loading backup from {BACKUP_FILE}...")
with open(BACKUP_FILE) as f:
    data = json.load(f)
    
# Extract nodes and connections
# row_to_json structure check: if it's wrapped, unwrap it.
# The previous command output `row_to_json` directly. 
# Let's assume standard structure or handle both.
if 'nodes' in data and 'connections' in data:
    nodes = data['nodes']
    conns = data['connections']
else:
    # Fallback if structure is different (e.g. list of rows)
    # But based on previous command, it should be a single object.
    print("Error: Invalid JSON structure in backup file.")
    exit(1)

print(f"Loaded {len(nodes)} nodes and {len(conns)} connections.")

# ── 1. Modify "Claude — Parse Intent" → classify only ───────────────────────
modified_intent = False
for node in nodes:
    if node['name'] == 'Claude — Parse Intent':
        # Preserve existing parameters but override jsonBody
        if 'parameters' not in node: node['parameters'] = {}
        
        node['parameters']['jsonBody'] = (
            "={{\n"
            "  JSON.stringify({\n"
            "    model: \"claude-haiku-4-5-20251001\",\n"
            "    max_tokens: 300,\n"
            "    messages: [{\n"
            "      role: \"user\",\n"
            "      content:\n"
            "        \"Extrae info del email y devuelve ÚNICAMENTE JSON (sin markdown):\\n\"\n"
            "        + \"{\\n\"\n"
            "        + \"  \\\"intent\\\": \\\"booking\\\" | \\\"restaurant\\\" | \\\"event\\\" | \\\"info\\\" | \\\"complaint\\\" | \\\"other\\\",\\n\"\n"
            "        + \"  \\\"language\\\": \\\"es\\\"|\\\"en\\\"|\\\"fr\\\"|\\\"de\\\"|etc,\\n\"\n"
            "        + \"  \\\"senderName\\\": \\\"nombre o null\\\",\\n\"\n"
            "        + \"  \\\"checkIn\\\": \\\"YYYY-MM-DD o null\\\",\\n\"\n"
            "        + \"  \\\"checkOut\\\": \\\"YYYY-MM-DD o null\\\",\\n\"\n"
            "        + \"  \\\"guests\\\": \\\"número o null\\\",\\n\"\n"
            "        + \"  \\\"restaurantDate\\\": \\\"YYYY-MM-DD o null\\\",\\n\"\n"
            "        + \"  \\\"restaurantGuests\\\": \\\"número o null\\\"\\n\"\n"
            "        + \"}\\n\"\n"
            "        + \"Fecha de hoy: \" + new Date().toISOString().substring(0,10) + \".\\n\\n\"\n"
            "        + \"De: \" + $(\"Email Idempotency\").first().json.from + \"\\n\"\n"
            "        + \"Asunto: \" + $(\"Email Idempotency\").first().json.subject + \"\\n\"\n"
            "        + \"Cuerpo: \" + $(\"Email Idempotency\").first().json.bodyText\n"
            "    }]\n"
            "  })\n"
            "}}"
        )
        modified_intent = True
        print("✓ Modified: Claude — Parse Intent (classify only, 300 tokens)")
        break

if not modified_intent:
    print("Warning: 'Claude — Parse Intent' node not found!")

# ── 2. New node: Parse Classify Result (Code) ────────────────────────────────
parse_node = {
    "id": "parse-classify-result-001",
    "name": "Parse Classify Result",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [928, 1856],
    "parameters": {
        "jsCode": (
            "const sd = $getWorkflowStaticData('global');\n"
            "const raw = items[0].json.content?.[0]?.text || '{}';\n"
            "let parsed;\n"
            "try {\n"
            "  parsed = JSON.parse(raw.replace(/^```json\\s*/i,'').replace(/```\\s*$/,'').trim());\n"
            "} catch(e) {\n"
            "  parsed = { intent: 'other', language: 'es' };\n"
            "}\n"
            "const email = $('Email Idempotency').first().json;\n"
            "return [{ json: {\n"
            "  msgKey:           email.msgKey,\n"
            "  from:             email.from,\n"
            "  subject:          email.subject,\n"
            "  bodyText:         email.bodyText,\n"
            "  intent:           parsed.intent          || 'other',\n"
            "  language:         parsed.language         || 'es',\n"
            "  senderName:       parsed.senderName       || null,\n"
            "  checkIn:          parsed.checkIn           || null,\n"
            "  checkOut:         parsed.checkOut          || null,\n"
            "  guests:           parsed.guests            || null,\n"
            "  restaurantDate:   parsed.restaurantDate    || null,\n"
            "  restaurantGuests: parsed.restaurantGuests  || null,\n"
            "} }];\n"
        )
    }
}

# ── 3. New node: Fetch Restaurant Context (HTTP GET) ─────────────────────────
fetch_node = {
    "id": "fetch-restaurant-context-001",
    "name": "Fetch Restaurant Context",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4,
    "position": [1152, 1856],
    "onError": "continueErrorOutput",
    "parameters": {
        "url": "=https://restaurant.hobbitonranch.com/api/internal/availability?date={{ $json.restaurantDate || new Date().toISOString().split('T')[0] }}&guests={{ $json.restaurantGuests || 2 }}",
        "method": "GET",
        "options": { "timeout": 8000 },
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                { "name": "X-Internal-Token", "value": "portadirta-n8n-2026" }
            ]
        }
    }
}

# ── 4. New node: Build Draft Prompt (Code) ───────────────────────────────────
build_node = {
    "id": "build-draft-prompt-001",
    "name": "Build Draft Prompt",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1376, 1856],
    "parameters": {
        "jsCode": (
            "const classify = $('Parse Classify Result').first().json;\n"
            "const fetchResult = items[0].json;\n\n"

            "// Build availability context note\n"
            "let contextNote = 'disponibilidad del restaurante no consultada en tiempo real';\n"
            "if (fetchResult && fetchResult.success === true) {\n"
            "  const status = fetchResult.available\n"
            "    ? 'hay disponibilidad'\n"
            "    : 'COMPLETO — no hay plazas libres';\n"
            "  contextNote = 'Restaurante el ' + fetchResult.date + ': ' + status\n"
            "    + ' (' + fetchResult.bookedSeats + ' de ' + fetchResult.capacity + ' plazas ocupadas)';\n"
            "}\n\n"

            "const roomInfo =\n"
            "  'Torre Badum: suite con terraza privada, vistas al Castillo Papal y al Mediterráneo, 2 personas, desde 180€/noche.\\n'\n"
            "  + 'Cala El Pebret: habitación con jardín y vistas a la naturaleza, 2 personas, desde 120€/noche.\\n'\n"
            "  + 'Cala Aljub: habitación con vistas a la piscina, 2 personas, desde 120€/noche.\\n'\n"
            "  + 'Ermita Sant Antoni: habitación con vistas a la Sierra de Irta, 2 personas, desde 120€/noche.';\n\n"

            "const today = new Date().toISOString().split('T')[0];\n\n"

            "const systemPrompt =\n"
            "  'Eres el asistente de email de Porta D\\'irta, hotel boutique en Peñíscola (Costa del Azahar, España).\\n'\n"
            "  + 'Redacta una respuesta al email del huésped: cálida, mediterránea, profesional.\\n'\n"
            "  + 'Firma siempre como \"El equipo de Porta D\\'irta\".\\n'\n"
            "  + 'Responde en el mismo idioma que el remitente.\\n'\n"
            "  + 'Si tienes datos de disponibilidad, úsalos. Si no, sé honesto y di que confirmaremos.\\n\\n'\n"
            "  + 'HABITACIONES:\\n' + roomInfo + '\\n\\n'\n"
            "  + 'RESTAURANTE: cocina mediterránea, almuerzo 13:00–16:00, cena 20:00–22:00, martes a domingo.\\n'\n"
            "  + 'Capacidad: 75 comensales. Reservas recomendadas.\\n\\n'\n"
            "  + 'CONTACTO: +34 644 026 066 · info@portadirta.com · Camí del Pebret s/n, 12598 Peñíscola.\\n\\n'\n"
            "  + 'DATOS EXTRAÍDOS DEL EMAIL:\\n'\n"
            "  + 'Intent: ' + classify.intent + '\\n'\n"
            "  + 'Remitente: ' + (classify.senderName || classify.from) + '\\n'\n"
            "  + (classify.checkIn          ? 'Check-in solicitado: '         + classify.checkIn          + '\\n' : '')\n"
            "  + (classify.checkOut         ? 'Check-out solicitado: '        + classify.checkOut         + '\\n' : '')\n"
            "  + (classify.guests           ? 'Huéspedes: '                   + classify.guests           + '\\n' : '')\n"
            "  + (classify.restaurantDate   ? 'Fecha restaurante solicitada: '+ classify.restaurantDate   + '\\n' : '')\n"
            "  + (classify.restaurantGuests ? 'Comensales: '                  + classify.restaurantGuests + '\\n' : '')\n"
            "  + '\\nCONTEXTO EN TIEMPO REAL: ' + contextNote + '\\n\\n'\n"
            "  + 'EMAIL ORIGINAL:\\n'\n"
            "  + 'De: '      + classify.from    + '\\n'\n"
            "  + 'Asunto: '  + classify.subject + '\\n'\n"
            "  + 'Cuerpo:\\n' + classify.bodyText + '\\n\\n'\n"
            "  + 'Devuelve ÚNICAMENTE JSON válido (sin markdown):\\n'\n"
            "  + '{\\n'\n"
            "  + '  \"draftSubject\": \"Re: <asunto>\",\\n'\n"
            "  + '  \"draftBody\": \"<respuesta completa>\"\\n'\n"
            "  + '}\\n'\n"
            "  + 'Fecha de hoy: ' + today;\n\n"

            "const apiBody = JSON.stringify({\n"
            "  model: 'claude-haiku-4-5-20251001',\n"
            "  max_tokens: 2048,\n"
            "  messages: [{ role: 'user', content: systemPrompt }]\n"
            "});\n\n"

            "return [{ json: { apiBody, classify, contextNote } }];\n"
        )
    }
}

# ── 5. New node: Claude — Generate Draft (HTTP POST) ─────────────────────────
draft_node = {
    "id": "claude-generate-draft-001",
    "name": "Claude — Generate Draft",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4,
    "position": [1600, 1856],
    "parameters": {
        "url": "https://api.anthropic.com/v1/messages",
        "method": "POST",
        "options": { "timeout": 30000 },
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": "={{ $json.apiBody }}",
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                { "name": "x-api-key",          "value": "={{ $env.ANTHROPIC_API_KEY }}" },
                { "name": "anthropic-version",   "value": "2023-06-01" },
                { "name": "content-type",        "value": "application/json" }
            ]
        }
    }
}

nodes.extend([parse_node, fetch_node, build_node, draft_node])
print("✓ Added 4 new nodes")

# ── 6. Update connections ────────────────────────────────────────────────────
# Remove old: Claude — Parse Intent → Email Store + Preview
if 'Claude — Parse Intent' in conns:
    # Filter out the connection to Email Store + Preview
    old_main = conns['Claude — Parse Intent'].get('main', [])
    new_main = []
    for port in old_main:
        # Filter connections to 'Email Store + Preview'
        new_port = [t for t in port if t.get('node') != 'Email Store + Preview']
        new_main.append(new_port)
    conns['Claude — Parse Intent']['main'] = new_main
    print("✓ Removed: Claude — Parse Intent → Email Store + Preview")

# Add: Claude — Parse Intent → Parse Classify Result
if 'Claude — Parse Intent' not in conns:
    conns['Claude — Parse Intent'] = {'main': []}
while len(conns['Claude — Parse Intent']['main']) < 1:
    conns['Claude — Parse Intent']['main'].append([])
conns['Claude — Parse Intent']['main'][0].append({
    "node": "Parse Classify Result", "type": "main", "index": 0
})
print("✓ Added: Claude — Parse Intent → Parse Classify Result")

# Add: Parse Classify Result → Fetch Restaurant Context
conns['Parse Classify Result'] = {
    'main': [[{"node": "Fetch Restaurant Context", "type": "main", "index": 0}]]
}
print("✓ Added: Parse Classify Result → Fetch Restaurant Context")

# Add: Fetch Restaurant Context [0] → Build Draft Prompt (success)
#       Fetch Restaurant Context [1] → Build Draft Prompt (error)
conns['Fetch Restaurant Context'] = {
    'main': [
        [{"node": "Build Draft Prompt", "type": "main", "index": 0}],  # port 0: success
        [{"node": "Build Draft Prompt", "type": "main", "index": 0}],  # port 1: error
    ]
}
print("✓ Added: Fetch Restaurant Context [0+1] → Build Draft Prompt")

# Add: Build Draft Prompt → Claude — Generate Draft
conns['Build Draft Prompt'] = {
    'main': [[{"node": "Claude — Generate Draft", "type": "main", "index": 0}]]
}
print("✓ Added: Build Draft Prompt → Claude — Generate Draft")

# Add: Claude — Generate Draft → Email Store + Preview
conns['Claude — Generate Draft'] = {
    'main': [[{"node": "Email Store + Preview", "type": "main", "index": 0}]]
}
print("✓ Added: Claude — Generate Draft → Email Store + Preview")

# ── 7. Save outputs ──────────────────────────────────────────────────────────
with open(OUTPUT_NODES, 'w') as f:
    json.dump(nodes, f, indent=2)
with open(OUTPUT_CONNS, 'w') as f:
    json.dump(conns, f, indent=2)

print(f"\n✅ Patch ready: {OUTPUT_NODES} + {OUTPUT_CONNS}")
