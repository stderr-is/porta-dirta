import json, copy, sys

# ── Load current state ───────────────────────────────────────────────────────
with open('backend/n8n-workflows/backups/workflow-b-PRE-HOTEL-ENRICHMENT.json') as f:
    wf = json.load(f)

nodes = wf['nodes']
conns = wf['connections']

# ── 1. Create: Fetch Hotel Context (HTTP POST) ────────────────────────────────
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
        "jsonBody": "={{ JSON.stringify({ date: $json.checkIn || new Date().toISOString().split('T')[0] }) }}",
        "options": { "timeout": 8000 },
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                { "name": "X-Internal-Token", "value": "portadirta-n8n-2026" }
            ]
        }
    }
}

# ── 2. Modify: Build Draft Prompt (Code) ───────────────────────────────────
for node in nodes:
    if node['name'] == 'Build Draft Prompt':
        node['parameters']['jsCode'] = (
            "const classify = $('Parse Classify Result').first().json;\n"
            "const restoResult = $('Fetch Restaurant Context').first().json;\n"
            "const hotelResult = items[0].json;\n\n"

            "// 1. Restaurant availability context\n"
            "let restoNote = 'disponibilidad del restaurante no consultada';\n"
            "if (restoResult && restoResult.success === true) {\n"
            "  const status = restoResult.available ? 'hay disponibilidad' : 'COMPLETO';\n"
            "  restoNote = 'Restaurante el ' + restoResult.date + ': ' + status\n"
            "    + ' (' + restoResult.bookedSeats + ' de ' + restoResult.capacity + ' plazas ocupadas)';\n"
            "}\n\n"

            "// 2. Hotel availability context\n"
            "let hotelNote = 'disponibilidad de habitaciones no consultada';\n"
            "if (hotelResult && hotelResult.success === true) {\n"
            "  const occupancy = hotelResult.occupancy || 0;\n"
            "  const status = occupancy < 100 ? 'HAY HABITACIONES LIBRES' : 'HOTEL COMPLETO';\n"
            "  hotelNote = 'Hotel el ' + hotelResult.date + ': ' + status + ' (' + occupancy + '% ocupación)';\n"
            "  if (hotelResult.rooms && hotelResult.rooms.length > 0) {\n"
            "    hotelNote += '\\nDetalle habitaciones:\\n' + hotelResult.rooms.map(r => ' - ' + r.name + ': ' + (r.booked ? 'Ocupada' : 'LIBRE')).join('\\n');\n"
            "  }\n"
            "}\n\n"

            "const roomInfo =\n"
            "  'Torre Badum: suite con terraza privada, vistas al Castillo Papal y al Mediterráneo, 2 personas, desde 180€/noche.\\n'\n"
            "  + 'Cala El Pebret: habitación con jardín y vistas a la naturaleza, 2 personas, desde 120€/noche.\\n'\n"
            "  + 'Cala Aljub: habitación con vistas a la piscina, 2 personas, desde 120€/noche.\\n'\n"
            "  + 'Ermita Sant Antoni: habitación con vistas a la Sierra de Irta, 2 personas, desde 120€/noche.';\n\n"

            "const today = new Date().toISOString().split('T')[0];\n\n"

            "const systemPrompt =\n"
            "  'Eres el asistente de email de Porta D\\'irta, hotel boutique en Peñíscola.\\n'\n"
            "  + 'Redacta una respuesta cálida, mediterránea y profesional.\\n'\n"
            "  + 'Responde en el mismo idioma que el remitente.\\n'\n"
            "  + 'Si tienes datos de disponibilidad (hotel y restaurante), úsalos para informar al cliente.\\n'\n"
            "  + 'Si el hotel o restaurante están completos para la fecha solicitada, sugiere amablemente que busquen otra fecha o diles que les contactaremos pronto para darles alternativas.\\n\\n'\n"
            "  + 'INFO HABITACIONES:\\n' + roomInfo + '\\n\\n'\n"
            "  + 'INFO RESTAURANTE: almuerzo 13:00–16:00, cena 20:00–22:00, martes a domingo.\\n\\n'\n"
            "  + 'DATOS EMAIL:\\n'\n"
            "  + 'Intent: ' + classify.intent + '\\n'\n"
            "  + 'Remitente: ' + (classify.senderName || classify.from) + '\\n'\n"
            "  + (classify.checkIn          ? 'Check-in solicitado: '         + classify.checkIn          + '\\n' : '')\n"
            "  + (classify.checkOut         ? 'Check-out solicitado: '        + classify.checkOut         + '\\n' : '')\n"
            "  + (classify.guests           ? 'Huéspedes: '                   + classify.guests           + '\\n' : '')\n"
            "  + (classify.restaurantDate   ? 'Fecha restaurante solicitada: '+ classify.restaurantDate   + '\\n' : '')\n"
            "  + (classify.restaurantGuests ? 'Comensales: '                  + classify.restaurantGuests + '\\n' : '')\n"
            "  + '\\nCONTEXTO HOTEL: ' + hotelNote + '\\n'\n"
            "  + 'CONTEXTO RESTAURANTE: ' + restoNote + '\\n\\n'\n"
            "  + 'EMAIL ORIGINAL:\\n'\n"
            "  + 'De: '      + classify.from    + '\\n'\n"
            "  + 'Asunto: '  + classify.subject + '\\n'\n"
            "  + 'Cuerpo:\\n' + classify.bodyText + '\\n\\n'\n"
            "  + 'Devuelve ÚNICAMENTE JSON válido (sin markdown):\\n'\n"
            "  + '{\\n'\n"
            "  + '  \"draftSubject\": \"Re: <asunto>\",\\n'\n"
            "  + '  \"draftBody\": \"<respuesta completa>\"\\n'\n"
            "  + '}\\n';\n\n"

            "const apiBody = JSON.stringify({\n"
            "  model: 'claude-haiku-4-5-20251001',\n"
            "  max_tokens: 2048,\n"
            "  messages: [{ role: 'user', content: systemPrompt }]\n"
            "});\n\n"

            "return [{ json: { apiBody, classify, hotelNote, restoNote } }];\n"
        )
        print("✓ Modified: Build Draft Prompt (added hotel context logic)")
        break

