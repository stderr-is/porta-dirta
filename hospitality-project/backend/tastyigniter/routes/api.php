<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

/**
 * Public restaurant reservation endpoint — no auth required.
 * Called directly from the frontend booking form.
 */
Route::post('public/reservations', function (Request $request) {
    $data = $request->validate([
        'nombre'        => 'required|string|max:200',
        'email'         => 'required|email|max:200',
        'telefono'      => 'required|string|max:30',
        'personas'      => 'required|integer|min:1|max:50',
        'fecha'         => 'required|date_format:Y-m-d',
        'hora'          => 'required|date_format:H:i',
        'observaciones' => 'nullable|string|max:1000',
    ]);

    $parts     = explode(' ', trim($data['nombre']), 2);
    $firstName = $parts[0];
    $lastName  = $parts[1] ?? '';
    $now       = now();

    // Format date for display: "miércoles, 1 de abril de 2026"
    $dateObj     = \DateTime::createFromFormat('Y-m-d', $data['fecha']);
    $dayNames    = ['domingo','lunes','martes','miércoles','jueves','viernes','sábado'];
    $monthNames  = ['','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    $dateDisplay = $dayNames[(int)$dateObj->format('w')] . ', ' .
                   (int)$dateObj->format('j') . ' de ' .
                   $monthNames[(int)$dateObj->format('n')] . ' de ' .
                   $dateObj->format('Y');

    DB::table('reservations')->insert([
        'location_id'  => 1,
        'table_id'     => 0,
        'guest_num'    => (int) $data['personas'],
        'first_name'   => $firstName,
        'last_name'    => $lastName,
        'email'        => $data['email'],
        'telephone'    => $data['telefono'],
        'reserve_date' => $data['fecha'],
        'reserve_time' => $data['hora'],
        'duration'     => 90,
        'status_id'    => null,
        'comment'      => $data['observaciones'] ?? '',
        'ip_address'   => $request->ip(),
        'user_agent'   => $request->userAgent() ?? '',
        'created_at'   => $now,
        'updated_at'   => $now,
    ]);

    // ── Internal notification to restaurant ─────────────────────────────
    $obs = !empty($data["observaciones"]) ? htmlspecialchars($data["observaciones"]) : "—";
    Mail::html(
        "<p>Nueva reserva recibida:</p>
         <table cellpadding='6' style='border-collapse:collapse;font-family:sans-serif;font-size:14px'>
           <tr><td><strong>Nombre</strong></td><td>{$data['nombre']}</td></tr>
           <tr><td><strong>Email</strong></td><td>{$data['email']}</td></tr>
           <tr><td><strong>Teléfono</strong></td><td>{$data['telefono']}</td></tr>
           <tr><td><strong>Personas</strong></td><td>{$data['personas']}</td></tr>
           <tr><td><strong>Fecha</strong></td><td>{$dateDisplay}</td></tr>
           <tr><td><strong>Hora</strong></td><td>{$data['hora']} h</td></tr>
           <tr><td><strong>Observaciones</strong></td><td>{$obs}</td></tr>
         </table>",
        fn ($m) => $m->to('info@portadirta.com')
                     ->subject("🍽 Nueva reserva — {$data['nombre']} · {$dateDisplay} {$data['hora']}h")
    );

    // ── Branded confirmation to guest ────────────────────────────────────
    $obsRow = !empty($data["observaciones"])
        ? "<tr>
             <td style='padding:10px 16px;color:#8b7355;font-size:12px;text-transform:uppercase;letter-spacing:.08em;white-space:nowrap'>Observaciones</td>
             <td style='padding:10px 16px;color:#0d2b45;font-size:15px'>" . htmlspecialchars($data['observaciones'] ?? '') . "</td>
           </tr>"
        : '';

    $html = "<!DOCTYPE html>
<html lang='es'>
<head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head>
<body style='margin:0;padding:0;background:#f5f3ef;font-family:Georgia,serif'>

  <!-- Wrapper -->
  <table width='100%' cellpadding='0' cellspacing='0' style='background:#f5f3ef;padding:40px 16px'>
    <tr><td align='center'>
    <table width='600' cellpadding='0' cellspacing='0' style='max-width:600px;width:100%'>

      <!-- Header -->
      <tr>
        <td align='center' style='background:#0d2b45;padding:40px 32px 32px'>
          <img src='https://portadirta.com/wp-content/uploads/2026/02/LOGO-negativo.png'
               alt=\"Porta D'irta\" width='160' style='display:block;margin:0 auto 24px'>
          <div style='width:48px;height:1px;background:#c9a84c;margin:0 auto 24px'></div>
          <h1 style='margin:0;color:#ffffff;font-size:26px;font-weight:400;letter-spacing:.02em'>
            Reserva Confirmada
          </h1>
          <p style='margin:12px 0 0;color:rgba(255,255,255,.65);font-family:Arial,sans-serif;font-size:13px;letter-spacing:.06em;text-transform:uppercase'>
            Restaurante Porta D'irta · Peñíscola
          </p>
        </td>
      </tr>

      <!-- Greeting -->
      <tr>
        <td style='background:#ffffff;padding:36px 40px 8px'>
          <p style='margin:0;color:#0d2b45;font-size:18px;line-height:1.6'>
            Hola, <strong>{$data['nombre']}</strong>.
          </p>
          <p style='margin:12px 0 0;color:#555;font-family:Arial,sans-serif;font-size:14px;line-height:1.7'>
            Hemos recibido tu reserva y estamos encantados de recibirte.
            A continuación encontrarás el resumen de tu reserva.
          </p>
        </td>
      </tr>

      <!-- Reservation details card -->
      <tr>
        <td style='background:#ffffff;padding:24px 40px 32px'>
          <table width='100%' cellpadding='0' cellspacing='0'
                 style='border:1px solid #e8e4dd;border-radius:6px;overflow:hidden'>
            <tr style='background:#f5f3ef'>
              <td colspan='2' style='padding:12px 16px;border-bottom:1px solid #e8e4dd'>
                <span style='color:#c9a84c;font-family:Arial,sans-serif;font-size:11px;
                             text-transform:uppercase;letter-spacing:.12em;font-weight:600'>
                  Detalles de la reserva
                </span>
              </td>
            </tr>
            <tr style='border-bottom:1px solid #e8e4dd'>
              <td style='padding:10px 16px;color:#8b7355;font-family:Arial,sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:.08em;white-space:nowrap'>Fecha</td>
              <td style='padding:10px 16px;color:#0d2b45;font-size:15px'>{$dateDisplay}</td>
            </tr>
            <tr style='border-bottom:1px solid #e8e4dd;background:#fafaf8'>
              <td style='padding:10px 16px;color:#8b7355;font-family:Arial,sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:.08em;white-space:nowrap'>Hora</td>
              <td style='padding:10px 16px;color:#0d2b45;font-size:15px'>{$data['hora']} h</td>
            </tr>
            <tr style='border-bottom:1px solid #e8e4dd'>
              <td style='padding:10px 16px;color:#8b7355;font-family:Arial,sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:.08em;white-space:nowrap'>Personas</td>
              <td style='padding:10px 16px;color:#0d2b45;font-size:15px'>{$data['personas']}</td>
            </tr>
            {$obsRow}
          </table>
        </td>
      </tr>

      <!-- Cancellation policy -->
      <tr>
        <td style='background:#ffffff;padding:0 40px 32px'>
          <table width='100%' cellpadding='0' cellspacing='0'
                 style='background:#fdf9f0;border-left:3px solid #c9a84c;border-radius:0 4px 4px 0;padding:0'>
            <tr>
              <td style='padding:16px 20px'>
                <p style='margin:0 0 6px;color:#c9a84c;font-family:Arial,sans-serif;font-size:11px;
                           text-transform:uppercase;letter-spacing:.12em;font-weight:600'>
                  Política de cancelación
                </p>
                <p style='margin:0;color:#555;font-family:Arial,sans-serif;font-size:13px;line-height:1.65'>
                  Puedes cancelar tu reserva sin coste hasta <strong>2 horas antes</strong> de la hora
                  reservada por cualquier medio (teléfono, email o respondiendo a este correo).
                  Cancelaciones con menos de 2 horas de antelación deben realizarse
                  <strong>exclusivamente por teléfono</strong>.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- Contact -->
      <tr>
        <td style='background:#ffffff;padding:0 40px 40px;text-align:center'>
          <div style='width:48px;height:1px;background:#e8e4dd;margin:0 auto 24px'></div>
          <p style='margin:0 0 4px;color:#0d2b45;font-size:15px'>¿Necesitas modificar tu reserva?</p>
          <p style='margin:0;font-family:Arial,sans-serif;font-size:13px;color:#8b7355'>
            Llámanos al
            <a href='tel:+34644026066' style='color:#c9a84c;text-decoration:none;font-weight:600'>
              +34 644 026 066
            </a>
            &nbsp;·&nbsp;
            <a href='mailto:info@portadirta.com' style='color:#c9a84c;text-decoration:none'>
              info@portadirta.com
            </a>
          </p>
        </td>
      </tr>

      <!-- Footer -->
      <tr>
        <td align='center' style='background:#0d2b45;padding:28px 32px'>
          <p style='margin:0 0 8px;color:rgba(255,255,255,.5);font-family:Arial,sans-serif;
                    font-size:12px;letter-spacing:.04em'>
            Restaurante Porta D'irta &nbsp;·&nbsp; Camí del Pebret, s/n &nbsp;·&nbsp; 12598 Peñíscola, Castellón
          </p>
          <p style='margin:0;color:rgba(255,255,255,.3);font-family:Arial,sans-serif;font-size:11px'>
            <a href='https://portadirta.com' style='color:#c9a84c;text-decoration:none'>portadirta.com</a>
          </p>
        </td>
      </tr>

    </table>
    </td></tr>
  </table>

</body>
</html>";

    Mail::html(
        $html,
        fn ($m) => $m->to($data['email'])
                     ->subject("Reserva confirmada — {$dateDisplay} · Porta D'irta")
    );

    return response()->json([
        'success' => true,
        'message' => 'Reserva creada correctamente.',
    ], 201);
});

// Shared auth check for internal endpoints
$internalAuth = function ($request) {
    if ($request->header('X-Internal-Token') !== 'portadirta-n8n-2026') {
        return response()->json(['error' => 'Unauthorized'], 401);
    }
    return null;
};

/**
 * POST /api/internal/beds24/calendar
 * Proxy for Beds24 v2 calendar API — accepts a flat JSON object and forwards
 * as the nested array structure Beds24 requires. n8n HTTP Request node cannot
 * send a raw JSON array body; PHP proxy builds the correct structure via curl.
 *
 * Body: { roomId, from, to, token, price1? (updatePrice), available? (blockRoom) }
 */
Route::post('internal/beds24/calendar', function (Request $request) use ($internalAuth) {
    if ($err = $internalAuth($request)) return $err;

    $data = $request->validate([
        'roomId'    => 'required|integer',
        'from'      => 'required|string|max:10',
        'to'        => 'required|string|max:10',
        'token'     => 'required|string',
        'price1'    => 'nullable|integer',
        'available' => 'nullable|integer',
    ]);

    $calendar = ['from' => $data['from'], 'to' => $data['to']];
    if (isset($data['price1']))    $calendar['price1']    = $data['price1'];
    if (isset($data['available'])) $calendar['available'] = $data['available'];

    $payload = json_encode([['roomId' => $data['roomId'], 'calendar' => [$calendar]]]);

    $ch = curl_init('https://beds24.com/api/v2/inventory/rooms/calendar');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => $payload,
        CURLOPT_HTTPHEADER     => [
            'token: ' . $data['token'],
            'Content-Type: application/json',
            'Content-Length: ' . strlen($payload),
        ],
        CURLOPT_TIMEOUT        => 15,
    ]);
    $body   = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $decoded = json_decode($body, true);
    return response()->json($decoded ?? ['error' => 'Invalid Beds24 response', 'raw' => $body], $status ?: 500);
});

