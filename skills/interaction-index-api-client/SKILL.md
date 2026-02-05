---
name: interaction-index-api-client
description: Call an interaction-index prediction API protected by a simple proof-of-work (PoW). Use when you want to score a text snippet or a Telegram public post via a remote API.
---

# interaction-index-api-client

## Setup

- API base URL is fixed: `https://zaihua.cone.im`

## Predict

Text:

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --text $'标题\n正文...\nhttps://example.com'
```

Telegram post:

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --tme-url https://t.me/<channel>/<id>
```
