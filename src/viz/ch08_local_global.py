"""Figures for chapter 8 — locally fine everywhere, globally broken."""

import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import out_dir
from jacobian_guide.examples import VARS, Z_SQUARED
from jacobian_guide.plotting import (BLUE, GREEN, INK2, MUTED, RED, SEQ_CMAP,
                                     VIOLET, lambdify_map, save_fig,
                                     style_axes)

OUT = out_dir("08-local-vs-global")

F = lambdify_map(Z_SQUARED, VARS)          # (x² − y², 2xy): angle doubling


def _annulus_lines(theta_lo, theta_hi, r_lo=0.55, r_hi=1.45, offset=0.0):
    """Polar grid lines for one half of the annulus.

    `offset` staggers the radii and ray angles so that when the two halves
    land on the same ring, their webs interleave instead of hiding each
    other — the double cover stays visible.
    """
    lines = []
    for r in np.arange(r_lo + offset * 0.075, r_hi + 1e-9, 0.15):
        th = np.linspace(theta_lo, theta_hi, 200)
        lines.append(np.column_stack([r * np.cos(th), r * np.sin(th)]))
    rays = np.linspace(theta_lo, theta_hi, 13)[:-1] + offset * np.pi / 24
    for th in rays:
        rr = np.linspace(r_lo, r_hi, 60)
        lines.append(np.column_stack([rr * np.cos(th), rr * np.sin(th)]))
    return lines


YELLOW_DARK = "#c98500"    # second-half color: high contrast against blue


def wrap_gif(frames=52, fps=18, hold=10):
    halves = [(_annulus_lines(-np.pi / 2, np.pi / 2), BLUE),
              (_annulus_lines(np.pi / 2, 3 * np.pi / 2, offset=1.0),
               YELLOW_DARK)]
    dots = [(1.0, 0.6), (-1.0, -0.6)]      # they land on the same spot

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    style_axes(ax, (-2.5, 2.5), (-2.5, 2.5))
    ax.set_title("each half is fine on its own — together they land on the SAME ring",
                 color=INK2, fontsize=11.5)

    artists, data = [], []
    for lines, color in halves:
        for pts in lines:
            art, = ax.plot([], [], lw=1.3, color=color, alpha=0.75, zorder=3)
            u, v = F(pts[:, 0], pts[:, 1])
            artists.append(art)
            data.append((pts[:, 0], pts[:, 1], u, v))
    dot_art, dot_data = [], []
    for (px, py), color in zip(dots, (BLUE, YELLOW_DARK)):
        (qx,), (qy,) = F(np.array([px]), np.array([py]))
        dot_art.append(ax.plot([], [], "o", ms=9, color=color, zorder=6)[0])
        dot_data.append((px, py, qx, qy))

    def ease(t):
        return 3 * t**2 - 2 * t**3

    def update(i):
        t = ease(min(max((i - hold) / frames, 0.0), 1.0))
        for art, (x0, y0, x1, y1) in zip(artists, data):
            art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
        for art, (px, py, qx, qy) in zip(dot_art, dot_data):
            art.set_data([(1 - t) * px + t * qx], [(1 - t) * py + t * qy])
        return artists

    anim = FuncAnimation(fig, update, frames=frames + 2 * hold,
                         interval=1000 / fps)
    anim.save(OUT / "wrap.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def one_bad_point_gif(frames=76, fps=16, hold=18):
    """A probe spirals inward over the map (x² − y², 2xy), reading off the
    local area factor 4(x² + y²) as it goes: healthy everywhere… until the
    single point at the origin, where it hits exactly 0."""
    xs = np.linspace(-2, 2, 400)
    xx, yy = np.meshgrid(xs, xs)
    zz = 4 * (xx**2 + yy**2)               # det J of (x²−y², 2xy)
    fig, ax = plt.subplots(figsize=(6.6, 5.7))
    im = ax.pcolormesh(xx, yy, zz, cmap=SEQ_CMAP, vmin=0, vmax=zz.max(),
                       shading="auto")
    style_axes(ax, (-2, 2), (-2, 2), show_axes=False)
    ax.set_title("(x² − y², 2xy): local area factor 4(x² + y²)",
                 color=INK2, fontsize=12)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.outline.set_visible(False)
    cb.ax.tick_params(color=MUTED, labelcolor=INK2)
    probe, = ax.plot([], [], "o", ms=10, color=VIOLET, mec="white", mew=1.5,
                     zorder=6)
    trail, = ax.plot([], [], lw=1.2, color=VIOLET, alpha=0.35, zorder=5)
    read = ax.text(0.5, -0.075, "", transform=ax.transAxes, ha="center",
                   fontsize=11.5, family="monospace", color=BLUE)
    bad = ax.text(0.5, 0.05, "hits 0 HERE — and only here", ha="center",
                  transform=ax.transAxes, fontsize=11.5, color=RED,
                  weight="bold", alpha=0.0)

    def ease(t):
        return 3 * t**2 - 2 * t**3

    total = frames + hold

    def update(i):
        t = ease(min(i / (frames - 1), 1.0))
        tt = np.linspace(0, t, 200)
        rr = 1.7 * (1 - tt)
        th = 4 * np.pi * tt
        px, py = rr[-1] * np.cos(th[-1]), rr[-1] * np.sin(th[-1])
        trail.set_data(rr * np.cos(th), rr * np.sin(th))
        probe.set_data([px], [py])
        v = 4 * (px**2 + py**2)
        read.set_text(f"area factor here = {v:.2f}")
        if t >= 1.0:
            probe.set_color(RED)
            read.set_text("area factor here = 0.00")
            read.set_color(RED)
            bad.set_alpha(1.0)
        return [probe, trail, read, bad]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "one_bad_point.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    wrap_gif()
    one_bad_point_gif()
    print(f"wrote figures to {OUT}")
