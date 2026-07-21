"""Figures for chapter 5, straight maps and the area factor (all animated)."""

import matplotlib.colors
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import out_dir
from jacobian_guide.core import linear_map
from jacobian_guide.examples import VARS
from jacobian_guide.plotting import (BLUE, GREEN, GRIDLINE, INK2, RED, YELLOW,
                                     animate_map, draw_grid, grid_polylines,
                                     lambdify_map, style_axes)

OUT = out_dir("05-straight-maps-and-area")

c, s = sp.cos(sp.rad(35)), sp.sin(sp.rad(35))
half = sp.Rational(1, 2)
PANELS = [
    ("turn: area ×1", linear_map(c, -s, s, c, VARS)),
    ("grow: area ×4", linear_map(2, 0, 0, 2, VARS)),
    ("squeeze: area ×1", linear_map(2, 0, 0, half, VARS)),
    ("lean: area ×1", linear_map(1, sp.Rational(3, 5), 0, 1, VARS)),
    ("mirror: area ×1, flipped (−1)", linear_map(0, 1, 1, 0, VARS)),
    ("squash: area ×0, flattened!", linear_map(1, 1, 1, 1, VARS)),
]


def gallery_gif(fps=16, frames=40, hold=16):
    """Six straight maps act on the plane at once; the yellow patch shows
    each map's area factor, its determinant, including the fatal ×0."""
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 7.6))
    lines = grid_polylines((-2, 2), (-2, 2), spacing=0.5)
    sq = np.linspace(0, 1, 30)
    movers, squares = [], []
    for ax, (label, F) in zip(axes.flat, PANELS):
        style_axes(ax, (-2.7, 2.7), (-2.7, 2.7))
        draw_grid(ax, None, xlim=(-2, 2), ylim=(-2, 2), color=GRIDLINE,
                  lw=1.0, zorder=2)
        ax.set_title(label, color=INK2, fontsize=11.5)
        f = lambdify_map(F, VARS)
        end_color = RED if "squash" in label else GREEN
        for pts in lines:
            u, v = f(pts[:, 0], pts[:, 1])
            art, = ax.plot([], [], lw=1.2, color=BLUE,
                           solid_capstyle="round", zorder=3)
            movers.append((art, pts[:, 0], pts[:, 1], u, v, end_color))
        corner = (0.5, 0.0) if "mirror" in label else (0.0, 0.0)
        xx, yy = np.meshgrid(corner[0] + sq, corner[1] + sq)
        ex, ey = f(xx, yy)
        squares.append({"ax": ax, "xx": xx, "yy": yy, "ex": ex, "ey": ey,
                        "art": None})
    fig.suptitle("straight maps: every patch of the plane changes area by "
                 "the SAME factor, the determinant", color=INK2,
                 fontsize=12.5)
    fig.tight_layout()

    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    total = frames + 2 * hold

    def update(i):
        t = min(max((i - hold) / frames, 0.0), 1.0)
        t = 3 * t**2 - 2 * t**3
        for art, x0, y0, x1, y1, endc in movers:
            c1 = np.array(matplotlib.colors.to_rgb(endc))
            art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
            art.set_color(matplotlib.colors.to_hex((1 - t) * c0 + t * c1))
        for q in squares:
            if q["art"] is not None:
                q["art"].remove()
            q["art"] = q["ax"].pcolormesh(
                (1 - t) * q["xx"] + t * q["ex"],
                (1 - t) * q["yy"] + t * q["ey"],
                np.ones((29, 29)), color=YELLOW, alpha=0.5,
                shading="flat", zorder=4)
        return [m[0] for m in movers]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "gallery.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def squash_gif():
    F = linear_map(1, 1, 1, 1, VARS)
    animate_map(F, VARS, OUT / "squash.gif", xlim=(-2, 2), ylim=(-2, 2),
                spacing=0.4, view=((-2.9, 2.9), (-2.9, 2.9)), frames=44,
                hold_frames=10, square=(0.0, 0.0),
                points=[(1.0, 0.0), (0.0, 1.0), (0.5, 0.5)],
                color_to=RED,
                title="det → 0: the whole plane lands on one line, information destroyed")


if __name__ == "__main__":
    gallery_gif()
    squash_gif()
    print(f"wrote figures to {OUT}")
