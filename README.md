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

## Input format

Two supported inputs:

- `--text`: paste a short news blurb.
- `--tme-url`: a public Telegram post link (`https://t.me/<channel>/<id>`).

Recommended `--text` layout (works best with the model):

```text
一句标题（尽量单独一行）
几行正文/摘要
https://source.domain/article
```

## Output fields

The client prints JSON from the API. Key fields:

- `score10`: 1-10 (higher -> more expected interactions)
- `pred_reactions_total`: predicted total reactions (emoji/reaction count)
- `yhat_log1p_reactions`: internal score (log1p scale)
- `title`: extracted title
- `domain`: extracted source domain
- `meta.weekday` / `meta.hour`: posting time features (Shanghai timezone)
- `input`: echoes what you sent
- `pow.solved_ms`: how long it took to solve PoW on the client

## Suggested reply format (for chats)

If you want a short human-friendly reply:

```text
标题：<title>
评分：score10 = X/10
预测互动：约 N
```

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
