# Using This As An OpenClaw Skill

This repo contains an OpenClaw skill at:

- `skills/interaction-index-api-client/`

It predicts an interaction index (互动分/互动指数) by calling the hosted API at `https://zaihua.cone.im`.

## Quick Start

1) Clone this repo somewhere:

```bash
git clone https://github.com/shiiwuz/interaction-index-api-client
```

2) Copy the skill folder into your OpenClaw skills directory (the one your gateway loads):

```bash
cp -r interaction-index-api-client/skills/interaction-index-api-client <YOUR_OPENCLAW_SKILLS_DIR>/
```

3) Test the client script directly (no OpenClaw required):

```bash
python3 <YOUR_OPENCLAW_SKILLS_DIR>/interaction-index-api-client/scripts/predict_via_api.py \
  --text $'标题\n正文...\nhttps://example.com'
```

## Output

The API returns JSON including:

- `score10`: 1-10 rating (higher -> more expected interactions)
- `pred_reactions_total`: predicted total reactions

## Notes

- The API is protected by PoW; each request will take ~1-2s of CPU to solve.
- API base URL is hardcoded to `https://zaihua.cone.im` in the client.
