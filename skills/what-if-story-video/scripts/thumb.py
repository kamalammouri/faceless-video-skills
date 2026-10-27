"""Thumbnail by code: a Flow image + 2 or 3 words in Impact + an optional red badge -> 1280x720 JPEG under 2 MB.

  python thumb.py flow/THUMB.jpg "TOO SLOW." [--line2 "500 IQ"] [--badge "PART 2"] [--right] [--out thumb.jpg]

The character fills the right half of the Flow image, so the text goes top-left by default (--right flips it).
Colours measured on the reference channel: first line yellow (242,196,70) or white, second line red (214,72,48), black stroke 10 px,
badge red with white text. Never let the generator write the words: Flow spells them wrong.
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

YELLOW, WHITE, RED, BLACK = (242, 196, 70), (255, 255, 255), (214, 72, 48), (0, 0, 0)
W, H = 1280, 720

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

def main():
    pos = [a for a in sys.argv[1:] if not a.startswith("--") and sys.argv[sys.argv.index(a) - 1] not in ("--line2", "--badge", "--out")]
    src, line1 = pathlib.Path(pos[0]), pos[1]
    line2, badge, out, right = arg("--line2"), arg("--badge"), arg("--out", "thumb.jpg"), "--right" in sys.argv
    im = Image.open(src).convert("RGB"); r = im.width / im.height
    if r > 16 / 9: nw = int(im.height * 16 / 9); im = im.crop(((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height))
    else: nh = int(im.width * 9 / 16); im = im.crop((0, (im.height - nh) // 2, im.width, (im.height - nh) // 2 + nh))
    im = ImageEnhance.Contrast(im.resize((W, H), Image.LANCZOS)).enhance(1.1); d = ImageDraw.Draw(im)
    def big(text, y, size, fill, anchor):
        f = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", size)
        while d.textlength(text, font=f) > 620 and size > 60: size -= 10; f = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", size)
        d.text((W - 40 if right else 40, y), text, font=f, fill=fill, stroke_width=10, stroke_fill=BLACK, anchor=anchor)
    anc = "ra" if right else "la"
    big(line1, 40, 150, YELLOW, anc)
    if line2: big(line2, 210, 150, RED if line2[:1].isdigit() else WHITE, anc)
    if badge:
        f = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 44); tw = d.textlength(badge, font=f)
        x0 = W - 40 - tw - 30 if not right else 40; y0 = H - 110
        d.rounded_rectangle([x0, y0, x0 + tw + 30, y0 + 64], 8, fill=RED); d.text((x0 + 15, y0 + 8), badge, font=f, fill=WHITE)
    q = 92
    while True:
        im.save(out, quality=q)
        if pathlib.Path(out).stat().st_size < 2_000_000 or q < 60: break
        q -= 6
    print(out, pathlib.Path(out).stat().st_size // 1024, "KB")

if __name__ == "__main__": main()
