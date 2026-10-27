"""Assemble the slideshow video: one image per shot, held until the next shot's sentence starts, on the voice track.

  python build_slideshow.py shots.json voice.wav timing.json out.mp4 [--flow flow/my-video] [--caption]

shots.json  = the same list as for prompts.py, one entry per shot, in order:
  {"i": 1, "sentence": "...", "family": "scene", "file": "F001"}                       -> flow/<dir>/F001.png (or .jpg)
  {"i": 2, "sentence": "...", "family": "card",  "card": {"icon": "clock", "big": "3:47", "small": "a.m.", "layout": "left"}}
  {"i": 3, "sentence": "...", "family": "chart", "chart": {"fn": "bar_ratio", "args": ["100x", "ROOM AIR", "5% CO2"]}}
  {"i": 4, "sentence": "...", "family": "title", "title": "THE HIDDEN COST"}
  optional on any shot: "start": seconds (overrides timing), "day": "DAY 68" (corner label), "dark": true (cards/charts dark variant)
timing.json = either {"chars": "...", "end": [t0, t1, ...]} (ElevenLabs with-timestamps, per character)
              or a list of sentence start times [0.0, 4.2, ...] (one per shot)
Missing Flow images fall back to a cream caption card so the build never stops; the list of missing files is printed.
"""
import json, pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cards, charts

W, H = 1920, 1080
CREAM, INK, GREY = (245, 239, 224), (30, 27, 22), (150, 145, 135)
def font(size, bold=False):
    try: return ImageFont.truetype("C:/Windows/Fonts/" + ("segoeprb.ttf" if bold else "segoepr.ttf"), size)
    except OSError: return ImageFont.load_default()

def starts_from_timing(shots, timing):
    if isinstance(timing, list): return [float(t) for t in timing]
    chars, end = timing["chars"], timing["end"]; pos, out = 0, []
    for s in shots:
        if "start" in s: out.append(float(s["start"])); continue
        k = chars.find(s["sentence"][:25], pos)          # locate the sentence in the voiced text
        out.append(end[k - 1] if k > 0 else (out[-1] if out else 0.0)); pos = max(pos, k)
    return out

def title_card(text, dark=False):
    im = Image.new("RGB", (W, H), (38, 48, 60) if dark else CREAM); d = ImageDraw.Draw(im)
    d.text((W // 2, H // 2), text, font=font(120, True), fill=CREAM if dark else INK, anchor="mm"); return im

def fallback(text):
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im); words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font(64)) <= 1500: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); y = H // 2 - 40 * len(lines)
    for i, ln in enumerate(lines): d.text((W // 2, y + i * 80), ln, font=font(64), fill=INK, anchor="mm")
    return im

def overlay(im, sentence, day, caption):
    d = ImageDraw.Draw(im, "RGBA"); f = font(40)
    if caption:
        tw = d.textlength(sentence, font=f); lines = [sentence]
        if tw > 1700:
            words, l1 = sentence.split(), ""
            while words and d.textlength(l1 + " " + words[0], font=f) < 1600: l1 = (l1 + " " + words.pop(0)).strip()
            lines = [l1, " ".join(words)]
        y = H - 70 - 50 * (len(lines) - 1)
        for i, ln in enumerate(lines):
            w = d.textlength(ln, font=f); d.rounded_rectangle([W // 2 - w // 2 - 24, y + i * 50 - 26, W // 2 + w // 2 + 24, y + i * 50 + 26], 14, fill=(245, 239, 224, 215))
            d.text((W // 2, y + i * 50), ln, font=f, fill=INK, anchor="mm")
    if day: d.text((50, 44), day, font=font(30, True), fill=(30, 27, 22, 170), anchor="lm")
    d.text((W - 50, 44), "SUBSCRIBE", font=font(26), fill=(30, 27, 22, 110), anchor="rm")
    return im

def render(s, flow_dir):
    fam = s["family"]
    if fam == "card": c = dict(s["card"]); return cards.card(c.pop("icon"), c.pop("big"), c.pop("small", ""), dark=s.get("dark", False), **c)
    if fam == "chart": c = s["chart"]; return getattr(charts, c["fn"])(*c.get("args", []), **c.get("kwargs", {}))
    if fam == "title": return title_card(s["title"], s.get("dark", False))
    for ext in (".png", ".jpg"):
        f = flow_dir / f"{s.get('file') or f'F{s['i']:03d}'}{ext}"
        if f.exists(): return Image.open(f).convert("RGB").resize((W, H))
    return None

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    shots_f, voice, timing_f, out = a[0], a[1], a[2], a[3] if len(a) > 3 else "slideshow.mp4"
    flow_dir = pathlib.Path(sys.argv[sys.argv.index("--flow") + 1]) if "--flow" in sys.argv else pathlib.Path("flow")
    caption = "--caption" in sys.argv
    shots = json.load(open(shots_f, encoding="utf-8")); timing = json.load(open(timing_f, encoding="utf-8"))
    starts = starts_from_timing(shots, timing)
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    hh, mm, ss = subprocess.run([FF, "-i", voice], capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0].split(":")
    dur = 3600 * int(hh) + 60 * int(mm) + float(ss)
    ends = starts[1:] + [dur]
    fr = pathlib.Path("build_slideshow/frames"); fr.mkdir(parents=True, exist_ok=True); missing, lines = [], []
    for k, s in enumerate(shots):
        im = render(s, flow_dir)
        if im is None: missing.append(s.get("file") or s["i"]); im = fallback(s["sentence"])
        else: im = overlay(im, s["sentence"], s.get("day"), caption)
        p = fr / f"f{k:04d}.png"; im.save(p, compress_level=1)
        lines.append(f"file '{p.resolve().as_posix()}'\nduration {max(ends[k] - starts[k], 0.4):.3f}\n")
    lst = pathlib.Path("build_slideshow/frames.txt"); lst.write_text("".join(lines) + f"file '{(fr / f'f{len(shots) - 1:04d}.png').resolve().as_posix()}'\n")
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", voice, "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    print(f"done -> {out} | {len(shots)} shots | missing Flow images: {missing}")

if __name__ == "__main__": main()
