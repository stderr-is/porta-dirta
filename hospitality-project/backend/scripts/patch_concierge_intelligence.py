import json, hashlib

# Load current nodes/connections from the LATEST backup (which includes the hotel fetch node)
# Note: I should get the current state from DB ideally, but I'll use the latest known good structure.
with open('backend/n8n-workflows/backups/workflow-b-PRE-HOTEL-ENRICHMENT.json') as f:
    wf = json.load(f)

nodes = wf['nodes']
connections = wf['connections']

def get_node(name):
    for n in nodes:
        if n['name'] == name: return n
    return None

# Rewire: Parse Classify Result → Fetch Restaurant Context
connections['Parse Classify Result'] = {
    'main': [
        [{"node": "Fetch Restaurant Context", "type": "main", "index": 0}]
    ]
}

# ── 1. Fix: Email Idempotency (Safe msgKey length + Sandbox compatible) ──────
node_idemp = get_node('Email Idempotency')
if node_idemp:
    node_idemp['parameters']['jsCode'] = (
        "const email = items[0].json;\n"
        "const sd = $getWorkflowStaticData('global');\nsd.processedEmails = sd.processedEmails || {};\n\n"
        "// Unique key from Message-ID or Date+Subject+From\n"
        "const idSource = email.metadata?.['message-id'] || (email.date + email.subject + email.from);\n"
        "const from = String(email.from || '').toLowerCase();\n"
        "if (from.includes('portadirta.com')) return [];\n\n"
        "// Use Base64 (cleaned) for a safe, unique, short key without crypto dependencies\n"
        "const msgKey = Buffer.from(idSource).toString('base64')\n"
        "  .replace(/[^a-zA-Z0-9]/g, '')\n"
        "  .substring(0, 32);\n\n"
        "if (sd.processedEmails[msgKey]) return [];\n\n"
        "const cutoff24h = Date.now() - 24 * 3600000;\n"
        "for (const k of Object.keys(sd.processedEmails)) {\n"
        "  if ((sd.processedEmails[k]?.ts || 0) < cutoff24h) delete sd.processedEmails[k];\n"
        "}\n\n"
        "sd.processedEmails[msgKey] = { ts: Date.now(), status: 'processing' };\n\n"
        "const stripHtml = (h) => String(h || '').replace(/<style[\\s\\S]*?<\\/style>/gi, '').replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim();\n"
        "const bodyText = (email.text || stripHtml(email.html || '') || '').substring(0, 3000);\n\n"
        "return [{ json: { msgKey, from: email.from, subject: email.subject, bodyText, date: email.date } }];"
    )

# ── 2. Fix: Claude — Parse Intent (Better Date Logic) ──────────────────────
node_parse = get_node('Claude — Parse Intent')
if node_parse:
    node_parse['parameters']['jsonBody'] = (
        "={{\n"
        "  JSON.stringify({\n"
        "    model: \"claude-haiku-4-5-20251001\",\n"
        "    max_tokens: 400,\n"
        "    messages: [{\n"
        "      role: \"user\",\n"
        "      content:\n"
        "        \"Actúa como un experto en extracción de entidades para un hotel boutique.\\n\"\n"
        "        + \"Analiza el email y extrae la intención y las fechas. REGLAS CRÍTICAS:\\n\"\n"
        "        + \"1. Si mencionan 'este sábado', calcula la fecha basándote en 'Hoy'.\\n\"\n"
        "        + \"2. Si mencionan meses (abril, mayo...), asume el año actual o el próximo si el mes ya pasó.\\n\"\n"
        "        + \"3. Si piden disponibilidad de habitación, el intent es 'booking'.\\n\"\n"
        "        + \"4. Si preguntan por comida/mesa, el intent es 'restaurant'.\\n\\n\"\n"
        "        + \"Devuelve ÚNICAMENTE JSON (sin markdown):\\n\"\n"
        "        + \"{\\n\"\n"
        "        + \"  \\\"intent\\\": \\\"booking\\\" | \\\"restaurant\\\" | \\\"event\\\" | \\\"info\\\" | \\\"other\\\",\\n\"\n"
        "        + \"  \\\"language\\\": \\\"es\\\"|\\\"en\\\"|\\\"fr\\\"|\\\"de\\\",\\n\"\n"
        "        + \"  \\\"senderName\\\": \\\"string o null\\\",\\n\"\n"
        "        + \"  \\\"checkIn\\\": \\\"YYYY-MM-DD o null\\\",\\n\"\n"
        "        + \"  \\\"checkOut\\\": \\\"YYYY-MM-DD o null\\\",\\n\"\n"
        "        + \"  \\\"guests\\\": \\\"número o null\\\",\\n\"\n"
        "        + \"  \\\"restaurantDate\\\": \\\"YYYY-MM-DD o null\\\",\\n\"\n"
        "        + \"  \\\"restaurantGuests\\\": \\\"número o null\\\"\\n\"\n"
        "        + \"}\\n\\n\"\n"
        "        + \"Hoy es: \" + new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) + \" (ISO: \" + new Date().toISOString().substring(0,10) + \").\\n\\n\"\n"
        "        + \"De: \" + $(\"Email Idempotency\").first().json.from + \"\\n\"\n"
        "        + \"Asunto: \" + $(\"Email Idempotency\").first().json.subject + \"\\n\"\n"
        "        + \"Cuerpo: \" + $(\"Email Idempotency\").first().json.bodyText\n"
        "    }]\n"
        "  })\n"
        "}}"
    )

