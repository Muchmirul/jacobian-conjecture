"""Independent verification of the July 2026 counterexample (chapter 12)
and of the Nagata automorphism facts (chapter 11)."""

import sympy as sp

from jacobian_guide.core import (
    degree,
    is_keller,
    jacobian_det,
    verify_inverse,
)
from jacobian_guide.examples import (
    COLLISION_2026,
    COUNTEREXAMPLE_2026,
    NAGATA,
    NAGATA_INV,
    VARS3,
    X3,
    Y3,
    Z3,
)


def image(F, pt):
    return tuple(sp.expand(f.subs(dict(zip(VARS3, pt)))) for f in F)


# --- the counterexample ----------------------------------------------------

def test_counterexample_satisfies_keller_hypothesis():
    assert jacobian_det(COUNTEREXAMPLE_2026, VARS3) == -2
    assert is_keller(COUNTEREXAMPLE_2026, VARS3)


def test_counterexample_is_not_injective():
    images = [image(COUNTEREXAMPLE_2026, p) for p in COLLISION_2026]
    assert len(set(COLLISION_2026)) == 3          # three genuinely different inputs
    assert images[0] == images[1] == images[2]    # one shared output
    assert images[0] == (sp.Rational(-1, 4), 0, 0)


def test_second_collision_pair():
    a = image(COUNTEREXAMPLE_2026, (-4, sp.Rational(1, 3), 0))
    b = image(COUNTEREXAMPLE_2026, (-2, sp.Rational(1, 3), -2))
    assert a == b == (0, sp.Rational(1, 3), -24)


def test_padding_breaks_conjecture_in_all_higher_dimensions():
    w = sp.Symbol("w")
    F4 = (*COUNTEREXAMPLE_2026, w)
    assert jacobian_det(F4, (*VARS3, w)) == -2


def test_component_degrees():
    assert [sp.Poly(f, *VARS3).total_degree()
            for f in COUNTEREXAMPLE_2026] == [7, 6, 4]


# --- the Nagata automorphism ----------------------------------------------

def test_nagata_is_keller_map_of_degree_five():
    assert jacobian_det(NAGATA, VARS3) == 1
    assert degree(NAGATA, VARS3) == 5


def test_nagata_preserves_w_and_has_polynomial_inverse():
    w = Y3**2 + X3 * Z3
    w_after = sp.expand(w.subs(dict(zip(VARS3, NAGATA)), simultaneous=True))
    assert sp.expand(w_after - w) == 0
    assert verify_inverse(NAGATA, NAGATA_INV, VARS3)
