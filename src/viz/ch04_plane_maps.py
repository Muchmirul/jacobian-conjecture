"""Figures for chapter 4 — maps of the plane (all animated)."""

import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from matplotlib.animation import FuncAnimation, PillowWriter

from common import out_dir
from jacobian_guide.examples import VARS, X, Y
from jacobian_guide.plotting import (BLUE, GREEN, GRIDLINE, INK2, animate_map,
                                     draw_grid, grid_polylines, lambdify_map,
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


def gallery_gif(fps=16, frames=40, hold=16):
    """Five basic ways to move the whole plane at once: the same blue grid
    obeys each rule and settles as the green result."""
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 7.6))
    lines = grid_polylines((-2, 2), (-2, 2), spacing=0.5)
    movers = []                     # (artist, x0, y0, x1, y1)
    for ax, (label, F) in zip(axes.flat, PANELS):
        style_axes(ax, (-2.7, 2.7), (-2.7, 2.7))
        draw_grid(ax, None, xlim=(-2, 2), ylim=(-2, 2), color=GRIDLINE,
                  lw=1.0, zorder=2)
        ax.set_title(label, color=INK2, fontsize=12)
        if F is None:
            draw_grid(ax, None, xlim=(-2, 2), ylim=(-2, 2), color=BLUE)
            continue
        f = lambdify_map(F, VARS)
        for pts in lines:
            u, v = f(pts[:, 0], pts[:, 1])
            art, = ax.plot([], [], lw=1.2, color=BLUE,
                           solid_capstyle="round", zorder=3)
            movers.append((art, pts[:, 0], pts[:, 1], u, v))
    fig.suptitle("a plane map is one rule that moves EVERY point at once",
                 color=INK2, fontsize=12.5)
    fig.tight_layout()

    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    c1 = np.array(matplotlib.colors.to_rgb(GREEN))
    total = frames + 2 * hold

    def update(i):
        t = min(max((i - hold) / frames, 0.0), 1.0)
        t = 3 * t**2 - 2 * t**3
        col = matplotlib.colors.to_hex((1 - t) * c0 + t * c1)
        for art, x0, y0, x1, y1 in movers:
            art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
            art.set_color(col)
        return [m[0] for m in movers]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "gallery.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def rubbersheet_gif():
    F = (X + sp.Rational(1, 4) * Y**2, Y + sp.Rational(1, 4) * X**2)
    animate_map(F, VARS, OUT / "rubbersheet.gif", xlim=(-2, 2), ylim=(-2, 2),
                spacing=0.4, view=((-2.8, 3.2), (-2.8, 3.2)), frames=44,
                hold_frames=10, points=[(1.0, 0.5), (-1.5, -1.0)],
                title="a plane map moves every point at once — watch the two travelers")


if __name__ == "__main__":
    gallery_gif()
    rubbersheet_gif()
    print(f"wrote figures to {OUT}")
