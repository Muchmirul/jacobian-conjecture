"""Figures for chapter 6 — polynomial maps bend the grid (all animated)."""

import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import out_dir
from jacobian_guide.examples import (CRUSH, FOLD, SHEAR_RIGHT, SHEAR_UP,
                                     TANGLED, VARS)
from jacobian_guide.plotting import (BLUE, GREEN, INK2, RED, VIOLET,
                                     animate_map, grid_polylines,
                                     lambdify_map, style_axes)

OUT = out_dir("06-bending-the-grid")


def shear_gif():
    animate_map(SHEAR_RIGHT, VARS, OUT / "shear.gif", xlim=(-2, 2),
                ylim=(-2, 2), spacing=0.4, view=((-2.6, 6.3), (-2.3, 2.3)),
                frames=48, hold_frames=10, square=(0.0, 0.0),
                figsize=(7.8, 4.3),
                title="slide each row right by y² — bent, but the yellow patch keeps area 1")


def fold_gif():
    animate_map(FOLD, VARS, OUT / "fold.gif", xlim=(-1.5, 1.5),
                ylim=(-1.5, 1.5), spacing=0.25,
                view=((-1.8, 2.6), (-1.8, 1.8)), frames=48, hold_frames=10,
                points=[(-1.0, 0.6), (1.0, 0.6)], figsize=(7.2, 5.2),
                title="(x², y) folds the plane like a book — the two dots crash")


def tangled_gif(fps=16, frames=36, hold=14):
    """The 'monster' built live: shear #1 slides columns up by x², then
    shear #2 slides rows right by y² — wild-looking, yet only two tame
    stacked moves."""
    f1 = lambdify_map(SHEAR_UP, VARS)
    f2 = lambdify_map(TANGLED, VARS)
    lines = grid_polylines((-1, 1), (-1, 1), spacing=0.2)
    P = [[(pts[:, 0], pts[:, 1]) for pts in lines],
         [f1(pts[:, 0], pts[:, 1]) for pts in lines],
         [f2(pts[:, 0], pts[:, 1]) for pts in lines]]

    fig, ax = plt.subplots(figsize=(10.0, 4.4))
    fig.subplots_adjust(top=0.86)
    style_axes(ax, (-1.6, 5.2), (-1.7, 2.3))
    arts = [ax.plot([], [], lw=1.2, solid_capstyle="round", zorder=3)[0]
            for _ in lines]
    titles = ("stack shear #1 — slide each column up by x²",
              "stack shear #2 — slide each row right by y²\n"
              "…a wild-looking map, built from two simple moves")
    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    c1 = np.array(matplotlib.colors.to_rgb(GREEN))

    stage_len = frames + hold
    total = 2 * stage_len + hold

    def update(i):
        i = max(0, i - hold)
        stage, j = divmod(i, stage_len)
        t = min(j / frames, 1.0)
        if stage >= 2:
            stage, t = 1, 1.0
        t = 3 * t**2 - 2 * t**3
        ax.set_title(titles[stage], color=INK2, fontsize=11.5)
        u = (stage + t) / 2
        col = matplotlib.colors.to_hex((1 - u) * c0 + u * c1)
        A, B = P[stage], P[stage + 1]
        for art, (x0, y0), (x1, y1) in zip(arts, A, B):
            art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
            art.set_color(col)
        return arts

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "tangled.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def crush_gif(fps=16, frames=44, hold=14):
    """(x, x·y): the grid morphs, and the RED vertical line — infinitely many
    different points — collapses onto the single point (0, 0)."""
    f = lambdify_map(CRUSH, VARS)
    lines = grid_polylines((-2, 2), (-2, 2), spacing=0.4)
    data = []
    for pts in lines:
        u, v = f(pts[:, 0], pts[:, 1])
        data.append((pts[:, 0], pts[:, 1], u, v))
    ry = np.linspace(-2, 2, 100)
    red = (np.zeros_like(ry), ry, np.zeros_like(ry), np.zeros_like(ry))

    fig, ax = plt.subplots(figsize=(7.0, 6.2))
    style_axes(ax, (-2.5, 2.5), (-2.5, 2.5))
    ax.set_title("(x, x·y) — watch the red line: a whole LINE of points\n"
                 "lands on the single point (0, 0)", color=INK2, fontsize=11.5)
    arts = [ax.plot([], [], lw=1.2, color=BLUE, solid_capstyle="round",
                    zorder=3)[0] for _ in lines]
    red_art, = ax.plot([], [], lw=3.0, color=RED, zorder=5,
                       solid_capstyle="round")
    crush_dot, = ax.plot([], [], "o", ms=10, color=RED, zorder=6)
    caption = ax.text(0.5, 0.04, "an entire line's worth of information — gone",
                      transform=ax.transAxes, ha="center", fontsize=11,
                      color=RED, alpha=0.0)
    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    c1 = np.array(matplotlib.colors.to_rgb(GREEN))

    total = frames + 2 * hold

    def update(i):
        t = min(max((i - hold) / frames, 0.0), 1.0)
        t = 3 * t**2 - 2 * t**3
        col = matplotlib.colors.to_hex((1 - t) * c0 + t * c1)
        for art, (x0, y0, x1, y1) in zip(arts, data):
            art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
            art.set_color(col)
        x0, y0, x1, y1 = red
        red_art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
        if t >= 1.0:
            crush_dot.set_data([0], [0])
            caption.set_alpha(1.0)
        return [*arts, red_art, crush_dot, caption]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "crush.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    shear_gif()
    fold_gif()
    tangled_gif()
    crush_gif()
    print(f"wrote figures to {OUT}")
