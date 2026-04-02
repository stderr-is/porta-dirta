/**
 * i18n-client.ts — Client-side dynamic translation engine
 *
 * Imported by Layout.astro (Vite bundles it once, browser caches it).
 * Exposes window.setLang(code) and window.__i18n (full translations).
 *
 * Each translated element carries a data-i18n="section.key" attribute.
 * Attribute translations use data-i18n-alt, data-i18n-placeholder,
 * data-i18n-aria-label.  Page title/desc keys live on <html>.
 *
 * Language preference is stored in localStorage under 'porta-lang'.
 * A 'langchange' CustomEvent is fired so sub-components can react.
 */

import { translations } from '../i18n/translations';

type FlatDict = Record<string, string>;

const VALID_LANGS = new Set(['es', 'en', 'fr', 'de']);

/** Flatten a nested object into 'section.key' → value pairs */
function flatten(obj: Record<string, unknown>, prefix = ''): FlatDict {
  const out: FlatDict = {};
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (v !== null && typeof v === 'object' && !Array.isArray(v)) {
      Object.assign(out, flatten(v as Record<string, unknown>, key));
    } else {
      // Store arrays as JSON so calendar month/day arrays work via flat lookup
      out[key] = Array.isArray(v) ? JSON.stringify(v) : String(v ?? '');
    }
  }
  return out;
}

const flatMap: Record<string, FlatDict> = {};
for (const lang of Object.keys(translations)) {
  flatMap[lang] = flatten(translations[lang as keyof typeof translations] as Record<string, unknown>);
}

// Expose the raw nested translations for components that need arrays (calendar)
(window as Window & { __i18n: typeof translations }).__i18n = translations;

function applyLang(lang: string): void {
  const dict = flatMap[lang] ?? flatMap['es'];

  // Text content
  document.querySelectorAll<HTMLElement>('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n')!;
    if (key in dict) el.textContent = dict[key];
  });

  // alt attributes
  document.querySelectorAll<HTMLElement>('[data-i18n-alt]').forEach(el => {
    const key = el.getAttribute('data-i18n-alt')!;
    if (key in dict) el.setAttribute('alt', dict[key]);
  });

  // placeholder attributes
  document.querySelectorAll<HTMLElement>('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder')!;
    if (key in dict) el.setAttribute('placeholder', dict[key]);
  });

  // aria-label attributes
  document.querySelectorAll<HTMLElement>('[data-i18n-aria-label]').forEach(el => {
    const key = el.getAttribute('data-i18n-aria-label')!;
    if (key in dict) el.setAttribute('aria-label', dict[key]);
  });

  // <title> — key lives on <html data-i18n-title="section.meta_title">
  const titleKey = document.documentElement.getAttribute('data-i18n-title');
  if (titleKey && dict[titleKey]) {
    document.title = `${dict[titleKey]} | Porta D'irta`;
  }

  // <meta name="description">
  const descKey = document.documentElement.getAttribute('data-i18n-desc');
  const metaDesc = document.querySelector<HTMLMetaElement>('meta[name="description"]');
  if (descKey && dict[descKey] && metaDesc) {
    metaDesc.setAttribute('content', dict[descKey]);
  }

  // html[lang]
  document.documentElement.lang = lang;

  // Nav language buttons — toggle active/inactive visual state
  document.querySelectorAll<HTMLElement>('[data-lang-btn]').forEach(btn => {
    const isActive = btn.getAttribute('data-lang-btn') === lang;
    btn.classList.toggle('font-semibold', isActive);
    btn.classList.toggle('text-brand-gold', isActive);
    btn.classList.toggle('text-white/70', !isActive);
    btn.classList.toggle('text-white/60', !isActive);
    btn.classList.toggle('text-white', !isActive && !btn.classList.contains('text-white/70'));
  });

  // Compact dropdown summary — update visible language code
  const summaryText = document.getElementById('lang-summary-current');
  if (summaryText) summaryText.textContent = lang.toUpperCase();

  // Reveal page if it was hidden by the early inline FOUC-prevention script
  document.documentElement.style.visibility = '';

  // Notify sub-components (e.g. BookingSearchForm calendar)
  document.dispatchEvent(new CustomEvent('langchange', { detail: { lang } }));
}

export function setLang(lang: string): void {
  // Guard against invalid or corrupted locale values
  if (!VALID_LANGS.has(lang)) {
    if (import.meta.env.DEV) console.warn(`[i18n] setLang called with unknown locale: "${lang}"`);
    return;
  }
  localStorage.setItem('porta-lang', lang);
  applyLang(lang);
}

// Expose globally so Nav inline onclick="" can call it
(window as Window & { setLang: typeof setLang }).setLang = setLang;

// Read and validate saved preference; clear any corrupted value
let rawSaved: string | null = null;
try { rawSaved = localStorage.getItem('porta-lang'); } catch (_) { /* storage blocked */ }
const saved = (rawSaved && VALID_LANGS.has(rawSaved)) ? rawSaved : 'es';
if (rawSaved && !VALID_LANGS.has(rawSaved)) {
  // Corrupted value — clear it so future loads use the default
  try { localStorage.removeItem('porta-lang'); } catch (_) {}
}

// Always apply the current language (even 'es') so:
//  • button highlight state is always correct
//  • the FOUC visibility:hidden set by the early inline script is always lifted
applyLang(saved);
