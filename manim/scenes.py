"""Flagship animations of the guide, as Manim Community Edition scenes.

These are OPTIONAL, fancier renders of the same stories told by the
committed matplotlib GIFs (see manim/README.md for install notes; every
committed image in guide/ was produced WITHOUT manim, so nothing in the
guide depends on this file).

Render examples:

    manim -qm --format=gif scenes.py TangledWarp
    manim -qh scenes.py FoldCollision

Scenes use Text (Pango) only — no LaTeX installation required.
"""

import numpy as np
from manim import (DOWN, ORANGE, PURPLE, RED, UP, Create, Dot, FadeIn,
                   NumberPlane, Scene, Text)


def _plane(x_range=(-4, 4), y_range=(-3, 3)):
    plane = NumberPlane(
        x_range=[x_range[0], x_range[1], 1],
        y_range=[y_range[0], y_range[1], 1],
        background_line_style={"stroke_opacity": 0.6},
    )
    plane.prepare_for_nonlinear_transform()
    return plane


class ShearBend(Scene):
    """Chapter 6: (x, y) -> (x + y^2/2, y) bends rows but preserves area."""

    def construct(self):
        title = Text("slide each row right by y²/2", font_size=28).to_edge(UP)
        plane = _plane()
        self.play(Create(plane), FadeIn(title))
        self.wait(0.5)
        self.play(
            plane.animate.apply_function(
                lambda p: np.array([p[0] + 0.5 * p[1] ** 2, p[1], 0.0])),
            run_time=3,
        )
        self.wait()


class TangledWarp(Scene):
    """Chapters 0/6: two stacked shears make a monster that is secretly tame."""

    def construct(self):
        plane = _plane((-2, 2), (-2, 2))
        self.play(Create(plane))
        self.wait(0.5)
        self.play(
            plane.animate.apply_function(
                lambda p: np.array([p[0], p[1] + 0.5 * p[0] ** 2, 0.0])),
            run_time=2,
        )
        self.play(
            plane.animate.apply_function(
                lambda p: np.array([p[0] + 0.5 * p[1] ** 2, p[1], 0.0])),
            run_time=2,
        )
        self.wait(0.5)
        # peel the layers in reverse: the undo is just as polynomial
        self.play(
            plane.animate.apply_function(
                lambda p: np.array([p[0] - 0.5 * p[1] ** 2, p[1], 0.0])),
            run_time=2,
        )
        self.play(
            plane.animate.apply_function(
                lambda p: np.array([p[0], p[1] - 0.5 * p[0] ** 2, 0.0])),
            run_time=2,
        )
        self.wait()


class FoldCollision(Scene):
    """Chapter 6: (x, y) -> (x^2/2, y) folds the plane; two dots collide."""

    def construct(self):
        plane = _plane((-3, 3), (-3, 3))
        f = lambda p: np.array([0.5 * p[0] ** 2, p[1], 0.0])
        d1 = Dot(np.array([-2.0, 1.0, 0.0]), color=PURPLE, radius=0.09)
        d2 = Dot(np.array([2.0, 1.0, 0.0]), color=ORANGE, radius=0.09)
        self.play(Create(plane), FadeIn(d1), FadeIn(d2))
        self.wait(0.5)
        self.play(
            plane.animate.apply_function(f),
            d1.animate.move_to(f(d1.get_center())),
            d2.animate.move_to(f(d2.get_center())),
            run_time=3,
        )
        crash = Text("crash — undo impossible", font_size=26, color=RED)
        crash.next_to(d1, DOWN)
        self.play(FadeIn(crash))
        self.wait()


class SquashDeterminant(Scene):
    """Chapter 5: determinant -> 0 flattens the plane onto a line."""

    def construct(self):
        plane = _plane((-3, 3), (-3, 3))
        self.play(Create(plane))
        self.wait(0.5)
        self.play(
            plane.animate.apply_function(
                lambda p: np.array([0.5 * (p[0] + p[1]),
                                    0.5 * (p[0] + p[1]), 0.0])),
            run_time=3,
        )
        label = Text("area factor 0: information destroyed", font_size=26,
                     color=RED).to_edge(DOWN)
        self.play(FadeIn(label))
        self.wait()
