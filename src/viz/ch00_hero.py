"""Figures for chapter 0, the hook and the roadmap (all animated)."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from common import bare_axes, out_dir
from jacobian_guide.examples import TANGLED, VARS
from jacobian_guide.plotting import (BLUE, GREEN, INK, INK2, MUTED, VIOLET,
                                     animate_map)

OUT = out_dir("00-start-here")

CHAPTERS = ["0 start", "1 machines", "2 undo", "3 polynomials", "4 plane maps",
            "5 area", "6 bending", "7 microscope", "8 local ≠ global",
            "9 the conjecture", "10 test drive", "11 why so hard", "12 the fall"]


def hero_gif():
    animate_map(TANGLED, VARS, OUT / "hero.gif", xlim=(-1, 1), ylim=(-1, 1),
                spacing=0.2, view=((-1.7, 5.3), (-1.7, 2.4)), frames=54,
                hold_frames=12, figsize=(7.6, 4.6),
                title="this scramble can be perfectly undone, and that is the easy part")


def roadmap_gif(step_frames=4, fps=14, hold=22):
    """The journey appears one small step at a time, in reading order."""
    fig, ax = plt.subplots(figsize=(10.4, 3.8))
    bare_axes(ax, (-0.4, 5 * 2.1), (-0.4, 3 * 1.25))
    cols, w, h, dx, dy = 5, 1.55, 0.62, 2.1, 1.25
    pos = {}
    groups = []          # per chapter: the artists that fade in together
    for i, label in enumerate(CHAPTERS):
        r, c = divmod(i, cols)
        c = c if r % 2 == 0 else cols - 1 - c          # snake layout
        x, y = c * dx, (2 - r) * dy
        pos[i] = (x, y)
        color = VIOLET if i == 12 else (GREEN if i == 9 else BLUE)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0.12,rounding_size=0.18",
                             fc="white", ec=color, lw=2.2, zorder=3, alpha=0.0)
        ax.add_patch(box)
        txt = ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                      fontsize=10.5, color=INK, zorder=4, alpha=0.0)
        group = [box, txt]
        if i > 0:
            (x0, y0), (x1, y1) = pos[i - 1], pos[i]
            if abs(y1 - y0) < 1e-9:
                s = 1 if x1 > x0 else -1
                a, b = (((x0 + w, y0 + h / 2), (x1, y1 + h / 2)) if s > 0
                        else ((x0, y0 + h / 2), (x1 + w, y1 + h / 2)))
            else:
                a, b = (x0 + w / 2, y0), (x1 + w / 2, y1 + h)
            ar = FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16,
                                 color=MUTED, lw=1.4, shrinkA=4, shrinkB=4,
                                 zorder=5, alpha=0.0)
            ax.add_patch(ar)
            group.append(ar)
        groups.append(group)
    ax.set_title("the journey: 13 small ideas, one per chapter, "
                 "from 'what is a function' to the fall of the conjecture",
                 color=INK2, fontsize=11.5)

    total = len(CHAPTERS) * step_frames + hold

    def update(i):
        for j, group in enumerate(groups):
            a = min(max((i - j * step_frames) / step_frames, 0.0), 1.0)
            for art in group:
                art.set_alpha(a)
        return [a for g in groups for a in g]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "roadmap.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    hero_gif()
    roadmap_gif()
    print(f"wrote figures to {OUT}")
