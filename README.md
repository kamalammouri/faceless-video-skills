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
git clone https://github.com/kamalammouri/faceless-video-skills
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
│   ├── flow-automation.md       # automatic image generation in Google Flow, house style prefix, no-bubble rules
│   ├── agents.md                # briefs of the six production agents
│   ├── scene-catalogue.md       # what the reference channel shows: shares, patterns, rhythm rules
│   ├── publication(-seo).md     # title, thumbnail, chapters, description, tags, category, Studio settings
│   └── …                        # fact bank, beat sheet, visual pipeline, topic bank
└── scripts/
    ├── cards.py                 # number cards with icons, five layouts
    ├── charts.py                # 24 chart / gauge / timeline / schema patterns measured on the reference channel
    ├── prompts.py               # shot list -> Flow prompts + rhythm lint
    ├── build_slideshow.py       # shot list + voice timing -> mp4
    └── flow/
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

## Number cards with icons (no bare numbers)

`skills/*/scripts/cards.py` renders every number of the script as a card with a hand-drawn icon (clock, calendar, fuel, thermometer, snow, water, food, pills, hourglass, key, radio, fire, plane, battery, wind, sun, moon, heart) in one of five layouts (left, top, stamp, compare, gauge). `python cards.py` writes a demo sheet. `scripts/*/charts.py` adds the 16 data-visual patterns measured on the reference channel (ratio bars, bars with reference line, detached-slice pie, lines, dot grid, scatter, single and double thermometers, cursor gauge, dial, timelines, day-night curve, split comparison, pills); `python charts.py` writes its own demo sheet.

## Production agents

`agents/` holds Claude Code agent definitions (copy them to `.claude/agents/` in your project): `fact-checker`, `visual-director` (shot-list variety audit), `image-qc` (vision check of the contact sheet: speech bubbles, text, wrong character). The full briefs, including Script critic, Prompt auditor and Publication checker, are in each skill's `references/agents.md`, so they work with the plain Agent tool too.

## Reference channel catalogue

`examples/apefully/` holds the measurements made on 30 videos of the reference channel (8,250 shots cut and classified by vision agents): `stats.md` (family shares, per-video table, transitions), one example sheet per family (`scene.jpg`, `schema.jpg`, `timeline.jpg`, `gauge.jpg`…), `patterns-all.md` (the reusable visual patterns noted video by video), and the two scripts that produced them (`ape_shots.py`, `ape_catalogue.py`). The rules derived from it are in each skill's `references/scene-catalogue.md`.

## One shot list, three tools

`shots.json` (format in the header of `scripts/prompts.py`) drives everything: `prompts.py` builds the Google Flow prompts and lints the list against the channel's rhythm rules (no 4 scenes in a row, a data visual at least every 14 shots, no bubble-triggering words, no bare number cards); `build_slideshow.py` assembles the video on the voice timing, rendering cards, charts and titles by code and loading the Flow images by name.

## Voice and assembly

The skills assume an AI voice with character-level timing (ElevenLabs `with-timestamps`, or edge-tts word boundaries as a free fallback) and ffmpeg concatenation of one image per sentence or per moment. Keep API keys in a local `.env`; nothing in this repository reads or stores them.

## License

MIT. See `LICENSE`.
