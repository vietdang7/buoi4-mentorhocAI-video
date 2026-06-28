# Seedance 2.0 — Copy-Paste Prompts

Replace `[...]`. Keep prompts 50–70 words. End with a positive-constraint suffix. For image-to-video, describe **motion/camera/sound only** — not what's already in the frame.

---

## A. Animate a still (image-to-video, basic)

> [SUBJECT in the frame] [ONE PRESENT-TENSE ACTION]. [CAMERA MOVE + speed adverb], [shot size]. [Lighting/atmosphere cue]. Maintain strict subject shape, no edge melting, no ghosting, sharp frames.

**Example**
> The woman slowly turns toward the window and tilts her head up. Gentle handheld push-in from medium to close-up. Soft golden-hour backlight, dust motes drifting in the air. Maintain face and clothing consistency, no distortion, no ghosting, sharp crisp frames.

---

## B. First/Last-frame transition (In-Between)

> Show what happens in between. [Subject from @Image1] [ACTION connecting the two frames]. [Camera move]. 5 different camera angles. Transitions by clean cuts, no morphing, no ghosting. No music.

**Example**
> Show what happens in between. The soldier from @Image1 runs powerfully through deep snow toward the base gate under a heavy blizzard, reaching it in @Image2. Low tracking shot. Transitions by clean cuts, no morphing, no ghosting. No music.

---

## C. Product / ad clip (orbit + beat-sync)

> [Product] on [surface]. Use @Audio1 as the rhythmic foundation. [Studio lighting]. Smooth 360-degree macro orbit around the product. At [Xs], precisely on the beat, [lighting/UI change]. [AUDIO: Xs] [soft sfx]. Maintain product geometry, no logo distortion, no text overlays, crisp sharp textures.

**Example**
> A sleek smartwatch on a wet marble slab. Use @Audio1 as the rhythmic foundation. Studio three-point lighting, soft gradient background. Smooth 360-degree macro orbit. At 4s, precisely on the heavy beat, the watch face illuminates cyan. [AUDIO: 4s] soft electric hum. Maintain watch geometry, no logo distortion, no text overlays, sharp textures.

---

## D. Multi-shot narrative (timed beats + native audio)

> Multi-shot [N]s sequence, 24fps.
> Shot 1 (0–5s): [wide establishing — subject, atmosphere]. [AUDIO: 2s] [ambience].
> Shot 2 (5–10s): [closer — one action]. [AUDIO: 6s] [sfx].
> Shot 3 (10–15s): [climax — slow-mo / push-in]. [AUDIO: 11s] [sfx].
> Transitions by clean cuts. Maintain strict subject detail, no face distortion, no morphing, no ghosting, sharp frames.

---

## E. Dialogue shot (lip-sync)

> [Subject] [small action/expression] in [setting already in frame]. Medium close-up, slow gentle push-in. The character says "[EXACT LINE]". [AUDIO: 0s] [room ambience]. Maintain face consistency, natural lip movement, no distortion, sharp frames.

---

## F. Performance driven by a video reference (multi-reference)

> The [subject] in @Image1 [action]. Pose references @Image2. The emotion, facial expression, and movement should fully reference @Video1. [Camera move]. Keep identity from @Image1 — maintain face and clothing consistency, no morphing, sharp frames.

> 70/30 rule: keep identity weighted over motion so @Video1's movement doesn't melt the face.

---

## G. Continuity-chain across shots (storyboard → film)

1. Shot 1: Panel 1 = first frame, Panel 2 = last frame → template **B**.
2. Take the **rendered last frame** of Shot 1 → use as **first frame** of Shot 2; Panel 3 = last frame → template **B** again.
3. Repeat for each panel. Apply one unified LUT in the edit to smooth lighting drift.

---

## Positive-constraint suffix library (no negative prompts exist)

- Stability: `Maintain strict subject shape, no edge melting, no ghosting, no distorted faces, sharp crisp frames.`
- Product: `Maintain product geometry, no logo distortion, no text overlays, sharp textures.`
- Cuts: `Transitions by clean cuts. No morphing, no ghosting, no camera cuts during action.`
- Clean plate: `Generate video without subtitles, no watermark.`
