"""Stitch every figure in guide/ into MP4 videos.

For each chapter, media are taken in the order they appear in the chapter's
README: PNGs become slow Ken-Burns segments, GIFs are played twice, and a
title card opens the chapter.  Output: video/chNN.mp4 per chapter plus the
full stitched video/jacobian-guide.mp4.

Requires ffmpeg (system) and the project venv (PIL + matplotlib for fonts).
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / "guide"
OUT = ROOT / "video"

W, H, FPS = 1280, 720, 30
STILL_SEC = 4.5          # duration of a PNG segment
CARD_SEC = 2.2           # duration of a chapter title card
GIF_PLAYS = 2            # each GIF is played this many times
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#898781"

FFMPEG = "ffmpeg"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
       "-pix_fmt", "yuv420p", "-r", str(FPS)]
FIT = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
       f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0xfcfcfb")


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")


def readme_media(chapter: Path) -> list[Path]:
    """Media files of a chapter, in the order the README shows them."""
    text = (chapter / "README.md").read_text()
    files = []
    for m in re.finditer(r'<img src="([^"]+\.(?:png|gif))"', text):
        p = chapter / m.group(1)
        if p.exists():
            files.append(p)
    return files


def chapter_title(chapter: Path) -> str:
    first = (chapter / "README.md").read_text().splitlines()[0]
    return first.lstrip("# ").strip()


def font(size: int) -> ImageFont.FreeTypeFont:
    path = font_manager.findfont("DejaVu Sans")
    return ImageFont.truetype(path, size)


def make_title_card(title: str, path: Path) -> None:
    img = Image.new("RGB", (W, H), SURFACE)
    d = ImageDraw.Draw(img)
    f_big, f_small = font(54), font(26)
    w = d.textlength(title, font=f_big)
    d.text(((W - w) / 2, H / 2 - 60), title, fill=INK, font=f_big)
    sub = "the Jacobian Conjecture, illustrated"
    w = d.textlength(sub, font=f_small)
    d.text(((W - w) / 2, H / 2 + 24), sub, fill=MUTED, font=f_small)
    img.save(path)


def still_segment(png: Path, out: Path, seconds: float, zoom: float) -> None:
    """A PNG as video: fitted to the canvas with a slow center zoom."""
    n = round(seconds * FPS)
    up = (f"scale={2 * W}:{2 * H}:force_original_aspect_ratio=decrease,"
          f"pad={2 * W}:{2 * H}:(ow-iw)/2:(oh-ih)/2:color=0xfcfcfb")
    zp = (f"zoompan=z='1+{zoom}*on/{n}':d={n}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"s={W}x{H}:fps={FPS}")
    run([FFMPEG, "-y", "-i", str(png), "-vf", f"{up},{zp}",
         "-frames:v", str(n), *ENC, str(out)])


def gif_segment(gif: Path, out: Path) -> None:
    run([FFMPEG, "-y", "-stream_loop", str(GIF_PLAYS - 1), "-i", str(gif),
         "-vf", f"fps={FPS},{FIT}", *ENC, str(out)])


def concat(parts: list[Path], out: Path) -> None:
    lst = out.with_suffix(".txt")
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(out)])
    lst.unlink()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    chapters = sorted(d for d in GUIDE.iterdir()
                      if d.is_dir() and (d / "README.md").exists())
    chapter_files = []
    with tempfile.TemporaryDirectory(prefix="guide-video-") as tmp:
        build = Path(tmp)
        for chapter in chapters:
            media = readme_media(chapter)
            if not media:
                continue
            num = chapter.name.split("-")[0]
            parts = []
            card = build / f"{num}-card.png"
            make_title_card(chapter_title(chapter), card)
            seg = build / f"{num}-card.mp4"
            still_segment(card, seg, CARD_SEC, zoom=0.0)
            parts.append(seg)
            for k, m in enumerate(media):
                seg = build / f"{num}-{k}{m.suffix}.mp4"
                if m.suffix == ".png":
                    still_segment(m, seg, STILL_SEC, zoom=0.045)
                else:
                    gif_segment(m, seg)
                parts.append(seg)
            out = OUT / f"ch{num}.mp4"
            concat(parts, out)
            chapter_files.append(out)
            print(f"wrote {out.relative_to(ROOT)}  "
                  f"({len(media)} figures)")
        concat(chapter_files, OUT / "jacobian-guide.mp4")
    print(f"wrote {(OUT / 'jacobian-guide.mp4').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
