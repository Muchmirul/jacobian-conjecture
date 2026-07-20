"""Shared drawing helpers for the 1D chapters (machines and number lines)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from jacobian_guide.plotting import (BASELINE, BLUE, GREEN, INK, INK2, MUTED,
                                     RED, SURFACE, VIOLET, YELLOW, save_fig)

GUIDE = Path(__file__).resolve().parents[2] / "guide"


def out_dir(chapter_folder: str) -> Path:
    d = GUIDE / chapter_folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def bare_axes(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def draw_machine(ax, xy, wh, label, color=BLUE, fontsize=13):
    """A rounded 'machine' box with a label."""
    box = FancyBboxPatch(xy, *wh, boxstyle="round,pad=0.12,rounding_size=0.18",
                         fc="white", ec=color, lw=2.2, zorder=3)
    ax.add_patch(box)
    ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] / 2, label, ha="center",
            va="center", fontsize=fontsize, color=INK, zorder=4)


def arrow(ax, p, q, color=INK2, lw=2, style="-|>", shrink=0.0, curve=0.0):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16, color=color,
                        lw=lw, shrinkA=shrink, shrinkB=shrink,
                        connectionstyle=f"arc3,rad={curve}", zorder=5)
    ax.add_patch(a)
    return a


def number_line(ax, y, xlim, ticks, color=BASELINE, label=None,
                tick_color=MUTED):
    ax.plot(xlim, [y, y], color=color, lw=1.6, zorder=2)
    for t in ticks:
        ax.plot([t, t], [y - 0.06, y + 0.06], color=color, lw=1.4, zorder=2)
        ax.text(t, y - 0.16, f"{t:g}", ha="center", va="top", fontsize=10,
                color=tick_color)
    if label:
        ax.text(xlim[0] - 0.35, y, label, ha="right", va="center",
                fontsize=11, color=INK2)


def animate_1d(f, xs, out_path, xlim=(-6.5, 10.5), fps=20, frames=36,
               hold=10, title=None, top_label="inputs",
               bottom_label="outputs", roundtrip=False, figsize=(7.2, 3.4)):
    """Dots fall from the input number line to their outputs on the one below.

    With roundtrip=True the dots then travel back up to where they started
    (the 'undo' animation of chapter 2).
    """
    y_top, y_bot = 1.0, 0.0
    fig, ax = plt.subplots(figsize=figsize)
    bare_axes(ax, (xlim[0] - 1.2, xlim[1] + 0.6), (-0.55, 1.55))
    ticks = [t for t in range(int(np.ceil(xlim[0])), int(xlim[1]) + 1)
             if t % 2 == 0]
    number_line(ax, y_top, xlim, ticks, label=top_label)
    number_line(ax, y_bot, xlim, ticks, label=bottom_label)
    if title:
        ax.set_title(title, color=INK2, fontsize=12)

    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    c1 = np.array(matplotlib.colors.to_rgb(GREEN))
    ys_end = [f(x) for x in xs]
    dots = [ax.plot([x], [y_top], "o", ms=9, color=BLUE, zorder=6)[0]
            for x in xs]
    trails = [ax.plot([], [], lw=1.2, color=BLUE, alpha=0.35, zorder=4)[0]
              for _ in xs]

    def ease(t):
        return 3 * t**2 - 2 * t**3

    stages = 2 if roundtrip else 1
    total = stages * (frames + hold) + hold

    def update(i):
        i = max(0, i - hold)
        stage, j = divmod(i, frames + hold)
        t = ease(min(j / frames, 1.0))
        if stage >= stages:
            stage, t = stages - 1, 1.0
        going_down = (stage == 0)
        u = t if going_down else 1 - t
        c = matplotlib.colors.to_hex((1 - u) * c0 + u * c1)
        for dot, trail, x0, x1 in zip(dots, trails, xs, ys_end):
            x = (1 - u) * x0 + u * x1
            y = (1 - u) * y_top + u * y_bot
            dot.set_data([x], [y])
            dot.set_color(c)
            trail.set_data([x0, x], [y_top, y])
            trail.set_color(c)
        return dots

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(out_path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    return out_path
