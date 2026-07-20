"""Matplotlib helpers shared by every figure and animation in the guide.

Visual language (kept consistent across all chapters):

* blue   = inputs / the plane before the map
* green  = outputs / the plane after the map
* red    = trouble (collisions, crushed directions, det = 0)
* thin warm-gray grid = the untouched background plane

Colors come from a validated colorblind-safe palette; figures render on a
near-white surface so they read on both light and dark GitHub themes.
"""

from __future__ import annotations

from typing import Callable, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap

# --- palette ---------------------------------------------------------------

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

BLUE = "#2a78d6"     # inputs / before
GREEN = "#008300"    # outputs / after
RED = "#d03b3b"      # trouble
GOOD = "#0ca30c"
VIOLET = "#4a3aa7"
YELLOW = "#eda100"

#: sequential blue ramp, light -> dark (steps 100..700 of the palette)
SEQ_BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
            "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281",
            "#0d366b"]

SEQ_CMAP = LinearSegmentedColormap.from_list("guide_seq", SEQ_BLUE)

#: diverging red <- gray -> blue for signed quantities (e.g. det J):
#: calm blue for positive, warning red for mirror-flipped negative, and the
#: recessive gray exactly at the dangerous value 0
DIV_CMAP = LinearSegmentedColormap.from_list(
    "guide_div", ["#7c1d1d", "#d03b3b", "#eea9a9", "#f0efec", "#9ec5f4",
                  "#2a78d6", "#0d366b"])

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "sans-serif",
    "font.size": 11,
    "text.color": INK,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.grid": False,
    "figure.dpi": 110,
})


# --- sympy -> fast numpy ---------------------------------------------------

def lambdify_map(F: Sequence[sp.Expr],
                 variables: Sequence[sp.Symbol]) -> Callable:
    """Turn a sympy map into f(x, y) -> (u, v) working on numpy arrays."""
    fs = [sp.lambdify(variables, f, "numpy") for f in F]

    def f(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        return tuple(np.broadcast_to(np.asarray(fi(x, y), float), x.shape).copy()
                     for fi in fs)

    return f


# --- axes styling ----------------------------------------------------------

def style_axes(ax, xlim=None, ylim=None, show_axes=True, equal=True):
    """Recessive chart chrome: hairline center axes, no box, no ticks."""
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    if equal:
        ax.set_aspect("equal")
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    if show_axes:
        ax.axhline(0, color=BASELINE, lw=1, zorder=1)
        ax.axvline(0, color=BASELINE, lw=1, zorder=1)


# --- grids and their images ------------------------------------------------

def grid_polylines(xlim=(-2, 2), ylim=(-2, 2), spacing=0.5,
                   samples=200) -> list[np.ndarray]:
    """The plane's grid as a list of (N, 2) polylines, densely sampled so
    curved images stay smooth."""
    lines = []
    xs = np.arange(xlim[0], xlim[1] + 1e-9, spacing)
    ys = np.arange(ylim[0], ylim[1] + 1e-9, spacing)
    t_v = np.linspace(ylim[0], ylim[1], samples)
    t_h = np.linspace(xlim[0], xlim[1], samples)
    for x in xs:
        lines.append(np.column_stack([np.full_like(t_v, x), t_v]))
    for y in ys:
        lines.append(np.column_stack([t_h, np.full_like(t_h, y)]))
    return lines


def draw_grid(ax, f=None, lines=None, color=BLUE, lw=1.2, alpha=0.9,
              xlim=(-2, 2), ylim=(-2, 2), spacing=0.5, zorder=3):
    """Draw the grid (or its image under map f) on ax."""
    if lines is None:
        lines = grid_polylines(xlim, ylim, spacing)
    for pts in lines:
        x, y = pts[:, 0], pts[:, 1]
        if f is not None:
            x, y = f(x, y)
        ax.plot(x, y, color=color, lw=lw, alpha=alpha,
                zorder=zorder, solid_capstyle="round")


def draw_unit_square(ax, f=None, corner=(0.0, 0.0), size=1.0, color=YELLOW,
                     alpha=0.45, samples=60, zorder=4):
    """Shade the image of a small square: the guide's 'patch of paint'."""
    cx, cy = corner
    s = np.linspace(0, size, samples)
    xx, yy = np.meshgrid(cx + s, cy + s)
    if f is not None:
        xx, yy = f(xx, yy)
    ax.pcolormesh(xx, yy, np.ones((samples - 1, samples - 1)),
                  color=color, alpha=alpha, shading="flat", zorder=zorder,
                  edgecolors="none")


# --- ready-made figures ----------------------------------------------------

def before_after(F, variables, xlim=(-2, 2), ylim=(-2, 2), spacing=0.5,
                 titles=("before", "after"), square=None, figsize=(9.6, 4.6),
                 out_lims=None):
    """Two panels: the blue grid, and its green image under F."""
    f = lambdify_map(F, variables)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=figsize)
    style_axes(axL, xlim, ylim)
    style_axes(axR, out_lims[0] if out_lims else xlim,
               out_lims[1] if out_lims else ylim)
    draw_grid(axL, None, xlim=xlim, ylim=ylim, spacing=spacing, color=BLUE)
    draw_grid(axR, f, xlim=xlim, ylim=ylim, spacing=spacing, color=GREEN)
    if square is not None:
        draw_unit_square(axL, None, corner=square)
        draw_unit_square(axR, f, corner=square)
    axL.set_title(titles[0], color=INK2, fontsize=12)
    axR.set_title(titles[1], color=INK2, fontsize=12)
    fig.tight_layout()
    return fig


