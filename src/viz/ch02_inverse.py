"""Figures for chapter 2, undo: inverse machines (all animated)."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from common import animate_1d, arrow, bare_axes, number_line, out_dir
from jacobian_guide.plotting import (BLUE, GREEN, INK2, MUTED, RED, VIOLET)

OUT = out_dir("02-the-undo-machine")


def undo_gif():
    animate_1d(lambda x: 2 * x, xs=[-3, -2, -1, 0, 1, 2, 3],
               out_path=OUT / "undo.gif", roundtrip=True,
               title="'double' sends numbers down, then 'halve' carries every one back home")


def collision_gif(fps=16, travel=24, settle=12, hold=20):
    """Left: «square it», the dots −3 and 3 ride their arrows onto the SAME
    output 9: a crash, no way back.  Right: «double it», every arrow keeps
    its own landing spot, so each one can be traced backwards."""
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.7))
    xlim = (-9.5, 10.5)

    axL, axR = axes
    bare_axes(axL, (-10.5, 11.5), (-0.8, 1.75))
    number_line(axL, 1.0, xlim, [-9, -6, -3, 0, 3, 6, 9], label="in")
    number_line(axL, 0.0, xlim, [0, 3, 6, 9], label="out")
    for x in (-3, 3):
        arrow(axL, (x, 0.93), (9, 0.07), color=BLUE, lw=1.4,
              curve=0.12 if x < 0 else -0.12)
    axL.text(-5.5, 0.22, "…and nothing ever lands over here",
             ha="center", fontsize=9.5, color=MUTED, style="italic")
    axL.set_title("'square it' cannot be undone", color=INK2, fontsize=12)
    crashL = axL.text(9, -0.5, "crash!  −3 and 3 both land on 9",
                      ha="center", fontsize=10.5, color=RED, alpha=0.0)
    crash_dot, = axL.plot([], [], "o", ms=10, color=RED, zorder=7)
    dotsL = [axL.plot([x], [1.0], "o", ms=8, color=BLUE, zorder=6)[0]
             for x in (-3, 3)]

    bare_axes(axR, (-10.5, 11.5), (-0.8, 1.75))
    number_line(axR, 1.0, xlim, [-9, -6, -3, 0, 3, 6, 9], label="in")
    number_line(axR, 0.0, xlim, [-9, -6, -3, 0, 3, 6, 9], label="out")
    RX = (-4, -2, 0, 2, 4)
    for x in RX:
        arrow(axR, (x, 0.93), (2 * x, 0.07), color=BLUE, lw=1.2)
    axR.set_title("'double it' can be undone", color=INK2, fontsize=12)
    okR = axR.text(0.5, -0.5, "no two arrows ever meet → trace each one back",
                   ha="center", fontsize=10.5, color=MUTED, alpha=0.0)
    dotsR = [axR.plot([x], [1.0], "o", ms=7, color=BLUE, zorder=6)[0]
             for x in RX]
    landR = [axR.plot([], [], "o", ms=7, color=GREEN, zorder=5)[0]
             for _ in RX]

    fig.tight_layout()

    def ease(t):
        return 3 * t**2 - 2 * t**3

    stage = travel + settle
    total = 2 * stage + hold

    def update(i):
        # stage 0: the squaring dots crash
        tL = ease(min(min(i, stage - settle) / travel, 1.0))
        for dot, x in zip(dotsL, (-3, 3)):
            bow = 1.1 if x < 0 else -1.1
            dot.set_data([(1 - tL) * x + tL * 9 + bow * np.sin(np.pi * tL)],
                         [(1 - tL) * 1.0 + tL * 0.0])
        if tL >= 1.0:
            crash_dot.set_data([9], [0.0])
            crashL.set_alpha(1.0)
        # stage 1: the doubling dots stay separate
        j = i - stage
        tR = ease(min(max(j, 0) / travel, 1.0))
        for dot, land, x in zip(dotsR, landR, RX):
            dot.set_data([(1 - tR) * x + tR * 2 * x],
                         [(1 - tR) * 1.0 + tR * 0.0])
            if tR >= 1.0:
                land.set_data([2 * x], [0.0])
        if tR >= 1.0:
            okR.set_alpha(1.0)
        return [*dotsL, *dotsR, crash_dot, crashL, okR, *landR]

    anim = FuncAnimation(fig, update, frames=total, interval=1000 / fps)
    anim.save(OUT / "collision.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)


if __name__ == "__main__":
    undo_gif()
    collision_gif()
    print(f"wrote figures to {OUT}")
