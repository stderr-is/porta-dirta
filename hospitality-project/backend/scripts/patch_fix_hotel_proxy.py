import json

# Load the last known good state before hotel enrichment was added
with open('backend/n8n-workflows/backups/workflow-b-PRE-HOTEL-ENRICHMENT.json') as f:
    wf = json.load(f)

nodes = wf['nodes']
connections = wf['connections']

# ── 1. Create: Fetch Hotel Context (HTTP POST - THE FIX) ────────────────────
hotel_fetch_node = {
    "id": "fetch-hotel-context-001",
    "name": "Fetch Hotel Context",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4,
    "position": [1152, 2080],
    "onError": "continueErrorOutput",
    "parameters": {
        "url": "https://restaurant.hobbitonranch.com/api/internal/daily-summary",
        "method": "POST",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({ 'date': $json.checkIn || new Date().toISOString().split('T')[0] }) }}",
        "options": { "timeout": 8000 },
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                { "name": "X-Internal-Token", "value": "portadirta-n8n-2026" }
            ]
        }
    }
}
nodes.append(hotel_fetch_node)

# ── 2. Modify: Build Draft Prompt (to accept hotel context) ────────────────
for node in nodes:
    if node['name'] == 'Build Draft Prompt':
        node['parameters']['jsCode'] = """
const classify = $('Parse Classify Result').first().json;
const restoResult = $('Fetch Restaurant Context').first().json;
const hotelResult = items[0].json;

// Build contexts
let restoNote = 'No hay datos específicos de disponibilidad de restaurante.';
if (restoResult?.success) {
  restoNote = `Restaurante el ${restoResult.date}: ${restoResult.available ? 'HAY PLAZAS' : 'COMPLETO'} (${restoResult.bookedSeats}/${restoResult.capacity})`;
}

let hotelNote = 'No hay datos específicos de disponibilidad de hotel.';
if (hotelResult?.success) {
  hotelNote = `Hotel el ${hotelResult.date}: ${hotelResult.occupancy < 100 ? 'HAY HABITACIONES' : 'COMPLETO'} (${hotelResult.occupancy}% ocupación)`;
}

const roomInfo = "Torre Badum (Suite vistas Castillo, 180€), Cala El Pebret (Jardín, 120€), Cala Aljub (Piscina, 120€), Ermita Sant Antoni (Sierra, 120€).";

const systemPrompt =
  "Eres el conserje experto de Porta D'irta. Tu misión es redactar una respuesta IMPECABLE.

"
  + "REGLAS DE ORO:
"
  + "1. RESPONDE A TODAS LAS PREGUNTAS: Si el cliente pregunta por algo específico (ej: opciones sin gluten, mascotas, parking), DEBES responderlo basándote en tu conocimiento o di que lo consultarás.
"
  + "2. USA LA DISPONIBILIDAD: Si los datos dicen que hay sitio, confírmalo con alegría. Si está completo, sugiere otras fechas.
"
  + "3. TONO: Cálido, mediterráneo, sofisticado pero cercano. No uses listas aburridas si puedes integrarlo en un párrafo fluido.
"
  + "4. IDIOMA: Responde siempre en el idioma del cliente.

"
  + "CONOCIMIENTO:
"
  + "- Restaurante: Cocina mediterránea de autor. SÍ tenemos opciones vegetarianas, veganas y SIN GLUTEN (avisar en reserva).
"
  + "- Habitaciones: " + roomInfo + "
"
  + "- Ubicación: Camí del Pebret, Peñíscola. Parking gratuito para clientes.

"
  + "CONTEXTO REAL:
"
  + "- Fecha de hoy: " + new Date().toISOString().split('T')[0] + "
"
  + "- Disponibilidad Hotel: " + hotelNote + "
"
  + "- Disponibilidad Restaurante: " + restoNote + "

"
  + "DATOS DEL CLIENTE:
"
  + "- Nombre: " + (classify.senderName || "cliente") + "
"
  + "- Email original:
" + classify.bodyText + "

"
  + "Devuelve JSON: { "draftSubject": "Re: ...", "draftBody": "..." }";

const apiBody = JSON.stringify({
  model: 'claude-haiku-4-5-20251001',
  max_tokens: 2048,
  messages: [{ role: 'user', content: systemPrompt }]
});

return [{ json: { apiBody, classify } }];
"""
        break

# ── 3. Update connections (Sequential Chaining) ─────────────────────────────
connections['Fetch Restaurant Context']['main'] = [
    [{"node": "Fetch Hotel Context", "type": "main", "index": 0}],
    [{"node": "Fetch Hotel Context", "type": "main", "index": 0}]
]
connections['Fetch Hotel Context'] = {
    'main': [
        [{"node": "Build Draft Prompt", "type": "main", "index": 0}],
        [{"node": "Build Draft Prompt", "type": "main", "index": 0}]
    ]
}

# ── 4. Save patched files ───────────────────────────────────────────────────
with open('/tmp/wf_b_patched_nodes.json', 'w') as f:
    json.dump(nodes, f)
with open('/tmp/wf_b_patched_conns.json', 'w') as f:
    json.dump(connections, f)

print("✅ Bugfix patch ready: /tmp/wf_b_patched_nodes.json + /tmp/wf_b_patched_conns.json")
