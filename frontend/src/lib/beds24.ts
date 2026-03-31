/**
 * beds24.ts — Beds24 API V2 client for Porta D'irta
 *
 * Base URL: https://beds24.com/api/v2
 *
 * RATE LIMIT WARNING: Beds24 API V2 allows only 1 concurrent request per token.
 * Do NOT fire parallel requests. If you need to fetch multiple resources,
 * chain them sequentially. On 429 responses, apply exponential backoff:
 *   wait = Math.min(initialDelay * 2^attempt, maxDelay)
 * Recommended initial delay: 500ms, max delay: 30s, max retries: 5.
 */

// Reserved for future SSR use — not imported by any page in SSG mode.
// Token comes from env var set in docker-compose.yml (Hostinger) or Cloudflare Pages env vars.
export const BEDS24_API_TOKEN = import.meta.env.BEDS24_API_KEY ?? '';
export const BEDS24_PROPERTY_ID = import.meta.env.BEDS24_PROP_ID ?? '318433';

const BASE_URL = 'https://beds24.com/api/v2';

// ─── TypeScript interfaces ────────────────────────────────────────────────────

/** A single room/unit as returned by the Beds24 API V2 */
export interface Room {
  /** Beds24 internal room ID */
  id: string;
  /** Display name of the room */
  name: string;
  /** Maximum number of guests the room can accommodate */
  maxPersons: number;
  /** Long-form room description */
  description: string;
  /** Array of image URLs associated with this room */
  images: string[];
  /** List of amenity labels (e.g. "WiFi", "Air conditioning") */
  amenities: string[];
  /** Property/unit type code from Beds24 */
  unitType?: string;
  /** Number of bedrooms */
  bedrooms?: number;
  /** Floor area in m² */
  floorArea?: number;
}

/** Pricing details for a room over a specific date range */
export interface Pricing {
  /** Beds24 room ID this pricing applies to */
  roomId: string;
  /** ISO date string: check-in date */
  checkIn: string;
  /** ISO date string: check-out date */
  checkOut: string;
  /** Total price for the stay (all nights combined) */
  totalPrice: number;
  /** Price per night (average if rates vary) */
  pricePerNight: number;
  /** Currency code, e.g. "EUR" */
  currency: string;
  /** Whether the room is available for the requested dates */
  available: boolean;
  /** Minimum stay in nights (if applicable) */
  minStay?: number;
  /** Breakdown of nightly rates, keyed by ISO date string */
  nightlyRates?: Record<string, number>;
}

/** Payload for creating a new booking inquiry */
export interface BookingInquiry {
  /** Beds24 room ID being requested */
  roomId: string;
  /** ISO date string: desired check-in date (YYYY-MM-DD) */
  checkIn: string;
  /** ISO date string: desired check-out date (YYYY-MM-DD) */
  checkOut: string;
  /** Number of adult guests */
  numAdults: number;
  /** Number of child guests */
  numChildren?: number;
  /** Guest's first name */
  firstName: string;
  /** Guest's last name */
  lastName: string;
  /** Guest's email address */
  email: string;
  /** Guest's phone number (optional) */
  phone?: string;
  /** Free-text notes or special requests */
  notes?: string;
}

/** Property-level information returned by Beds24 */
export interface PropertyInfo {
  /** Beds24 property ID */
  id: string;
  /** Property display name */
  name: string;
  /** Street address */
  address: string;
  /** City */
  city: string;
  /** Country code (ISO 3166-1 alpha-2) */
  country: string;
  /** Property description */
  description: string;
  /** Primary contact email */
  email?: string;
  /** Primary contact phone */
  phone?: string;
  /** Latitude coordinate */
  lat?: number;
  /** Longitude coordinate */
  lng?: number;
  /** Array of property-level image URLs */
  images: string[];
}

// ─── Internal helpers ─────────────────────────────────────────────────────────

/**
 * Build the standard Beds24 API V2 Authorization header.
 * NOTE: Beds24 API V2 uses a custom 'token' header, NOT 'Authorization: Bearer'.
 */
function authHeader(): HeadersInit {
  return {
    'token': BEDS24_API_TOKEN,
    'Content-Type': 'application/json',
  };
}

/**
 * Generic fetch wrapper with exponential backoff on 429 (rate limit) responses.
 * Beds24 API V2 allows only 1 concurrent request per token — this handles the
 * case where a previous request is still in flight when we fire the next one.
 *
 * Backoff: 500ms → 1s → 2s → 4s → 8s (max 30s cap, 5 retries).
 */
