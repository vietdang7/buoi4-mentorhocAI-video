# AI Storyboard & Video Skills

Two [Claude Code](https://claude.com/claude-code) skills for an AI ad/short-film pipeline: generate cinematic **storyboard frames** with GPT Image 2, then **animate** them with Seedance 2.0.

## Skills

### `gpt-image-2-storyboard`
Prompting GPT Image 2 (`gpt-image-2` / ChatGPT Images 2.0) for film storyboards, short-film frames, and commercial/ad creative — through three expert lenses (film director/DP + advertising art director + JSON prompt engineer).

- Prose **and** JSON prompt formulas
- Full cinematography vocabulary (shot sizes, angles, lenses, lighting, film stocks, composition)
- Advertising art-direction playbook (hero framing, exact in-image text, brand palette, negative space)
- Character/scene **consistency pipeline** (reference sheet → multi-image roles → three-sentence edit)
- Model capabilities, limits, and the noise/grid bug workaround

### `seedance-2-cinematic-motion`
Prompting Seedance 2.0 (ByteDance, `doubao-seedance-2.0`) for image-to-video — camera moves, VFX/atmosphere, native synchronized audio (dialogue lip-sync, SFX, music beat-sync), and multi-shot consistency.

- 5 Iron Rules + the **CRAFT** prompt framework
- Full camera-movement table and audio syntax (`[AUDIO: Xs]`, `@` references, beat-sync)
- Failure-mode fixes (morphing, jitter, lip-sync lag)
- End-to-end storyboard-grid → finished-clip workflow (first/last-frame + continuity chaining)

Each skill ships `SKILL.md` + `reference.md` (deep reference) + `templates.md` (copy-paste prompts).

## Install

Copy a skill folder into your Claude Code skills directory:

```bash
# user-level (all projects)
cp -R .claude/skills/* ~/.claude/skills/

# or keep them project-scoped under .claude/skills/ (as in this repo)
```

The skill activates automatically when you work on prompts for either tool, or invoke it with `/gpt-image-2-storyboard` / `/seedance-2-cinematic-motion`.

## Notes

Exact API specs (resolutions, parameters, pricing) were compiled June 2026 from secondary sources (incl. arXiv:2604.14148 for Seedance 2.0) — verify against current vendor docs before relying on exact numbers. Each skill flags this inline.
