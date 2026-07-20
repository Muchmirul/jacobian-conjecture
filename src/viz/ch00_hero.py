"""Figures for chapter 0 — the hook and the roadmap."""

import matplotlib.pyplot as plt

from common import bare_axes, draw_machine, arrow, out_dir
from jacobian_guide.examples import TANGLED, VARS
from jacobian_guide.plotting import BLUE, GREEN, INK2, MUTED, VIOLET, animate_map, save_fig

OUT = out_dir("00-start-here")

CHAPTERS = ["0 start", "1 machines", "2 undo", "3 polynomials", "4 plane maps",
            "5 area", "6 bending", "7 microscope", "8 local ≠ global",
            "9 the conjecture", "10 test drive", "11 why so hard", "12 the fall"]


def hero_gif():
    animate_map(TANGLED, VARS, OUT / "hero.gif", xlim=(-1, 1), ylim=(-1, 1),
                spacing=0.2, view=((-1.7, 5.3), (-1.7, 2.4)), frames=54,
                hold_frames=12, figsize=(7.6, 4.6),
                title="this scramble can be perfectly undone — that's the easy part of the story")


def roadmap():
    fig, ax = plt.subplots(figsize=(10.4, 3.6))
    bare_axes(ax, (-0.4, 5 * 2.1), (-0.4, 3 * 1.25))
    cols, w, h, dx, dy = 5, 1.55, 0.62, 2.1, 1.25
    pos = {}
    for i, label in enumerate(CHAPTERS):
        r, c = divmod(i, cols)
        c = c if r % 2 == 0 else cols - 1 - c          # snake layout
        x, y = c * dx, (2 - r) * dy
        pos[i] = (x, y)
        color = VIOLET if i == 12 else (GREEN if i == 9 else BLUE)
        draw_machine(ax, (x, y), (w, h), label, color=color, fontsize=10.5)
    for i in range(len(CHAPTERS) - 1):
        (x0, y0), (x1, y1) = pos[i], pos[i + 1]
        if abs(y1 - y0) < 1e-9:
            s = 1 if x1 > x0 else -1
            a = ((x0 + w, y0 + h / 2), (x1, y1 + h / 2)) if s > 0 else \
                ((x0, y0 + h / 2), (x1 + w, y1 + h / 2))
            arrow(ax, *a, color=MUTED, lw=1.4, shrink=4)
        else:
            arrow(ax, (x0 + w / 2, y0), (x1 + w / 2, y1 + h),
                  color=MUTED, lw=1.4, shrink=4)
    ax.set_title("the journey — each step is one small idea", color=INK2,
                 fontsize=12)
    save_fig(fig, OUT / "roadmap.png")


if __name__ == "__main__":
    hero_gif()
    roadmap()
    print(f"wrote figures to {OUT}")
