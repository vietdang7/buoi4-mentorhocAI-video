---
name: seedance-2-cinematic-motion
description: Use when writing prompts for Seedance 2.0 (ByteDance, doubao-seedance-2.0, on Dreamina/Jimeng/CapCut/Volcengine/fal/ComfyUI) to animate still images or storyboard frames into cinematic video — image-to-video, first/last-frame transitions, camera moves, VFX/atmosphere, native synchronized audio (dialogue, SFX, music beat-sync), and multi-shot consistency for ads and short films.
---

# Seedance 2.0 — Cinematic Image-to-Video

## Overview

Seedance 2.0 is a native **audio-video** model: it generates picture and synchronized sound in one pass (Dual-Branch DiT). Prompt it like a **director giving shot directions to a crew** — when animating a still, the image already defines the world, so your text's job is **motion, camera, timing, and sound**, not re-describing what's visible.

Adopt three lenses on every clip:
- **Director/DP** — one clear action per shot + explicit camera rig moves matched to the energy.
- **VFX/atmosphere** — volumetric particles, dynamic lighting changes, speed (slow-mo/timelapse).
- **Sound designer** — native dialogue (double quotes → lip-sync), timestamped SFX, music beat-sync.

## The Iron Rules

1. **Describe motion, not the picture.** For image-to-video, omit hair color, wardrobe, scene details already in the frame. Re-describing them creates vector conflicts → face morphing / "identity drift."
2. **One shot, one verb.** Center each shot on a single present-tense action ("she turns and looks up"). Stacking verbs confuses the temporal branch.
3. **No negative prompts — use positive constraints.** Seedance has no negative-prompt field. Write "sharp, crisp frames" not "no blur"; append a guardrail suffix: *"Maintain subject shape, no edge melting, no ghosting, no distorted faces."*
4. **Name real camera rigs, not vibes.** "slow dolly-in," "360 orbit," "handheld tracking" — not "dynamic" or "cinematic" (those default to a static medium shot).
5. **Keep it 30–100 words** (sweet spot 50–70). Over ~200 words = conflicting instructions and artifacts.

## Prompt Formula

Quick: `[Subject] + [Motion] + [Scene] + [Camera] + [Style]`

Production (**CRAFT**):
- **C**ontext — environment, time, lighting.
- **R**eference — tag assets with `@` and assign roles: `@Image1` = start frame, `@Video1` = motion to copy, `@Audio1` = music.
- **A**ction — subject's movement, active present tense, one dominant verb.
- **F**raming — camera move + shot size + angle (e.g. "slow dolly-in from MS to CU").
- **T**iming — beats / second markers to pace action and sync audio ("0–4s: …; 4–8s: …").

## Camera, VFX & Audio (essentials)

- **Camera moves:** dolly in/out · pan · tilt · truck · crane/aerial/drone · tracking/follow · orbit/arc (specify 180°/360°) · zoom (dolly-zoom = Vertigo) · whip pan · handheld vs gimbal/steadicam. Tune with adverbs (slowly, smoothly, dramatically) and 2–3 moves max in sequence.
- **VFX/atmosphere:** physical terms ("volumetric dust," "drifting embers," "billowing smoke," "wind moving her hair"); dynamic lighting over time ("at 8s the overhead lights snap on"); speed ("slow-motion 2x," "time-lapse: shadows rotate as dusk falls").
- **Audio (native):** dialogue in **double quotes** → auto lip-sync (8+ languages). Timestamped cues `[AUDIO: 3s] sword scrape`. Describe SFX physically ("glass shattering"), not "scary noise." Music: upload a ≤15s clip with a clear build/drop as `@Audio1` and prompt "sync cuts to the beat positions."
  - **One line in a single continuous shot:** timestamp it to land on a motion beat — `[AUDIO: 6s] a low calm male voice says "Almost there."` Place the marker where you want lip movement, and order the action so the camera/gesture peaks on it.
  - **No voice reference?** The model invents the voice. Steer it by naming the speaker in the cue ("a warm female voice," "a gravelly older man") instead of leaving it generic. For an exact voice, upload `@Audio1` and paste the transcript in double quotes (transcript trick).

See **reference.md** for the full camera table, audio syntax, failure-mode fixes, and capabilities. See **templates.md** for copy-paste prompts.

## Storyboard → Cinematic Video Workflow

1. **Generate consistent keyframes** (e.g. with GPT Image 2 / the gpt-image-2-storyboard skill). Append a fixed style block to every frame. Slice into clean ≥1024px keyframes; label assets (`@Image1_char`, `@Image2_bg`).
2. **Animate shot 1** with **first-and-last-frame** mode: Panel 1 = first frame, Panel 2 = last frame. Prompt: *"Show what happens in between. [action]. Slow camera push-in. Transitions by clean cuts, no morphing, no ghosting."*
3. **Continuity-chain:** use the rendered last frame of shot 1 as the first frame of shot 2 (with Panel 3 as its last frame). Repeat.
4. **Identity:** bind the same reference package to every shot; apply the **70/30 rule** — weight identity over motion so a video reference's movement doesn't melt the face.
5. **Audio pass:** add `@Audio1` for beat-sync and an `[AUDIO: …]` script block for dialogue/SFX.
6. **Finish:** assemble in DaVinci/CapCut, trim the first 1–2 "ramp-up" seconds per clip, apply one unified LUT, export 1080p+ 24fps high-bitrate.

## Quick Reference

| Need | Do this |
|------|---------|
| Animate a still cleanly | One verb, name a camera move, add positive-constraint suffix |
| Stable identity | Don't re-describe the subject; 70/30 identity-over-motion; bind references |
| Smooth motion | "gimbal stabilized / steadicam"; keep pans slow; one action per shot |
| Transition between 2 frames | First/last-frame mode + "Show what happens in between…" |
| Dialogue | Put exact words in double quotes; for voice refs paste the transcript too |
| Music-cut sync | `@Audio1` (≤15s, clear drop) + "sync cuts to the beat positions" |
| Multi-shot scene | Timed beats `00:00–00:04 …` + "transitions by clean cuts, no morphing" |

## Common Mistakes

- **Re-describing the reference image** → morphing. Strip physical adjectives; let `@Image` do the work.
- **Vibe words as camera directions** ("epic," "dynamic") → static medium shot. Use rig metaphors.
- **Trying negative prompts** → ignored. Convert to positive constraints.
- **Motion-reference too fast/complex** → jitter/warping. Simplify it; match text energy to the reference speed.
- **Over-long prompt** → conflicting instructions. Trim to 50–70 words.

> **Accuracy note:** Platform availability, durations, resolutions, model IDs, and pricing change fast and were compiled June 2026 from secondary sources (incl. arXiv:2604.14148). Confirm against current Dreamina/ModelArk/fal docs before relying on exact numbers. Research notebook: NotebookLM "Seedance 2.0 Image-to-Video Cinematic Motion 2026".
