"""Figure for chapter 9 — the statement card."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from common import bare_axes, out_dir
from jacobian_guide.plotting import (BLUE, GOOD, GREEN, INK, INK2, MUTED,
                                     VIOLET, save_fig)

OUT = out_dir("09-the-conjecture")


def statement_card():
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    bare_axes(ax, (0, 10), (0, 10))
    card = FancyBboxPatch((0.45, 0.7), 9.1, 8.6,
                          boxstyle="round,pad=0.25,rounding_size=0.35",
                          fc="white", ec=BLUE, lw=2.6, zorder=2)
    ax.add_patch(card)
    ax.text(5, 8.55, "THE JACOBIAN CONJECTURE", ha="center", fontsize=17,
            color=INK, weight="bold")
    ax.text(5, 7.75, "Ott-Heinrich Keller, 1939", ha="center", fontsize=11,
            color=MUTED, style="italic")
    ax.text(0.95, 6.6, "Take a map of n-dimensional space in which every "
            "coordinate\nis computed by a polynomial.", fontsize=12.5,
            color=INK, va="center")
    ax.text(0.95, 5.15, "✓", fontsize=16, color=GOOD, weight="bold")
    ax.text(1.55, 5.15, "Suppose its local area factor (det of the Jacobian) is\n"
            "the SAME nonzero constant at every single point.", fontsize=12.5,
            color=INK, va="center")
    ax.text(0.95, 3.3, "?", fontsize=18, color=VIOLET, weight="bold")
    ax.text(1.55, 3.3, "Must the map then be perfectly invertible —\n"
            "with an undo map that is itself polynomial?", fontsize=13.5,
            color=VIOLET, va="center", weight="bold")
    ax.text(5, 1.6, "«yes» was believed, but never proved, for 87 years",
            ha="center", fontsize=11, color=MUTED, style="italic")
    save_fig(fig, OUT / "statement_card.png")


if __name__ == "__main__":
    statement_card()
    print(f"wrote figures to {OUT}")
