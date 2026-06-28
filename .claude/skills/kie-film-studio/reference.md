# KIE Film Studio — API Reference & Troubleshooting

Docs: GPT Image 2 text-to-image · Seedance 2.0 mini · unified jobs API (kie.ai). Verified June 2026.

## Unified jobs API

All models share one task API. Auth: `Authorization: Bearer $KIE_AI_API_KEY`, `Content-Type: application/json`.

### Create task
`POST https://api.kie.ai/api/v1/jobs/createTask`
```json
{ "model": "<model-slug>", "input": { ... }, "callBackUrl": "optional" }
```
Response: `{ "code": 200, "msg": "success", "data": { "taskId": "..." } }`

### Poll task
`GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=<id>`
```json
{ "code": 200, "data": {
    "taskId": "...", "model": "...",
    "state": "waiting | queuing | generating | success | fail",
    "resultJson": "{\"resultUrls\":[\"https://.../file.png\"]}",
    "failCode": "", "failMsg": "", "costTime": 15000, "creditsConsumed": 50 } }
```
- `resultJson` is a **stringified** JSON — parse it, then read `resultUrls[]`.
- Seedance frame variants may also return `firstFrameUrl[]`, `lastFrameUrl[]`.
- Result URLs are KIE-hosted (`tempfile.aiquickdraw.com`) and **temporary** — download promptly. Downloads need a browser-like `User-Agent` (the driver sets one; raw urllib gets HTTP 403).

### Status codes
200 ok · 401 auth · 402 insufficient credits · 422 validation · 429 rate-limited · 501 generation failed · 505 feature disabled. The driver retries 429/5xx with exponential backoff.

## Image models — text-to-image & image-to-image

**`gpt-image-2-text-to-image`** (generate from prompt):
```json
"input": {
  "prompt": "string, 1–20000 chars, required",
  "aspect_ratio": "auto|1:1|3:2|2:3|4:3|3:4|5:4|4:5|16:9|9:16|2:1|1:2|3:1|1:3|21:9|9:21",
  "resolution": "1K|2K|4K"   // 1:1 cannot be 4K; auto -> 1K only
}
```

**`gpt-image-2-image-to-image`** (generate with reference images — the consistency path):
```json
"input": {
  "prompt": "string, ≤20000 chars, required",
  "input_urls": ["array of image URLs, required, max 16"],
  "aspect_ratio": "same enum as above (default auto)",
  "resolution": "1K|2K|4K"
}
```
Use `input_urls` to pass a character/product reference sheet (and/or prior frames) so identity, wardrobe, and product geometry carry across panels. The driver auto-selects this model whenever `input_urls` is non-empty. Still repeat the Style/Character Bible text for grade/light/world. Verified: a barista rendered from a turnaround sheet stayed on-model across a new shot.

## Video model — `bytedance/seedance-2-fast` (Seedance 2.0 mini)
```json
"input": {
  "prompt": "string, 3–20000 chars, required",
  "first_frame_url": "string (optional) — the storyboard frame to animate",
  "last_frame_url": "string (optional) — for first/last-frame transitions",
  "reference_image_urls": ["max 9"],
  "reference_video_urls": ["max 3"],
  "reference_audio_urls": ["max 3"],
  "generate_audio": true,
  "resolution": "480p|720p",
  "aspect_ratio": "1:1|4:3|3:4|16:9|9:16|21:9|adaptive",
  "duration": 5,            // integer 4–15 seconds
  "web_search": false,
  "nsfw_checker": false
}
```
For image-to-video, pass the GPT Image 2 result URL as `first_frame_url`. Aspect/resolution should match the source frame to avoid letterboxing.

## Driver internals (`scripts/kie_studio.py`)
- Pure stdlib (urllib) — no pip install. Reads `.env` upward from CWD.
- `create_task` → `poll_task` (6s interval, 900s cap) → `download` (UA header).
- `run` phases write the manifest back atomically after every shot → resumable; re-run skips shots that already have `image_url`/`video_file`.
- `_parallel` runs shots concurrently (`--concurrency`, default 3); collects per-shot errors.
- `_ffmpeg_concat` tries stream-copy concat, falls back to re-encode (libx264/aac) if inputs differ.

## Troubleshooting
| Symptom | Cause / fix |
|---|---|
| `KIE_AI_API_KEY not found` | Add `KIE_AI_API_KEY=...` to project `.env`, or export it. |
| HTTP 402 | Out of credits — top up at kie.ai. |
| HTTP 422 | Bad input (prompt too short/long, invalid enum). Check resolution/aspect values. |
| Download HTTP 403 | CDN needs UA header — driver handles it; if scripting raw, set `User-Agent`. |
| task `fail` w/ failMsg | Read failMsg; often moderation or unsupported combo (e.g. 1:1 + 4K). |
| Clips won't concat (copy) | Different codecs/res between clips → driver auto re-encodes; keep all shots same aspect/resolution to allow fast copy. |
| Letterboxed video | `aspect_ratio` mismatch between frame and clip — keep them equal. |
| Consistency drift across frames | Repeat the Style/Character Bible verbatim in every `image_prompt`; chain Seedance with `first_frame_url`/`last_frame_url`. |

## Cost discipline
Each image and clip burns credits. Lock the look at `1K` / `480p` / 4–5s, then scale `2K`/`720p` and longer. The review gate after Phase 3 exists to avoid animating a frame you'll reject.
