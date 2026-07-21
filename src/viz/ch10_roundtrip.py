"""Figure for chapter 10 — the round trip: apply F, then its inverse G."""

import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import out_dir
from jacobian_guide.examples import TANGLED, VARS
from jacobian_guide.plotting import (BLUE, GREEN, INK2, grid_polylines,
                                     lambdify_map, style_axes)

OUT = out_dir("10-kicking-the-tires")

F = lambdify_map(TANGLED, VARS)


def roundtrip_gif(frames=40, fps=18, hold=12):
    lines = grid_polylines((-1, 1), (-1, 1), spacing=0.2)
    starts = [(pts[:, 0], pts[:, 1]) for pts in lines]
    ends = [F(x, y) for x, y in starts]

    c0 = np.array(matplotlib.colors.to_rgb(BLUE))
    c1 = np.array(matplotlib.colors.to_rgb(GREEN))

    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    fig.subplots_adjust(top=0.84)
    style_axes(ax, (-1.7, 5.3), (-1.7, 2.4))
    artists = [ax.plot([], [], lw=1.2, solid_capstyle="round", zorder=3)[0]
               for _ in lines]

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
        titles = ("step 1 · the monster map  $H(x,y) = (x+(y+x^2)^2,\\; y+x^2)$\n"
                  "tangles the blue grid into the green one",
                  "step 2 · its polynomial undo  $G(x,y) = (x-y^2,\\; y-(x-y^2)^2)$\n"
                  "walks every point exactly back home")
        ax.set_title(titles[stage], color=INK2, fontsize=11.5)
        c = matplotlib.colors.to_hex((1 - u) * c0 + u * c1)
        for art, (x0, y0), (x1, y1) in zip(artists, starts, ends):
            art.set_data((1 - u) * x0 + u * x1, (1 - u) * y0 + u * y1)
            art.set_color(c)
        return artists

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "roundtrip.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    roundtrip_gif()
    print(f"wrote figures to {OUT}")
