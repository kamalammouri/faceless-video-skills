"""Voice track of the slideshow: one audio clip per shot, concatenated, with exact start times.

  python tts.py shots.json [--engine gemini|edge] [--voice NAME] [--style "..."] [--rate +0%] [--model ID] [--gap 0.35]
                           [--brief brief.json] [--out voice.wav] [--timing timing.json] [--cache tts] [--pace 2000] [--only 1,2,3]

Engine, voice, style, rate and language come from brief.json ("voice": {"engine", "name", "style", "rate", "model"}, "voice_language"),
each overridable by a flag. The engine is chosen by the user at the pre-production brief (references/brief.md); nothing is assumed.

Each shot's "sentence" is synthesised to <cache>/<engine>/S<i>.wav, next to a .txt with the text that produced it: a clip whose text
has not changed is skipped (the run is resumable; delete a clip or change its sentence to redo it). The clips are then concatenated
with --gap seconds of silence into voice.wav, and timing.json receives the list of start times, one per shot, in shot order (the
second format build_slideshow.py accepts). A shot without a sentence takes the start time of the next clip.

gemini : pip install "google-genai>=2.25" ; GEMINI_API_KEY in the environment or in a local .env (never in the repo) ; 24 kHz WAV ;
         model gemini-3.8-flash-tts by default (gemini-2.5-*-preview-tts models go through generate_content) ; the style sentence
         is sent with every call so the clips match ; --pace ms between calls keeps under the quota ; 429 and 5xx are retried.
edge   : pip install edge-tts ; free, no key ; mp3 converted to 24 kHz mono WAV with the ffmpeg of imageio_ffmpeg (already needed
         by build_slideshow.py) ; --rate like "-5%" ; no style control, the voice name carries the tone.
Several voices: brief.json "voices": {"NARRATOR": "en-US-GuyNeural", "MOM": "en-US-JennyNeural", ...} and, on a shot, "speaker": "MOM".
         A shot without "speaker" uses the main voice; a speaker missing from the table falls back to it too (and is listed at the end).
         Gemini: the table gives the voice name; the style sentence stays the brief's one, so put the tone in the sentence itself.
Always test on three shots first: --only 1,2,3 , listen, then run the full list.
"""
import json, sys, os, time, wave, pathlib, subprocess, base64, io, shutil

SR = 24000
DEFAULT_MODEL = "gemini-3.8-flash-tts"
DEFAULT_VOICE = {"gemini": {"en": "Kore", "fr": "Kore"}, "edge": {"en": "en-US-GuyNeural", "fr": "fr-FR-HenriNeural"}}
DEFAULT_STYLE = "calm, slow, low-pitched documentary narration, no enthusiasm"

def arg_value(args, flag, default=None):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default

def load_env():
    """Read KEY=VALUE lines of a .env in the working directory or its parents (3 levels) into os.environ, without overriding."""
    here = pathlib.Path.cwd()
    for d in [here, *here.parents[:3]]:
        f = d / ".env"
        if f.exists():
            for line in f.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return

def ffmpeg():
    try:
        import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return shutil.which("ffmpeg") or sys.exit("ffmpeg not found: pip install imageio-ffmpeg")

def to_wav24(src, dst):
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(dst)], check=True)

def pcm_to_wav_bytes(pcm, sr=SR):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm)
    return buf.getvalue()

def read_frames(path):
    """Return the 16-bit mono 24 kHz frames of a WAV, converting through ffmpeg when the format differs."""
    with wave.open(str(path), "rb") as w:
        if w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR: return w.readframes(w.getnframes())
    tmp = path.with_suffix(".24k.wav"); to_wav24(path, tmp)
    with wave.open(str(tmp), "rb") as w: frames = w.readframes(w.getnframes())
    tmp.unlink(); return frames

# ---------- engines ----------
def tts_gemini(text, voice, style, model, dst):
    from google import genai
    client = genai.Client()  # reads GEMINI_API_KEY
    if "2.5" in model:  # preview models: generate_content with AUDIO modality, raw PCM back
        from google.genai import types
        r = client.models.generate_content(model=model, contents=(f"Say in a {style} voice: " if style else "") + text,
            config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)))))
        pcm = r.candidates[0].content.parts[0].inline_data.data
        dst.write_bytes(pcm_to_wav_bytes(pcm if isinstance(pcm, bytes) else base64.b64decode(pcm))); return
    content = {"type": "text", "text": text}
    if style: content["annotations"] = [{"type": "speech_metadata", "style": style}]
    it = client.interactions.create(model=model, input=[{"type": "user_input", "content": [content]}],
                                    response_format={"type": "audio"}, generation_config={"speech_config": [{"voice": voice}]})
    data = it.output_audio.data
    dst.write_bytes(base64.b64decode(data) if isinstance(data, str) else data)

