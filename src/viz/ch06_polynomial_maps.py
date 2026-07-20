"""Figures for chapter 6 — polynomial maps bend the grid (but heroes never crush it)."""

from common import out_dir
from jacobian_guide.examples import CRUSH, FOLD, SHEAR_RIGHT, TANGLED, VARS
from jacobian_guide.plotting import (animate_map, before_after, save_fig)

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


def tangled_png():
    fig = before_after(TANGLED, VARS, xlim=(-1, 1), ylim=(-1, 1), spacing=0.2,
                       titles=("before", "after two stacked shears"),
                       out_lims=((-1.6, 5.2), (-1.7, 2.3)),
                       figsize=(10.6, 4.2))
    save_fig(fig, OUT / "tangled.png")


def crush_png():
    fig = before_after(CRUSH, VARS, xlim=(-2, 2), ylim=(-2, 2), spacing=0.4,
                       titles=("before", "(x, x·y): the whole middle line lands on one point"),
                       figsize=(9.6, 4.6))
    save_fig(fig, OUT / "crush.png")


if __name__ == "__main__":
    shear_gif()
    fold_gif()
    tangled_png()
    crush_png()
    print(f"wrote figures to {OUT}")
