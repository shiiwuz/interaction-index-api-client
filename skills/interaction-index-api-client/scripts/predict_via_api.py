#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.request


def sha_ok(difficulty: int, data: str) -> bool:
    h = hashlib.sha256(data.encode("utf-8")).hexdigest()
    return h.startswith("0" * difficulty)


def http_json(url: str, *, method: str = "GET", headers: dict[str, str] | None = None, body: dict | None = None) -> dict:
    data = None
    hdrs = {"accept": "application/json"}
    if headers:
        hdrs.update(headers)
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        hdrs["content-type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def solve_pow(base: str, *, max_seconds: float = 20.0) -> tuple[str, str, int, int]:
    ch = http_json(base.rstrip("/") + "/pow/challenge")
    pow_id = ch["pow_id"]
    challenge = ch["challenge"]
    diff = int(ch["difficulty"])

    start = time.time()
    nonce = 0
    while True:
        s = str(nonce)
        if sha_ok(diff, f"{pow_id}:{challenge}:{s}"):
            break
        nonce += 1
        if time.time() - start > max_seconds:
            raise RuntimeError(f"PoW timeout after {max_seconds}s (difficulty={diff})")

    solved_ms = int((time.time() - start) * 1000)
    return pow_id, s, diff, solved_ms


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=os.environ.get("INTERACTION_INDEX_API_BASE_URL"))
    ap.add_argument("--text", default=None)
    ap.add_argument("--tme-url", default=None)
    ap.add_argument("--ts", default=None)
    ap.add_argument("--pow-timeout", type=float, default=float(os.environ.get("POW_SOLVE_TIMEOUT", "20")))
    args = ap.parse_args()

    if not args.base_url:
        raise SystemExit("Missing --base-url or INTERACTION_INDEX_API_BASE_URL")
    if not args.text and not args.tme_url:
        raise SystemExit("Provide --text or --tme-url")

    pow_id, pow_nonce, diff, solved_ms = solve_pow(args.base_url, max_seconds=args.pow_timeout)

    body: dict = {}
    if args.text:
        body["text"] = args.text
    if args.tme_url:
        body["tme_url"] = args.tme_url
    if args.ts:
        body["ts"] = args.ts

    try:
        out = http_json(
            args.base_url.rstrip("/") + "/predict",
            method="POST",
            headers={"x-pow-id": pow_id, "x-pow-nonce": pow_nonce},
            body=body,
        )
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "ignore")
        raise SystemExit(f"HTTP {e.code}: {msg}")

    out["pow"] = {"difficulty": diff, "solved_ms": solved_ms}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
