# Faceless Video Skills

Two Claude skills for producing faceless YouTube videos end to end: script, image list, automatic image generation in Google Flow, slideshow assembly on an AI voice, thumbnail and a complete publication sheet.

| Skill | Format | Length | Reference channel |
|---|---|---|---|
| `why-explainer-video` | "Why Evolution Made…" science explainer: a human paradox opened by a second-person scene, resolved by named studies, reframed as a trade-off | 20 min, 3,300–3,600 words | Apefully |
| `survival-story-video` | Second-person survival story, day by day, with real technical facts and an open ending | 10–12 min, 1,500–1,700 words | "Bunker Survival 1 Year" |

Both skills share the same production method: one static image per moment (no animation), a recurring hand-drawn character, numbers and charts rendered by code, images generated in Google Flow through a Playwright-driven Chrome, assembly with ffmpeg on the voice timing.

The skills are written in French (the instructions Claude reads); the videos they produce are in English.

## Install

**Claude Code**: copy a skill folder into your skills directory, then start a new session.

```bash
git clone https://github.com/<you>/faceless-video-skills
cp -r faceless-video-skills/skills/why-explainer-video ~/.claude/skills/
cp -r faceless-video-skills/skills/survival-story-video ~/.claude/skills/
```

**claude.ai / Claude desktop**: zip a skill folder (the folder itself as the root of the archive) and upload it in Settings → Skills.

## What each skill contains

```
<skill>/
├── SKILL.md                     # formula, workflow, calibrated structure, writing rules, QC checklist
├── references/
│   ├── script-template.md       # mechanics of each section, word budgets
│   ├── flow-automation.md       # automatic image generation in Google Flow + house style prefix
│   ├── publication(-seo).md     # title, thumbnail, chapters, description, tags, category, Studio settings
│   └── …                        # fact bank, beat sheet, visual pipeline, topic bank
└── scripts/flow/
    ├── browser.mjs              # opens a real Chrome on Google Flow with a persistent profile (CDP :9222)
    ├── login.mjs                # waits for YOU to sign in (never types credentials)
    ├── batch.mjs                # pastes every prompt of prompts.json, downloads each image, resumable
    ├── cdp.mjs                  # shared Playwright attach helper
    └── convert.py               # JPEG → PNG for the build scripts
```

## Automatic image generation (Google Flow)

Google Flow has no API. The scripts drive a real Chrome instead:

```bash
npm i playwright                                   # once, anywhere; set PLAYWRIGHT_DIR to that folder
node skills/why-explainer-video/scripts/flow/browser.mjs &   # keep it running
node skills/why-explainer-video/scripts/flow/login.mjs       # sign in by hand in the window
node skills/why-explainer-video/scripts/flow/batch.mjs prompts.json flow/my-video
python skills/why-explainer-video/scripts/flow/convert.py flow/my-video
```

`prompts.json` is `[{"file": "F01", "prompt": "<style prefix> <scene>"}, …]`. Measured: about 25 s per image, 65 images in 27 minutes. Requirements: Node 18+, Chrome, a Google account with Flow (AI Pro or Ultra credits), Python 3 with Pillow.

## Voice and assembly

The skills assume an AI voice with character-level timing (ElevenLabs `with-timestamps`, or edge-tts word boundaries as a free fallback) and ffmpeg concatenation of one image per sentence or per moment. Keep API keys in a local `.env`; nothing in this repository reads or stores them.

## License

MIT. See `LICENSE`.
