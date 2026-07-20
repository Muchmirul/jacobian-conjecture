# Research notes — Jacobian Conjecture content

Condensed from a web-research pass (2026-07-20) plus **independent symbolic
verification run in this repo** (see tests/). Verification tags:
[V-repo] = re-verified here with sympy exact arithmetic; [V-web] = verified
against cited sources; [STD] = standard textbook fact.

## The statement

**Keller 1939.** F = (F₁,…,Fₙ): ℂⁿ → ℂⁿ polynomial. If det JF is a nonzero
constant, then F is invertible and the inverse is polynomial. [V-web]

- Easy direction: if a polynomial inverse exists, chain rule ⇒ det JF · det JG = 1,
  two polynomials multiplying to 1 are nonzero constants. [STD]
- Over ℂ, "det JF constant ≠ 0" ⟺ "det JF vanishes nowhere": a polynomial with
  no zeros on ℂⁿ is a nonzero constant (weak Nullstellensatz; n = 1 case is the
  fundamental theorem of algebra). Over ℝ this equivalence FAILS (1 + x²). [STD]
- Injectivity is the whole game: injective polynomial ℂⁿ → ℂⁿ ⇒ surjective
  (Ax–Grothendieck, via finite-field counting) with automatically-polynomial
  inverse. [V-web]
- Char p counterexample: F(x) = x − xᵖ has F′ ≡ 1 but kills all of 𝔽ₚ
  (Fermat's little theorem). [V-repo: tests/test_core.py]

## History

- **Kraus 1884**: two-variable case claimed as a theorem; flawed control of
  ramification at infinity (Rodríguez Díaz, C. R. Math. 364 (2026) 363–370,
  arXiv:2512.23614). The same "infinity" difficulty is still the crux. [V-web]
- **Keller 1939** ("Ganze Cremona-Transformationen"), originally 2 variables /
  integer coefficients. Named + popularized by Abhyankar. [V-web]
- **False-proof graveyard**: Engel 1955, Segre (3×, 1956–60), Gröbner 1961,
  Oda 1980, many arXiv attempts (Drużkowski's survey, Banach Center Publ. 31). [V-web]
- **Smale's problem 16** (1998). [V-web]

## Known results

| Result | Who / when |
|---|---|
| n = 1 (trivial: F′ const ⇒ deg 1) | — |
| deg F ≤ 2, all n | Wang 1980 |
| Enough to prove deg 3 (cubic homogeneous F = X + H), all n | Bass–Connell–Wright 1982 |
| Enough: cubic-linear Fᵢ = xᵢ + (linear)³ | Drużkowski 1983 |
| Injective ⇒ surjective (ℂⁿ) | Ax–Grothendieck |
| n = 2 true up to deg 100 (→108 recently) | Moh 1983; arXiv:2204.14178 |
| Real version with det > 0 everywhere is FALSE | Pinchuk 1994, degrees (10, 25) |
| Dixmier ⟺ JC (stably): JC₂ₙ ⇒ DCₙ | Tsuchimoto 2005; Belov-Kanel–Kontsevich 2007 |
| Nagata automorphism is wild (n = 3) | Shestakov–Umirbaev 2004 |
| Every n = 2 automorphism is tame | Jung–van der Kulk |

## THE JULY 2026 COUNTEREXAMPLE (n ≥ 3)

Announced 2026-07-19/20 (attributed to Levent Alpöge, with the question posed
by "Akhil" and the example produced with the AI model Claude Fable; not yet
peer-reviewed, no arXiv paper at time of writing — treat the *narrative*
cautiously and the *math* confidently, because it re-verifies instantly):

With u = 1 + xy:

```
P = u³·z + y²·u·(4 + 3xy)
Q = y + 3x·u²·z + 3xy²·(4 + 3xy)
R = 2x − 3x²y − x³z
```

- det J(P,Q,R) ≡ **−2**. [V-repo]
- **Not injective**: F(0, 0, −1/4) = F(1, −3/2, 13/2) = F(−1, 3/2, 13/2)
  = (−1/4, 0, 0); also F(−4, 1/3, 0) = F(−2, 1/3, −2) = (0, 1/3, −24). [V-repo]
- Padding with identity coordinates ⇒ **false for every n ≥ 3**. [V-repo]
- **n = 2 (Keller's original) remains open.**
- Component degrees (7, 6, 4); non-properness / escape-to-infinity is the
  mechanism (fibers run off to infinity).

Coverage: Wikipedia (updated), jacobianfun.org/jacobian-explained (Gallagher),
zzhang-iu.github.io consequences note.

## Teaching examples (all [V-repo] in tests/)

- Shear (x, y + x²): det ≡ 1, inverse (x, y − x²).
- H = (x + (y+x²)², y + x²) (two shears composed): det ≡ 1, inverse
  (u − v², v − (u−v²)²). Messy-looking yet perfectly undoable.
- Fold (x², y): det = 2x, folds along the line where det = 0.
- Crush (x, xy): det = x, crushes the y-axis to a point; also the standard
  NON-PROPER example: (1/k, k) ↦ (1/k, 1).
- z² as real map (x²−y², 2xy): real det = 4(x²+y²) = |2z|² — zero only at the
  origin, yet the map is globally 2-to-1: ONE bad point is enough. General
  fact: holomorphic F as real map has real Jacobian det = |det_ℂ JF|²
  (n = 1 proof via Cauchy–Riemann: u_x v_y − u_y v_x = u_x² + v_x² = |f′|²). [STD]
- eᶻ as real map (eˣcos y, eˣsin y): det = e²ˣ > 0 everywhere, ∞-to-1 — shows
  the conjecture is really about POLYNOMIALS.
- Nagata (w = y² + xz): N = (x − 2yw − zw², y + zw, z), det ≡ 1, preserves w,
  explicit polynomial inverse; provably not a composition of elementary maps
  (wild). [V-repo for det/inverse]

## Why it resisted (and where the counterexample lives)

- Inverse function theorem is LOCAL; global injectivity can fail across distant
  points (z², exp, Pinchuk).
- Hadamard: local diffeo + proper ⇒ global diffeo. So any counterexample must
  be non-proper — all difficulty hides at infinity. The 2026 map exploits
  exactly this.
- Degree is a red herring: deg 2 is a theorem; deg 3 already fully general.

## Existing treatments (positioning)

- van den Essen, *Polynomial Automorphisms and the JC* (2000) + 2021 sequel — graduate.
- Garland, UChicago REU 2018 intro — undergraduate.
- Drużkowski survey — false-proof history.
- Tao's blog on Ax–Grothendieck; "Picturing Pinchuk's Plane Polynomial Pair"
  (arXiv:math/9812032) — visual real-case treatment.
- Post-counterexample: jacobianfun.org (assumes calculus+linear algebra).
- **Gap: nothing for a zero-math-background audience — this guide's niche.**
