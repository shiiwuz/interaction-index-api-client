# interaction-index-api-client (OpenClaw skill)

Predict an "interaction index" (互动分/互动指数) for short news/posts.

- Input: a text snippet (title + summary + links) or a Telegram public post link (`t.me/.../...`).
- Output: `score10` (1-10) + `pred_reactions_total` (expected emoji/reaction count).

This repo provides:
- an OpenClaw skill (`skills/interaction-index-api-client/`)
- a tiny Python client that calls the hosted API at `https://zaihua.cone.im`

## How it works

The API requires a PoW per request:

1) `GET /pow/challenge` -> returns `{pow_id, challenge, difficulty}`
2) Find a `nonce` so that:

`sha256("{pow_id}:{challenge}:{nonce}")` (hex) starts with `difficulty` leading `0` chars.

3) Call `/predict` with headers:

- `X-PoW-Id: <pow_id>`
- `X-PoW-Nonce: <nonce>`

## Usage

The API base URL is fixed: `https://zaihua.cone.im`

Text example:

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --text $'标题\n正文...\nhttps://example.com'
```

Telegram post example:

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --tme-url https://t.me/<channel>/<id>
```

Install notes for OpenClaw users: `skills.md`
