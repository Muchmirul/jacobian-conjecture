"""Figures for chapter 4 — maps of the plane."""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from common import out_dir
from jacobian_guide.examples import VARS, X, Y
from jacobian_guide.plotting import (BLUE, GREEN, GRIDLINE, INK2, animate_map,
                                     draw_grid, lambdify_map, save_fig,
                                     style_axes)

OUT = out_dir("04-maps-of-the-plane")

c, s = sp.cos(sp.rad(35)), sp.sin(sp.rad(35))
PANELS = [
    ("the plane, untouched", None),
    ("slide", (X + 1.1, Y + 0.5)),
    ("turn", (c * X - s * Y, s * X + c * Y)),
    ("grow", (sp.Rational(3, 2) * X, sp.Rational(3, 2) * Y)),
    ("lean", (X + sp.Rational(3, 5) * Y, Y)),
    ("bend", (X + sp.Rational(1, 4) * Y**2, Y + sp.Rational(1, 4) * X**2)),
]


def gallery():
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 7.4))
    for ax, (label, F) in zip(axes.flat, PANELS):
        style_axes(ax, (-2.7, 2.7), (-2.7, 2.7))
        draw_grid(ax, None, xlim=(-2, 2), ylim=(-2, 2), color=GRIDLINE,
                  lw=1.0, zorder=2)
        if F is None:
            draw_grid(ax, None, xlim=(-2, 2), ylim=(-2, 2), color=BLUE)
        else:
            draw_grid(ax, lambdify_map(F, VARS), xlim=(-2, 2), ylim=(-2, 2),
                      color=GREEN)
        ax.set_title(label, color=INK2, fontsize=12)
    fig.tight_layout()
    save_fig(fig, OUT / "gallery.png")


def rubbersheet_gif():
    F = (X + sp.Rational(1, 4) * Y**2, Y + sp.Rational(1, 4) * X**2)
    animate_map(F, VARS, OUT / "rubbersheet.gif", xlim=(-2, 2), ylim=(-2, 2),
                spacing=0.4, view=((-2.8, 3.2), (-2.8, 3.2)), frames=44,
                hold_frames=10, points=[(1.0, 0.5), (-1.5, -1.0)],
                title="a plane map moves every point at once — watch the two travelers")


if __name__ == "__main__":
    gallery()
    rubbersheet_gif()
    print(f"wrote figures to {OUT}")
