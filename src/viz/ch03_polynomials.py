"""Figures for chapter 3 — polynomials, the machines made of + and × (animated)."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import bare_axes, out_dir
from jacobian_guide.plotting import BASELINE, BLUE, INK2, MUTED

OUT = out_dir("03-polynomials")


def gallery_gif(fps=16, seg=18, hold=24):
    """Each machine draws its own graph, one panel at a time: three smooth
    unbroken polynomial sweeps, then the impostors (dashed, gray) that need
    trig, division or roots — not + and × alone."""
    xs = np.linspace(-3, 3, 400)
    with np.errstate(divide="ignore", invalid="ignore"):
        inv = 1 / xs
        inv[np.abs(xs) < 0.18] = np.nan
        sq = np.sqrt(np.where(xs >= 0, xs, np.nan))
    curves = [                     # (panel, ys, color, dashed)
        (0, 2 * xs + 1, BLUE, False),
        (1, xs**2, BLUE, False),
        (2, xs**3 - 2 * xs, BLUE, False),
        (3, np.sin(3 * xs), MUTED, True),
        (3, inv, MUTED, True),
        (3, sq, MUTED, True),
    ]
    titles = ["2x + 1", "x²", "x³ − 2x", "not polynomials"]

    fig, axes = plt.subplots(1, 4, figsize=(12.8, 3.6))
    for ax, label in zip(axes, titles):
        ax.axhline(0, color=BASELINE, lw=1, zorder=1)
        ax.axvline(0, color=BASELINE, lw=1, zorder=1)
        bare_axes(ax, (-3, 3), (-4.5, 4.5))
        ax.set_title(label, color=INK2, fontsize=12)
    impostor_label = axes[3].text(0.03, 0.03, "sin x,  1/x,  √x",
                                  transform=axes[3].transAxes, fontsize=10.5,
                                  color=MUTED, alpha=0.0)
    fig.suptitle("machines made only of  +  and  ×  draw single unbroken sweeps",
                 color=INK2, fontsize=12, y=1.0)
    arts = [axes[p].plot([], [], color=c, lw=2.2 if not d else 1.8,
                         ls="--" if d else "-")[0] for p, _, c, d in curves]
    fig.tight_layout()

    total = 4 * seg + hold

    def update(i):
        for art, (p, ys, _, _) in zip(arts, curves):
            t = min(max((i - p * seg) / seg, 0.0), 1.0)
            n = int(t * len(xs))
            art.set_data(xs[:n], ys[:n])
        impostor_label.set_alpha(1.0 if i >= 4 * seg else 0.0)
        return [*arts, impostor_label]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "gallery.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    gallery_gif()
    print(f"wrote figures to {OUT}")
