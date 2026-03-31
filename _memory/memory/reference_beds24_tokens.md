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
- API key: `portadirta2026xK9mR4vL`
- Prop key: `318433_151ad25191cd7515eb857044e0958f1c16e37aafc6fa8fae`

## V2 Refresh token
⚠️ **EXPIRED** — needs regeneration.
beds24.com → Account → API → Refresh Tokens → Create new

## How to get an access token (V2)
```bash
curl -X GET "https://beds24.com/api/v2/authentication/setup" \
  -H "refreshToken: YOUR_REFRESH_TOKEN"
```
Returns `{ "token": "...", "expiresIn": 3600 }`
