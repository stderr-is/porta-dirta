/**
 * config.ts — Central configuration for Porta D'irta integrations
 *
 * Replace every REPLACE_WITH_* value with real credentials before deploying.
 * Do NOT commit real tokens to version control.
 */

export const CONFIG = {
  beds24: {
    token: 'REPLACE_WITH_BEDS24_TOKEN',
    propertyId: 'REPLACE_WITH_PROPERTY_ID',
    widgetUrl: 'https://beds24.com/booking2.php?propid=REPLACE_WITH_PROPERTY_ID',
  },
  tastyigniter: {
    baseUrl: 'REPLACE_WITH_TASTYIGNITER_URL',
    apiKey: 'REPLACE_WITH_TASTYIGNITER_API_KEY',
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
