---
name: kie-film-studio
description: Use when the user wants to produce a complete short film, ad, or video clip end-to-end from a brief via KIE.ai — generating storyboard frames with GPT Image 2 and animating them into video with Seedance 2.0 mini, then assembling the final cut. Triggers include "make me a film/ad/commercial/clip", "storyboard to video", "turn this idea into a video", KIE.ai pipeline, GPT Image 2 + Seedance workflow.
---

# KIE Film Studio — Brief → Storyboard → Video → Film

## Overview

An orchestration workflow (operates like `/deep-research`: phased, fan-out, checkpointed) that turns a creative brief into a finished video. You, the orchestrator, run the phases: break the brief into shots, **author the prompts using the two prompting skills**, then call the KIE.ai API via `scripts/kie_studio.py` to render frames (GPT Image 2) and clips (Seedance 2.0 mini), and assemble with ffmpeg.

**REQUIRED SUB-SKILLS — invoke both and apply them when writing prompts:**
- **gpt-image-2-storyboard** — author every `image_prompt` (cinematic/ad framing, JSON or prose, consistency).
- **seedance-2-cinematic-motion** — author every `motion_prompt` (camera move, VFX, native audio, one verb).

Do not hand-wave prompts. Each shot's prompts MUST come from applying those skills.

## The Pipeline (phases)

```
0 Intake → 1 Breakdown → 2 Prompt authoring → 3 Storyboard (images) →
  [REVIEW GATE] → 4 Animate (video) → 5 Assemble → final.mp4
```

1. **Intake.** Confirm: concept/logline, mood/style, aspect ratio, total length & number of shots, per-shot duration, dialogue/audio, whether audio is generated. Ask only what's missing.
2. **Breakdown.** Write a shot list (one row per shot: beat, shot size, action) + a **Style & Character Bible** — a fixed block (wardrobe, palette, lens, film stock, lighting) repeated in every image prompt. For recurring characters/products, also define a `character` sheet (below) — KIE has **both** `gpt-image-2-text-to-image` and `gpt-image-2-image-to-image` (reference images, up to 16), so the driver renders the sheet once and feeds it as a reference into every panel for true identity lock.
3. **Prompt authoring.** Using the two skills, write `image_prompt` and `motion_prompt` for every shot. Build the manifest (schema below). Show it to the user.
4. **Storyboard.** `kie_studio.py run manifest.json --only storyboard` — renders all frames in parallel, writes image URLs + local PNGs back into the manifest.
5. **REVIEW GATE.** Show the rendered frames. Video is the expensive step — get approval (or regenerate specific frames) before animating.
6. **Animate.** `kie_studio.py run manifest.json --from animate` — feeds each frame's hosted URL as Seedance's `first_frame_url`, renders clips, then assembles. (Or split: `--only animate` then `--only assemble`.)
7. **Deliver** the final film path; offer a colour-grade/edit pass note.

## Running the driver

```bash
PY=.claude/skills/kie-film-studio/scripts/kie_studio.py

# one-off frame / clip (for tests or single shots)
python3 $PY image --prompt "..." --aspect-ratio 16:9 --resolution 2K --out frames/s01.png
python3 $PY video --prompt "..." --first-frame-url "<hosted url>" --duration 5 --resolution 720p --out clips/s01.mp4

# full film from a manifest (the deep-research-style run)
python3 $PY run film.json --only storyboard          # phase 3: all frames
python3 $PY run film.json --from animate             # phase 4+5: clips then assemble
python3 $PY run film.json                            # all phases at once
```

- Auth: reads `KIE_AI_API_KEY` from the project `.env` automatically (or env var).
- The driver is **resumable**: it writes URLs/paths back into the manifest after each task, so re-running skips finished shots. Pass `--concurrency N` (default 3).
- The image `resultUrl` is already KIE-hosted → passed directly to Seedance as `first_frame_url` (no re-upload).

## Manifest schema (`film.json`)

```json
{
  "title": "Mountain Run",
  "defaults": {
    "aspect_ratio": "16:9",
    "image_resolution": "2K",
    "video_resolution": "720p",
    "duration": 5,
    "generate_audio": true
  },
  "character": {
    "image_prompt": "<character/product reference sheet — multi-view turnaround + expressions, off-white background, from gpt-image-2-storyboard>"
  },
  "shots": [
    {
      "id": "s01",
      "image_prompt": "<from gpt-image-2-storyboard skill. Start with: 'Use the reference image as the exact identity/wardrobe.' then the shot's framing/action/lighting + the Bible>",
      "motion_prompt": "<from seedance-2-cinematic-motion skill — one verb + camera + audio>",
      "duration": 5,
      "reference_character": true
    }
  ]
}
```

**Character consistency (the strong path):** define `character.image_prompt`. In the storyboard phase the driver renders it first (text-to-image), then passes its URL as a reference into every shot where `reference_character` is true (default true) via `gpt-image-2-image-to-image`. Begin those `image_prompt`s with *"Use the reference image as the exact identity and wardrobe…"* and end with *"keep face/hair/wardrobe identical to the reference."* Verified to hold a character across frames.

Optional per-shot overrides: `aspect_ratio`, `image_resolution`, `video_resolution`, `generate_audio`, `image_model`, `video_model`, `reference_character` (bool), `input_urls` (extra reference image URLs for the image step), `last_frame_url`, `reference_image_urls` (video step). The driver fills `image_url`, `image_file`, `video_url`, `video_file`, and `final_video`. See `templates/film.example.json`.

**Style/Character Bible scope:** even with reference images, still hold the *grade, lighting, film stock, and world* constant and **verbatim** across every `image_prompt`. The *lens/shot size* changes per shot (e.g. 24mm establishing vs 85mm macro) — that's the one camera line you vary; everything else stays identical so the frames read as one film.

## Key constraints (KIE.ai)

| | Values |
|---|---|
| Image model | `gpt-image-2-text-to-image` (prompt) or `gpt-image-2-image-to-image` (prompt + `input_urls`, up to 16 refs) · resolution `1K`/`2K`/`4K` (1:1 can't be 4K; `auto` aspect → 1K only) · aspect `1:1,3:2,2:3,4:3,3:4,16:9,9:16,21:9,…` |
| Video model | `bytedance/seedance-2-fast` (= Seedance 2.0 mini) · resolution `480p`/`720p` · duration `4–15s` · aspect `16:9,9:16,1:1,4:3,3:4,21:9,adaptive` · `generate_audio` default true |
| API | create `POST /api/v1/jobs/createTask` → poll `GET /api/v1/jobs/recordInfo?taskId=` (`state`: waiting→generating→success/fail; `resultJson.resultUrls`) |

## Common Mistakes

- **Skipping the skills** → generic prompts, weak frames. Always author via the two sub-skills.
- **Animating before review** → wasted credits on a bad frame. Honour the review gate.
- **Consistency drift** → define a `character` sheet and reference it via image-to-image (`reference_character`), AND repeat the Style/Character Bible verbatim in every `image_prompt`; then carry it into motion via Seedance `first_frame_url` (+ `last_frame_url` for transitions).
- **Re-describing the frame in `motion_prompt`** → morphing. Per the Seedance skill, describe motion/camera/audio only.

> Cost & verification: each image and each clip consumes KIE credits. Test with `1K`/`480p`/short durations first; scale up after the look is locked. Driver was smoke-tested end-to-end (image → video w/ native audio → ffmpeg concat) June 2026. See **reference.md** for the full API spec and troubleshooting.