async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const mergedOptions: RequestInit = {
    ...options,
    headers: {
      ...authHeader(),
      ...(options.headers ?? {}),
    },
  };

  const MAX_RETRIES = 5;
  const INITIAL_DELAY_MS = 500;
  const MAX_DELAY_MS = 30_000;

  let attempt = 0;
  while (true) {
    const response = await fetch(url, mergedOptions);

    if (response.status === 429 && attempt < MAX_RETRIES) {
      const delay = Math.min(INITIAL_DELAY_MS * Math.pow(2, attempt), MAX_DELAY_MS);
      console.warn(`[beds24] Rate limited on ${path}. Retry ${attempt + 1}/${MAX_RETRIES} in ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
      attempt++;
      continue;
    }

    if (!response.ok) {
      const body = await response.text().catch(() => '');
      throw new Error(`Beds24 API error ${response.status} on ${path}: ${body}`);
    }

    return response.json() as Promise<T>;
  }
}

// ─── Public API functions ─────────────────────────────────────────────────────

/**
 * Get room availability for a date range.
 *
 * Calls: GET /inventory/rooms/availability
 * Query params: propertyId, checkIn, checkOut
 *
 * Returns only rooms that have at least one available unit for the full
 * requested period.
 *
 * @param checkIn  - Check-in date in YYYY-MM-DD format
 * @param checkOut - Check-out date in YYYY-MM-DD format
 */
export async function getRoomAvailability(
  checkIn: string,
  checkOut: string
): Promise<Room[]> {
  const params = new URLSearchParams({
    propertyId: BEDS24_PROPERTY_ID,
    checkIn,
    checkOut,
  });

  const data = await apiFetch<{ rooms: Room[] }>(
    `/inventory/rooms/availability?${params}`
  );

  return data.rooms ?? [];
}

/**
 * Get all rooms for the property with their full details.
 *
 * Calls: GET /inventory/rooms
 * Query params: propertyId
 *
 * Returns the complete room catalogue including descriptions, images,
 * amenities, and capacity — regardless of availability.
 */
export async function getRooms(): Promise<Room[]> {
  const params = new URLSearchParams({ propertyId: BEDS24_PROPERTY_ID });

  const data = await apiFetch<{ rooms: Room[] }>(
    `/inventory/rooms?${params}`
  );

  return data.rooms ?? [];
}

/**
 * Get pricing for a specific room over a date range.
 *
 * Calls: GET /inventory/rooms/prices
 * Query params: propertyId, roomId, checkIn, checkOut
 *
 * Returns a Pricing object with total cost, nightly breakdown, and
 * availability status. Use this to show the user real-time rates before
 * they complete a booking inquiry.
 *
 * @param roomId   - Beds24 internal room ID
 * @param checkIn  - Check-in date in YYYY-MM-DD format
 * @param checkOut - Check-out date in YYYY-MM-DD format
 */
export async function getRoomPricing(
  roomId: string,
  checkIn: string,
  checkOut: string
): Promise<Pricing> {
  const params = new URLSearchParams({
    propertyId: BEDS24_PROPERTY_ID,
    roomId,
    checkIn,
    checkOut,
  });

  const data = await apiFetch<Pricing>(
    `/inventory/rooms/prices?${params}`
  );

  return data;
}

/**
 * Create a booking inquiry (NOT a confirmed booking).
 *
 * Calls: POST /bookings
 *
 * Submits the guest's details and preferred dates to Beds24 as an inquiry.
 * The property team will manually review and confirm within 24 hours.
 * This does NOT charge the guest or guarantee availability.
 *
 * On success, Beds24 returns a booking reference ID that can be shown to
 * the guest as a confirmation number for their inquiry.
 *
 * @param inquiry - Guest details and requested stay
 */
export async function createBookingInquiry(
  inquiry: BookingInquiry
): Promise<{ success: boolean; bookingId?: string }> {
  const payload = {
    propertyId: BEDS24_PROPERTY_ID,
    roomId: inquiry.roomId,
    arrival: inquiry.checkIn,
    departure: inquiry.checkOut,
    numAdult: inquiry.numAdults,
    numChild: inquiry.numChildren ?? 0,
    firstName: inquiry.firstName,
    lastName: inquiry.lastName,
    email: inquiry.email,
    phone: inquiry.phone ?? '',
    notes: inquiry.notes ?? '',
    // status 0 = inquiry (not confirmed) in Beds24 API V2
    status: 0,
  };

  try {
    const data = await apiFetch<{ bookingId?: string; id?: string }>(
      '/bookings',
      {
        method: 'POST',
        body: JSON.stringify(payload),
      }
    );

    const bookingId = data.bookingId ?? data.id;
    return { success: true, bookingId };
  } catch (err) {
    console.error('[beds24] createBookingInquiry failed:', err);
    return { success: false };
  }
}

/**
 * Get property-level information for Porta D'irta.
 *
 * Calls: GET /properties/{propertyId}
 *
 * Returns address, contact details, description, coordinates, and
 * property-level images. Useful for the "About" section and SEO metadata.
 */
export async function getPropertyInfo(): Promise<PropertyInfo> {
  const data = await apiFetch<PropertyInfo>(
    `/properties/${BEDS24_PROPERTY_ID}`
  );

  return data;
}
