"""Merge all ape_shots/<id>/classes.json + patterns.md into stats and an example sheet per family.
  python ape_catalogue.py -> ape_catalogue/stats.md, ape_catalogue/<family>.jpg (up to 24 examples each), ape_catalogue/patterns-all.md
"""
import json, pathlib, collections, random, csv
from PIL import Image, ImageDraw, ImageFont

ROOT, OUT = pathlib.Path("ape_shots"), pathlib.Path("ape_catalogue"); OUT.mkdir(exist_ok=True)
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
meta = {}
try:
    for r in csv.DictReader(open("apefully-videos.csv", encoding="utf-8-sig"), delimiter=";"):
        meta[r["url"].rsplit("/", 1)[-1]] = r
except FileNotFoundError: pass

fam_total, per_video, examples, durations = collections.Counter(), {}, collections.defaultdict(list), collections.defaultdict(list)
seq_pairs = collections.Counter()
for d in sorted(ROOT.iterdir()):
    cj, sj = d / "classes.json", d / "shots.json"
    if not (cj.exists() and sj.exists()): continue
    cls = {c["n"]: c for c in json.load(open(cj, encoding="utf-8"))}
    shots = json.load(open(sj))["shots"]; vid = d.name
    cnt = collections.Counter(); prev = None
    for s in shots:
        c = cls.get(s["n"]); fam = c["family"] if c else "unclassified"
        cnt[fam] += 1; durations[fam].append(s["dur"]); examples[fam].append((d / "frames" / s["frame"], f"{vid[:6]} {s['n']:03d}"))
        if prev: seq_pairs[(prev, fam)] += 1
        prev = fam
    per_video[vid] = (cnt, len(shots), sum(s["dur"] for s in shots) / max(1, len(shots)))
    fam_total.update(cnt)

N = sum(fam_total.values())
lines = ["# Apefully : statistiques sur tous les plans classés", "", f"{len(per_video)} vidéos, {N} plans.", "",
         "## Part de chaque famille (tous plans)", "", "| Famille | Plans | Part | Durée moyenne |", "|---|---|---|---|"]
for fam, n in fam_total.most_common():
    lines.append(f"| {fam} | {n} | {100 * n / N:.1f} % | {sum(durations[fam]) / len(durations[fam]):.1f} s |")
data = sum(fam_total[f] for f in fam_total if f.startswith("chart") or f in ("gauge", "timeline", "map", "table"))
lines += ["", f"Visuels de données (chart-*, gauge, timeline, map, table) : **{data}** plans, {100 * data / N:.1f} %, soit un toutes les {N / max(1, data):.0f} images, environ un par minute de vidéo.", "",
          "## Par vidéo", "", "| Vidéo | Titre | Vues | Plans | s/plan | scene | schema | icon | données | title |", "|---|---|---|---|---|---|---|---|---|---|"]
for vid, (cnt, n, avg) in sorted(per_video.items(), key=lambda kv: -int(meta.get(kv[0], {}).get("vues", 0) or 0)):
    m = meta.get(vid, {}); dv = sum(v for f, v in cnt.items() if f.startswith("chart") or f in ("gauge", "timeline", "map", "table"))
    lines.append(f"| {vid} | {m.get('titre', '')[:45]} | {m.get('vues', '')} | {n} | {avg:.1f} | {cnt['scene']} | {cnt['schema']} | {cnt['icon']} | {dv} | {cnt['title']} |")
lines += ["", "## Enchaînements les plus fréquents (famille → famille suivante)", ""]
for (a, b), n in seq_pairs.most_common(12): lines.append(f"- {a} → {b} : {n}")
(OUT / "stats.md").write_text("\n".join(lines), encoding="utf-8")

random.seed(1); W, H = 320, 180
for fam, ex in examples.items():
    pick = random.sample(ex, min(24, len(ex))); rows = (len(pick) + 5) // 6
    sheet = Image.new("RGB", (W * 6, H * rows), "white"); d = ImageDraw.Draw(sheet)
    for i, (p, lab) in enumerate(pick):
        if not p.exists(): continue
        x, y = (i % 6) * W, (i // 6) * H; sheet.paste(Image.open(p).resize((W, H)), (x, y))
        d.rectangle([x, y, x + 120, y + 20], fill="black"); d.text((x + 3, y + 2), lab, font=FONT, fill="yellow")
    sheet.save(OUT / f"{fam}.jpg", quality=80)

allp = ["# Patrons visuels relevés par les agents, vidéo par vidéo", ""]
for d in sorted(ROOT.iterdir()):
    p = d / "patterns.md"
    if p.exists(): allp += [f"## {d.name} — {meta.get(d.name, {}).get('titre', '')[:60]}", "", p.read_text(encoding="utf-8").split("\n", 1)[-1].strip(), ""]
(OUT / "patterns-all.md").write_text("\n".join(allp), encoding="utf-8")
print(len(per_video), "videos", N, "shots ->", OUT)
