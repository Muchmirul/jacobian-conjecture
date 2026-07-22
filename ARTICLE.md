# Jacobian Conjecture for Baby

*A step-by-step guide, starting from zero, to a famous math problem that stayed open for 87 years and then fell in July 2026. Every idea is shown as an animation, and you can check the final discovery yourself.*

![A square grid smoothly deforming into a curved shape that can be perfectly undone](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/00-start-here/hero.gif)

Look at this animation. A flat grid gets bent into a strange curved shape. It looks like the grid is ruined.

It is not. **This bending can be perfectly undone.** There is a second simple rule that moves every point back to exactly where it started. Nothing is lost.

In 1939, a mathematician named Ott-Heinrich Keller asked a simple question about maps like this one. His question became one of the most famous unsolved problems in mathematics. Many mathematicians published proofs. **Every proof turned out to be wrong.**

The problem stayed open for 87 years. Then, in July 2026, it fell. Only partly, and in a way nobody expected. (The original two-dimensional case is *still* open.)

This article explains the whole story from zero. You do not need any math background. Each chapter is one small idea, explained with a picture first. At the end, you can check the 2026 discovery **with your own hands**, using simple arithmetic.

(Everything here is backed by an open repository: [github.com/Muchmirul/jacobian-conjecture](https://github.com/Muchmirul/jacobian-conjecture). It contains the code for every animation and a test suite that re-checks every mathematical claim.)

Here is the plan. Chapters 1 to 8 build the ideas one by one. Chapter 9 states the famous question. Chapters 10 to 12 tell what happened to it.

---

## 1 · Functions are machines

We start with the smallest idea: what a "function" is.

A **function** is a machine. You feed it a number. It gives you back a number. That is all.

![Numbers ride through the machine 'double it, then add 1' one at a time, with a scoreboard recording each trip](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/01-functions-are-machines/machine.gif)

The machine above uses the rule "double the number, then add 1." Feed it 3, you get 7. Feed it 0, you get 1. Feed it 10, you get 21.

Two rules make a machine a function. First, it always gives an answer. Second, the same input always gives the same output, with no randomness and no "it depends".

Now change the viewpoint. This new picture powers the rest of the article. Instead of feeding the machine one number at a time, imagine it moving **every number on the number line at the same time**.

![Dots on a number line all travel simultaneously to their outputs on a second line below](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/01-functions-are-machines/numberline.gif)

Same machine, new picture: a function moves the whole line. Keep this picture in mind. We will soon use it on bigger spaces.

One piece of notation, and it is the only one we need. Mathematicians name a machine with a letter like $f$ and write its rule as $f(x) = 2x + 1$. Read it as "$f$ takes a number $x$ and returns $2x+1$." The letter $x$ is just a placeholder for the input.

> **The one thing to remember:** a function is a machine that turns each input into exactly one output, and you can picture it moving every number at once.

---

## 2 · The undo machine

A machine moves every number. The next question is whether the move can be reversed. This small idea is the seed of the whole story.

The machine "double it" sends 3 to 6. The machine "halve it" sends 6 back to 3. Run one after the other, and every number ends up exactly where it started.

![Dots travel from the input line down to their doubled outputs, then travel back up home](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/02-the-undo-machine/undo.gif)

When a second machine brings every output back to its original input, it is called the **inverse**, or the undo machine. Doubling and halving undo each other. So do "add 5" and "subtract 5".

Now try to undo "square it", which multiplies the number by itself.

![Left: the dots minus 3 and 3 land on the same output 9. Right: the doubling dots land on separate outputs](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/02-the-undo-machine/collision.gif)

Feed it −3: you get 9. Feed it 3: you also get 9. Now stand at 9 and try to walk back. **Which input did you come from?** You cannot know. The information "was it negative?" is gone.

An undo machine cannot exist when either of two things happens:

1. **Collisions:** two different inputs land on the same output. (−3 and 3 both land on 9.)
2. **Gaps:** some outputs are never produced, so the undo machine would have nothing to say there. (Squaring never outputs −4.)

If there are no collisions and no gaps, then every output has exactly one origin. So "walk back where you came from" is itself a machine.

*(The official words, if you want them: no collisions is called **injective**, no gaps is called **surjective**, both together is called **invertible**. You can forget these words. "No collisions, no gaps" is all you need.)*

> **The one thing to remember:** a machine can be undone exactly when no two inputs share an output and no output is missing. Undoing fails the moment information is destroyed.

---

## 3 · Polynomials

So far a machine could use any rule. The famous problem is about one specific family of machines: the ones built from nothing but plus and times.

Take an input $x$. Allow yourself only two operations, adding and multiplying, using numbers or pieces you have already built. Any machine you can build this way is called a **polynomial**.

- $2x + 1$ doubles and then adds one. It is a polynomial.
- $x^2$ is $x$ times $x$. It is a polynomial, since a power is just repeated multiplication.
- $x^3 - 2x$ builds $x \cdot x \cdot x$, builds $2x$, and subtracts. It is a polynomial, since subtracting is adding a negative.

Here are their graphs. For each input $x$ along the bottom, the height of the curve shows the output.

![The graphs of 2x+1, x squared, and x cubed minus 2x draw themselves; then dashed gray curves appear](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/03-polynomials/gallery.gif)

The dashed gray curves, $\sin x$, $1/x$, and $\sqrt{x}$, are **not** polynomials. Each one needs an operation we did not allow: dividing by the input, or an infinite process.

Why focus on polynomials? Because they are the machines you can run **exactly, with pencil and paper, in a finite number of steps**. There is no approximation, no "undefined at zero", and no infinite sums. They are the most concrete and most checkable machines in mathematics.

That is what makes the coming problem so surprising. It is a question about the simplest machines we have, and it defeated everyone for 87 years.

One more word: the **degree** of a polynomial is its biggest power. So $x^3 - 2x$ has degree 3. This word becomes important in chapter 10.

> **The one thing to remember:** a polynomial is any machine built using only plus and times. These are the most finite, most checkable machines there are.

---

## 4 · Maps of the plane

Machines that eat one number were the warm-up. Now our machines eat **points**.

A **point** of the plane is a pair of numbers $(x, y)$: how far right, and how far up. A **plane map** is a machine that takes a point and returns a point. A point is two numbers, so the machine has two output slots. Each slot may use both inputs: $F(x, y) = (\text{rule using } x, y,\ \text{rule using } x, y)$.

In chapter 1, a machine moved the whole number line. A plane map moves the **whole plane**. To see it, draw a grid on the plane and watch the map carry it.

![A square grid warps smoothly, two marked dots travel with it](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/04-maps-of-the-plane/rubbersheet.gif)

The plane moves like a rubber sheet. The two dots are examples: each one is picked up at $(x, y)$ and put down at $F(x, y)$.

Here are six basic plane maps, all moving at once.

![Six panels animate at once: the untouched plane, then slide, turn, grow, lean and bend](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/04-maps-of-the-plane/gallery.gif)

Slide, turn, grow, and lean all keep the grid lines straight. The last one, *bend*, does not, because its rule uses $y^2$ and $x^2$, and squaring is what bends lines. This connects back to chapter 3.

> A **polynomial map** of the plane is a map where both output rules are polynomials, built from $x$ and $y$ using only plus and times. For example, $F(x, y) = (x + \tfrac{1}{4}y^2,\; y + \tfrac{1}{4}x^2)$ is the "bend" panel above.

The rest of this article is about exactly these: polynomial maps of flat space.

> **The one thing to remember:** a plane map moves every point of the plane at once, like a rubber sheet. It is a polynomial map when both of its rules use only plus and times.

---

## 5 · Straight maps and the area factor

Before we let maps bend anything, we need one number from the simplest maps. It is the most useful number in this story.

Some plane maps are perfectly regular. Grid lines stay **straight**, stay **parallel**, and stay **evenly spaced**, and the center point does not move. These are called **linear maps**, and we will call them straight maps. The turns, grows, squeezes, and leans of the last chapter are all straight maps.

Watch what each one does to the yellow square, which starts with area 1.

![Six straight maps morph the grid at once while a yellow patch shows each area factor](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/05-straight-maps-and-area/gallery.gif)

There is a pattern here. A straight map scales the yellow square's area by some factor, and it scales **every** piece of the plane, everywhere, by that **same** factor.

- turn, squeeze, and lean each give area × 1
- grow, which doubles everything, gives area × 4
- mirror gives area × 1, but the square comes out flipped, like a page turned over
- squash gives area × 0, and the whole plane lands on a single line

This one number, the area-scaling factor, is called the map's **determinant**. For the mirror we record the flip with a minus sign, so its determinant is −1. The determinant therefore tells you two things at once: how much area is scaled, and whether the plane got flipped over.

Determinant zero is the disaster case.

![The grid collapses onto a single diagonal line; three marked dots merge into one](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/05-straight-maps-and-area/squash.gif)

Watch the three dots. When the determinant is 0, the plane is pressed flat onto a line. Different points land on the same spot, which means collisions everywhere. Chapter 2 told us what that means: information destroyed, undo impossible.

And if the determinant is not zero? Then a straight map has no collisions and no gaps, and it has an undo map, which is also straight. For straight maps, one number decides everything:

> **A straight map can be undone exactly when its determinant is not zero.**

*(Where the number comes from: a straight map is fully described by four numbers, $F(x, y) = (ax + by,\; cx + dy)$. Its determinant is $ad - bc$. You will never need to compute this by hand here.)*

> **The one thing to remember:** a straight map scales all areas by one fixed factor, the determinant. If the factor is nonzero, the map can be undone. If the factor is zero, the plane is crushed and information is lost.

---

## 6 · Bending the grid

Now we let polynomial maps bend things, and we compare two kinds. Some maps bend the plane but never squeeze it. Others press area down to zero somewhere. This difference is the center of the whole story.

Start with the first kind. Here is the **shear**:

```math
F(x, y) = (x + y^2,\; y)
```

In words, it slides each horizontal row to the right by $y^2$. Rows near the middle barely move, and rows far away move a lot. Watch the yellow square as the plane bends.

![A grid bends into a sideways parabola shape; a yellow unit patch deforms but visibly keeps its size](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/06-bending-the-grid/shear.gif)

The grid bends, but nothing is squeezed or stretched, so every small piece keeps **exactly its area**. This map is easy to undo. Each row slid right by $y^2$, so to undo it you slide it back: $G(x, y) = (x - y^2,\; y)$. $G$ undoes $F$ perfectly, and $G$ is itself a polynomial map. This is our first interesting **polynomial map with a polynomial undo**.

You can stack shears to build much wilder maps. Do a vertical shear, then a horizontal one. The two steps together form one polynomial map:

```math
H(x, y) = (\,x + (y + x^2)^2,\; y + x^2\,)
```

![Two shears stacked produce a wild-looking curved map](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/06-bending-the-grid/tangled.gif)

This is the bending from the very first animation of the article. It looks hopeless, but you know its secret: it is two simple shears, one after the other. To undo it, undo the layers in reverse order, like taking off your shoes and then your socks. Its undo map is again a polynomial, and in chapter 10 the computer will find it for us.

You can stack as many shears and straight maps as you like. The result looks more and more complicated, and it always stays perfectly undoable.

Now the second kind. Some polynomial maps destroy information.

![The plane folds like a closing book onto the right half plane; two marked dots crash into one](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/06-bending-the-grid/fold.gif)

$F(x, y) = (x^2, y)$ **folds** the plane like closing a book, so the left half lands exactly on the right half. The two dots show a collision: two different points reach one landing spot. This map cannot be undone.

![Under (x, xy) the grid morphs while the red vertical line collapses onto a single point at the origin](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/06-bending-the-grid/crush.gif)

$F(x, y) = (x, x\cdot y)$ **crushes**, so the entire vertical center line collapses onto one single point. It also cannot be undone.

Compare the two kinds. The shear and stacked shears bend but never crush, so they can be undone, with a polynomial undo. The fold and crush press area down to zero somewhere, which causes collisions, so they have no undo.

This looks like chapter 5's rule, that a map can be undone exactly when its area factor is nonzero, trying to extend from straight maps to bent maps. But a bent map stretches area by different amounts in different places. So what plays the role of "the" area factor? For that we need a microscope.

> **The one thing to remember:** stacked shears bend the plane into complicated shapes that are still easy to undo. Folds and crushes press area to zero somewhere, and they can never be undone.

---

## 7 · The microscope

Now the word that sounds the scariest in this subject: the **Jacobian**. It is just a microscope.

Take the curved graph of $y = x^2$ and zoom in on one point.

![A continuous zoom into the parabola at (1,1): the curve straightens until it is a straight line of slope 2](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/07-the-microscope/zoom1d.gif)

Under the microscope, the curve straightens out. Zoom in enough and it looks exactly like a straight line. The slope of that line, here 2, is called the *derivative* at that point. This one observation, that smooth things look straight up close, is all the calculus you need today.

Now do the same with a bent grid. Take the stacked-shear map $H$ from the last chapter, pick the point $p = (0.5,\, 0.5)$, and zoom in on what $H$ does near $p$.

![The camera stays locked on one dot while zooming in; the bent grid straightens into a perfect parallelogram grid](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/07-the-microscope/microscope.gif)

Straight. Parallel. Evenly spaced. This is exactly what chapter 5 described. **Up close, a bent polynomial map looks just like a straight map.**

> The **Jacobian** of $F$ at a point $p$ is the straight map you see when you zoom in on $F$ near $p$.

Different points show different straight maps under the microscope, so the Jacobian depends on where you look. (Computers find it by a mechanical rule, a small table of derivatives. You will never compute one by hand here; the computer does it in chapter 10.)

Here is why this matters. Straight maps have a determinant, an area factor. So at **every point** $p$, the map has a *local area factor*, written $\det J_F(p)$. It is the determinant of the straight map seen under the microscope at $p$. It says how strongly $F$ stretches or squeezes *tiny* pieces right at $p$, and whether it flips them.

Let us paint this number over the whole plane for two maps, and send a probe dot to read it out.

![A probe dot wanders over two heatmaps: over the shear its readout stays 1, over the fold it reads 2x and hits 0 on the fold line](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/07-the-microscope/det_heatmaps.gif)

- The shear $(x + y^2, y)$ has local area factor **exactly 1 at every point**. At every location, under every zoom, it is a perfect area-preserving straight map. That is the precise meaning of "bends but never crushes".
- The fold $(x^2, y)$ has local area factor $2x$. It is positive on the right half (blue), negative on the left half where that half got flipped (red), and exactly zero on the fold line. The picture shows exactly where the map destroys information.

> **The one thing to remember:** zoom in anywhere on a smooth map and you see a straight map, the Jacobian at that point. Its determinant is the local area factor, and the places where this factor is 0 are exactly the places where the map crushes.

---

## 8 · Local vs global

The microscope looks like the perfect tool. Here is the trap at the heart of the subject: a map can look perfect under every microscope and still be broken.

The tempting shortcut goes like this. To know if a map can be undone, check the local area factor everywhere. If it is never zero, the map never crushes anything, so surely it can be undone. Can it?

Part of this is true. If the local factor at a point $p$ is not zero, then near $p$ the map can be undone. Zoom in enough and it is a healthy straight map. This fact is called the *inverse function theorem*, and it is solid.

But look at what it does **not** promise.

Take the polynomial map $F(x, y) = (x^2 - y^2,\; 2xy)$ and apply it to a ring around the center. The blue half is on the right, and the gold half is on the left.

![Two half-rings, blue and gold, each smoothly map onto the same full ring, interleaving](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/08-local-vs-global/wrap.gif)

Each half maps smoothly, with no creases and no crushing, and near every single point the microscope says "all clear". But the blue half covers the **entire** target ring, and the gold half covers **the same ring again**. Every target point is hit **twice**, by two points far away from each other. Watch the blue and gold dots collide.

These are collisions, but not local ones. Each collision pairs two points from opposite sides of the plane. No microscope can see both at once. So the map is locally fine everywhere, yet globally broken.

How many bad points caused this? On the whole plane, this map's local area factor is $4(x^2 + y^2)$.

![A probe spirals inward, its readout shrinking until it hits exactly 0 at the origin, the only bad point](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/08-local-vs-global/one_bad_point.gif)

It is zero at **one single point**, the center, and healthy everywhere else. One bad point out of infinitely many, and the map uses it to wrap the plane around twice. That is how sensitive this game is.

*(It gets worse. There are smooth non-polynomial maps whose local factor is nonzero at every point, with no exception at all, that still hit target points infinitely often. So for general smooth maps, "locally fine everywhere" is very far from "globally undoable". If any hope remains, it must come from using very special machines, such as polynomials.)*

So "local factor never zero" is not enough on its own. If we want a local condition that guarantees a global undo, we must add something. Keller chose the strongest possible local condition: the local area factor must be **the same constant at every point**, not just nonzero. And the map must be **polynomial**. Is that enough?

That is the Jacobian Conjecture. The next chapter states it fully.

> **The one thing to remember:** the microscope only checks a map near each point. Points far apart can still collide, so local undoability everywhere does not give global undoability.

---

## 9 · The conjecture

You now have every piece:

1. **Undoable** means no collisions and no gaps (chapter 2).
2. **Polynomial maps** are machines built from plus and times only (chapters 3 and 4).
3. **Determinant** is the area factor of a straight map, where zero means crushed (chapter 5).
4. **Jacobian** is the straight map seen under the microscope, and $\det J$ is the local area factor at each point (chapter 7).
5. **The trap** is that a nonzero local factor everywhere still does not force global undoability (chapter 8).

Here is Keller's question, from 1939. Do not just ask the local area factor to avoid zero. Ask it to be **the same nonzero constant at every single point**, like the shear and the stacked shears, where the factor is exactly 1 everywhere. And keep the maps polynomial, the simplest machines there are.

Surely such a map must be undoable, with a polynomial undo?

![The statement card assembles clause by clause](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/09-the-conjecture/statement_card.gif)

Here is the same question in motion, with the condition first and then the question.

![A polynomial map tangles the grid while a yellow patch keeps exactly the same area; then the motion reverses under the question](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/09-the-conjecture/conjecture.gif)

That is the **Jacobian Conjecture**. It is not a theorem but a conjecture: a statement everyone believed and nobody could prove.

**Three details, for completeness:**

- **All dimensions.** The question is asked for the plane, for 3D space, for 4D space, and so on. Each output coordinate is a polynomial in all the input coordinates. Our pictures are 2D because that is what eyes can see.
- **Complex numbers.** Officially the conjecture is asked over the complex numbers, a larger number system where every polynomial equation has solutions. Over ℂ, "the local factor is never zero" and "the local factor is a nonzero constant" turn out to be the same condition. Chapter 11 shows that over the ordinary real numbers the conjecture is actually **false**, so this choice of number system genuinely matters.
- **Only collisions matter.** A deep theorem (Ax–Grothendieck) helps here. If a complex polynomial map has no collisions, then it automatically has no gaps. Its undo map is automatically a polynomial too. So the entire 87-year battle was about one question: **can two different points share an output?**

Why did it look provable? Every no-crush map we met satisfies the condition, with factor 1 everywhere, and can be undone. The next chapter shows that every example anyone ever built confirmed the conjecture, and that for degree-2 maps it was actually proved. It looked close to certain.

Nobody proved it, from 1939 to 2026.

> **The one thing to remember, the Jacobian Conjecture:** if a polynomial map's local area factor is the same nonzero constant at every point, must the map be undoable, with a polynomial undo?

---

## 10 · Test it yourself

Before seeing what happened to the conjecture, you can test it, using a computer that does exact algebra rather than approximations.

Python's `sympy` library works with polynomials exactly, the way you would with a pencil and unlimited patience. The [companion repo](https://github.com/Muchmirul/jacobian-conjecture) wraps it in a few helpers. Here is a real session with the stacked-shear map $H(x,y) = (x + (y+x^2)^2,\; y + x^2)$:

```python
>>> from jacobian_guide.core import jacobian_det, invert, compose, degree
>>> from jacobian_guide.examples import VARS, TANGLED   # TANGLED is H

>>> jacobian_det(TANGLED, VARS)          # local area factor, symbolically
1
```

It answers: the factor is the constant 1. Algebra checked the formula itself, so this covers every one of the infinitely many points at once. So $H$ satisfies Keller's condition. Now the real test. Ask for the undo map:

```python
>>> G = invert(TANGLED, VARS)
>>> G
(x - y**2, -x**2 + 2*x*y**2 - y**4 + y)

>>> compose(G, TANGLED, VARS)            # undo after do = ?
(x, y)
```

The computer returns an explicit polynomial undo, and the round trip simplifies to exactly $(x, y)$, the do-nothing map. Every point walks back home.

![Step 1: the map H tangles the blue grid; step 2: its undo map G walks every point exactly back home](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/10-kicking-the-tires/roundtrip.gif)

For contrast, the fold $(x^2, y)$ has local area factor $2x$, which is not constant, so it never satisfied the condition. The conjecture makes no promise about it. That is consistent.

The score after decades of such tests:

| map | local area factor | undoable? | degree, undo degree |
|---|---|---|---|
| shear $(x+y^2,\,y)$ | 1 | yes | 2, 2 |
| stacked map $H$ | 1 | yes | 4, 4 |
| triple-stacked $H_3$ | 1 | yes | 4, 4 |
| fold $(x^2,\,y)$ | $2x$, does not qualify | no | n/a |

Every example anyone ever built agreed with the conjecture. Theory added more:

- **Degree up to 2 was proved** (Wang, 1980): every degree-2 map satisfying the condition, in any dimension, can be undone.
- **Degree 3 contains the whole problem** (Bass–Connell–Wright, 1982): if the conjecture holds for all degree-3 maps, it holds for all degrees. The entire problem was compressed into degree 3, and still nobody could prove it.
- **In the plane, it was checked up to degree 100** (Moh, 1983, with computer help).

One detail is worth noticing. In the plane, the undo map always has the *same* degree as the map. In dimension 3 and higher, the undo can be far more complicated than the map. Higher dimensions play by wilder rules. Remember that.

> **The one thing to remember:** every example ever built confirmed the conjecture. Degree 2 was proved. The whole problem was squeezed into degree 3, and there it stayed unsolved for four more decades.

---

## 11 · Why it was so hard

If every test passes and the statement looks true, why could nobody prove it? Because any proof must get past three separate obstacles at the same time. They stopped 87 years of attempts, including published proofs by serious mathematicians.

![The timeline fills in event by event, 1884 to 2026](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/11-why-it-was-so-hard/timeline.gif)

The same pattern repeated for a century. Someone announces a proof, the world gets excited, and a subtle hole is found. It happened to Kraus in 1884, before Keller even asked the question, to Engel in 1955, three times to Segre, to Gröbner, and to many modern attempts.

**Obstacle 1: the statement is false over the real numbers.** One hope was that ordinary real-plane geometry, the kind our pictures show, already forces a map to be undoable once the local factor is never zero. It does not. In 1994, Sergey Pinchuk built an explicit pair of polynomials, of degrees 10 and 25. Their local area factor is **positive at every real point**. And the map still sends two different points to the same place. Watch the probe below read this factor everywhere: the running minimum dips low, but it never touches 0.

![A probe sweeps Pinchuk's log-scale determinant heatmap; the running minimum never reaches zero](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/11-why-it-was-so-hard/pinchuk_det.gif)

There is no crushing anywhere and no flipping anywhere, and yet there is still a collision. So reasoning about real numbers alone can never prove the conjecture, because over the reals the statement is simply not true.

*(How do we know Pinchuk's factor is never zero? It equals $\det J = t^2 + (t + f\,(13 + 15h))^2 + f^2$ for certain helper polynomials $t, f, h$. That is a sum of three squares, so it is never negative, and a short argument shows it is never zero. It is positive everywhere but not constant, and over the complex numbers "never zero" and "constant" would be the same thing. This is why the complex setting in chapter 9 matters. The repo verifies the identity symbolically in `tests/test_pinchuk.py`.)*

**Obstacle 2: the statement is false in clock arithmetic.** Another hope was that pure symbol manipulation, meaning algebra that works in any number system, might be enough. It is not. Take a clock with a prime number $p$ of positions, where numbers wrap around. The simple machine $F(x) = x - x^p$ has constant slope 1, the perfect condition. Yet it sends *every* clock position to 0. That is a total collapse. So any proof must use a property that ordinary numbers have and clock arithmetic lacks (*characteristic zero*, in the jargon). Pure symbol-pushing cannot be enough.

Watch the collapse on a clock with 5 positions.

![Five numbers around a clock face all travel to position 0; the machine x minus x to the fifth has slope 1 yet collapses the whole clock](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/11-why-it-was-so-hard/clock.gif)

**Obstacle 3: the danger sits at infinity.** A classical theorem, due to Hadamard, says that a map that is locally undoable everywhere, and that does not let points run away to infinity, is globally undoable. So maybe polynomial maps cannot send points to infinity in a bad way? They can. Under the crush map $(x, xy)$, take the points $(1/2, 2), (1/3, 3), (1/4, 4), \dots$ The points themselves run off to infinity. Their outputs $(1/2, 1), (1/3, 1), (1/4, 1), \dots$ quietly approach the ordinary point $(0, 1)$.

![Left: the input rides the hyperbola out of every window; right: its output slides along y = 1 toward (0, 1)](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/11-why-it-was-so-hard/escape.gif)

So the escape route to infinity is open, and the important behavior happens near infinity. That is exactly where the mistaken proofs, starting with Kraus in 1884, quietly leaked.

**One more warning sign: dimension 3 is stranger than the plane.** Every complicated undoable map we built was a stack of shears and straight maps. Until 2004, one could hope that all constant-factor maps, in all dimensions, are secretly such stacks. Stacks are always undoable, so the conjecture would follow. In the plane this is a true theorem, because every undoable polynomial map of the plane can be broken into shears. But three dimensions holds Nagata's map. It has local factor 1, a polynomial undo, and perfect behavior everywhere. Yet in 2004 it was proved (Shestakov–Umirbaev) impossible to build from shears and straight maps. Three-dimensional space contains genuinely wilder maps than the plane. Remember that too.

> **The one thing to remember:** a proof had to use all three at once: the maps are polynomial, the numbers are complex, and infinity is kept under control. Real-number reasoning fails because of Pinchuk, formal algebra fails because of clock arithmetic, and the escape to infinity is real. Almost no argument survives all three.

---

## 12 · The fall

July 2026. The 87-year-old conjecture collapsed in every dimension except the one where it was born. This chapter shows the actual object that did it. You can check it yourself.

On July 19–20, 2026, an explicit counterexample to the Jacobian Conjecture in **three variables** was announced. The construction is credited to the mathematician Levent Alpöge, answering a version of the question raised by a colleague. The final example was produced with the help of the AI model Claude Fable. At the time of writing there is no peer-reviewed paper yet, so this article does what mathematics always does with an announcement: verify before trusting. Every claim below is re-checked, independently and exactly, by the companion repository (`tests/test_counterexample.py`). Nothing here asks for your trust.

**The map.** Write $u = 1 + xy$ as a shorthand. The map takes a 3D point $(x, y, z)$ to the 3D point $(P, Q, R)$:

```math
\begin{aligned}
P &= u^3\,z + y^2\,u\,(4 + 3xy) \\
Q &= y + 3x\,u^2\,z + 3xy^2\,(4 + 3xy) \\
R &= 2x - 3x^2 y - x^3 z
\end{aligned}
```

These are three short polynomials, of degrees 7, 6, and 4, with small whole-number coefficients.

**Fact 1: the condition holds.** Its local volume factor, the 3D Jacobian determinant, is exactly the constant $-2$ everywhere. This is precisely Keller's condition. (The minus sign only means space comes out mirror-flipped, uniformly. The size of the factor never changes.)

**Fact 2: and yet.**

![The three input points appear one by one, then three dots ride the arrows and all arrive at the single output (minus 1/4, 0, 0)](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/12-the-fall/collision_card.gif)

Watch it happen in 3D. Each point travels to its output, and all three paths end on the same red X.

![Three points in 3D space travel along dotted roads that converge on one red X at (minus 1/4, 0, 0)](https://raw.githubusercontent.com/Muchmirul/jacobian-conjecture/main/guide/12-the-fall/collision.gif)

Three different points. One landing spot. Standing at $(-1/4,\, 0,\, 0)$, you cannot know which of the three points you came from. This is the collision from chapter 2, and with it, the end of any undo machine. **The Jacobian Conjecture is false in three dimensions.**

It also fails in every higher dimension. In 4D, send the extra coordinate to itself, so $(x,y,z,w) \mapsto (P, Q, R, w)$. The volume factor is still $-2$, and the collision is still there. The same works for 5D, 6D, and so on.

**Check it yourself, by hand.** The third coordinate is the easy one: $R = 2x - 3x^2y - x^3z$. Take the three points and plug in:

- $(0,\ 0,\ -\tfrac14)$: $\quad R = 0 - 0 - 0 = 0$ ✓
- $(1,\ -\tfrac32,\ \tfrac{13}{2})$: $\quad R = 2 - 3\cdot(-\tfrac32) - \tfrac{13}{2} = 2 + \tfrac92 - \tfrac{13}{2} = 0$ ✓
- $(-1,\ \tfrac32,\ \tfrac{13}{2})$: $\quad R = -2 - \tfrac92 + \tfrac{13}{2} = 0$ ✓ &nbsp; *(here $-3x^2y = -\tfrac92$, and $-x^3z = +\tfrac{13}{2}$ because $x^3 = -1$)*

Now the first point in full. At $(0, 0, -\tfrac14)$ we get $u = 1$, so $P = 1 \cdot (-\tfrac14) + 0 = -\tfrac14$ and $Q = 0 + 0 + 0 = 0$. So this point maps to $(-\tfrac14, 0, 0)$, which is arithmetic you can do in your head.

**Check it yourself, by computer.** The other two points involve fractions like $\tfrac{13}{2}$ raised to powers. That is doable on paper, but exact algebra settles it in ten lines:

```python
from sympy import symbols, Matrix, Rational

x, y, z = symbols("x y z")
u = 1 + x*y
P = u**3*z + y**2*u*(4 + 3*x*y)
Q = y + 3*x*u**2*z + 3*x*y**2*(4 + 3*x*y)
R = 2*x - 3*x**2*y - x**3*z

print(Matrix([P, Q, R]).jacobian([x, y, z]).det().expand())   # -> -2

for pt in [(0, 0, Rational(-1, 4)),
           (1, Rational(-3, 2), Rational(13, 2)),
           (-1, Rational(3, 2), Rational(13, 2))]:
    print([f.subs(dict(zip((x, y, z), pt))) for f in (P, Q, R)])
# -> [-1/4, 0, 0]  three times
```

Or simply run the repo's test suite: `python -m pytest tests/test_counterexample.py -q`.

**What survives.** Keller asked his question in 1939 **for the plane**. The counterexample lives in dimension 3, and it needs the extra room. Remember the warning signs: maps that cannot be broken into shears exist only in dimension 3 and up, and undo-degrees only explode in dimension 3 and up. The plane case, meaning two variables and the original question, checked up to degree 100, **is still open today.** The oldest piece of the puzzle is still on the table.

**What the ending means.** For 87 years the question was which extra condition forces a map to be globally undoable. Everyone believed "polynomial plus constant factor" was enough, and many wrong proofs of it were published. The true answer is that **it is not enough**. The escape-to-infinity obstacle from chapter 11 is real, and it can be exploited by polynomials of degree seven. The conjecture did not need a cleverer proof. It needed a counterexample, and the counterexample is so concrete that a person with no mathematical training can check it by hand.

That is what you just did.

> **The one thing to remember:** an explicit degree-7 map of 3D space has constant volume factor −2, yet three different points land on one spot. So the Jacobian Conjecture is **false in dimension 3 and above**, and **still open in the plane**, where it began.

---

## Where to go next

- **The companion repository**, [github.com/Muchmirul/jacobian-conjecture](https://github.com/Muchmirul/jacobian-conjecture), has the code for every animation, the exact-algebra helpers, the full test suite, and research notes with sources.
- A. van den Essen, *Polynomial Automorphisms and the Jacobian Conjecture*, the standard book (advanced).
- T. Tao's blog post on the Ax–Grothendieck theorem, on why "no collisions" automatically gives "no gaps".
- L. A. Campbell, *Picturing Pinchuk's Plane Polynomial Pair* (arXiv:math/9812032), the real-numbers counterexample in pictures.
- The Wikipedia article *Jacobian conjecture*, for current status and references.

*Written July 2026. All figures are animations generated from the repository; run `make figures` to rebuild every one, and `make test` to re-verify every mathematical claim in this article.*
