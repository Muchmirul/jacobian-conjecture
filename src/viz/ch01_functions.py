"""Figures for chapter 1, functions are machines (all animated)."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import animate_1d, arrow, bare_axes, draw_machine, out_dir
from jacobian_guide.plotting import BLUE, GREEN, INK2, MUTED

OUT = out_dir("01-functions-are-machines")

EXAMPLES = [(3, 7), (0, 1), (10, 21)]          # x  ->  2x + 1


def machine_gif(fps=16, t_in=16, t_work=8, t_out=16, t_rest=10, hold=20):
    """One number at a time rides through the machine «double it, then add 1»:
    blue in on the left, green out on the right, and a growing scoreboard , 
    the same input always produces the same output."""
    fig, ax = plt.subplots(figsize=(7.6, 3.1))
    bare_axes(ax, (0, 10), (0, 3.1))
    draw_machine(ax, (3.4, 0.9), (3.2, 1.2), "double it,\nthen add 1")
    arrow(ax, (1.6, 1.5), (3.25, 1.5))
    arrow(ax, (6.85, 1.5), (8.5, 1.5), color=GREEN)
    ax.text(1.1, 0.85, "in", fontsize=10, ha="center", color=MUTED)
    ax.text(9.0, 0.85, "out", fontsize=10, ha="center", color=MUTED)
    ax.text(5.0, 0.32, "same input in, same output out, every single time",
            fontsize=10.5, ha="center", color=MUTED, style="italic")
    ax.set_title("a function is a reliable machine", color=INK2, fontsize=12)

    mover = ax.text(0, 1.5, "", fontsize=21, ha="center", va="center",
                    color=BLUE, zorder=6)
    history = [ax.text(1.7, 2.78 - 0.34 * k, f"{x:>2}  →  {y}", fontsize=10,
                       ha="center", color=INK2, family="monospace", alpha=0.0)
               for k, (x, y) in enumerate(EXAMPLES)]

    def ease(t):
        return 3 * t**2 - 2 * t**3

    per = t_in + t_work + t_out + t_rest
    total = len(EXAMPLES) * per + hold

    def update(i):
        k, j = divmod(min(i, len(EXAMPLES) * per - 1), per)
        x_in, x_out = EXAMPLES[k]
        for h, art in enumerate(history):
            done = h < k or (h == k and j >= t_in + t_work + t_out)
            art.set_alpha(1.0 if done else 0.0)
        if j < t_in:                                   # ride in, blue
            t = ease(j / t_in)
            mover.set_text(str(x_in))
            mover.set_color(BLUE)
            mover.set_position((1.1 + t * (4.9 - 1.1), 1.5))
            mover.set_alpha(1.0 if t < 0.85 else (1 - t) / 0.15)
        elif j < t_in + t_work:                        # machine is working
            mover.set_alpha(0.0)
        elif j < t_in + t_work + t_out:                # ride out, green
            t = ease((j - t_in - t_work) / t_out)
            mover.set_text(str(x_out))
            mover.set_color(GREEN)
            mover.set_position((5.1 + t * (9.0 - 5.1), 1.5))
            mover.set_alpha(t / 0.15 if t < 0.15 else 1.0)
        else:                                          # rest, keep the output
            mover.set_alpha(1.0)
        return [mover, *history]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "machine.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


def numberline_gif():
    animate_1d(lambda x: 2 * x + 1, xs=[-3, -2, -1, 0, 1, 2, 3],
               out_path=OUT / "numberline.gif",
               title="the machine 'double, then add 1' moves every number at once")


if __name__ == "__main__":
    machine_gif()
    numberline_gif()
    print(f"wrote figures to {OUT}")
