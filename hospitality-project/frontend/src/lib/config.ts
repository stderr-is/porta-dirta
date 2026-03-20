/**
 * config.ts — Central configuration for Porta D'irta integrations
 *
 * Replace every REPLACE_WITH_* value with real credentials before deploying.
 * Do NOT commit real tokens to version control.
 */

export const CONFIG = {
  beds24: {
    token: import.meta.env.BEDS24_API_KEY,
    propertyId: import.meta.env.BEDS24_PROP_ID ?? '318433',
    widgetUrl: 'https://media.xmlcal.com/widget/1.01/js/bookWidget.min.js',
  },
  tastyigniter: {
    baseUrl: import.meta.env.PUBLIC_TASTYIGNITER_URL ?? 'http://localhost:8081',
  },
  n8n: {
    restaurantWebhook: 'REPLACE_WITH_N8N_WEBHOOK_URL',
    contactWebhook: 'REPLACE_WITH_N8N_WEBHOOK_URL',
    eventsWebhook: 'REPLACE_WITH_N8N_WEBHOOK_URL',
    experienciasWebhook: 'REPLACE_WITH_N8N_WEBHOOK_URL',
  },
  hievents: {
    baseUrl: 'REPLACE_WITH_HIEVENTS_URL',
  },
} as const;
