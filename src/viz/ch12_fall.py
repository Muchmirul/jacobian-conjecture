"""Figures for chapter 12, the 2026 counterexample: collision card + GIF."""

import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import arrow, bare_axes, draw_machine, out_dir
from jacobian_guide.plotting import (BASELINE, BLUE, GREEN, GRIDLINE, INK,
                                     INK2, MUTED, RED, SURFACE, VIOLET,
                                     save_fig)

OUT = out_dir("12-the-fall")

POINTS = ["( 0,  0,  −1/4 )", "( 1,  −3/2,  13/2 )", "( −1,  3/2,  13/2 )"]


def collision_card_gif(fps=14, step=7, travel=26, hold=30):
    """The collision, played out: three starting points appear, three dots
    ride the arrows, and all of them arrive at the SAME landing spot."""
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    bare_axes(ax, (0, 10), (0, 10))
    ax.text(5, 9.35, "one map, constant det J = −2   …and yet:", ha="center",
            fontsize=13, color=INK2)

    def machine(xy, wh, label, color, fontsize):
        box = FancyBboxPatch(xy, *wh,
                             boxstyle="round,pad=0.12,rounding_size=0.18",
                             fc="white", ec=color, lw=2.2, zorder=3)
        ax.add_patch(box)
        txt = ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] / 2, label,
                      ha="center", va="center", fontsize=fontsize, color=INK,
                      zorder=4)
        return [box, txt]

    groups, dots, paths = [], [], []
    for i, p in enumerate(POINTS):
        y = 6.9 - 2.1 * i
        g = machine((0.7, y), (2.9, 1.05), p, BLUE, 11.5)
        g.append(arrow(ax, (3.85, y + 0.5),
                       (6.05, 4.85 + (y + 0.5 - 4.85) * 0.12),
                       color=MUTED, lw=1.8, curve=0.0))
        groups.append(g)
        dots.append(ax.plot([], [], "o", ms=9, color=BLUE, zorder=6)[0])
        paths.append(((3.9, y + 0.5), (6.55, 4.85)))
    finale = machine((6.3, 4.28), (3.0, 1.15), "( −1/4,  0,  0 )", RED, 12.5)
    finale.append(ax.text(7.8, 3.35, "three different starting points,\n"
                          "exactly the same landing spot", ha="center",
                          fontsize=10.5, color=RED))
    finale.append(ax.text(5, 1.15, "a perfect undo machine is impossible: "
                          "standing at (−1/4, 0, 0)\nyou cannot know which "
                          "of the three roads you came by", ha="center",
                          fontsize=11.5, color=INK))
    for g in (*groups, finale):
        for art in g:
            art.set_alpha(0.0)

    def ease(t):
        return 3 * t**2 - 2 * t**3

    t_appear = 3 * step + 6
    total = t_appear + travel + step + hold

    def update(i):
        for j, g in enumerate(groups):
            a = min(max((i - j * step) / step, 0.0), 1.0)
            for art in g:
                art.set_alpha(a)
        t = ease(min(max((i - t_appear) / travel, 0.0), 1.0))
        for dot, ((x0, y0), (x1, y1)) in zip(dots, paths):
            dot.set_data([(1 - t) * x0 + t * x1], [(1 - t) * y0 + t * y1])
            dot.set_color(RED if t >= 1.0 else BLUE)
        a = min(max((i - t_appear - travel) / step, 0.0), 1.0)
        for art in finale:
            art.set_alpha(a)
        return [*dots, *finale, *[a for g in groups for a in g]]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "collision_card.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def collision_gif(frames=56, fps=18, hold=16):
    """The fall, animated in 3D: each of the three inputs travels straight
    to its output under the counterexample map, and all three outputs are
    the SAME point (−1/4, 0, 0).  The camera drifts to make the depth read."""
    starts = np.array([[0.0, 0.0, -0.25], [1.0, -1.5, 6.5], [-1.0, 1.5, 6.5]])
    target = np.array([-0.25, 0.0, 0.0])
    cols = (BLUE, GREEN, VIOLET)
    labels = ("(0, 0, −1/4)", "(1, −3/2, 13/2)", "(−1, 3/2, 13/2)")

    fig = plt.figure(figsize=(7.4, 6.4))
    ax = fig.add_subplot(projection="3d")

    def ease(t):
        return 3 * t**2 - 2 * t**3

    total = frames + 2 * hold

    def update(i):
        ax.clear()
        t = ease(min(max((i - hold) / (frames - 1), 0.0), 1.0))
        # faint ground grid at z = 0, where the landing spot lives
        for g in np.linspace(-1.4, 1.4, 8):
            ax.plot([g, g], [-1.9, 1.9], [0, 0], color=GRIDLINE, lw=0.7,
                    zorder=1)
        for g in np.linspace(-1.9, 1.9, 8):
            ax.plot([-1.4, 1.4], [g, g], [0, 0], color=GRIDLINE, lw=0.7,
                    zorder=1)
        for p, c, lab in zip(starts, cols, labels):
            pos = (1 - t) * p + t * target
            road = np.column_stack([p, target])
            done = np.column_stack([p, pos])
            ax.plot(road[0], road[1], road[2], color=c, lw=1.1, ls=":",
                    alpha=0.35)
            ax.plot(done[0], done[1], done[2], color=c, lw=2.0, alpha=0.6)
            ax.scatter(*pos, color=c, s=48, depthshade=False)
            ax.text(p[0], p[1], p[2] + 0.55, lab, color=c, fontsize=9.5,
                    ha="center")
        ax.scatter(*target, marker="x", s=80, color=RED, lw=2.2,
                   depthshade=False)
        ax.text(target[0], target[1], target[2] - 1.6, "(−1/4, 0, 0)",
                color=RED, fontsize=10.5, ha="center")
        titles = ("the 2026 counterexample: local volume factor −2 at EVERY "
                  "point of 3D space…",
                  "…yet three different points land on ONE spot: "
                  "no undo machine can exist")
        ax.set_title(titles[0] + "\n" + (titles[1] if t > 0.55 else ""),
                     color=INK2, fontsize=11)
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.9, 1.9)
        ax.set_zlim(-1.8, 7.4)
        ax.set_box_aspect((1, 1, 1.45))
        ax.view_init(elev=16, azim=-58 + 24 * t)
        ax.set_xticks([]), ax.set_yticks([]), ax.set_zticks([])
        ax.grid(False)
        ax.set_facecolor(SURFACE)
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.set_pane_color((1, 1, 1, 0))
            axis.line.set_color(BASELINE)

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "collision.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    collision_card_gif()
    collision_gif()
    print(f"wrote figures to {OUT}")
