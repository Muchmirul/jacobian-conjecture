"""Figures for chapter 9 — the statement card + the question as a GIF."""

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyBboxPatch

from common import bare_axes, out_dir
from jacobian_guide.examples import TANGLED, VARS
from jacobian_guide.plotting import (BLUE, GOOD, GREEN, INK, INK2, MUTED,
                                     VIOLET, YELLOW, grid_polylines,
                                     lambdify_map, save_fig, style_axes)

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


def conjecture_gif(frames=42, fps=18, hold=16):
    """The whole question in one motion: a polynomial map scrambles the
    plane while its local area factor stays pinned at 1 (watch the yellow
    patch keep its area) — must the scrambling always be undoable?"""
    F = lambdify_map(TANGLED, VARS)
    lines = grid_polylines((-1, 1), (-1, 1), spacing=0.2)
    starts = [(pts[:, 0], pts[:, 1]) for pts in lines]
    ends = [F(x, y) for x, y in starts]
    s = np.linspace(-0.4, 0.4, 40)
    sq_x, sq_y = np.meshgrid(s, s)
    sq_u, sq_v = F(sq_x, sq_y)

    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    c1 = np.array(matplotlib.colors.to_rgb(GREEN))

    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    fig.subplots_adjust(top=0.84)
    style_axes(ax, (-1.7, 5.3), (-1.7, 2.4))
    artists = [ax.plot([], [], lw=1.2, solid_capstyle="round", zorder=3)[0]
               for _ in lines]
    state = {"sq": None}

    titles = (
        "take a polynomial map whose LOCAL area factor is exactly 1\n"
        "at every point — the yellow patch bends but never changes area…",
        "…must a polynomial undo map always exist?\n"
        "Keller, 1939: believed «yes» — unproven for 87 years",
    )

    def ease(t):
        return 3 * t**2 - 2 * t**3

    stage_len = frames + hold
    total = 2 * stage_len + hold

    def update(i):
        i = max(0, i - hold)
        stage, j = divmod(i, stage_len)
        t = ease(min(j / frames, 1.0))
        if stage >= 2:
            stage, t = 1, 1.0
        u = t if stage == 0 else 1 - t
        ax.set_title(titles[stage], color=INK2, fontsize=11.5)
        c = matplotlib.colors.to_hex((1 - u) * c0 + u * c1)
        for art, (x0, y0), (x1, y1) in zip(artists, starts, ends):
            art.set_data((1 - u) * x0 + u * x1, (1 - u) * y0 + u * y1)
            art.set_color(c)
        if state["sq"] is not None:
            state["sq"].remove()
        state["sq"] = ax.pcolormesh((1 - u) * sq_x + u * sq_u,
                                    (1 - u) * sq_y + u * sq_v,
                                    np.ones((39, 39)), color=YELLOW,
                                    alpha=0.5, shading="flat", zorder=4)
        return artists

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "conjecture.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    statement_card()
    conjecture_gif()
    print(f"wrote figures to {OUT}")
