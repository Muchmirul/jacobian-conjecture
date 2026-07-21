# Optional manim scenes

Fancier animated versions of the guide's flagship visuals, for
[Manim Community Edition](https://docs.manim.community/). **Nothing in the
guide depends on these**, every committed image and GIF under `guide/` is
rendered by the plain-matplotlib scripts in `src/viz/`.

## Install (Manim CE ≥ 0.19, Python ≥ 3.11)

```bash
pip install manim
```

Notes (as of mid-2026):

- No separate ffmpeg install needed since manim 0.19 (bundled via pyav wheels).
- No LaTeX needed: these scenes use `Text` (Pango), not `Tex`/`MathTex`.
- On **Linux**, ManimPango ships no prebuilt wheels, so pip builds it from
  source, install the headers first:
  `sudo apt install libpango1.0-dev libcairo2-dev pkg-config python3-dev`.
  (Windows/macOS have prebuilt wheels; nothing extra needed.)

## Render

```bash
cd manim
manim -qm --format=gif scenes.py TangledWarp      # 720p GIF
manim -qh scenes.py ShearBend                     # 1080p MP4
manim -qm scenes.py FoldCollision
manim -qm scenes.py SquashDeterminant
```

Output lands in `manim/media/` (git-ignored).
