"""Builds shots.json from script.md: one line of the script = one shot, zipped with the shot specs of SPECS below.
This file is the worked example of the appendix episode (The Hidden Bargain, 28 Oct 2026, 100 shots, 47 Flow images, 9 min 43):
copy it into the video folder and replace SPECS (one list per chapter, one spec per script line, same count or the assert fails).

  python make_shots.py            -> shots.json + chapters.json (first shot index of each chapter) + files.json (key -> Flow file)

Spec vocabulary:
  S(key, scene, comp, dark=False, costume=None, nochar=False)   Flow scene with the recurring pair (same key = same image, built once, held over consecutive lines)
  M(key, kind, scene, comp=None, dark=False)                     Flow insert without character: kind = schema | metaphor | icon
  H(spec, dark=False)                                            hand-drawn insert by code (hand-drawn-visuals skill, references/spec-format.md)
  T(title, sub)                                                  chapter title card (code), shown while the chapter's first line is spoken
Flow files are numbered F01, F02... in order of first appearance. Scene texts describe their own place (bathroom, savannah, lab)
and never use the words that make Flow draw text (sign, label, poster, map, written, number...) ; objects that carry text are
"plain", "blank", "unmarked". After the voice is generated, copy timing.json starts into shots.json ("start") before prompts.py.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
NIGHT = "barefoot, a grey wool blanket over the shoulders"
MORNING = "barefoot, the grey blanket folded over one arm"
LABCOATS = "barefoot, both wearing white lab coats over the fur tunics"
HOSPITAL = "barefoot, the woman in a pale paper hospital gown over her tunic, the man in a white lab coat"

def S(key, scene, comp, dark=False, costume=None, nochar=False):
    d = {"family": "scene", "key": key, "scene": scene, "composition": comp, "dark": dark}
    if costume: d["costume"] = costume
    if nochar: d["nochar"] = True
    return d
def M(key, kind, scene, comp=None, dark=False):
    d = {"family": kind, "key": key, "scene": scene, "dark": dark}
    if comp: d["composition"] = comp
    return d
def H(spec, dark=False): return {"family": "html", "html": spec, "dark": dark}
def T(title, sub): return H({"type": "title", "title": title, "sub": sub})

# ---- the two recurring settings (copied into the prompt by the "scene" text; the brief setting sentence is added by prompts.py)
BATH = "a small modern bathroom at night lit by a single dim night light, deep blue shadows, white tiles, a round mirror, a chrome tap"
SAV = "an East African savannah, acacia trees, a dry riverbed, warm light"
KITCH = "a bright modern kitchen, a chrome tap over a steel sink, daylight"

SPECS = {
 1: [
  S("sink", f"the man caveman gripping the edge of a bathroom sink with both hands, head hanging, pale and sweaty, the woman asleep through a doorway behind, {BATH}", "wide", costume=NIGHT),
  S("sink", f"the man caveman gripping the edge of a bathroom sink with both hands, head hanging, pale and sweaty, the woman asleep through a doorway behind, {BATH}", "wide", costume=NIGHT),
  S("cup", f"seen from the man's own eyes looking down, his two cupped cartoon hands held under a running chrome tap, water pooling in the palms, {BATH}", "pov", costume=NIGHT),
  M("emptyhouse", "metaphor", "a cutaway of an empty cartoon house in bright daylight, bare rooms, bare shelves, one lone cardboard box on the floor, dust floating in sunbeams, a moving van driving away seen through the window", "cutaway"),
  S("sink", f"the man caveman gripping the edge of a bathroom sink with both hands, head hanging, pale and sweaty, the woman asleep through a doorway behind, {BATH}", "wide", costume=NIGHT),
  M("belly", "schema", "a flat cartoon belly outline, the large intestine drawn as one thick upside-down U tube, a tiny worm-shaped nub hanging from its lower right end, circled in red"),
  M("belly", "schema", "a flat cartoon belly outline, the large intestine drawn as one thick upside-down U tube, a tiny worm-shaped nub hanging from its lower right end, circled in red"),
  H({"type": "card", "icon": "hourglass", "big": "150 YEARS", "small": "declared useless", "layout": "left", "colour": "terra"}),
 ],
 2: [
  T("THE USELESS ORGAN VERDICT", "chapter two"),
  S("darwin", "a simplified flat cartoon figure of a Victorian naturalist, long white beard, black coat, few facial details, seen in profile at a wooden desk, a thick closed leather book with a plain cover under his hand, a quill in an inkpot, an oil lamp, shelves of jars behind", "medium", nochar=True),
  M("shrink", "schema", "a large round fermentation pouch on a herbivore gut on the left, a thick arrow pointing right, a much smaller gut with a tiny thin tube on the right"),
  M("orang", "icon", "a cartoon orangutan with long orange fur sitting on a branch, one hand on its belly"),
  S("classroom", "the pair sitting at small school desks in a classroom, looking up at a big picture of the human digestive system painted on the wall with the appendix as a tiny grey stub circled in red, a surgeon and a teacher standing beside it nodding", "wide"),
  S("magnifier", "the pair leaning over a wooden table, the man holding a huge magnifying glass over a tiny pink tube, the woman squinting beside him, a modern study with shelves of plain unmarked books, jars and plants", "medium"),
  S("magnifier", "the pair leaning over a wooden table, the man holding a huge magnifying glass over a tiny pink tube, the woman squinting beside him, a modern study with shelves of plain unmarked books, jars and plants", "medium"),
  H({"type": "symbol", "icon": "door-closed", "caption": "a locked room", "colour": "blue"}),
  S("magnifier", "the pair leaning over a wooden table, the man holding a huge magnifying glass over a tiny pink tube, the woman squinting beside him, a modern study with shelves of plain unmarked books, jars and plants", "medium"),
 ],
 3: [
  T("THE POUCH WE INHERITED", "chapter three"),
  H({"type": "list", "title": "WHATEVER THE SEASON ALLOWS", "items": [{"icon": "carrot", "text": "roots"}, {"icon": "leaf", "text": "bitter leaves"}, {"icon": "apple", "text": "unripe fruit"}, {"icon": "bone", "text": "a scavenged carcass"}]}),
  S("riverbed", f"the pair walking along a dry riverbed, the man carrying a root over his shoulder, the woman scooping brown water from a muddy pool with one hand, {SAV}", "wide"),
  M("gut", "schema", "a thick upside-down U tube, a short thin coiled tube joining it at the lower right, the small round pouch where they meet coloured orange"),
  M("caecum", "schema", "a zoomed view of the round pouch where the thin tube joins the thick tube, a narrow closed pink nub hanging from its bottom, a dotted circle around the nub"),
  H({"type": "timeline", "title": "OLDER THAN ANY APE", "start": "80 MILLION YEARS AGO", "end": "TODAY", "marks": [{"at": 0.0, "label": "first appendix", "colour": "terra"}, {"at": 0.69, "label": "first apes", "colour": "blue"}, {"at": 0.99, "label": "us", "colour": "sage"}]}),
  S("deadend", "the pair standing at the end of a short dirt track that stops abruptly in a patch of grass, beside a plain country road with a few tiny cars, the man pointing at the empty track, open countryside in daylight", "wide"),
 ],
 4: [
  T("THE IMMUNE WALL", "chapter four"),
  M("wall", "schema", "a microscope view of the appendix wall cut open, the lining packed with dense clusters of small round purple cells, a few green round microbes in the hollow centre"),
  H({"type": "card", "icon": "trending-down", "big": "AFTER 30", "small": "the tissue thins out", "layout": "top", "colour": "blue"}),
  S("guard", f"the man caveman standing in a tiny wooden guard booth at a gate in a fence, waving through a line of smiling round green blob creatures, one spiky purple blob held back by his raised palm, {SAV}", "wide"),
  S("guard", f"the man caveman standing in a tiny wooden guard booth at a gate in a fence, waving through a line of smiling round green blob creatures, one spiky purple blob held back by his raised palm, {SAV}", "wide"),
  H({"type": "card", "icon": "bug", "big": "38 TRILLION", "small": "bacteria in your gut", "layout": "top", "colour": "sage"}),
  H({"type": "symbol", "icon": "circle-help", "caption": "a bigger riddle", "colour": "orange"}),
  S("sidecave", "the pair standing dry inside a small side cave, a fast river rushing past the cave mouth with white foam, the man peeking out", "medium"),
 ],
 5: [
  T("THE FIRE HOSE MECHANISM", "chapter five"),
  S("sick", "close on the woman caveman curled up on a fur by a campfire holding her belly, eyes shut, the man's hand offering a gourd of water from the edge of the frame, firelight at night, an East African savannah", "close", dark=True),
  H({"type": "symbol", "icon": "amphora", "caption": "a bad batch of water", "colour": "terra"}),
  S("wildhose", f"the man caveman gripping a red fire hose that sprays a wild jet of water in every direction, the woman leaping out of the way with wide eyes, {SAV}", "wide"),
  S("wildhose", f"the man caveman gripping a red fire hose that sprays a wild jet of water in every direction, the woman leaping out of the way with wide eyes, {SAV}", "wide"),
  H({"type": "compare", "left": "1 MILLION+ DEATHS", "right": "500,000 CHILDREN", "icon_left": "skull", "icon_right": "baby", "sign": "of which", "colour": "grey", "colour2": "terra"}, dark=True),
  H({"type": "compare", "left": "1 MILLION+ DEATHS", "right": "500,000 CHILDREN", "icon_left": "skull", "icon_right": "baby", "sign": "of which", "colour": "grey", "colour2": "terra"}, dark=True),
  S("wildhose", f"the man caveman gripping a red fire hose that sprays a wild jet of water in every direction, the woman leaping out of the way with wide eyes, {SAV}", "wide"),
  M("flush", "schema", "a cutaway of a gut tube with a rushing wave of blue water sweeping along it, carrying both smiling green round microbes and spiky purple microbes toward the exit"),
  M("floodtown", "metaphor", "an aerial view of a small cartoon town after a flood, muddy empty streets, puddles, no people, a few overturned carts, plain house fronts, no shop fronts", "overhead"),
  H({"type": "symbol", "icon": "trophy", "caption": "first one in wins", "colour": "orange"}),
  S("emptystreet", "the pair standing in the middle of an empty muddy street of a small cartoon town after a flood, looking around with raised eyebrows, puddles on the ground, plain house fronts, no shop fronts", "medium"),
  S("emptystreet", "the pair standing in the middle of an empty muddy street of a small cartoon town after a flood, looking around with raised eyebrows, puddles on the ground, plain house fronts, no shop fronts", "medium"),
 ],
 6: [
  T("WHAT DUKE REVEALED IN 2007", "chapter six"),
  H({"type": "card", "icon": "file-text", "big": "6 PAGES", "small": "J. Theor. Biol., 2007", "layout": "left", "colour": "blue"}),
  S("mossstone", "the pair crouching at the edge of a stream, the woman running one finger over a grey river stone covered with a thin film of bright green moss, the man leaning in close, water flowing around the stone", "close"),
  M("biofilm", "schema", "a cross-section of the large intestine drawn as a thick upside-down U tube, a thin green film lining it, the film drawn thickest inside the small tube at the lower right, a red pin on that tube"),
  S("sidecave", "the pair standing dry inside a small side cave, a fast river rushing past the cave mouth with white foam, the man peeking out", "medium"),
  S("sidecave", "the pair standing dry inside a small side cave, a fast river rushing past the cave mouth with white foam, the man peeking out", "medium"),
  M("bunker", "metaphor", "a cutaway of a small underground bunker with a round steel door under a grassy hill, a storm and rain raging above, smiling green round microbes safe inside", "cutaway", dark=True),
  M("reseed", "schema", "a zoomed cutaway of just the junction, the small side tube and the first stretch of the empty gut, a stream of smiling green round microbes pouring out of the side tube, thick green arrows"),
  S("noexperiment", "the pair in a modern lab in front of a corkboard covered with pinned blank cards and red string, an empty picture frame pinned in the centre, the woman shrugging with open palms, the man pointing at the empty frame", "medium", costume=LABCOATS),
  H({"type": "symbol", "icon": "lightbulb", "caption": "not a flaw", "colour": "orange"}),
  M("caecum", "schema", "a zoomed view of the round pouch where the thin tube joins the thick tube, a narrow closed pink nub hanging from its bottom, a dotted circle around the nub"),
 ],
 7: [
  T("THE HIDDEN COST OF A CLEAN WORLD", "chapter seven"),
  S("hospital", "the woman caveman sitting on a hospital bed with a small square bandage low on the right of her belly, the man at the bedside holding a small jar, a modern hospital room with plain walls, no screens, no monitors", "medium", costume=HOSPITAL),
  S("cdiffstreet", "a spiky purple blob creature with angry eyebrows strolling alone down the empty muddy street of a small cartoon town at dusk, carrying a suitcase, the pair peeking out from behind a doorway, puddles on the ground, plain house fronts", "wide", dark=True),
  H({"type": "card", "icon": "users", "big": "254 PATIENTS", "small": "2005 to 2007", "layout": "top", "colour": "blue"}),
  S("hospital", "the woman caveman sitting on a hospital bed with a small square bandage low on the right of her belly, the man at the bedside holding a small jar, a modern hospital room with plain walls, no screens, no monitors", "medium", costume=HOSPITAL),
  H({"type": "card", "icon": "shield-check", "big": "HALF", "small": "the relapse risk, at most", "layout": "top", "colour": "sage"}),
  S("kitchen", "close on the woman caveman's two cupped cartoon hands under a running chrome kitchen tap, clear water pooling in the palms, the man's hand setting a small plain white pill bottle on the steel sink edge, a bright modern kitchen, daylight", "close"),
  M("emptybunker", "metaphor", "an empty concrete bunker room with its round steel door open, sunlight pouring in, dust in the air, bare shelves", "cutaway"),
  H({"type": "symbol", "icon": "bell", "caption": "subscribe", "colour": "terra"}),
  S("lantern", "the pair walking at night holding a lantern toward a huge tree whose many branches glow, small animal silhouettes sitting on the branches, an East African savannah at night, the lantern and the glowing branches as the only lights", "wide", dark=True),
  S("lantern", "the pair walking at night holding a lantern toward a huge tree whose many branches glow, small animal silhouettes sitting on the branches, an East African savannah at night, the lantern and the glowing branches as the only lights", "wide", dark=True),
 ],
 8: [
  T("WHAT 533 MAMMALS REVEALED IN 2017", "chapter eight"),
  S("scroll", "seen from directly above, the woman caveman unrolling a huge paper scroll across a long wooden table, rows and rows of tiny animal drawings on it, the man counting on his fingers, a museum archive room", "overhead"),
  M("onedot", "schema", "a simple tree diagram with one single red dot at the base of the trunk and the branches above fading to pale dotted lines"),
  M("manydots", "schema", "the same simple tree diagram with many bright red dots scattered on separate branches all over the crown"),
  S("mammals", f"the pair standing in a circle with a cartoon rat, a monkey and a kangaroo, each animal with a tiny pink worm-shaped nub showing on its lower belly, {SAV}", "medium"),
  H({"type": "compare", "left": "29 GAINS", "right": "12 LOSSES", "icon_left": "plus", "icon_right": "minus", "sign": "vs", "colour": "sage", "colour2": "terra"}),
  S("huts", f"the pair stacking stones to build a small round stone hut, a row of five identical finished stone huts behind them, {SAV}", "wide"),
  M("wall", "schema", "a microscope view of the appendix wall cut open, the lining packed with dense clusters of small round purple cells, a few green round microbes in the hollow centre"),
  S("darwin", "a simplified flat cartoon figure of a Victorian naturalist, long white beard, black coat, few facial details, seen in profile at a wooden desk, a thick closed leather book with a plain cover under his hand, a quill in an inkpot, an oil lamp, shelves of jars behind", "medium", nochar=True),
 ],
 9: [
  T("THE FINAL VERDICT", "chapter nine"),
  S("pain", "the man caveman doubled over clutching the lower right of his belly with a pained face and sweat drops, the woman holding his shoulder with worried eyes, under a dark stormy sky over the savannah, the first drops of rain", "medium", dark=True),
  M("blocked", "schema", "a diagram of the narrow pink tube with its opening plugged by a hard dark pellet, the wall swollen and red, small pressure lines radiating outward"),
  M("blocked", "schema", "a diagram of the narrow pink tube with its opening plugged by a hard dark pellet, the wall swollen and red, small pressure lines radiating outward"),
  M("jammed", "metaphor", "a cutaway of the underground bunker with its only round steel door jammed by a boulder, cracks spreading across the walls", "cutaway", dark=True),
  S("office", "a modern office with grey filing cabinets with plain blank drawer fronts, a small simplified cartoon figure in a tie at a desk under tall stacks of plain blank folders, a window with pine trees", "wide", nochar=True),
  H({"type": "bar", "title": "Lifetime risk of appendicitis", "labels": ["MEN", "WOMEN"], "values": [8.6, 6.7], "unit": "%", "colour": "terra"}),
  S("pain", "the man caveman doubled over clutching the lower right of his belly with a pained face and sweat drops, the woman holding his shoulder with worried eyes, under a dark stormy sky over the savannah, the first drops of rain", "medium", dark=True),
  S("handshake", f"the pair shaking hands across a campfire at night with serious faces, {SAV} at night", "medium", dark=True),
  H({"type": "card", "icon": "bed", "big": "1 IN 13", "small": "a fever and a scar", "layout": "left", "colour": "terra"}),
  H({"type": "symbol", "icon": "scale", "caption": "a trade off", "colour": "orange"}),
  S("kitchen", "close on the woman caveman's two cupped cartoon hands under a running chrome kitchen tap, clear water pooling in the palms, the man's hand setting a small plain white pill bottle on the steel sink edge, a bright modern kitchen, daylight", "close"),
  S("letgo", "the man caveman opening both hands and letting a small grey cloud float away out of a window, the woman smiling beside him, a modern living room", "medium"),
  S("letgo", "the man caveman opening both hands and letting a small grey cloud float away out of a window, the woman smiling beside him, a modern living room", "medium"),
  M("seedbank", "metaphor", "a cosy underground vault with wooden shelves lined with rows of small plain glass jars with no markings, full of seeds, warm lamp light", "cutaway"),
 ],
 10: [
  S("morningsink", "seen from behind the man's shoulder at the bathroom sink, his rested face reflected in the round mirror, white tiles, a chrome tap, soft morning daylight", "medium", costume=MORNING),
  S("morningcup", "seen from the man's own eyes looking down into the sink, his two cupped cartoon hands under the running chrome tap, clear water catching the light, in the small modern bathroom, white tiles, soft morning daylight", "pov", costume=MORNING),
  M("belly", "schema", "a flat cartoon belly outline, the large intestine drawn as one thick upside-down U tube, a tiny worm-shaped nub hanging from its lower right end, circled in red"),
  M("release", "schema", "a flat cartoon belly outline in dawn colours, the thick gut tube inside it, the small side tube releasing a gentle stream of smiling green round microbes that spread along the whole gut, soft orange arrows"),
  H({"type": "symbol", "icon": "shield-check", "caption": "nothing worse moved in", "colour": "sage"}),
  S("doorway", "the pair side by side in a bathroom doorway in morning light, the woman pointing at the lower right of the man's belly, both smiling", "medium", costume=MORNING),
  H({"type": "symbol", "icon": "refresh-cw", "caption": "restocked", "colour": "sage"}),
  S("doorway", "the pair side by side in a bathroom doorway in morning light, the woman pointing at the lower right of the man's belly, both smiling", "medium", costume=MORNING),
  H({"type": "symbol", "icon": "message-circle", "caption": "tell me in the comments", "colour": "terra"}),
 ],
}

def chapters():
    text = (HERE / "script.md").read_text(encoding="utf-8")
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, *lines = block.strip().splitlines()
        m = re.match(r"Chapter (\d+) — (.+)", head)
        out.append((int(m.group(1)), m.group(2).strip(), [l.strip() for l in lines if l.strip()]))
    return out

def main():
    shots, chap_index, files = [], [], {}
    for num, title, lines in chapters():
        specs = SPECS[num]
        assert len(specs) == len(lines), f"chapter {num}: {len(lines)} lines but {len(specs)} specs"
        chap_index.append({"chapter": num, "title": title, "shot": len(shots) + 1})
        for line, spec in zip(lines, specs):
            s = {"i": len(shots) + 1, "sentence": line, "family": spec["family"]}
            if "key" in spec:
                files.setdefault(spec["key"], f"F{len(files) + 1:02d}")
                s["file"] = files[spec["key"]]; s["scene"] = spec["scene"]
                if spec.get("composition"): s["composition"] = spec["composition"]
                if spec.get("nochar"): s["nochar"] = True
                if spec.get("costume"): s["costume"] = spec["costume"]
            if spec["family"] == "html": s["html"] = spec["html"]
            if spec.get("dark"): s["dark"] = True
            shots.append(s)
    (HERE / "shots.json").write_text(json.dumps(shots, indent=1, ensure_ascii=False), encoding="utf-8")
    (HERE / "files.json").write_text(json.dumps(files, indent=1), encoding="utf-8")
    (HERE / "chapters.json").write_text(json.dumps(chap_index, indent=1, ensure_ascii=False), encoding="utf-8")
    fam = {}
    for s in shots: fam[s["family"]] = fam.get(s["family"], 0) + 1
    print(f"{len(shots)} shots, {len(files)} Flow images, families {fam}")

if __name__ == "__main__":
    main()
