"""Music bed, real sound effects and mastering for the finished slideshow (Openverse: Freesound, Jamendo, Wikimedia; CC0 and CC BY only).

  python audio_mix.py search "dark ambient drone" [--n 8]                      list candidates (id, license, duration, title)
  python audio_mix.py get <openverse_id> [--dir audio]                          download to audio/<id>.mp3, attribution to audio/credits.json
  python audio_mix.py mix out.mp4 voice.wav --music audio/<id>.mp3 [--music-db -24]
                         [--sfx audio/<id>.mp3@START[+DUR][:DB]]... [--out out_mix.mp4]

No API key: Openverse allows anonymous searches (rate-limited). Only licenses usable on a monetized channel are requested (CC0, CC BY);
CC BY needs the credit line, so `get` prints it and keeps it in audio/credits.json for the description.

mix: voice cleaned (high-pass 70 Hz, -2 dB of mud at 250 Hz, +2.5 dB presence at 3.5 kHz, gentle 3:1 compression), music looped,
faded in and out and ducked under the voice (sidechain), each SFX placed at its start time, then the whole track mastered to
-14 LUFS / -1.5 dBTP (YouTube's playback level) in 48 kHz stereo; the video stream is copied, not re-encoded.
"""
import json, sys, pathlib, subprocess, urllib.request, urllib.parse
import imageio_ffmpeg

API = "https://api.openverse.org/v1/audio/"
FF = imageio_ffmpeg.get_ffmpeg_exe()

def arg(args, name, default=None):
    return args[args.index(name) + 1] if name in args else default

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": "faceless-video-skills/audio_mix"})
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)

def search(q, n):   # no category filter: Freesound, the main source, leaves it empty
    p = {"q": q, "license": "cc0,by", "page_size": n, "mature": "false"}
    for r in api(API + "?" + urllib.parse.urlencode(p))["results"]:
        print(f"{r['id']}  {r['license']:>3}  {(r['duration'] or 0) / 1000:6.0f}s  {r['title'][:60]}")

def get(oid, d):
    r = api(API + oid + "/"); d = pathlib.Path(d); d.mkdir(exist_ok=True)
    if r["license"] not in ("cc0", "by"): sys.exit(f"license {r['license']} refused: CC0 or CC BY only")
    dst = d / f"{oid}.mp3"
    req = urllib.request.Request(r["url"], headers={"User-Agent": "faceless-video-skills/audio_mix"})
    with urllib.request.urlopen(req, timeout=60) as f: dst.write_bytes(f.read())
    cred = d / "credits.json"; c = json.loads(cred.read_text(encoding="utf-8")) if cred.exists() else {}
    c[oid] = {"title": r["title"], "license": r["license"], "page": r["foreign_landing_url"], "attribution": r["attribution"]}
    cred.write_text(json.dumps(c, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{dst}\n{r['attribution'] if r['license'] == 'by' else 'CC0: no credit required'}")

def duration(path):
    s = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0]
    h, m, sec = s.split(":"); return 3600 * int(h) + 60 * int(m) + float(sec)

def mix(video, voice, args):
    music, mdb, out = arg(args, "--music"), float(arg(args, "--music-db", -24)), arg(args, "--out", "out_mix.mp4")
    sfx = [args[i + 1] for i, a in enumerate(args) if a == "--sfx"]
    T = duration(voice)
    ins, fc, bus = ["-i", video, "-i", voice], [], ["[v]"]
    fc.append("[1:a]aresample=48000,highpass=f=70,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1:g=2.5,"
              "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,asplit=2[v][key]")
    k = 2
    if music:
        ins += ["-stream_loop", "-1", "-i", music]
        fc.append(f"[{k}:a]aresample=48000,atrim=0:{T:.2f},volume={mdb}dB,afade=in:d=3,afade=out:st={T - 4:.2f}:d=4[m];"
                  f"[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[mb]")
        bus.append("[mb]"); k += 1
    else: fc.append("[key]anullsink")
    for j, s in enumerate(sfx):          # path@START[+DUR][:DB]
        path, rest = s.rsplit("@", 1); db = -18.0
        if ":" in rest: rest, db = rest.split(":"); db = float(db)
        start, dur = (rest.split("+") + [None])[:2]; start = float(start)
        trim = f"atrim=0:{float(dur):.2f},afade=out:st={max(float(dur) - 1.5, 0):.2f}:d=1.5," if dur else ""
        ins += ["-i", path]
        fc.append(f"[{k}:a]aresample=48000,{trim}afade=in:d=0.5,volume={db}dB,adelay={int(start * 1000)}:all=1[s{j}]")
        bus.append(f"[s{j}]"); k += 1
    fc.append(f"{''.join(bus)}amix=inputs={len(bus)}:duration=first:normalize=0,"
              "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]")   # ponytail: one-pass loudnorm, two-pass if levels drift
    subprocess.run([FF, "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T:.2f}", out], check=True)
    print(f"done -> {out} | music {music or 'none'} at {mdb} dB | {len(sfx)} sfx | -14 LUFS 48 kHz stereo")

def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "search": search(a[1], int(arg(a, "--n", 8)))
    elif a[0] == "get": get(a[1], arg(a, "--dir", "audio"))
    elif a[0] == "mix": mix(a[1], a[2], a[3:])
    else: sys.exit(__doc__)

if __name__ == "__main__": main()
