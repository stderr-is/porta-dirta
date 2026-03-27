---
name: n8n HTTP Request node JSON body
description: How to correctly send a JSON body from an n8n HTTP Request node v4 (the jsonBody fix)
type: feedback
---

In HTTP Request node v4, to send a JSON body:
- Set **Body Content Type** to `JSON`
- Use **JSON Body** field (not "Body Parameters")
- Expression: `={{ $json.someField }}`

The old "Body Parameters" approach sends form-encoded, not JSON — APIs reject it silently.
