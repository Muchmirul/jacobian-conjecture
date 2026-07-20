"""Figures for chapter 11 — the timeline of attempts + Pinchuk's heatmap."""

import numpy as np
import matplotlib.pyplot as plt
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


def timeline():
    fig, ax = plt.subplots(figsize=(12.6, 3.9))
    n = len(EVENTS)
    bare_axes(ax, (-0.6, n - 0.4), (-2.4, 2.4))
    ax.axhline(0, color=BASELINE, lw=2, zorder=1)
    for i, (year, label, color) in enumerate(EVENTS):
        up = i % 2 == 0
        y = 0.55 if up else -0.55
        ax.plot([i, i], [0, y], color=color, lw=1.6, zorder=2)
        ax.plot([i], [0], "o", ms=7, color=color, zorder=3)
        ax.text(i, y + (0.18 if up else -0.18), label, ha="center",
                va="bottom" if up else "top", fontsize=9.3, color=INK)
        ax.text(i, y + (1.28 if up else -1.28), year, ha="center",
                va="bottom" if up else "top", fontsize=10.5, color=color,
                weight="bold")
    ax.set_title("87 years of the Jacobian Conjecture", color=INK2,
                 fontsize=13)
    save_fig(fig, OUT / "timeline.png")


def pinchuk_heatmap():
    dfun = sp.lambdify(VARS, PINCHUK_DET_IDENTITY, "numpy")
    xs = np.linspace(-3, 3, 600)
    xx, yy = np.meshgrid(xs, xs)
    zz = np.asarray(dfun(xx, yy), float)
    zmin = zz.min()
    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    im = ax.pcolormesh(xx, yy, zz, cmap=SEQ_CMAP,
                       norm=LogNorm(vmin=max(zmin, 1e-4), vmax=zz.max()),
                       shading="auto")
    style_axes(ax, (-3, 3), (-3, 3), show_axes=False)
    ax.set_title("Pinchuk's map: local area factor at every real point\n"
                 f"(log scale — smallest value in this window ≈ {zmin:.3g}, never 0)",
                 color=INK2, fontsize=11.5)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.outline.set_visible(False)
    cb.ax.tick_params(color=MUTED, labelcolor=INK2)
    cb.set_label("det J  (always > 0)", color=INK2)
    save_fig(fig, OUT / "pinchuk_det.png")


if __name__ == "__main__":
    timeline()
    pinchuk_heatmap()
    print(f"wrote figures to {OUT}")
