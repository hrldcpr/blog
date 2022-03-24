---
layout: post
title: Visual Sum of Cubes
latex: true
postprocess: _scripts/latex3d.py
---

## $$\sum k$$ using two lines

There's a famous visual proof of the formula for the sum $$1+2+\dots+n$$.
Leaving out a bunch of $$+$$ symbols, it looks like this:

$$
\begin{aligned}
\sum_{k=1}^n k
&= \begin{array}{c}1&2&\dots&n-1&n\end{array} \\
&= \frac{1}{2} \left( \begin{array}{c}1&2&\dots&n-1&n \\ n&n-1&\dots&2&1\end{array} \right) \\[1ex]
&= \frac{1}{2} \left(\begin{array}{c}n+1&n+1&\dots&n+1&n+1\end{array}\right) \\[1ex]
&= \frac{1}{2}n(n+1)
\end{aligned}
$$

In other words, we arrange the sum as a line, then add a flipped copy of the line, and then combine them.

Thanks to the two lines' symmetry, this leads to a line of $$n$$ entries all with the same value $$n+1$$, so we can simply multiply to get the sum.


## $$\sum k^2$$ using three triangles

It turns out we can use a similar trick for the sum of squares $$1^2+2^2+\dots+n^2$$, but this time we use three triangles instead of two lines!

I learned this from a tweet by @shukudai_sujaku:

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">自然数の２乗の和の公式を、視覚的に理解できる方法を発見しました！ <a href="https://t.co/T38kgPQJOM">pic.twitter.com/T38kgPQJOM</a></p>&mdash; 3月の宿題で(1)のみ正解の数弱 (@shukudai_sujaku) <a href="https://twitter.com/shukudai_sujaku/status/1296886201819906048?ref_src=twsrc%5Etfw">August 21, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<small>*Google's translations: "I found a way to visually understand the formula of the sum of squares of natural numbers!" and "(Represents the sum of the numbers in a row. The same applies below.)"*</small>

TODO note it's also from 1989 by Sidney H. Kung https://twitter.com/3blue1brown/status/1473032237926862852

TODO don't rely on twitter embed—host image locally or reproduce katex

In other words, we arrange the sum as a triangle—one one ($$1^2$$), followed by two twos ($$2^2$$), and so on, up to the last row of $$n$$ $$n$$'s ($$n^2$$).

We then add two rotated copies of the triangle so we have all three orientations (i.e. the 1 gets to be at each of the three corners), and combine them. Thanks to the three triangles' symmetry, each combined entry adds up to $$2n+1$$.[^trisymmetry]

[^trisymmetry]:
    It's easy to see that any corner is a 1 in one triangle and an $$n$$ in the other two, so the corners clearly add up to $$2n+1$$. We can then consider what happens if we move from one entry in the triangle to a neighboring one.

    If we start at an arbitrary entry, with values $$i$$, $$j$$, $$k$$ in the three triangles, and then move to a neighboring entry, the new values will be $$i+1$$, $$j-1$$, $$k$$. ...

    **TODO diagram**

    $$
    \newcommand\iddots{\mathinner{
      \kern1mu\raise1pt{.}
      \kern2mu\raise4pt{.}
      \kern2mu\raise7pt{\Rule{0pt}{7pt}{0pt}.}
      \kern1mu
    }}
    \def\arraystretch{0.2}
    \begin{array}{c}
    1 \\
    2\phantom{1}2 \\
    ⋰\phantom{212}⋱ \\
    n \cdots \cdots n
    \end{array}
    $$

    Thus moving from any entry to any neighboring entry in the combined triangle goes from $$i+j+k$$ to $$(i+1)+(j-1)+k=i+j+k$$, so all entries are equal.

There are $$1+2+\dots+n$$ entries in the triangle—but as we proved above, that simplifies to $$\frac{1}{2}n(n+1)$$, so again we can simply multiply to get the sum.


## $$\sum k^3$$ using four tetrahedra

Since this symmetry trick worked for $$\sum k$$ using lines and $$\sum k^2$$ using triangles, I wanted to see if any shape would work for the sum of cubes $$1^3+2^3+\dots+n^3$$.

### Pyramids?

The simplest way to arrange $$\sum k^3$$ is as a pyramid, where the top layer is one one ($$1^3$$), the second layer is two-by-two twos ($$2^3$$), and so on, up to the last layer of $$n$$-by-$$n$$ $$n$$'s ($$n^3$$). For example, for $$n=3$$:

$$
1222201
$$

<small>*Pyramid arrangement of $$1^3+2^3+3^3$$.*</small>
{: style="text-align: center;"}

But pyramids aren't very symmetrical—the sides are triangles but the base is a square, so every symmetry leaves the 1 at the top and doesn't actually change our entries at all, meaning we can't combine symmetric copies in a useful way.

### Octahedra?

