# Seedance 2.0 — Deep Reference

*Compiled June 2026 from secondary sources + arXiv:2604.14148. Verify exact figures against current docs.*

---

## 1. Capabilities & Access

- **What:** ByteDance SEED Lab native multimodal audio-video model. Architecture: **Dual-Branch Diffusion Transformer** — processes pixels and audio waveforms in parallel, so visual events and sound (footstep ↔ foot landing) stay physically synced.
- **Input modes:** Text-to-Video · **Image-to-Video** (still as first frame) · **First-and-Last-Frame / In-Between** (start + end keyframe, model animates between) · **Reference-to-Video** (Universal Reference System with `@` tags) · **Edit / Extend** existing video.
- **Reference budget (reported):** up to ~12 files — up to 9 images (lock face/costume/environment/grade), up to 3 videos ≤15s total (copy camera moves/physics/choreography), up to 3 audio ≤15s total (set tone/timbre/beat).
- **Duration:** ~4–15s single pass, 1s increments. (Seedance 2.5 preview: native 30s.)
- **Resolution / fps:** 480p/720p/1080p, native 4K added mid-2026; 24fps default (cinematic motion blur), up to 60fps on some integrations.
- **Aspect:** 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive.
- **Where:** Dreamina (dreamina.capcut.com), Jimeng/即梦 (China), CapCut, Volcengine/BytePlus ModelArk (model id **`doubao-seedance-2.0`**), fal.ai, ComfyUI, and third parties (Morphic, Higgsfield, WaveSpeed, etc.). A lighter **Seedance 2.0 Mini** ≈ half the cost.

---

## 2. Camera Movement Table

| Move | Keywords | Effect / tip |
|------|----------|--------------|
| Dolly in/out (push/pull) | `dolly-in`, `push in`, `pull back`, `move toward/away` | Build intensity (in) / reveal context (out) |
| Pan L/R | `pan left/right`, `sweep` | Lateral rotation on axis. Keep slow → avoid smear |
| Tilt up/down | `tilt up/down` | Up = scale/awe; down = discovery/intimacy |
| Truck L/R | `truck left/right`, `move laterally` | Translate parallel to subject; scan shelves, walk beside |
| Crane/aerial | `crane up/down`, `drone`, `bird's eye`, `ascending` | Vertical through space; pair with pull-back for scale |
| Tracking/follow | `tracking shot`, `follow`, `alongside` | Travels with a moving subject at constant distance |
| Orbit/arc | `orbit`, `360 degrees`, `arc`, `revolve` | Circles subject; product reveals/entrances. Specify angle |
| Zoom | `zoom in/out`, `dolly zoom` | Compresses background; dolly-zoom = Vertigo effect |
| Whip/swish pan | `whip pan`, `snap pan` | Fast blur streak; energetic transition cut |
| Handheld | `handheld`, `natural sway`, `documentary` | Grit/intimacy; swap for `gimbal`/`steadicam` if smooth needed |

**Modifiers:** adverbs — `slowly, smoothly, gradually, dramatically, powerfully, aggressively, subtly, suddenly`. **Compound:** max 2–3 moves in sequence: *"slow dolly-in for 5s, then a rapid 1s whip pan right."*

**Shot sizes:** wide/establishing (use slow dolly or locked-off; avoid fast pans), medium (safest, most stable), close-up/macro (tiny slow push-ins only; lateral moves warp edges).
**Angles:** eye-level (neutral), low (power), high (vulnerability), Dutch (unease).

---

## 3. Combining Camera + Subject Motion

1. **One shot, one verb** (present tense).
2. **Match energy to tempo** — running/sports ↔ aggressive handheld tracking/whip pan; luxury/portrait ↔ slow smooth dolly or eye-level orbit.
3. **Sync to audio beats** — *"Sync camera transitions to the beat positions of `@Audio1`; cuts land on downbeats, push in on the climax."*
4. **Positive-constraint suffix** — *"Maintain strict subject shape, no edge melting, smooth camera tracking, no jittery frames, highly consistent details."*

