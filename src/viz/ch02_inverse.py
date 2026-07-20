"""Figures for chapter 2 — undo: inverse machines."""

import matplotlib.pyplot as plt

from common import animate_1d, arrow, bare_axes, number_line, out_dir
from jacobian_guide.plotting import (BLUE, GREEN, INK2, MUTED, RED, VIOLET,
                                     save_fig)

OUT = out_dir("02-the-undo-machine")


def undo_gif():
    animate_1d(lambda x: 2 * x, xs=[-3, -2, -1, 0, 1, 2, 3],
               out_path=OUT / "undo.gif", roundtrip=True,
               title="«double» sends numbers down — «halve» carries every one back home")


def collision_figure():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.6))

    # left: squaring collides
    ax = axes[0]
    bare_axes(ax, (-10.5, 11.5), (-0.75, 1.75))
    xlim = (-9.5, 10.5)
    number_line(ax, 1.0, xlim, [-9, -6, -3, 0, 3, 6, 9], label="in")
    number_line(ax, 0.0, xlim, [0, 3, 6, 9], label="out")
    for x in (-3, 3):
        arrow(ax, (x, 0.93), (x * x, 0.07), color=BLUE, lw=1.8, curve=0.12 if x < 0 else -0.12)
        ax.plot([x], [1.0], "o", ms=8, color=BLUE, zorder=6)
    ax.plot([9], [0.0], "o", ms=9, color=RED, zorder=6)
    ax.text(9, -0.42, "crash!  −3 and 3 both land on 9",
            ha="center", fontsize=10.5, color=RED)
    ax.text(-5.5, 0.22, "…and nothing ever lands over here",
            ha="center", fontsize=9.5, color=MUTED, style="italic")
    ax.set_title("«square it» cannot be undone", color=INK2, fontsize=12)

    # right: doubling keeps everyone separate
    ax = axes[1]
    bare_axes(ax, (-10.5, 11.5), (-0.75, 1.75))
    number_line(ax, 1.0, xlim, [-9, -6, -3, 0, 3, 6, 9], label="in")
    number_line(ax, 0.0, xlim, [-9, -6, -3, 0, 3, 6, 9], label="out")
    for x in (-4, -2, 0, 2, 4):
        arrow(ax, (x, 0.93), (2 * x, 0.07), color=BLUE, lw=1.6)
        ax.plot([x], [1.0], "o", ms=7, color=BLUE, zorder=6)
        ax.plot([2 * x], [0.0], "o", ms=7, color=GREEN, zorder=6)
    ax.text(0.5, -0.42, "no two arrows ever meet → you can trace each one back",
            ha="center", fontsize=10.5, color=MUTED)
    ax.set_title("«double it» can be undone", color=INK2, fontsize=12)

    fig.tight_layout()
    save_fig(fig, OUT / "collision.png")


if __name__ == "__main__":
    undo_gif()
    collision_figure()
    print(f"wrote figures to {OUT}")