// GET /api/internal/reservations?date=YYYY-MM-DD  (or ?startDate=&endDate=)
Route::get('internal/reservations', function (Request $request) use ($internalAuth) {
    if ($err = $internalAuth($request)) return $err;
    $q = DB::table('reservations');
    if ($request->date) {
        $q->whereDate('reserve_date', $request->date);
    } elseif ($request->startDate) {
        $q->whereBetween('reserve_date', [$request->startDate, $request->endDate ?? $request->startDate]);
    }
    $rows = $q->orderBy('reserve_date')->orderBy('reserve_time')->get();
    return response()->json(['success' => true, 'count' => $rows->count(), 'data' => $rows]);
});

// GET /api/internal/availability?date=YYYY-MM-DD&guests=N
Route::get('internal/availability', function (Request $request) use ($internalAuth) {
    if ($err = $internalAuth($request)) return $err;
    $date     = $request->date ?? now()->format('Y-m-d');
    $guests   = (int)($request->guests ?? 2);
    $count    = DB::table('reservations')->whereDate('reserve_date', $date)->sum('guest_num');
    $capacity = 75;
    return response()->json([
        'success'     => true,
        'date'        => $date,
        'available'   => ($count + $guests) <= $capacity,
        'bookedSeats' => $count,
        'capacity'    => $capacity,
    ]);
});

