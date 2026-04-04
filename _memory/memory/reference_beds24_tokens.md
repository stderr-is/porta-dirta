---
name: Beds24 API tokens and room IDs
description: Beds24 API V2 refresh token, room IDs, and how to get an access token
type: reference
---

## Property
- **Prop ID:** 318433

## Room IDs
| ID | Name |
|---|---|
| 662792 | Torre Badum |
| 662793 | Cala El Pebret |
| 662794 | Cala Aljub |
| 662795 | Ermita Sant Antoni |

## V1 credentials
- API key: `${BEDS24_V1_API_KEY}` (stored in local `.env`, never commit real value)
- Prop key: `${BEDS24_V1_PROP_KEY}` (stored in local `.env`, never commit real value)

## V2 Refresh token
⚠️ **EXPIRED** — needs regeneration.
beds24.com → Account → API → Refresh Tokens → Create new

## How to get an access token (V2)
```bash
curl -X GET "https://beds24.com/api/v2/authentication/setup" \
  -H "refreshToken: YOUR_REFRESH_TOKEN"
```
Returns `{ "token": "...", "expiresIn": 3600 }`
