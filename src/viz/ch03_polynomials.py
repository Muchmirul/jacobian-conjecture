"""Figures for chapter 3 — polynomials, the machines made of + and ×."""

import numpy as np
import matplotlib.pyplot as plt

from common import bare_axes, out_dir
from jacobian_guide.plotting import (BASELINE, BLUE, INK2, MUTED, save_fig)

OUT = out_dir("03-polynomials")


def panel(ax, xs, ys, label, color=BLUE, dashed=False):
    ax.plot(xs, ys, color=color, lw=2.2,
            ls="--" if dashed else "-")
    ax.axhline(0, color=BASELINE, lw=1, zorder=1)
    ax.axvline(0, color=BASELINE, lw=1, zorder=1)
    bare_axes(ax, (-3, 3), (-4.5, 4.5))
    ax.set_title(label, color=INK2, fontsize=12)


def gallery():
    xs = np.linspace(-3, 3, 400)
    fig, axes = plt.subplots(1, 4, figsize=(12.8, 3.4))
    panel(axes[0], xs, 2 * xs + 1, "2x + 1")
    panel(axes[1], xs, xs**2, "x²")
    panel(axes[2], xs, xs**3 - 2 * xs, "x³ − 2x")
    ax = axes[3]
    with np.errstate(divide="ignore", invalid="ignore"):
        panel(ax, xs, np.sin(3 * xs), "not polynomials", color=MUTED,
              dashed=True)
        inv = 1 / xs
        inv[np.abs(xs) < 0.18] = np.nan
        ax.plot(xs, inv, color=MUTED, lw=1.8, ls="--")
        sq = np.sqrt(np.where(xs >= 0, xs, np.nan))
        ax.plot(xs, sq, color=MUTED, lw=1.8, ls="--")
    ax.text(0.03, 0.03, "sin x,  1/x,  √x", transform=ax.transAxes,
            fontsize=10.5, color=MUTED)
    fig.tight_layout()
    save_fig(fig, OUT / "gallery.png")


if __name__ == "__main__":
    gallery()
    print(f"wrote figures to {OUT}")
