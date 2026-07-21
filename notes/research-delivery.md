# Research notes, how to deliver the guide (visuals, tooling, format)

Condensed from a web-research pass (July 2026). URLs at bottom.

## Pedagogy

- **3Blue1Brown (Essence of Linear Algebra)**: animate the *whole plane* moving;
  linearity = gridlines stay straight, parallel, evenly spaced, origin fixed;
  determinant introduced as *the factor by which the unit square's area scales*
  (negative = flip, zero = squished to a line); inverse = playing the film
  backwards, exists iff det ≠ 0. One persistent moving-grid visual anchors the
  whole series. Picture first, formula last.
- **Explorable explanations** (Bret Victor, Nicky Case): reader active, toys
  before formalism. Static-GitHub approximation: looping GIFs as toys +
  "change this line and re-render" scripts + `<details>` blocks for optional depth.
- **ADEPT** (BetterExplained): per concept, Analogy → Diagram → Example →
  Plain-English → Technical. Symbols come last.
- Recommended concept order (one per chapter): function → inverse → polynomial →
  2D map → linear map → determinant → derivative-as-local-linear-map → Jacobian →
  local vs global → the conjecture. Thread one worked example throughout:
  F(x, y) = (x + y², y), det ≡ 1, inverse (x − y², y).

## Tooling facts (verified against PyPI / docs, July 2026)

- **Manim CE** stable v0.20.1, needs Python ≥ 3.11. Since v0.19.0 no external
  ffmpeg binary (uses pyav wheels). LaTeX only needed for `Tex`/`MathTex`, `Text`/`MarkupText` use Pango, no LaTeX. Headless rendering is the default
  (Cairo). Flags: `-qm` 720p30, `--format=gif`, `-s` last-frame PNG.
- **ManimPango 0.6.1 ships NO Linux wheels**, Linux builds from source and needs
  `libpango1.0-dev libcairo2-dev pkg-config python3-dev`. (This machine has no
  sudo ⇒ manim scenes ship as optional code, all committed media rendered with
  matplotlib.)
- Nonlinear warp in manim: `plane.prepare_for_nonlinear_transform()` then
  `plane.animate.apply_function(lambda p: ...)`.
- **matplotlib**: PillowWriter is the one animation writer with no external
  dependency → GIFs via `FuncAnimation` + `PillowWriter`. Morph animation =
  interpolate `(1−t)·p + t·F(p)`. Heatmaps of det J: `pcolormesh` with a
  diverging map centered at 0; `contour(levels=[0])` for the crease.
- **sympy**: `sp.Matrix(F).jacobian(vars)`, `.det()`; invert automorphisms with
  `sp.solve([Eq(u, f1), Eq(v, f2)], [x, y])` (Gröbner with lex order for the
  general case).

## GitHub format

- Math renders in .md via MathJax: `$...$`, `$$...$$`, and ` ```math ` fences.
  Gotchas: no spaces touching `$` delimiters; `|` inside `$...$` breaks tables
  (use `\vert` or avoid math in tables); use ``$`...`$`` when markdown chars clash.
- GIFs referenced by relative path autoplay in READMEs; committed MP4s do NOT
  render a player. Ship GIFs (modest size: ~720 px, ≤ 20 fps, few seconds).
- Width control needs HTML: `<img src="..." width="600">`.
- **Folder-per-chapter, each with its own README.md**, GitHub auto-renders it
  when you click the folder. End chapters with "Next →" links.
- Notebooks on GitHub: diff noise, stale outputs, flaky rendering, prefer
  markdown + runnable scripts + committed media (pattern of Jam3/math-as-code,
  microsoft/ML-For-Beginners).

## Sources

- https://docs.manim.community/en/stable/installation.html /
  .../changelog/0.19.0-changelog.html / .../guides/using_text.html /
  .../tutorials/output_and_config.html / NumberPlane reference
- https://pypi.org/project/ManimPango/ (wheel platforms)
- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions
- https://matplotlib.org/stable/users/explain/animations/animations.html
- https://docs.sympy.org/latest/modules/solvers/solvers.html
- https://www.3blue1brown.com/topics/linear-algebra
- https://betterexplained.com/articles/adept-method/
- http://worrydream.com/ExplorableExplanations/ , https://explorabl.es/
- https://github.com/Jam3/math-as-code , https://github.com/microsoft/ML-For-Beginners
