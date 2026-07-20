"""Verification of the Pinchuk map facts used in chapter 11."""

import sympy as sp

from jacobian_guide.core import jacobian_det
from jacobian_guide.examples import (PINCHUK, PINCHUK_DET_IDENTITY, VARS, X, Y)


def test_pinchuk_degrees_are_10_and_25():
    assert sp.Poly(PINCHUK[0], X, Y).total_degree() == 10
    assert sp.Poly(PINCHUK[1], X, Y).total_degree() == 25


def test_pinchuk_det_is_a_sum_of_three_squares():
    det = jacobian_det(PINCHUK, VARS)
    assert sp.expand(det - PINCHUK_DET_IDENTITY) == 0


def test_pinchuk_det_never_vanishes_on_the_reals():
    # The sum of squares t^2 + (t + f(13+15h))^2 + f^2 vanishes only if
    # t = 0 AND f = 0.  On the curve t = xy - 1 = 0 we have f = y != 0
    # (y = 0 would force t = -1).  So det J > 0 everywhere on R^2.
    t = X * Y - 1
    f = (X * t + 1) ** 2 * (t**2 + Y)
    y0 = sp.Symbol("y0", nonzero=True)
    f_on_curve = sp.simplify(f.subs(X, 1 / y0).subs(Y, y0))
    assert f_on_curve == y0


def test_pinchuk_hyperbola_maps_to_axis():
    # (1/c, c) -> (c, 0): the whole hyperbola xy = 1 lands on the x-axis,
    # one hint that this map treats infinity strangely.
    c = sp.Symbol("c", nonzero=True)
    p = sp.simplify(PINCHUK[0].subs({X: 1 / c, Y: c}))
    q = sp.simplify(PINCHUK[1].subs({X: 1 / c, Y: c}))
    assert p == c and q == 0


def test_pinchuk_is_not_injective_numeric_witness():
    # A = (-1/2, -2) maps exactly to (-2, 0).  A second preimage of (-2, 0)
    # exists on the fiber parameterization from arXiv:math/9812032; we locate
    # it numerically and check it is far from A yet lands on the same image.
    h = sp.Symbol("h", real=True)
    c = -2
    xh = (c - h) * (h + 1) / (c - 2 * h - h**2) ** 2
    yh = (c - 2 * h - h**2) ** 2 * (c - h - h**2) / (c - h) ** 2
    # p is identically c along the fiber:
    p_on_fiber = sp.cancel(PINCHUK[0].subs({X: xh, Y: yh}) - c)
    assert p_on_fiber == 0
    # find h* with q = 0 in the certified bracket (-29/8, -7/2):
    q_on_fiber = sp.cancel(PINCHUK[1].subs({X: xh, Y: yh}))
    h_star = sp.nsolve(q_on_fiber, h, (sp.Rational(-29, 8), sp.Rational(-7, 2)),
                       solver="bisect", prec=40)
    B = (float(xh.subs(h, h_star)), float(yh.subs(h, h_star)))
    A = (-0.5, -2.0)
    assert abs(B[0] - A[0]) + abs(B[1] - A[1]) > 100     # genuinely different point
    q_at_B = float(PINCHUK[1].subs({X: sp.Float(B[0], 30), Y: sp.Float(B[1], 30)}))
    p_at_B = float(PINCHUK[0].subs({X: sp.Float(B[0], 30), Y: sp.Float(B[1], 30)}))
    assert abs(p_at_B - c) < 1e-6 and abs(q_at_B) < 1e-3
