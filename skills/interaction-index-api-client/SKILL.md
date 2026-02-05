---
name: interaction-index-api-client
description: Predict an "interaction index" (互动分/互动指数) for a text snippet or a Telegram public post by calling the hosted API (PoW-protected). Output includes score10 and predicted reactions.
---

# interaction-index-api-client

Use this skill when the user asks to 预测互动分/互动指数 for a short news blurb.

## Setup

- API base URL is fixed: `https://zaihua.cone.im`
- No API key needed; each request uses a short proof-of-work (PoW) to throttle RPM.

## Predict

Text (title + body + link recommended):

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --text $'标题\n正文...\nhttps://example.com'
```

Telegram post:

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --tme-url https://t.me/<channel>/<id>
```
