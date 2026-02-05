# interaction-index-api-client (OpenClaw skill)

A tiny client + OpenClaw skill that calls an `interaction-index-api` service that is protected by a simple proof-of-work (PoW).

## How it works

The API requires a PoW per request:

1) `GET /pow/challenge` -> returns `{pow_id, challenge, difficulty}`
2) Find a `nonce` so that:

`sha256("{pow_id}:{challenge}:{nonce}")` (hex) starts with `difficulty` leading `0` chars.

3) Call `/predict` with headers:

- `X-PoW-Id: <pow_id>`
- `X-PoW-Nonce: <nonce>`

## Usage

The API base URL is fixed:

- `https://zaihua.cone.im`

Example:

```bash
python3 skills/interaction-index-api-client/scripts/predict_via_api.py \
  --text $'标题\n正文...\nhttps://example.com'
```