# ── 3. Fix: Build Draft Prompt (Coverage of specific questions) ────────────
node_draft = get_node('Build Draft Prompt')
if node_draft:
    node_draft['parameters']['jsCode'] = (
        "const classify = $('Parse Classify Result').first().json;\n"
        "const restoResult = $('Fetch Restaurant Context').first().json;\n"
        "const hotelResult = $('Fetch Hotel Context').first().json;\n\n"

        "// Build contexts\n"
        "let restoNote = 'No hay datos específicos de disponibilidad de restaurante.';\n"
        "if (restoResult?.success) {\n"
        "  restoNote = `Restaurante el ${restoResult.date}: ${restoResult.available ? 'HAY PLAZAS' : 'COMPLETO'} (${restoResult.bookedSeats}/${restoResult.capacity})`;\n"
        "}\n\n"
        "let hotelNote = 'No hay datos específicos de disponibilidad de hotel.';\n"
        "if (hotelResult?.success) {\n"
        "  hotelNote = `Hotel el ${hotelResult.date}: ${hotelResult.occupancy < 100 ? 'HAY HABITACIONES' : 'COMPLETO'} (${hotelResult.occupancy}% ocupación)`;\n"
        "}\n\n"
        "const roomInfo = \"Torre Badum (Suite vistas Castillo, 180€), Cala El Pebret (Jardín, 120€), Cala Aljub (Piscina, 120€), Ermita Sant Antoni (Sierra, 120€).\";\n\n"

        "const systemPrompt =\n"
        "  \"Eres el conserje experto de Porta D'irta. Tu misión es redactar una respuesta IMPECABLE.\\n\\n\"\n"
        "  + \"REGLAS DE ORO:\\n\"\n"
        "  + \"1. RESPONDE A TODAS LAS PREGUNTAS: Si el cliente pregunta por algo específico (ej: opciones sin gluten, mascotas, parking), DEBES responderlo basándote en tu conocimiento o di que lo consultarás.\\n\"\n"
        "  + \"2. USA LA DISPONIBILIDAD: Si los datos dicen que hay sitio, confírmalo con alegría. Si está completo, sugiere otras fechas.\\n\"\n"
        "  + \"3. TONO: Cálido, mediterráneo, sofisticado pero cercano. No uses listas aburridas si puedes integrarlo en un párrafo fluido.\\n\"\n"
        "  + \"4. IDIOMA: Responde siempre en el idioma del cliente.\\n\\n\"\n"
        "  + \"CONOCIMIENTO:\\n\"\n"
        "  + \"- Restaurante: Cocina mediterránea de autor. SÍ tenemos opciones vegetarianas, veganas y SIN GLUTEN (avisar en reserva).\\n\"\n"
        "  + \"- Habitaciones: \" + roomInfo + \"\\n\"\n"
        "  + \"- Ubicación: Camí del Pebret, Peñíscola. Parking gratuito para clientes.\\n\\n\"\n"
        "  + \"CONTEXTO REAL:\\n\"\n"
        "  + \"- Fecha de hoy: \" + new Date().toISOString().split('T')[0] + \"\\n\"\n"
        "  + \"- Disponibilidad Hotel: \" + hotelNote + \"\\n\"\n"
        "  + \"- Disponibilidad Restaurante: \" + restoNote + \"\\n\\n\"\n"
        "  + \"DATOS DEL CLIENTE:\\n\"\n"
        "  + \"- Nombre: \" + (classify.senderName || \"cliente\") + \"\\n\"\n"
        "  + \"- Email original:\\n\" + classify.bodyText + \"\\n\\n\"\n"
        "  + \"Devuelve JSON: { \\\"draftSubject\\\": \\\"Re: ...\\\", \\\"draftBody\\\": \\\"...\\\" }\";\n\n"

        "const apiBody = JSON.stringify({\n"
        "  model: 'claude-haiku-4-5-20251001',\n"
        "  max_tokens: 2048,\n"
        "  messages: [{ role: 'user', content: systemPrompt }]\n"
        "});\n\n"
        "return [{ json: { apiBody, classify } }];"
    )

# ── 4. Fix: Email Store + Preview (Safer cbKey) ────────────────────────────
node_store = get_node('Email Store + Preview')
if node_store:
    node_store['parameters']['jsCode'] = (
        "const sd = $getWorkflowStaticData('global');\nsd.pendingDrafts = sd.pendingDrafts || {};\n\n"
        "const { msgKey, from, subject } = $('Email Idempotency').first().json;\n"
        "const raw = items[0].json.content?.[0]?.text || '{}';\n\n"
        "let draft;\ntry {\n  draft = JSON.parse(raw.replace(/^```json\\s*/i, '').replace(/```\\s*$/, '').trim());\n} catch(e) {\n  draft = { draftSubject: 'Re: ' + subject, draftBody: 'Error generando borrador.' };\n}\n\n"
        "const cbKey = msgKey; // msgKey is already a short 24-char hash\n\n"
        "sd.pendingDrafts[cbKey] = {\n"
        "  to: from, subject: draft.draftSubject, body: draft.draftBody, msgKey, ts: Date.now()\n"
        "};\n\n"
        "const preview = draft.draftBody.substring(0, 600) + (draft.draftBody.length > 600 ? '…' : '');\n"
        "const msg = `📧 *Nuevo email*\\nDe: \\`${from}\\`\\nAsunto: _${subject}_\\n\\n*Borrador:*\\n${preview}`;\n\n"
        "return [{ json: { msg, cbKey, adminId: $env.TELEGRAM_ADMIN_ID } }];"
    )

# Save patched state
with open('/tmp/wf_b_patched_nodes.json', 'w') as f:
    json.dump(nodes, f)
print("✅ Intelligence patch ready in /tmp/wf_b_patched_nodes.json")
