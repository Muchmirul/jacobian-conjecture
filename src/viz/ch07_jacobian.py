"""Figures for chapter 7 — the microscope: Jacobian = the local straight map."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import bare_axes, out_dir
from jacobian_guide.core import jacobian_det
from jacobian_guide.examples import FOLD, SHEAR_RIGHT, TANGLED, VARS
from jacobian_guide.plotting import (BLUE, DIV_CMAP, GREEN, INK2, MUTED, RED,
                                     VIOLET, lambdify_map, style_axes)
import sympy as sp

OUT = out_dir("07-the-microscope")

P = (0.5, 0.5)                      # where we point the microscope
F = lambdify_map(TANGLED, VARS)


def zoom1d_gif(frames=56, fps=16, hold=12):
    """Zoom into the parabola y = x² at (1, 1): the closer you look, the
    straighter it gets, until it IS a straight line of slope 2."""
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    r0, r1 = 1.6, 0.05

    def ease(t):
        return 3 * t**2 - 2 * t**3

    total = frames + 2 * hold

    def update(i):
        ax.clear()
        t = ease(min(max((i - hold) / (frames - 1), 0.0), 1.0))
        r = r0 * (r1 / r0) ** t
        xs = np.linspace(1 - r, 1 + r, 300)
        ax.plot(xs, xs**2, color=BLUE, lw=2.4)
        if t > 0.75:                       # the tangent emerges from the curve
            a = (t - 0.75) / 0.25
            ax.plot(xs, 1 + 2 * (xs - 1), ls="--", lw=1.6, color=VIOLET,
                    alpha=0.8 * a)
            ax.text(0.97, 0.06, "…just a straight line of slope 2",
                    transform=ax.transAxes, ha="right", fontsize=11,
                    color=MUTED, style="italic", alpha=a)
        ax.plot([1], [1], "o", ms=7, color=VIOLET, zorder=5)
        bare_axes(ax, (1 - r, 1 + r), (1 - 2.2 * r, 1 + 2.2 * r))
        ax.set_title("zooming in on the curve y = x² at the point (1, 1)",
                     color=INK2, fontsize=12)
        ax.text(0.03, 0.03, f"zoom ×{r0 / r:.0f}", transform=ax.transAxes,
                fontsize=11, color=MUTED, style="italic")

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "zoom1d.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def microscope_gif(frames=64, fps=16, hold=10):
    """A real microscope move: the camera stays locked on the dot F(p) with a
    fixed (equal) aspect and simply narrows its field of view, so the only
    motion is a pure zoom.  The grid refines as we go deeper — finer lines
    (aligned to p, so they subdivide the coarse ones) fade in — and under
    magnification everything straightens out."""
    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    r0, r1 = 1.1, 0.035              # source-window radius, start -> end
    s0 = r0 / 3                      # coarsest grid spacing
    q = np.concatenate(F(np.array([P[0]]), np.array([P[1]])))

    def ease(t):
        return 3 * t**2 - 2 * t**3

    def window_lines(spacing, r, odd_only=False):
        """Grid lines through p at multiples of `spacing`, covering radius r."""
        ks = np.arange(np.ceil(-r / spacing), np.floor(r / spacing) + 1)
        if odd_only:
            ks = ks[ks.astype(int) % 2 != 0]
        t = np.linspace(-r, r, 160)
        lines = []
        for k in ks:
            c = np.full_like(t, k * spacing)
            lines.append((P[0] + c, P[1] + t))
            lines.append((P[0] + t, P[1] + c))
        return lines

    def camera_radius(r):
        """Half-width of the view: fit the mapped boundary of the radius-r
        source square around p, keeping q dead center."""
        t = np.linspace(-r, r, 240)
        e = np.full_like(t, r)
        bx = np.concatenate([P[0] + t, P[0] + t, P[0] - e, P[0] + e])
        by = np.concatenate([P[1] - e, P[1] + e, P[1] + t, P[1] + t])
        u, v = F(bx, by)
        # 0.65: crop into the window so the grid fills the frame and bleeds
        # past the edges (the drawn window is 2r, so there is plenty drawn)
        return 0.65 * max(np.abs(u - q[0]).max(), np.abs(v - q[1]).max())

    def update(i):
        ax.clear()
        t = ease(min(max((i - hold) / (frames - 1), 0.0), 1.0))
        r = r0 * (r1 / r0) ** t
        level = np.log2(r0 / r)
        n, frac = int(level), level - int(level)
        for spacing, alpha, odd in ((s0 / 2**n, 1.0, False),
                                    (s0 / 2**(n + 1), ease(frac), True)):
            if alpha < 0.02:
                continue
            for lx, ly in window_lines(spacing, 2 * r, odd):
                u, v = F(lx, ly)
                ax.plot(u, v, color=GREEN, lw=1.4, alpha=alpha,
                        solid_capstyle="round", zorder=3)
        ax.plot([q[0]], [q[1]], "o", ms=7, color=VIOLET, zorder=6)
        R = camera_radius(r)
        style_axes(ax, (q[0] - R, q[0] + R), (q[1] - R, q[1] + R),
                   show_axes=False)
        ax.set_title("zooming in on one dot — the bent grid straightens out",
                     color=INK2, fontsize=12)
        ax.text(0.03, 0.03, f"zoom ×{r0 / r:.0f}", transform=ax.transAxes,
                fontsize=11, color=MUTED, style="italic")

    anim = FuncAnimation(fig, update, frames=frames + 2 * hold,
                         interval=1000 / fps)
    anim.save(OUT / "microscope.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def det_heatmaps_gif(frames=88, fps=16):
    """A probe wanders over two maps at once.  Over the shear its local area
    factor reads 1.00 wherever it goes; over the fold the readout is 2x —
    positive, negative, and exactly 0 on the crease."""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.1))
    dfuns = []
    for ax, Fm, title in ((axes[0], SHEAR_RIGHT,
                           "(x + y², y)   local area factor ≡ 1 everywhere"),
                          (axes[1], FOLD,
                           "(x², y)   local area factor = 2x")):
        d = jacobian_det(Fm, VARS)
        dfun = sp.lambdify(VARS, d, "numpy")
        dfuns.append(dfun)
        xs = np.linspace(-2, 2, 400)
        xx, yy = np.meshgrid(xs, xs)
        zz = np.broadcast_to(np.asarray(dfun(xx, yy), float), xx.shape)
        im = ax.pcolormesh(xx, yy, zz, cmap=DIV_CMAP, vmin=-4.2, vmax=4.2,
                           shading="auto")
        style_axes(ax, (-2, 2), (-2, 2), show_axes=False)
        ax.set_title(title, color=INK2, fontsize=11.5)
    axes[1].plot([0, 0], [-2, 2], ls="--", lw=2, color=RED)
    axes[1].text(0.12, -1.75, "area factor 0 — the crease", color=RED,
                 fontsize=10.5, rotation=90)
    cb = fig.colorbar(im, ax=axes, shrink=0.85, pad=0.02)
    cb.outline.set_visible(False)
    cb.ax.tick_params(color=MUTED, labelcolor=INK2)
    cb.set_label("local area factor (det J)", color=INK2)

    probes = [ax.plot([], [], "o", ms=10, color=VIOLET, mec="white",
                      mew=1.5, zorder=6)[0] for ax in axes]
    reads = [ax.text(0.5, -0.075, "", transform=ax.transAxes, ha="center",
                     fontsize=11.5, family="monospace") for ax in axes]

    def update(i):
        t = i / frames
        px = 1.55 * np.sin(2 * np.pi * t)
        py = 1.55 * np.sin(4 * np.pi * t + np.pi / 3)
        for probe, read, dfun in zip(probes, reads, dfuns):
            probe.set_data([px], [py])
            v = float(dfun(px, py))
            if abs(v) < 0.12:
                read.set_text("area factor here = 0 — crushed!")
                read.set_color(RED)
            else:
                read.set_text(f"area factor here = {v:+.2f}")
                read.set_color(RED if v < 0 else BLUE)
        return [*probes, *reads]

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps)
    anim.save(OUT / "det_heatmaps.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    zoom1d_gif()
    microscope_gif()
    det_heatmaps_gif()
    print(f"wrote figures to {OUT}")
