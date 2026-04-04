export interface MenuTranslationItem {
  name?: string;
  description?: string;
}

export interface MenuTranslationSection {
  name?: string;
  note?: string;
  items?: MenuTranslationItem[];
}

export interface MenuTranslationData {
  name?: string;
  priceNote?: string;
  available?: string;
  sections?: MenuTranslationSection[];
}

export interface MenuItem {
  name: string;
  description?: string;
  allergens?: string[];
  unit?: string;
  price: number;
  supplement?: number;
}

export interface MenuSection {
  name: string;
  note?: string;
  items: MenuItem[];
}

export interface DynamicMenuData {
  sections: MenuSection[];
  translations?: Record<string, MenuTranslationData | undefined>;
  updated: string;
}

export interface FixedPriceMenuData extends DynamicMenuData {
  name: string;
  price: number;
  priceNote: string;
  available: string;
}