If you double the pyramid, you get a much more symmetrical object—the octahedron. It represents $$2\sum_{k=1}^n k^3 - n^3$$ (two pyramids, minus the final layer since it isn't doubled). For example, for $$n=3$$:

**TODO** 3d diagram

This looks much more promising, since we can overlap rotated copies of it as in the previous proofs. But it turns out the resulting sum isn't the same everywhere, as you can see with this counterexample for $$n=3$$:

**TODO** 3d diagram

<small>*(This is the 3 unique rotations of the octahedron combined. The combined value at any point is the sum of the numbers at that point, but it's not the same everywhere, for example the top is $$1+3+3=7$$ but the center is $$3+3+3=9$$)*</small>

### Tetrahedra!

Finally I tried a tetrahedron:

**TODO** 3d diagram

This tetrahedron doesn't sum as cleanly as the lines, triangles, and pyramids, so we have to rearrange things a bit to get our desired $$\sum k^3$$.

Since the $$k$$th layer is a triangle with $$1+2+...+k=\frac{k(k+1)}{2}$$ (as proved above!) entries all of value $$k$$, the sum of all the layers is:

$$
T = \sum_{k=1}^n k\frac{k(k+1)}{2}
= \sum_{k=1}^n \frac{k^3+k^2}{2}
= \frac{1}{2}\left(\sum_{k=1}^n k^3 + \sum_{k=1}^n k^2\right)
$$

We rearrange to solve for the desired $$\sum k^3$$, and then use four symmetric tetrahedra to get our final formula:

$$
\begin{aligned}
\sum_{k=1}^n k^3
&= 2T - \sum_{k=1}^n k^2 \\[1ex]
&= 2\cdot\frac{1}{4}(T+T+T+T) - \sum_{k=1}^n k^2 \\[1ex]
&= \frac{1}{2}T - \sum_{k=1}^n k^2 \\[1ex]
&= \frac{1}{2}(3n+1)\frac{n(n+1)(n+2)}{6} - \sum_{k=1}^n k^2 \\[1ex]
&= \frac{n(n+1)(n+2)(3n+1)}{12} - \frac{n(n+1)(2n+1)}{6} \\[1ex]
&= \frac{1}{4}n^2(n+1)^2
\end{aligned}
$$

In other words, we add three rotated copies of the tetrahedron so we have all four orientations (i.e. the 1 gets to be at each of the four corners), and combine them. Thanks to the four tetrahedra's symmetry, each combined entry adds up to $$3n+1$$.[^tetsymmetry]

[^tetsymmetry]:
    TODO

There are $$\frac{n(n+1)(n+2)}{6}$$ entries in the tetrahedron (we can prove this using our formulas for $$\sum k$$ and $$\sum k^2$$[^tetnumber]) so once again we can simply multiply to get the sum.

[^tetnumber]:
    The number of entries in the tetrahedron is called a [tetrahedral number](https://en.wikipedia.org/wiki/Tetrahedral_number). Since each layer is a triangle of $$\sum_{k=1}^n k = \frac{n(n+1)}{2}$$ entries, and since we also know that $$\sum_{k=1}^n k^2 = \frac{n(n+1)(2n+1)}{6}$$ the total is:

    $$
    \begin{aligned}
    \sum_{j=1}^n \sum_{k=1}^j k
    &= \sum_{j=1}^n \frac{j(j+1)}{2} \\
    &= \frac{1}{2}\left(\sum_{j=1}^n j^2 + \sum_{j=1}^n j \right) \\
    &= \frac{1}{2}\left(\frac{n(n+1)}{2} + \frac{n(n+1)(2n+1)}{6}\right) \\
    &= \frac{n(n+1)(n+2)}{6}
    \end{aligned}
    $$

The last two steps are just inserting the formula for $$\sum k^2$$ from above, and simplifying the polynomial.[^algebra]

[^algebra]:
    Here are the steps for simplifying the polynomial:
    $$
    \begin{aligned}
    \sum_{k=1}^n k^3
    &= \frac{n(n+1)(n+2)(3n+1)}{12} - \frac{n(n+1)(2n+1)}{6} \\[1ex]
    &= n(n+1)\frac{(n+2)(3n+1) - 2(2n+1)}{12} \\[1ex]
    &= n(n+1)\frac{3n^2+7n+2 - 4n-2}{12} \\[1ex]
    &= n(n+1)\frac{3n^2+3n}{12} = n(n+1)\frac{n(n+1)}{4} \\[1ex]
    &= \frac{1}{4}n^2(n+1)^2
    \end{aligned}
    $$


## Summary

So there we have it, all the 'visual' proofs of sums of powers before you have to start using more than 3 dimensions, which isn't very 'visual' for humans.

$$
\begin{aligned}
\sum_{k=1}^n k &= \begin{array}{c}1&2&\dots&n-1&n\end{array} = \frac{1}{2}n(n+1) \\[4ex]
\sum_{k=1}^n k^2 &= T = \frac{1}{6}n(n+1)(2n+1) \\[4ex]
\sum_{k=1}^n k^3 &= 2T - \sum_{k=1}^n k^2 = \frac{1}{4}n^2(n+1)^2
\end{aligned}
$$

In the context of [simplices](https://en.wikipedia.org/wiki/Simplex), going from 2 line segments to 3 triangles to 4 tetrahedra is a nice pattern—line segments are 1-simplices, triangles are 2-simplices, and tetrahedra are 3-simplices.

I *think* the pattern can continue, using 5 four-dimensional 4-simplices to derive the formula for $$1^4+2^4+\dots+n^4$$, and so on in increasingly high dimensions. But that might defeat the point of it being a 'visual' proof.

TODO note the nicer visual proof of Nicomachus's theorem https://en.wikipedia.org/wiki/Squared_triangular_number

<script src="{{ site.baseurl }}/assets/latex3d.js">
</script>