/**
 * POST /api/internal/daily-summary
 * Arrivals + departures from Beds24 + restaurant reservations for a given date.
 * Body: { date: "YYYY-MM-DD", token: "<beds24_access_token>" }
 */
Route::post('internal/daily-summary', function (Request $request) use ($internalAuth) {
    if ($err = $internalAuth($request)) return $err;

    $data = $request->validate([
        'date'  => 'required|string|max:10',
        'token' => 'required|string',
    ]);
    $date  = $data['date'];
    $token = $data['token'];

    $roomNames  = [662792 => 'Torre Badum', 662793 => 'Cala El Pebret', 662794 => 'Cala Aljub', 662795 => 'Ermita Sant Antoni'];
    $channelMap = ['bookingdotcom' => 'Booking.com', 'airbnb' => 'Airbnb', 'direct' => 'Directo'];

    // Fetch all bookings for property (Beds24 V2 doesn't reliably filter by arrival/departure via query param)
    $ch = curl_init('https://beds24.com/api/v2/bookings?propId=318433');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => ["token: $token", 'Accept: application/json'],
        CURLOPT_TIMEOUT        => 20,
    ]);
    $bookings = json_decode(curl_exec($ch), true)['data'] ?? [];
    curl_close($ch);

    $fmt = function ($b) use ($roomNames, $channelMap) {
        return [
            'id'         => $b['id'] ?? null,
            'name'       => trim(($b['firstName'] ?? '') . ' ' . ($b['lastName'] ?? '')) ?: '(sin nombre)',
            'room'       => $roomNames[$b['roomId'] ?? 0] ?? 'Hab.' . ($b['roomId'] ?? '?'),
            'roomId'     => $b['roomId'] ?? null,
            'arrival'    => $b['arrival'] ?? '',
            'departure'  => $b['departure'] ?? '',
            'numAdult'   => $b['numAdult'] ?? 0,
            'numChild'   => $b['numChild'] ?? 0,
            'channel'    => $channelMap[$b['channel'] ?? ''] ?? ($b['channel'] ?? 'Directo'),
            'price'      => $b['price'] ?? 0,
            'status'     => $b['status'] ?? '',
        ];
    };

    $arrivals        = array_values(array_filter($bookings, fn ($b) => ($b['arrival']   ?? '') === $date));
    $departures      = array_values(array_filter($bookings, fn ($b) => ($b['departure'] ?? '') === $date));
    $currentlyStaying = array_values(array_filter($bookings, fn ($b) =>
        ($b['arrival'] ?? '') <= $date && ($b['departure'] ?? '') > $date
    ));

    $restaurantResos = DB::table('reservations')
        ->whereDate('reserve_date', $date)
        ->orderBy('reserve_time')
        ->get()
        ->map(fn ($r) => [
            'id'      => $r->reservation_id,
            'name'    => trim($r->first_name . ' ' . $r->last_name),
            'time'    => $r->reserve_time,
            'guests'  => $r->guest_num,
            'phone'   => $r->telephone  ?? '',
            'comment' => $r->comment    ?? '',
        ])->toArray();

    return response()->json([
        'success'               => true,
        'date'                  => $date,
        'arrivals'              => array_map($fmt, $arrivals),
        'departures'            => array_map($fmt, $departures),
        'currentlyStaying'      => array_map($fmt, $currentlyStaying),
        'restaurantReservations'=> $restaurantResos,
    ]);
});

