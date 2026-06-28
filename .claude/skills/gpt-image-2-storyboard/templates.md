# GPT Image 2 — Copy-Paste Templates

Replace bracketed `[...]` fields. Keep the order. Lead with the subject.

---

## A. Storyboard frame (prose)

> Create a widescreen 16:9 storyboard frame. [SHOT SIZE] of [SUBJECT + concrete details] [ACTION] in [SETTING]. [CAMERA ANGLE] camera, [FOCAL LENGTH] lens, [DEPTH OF FIELD]. [LIGHTING SETUP] with [LIGHT DIRECTION/COLOR]. [MOOD] cinematic mood, [COLOR GRADE], [FILM STOCK] aesthetic, realistic film grain, no text.

**Filled example**
> Create a widescreen 16:9 storyboard frame. Two-shot of a tense conversation in a dimly lit office. Eye-level camera, 50mm lens feel, shallow depth of field. Detective on the left in sharp focus, suspect on the right shadowed in three-quarter profile. Chiaroscuro lighting with hard blinds-shadow stripes across the desk. Quiet, suspenseful mood, warm amber highlights on faces and deep blue-gray shadows, Kodak Portra 400 aesthetic, realistic film grain, no text.

---

## B. Storyboard frame (JSON)

```json
{
  "type": "cinematic storyboard frame",
  "subject": "[subject + concrete physical details]",
  "action": "[what the subject is doing]",
  "setting": "[location, time of day, weather, props]",
  "camera": "[shot size] + [angle] + [focal length] + [aperture/DoF]",
  "lighting": "[setup: rim/chiaroscuro/golden hour] + [direction] + [color]",
  "mood": "[emotional tone]",
  "color_palette": "[3–4 specific colors / grade]",
  "aspect_ratio": "16:9",
  "text_rendering": { "verbatim_text": "", "placement": "none" },
  "constraints": "no watermark, no extra text, realistic film grain, clean margins"
}
```

---

## C. Character reference sheet (lock identity first)

> Create a character concept sheet on a pure off-white background. Subject: [NAME], [age, build, skin, hair]. Wearing [WARDROBE + colors + accessories]. Show front, side, and back turnaround views plus a row of four facial expressions (neutral, intense, surprised, smiling). [STYLE: semi-realistic painterly / photoreal], sharp focus, consistent lighting, no text.

Reuse this image as **Image 1** in every following panel.

---

## D. Multi-image reference panel

> Use **Image 1** as the character identity and face reference. Use **Image 2** as the wardrobe reference. Use **Image 3** as the environment and lighting reference. Render the character from Image 1, in the wardrobe of Image 2, inside the setting of Image 3. [SHOT SIZE], [FOCAL LENGTH] lens, [LIGHTING] matching Image 3. Keep face, hairstyle, and wardrobe identical to Image 1. No text.

---

## E. Three-sentence edit (coverage / close-ups)

> Image 1 is the source frame. **Change:** [the one modification, e.g. "crop into a tight close-up on her face as she reacts"]. **Preserve:** [invariants — "her hairstyle, gold earrings, wardrobe, lighting direction, camera angle exactly"]. **Match:** maintain the shallow depth of field, highlight roll-off, and film grain of the source frame.

---

## F. Ad poster (JSON, portrait OOH / social)

```json
{
  "type": "high-end [category] ad poster",
  "subject": "[hero product + material + color]",
  "placement": "[where in frame, e.g. centered on a stone plinth]",
  "background": "[clean backdrop], generous negative space, no clutter",
  "camera": "85mm lens, f/1.4, eye-level, shallow depth of field, soft highlight roll-off",
  "lighting": "soft directional daylight from upper-left, realistic drop shadow",
  "color_palette": "[brand colors — be specific]",
  "aspect_ratio": "9:16",
  "text_rendering": {
    "verbatim_text": "[EXACT HEADLINE]",
    "typography": "[weight, case, family feel]",
    "placement": "top third, sharp contrast, highly legible, exact text only"
  },
  "constraints": "no duplicate text, no fake logos, clean margins, realistic [material] texture, no watermark"
}
```

---

## G. Product hero shot (prose)

> A [PRODUCT + material + color] on a [SURFACE] with clean realistic reflections. [softbox/studio] lighting from the left, soft highlight roll-off and gentle rim light. [Mood] mood, [palette]. Product in sharp focus on the right third; left two-thirds soft blurred background with generous negative space for copy. 85mm f/1.4, shallow depth of field. In-image text reads EXACT TEXT: "[BRAND]" with smaller "[tagline]" below. No extra words, no fake logos, no duplicate text. Aspect ratio 3:2.

---

## Reusable style block (paste into every panel for a unified series)

> `Cinematic [film stock] aesthetic, [grade phrasing], [lens consistency], realistic analog film grain, 16:9.`

Keep this string identical across the whole sequence so panels share one visual register.
