# GPT Image 2 — Deep Reference

Three expert lenses, in detail. Pull the exact vocabulary into prompts; the model translates industry terms into geometry, light, and grade far more reliably than vague praise words.

---

## 1. Cinematography Vocabulary (Director / DP lens)

### Shot sizes (emotional distance)
| Term | Frames | Use for |
|------|--------|---------|
| Extreme Wide / Establishing (EWS) | Environment dominates, subject tiny | Scale, isolation, location intro |
| Wide / Long (WS) | Full body head-to-toe | Action, movement, blocking |
| Medium (MS) | Waist up | Default dialogue, body + context |
| Medium Close-Up (MCU) | Chest up | Standard dialogue coverage |
| Close-Up (CU) | Face / a single object | Reactions, tension, emphasis |
| Extreme Close-Up (ECU) | A detail (eye, hand, watch) | Suspense, symbolism, intensity |
| Two-Shot | Two characters sharing frame | Relationships, power dynamics |
| Insert / Cut-in | Tight on a prop | Plot detail without dialogue |

### Camera angles (how we feel about the subject)
- **Eye-level** — neutral, realistic, equal.
- **Low-angle / up shot** — powerful, heroic, intimidating.
- **High-angle / down shot** — small, vulnerable, powerless.
- **Dutch / tilted** — instability, unease, chaos.
- **Overhead (God's eye)** — abstract, fragile, symbolic.
- **POV** — subjective, inside the character's eyes.
- **Worm's-eye** — extreme ground-up, exaggerated height.

### Camera height & rig positions
Over-the-shoulder (OTS), over-the-hip, shoulder-level, knee-level, over-the-back (third-person game feel), behind-the-object/spying (voyeuristic tension through doors/foliage), over-the-weapon (foreground tension).

### Lenses & depth of field
- **24–28mm wide** — establishing, exaggerated depth.
- **35–50mm standard** — natural, believable proportions (street/action).
- **85mm telephoto** — portrait isolation, compressed background, clean silhouette.
- **Anamorphic** — say "anamorphic lens flare / oval bokeh" for horizontal flares + cinematic edge.
- **Aperture** — "f/1.4" or "f/2.0" + "shallow depth of field, soft highlight roll-off" → creamy background blur.

### Lighting setups
- **Rembrandt** — soft single side key, triangular cheek highlight; classic, moody.
- **Chiaroscuro** — extreme high-contrast light/shadow; noir tension.
- **Rim / backlight** — light behind subject, halo silhouette against dark.
- **Golden hour** — long shadows, warm low sun, soft directional.
- **Practical / fluorescent** — cold overheads + warm desk lamps; gritty late-night realism.
- **Volumetric** — "volumetric light rays / shafts of light through dust/smoke."

### Composition
Rule of thirds (subject off-center on grid intersections) · leading lines (roads, hallways guide the eye) · negative space (empty area reserved for titles/copy) · partial occlusion / depth layering (foreground branches, wet glass, banners for depth).

### Film stock & color grade
- **Kodak Portra 400** — warm glowing skin, low contrast, elegant roll-off.
- **Fujifilm Pro 400H / Superia** — soft pastels, fine grain, subtle halation, green-magenta shift.
- **Grade phrasing** — "cool-toned shadows with warm amber highlights," "teal-and-orange," "desaturated natural tones."
- **Texture** — "realistic analog film grain, matte finish" prevents plastic digital surfaces.

---

## 2. Advertising Art Direction (Ad creative director lens)

Treat the prompt as a **creative brief**, not artwork fluff.

- **Hero framing** — lead with the product noun; give physical camera specs (`85mm f/1.4`, shallow DoF) for real separation; direct placement ("product on the right third").
- **Exact copy** — text in straight double quotes (`"SOUND YOU CAN FEEL"`); add `"render headline verbatim, no extra words, no duplicate text"`. For odd brand names, spell letter-by-letter (`Z-A-V-A`).
- **Brand & palette** — be specific: "muted pastel blue-gray, warm cream paper, single crimson accent." Avoid "cool colors."
- **Mood = mechanics** — convert "luxurious/calm" into "soft directional window light, natural specular highlights, slightly textured fabric drape."
- **Negative space & hierarchy** — "generous negative space on the left two-thirds for typography"; numbered layouts: "1) bold headline top-center, 2) hero in lower two-thirds, 3) small callouts in bottom margin."
- **Formats** — 1:1 social/e-com thumbnails · 2:3 or 9:16 posters/OOH/mobile · 3:2 or 16:9 billboards/banners/landing heroes.
- **Product mockups** — name materials ("brushed aluminum," "frosted glass," "matte paper with visible folds"); keep label text sharp; for cutouts keep background opaque and remove it downstream.
- **Banish slop** — never "stunning, epic, masterpiece, insane detail, 8k." The model reads descriptive language, not tags.
- **Logo trap** — generate logo *concepts* only; composite exact corporate marks from approved assets in post.

---

## 3. Model Capabilities & Limits (Prompt engineer lens)

*Reported June 2026 from secondary sources — verify exact figures against current OpenAI API docs.*

**Strengths**
- Plans/reasons about layout and resolves contradictions before rendering — excels at structured visuals (posters, UI mockups, infographics, storyboards, character sheets), readable in-image text (Latin + CJK/Arabic/Hindi), and instruction-following.
- **Multi-image reference** (reported up to ~16 images/call) with role assignment per image.
- **Character/identity consistency** via multi-view reference sheets — kills drift across panels.
- Edit endpoint auto-adjusts shadows/reflections/grade to match changes.

**Parameters (reported)** — `quality` (low/medium/high/auto: low for drafts, high for text-heavy finals), `moderation` (auto/low), `background` (auto/opaque; transparency unreliable), `output_format` (png/jpeg/webp). Aspect: width & height multiples of 16; long edge under ~3840px; common sizes 1024×1024, 1024×1536, 1536×1024, up to ~16:9 2K.

**Known weak spots**
- **Transparency** inconsistent — expect opaque output, remove background downstream.
- **Exact logos / proprietary fonts / tiny legal copy** — drift; composite or enlarge.
- **Noise / diagonal-grid bug** — the session reuses latent data, so artifacts ("digital ripples," "flicker confetti") amplify after ~3–5 images in one session. Not fixable by prompting → **reload/restart the session**; partially mitigate mid-session with "LESS DETAILS" / "clean background."
- Do **not** rely on `n=4`-in-one-call for character consistency (unverified) — use reference sheets + edits instead.

---

## 4. Consistency Pipeline (storyboard sequence)

```
[Character Reference Sheet] → [Establishing Shot] → [Mid-Shot Coverage] → [Surgical CU Edits] → [refresh session]
   (lock identity)             (orient location)      (dialogue setup)       (preserve invariants)
```

1. **Master sheet** — "character concept sheet on pure white: front/side/back views + 4 expressions, [identity, wardrobe, palette], semi-realistic, sharp focus."
2. **Establishing (EWS/WS)** — introduce location; character small; reference Image 1 for identity; fix lens + grade.
3. **Coverage (MS/MCU)** — bring camera in; keep wardrobe/light/palette matching Image 1; state lens (e.g. 50mm f/2.0).
4. **Close-ups** — edit endpoint, three-sentence pattern (Change / Invariants / Realism match). Repeat the preserve-list **every** turn.
5. **Hold optics & light constant** across shots; emulate one film stock for unified grain.
6. **Refresh session** after 3–5 panels to reset the latent buffer.

The same multi-image role discipline ("Image 1 = face, Image 2 = wardrobe, Image 3 = location/light. Render Image 1's character in Image 3's setting.") keeps backgrounds from bleeding onto the subject.
