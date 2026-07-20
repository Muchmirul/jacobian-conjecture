"""The named example maps used throughout the guide.

Import X, Y and use the maps as sympy expression tuples, e.g.

    from jacobian_guide.examples import X, Y, SHEAR_UP, TANGLED
"""

from __future__ import annotations

import sympy as sp

from .core import compose, complex_poly_as_real_map

X, Y = sp.symbols("x y", real=True)
VARS = (X, Y)

# --- Heroes: polynomial maps with constant nonzero Jacobian determinant -----

#: The basic shear: slide each vertical line up by x^2.  det J = 1.
SHEAR_UP = (X, Y + X**2)

#: Its undo map.
SHEAR_UP_INV = (X, Y - X**2)

#: The sideways shear: slide each horizontal line right by y^2.  det J = 1.
SHEAR_RIGHT = (X + Y**2, Y)

#: Two shears composed: looks wild, still perfectly undoable.  det J = 1.
#: TANGLED(p) = SHEAR_RIGHT(SHEAR_UP(p)) = (x + (y + x^2)^2, y + x^2), degree 4.
TANGLED = compose(SHEAR_RIGHT, SHEAR_UP, VARS)

#: Three layers: a linear squeeze between the shears.  det J = 1.
TANGLED3 = compose(SHEAR_UP, compose((X + 2 * Y, Y), SHEAR_RIGHT, VARS), VARS)

# --- Villains: polynomial maps that crush or fold somewhere -----------------

#: Folds the plane onto the right half plane.  det J = 2x: zero on the y-axis.
FOLD = (X**2, Y)

#: Crushes the whole y-axis to one point.  det J = x: zero on the y-axis.
CRUSH = (X, X * Y)

# --- The cautionary tale: locally fine almost everywhere, globally 2-to-1 ---

#: z^2 viewed as a real plane map: (x^2 - y^2, 2xy).  det J = 4(x^2 + y^2):
#: zero ONLY at the origin — and that lone bad point is enough to let the
#: map wrap the plane around twice.
Z_SQUARED = complex_poly_as_real_map(sp.Symbol("z") ** 2, sp.Symbol("z"), VARS)


# --- Pinchuk's map: the real Jacobian conjecture is false -------------------

_t = X * Y - 1
_h = _t * (X * _t + 1)
_f = (X * _t + 1) ** 2 * (_t**2 + Y)

#: Pinchuk (1994): det J > 0 at EVERY point of the real plane, yet the map is
#: not injective.  Degrees (10, 25).  Source: Campbell, "Picturing Pinchuk's
#: Plane Polynomial Pair" (arXiv:math/9812032).
PINCHUK = (
    sp.expand(_f + _h),
    sp.expand(-_t**2 - 6 * _t * _h * (_h + 1) - 170 * _f * _h - 91 * _h**2
              - 195 * _f * _h**2 - 69 * _h**3 - 75 * _f * _h**3
              - sp.Rational(75, 4) * _h**4),
)

#: det J PINCHUK equals this sum of squares (so it can never be negative,
#: and a short argument shows it can never be zero either).
PINCHUK_DET_IDENTITY = sp.expand(
    _t**2 + (_t + _f * (13 + 15 * _h)) ** 2 + _f**2)


# --- Three variables: the July 2026 counterexample and the Nagata map -------

X3, Y3, Z3 = sp.symbols("x y z", real=True)
VARS3 = (X3, Y3, Z3)

_u = 1 + X3 * Y3

#: The map that DISPROVED the Jacobian Conjecture for n >= 3 (announced
#: 2026-07-19/20, attributed to Levent Alpöge, found with the AI model Claude
#: Fable; peer review pending — but the certificates below re-verify in
#: milliseconds, see tests/test_counterexample.py).
#: det J = -2 (constant!), yet three different points share one image.
COUNTEREXAMPLE_2026 = (
    _u**3 * Z3 + Y3**2 * _u * (4 + 3 * X3 * Y3),
    Y3 + 3 * X3 * _u**2 * Z3 + 3 * X3 * Y3**2 * (4 + 3 * X3 * Y3),
    2 * X3 - 3 * X3**2 * Y3 - X3**3 * Z3,
)

#: Three distinct inputs with the SAME output under COUNTEREXAMPLE_2026.
COLLISION_2026 = (
    (0, 0, sp.Rational(-1, 4)),
    (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
    (-1, sp.Rational(3, 2), sp.Rational(13, 2)),
)

_w = Y3**2 + X3 * Z3

#: Nagata's automorphism (1972): det J = 1, has a polynomial inverse, yet is
#: provably NOT a composition of linear maps and shears (Shestakov–Umirbaev
#: 2004).  It preserves w = y^2 + xz, which is the key to inverting it.
NAGATA = (X3 - 2 * Y3 * _w - Z3 * _w**2, Y3 + Z3 * _w, Z3)

#: Its inverse: subtract back using the preserved quantity w.
NAGATA_INV = (X3 + 2 * Y3 * _w - Z3 * _w**2, Y3 - Z3 * _w, Z3)


def char_p_demo(p: int) -> list[int]:
    """F(x) = x - x^p evaluated on all of F_p (returns all zeros: not injective).

    Shows why the Jacobian Conjecture needs characteristic 0: this F has
    F'(x) = 1 - p x^(p-1) = 1 (a nonzero constant) in F_p, yet by Fermat's
    little theorem x^p = x, so F sends EVERY element to 0.
    """
    return [(x - x**p) % p for x in range(p)]