def tts_edge(text, voice, rate, dst):
    import asyncio, edge_tts
    mp3 = dst.with_suffix(".mp3")
    asyncio.run(edge_tts.Communicate(text, voice, rate=rate).save(str(mp3)))
    to_wav24(mp3, dst); mp3.unlink()

def synth(engine, text, cfg, dst, attempts=4):
    for n in range(attempts):
        try:
            if engine == "gemini": tts_gemini(text, cfg["voice"], cfg["style"], cfg["model"], dst)
            else: tts_edge(text, cfg["voice"], cfg["rate"], dst)
            return True
        except Exception as e:  # quota (429), transient 5xx, network: wait and retry
            wait = 10 * (3 ** n)
            print(f"  retry in {wait}s after: {str(e)[:160]}")
            if dst.exists(): dst.unlink()
            time.sleep(wait)
    return False

# ---------- main ----------
def main(args):
    load_env()
    src = next((a for a in args if a.endswith(".json") and (args.index(a) == 0 or not args[args.index(a) - 1].startswith("--"))), "shots.json")
    shots = json.load(open(src, encoding="utf-8"))
    bp = pathlib.Path(arg_value(args, "--brief", "brief.json")); brief = json.load(open(bp, encoding="utf-8")) if bp.exists() else {}
    bv = brief.get("voice") or {}
    engine = arg_value(args, "--engine", bv.get("engine") or "edge")
    if engine not in DEFAULT_VOICE: sys.exit(f"unknown engine '{engine}': gemini | edge")
    lang = (brief.get("voice_language") or "en")[:2].lower()
    cfg = {"voice": arg_value(args, "--voice", bv.get("name") or DEFAULT_VOICE[engine].get(lang, DEFAULT_VOICE[engine]["en"])),
           "style": arg_value(args, "--style", bv.get("style") if bv.get("style") is not None else DEFAULT_STYLE),
           "rate": arg_value(args, "--rate", bv.get("rate") or "+0%"),
           "model": arg_value(args, "--model", bv.get("model") or DEFAULT_MODEL)}
    gap, pace = float(arg_value(args, "--gap", 0.35)), int(arg_value(args, "--pace", 2000 if engine == "gemini" else 300))
    only = {int(x) for x in arg_value(args, "--only", "").split(",") if x.strip()}
    cache = pathlib.Path(arg_value(args, "--cache", "tts")) / engine; cache.mkdir(parents=True, exist_ok=True)
    if engine == "gemini" and not os.environ.get("GEMINI_API_KEY"): sys.exit("GEMINI_API_KEY missing: put it in the environment or in a local .env")
    print(f"engine {engine} | voice {cfg['voice']} | {'model ' + cfg['model'] + ' | style ' + repr(cfg['style']) if engine == 'gemini' else 'rate ' + cfg['rate']} | lang {lang}")

    voices = brief.get("voices") or {}; unknown = set()
    made = skipped = failed = 0
    for s in shots:
        text = (s.get("sentence") or "").strip()
        if not text or (only and s["i"] not in only): continue
        spk = s.get("speaker"); vcfg = dict(cfg)
        if spk and spk in voices: vcfg["voice"] = voices[spk]
        elif spk: unknown.add(spk)
        name = f"S{s['i']:04d}"; dst, txt = cache / f"{name}.wav", cache / f"{name}.txt"   # by shot, not by image: one image may carry several sentences
        key = f"{vcfg['voice']}|{text}"
        if dst.exists() and txt.exists() and txt.read_text(encoding="utf-8") == key: skipped += 1; continue
        print(f"#{s['i']:>3} {name} [{spk or 'narrator'} / {vcfg['voice']}]: {text[:60]}")
        if synth(engine, text, vcfg, dst): txt.write_text(key, encoding="utf-8"); made += 1; time.sleep(pace / 1000)
        else: failed += 1
    print(f"clips: {made} made, {skipped} unchanged, {failed} failed" + (f" | speakers without a voice in brief.voices (main voice used): {sorted(unknown)}" if unknown else ""))

    # concatenate in shot order, exact start times
    silence = b"\x00\x00" * int(gap * SR); frames, starts, missing, t = [], [], [], 0.0
    for s in shots:
        starts.append(round(t, 3))
        name = f"S{s['i']:04d}"; clip = cache / f"{name}.wav"
        if not (s.get("sentence") or "").strip(): continue
        if not clip.exists(): missing.append(s["i"]); continue
        fr = read_frames(clip); frames.append(fr); frames.append(silence); t += (len(fr) // 2 + len(silence) // 2) / SR
    out, timing = pathlib.Path(arg_value(args, "--out", "voice.wav")), pathlib.Path(arg_value(args, "--timing", "timing.json"))
    with wave.open(str(out), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(b"".join(frames))
    json.dump(starts, open(timing, "w", encoding="utf-8"))
    print(f"{out} {t / 60:.1f} min | {timing} {len(starts)} starts | missing clips: {missing or 'none'}"
          + (" (run again without --only for the full track)" if only else ""))

if __name__ == "__main__":
    main(sys.argv[1:])
