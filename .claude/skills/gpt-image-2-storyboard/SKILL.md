---
name: gpt-image-2-storyboard
description: Use when writing prompts for GPT Image 2 (gpt-image-2 / ChatGPT Images 2.0) to generate film storyboards, short-film frames, commercial/ad creative, key art, product shots, or any cinematic still — especially when JSON-structured prompts, character consistency across panels, in-image text, or art-direction quality matter.
---

# GPT Image 2 — Storyboard & Ad Creative Prompting

## Overview

Prompt GPT Image 2 like a **film director + cinematographer + advertising art director** who is also a **prompt engineer fluent in JSON prompting**. The model plans layout and composition *before* rendering, so it rewards precise, structured creative briefs — and punishes keyword spam ("masterpiece, 8k, stunning"). Describe **visual facts**, not adjectives of praise.

Adopt all three expert lenses on every shot:
- **Director/DP** — shot size, angle, lens, lighting, blocking, color grade.
- **Ad art director** — hero framing, negative space for copy, exact in-image text, brand palette.
- **Prompt engineer** — structure (prose formula or JSON), invariants/preserve-lists, iterative single-variable edits.

## The Two Prompt Forms

**Prose formula** (fast, single hero shots) — order matters; lead with the subject (early tokens weigh more):

`[Subject + concrete adjectives] → [Action] → [Scene/setting] → [Composition/camera: lens, shot size, angle] → [Lighting/atmosphere] → ["exact in-image text" + constraints]`

**JSON prompt** (repeatable series, complex layouts, ad campaigns) — isolates each attribute so descriptors don't "bleed" (e.g. a "dark, metallic" background leaking onto the subject). Use JSON when you batch-generate panels keeping `camera`/`lighting`/`grading` constant and swap only `subject`/`text`.

```json
{
  "type": "cinematic storyboard frame",
  "subject": "weathered detective in a charcoal trench coat",
  "action": "leaning over a rain-streaked car window, peering inside",
  "setting": "neon-lit alley at night, wet asphalt, distant traffic",
  "camera": "35mm lens, medium close-up, low-angle, shallow depth of field",
  "lighting": "hard cyan key from a neon sign, warm sodium rim light, deep shadows",
  "mood": "tense, noir, observational",
  "color_palette": "teal shadows, amber highlights, desaturated mids",
  "aspect_ratio": "16:9",
  "text_rendering": { "verbatim_text": "", "placement": "none" },
  "constraints": "no watermark, no extra text, realistic film grain, clean margins"
}
```

> JSON helps because it organizes the brief and disambiguates attributes — treat it as a discipline for *you*, not a guarantee the model parses keys as a layout engine. Plain prose with the same precision also works.

See **templates.md** for ready-to-paste prose + JSON templates (storyboard, ad poster, product hero, character sheet).

## Core Workflow for a Storyboard Sequence

1. **Lock identity first.** Generate a multi-view **character reference sheet** (front/side/back + expression row, clean off-white background) before any panel. This is your visual anchor.
2. **Generate panels** using the reference as input. With multi-image reference, assign **explicit roles**: *"Use Image 1 as face/identity, Image 2 as wardrobe, Image 3 as location/lighting."*
3. **Hold optics & light constant across panels** — same lens, lighting setup, film-stock/grade phrasing — to keep the sequence visually unified.
4. **Edit, don't regenerate.** For coverage (CU after the MS), use the edit endpoint with the **three-sentence edit pattern**:
   - *Change:* "Crop into a tight close-up on her face."
   - *Invariants:* "Preserve hairstyle, wardrobe, lighting direction, camera angle exactly."
   - *Realism match:* "Match depth of field, highlight roll-off, and film grain of the source."
5. **Refresh the session every 3–5 generations** to dodge the noise/grid artifact bug (below).

## Quick Reference

| Need | Do this |
|------|---------|
| Cinematic look | Name lens + shot size + angle + lighting setup + film stock/grade. See reference.md |
| Exact ad copy | Put text in **straight double quotes**; add `"render verbatim, no extra words, no duplicate text"` |
| Hero product | Lead with the product noun; `85mm f/1.4`, shallow DoF; state where copy goes (negative space) |
| Consistency | Character sheet → multi-image reference with explicit roles → edit-with-preserve-list |
| Mood | Translate emotion into physical light/texture, not "epic/beautiful" |
| Aspect/format | 16:9 banners, 2:3/9:16 posters & mobile, 1:1 social. Width/height multiples of 16 |

## Common Mistakes

- **Keyword spam.** "masterpiece, 8k, ultra-detailed" → generic slop. Describe what's literally in frame.
- **Asking the model to invent copy.** It garbles invented slogans. Always quote exact text.
- **No invariants on edits.** Omitting a preserve-list causes face/geometry drift. Repeat the list every edit turn.
- **Five changes in one edit.** Change one variable at a time.
- **Expecting perfect logos / transparent PNGs / tiny legal copy.** These are weak spots — composite logos from approved assets, remove backgrounds downstream, enlarge fine print.

## From storyboard to motion

This skill makes **stills**. For a finished spot/short, the frames are inputs to a video step: animate them with **seedance-2-cinematic-motion** (REQUIRED for image-to-video — camera moves, VFX, native audio, first/last-frame transitions). Generate consistent panels here, then chain them there. Real brand logos / legal supers / exact typefaces should be composited downstream from approved assets, not generated.

## Deeper reference

- **reference.md** — full cinematography vocabulary (shot sizes, angles, lenses, lighting, film stocks, composition), ad art-direction playbook, model capabilities/limits, and the consistency pipeline.
- **templates.md** — copy-paste prose and JSON templates.

> **Accuracy note:** Specifics like exact resolution caps, the `quality`/`moderation`/`background` parameter set, reference-image count, and pricing change with model versions and were reported by secondary sources (June 2026). Confirm against the current OpenAI API docs before relying on exact numbers. Research notebooks: NotebookLM "GPT Image 2 Prompting for Film/Ad Storyboards 2026".
