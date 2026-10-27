"""Build Google Flow prompts from a shot list, and lint the shot list for the channel's rhythm rules.

  python prompts.py shots.json             -> prompts.json (for scripts/flow/batch.mjs) + lint report on stdout
  python prompts.py shots.json --strict    -> exit 1 if the lint finds an error

shots.json = [ {"i": 1, "sentence": "...", "family": "scene", "scene": "the character stands at a frosted window, back to viewer",
                "composition": "wide", "dark": false, "file": "F01"}, ... ]
  family: scene | icon | schema | metaphor | map | card | chart | title      (card/chart/title are rendered by code: no prompt)
  composition (optional, rotated automatically if missing): wide | medium | close | cutaway | overhead | pov
  Flow prompts are built only for scene / icon / schema / metaphor / map.

A STYLE dict at the top holds the channel's house style; edit it once per channel, never per prompt.
"""
import json, re, sys, itertools

STYLE = {
    "prefix": "Modern storybook illustration, soft textured pencil shading, gentle ambient lighting, clean minimalist composition, generous empty space, 16:9 wide format.",
    "character": "Recurring character: a whimsical figure with a smooth matte white egg for a head, small dark dot eyes and thin expressive eyebrows, thin stick-figure arms and legs, wearing a simple dusty-blue t-shirt and dark mittens, with large vintage over-ear headphones in warm orange-brown leather tones around the egg head. Keep this exact character design in every image.",
    "setting": "",   # one sentence, identical in every scene prompt, e.g. "Setting: a small Antarctic research station of three plywood modules on a white plateau."
    "scene_bg": "Full coloured set with simple flat shapes and a soft gradient sky or wall, the character small to medium in the frame.",
    "insert_bg": "Plain cream-coloured paper background, nothing else drawn around the subject, the subject centred with generous empty space.",
    "dark": "Dark variant: same drawing style, but a dark slate-blue background instead of cream, with a single warm orange light source.",
    "suffix": "no text, no letters, no numbers, no speech bubbles, no signs, no labels, no watermark.",
}
COMPOSITIONS = {
    "wide": "Wide shot, the whole set visible, horizon line low,",
    "medium": "Medium shot, waist up, the set suggested behind,",
    "close": "Close-up on hands and one object, the face out of frame,",
    "cutaway": "Cutaway view as if one wall were removed, the inside drawn like a dollhouse,",
    "overhead": "Overhead view looking straight down,",
    "pov": "First-person point of view, the character's mitten hands visible at the bottom of the frame,",
}
FAMILY_TEMPLATE = {
    "scene": "{comp} {scene}. {scene_bg}",
    "icon": "A single isolated object: {scene}. {insert_bg} Thick clean outline, flat pastel fill.",
    "schema": "Simple explanatory diagram: {scene}. {insert_bg} Thin outlines, two or three flat colours, thick coloured arrows where motion matters.",
    "metaphor": "Visual metaphor, drawn literally: {scene}. {insert_bg}",
    "map": "Simple flat map silhouette: {scene}. {insert_bg} One red pin, no place names.",
}
BANNED = ["talking", "talks", "calling", "says", "saying", "speaks", "speaking", "conversation", "sign ", "signs", "label", "poster", "screen showing",
          "reads ", "written", "writing", "text", "clock showing", "gauge reading", "number", "digits", "letters", "caption", "subtitle"]
DATA = {"card", "chart", "map"}; INSERT = {"icon", "schema", "metaphor", "map", "card", "chart", "title"}

def tokens(s): return set(re.findall(r"[a-z]{4,}", s.lower()))

def lint(shots, data_every=14):
    errs, warns = [], []
    run = 0
    for k, s in enumerate(shots):
        fam = s["family"]
        run = run + 1 if fam == "scene" else 0
        if run == 4: errs.append(f"#{s['i']}: 4 scenes in a row, insert an icon, schema or data visual before")
        if fam in FAMILY_TEMPLATE:
            low = " " + s.get("scene", "").lower() + " "
            hit = [b for b in BANNED if b in low]
            if hit: errs.append(f"#{s['i']}: banned words {hit} in scene text (they trigger bubbles or text)")
            if not s.get("scene"): errs.append(f"#{s['i']}: empty scene description")
        if k > 0 and fam in DATA and shots[k - 1]["family"] in DATA: warns.append(f"#{s['i']}: two data visuals in a row, put a scene between")
        for j in range(max(0, k - 10), k):
            o = shots[j]
            if o["family"] == fam and fam in FAMILY_TEMPLATE and o.get("composition") == s.get("composition"):
                a, b = tokens(o.get("scene", "")), tokens(s.get("scene", ""))
                if a and b and len(a & b) / len(a | b) > 0.6: warns.append(f"#{s['i']}: near-duplicate of #{o['i']} (same composition, same words)")
    last = -1
    for k, s in enumerate(shots):
        if s["family"] in DATA | {"chart"}: last = k
        elif k - last > data_every: warns.append(f"#{s['i']}: {k - last} shots since the last data visual (max {data_every})"); last = k
    cards_without = [s["i"] for s in shots if s["family"] == "card" and not s.get("card", {}).get("icon")]
    if cards_without: errs.append(f"cards without an icon: {cards_without} (use cards.card with an icon)")
    return errs, warns

def build(shots):
    out, comps = [], itertools.cycle(["wide", "medium", "close", "cutaway", "overhead", "pov"])
    for s in shots:
        fam = s["family"]
        if fam not in FAMILY_TEMPLATE: continue
        comp = s.get("composition") or (next(comps) if fam == "scene" else "")
        body = FAMILY_TEMPLATE[fam].format(comp=COMPOSITIONS.get(comp, ""), scene=s["scene"].rstrip("."), scene_bg=STYLE["scene_bg"], insert_bg=STYLE["insert_bg"])
        parts = [STYLE["prefix"], STYLE["character"] if fam in ("scene", "metaphor") else "", STYLE["setting"] if fam == "scene" else "", body,
                 STYLE["dark"] if s.get("dark") else "", STYLE["suffix"]]
        out.append({"file": s.get("file") or f"F{s['i']:03d}", "i": s["i"], "family": fam, "prompt": re.sub(r"\s+", " ", " ".join(p for p in parts if p)).strip()})
    return out

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "shots.json"
    shots = json.load(open(src, encoding="utf-8"))
    errs, warns = lint(shots)
    for e in errs: print("ERROR ", e)
    for w in warns: print("warn  ", w)
    prompts = build(shots)
    json.dump(prompts, open("prompts.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    fams = {}
    for s in shots: fams[s["family"]] = fams.get(s["family"], 0) + 1
    print(f"{len(prompts)} Flow prompts written to prompts.json | families: {fams} | {len(errs)} errors, {len(warns)} warnings")
    if "--strict" in sys.argv and errs: sys.exit(1)
