"""Figures for chapter 1 — functions are machines."""

import matplotlib.pyplot as plt

from common import (animate_1d, arrow, bare_axes, draw_machine, out_dir)
from jacobian_guide.plotting import BLUE, GREEN, INK, INK2, MUTED, save_fig

OUT = out_dir("01-functions-are-machines")


def machine_diagram():
    fig, ax = plt.subplots(figsize=(7.6, 2.9))
    bare_axes(ax, (0, 10), (0, 3))
    draw_machine(ax, (3.4, 0.9), (3.2, 1.2), "double it,\nthen add 1")
    arrow(ax, (1.6, 1.5), (3.25, 1.5))
    arrow(ax, (6.85, 1.5), (8.5, 1.5), color=GREEN)
    ax.text(1.1, 1.5, "3", fontsize=22, ha="center", va="center", color=BLUE)
    ax.text(9.0, 1.5, "7", fontsize=22, ha="center", va="center", color=GREEN)
    ax.text(1.1, 0.95, "in", fontsize=10, ha="center", color=MUTED)
    ax.text(9.0, 0.95, "out", fontsize=10, ha="center", color=MUTED)
    for x_in, y in ((0, 2.72), (1, 2.40), (10, 2.08)):
        ax.text(1.15, y, f"{x_in:>2}  →  {2 * x_in + 1}", fontsize=10,
                ha="center", color=INK2, family="monospace")
    ax.text(5.0, 0.35, "same input in, same output out — every single time",
            fontsize=10.5, ha="center", color=MUTED, style="italic")
    save_fig(fig, OUT / "machine.png")


def numberline_gif():
    animate_1d(lambda x: 2 * x + 1, xs=[-3, -2, -1, 0, 1, 2, 3],
               out_path=OUT / "numberline.gif",
               title="the machine  «double, then add 1»  moves every number at once")


if __name__ == "__main__":
    machine_diagram()
    numberline_gif()
    print(f"wrote figures to {OUT}")