/**
 * POST /api/internal/guest-info
 * Who is staying in a specific room on a given date + upcoming.
 * Body: { roomId: 662792, date?: "YYYY-MM-DD", token: "<beds24_token>" }
 */
Route::post('internal/guest-info', function (Request $request) use ($internalAuth) {
    if ($err = $internalAuth($request)) return $err;

    $data = $request->validate([
        'roomId' => 'required|integer',
        'date'   => 'nullable|string|max:10',
        'token'  => 'required|string',
    ]);
    $roomId = $data['roomId'];
    $date   = $data['date'] ?? now()->format('Y-m-d');
    $token  = $data['token'];

    $roomNames = [662792 => 'Torre Badum', 662793 => 'Cala El Pebret', 662794 => 'Cala Aljub', 662795 => 'Ermita Sant Antoni'];

    $ch = curl_init("https://beds24.com/api/v2/bookings?propId=318433&roomId={$roomId}");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => ["token: $token", 'Accept: application/json'],
        CURLOPT_TIMEOUT        => 15,
    ]);
    $bookings = json_decode(curl_exec($ch), true)['data'] ?? [];
    curl_close($ch);

    $fmtGuest = fn ($b) => [
        'name'      => trim(($b['firstName'] ?? '') . ' ' . ($b['lastName'] ?? '')) ?: '(sin nombre)',
        'arrival'   => $b['arrival']   ?? '',
        'departure' => $b['departure'] ?? '',
        'numAdult'  => $b['numAdult']  ?? 0,
        'numChild'  => $b['numChild']  ?? 0,
        'channel'   => $b['channel']   ?? 'direct',
        'email'     => $b['email']     ?? '',
    ];

    $current = array_values(array_filter($bookings, fn ($b) =>
        ($b['arrival'] ?? '') <= $date && ($b['departure'] ?? '') > $date
    ));

    $nextWeek = date('Y-m-d', strtotime($date . ' +7 days'));
    $upcoming = array_values(array_filter($bookings, fn ($b) =>
        ($b['arrival'] ?? '') > $date && ($b['arrival'] ?? '') <= $nextWeek
    ));

    return response()->json([
        'success'       => true,
        'roomId'        => $roomId,
        'roomName'      => $roomNames[$roomId] ?? 'Habitación ' . $roomId,
        'date'          => $date,
        'currentGuest'  => $current ? $fmtGuest($current[0]) : null,
        'upcoming'      => array_map($fmtGuest, array_slice($upcoming, 0, 3)),
    ]);
});

