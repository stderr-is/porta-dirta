import { translations, type Locale } from './translations';

export const defaultLocale: Locale = 'es';

/**
 * Returns a build-time translation function for the default locale (Spanish).
 * All pages render Spanish HTML at build time; client-side swapping is handled
 * by src/scripts/i18n-client.ts using data-i18n attributes.
 */
export function useTranslations(lang: Locale = defaultLocale) {
  return function t(key: string): string {
    const keys = key.split('.');
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let result: any = translations[lang] ?? translations[defaultLocale];
    for (const k of keys) {
      result = result?.[k];
    }
    if (result === undefined) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let fallback: any = translations[defaultLocale];
      for (const k of keys) fallback = fallback?.[k];
      return fallback ?? key;
    }
    return result;
  };
}
