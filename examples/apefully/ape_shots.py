"""Cut every Apefully video into shots and make labelled contact sheets.
  python ape_shots.py            -> ape_shots/<id>/shots.json, frames/<n>.jpg (one mid-shot frame, 640x360), sheets/<k>.jpg (48 per sheet)
Method: 4 fps grayscale 160x90 diff for cut detection (same as the earlier study), 1 fps 640x360 frames for the pictures.
"""
import json, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
SRC, OUT = pathlib.Path("ape_dl"), pathlib.Path("ape_shots")
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)

def cuts(mp4):
    raw = subprocess.run([FF, "-v", "error", "-i", str(mp4), "-vf", "fps=4,scale=160:90,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    g = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.int16)
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))          # mean abs diff between consecutive frames
    thr = max(12.0, float(np.percentile(d, 97)) * 0.6)          # ponytail: fixed-ish threshold, tuned on the 2 studied videos
    idx = np.where(d > thr)[0] + 1
    t = [0.0]
    for i in idx:
        if i / 4 - t[-1] >= 1.0: t.append(i / 4)               # min shot length 1 s
    t.append(len(g) / 4)
    return [(t[i], t[i + 1]) for i in range(len(t) - 1)]

def frames_1fps(mp4, d):
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run([FF, "-v", "error", "-i", str(mp4), "-vf", "fps=1,scale=640:360", "-q:v", "4", str(d / "%05d.jpg")], check=True)

def process(mp4):
    vid = mp4.stem; o = OUT / vid
    if (o / "shots.json").exists(): return
    tmp = o / "all1fps"; frames_1fps(mp4, tmp)
    shots = cuts(mp4); (o / "frames").mkdir(exist_ok=True)
    rows = []
    for n, (a, b) in enumerate(shots):
        mid = int((a + b) / 2) + 1; src = tmp / f"{mid:05d}.jpg"
        if not src.exists(): continue
        dst = o / "frames" / f"{n:03d}.jpg"; src.replace(dst)
        rows.append({"n": n, "start": round(a, 2), "end": round(b, 2), "dur": round(b - a, 2), "frame": dst.name})
    for f in tmp.glob("*.jpg"): f.unlink()
    tmp.rmdir()
    (o / "sheets").mkdir(exist_ok=True); W, H = 320, 180
    for k in range(0, len(rows), 48):
        chunk = rows[k:k + 48]; sheet = Image.new("RGB", (W * 6, H * 8), "white"); d = ImageDraw.Draw(sheet)
        for i, r in enumerate(chunk):
            im = Image.open(o / "frames" / r["frame"]).resize((W, H)); x, y = (i % 6) * W, (i // 6) * H
            sheet.paste(im, (x, y)); d.rectangle([x, y, x + 150, y + 22], fill="black"); d.text((x + 4, y + 2), f"{r['n']:03d} {int(r['start'] // 60)}:{int(r['start'] % 60):02d}", font=FONT, fill="yellow")
        sheet.save(o / "sheets" / f"{k // 48 + 1:02d}.jpg", quality=80)
    json.dump({"video": vid, "shots": rows}, open(o / "shots.json", "w"), indent=0)
    print(vid, len(rows), "shots", round(sum(r["dur"] for r in rows) / max(len(rows), 1), 2), "s avg", len(list((o / "sheets").glob("*.jpg"))), "sheets", flush=True)

if __name__ == "__main__":
    files = [SRC / a for a in sys.argv[1:]] or sorted(SRC.glob("*.mp4"))
    for f in files: process(f)