/**
 * POST /api/internal/reservations/cancel
 * Cancels the next upcoming restaurant reservation matching a guest name.
 * Body: { name: "Apellido", date?: "YYYY-MM-DD" }
 */
Route::post('internal/reservations/cancel', function (Request $request) use ($internalAuth) {
    if ($err = $internalAuth($request)) return $err;

    $data = $request->validate([
        'name' => 'required|string|max:200',
        'date' => 'nullable|string|max:10',
    ]);

    $q = DB::table('reservations')
        ->where(function ($query) use ($data) {
            $query->where('first_name', 'LIKE', '%' . $data['name'] . '%')
                  ->orWhere('last_name',  'LIKE', '%' . $data['name'] . '%');
        });

    if (!empty($data['date'])) {
        $q->whereDate('reserve_date', $data['date']);
    } else {
        $q->where('reserve_date', '>=', now()->format('Y-m-d'));
    }

    $reso = $q->orderBy('reserve_date', 'asc')->first();

    if (!$reso) {
        return response()->json([
            'success' => false,
            'error'   => "No se encontró ninguna reserva próxima para \"{$data['name']}\".",
        ], 404);
    }

    DB::table('reservations')->where('reservation_id', $reso->reservation_id)->delete();

    return response()->json([
        'success'   => true,
        'cancelled' => [
            'id'     => $reso->reservation_id,
            'name'   => trim($reso->first_name . ' ' . $reso->last_name),
            'date'   => $reso->reserve_date,
            'time'   => $reso->reserve_time,
            'guests' => $reso->guest_num,
        ],
    ]);
});

