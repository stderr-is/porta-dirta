import { translations, type Locale } from './translations';
import type { TranslationNode, TranslationValue } from '../types/i18n';

export const locales = ['es', 'en', 'fr', 'de'] as const;
export const defaultLocale: Locale = 'es';

export function getLangFromUrl(url: URL): Locale {
  const [, lang] = url.pathname.split('/');
  if ((locales as readonly string[]).includes(lang)) return lang as Locale;
  return defaultLocale;
}

export function useTranslations(lang: Locale) {
  function t(key: string): string | TranslationValue;
  function t(
    key: string,
    options: { returnObjects: true },
  ): TranslationValue;
  function t(
    key: string,
    options?: { returnObjects?: boolean },
  ): string | TranslationValue {
    const keys = key.split('.');
    let result: TranslationValue =
      (translations[lang] ?? translations[defaultLocale]) as TranslationNode;
    for (const k of keys) {
      if (!result || typeof result !== 'object' || Array.isArray(result)) {
        result = undefined;
        break;
      }
      result = (result as TranslationNode)[k];
    }
    // Fallback to Spanish if key missing in target locale
    if (result === undefined) {
      let fallback: TranslationValue = translations[defaultLocale] as TranslationNode;
      for (const k of keys) {
        if (!fallback || typeof fallback !== 'object' || Array.isArray(fallback)) {
          fallback = undefined;
          break;
        }
        fallback = (fallback as TranslationNode)[k];
      }
      if (options?.returnObjects) return fallback ?? key;
      return fallback ?? key;
    }
    if (options?.returnObjects) return result;
    return result;
  };
  return t;
}
