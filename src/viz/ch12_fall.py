"""Figure for chapter 12 — the 2026 counterexample collision card."""

import matplotlib.pyplot as plt

from common import arrow, bare_axes, draw_machine, out_dir
from jacobian_guide.plotting import (BLUE, GREEN, INK, INK2, MUTED, RED,
                                     VIOLET, save_fig)

OUT = out_dir("12-the-fall")

POINTS = ["( 0,  0,  −1/4 )", "( 1,  −3/2,  13/2 )", "( −1,  3/2,  13/2 )"]


def collision_card():
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    bare_axes(ax, (0, 10), (0, 10))
    ax.text(5, 9.35, "one map, constant det J = −2   …and yet:", ha="center",
            fontsize=13, color=INK2)
    for i, p in enumerate(POINTS):
        y = 6.9 - 2.1 * i
        draw_machine(ax, (0.7, y), (2.9, 1.05), p, color=BLUE, fontsize=11.5)
        arrow(ax, (3.85, y + 0.5), (6.05, 4.85 + (y + 0.5 - 4.85) * 0.12),
              color=MUTED, lw=1.8, curve=0.0)
    draw_machine(ax, (6.3, 4.28), (3.0, 1.15), "( −1/4,  0,  0 )",
                 color=RED, fontsize=12.5)
    ax.text(7.8, 3.35, "three different starting points,\nexactly the same landing spot",
            ha="center", fontsize=10.5, color=RED)
    ax.text(5, 1.15, "a perfect undo machine is impossible: standing at (−1/4, 0, 0)\n"
            "you cannot know which of the three roads you came by",
            ha="center", fontsize=11.5, color=INK)
    save_fig(fig, OUT / "collision_card.png")


if __name__ == "__main__":
    collision_card()
    print(f"wrote figures to {OUT}")