/**
 * Public experience inquiry endpoint — no auth required.
 * Called from the /experiencias contact form.
 */
Route::post('public/contact', function (Request $request) {
    $data = $request->validate([
        'nombre'      => 'required|string|max:200',
        'email'       => 'required|email|max:200',
        'telefono'    => 'nullable|string|max:30',
        'experiencia' => 'nullable|string|max:100',
        'fecha'       => 'nullable|string|max:30',
        'personas'    => 'nullable|integer|min:1|max:50',
        'mensaje'     => 'nullable|string|max:2000',
    ]);

    $exp     = $data['experiencia'] ?? '—';
    $tel     = $data['telefono'] ?? '—';
    $fecha   = $data['fecha'] ?? '—';
    $pers    = isset($data['personas']) ? (int)$data['personas'] : '—';
    $msg     = isset($data['mensaje']) ? htmlspecialchars($data['mensaje']) : '—';

    Mail::html(
        "<p>Nueva consulta de experiencia recibida:</p>
         <table cellpadding='6' style='border-collapse:collapse;font-family:sans-serif;font-size:14px'>
           <tr><td><strong>Nombre</strong></td><td>{$data['nombre']}</td></tr>
           <tr><td><strong>Email</strong></td><td>{$data['email']}</td></tr>
           <tr><td><strong>Teléfono</strong></td><td>{$tel}</td></tr>
           <tr><td><strong>Experiencia</strong></td><td>{$exp}</td></tr>
           <tr><td><strong>Fecha llegada</strong></td><td>{$fecha}</td></tr>
           <tr><td><strong>Personas</strong></td><td>{$pers}</td></tr>
           <tr><td><strong>Mensaje</strong></td><td>{$msg}</td></tr>
         </table>",
        fn ($m) => $m->to('info@portadirta.com')
                     ->subject("✨ Consulta experiencia — {$data['nombre']} · {$exp}")
    );

    return response()->json([
        'success' => true,
        'message' => 'Consulta recibida correctamente.',
    ], 201);
});

/**
 * POST /api/internal/menu/carta
 * POST /api/internal/menu/menu
 * POST /api/internal/menu/bebidas
 *
 * Receives a parsed JSON menu object from n8n and writes it to the shared
 * Docker volume so that the Astro SSR frontend can read it on each request.
 *
 * Body: the full menu JSON (validated against each schema).
 * Auth: X-Internal-Token header (same shared secret as all internal endpoints).
 *
 * Volume path is set via MENU_DATA_PATH env var; falls back to /var/www/data.
 */
foreach (['carta', 'menu', 'bebidas'] as $menuType) {
    Route::post("internal/menu/{$menuType}", function (Request $request) use ($internalAuth, $menuType) {
        if ($err = $internalAuth($request)) return $err;

        $body = $request->getContent();
        if (empty($body)) {
            return response()->json(['error' => 'Empty body'], 400);
        }

        $decoded = json_decode($body, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            return response()->json(['error' => 'Invalid JSON: ' . json_last_error_msg()], 400);
        }

        // Basic schema sanity checks per menu type
        if ($menuType === 'carta' || $menuType === 'bebidas') {
            if (empty($decoded['sections']) || !is_array($decoded['sections'])) {
                return response()->json(['error' => "Field 'sections' is required and must be an array"], 422);
            }
        } elseif ($menuType === 'menu') {
            if (!isset($decoded['price']) || empty($decoded['sections'])) {
                return response()->json(['error' => "Fields 'price' and 'sections' are required for menu"], 422);
            }
        }

        $dataPath = getenv('MENU_DATA_PATH') ?: '/var/www/data';
        if (!is_dir($dataPath)) {
            if (!mkdir($dataPath, 0755, true)) {
                return response()->json(['error' => "Cannot create data directory: {$dataPath}"], 500);
            }
        }

        $filePath = "{$dataPath}/{$menuType}.json";
        $written  = file_put_contents($filePath, json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        if ($written === false) {
            return response()->json(['error' => "Failed to write {$menuType}.json to {$filePath}"], 500);
        }

        return response()->json([
            'success'  => true,
            'file'     => $filePath,
            'bytes'    => $written,
            'updated'  => $decoded['updated'] ?? date('Y-m-d'),
        ], 200);
    });
}
