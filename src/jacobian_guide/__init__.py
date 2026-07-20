"""Tools behind the "Zero to the Jacobian Conjecture" guide.

core      symbolic math (sympy): Jacobians, determinants, inverses, composition
examples  the named example maps used throughout the guide
plotting  matplotlib helpers: warped grids, heatmaps, GIF animations
"""

from . import core, examples

__all__ = ["core", "examples"]