# ── 3. Add node and Update connections ──────────────────────────────────────
nodes.append(hotel_fetch_node)
print("✓ Added: Fetch Hotel Context node")

# Rewire: Fetch Restaurant Context → Fetch Hotel Context
# Fetch Restaurant Context port 0 (success) and port 1 (error) both go to Hotel Context
conns['Fetch Restaurant Context'] = {
    'main': [
        [{"node": "Fetch Hotel Context", "type": "main", "index": 0}],  # port 0
        [{"node": "Fetch Hotel Context", "type": "main", "index": 0}],  # port 1
    ]
}
print("✓ Rewired: Fetch Restaurant Context → Fetch Hotel Context")

# Rewire: Fetch Hotel Context → Build Draft Prompt
# Fetch Hotel Context port 0 (success) and port 1 (error) both go to Build Draft Prompt
conns['Fetch Hotel Context'] = {
    'main': [
        [{"node": "Build Draft Prompt", "type": "main", "index": 0}],  # port 0
        [{"node": "Build Draft Prompt", "type": "main", "index": 0}],  # port 1
    ]
}
print("✓ Rewired: Fetch Hotel Context → Build Draft Prompt")

# ── 4. Save patched files ────────────────────────────────────────────────────
with open('/tmp/wf_b_patched_nodes.json', 'w') as f:
    json.dump(nodes, f)
with open('/tmp/wf_b_patched_conns.json', 'w') as f:
    json.dump(conns, f)

print("\n✅ Patch ready: /tmp/wf_b_patched_nodes.json + /tmp/wf_b_patched_conns.json")
