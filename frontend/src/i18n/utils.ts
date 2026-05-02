import { translations, type Locale } from './translations';

export const locales = ['es', 'en', 'fr', 'de'] as const;
export const defaultLocale: Locale = 'es';

export function getLangFromUrl(url: URL): Locale {
  const [, lang] = url.pathname.split('/');
  if ((locales as readonly string[]).includes(lang)) return lang as Locale;
  return defaultLocale;
}

export function useTranslations(lang: Locale) {
  return function t(key: string): string {
    const keys = key.split('.');
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let result: any = translations[lang] ?? translations[defaultLocale];
    for (const k of keys) {
      result = result?.[k];
    }
    // Fallback to Spanish if key missing in target locale
    if (result === undefined) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let fallback: any = translations[defaultLocale];
      for (const k of keys) fallback = fallback?.[k];
      return fallback ?? key;
    }
    return result;
  };
}