---

## 4. VFX, Atmosphere, Lighting, Speed, Transitions

- **Particles/weather** (volumetric, interactive — they collide/wrap with subjects): `volumetric dust particles`, `swirling ash`, `billowing smoke`, `drifting embers`, `volumetric light rays`, `splintering sparks`. Couple to physics: "wind gently moving her hair," "boots splashing through puddles," "steam rising."
- **Dynamic lighting:** name source + mood (`golden hour backlight`, `chiaroscuro`, `neon backlit`, `studio three-point`, `harsh overhead fluorescent`); reflective surfaces ("neon on wet asphalt") force realistic interaction; time-based change ("at 8s the overhead lights snap on").
- **Speed:** `slow-motion`, `2x slow speed`, `high-speed descent`; time-lapse — *"Time-lapse: morning light sweeps the skyline, shadows rotate, city lights ignite as dusk falls."* Target `24fps` for natural motion blur.
- **Transitions:** numbered shots with timing markers + guardrail *"Transitions by clean cuts. No morphing, no ghosting, no camera cuts during action."* Vocabulary: `whip pan`, `match cut`, `morph dissolve`, `rack focus`.

---

## 5. Native Audio Syntax

- **Dialogue:** wrap exact words in **double quotes** → auto speech + lip-sync (English, Mandarin, Japanese, Korean, Spanish, French, German, Portuguese…).
- **Transcript trick:** when using a voice reference `@Audio1`, also paste the exact spoken words in double quotes → tighter lip-sync, no verbal hallucination.
- **Audio script block** (timestamped cues):
  ```
  [AUDIO: 0s] heavy footsteps on wet soil, echoing in a cave
  [AUDIO: 3s] sword draws with a sharp metallic scrape
  [AUDIO: 5s] character says "I knew you would come."
  [AUDIO: 8s] a low thunderous boom rumbles
  ```
- **SFX:** describe physical acoustics ("glass shattering," "heavy metallic clink"), not mood ("scary noise").
- **Music beat-sync:** upload a pre-trimmed ≤15s WAV/high-bitrate MP3 with a clear build + drop as `@Audio1`; prompt "sync cuts and motion peaks to the beat positions; peak on the drop."

---

## 6. Failure Modes → Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| Character morphing / identity shift | Text contradicts the `@Image` reference | Strip physical adjectives from text; add suffix "maintain face & clothing consistency, no distortion" |
| Jittery / warping motion | Reference video too fast/complex | Simplify the motion ref; match text energy to its speed; add `gimbal stabilized`/`steadicam` |
| Ignored prompt / camera drift | Vague vibe words ("dynamic," "epic") | Use formula Subject→Action→Camera→Style→Constraints; precise rig metaphors; one verb per shot |
| Lip-sync lag / mouth jitter | Noisy/fast audio, no enunciation cues | Trim silence but keep 150–400ms breath pauses; paste exact transcript in double quotes |
| Edge melting in close-ups | Lateral/fast moves at macro range | Use tiny slow push-ins only at CU/macro |

**70/30 rule:** weight conditioning toward identity (70) over motion (30). Use ≥1024px (ideally 2K/4K) references — low-res forces the model to hallucinate faces.

---

## 7. End-to-End: Storyboard Grid → Finished Clip

1. **Plan** a short shot list (who, action, camera per scene).
2. **Generate keyframes** (GPT Image 2 etc.) with a fixed reusable style block on every frame.
3. **Slice & label** assets (`@Image1_char`, `@Image2_bg`) at high res.
4. **Animate shot 1** — Panel 1 first frame, Panel 2 last frame, In-Between formula.
5. **Chain** — last frame of shot 1 → first frame of shot 2 (Panel 3 as its end). Repeat.
6. **Audio pass** — `@Audio1` beat-sync + `[AUDIO:]` dialogue/SFX block.
7. **Finish** — DaVinci/CapCut, trim 1–2 ramp-up seconds/clip, one unified LUT, export 1080p+ 24fps 40–60 Mbps.
