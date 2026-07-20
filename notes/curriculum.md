# Curriculum design — "Zero to the Jacobian Conjecture"

**Goal.** A reader with no math background reads short chapters, looks at pictures and
animations, and ends up genuinely understanding what the Jacobian Conjecture says —
and why it is surprising that nobody can prove it.

**Design principles** (to be refined by research notes in this folder):

1. **Picture first, words second, symbols last.** Every concept gets a visual before
   it gets a name, and a name before it gets a formula.
2. **One idea per chapter.** Each chapter is readable in ~5 minutes and ends with a
   single boxed take-away sentence.
3. **Simple sentences.** Short sentences. Everyday words. Jargon only after the idea
   already exists in the reader's head, introduced in **bold**.
4. **Everything is runnable.** Every figure/animation in the guide is produced by a
   script in this repo. Readers can tweak numbers and re-render.
5. **Honest math.** No lies-to-children that must be unlearned later. Simplify by
   omission, never by falsehood.

## The learning journey (chapter map)

| # | Chapter | The one idea | Flagship visual |
|---|---------|--------------|-----------------|
| 0 | Start here | A 1939 puzzle nobody has solved — and you can understand it | "scrambled grid" hero image + roadmap |
| 1 | Functions are machines | A function turns each input into exactly one output | number-line mapping animation |
| 2 | Undo: inverse machines | Invertible = no two inputs collide + every output reachable | arrow collision diagram (squaring loses the sign) |
| 3 | Polynomials | Machines built only from + and × ; tame and predictable | graph gallery |
| 4 | Maps of the plane | A 2D map moves every point of the plane at once | before/after warped grids (shift, rotate, shear) |
| 5 | Straight maps and the determinant | det = area-scaling factor; det 0 = squashed = information lost | unit square → parallelogram animation, det counter |
| 6 | Polynomial maps bend the grid | Polynomial plane-maps; some bend but never crush | shear (x, y+x²) bending animation; fold (x², y) non-example |
| 7 | Zoom in: the Jacobian | Up close every smooth map looks straight; Jacobian = the local straight map, det J = local area factor | zoom-in animation; det-J heatmaps |
| 8 | Local vs global | Locally undoable everywhere ≠ globally undoable | angle-doubling wrap-around animation |
| 9 | The conjecture | Keller 1939: constant nonzero det J ⇒ polynomial inverse? | statement card assembled from prior chapters |
| 10 | Kicking the tires | Verify it on real examples with the computer (sympy) | F then F⁻¹ round-trip animation; degree table |
| 11 | Why it was so hard | Pinchuk (real fails), char p fails, 87 years of attempts, known partial results | results timeline; Pinchuk det>0 heatmap |
| 12 | July 2026: the conjecture falls (in 3D) | An explicit 3-variable map with det ≡ −2 that is not injective; n = 2 still open | collision certificate the reader can check by hand + sympy |

Ends with "where to go next" pointers (van den Essen's book, surveys).

**Timeliness note (2026-07-20).** During the research pass for this guide we
learned the conjecture was disproved for n ≥ 3 *this very week*; the repo's
tests re-verify the counterexample's certificates independently
(tests/test_counterexample.py). The guide teaches the conjecture as history
demanded (chapters 1–10), then tells the ending honestly (chapters 11–12):
false for n ≥ 3 (announced July 2026, peer review pending), open for n = 2.

## Chapter template

1. *Promise*: "By the end of this page you will …" (one sentence)
2. *Picture/animation* immediately
3. Short explanation in simple sentences, interleaved with figures
4. *Try it*: command to re-render / tweak the figure
5. *The one thing to remember* (boxed sentence)
6. Link to next chapter

## Repo layout (target)

Folder-per-chapter (research: GitHub auto-renders each folder's README.md, giving
click-through navigation; media lives beside the text that uses it):

```
guide/NN-slug/README.md   one chapter per folder, PNG/GIF assets alongside
src/jacobian_guide/       core.py (sympy math), examples.py, plotting.py (matplotlib)
src/viz/                  per-chapter figure scripts (chNN_*.py), runnable standalone
manim/                    flagship manim scenes (optional, fancier renders)
tests/                    symbolic sanity tests for every claim about the examples
notes/                    research + this design doc
Makefile                  `make figures` / `make ch04` re-render media, `make test`
```

## Chapter writing style (ADEPT, from pedagogy research)

Each concept: **A**nalogy first, then **D**iagram/animation, then a concrete
**E**xample, then **P**lain-English statement, and only then the **T**echnical
symbols. GitHub math gotchas: use ```math fences for display math, avoid `|`
and spaces touching `$` in inline math, no math inside tables.

## Toolchain decisions

- **matplotlib + Pillow GIFs** are the workhorse: render everywhere, embed inline on
  GitHub, no LaTeX needed.
- **manim (Community Edition)** for the flagship scenes (grid morphs, zoom); use
  `Text` (Pango) rather than `Tex` to avoid a LaTeX dependency. ffmpeg is available.
- **sympy** computes every Jacobian, determinant and inverse that the guide claims —
  tests assert them, so the guide can't drift from the math.
- GitHub markdown renders `$…$` math; keep formulas few and small anyway.

## Correctness guardrails (facts the text must respect)

- Over ℂ, "det J F is a nonzero constant" ⟺ "det J F vanishes nowhere" (a
  non-vanishing polynomial is constant). Over ℝ these differ — Pinchuk's map has
  det > 0 everywhere yet is not injective, so the real version of the conjecture
  is FALSE with "nowhere zero", which is why the statement lives over ℂ / uses
  "constant".
- Char p > 0 fails: F(x) = x − xᵖ has F′ = 1 but is not injective (all of 𝔽ₚ maps to 0).
- Injectivity of a polynomial map ℂⁿ→ℂⁿ already implies surjectivity
  (Ax–Grothendieck) and the inverse is automatically polynomial — so the hard part
  is injectivity.
- Known: n = 1; degree 2 (Wang 1980); reduction to degree 3 (Bass–Connell–Wright
  1982); status: open for all n ≥ 2 (as of 2026).
- (Exact Pinchuk formulas, degrees, and further attributions: see research notes.)
