export interface HiEventProduct {
  price: number | null;
}

export interface HiEventCategory {
  products?: HiEventProduct[] | null;
}

export interface HiEventImage {
  url: string;
}

export interface HiEvent {
  id: number;
  title: string;
  slug: string;
  status?: string;
  description_preview?: string | null;
  start_date: string;
  lifecycle_status?: 'UPCOMING' | 'PAST' | 'ENDED' | null;
  product_categories?: HiEventCategory[] | null;
  images?: HiEventImage[] | null;
}

export interface HiEventPackage {
  id: number;
  title: string;
  slug: string;
  description_preview: string;
  start_date: string;
  lifecycle_status: 'UPCOMING' | 'PAST' | 'ENDED';
  cover_url: string | null;
  price: number | null;
  booking_url: string;
}
