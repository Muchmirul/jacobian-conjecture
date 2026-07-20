"""Figures for chapter 5 — straight maps and the area factor (determinant)."""

import sympy as sp
import matplotlib.pyplot as plt

from common import out_dir
from jacobian_guide.core import linear_map
from jacobian_guide.examples import VARS
from jacobian_guide.plotting import (BLUE, GREEN, GRIDLINE, INK2, RED,
                                     animate_map, draw_grid, draw_unit_square,
                                     lambdify_map, save_fig, style_axes)

OUT = out_dir("05-straight-maps-and-area")

c, s = sp.cos(sp.rad(35)), sp.sin(sp.rad(35))
half = sp.Rational(1, 2)
PANELS = [
    ("turn — area ×1", linear_map(c, -s, s, c, VARS)),
    ("grow — area ×4", linear_map(2, 0, 0, 2, VARS)),
    ("squeeze — area ×1", linear_map(2, 0, 0, half, VARS)),
    ("lean — area ×1", linear_map(1, sp.Rational(3, 5), 0, 1, VARS)),
    ("mirror — area ×1, flipped (−1)", linear_map(0, 1, 1, 0, VARS)),
    ("squash — area ×0 : flattened!", linear_map(1, 1, 1, 1, VARS)),
]


def gallery():
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 7.4))
    for ax, (label, F) in zip(axes.flat, PANELS):
        style_axes(ax, (-2.7, 2.7), (-2.7, 2.7))
        draw_grid(ax, None, xlim=(-2, 2), ylim=(-2, 2), color=GRIDLINE,
                  lw=1.0, zorder=2)
        f = lambdify_map(F, VARS)
        draw_grid(ax, f, xlim=(-2, 2), ylim=(-2, 2),
                  color=RED if "squash" in label else GREEN)
        # off-diagonal square so the mirror panel's flip is actually visible
        draw_unit_square(ax, f, corner=(0.5, 0.0) if "mirror" in label
                         else (0.0, 0.0))
        ax.set_title(label, color=INK2, fontsize=12)
    fig.tight_layout()
    save_fig(fig, OUT / "gallery.png")


def squash_gif():
    F = linear_map(1, 1, 1, 1, VARS)
    animate_map(F, VARS, OUT / "squash.gif", xlim=(-2, 2), ylim=(-2, 2),
                spacing=0.4, view=((-2.9, 2.9), (-2.9, 2.9)), frames=44,
                hold_frames=10, square=(0.0, 0.0),
                points=[(1.0, 0.0), (0.0, 1.0), (0.5, 0.5)],
                color_to=RED,
                title="det → 0 : the whole plane lands on one line — information destroyed")


if __name__ == "__main__":
    gallery()
    squash_gif()
    print(f"wrote figures to {OUT}")
