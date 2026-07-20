"""Every mathematical claim the guide makes about its examples, as a test."""

import sympy as sp

from jacobian_guide.core import (
    compose,
    degree,
    invert,
    is_keller,
    jacobian_det,
    jacobian_matrix,
    linear_map,
    verify_inverse,
)
from jacobian_guide.examples import (
    CRUSH,
    FOLD,
    SHEAR_UP,
    SHEAR_UP_INV,
    SHEAR_RIGHT,
    TANGLED,
    TANGLED3,
    VARS,
    X,
    Y,
    Z_SQUARED,
    char_p_demo,
)


# --- Jacobians of the named examples (chapter 7) ---------------------------

def test_shear_jacobian_matrix():
    assert jacobian_matrix(SHEAR_UP, VARS) == sp.Matrix([[1, 0], [2 * X, 1]])


def test_hero_maps_have_constant_det_one():
    for F in (SHEAR_UP, SHEAR_RIGHT, TANGLED, TANGLED3):
        assert jacobian_det(F, VARS) == 1
        assert is_keller(F, VARS)


def test_villain_maps_have_vanishing_det_somewhere():
    assert jacobian_det(FOLD, VARS) == 2 * X
    assert jacobian_det(CRUSH, VARS) == X
    assert not is_keller(FOLD, VARS)
    assert not is_keller(CRUSH, VARS)


def test_linear_map_det_is_ad_minus_bc():
    a, b, c, d = sp.symbols("a b c d")
    assert sp.simplify(jacobian_det(linear_map(a, b, c, d, VARS), VARS)
                       - (a * d - b * c)) == 0


# --- Invertibility claims (chapters 2, 6, 10) ------------------------------

def test_shear_inverse_is_the_known_one():
    assert invert(SHEAR_UP, VARS) == SHEAR_UP_INV
    assert verify_inverse(SHEAR_UP, SHEAR_UP_INV, VARS)


def test_tangled_has_polynomial_inverse():
    G = invert(TANGLED, VARS)
    assert G is not None
    assert verify_inverse(TANGLED, G, VARS)
    # undo shears in reverse order: first unshear right, then unshear up
    expected = compose(SHEAR_UP_INV, (X - Y**2, Y), VARS)
    assert tuple(sp.expand(g - e) for g, e in zip(G, expected)) == (0, 0)


def test_tangled3_has_polynomial_inverse_same_degree():
    # In the plane the inverse of a polynomial automorphism has the SAME
    # degree as the map (in dimension >= 3 it can blow up to deg^(n-1)).
    G = invert(TANGLED3, VARS)
    assert G is not None
    assert verify_inverse(TANGLED3, G, VARS)
    assert degree(TANGLED3, VARS) == 4
    assert degree(G, VARS) == 4


def test_fold_is_not_injective_hence_no_inverse():
    assert invert(FOLD, VARS) is None
    p, q = (sp.Integer(2), sp.Integer(3)), (sp.Integer(-2), sp.Integer(3))
    image = lambda F, pt: tuple(f.subs({X: pt[0], Y: pt[1]}) for f in F)
    assert image(FOLD, p) == image(FOLD, q)  # two inputs collide


# --- The z^2 story (chapters 8 and 11) -------------------------------------

def test_z_squared_real_form_and_det():
    assert Z_SQUARED == (X**2 - Y**2, 2 * X * Y)
    # det = 4(x^2+y^2) = |2z|^2: zero only at the origin
    assert sp.expand(jacobian_det(Z_SQUARED, VARS) - 4 * (X**2 + Y**2)) == 0


def test_z_squared_is_two_to_one_away_from_origin():
    image = lambda pt: tuple(f.subs({X: pt[0], Y: pt[1]}) for f in Z_SQUARED)
    assert image((1, 1)) == image((-1, -1))


# --- Characteristic p cautionary tale (chapter 11) -------------------------

def test_char_p_map_sends_everything_to_zero():
    for p in (2, 3, 5, 7):
        assert char_p_demo(p) == [0] * p


# --- Composition sanity ----------------------------------------------------

def test_compose_order_convention():
    # compose(F, G) applies G first
    F, G = (X + 1, Y), (2 * X, Y)
    assert compose(F, G, VARS) == (2 * X + 1, Y)
    assert compose(G, F, VARS) == (2 * X + 2, Y)
