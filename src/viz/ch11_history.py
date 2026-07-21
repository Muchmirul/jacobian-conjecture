"""Figures for chapter 11 — the timeline, Pinchuk's heatmap, and the
escape-to-infinity GIF (trapdoor 3)."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LogNorm
import sympy as sp

from common import bare_axes, out_dir
from jacobian_guide.examples import PINCHUK_DET_IDENTITY, VARS
from jacobian_guide.plotting import (BASELINE, BLUE, GOOD, GREEN, INK, INK2,
                                     MUTED, RED, SEQ_CMAP, VIOLET, save_fig,
                                     style_axes)

OUT = out_dir("11-why-it-was-so-hard")

EVENTS = [
    ("1884", "Kraus claims a proof —\nflawed at infinity", MUTED),
    ("1939", "Keller poses\nthe conjecture", BLUE),
    ("1955–61", "wave of published\nproofs… all wrong", MUTED),
    ("1980", "Wang: true for\ndegree ≤ 2", GOOD),
    ("1982", "Bass–Connell–Wright:\ndegree 3 is enough", GOOD),
    ("1983", "Moh: true in the plane\nup to degree 100", GOOD),
    ("1994", "Pinchuk: REAL\nversion is false", RED),
    ("1998", "Smale lists it as\nProblem 16", BLUE),
    ("2004", "Nagata's map proved\nwild (3D is stranger)", VIOLET),
    ("2026", "counterexample: FALSE\nfor n ≥ 3 — plane still open", RED),
]


def timeline_gif(step=8, fps=14, hold=30):
    """87 years appear one event at a time: claimed proofs, partial
    victories, warnings — and the 2026 ending."""
    fig, ax = plt.subplots(figsize=(12.6, 3.9))
    n = len(EVENTS)
    bare_axes(ax, (-0.6, n - 0.4), (-2.4, 2.4))
    ax.axhline(0, color=BASELINE, lw=2, zorder=1)
    groups = []
    for i, (year, label, color) in enumerate(EVENTS):
        up = i % 2 == 0
        y = 0.55 if up else -0.55
        g = [ax.plot([i, i], [0, y], color=color, lw=1.6, zorder=2)[0],
             ax.plot([i], [0], "o", ms=7, color=color, zorder=3)[0],
             ax.text(i, y + (0.18 if up else -0.18), label, ha="center",
                     va="bottom" if up else "top", fontsize=9.3, color=INK),
             ax.text(i, y + (1.28 if up else -1.28), year, ha="center",
                     va="bottom" if up else "top", fontsize=10.5, color=color,
                     weight="bold")]
        for art in g:
            art.set_alpha(0.0)
        groups.append(g)
    ax.set_title("87 years of the Jacobian Conjecture", color=INK2,
                 fontsize=13)

    total = n * step + hold

    def update(i):
        for j, g in enumerate(groups):
            a = min(max((i - j * step) / step, 0.0), 1.0)
            for art in g:
                art.set_alpha(a)
        return [a for g in groups for a in g]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "timeline.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def pinchuk_gif(frames=96, fps=16):
    """A probe sweeps Pinchuk's plane, reading the local area factor and
    remembering the smallest value it has seen: it dips into deep valleys
    but NEVER reaches 0 — yet the map still collides."""
    dfun = sp.lambdify(VARS, PINCHUK_DET_IDENTITY, "numpy")
    xs = np.linspace(-3, 3, 600)
    xx, yy = np.meshgrid(xs, xs)
    zz = np.asarray(dfun(xx, yy), float)
    zmin = zz.min()
    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    im = ax.pcolormesh(xx, yy, zz, cmap=SEQ_CMAP,
                       norm=LogNorm(vmin=max(zmin, 1e-4), vmax=zz.max()),
                       shading="auto")
    style_axes(ax, (-3, 3), (-3, 3), show_axes=False)
    ax.set_title("Pinchuk's map: local area factor at every real point\n"
                 "(log scale — deep valleys, but the floor is never 0)",
                 color=INK2, fontsize=11.5)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.outline.set_visible(False)
    cb.ax.tick_params(color=MUTED, labelcolor=INK2)
    cb.set_label("det J  (always > 0)", color=INK2)
    probe, = ax.plot([], [], "o", ms=10, color=VIOLET, mec="white", mew=1.5,
                     zorder=6)
    read = ax.text(0.5, -0.075, "", transform=ax.transAxes, ha="center",
                   fontsize=11, family="monospace", color=INK2)

    rows = (-1.5, 0.0, 1.5)
    seen = {"min": np.inf}

    def update(i):
        t = i / frames
        k = min(int(t * len(rows)), len(rows) - 1)
        u = t * len(rows) - k
        px = -2.8 + u * 5.6 if k % 2 == 0 else 2.8 - u * 5.6
        py = rows[k]
        v = float(dfun(px, py))
        seen["min"] = min(seen["min"], v)
        probe.set_data([px], [py])
        read.set_text(f"det J here = {v:9.3g}   "
                      f"smallest seen = {seen['min']:.3g}  (never 0)")
        return [probe, read]

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps)
    anim.save(OUT / "pinchuk_det.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def escape_gif(frames=70, fps=18, hold=12):
    """Trapdoor 3 in motion.  Under the crush map (x, y) -> (x, xy), the
    inputs (1/s, s) march off to infinity along the hyperbola xy = 1, while
    their outputs (1/s, 1) calmly approach the ordinary point (0, 1)."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.8, 4.7))
    fig.suptitle("trapdoor 3 — under the crush map $(x, y)\\mapsto(x, xy)$: "
                 "a sequence flees, its shadow stays",
                 color=INK2, fontsize=12, y=0.97)
    s0, s1 = 1.05, 60.0
    YLIM = 8.2

    def ease(t):
        return 3 * t**2 - 2 * t**3

    total = frames + 2 * hold

    def update(i):
        axL.clear()
        axR.clear()
        t = ease(min(max((i - hold) / (frames - 1), 0.0), 1.0))
        s = s0 * (s1 / s0) ** t
        ss = np.geomspace(s0, s, 300)

        # left: the inputs, riding the hyperbola x*y = 1 out of every window
        axL.plot(1 / ss, ss, color=BLUE, lw=1.6, alpha=0.4, zorder=3)
        axL.plot([1 / s], [s], "o", ms=8, color=BLUE, zorder=5)
        style_axes(axL, (-0.08, 1.08), (-0.5, YLIM), equal=False)
        axL.set_title("inputs  $(1/s,\\ s)$ — marching off to infinity",
                      color=INK2, fontsize=11)
        axL.text(0.04, 0.93, f"$s = {s:.1f}$", transform=axL.transAxes,
                 fontsize=11, color=MUTED)
        if s > YLIM:
            axL.text(0.35, 0.93, "…already above every window",
                     transform=axL.transAxes, fontsize=10.5, color=BLUE,
                     style="italic")

        # right: their outputs, calmly walking home along y = 1
        axR.plot(1 / ss, np.ones_like(ss), color=GREEN, lw=1.6, alpha=0.4,
                 zorder=3)
        axR.plot([1 / s], [1.0], "o", ms=8, color=GREEN, zorder=5)
        axR.plot([0], [1], "o", ms=9, mfc="none", mec=RED, mew=1.8, zorder=4)
        axR.annotate("(0, 1)", (0, 1), xytext=(0.05, 1.9), color=RED,
                     fontsize=10.5)
        style_axes(axR, (-0.08, 1.08), (-0.5, YLIM), equal=False)
        axR.set_title("outputs  $(1/s,\\ 1)$ — calmly approaching (0, 1)",
                      color=INK2, fontsize=11)

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "escape.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    timeline_gif()
    pinchuk_gif()
    escape_gif()
    print(f"wrote figures to {OUT}")
