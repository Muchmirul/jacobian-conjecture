"""Symbolic tools for polynomial maps and their Jacobians.

A "map" here is a tuple of sympy expressions, one per output coordinate,
together with a tuple of input symbols.  Example:

    x, y = sp.symbols("x y")
    F = (x, y + x**2)          # the basic shear used throughout the guide

Every claim the guide makes about an example map is checked by these
functions in tests/.
"""

from __future__ import annotations

from typing import Sequence

import sympy as sp

Map = tuple[sp.Expr, ...]


def _as_exprs(F: Sequence[sp.Expr]) -> Map:
    return tuple(sp.sympify(f) for f in F)


def jacobian_matrix(F: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> sp.Matrix:
    """The matrix of all partial derivatives of F."""
    return sp.Matrix([[sp.diff(f, v) for v in variables] for f in _as_exprs(F)])


def jacobian_det(F: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> sp.Expr:
    """The Jacobian determinant of F, expanded."""
    return sp.expand(jacobian_matrix(F, variables).det())


def is_keller(F: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> bool:
    """True if det JF is a nonzero constant (the Jacobian Conjecture hypothesis)."""
    d = jacobian_det(F, variables)
    return d.free_symbols.isdisjoint(set(variables)) and not d.is_zero


def compose(F: Sequence[sp.Expr], G: Sequence[sp.Expr],
            variables: Sequence[sp.Symbol]) -> Map:
    """The map F after G:  compose(F, G) sends p to F(G(p))."""
    F, G = _as_exprs(F), _as_exprs(G)
    subs = dict(zip(variables, G))
    return tuple(sp.expand(f.subs(subs, simultaneous=True)) for f in F)


def identity(variables: Sequence[sp.Symbol]) -> Map:
    return tuple(variables)


def is_identity(F: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> bool:
    return all(sp.expand(f - v) == 0 for f, v in zip(_as_exprs(F), variables))


def verify_inverse(F: Sequence[sp.Expr], G: Sequence[sp.Expr],
                   variables: Sequence[sp.Symbol]) -> bool:
    """True if G undoes F and F undoes G (both compositions are the identity)."""
    return (is_identity(compose(G, F, variables), variables)
            and is_identity(compose(F, G, variables), variables))


def invert(F: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> Map | None:
    """A polynomial inverse of F, or None if sympy cannot find one.

    Solves the system  u_i = F_i(x)  for the x's and keeps a solution whose
    every component is a polynomial in the u's, renamed back to the original
    variables.  The result is verified with verify_inverse before returning.
    """
    F = _as_exprs(F)
    us = sp.symbols(f"_u0:{len(variables)}")
    solutions = sp.solve([sp.Eq(u, f) for u, f in zip(us, F)],
                         list(variables), dict=True)
    for sol in solutions:
        if set(sol) != set(variables):
            continue
        candidate = []
        for v in variables:
            expr = sp.expand(sol[v])
            if not expr.free_symbols <= set(us):
                break
            if expr.as_poly(*us) is None:
                break
            candidate.append(expr.subs(dict(zip(us, variables)), simultaneous=True))
        else:
            G = tuple(sp.expand(g) for g in candidate)
            if verify_inverse(F, G, variables):
                return G
    return None


def degree(F: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> int:
    """The degree of the map: the largest total degree among its components."""
    return max(sp.Poly(f, *variables).total_degree() for f in _as_exprs(F))


# ---------------------------------------------------------------------------
# Constructors for the elementary ("shear") maps the guide leans on.
# ---------------------------------------------------------------------------

def shear_up(p: sp.Expr, variables: Sequence[sp.Symbol]) -> Map:
    """(x, y) -> (x, y + p(x)): slide each vertical line up by p(x)."""
    x, y = variables
    return (x, y + sp.sympify(p))


def shear_right(p: sp.Expr, variables: Sequence[sp.Symbol]) -> Map:
    """(x, y) -> (x + p(y), y): slide each horizontal line right by p(y)."""
    x, y = variables
    return (x + sp.sympify(p), y)


def linear_map(a, b, c, d, variables: Sequence[sp.Symbol]) -> Map:
    """(x, y) -> (a x + b y, c x + d y)."""
    x, y = variables
    return (a * x + b * y, c * x + d * y)


# ---------------------------------------------------------------------------
# Bridging complex 1-variable maps and real plane maps (used in chapter 11).
# ---------------------------------------------------------------------------

def complex_poly_as_real_map(fz: sp.Expr, z: sp.Symbol,
                             variables: Sequence[sp.Symbol]) -> Map:
    """View a complex polynomial f(z) as a map of the real plane.

    Substitutes z = x + i y and returns (Re f, Im f).  For example z**2
    becomes (x**2 - y**2, 2 x y).
    """
    x, y = variables
    w = sp.expand(fz.subs(z, x + sp.I * y))
    return (sp.expand(sp.re(w)), sp.expand(sp.im(w)))
