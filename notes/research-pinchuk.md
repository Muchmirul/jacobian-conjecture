# Research notes — the explicit Pinchuk map

Source: L. A. Campbell, *Picturing Pinchuk's Plane Polynomial Pair*,
arXiv:math/9812032 (citing Pinchuk, Math. Z. 217 (1994) 1–4, and van den
Essen's June-1994 communication for the (10, 25) form). Everything below is
re-verified in this repo: `tests/test_pinchuk.py`.

## The map

```python
t = x*y - 1
h = t*(x*t + 1)
f = (x*t + 1)**2 * (t**2 + y)      # = ((h+1)/x)(xt+1)^2, polynomial since h+1 = x(t^2+y)
p = f + h                           # degree 10
q = (-t**2 - 6*t*h*(h+1) - 170*f*h - 91*h**2 - 195*f*h**2
     - 69*h**3 - 75*f*h**3 - Rational(75,4)*h**4)   # degree 25
```

(Only non-integer coefficient: −75/4. A PDF-extraction pitfall: the first term
of q is −t², not −t.)

## Positivity of det J

Exact identity (verified symbolically in tests):

```
det J(p, q) = t² + (t + f·(13 + 15h))² + f²
```

Vanishing would need t = 0 and f = 0; but on t = 0 (the hyperbola xy = 1),
f = y ≠ 0. So det J > 0 at every real point — yet the map is NOT injective.

## Non-injectivity

- Whole hyperbola collapses: (1/c, c) ↦ (c, 0) for every c ≠ 0.
- Witness pair (Campbell's fiber machinery): A = (−1/2, −2) ↦ (−2, 0) exactly;
  a second preimage B ≈ (−0.07116, −252.39) on the fiber parameterization
  x(h) = (c−h)(h+1)/(c−2h−h²)², y(h) = (c−2h−h²)²(c−h−h²)/(c−h)² at c = −2,
  q-root h* ≈ −3.508256 in the bracket (−29/8, −7/2). Verified numerically in
  tests (p exact on the fiber; |q| < 1e−3 at the bisection approximant).
- Campbell: image misses exactly two points, (0, 0) and (−1, −163/4); the map
  is generically 2-to-1 off the asymptotic variety.

## Teaching use (chapter 11)

Real plane + "det never 0" (even "det > 0 everywhere") is NOT enough for
global invertibility — the complex/constant hypothesis in the Jacobian
Conjecture is doing real work. Show the det heatmap (all positive), state the
witness pair, link Campbell's paper for the pictures.
