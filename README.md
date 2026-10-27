# Faceless Video Skills

Two Claude skills for producing faceless YouTube videos end to end: script, image list, automatic image generation in Google Flow, slideshow assembly on an AI voice, thumbnail and a complete publication sheet.

| Skill | Format | Length | Reference channel |
|---|---|---|---|
| `why-explainer-video` | "Why Evolution Made…" science explainer: a human paradox opened by a second-person scene, resolved by named studies, reframed as a trade-off | 20 min, 3,300–3,600 words | Apefully |
| `survival-story-video` | Second-person survival story, day by day, with real technical facts and an open ending | 10–12 min, 1,500–1,700 words | "Bunker Survival 1 Year" |

Both skills start with a two-round brief that asks the user for the character style, the scenario (three angles proposed by a Story architect agent) and the main parameters, then share the same production method: one static image per moment (no animation), a recurring character in the chosen style, numbers and charts rendered by code, images generated in Google Flow through a Playwright-driven Chrome, assembly with ffmpeg on the voice timing.

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
│   ├── brief.md                 # questions asked BEFORE writing: character style, scenario, parameters -> brief.json
│   ├── character-styles.md      # catalogue of character styles (stickman meme, egg + headphones, painted human, caveman duo, thin line)
│   ├── voice.md                 # voice track: Gemini TTS or edge-tts, chosen at the brief
│   ├── agents.md                # briefs of the eight production agents
│   ├── scene-catalogue.md       # what the reference channel shows: shares, patterns, rhythm rules
│   ├── publication(-seo).md     # title, thumbnail, chapters, description, tags, category, Studio settings
│   └── …                        # fact bank, beat sheet, visual pipeline, topic bank
└── scripts/
    ├── cards.py                 # number cards with icons, five layouts
    ├── charts.py                # 24 chart / gauge / timeline / schema patterns measured on the reference channel
    ├── styles.json              # character styles: prefix, character sheet, costume slot, backgrounds, thumbnail template, QC sentence
    ├── prompts.py               # shot list + brief.json -> Flow prompts + rhythm lint
    ├── tts.py                   # shot list + brief.json -> voice.wav + timing.json (Gemini TTS or edge-tts, one clip per shot)
    ├── build_slideshow.py       # shot list + voice timing -> mp4
    └── flow/
    ├── browser.mjs              # opens a real Chrome on Google Flow with a persistent profile (CDP :9222)
    ├── login.mjs                # waits for YOU to sign in (never types credentials)
    ├── batch.mjs                # pastes every prompt of prompts.json, downloads each image, resumable
    ├── cdp.mjs                  # shared Playwright attach helper
    └── convert.py               # JPEG → PNG for the build scripts
```

## Pre-production brief and character styles

Nothing is written before the user has answered two rounds of questions (`references/brief.md`): round 1 asks the subject (if missing), the **character style**, the **voice engine and language** (Gemini TTS or edge-tts) and the deliverable; round 2 shows three scenario angles written by the `story-architect` agent and asks which one to produce. The answers go to `brief.json` in the working folder, and every downstream step reads it.

The character styles live in `scripts/styles.json` (`python scripts/<skill>/prompts.py --styles` lists them): `stickman-meme` (big white round head, rage-comic face, thick outlines, saturated painted sets: the style of the Galon Zéro thumbnails, default), `egg-headphones` (the original cream storybook character), `storybook-human` (painted human protagonist, 1990s animation film look), `caveman-duo`, `thin-line`, or a custom sheet written by the `character-designer` agent. Each style carries its prefix, character sheet with a `{costume}` slot (the costume changes with rank, season or state), backgrounds, dark variant, thumbnail template and the sentence the Image QC agent checks against. `prompts.py` assembles every Flow prompt from the chosen style, so no character description is hard-coded any more.

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

`agents/` holds Claude Code agent definitions (copy them to `.claude/agents/` in your project): `story-architect` (three scenario angles for the user to choose from), `character-designer` (prompt sheet of a custom character), `fact-checker`, `visual-director` (shot-list variety audit), `image-qc` (vision check of the contact sheet against the character sheet of the brief: speech bubbles, text, wrong character). The full briefs, including Script critic, Prompt auditor and Publication checker, are in each skill's `references/agents.md`, so they work with the plain Agent tool too.

## Reference channel catalogue

`examples/apefully/` holds the measurements made on 30 videos of the reference channel (8,250 shots cut and classified by vision agents): `stats.md` (family shares, per-video table, transitions), one example sheet per family (`scene.jpg`, `schema.jpg`, `timeline.jpg`, `gauge.jpg`…), `patterns-all.md` (the reusable visual patterns noted video by video), and the two scripts that produced them (`ape_shots.py`, `ape_catalogue.py`). The rules derived from it are in each skill's `references/scene-catalogue.md`.

`examples/galonzero/` holds the analysis of the French channel Galon Zéro ("Ta vie à chaque grade": 18 videos, 1.6 M views in five weeks): video table, title and description template, the ten-rank structure, and the two-style visual system (stickman-meme split thumbnails, painted human interior), with sample thumbnails and storyboard sheets.

## One shot list, three tools

`shots.json` (format in the header of `scripts/prompts.py`) drives everything: `prompts.py` reads `brief.json` for the style and builds the Google Flow prompts and lints the list against the channel's rhythm rules (no 4 scenes in a row, a data visual at least every 14 shots, no bubble-triggering words, no bare number cards); `build_slideshow.py` assembles the video on the voice timing, rendering cards, charts and titles by code and loading the Flow images by name.

## Voice and assembly

The voice engine is asked at the brief: **Gemini TTS** (the "Generate speech" tool of Google AI Studio, through the Gemini API: studio voices, a style sentence such as "calm, slow, documentary narration", French and English, needs `GEMINI_API_KEY`) or **edge-tts** (free, no key, less steerable). `scripts/tts.py shots.json` synthesises one clip per shot with the chosen engine, concatenates them and writes `voice.wav` plus `timing.json` with the exact start time of every shot, so no timestamp API is needed; a clip is regenerated only when its sentence changes. `build_slideshow.py` then concatenates one image per shot on that track with ffmpeg. Keep `GEMINI_API_KEY` in a local `.env` (git-ignored); `tts.py` reads it from there and nothing else in the repository stores a key. ElevenLabs `with-timestamps` output is still accepted by `build_slideshow.py` as an alternative `timing.json`.

## License

MIT. See `LICENSE`.