def det_heatmap(F, variables, xlim=(-2, 2), ylim=(-2, 2), n=400,
                title=None, figsize=(6.4, 5.4), signed=True, vmax=None):
    """Heatmap of det JF over the plane (diverging: red < 0 < blue)."""
    from .core import jacobian_det
    d = jacobian_det(F, variables)
    dfun = sp.lambdify(variables, d, "numpy")
    xs = np.linspace(*xlim, n)
    ys = np.linspace(*ylim, n)
    xx, yy = np.meshgrid(xs, ys)
    zz = np.broadcast_to(np.asarray(dfun(xx, yy), float), xx.shape)
    fig, ax = plt.subplots(figsize=figsize)
    if signed:
        m = vmax or np.nanmax(np.abs(zz)) or 1
        im = ax.pcolormesh(xx, yy, zz, cmap=DIV_CMAP, vmin=-m, vmax=m,
                           shading="auto")
    else:
        im = ax.pcolormesh(xx, yy, zz, cmap=SEQ_CMAP, vmin=0,
                           vmax=vmax or np.nanmax(zz), shading="auto")
    style_axes(ax, xlim, ylim)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.outline.set_visible(False)
    cb.ax.tick_params(color=MUTED, labelcolor=INK2)
    if title:
        ax.set_title(title, color=INK2, fontsize=12)
    fig.tight_layout()
    return fig


# --- animation -------------------------------------------------------------

def _ease(t):
    return 3 * t**2 - 2 * t**3  # smoothstep


def animate_map(F, variables, out_path, xlim=(-2, 2), ylim=(-2, 2),
                spacing=0.5, frames=48, fps=20, figsize=(6.0, 6.0),
                view=None, square=None, points=None, title=None,
                hold_frames=8, color_from=BLUE, color_to=GREEN):
    """GIF: the grid morphs from itself to its image under F.

    Every point travels in a straight line p -> F(p) (positions are
    interpolated, colors fade blue -> green).  `points` is an optional list
    of (x, y) dots to track; `view` fixes the camera box.
    """
    f = lambdify_map(F, variables)
    lines = grid_polylines(xlim, ylim, spacing)
    starts = [(pts[:, 0], pts[:, 1]) for pts in lines]
    ends = [f(x, y) for x, y in starts]

    c0 = np.array(matplotlib.colors.to_rgb(color_from))
    c1 = np.array(matplotlib.colors.to_rgb(color_to))

    fig, ax = plt.subplots(figsize=figsize)
    view = view or (xlim, ylim)
    style_axes(ax, view[0], view[1])
    if title:
        ax.set_title(title, color=INK2, fontsize=12)

    artists = [ax.plot([], [], lw=1.2, color=color_from,
                       solid_capstyle="round", zorder=3)[0] for _ in lines]
    dot_artists = []
    dot_ends = []
    if points:
        for (px, py) in points:
            (qx,), (qy,) = f(np.array([px]), np.array([py]))
            dot_ends.append((px, py, qx, qy))
            dot_artists.append(ax.plot([px], [py], "o", ms=7, color=VIOLET,
                                       zorder=6)[0])
    sq_artist = None

    total = frames + 2 * hold_frames

    def update(i):
        t = _ease(min(max((i - hold_frames) / frames, 0.0), 1.0))
        c = matplotlib.colors.to_hex((1 - t) * c0 + t * c1)
        for art, (x0, y0), (x1, y1) in zip(artists, starts, ends):
            art.set_data((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)
            art.set_color(c)
        for art, (px, py, qx, qy) in zip(dot_artists, dot_ends):
            art.set_data([(1 - t) * px + t * qx], [(1 - t) * py + t * qy])
        nonlocal sq_artist
        if square is not None:
            if sq_artist is not None:
                sq_artist.remove()
            s = np.linspace(0, 1, 40)
            xx, yy = np.meshgrid(square[0] + s, square[1] + s)
            ex, ey = f(xx, yy)
            sq_artist = ax.pcolormesh((1 - t) * xx + t * ex,
                                      (1 - t) * yy + t * ey,
                                      np.ones((39, 39)), color=YELLOW,
                                      alpha=0.45, shading="flat", zorder=4)
        return artists

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(out_path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    return out_path


# --- saving ----------------------------------------------------------------

def save_fig(fig, path, dpi=150):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return path
