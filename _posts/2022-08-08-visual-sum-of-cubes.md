---
layout: post
title: Visual Sum of Cubes
description: This article discusses a ‘visual’ derivation of the formula for 1³+2³+…+n³.
excerpt: This article discusses a pattern I noticed in ‘visual’ derivations of the formulas for 1+2+…+n and 1²+2²+…+n², which led me to a similar derivation for 1³+2³+…+n³.
image: /assets/visual-sum-of-cubes.png
latex: true
postprocess: _scripts/latex3d.py
---

$$
1201 \qquad 12201 \qquad 122201 \\[8ex]
$$

This article discusses a pattern I noticed in ‘visual’ derivations of the formulas for $$1+2+\dots+n$$ and $$1^2+2^2+\dots+n^2$$, which led me to a similar derivation for $$1^3+2^3+\dots+n^3$$.

## $$\sum k$$ using two lines

There's a well-known trick for adding $$1+2+\dots+n$$.
Leaving out a bunch of $$+$$ symbols, it looks like this:

$$
\begin{aligned}
\sum_{k=1}^n k
&= \begin{array}{c}1&2&\dots&n-1&n\end{array} \\
&= \frac{1}{2} \left( \begin{array}{c}&1&2&\dots&n-1&n \\ +&n&n-1&\dots&2&1\end{array} \right) \\[2ex]
&= \frac{1}{2} \left(\begin{array}{c}n+1&n+1&\dots&n+1&n+1\end{array}\right) \\[2ex]
&= \frac{1}{2}n(n+1)
\end{aligned}
$$

In other words, we arrange the sum as a line, then add a flipped copy of the line, multiplying by $$\frac{1}{2}$$ to keep the total the same.

Since consecutive entries increase by $$1$$ in the first line but decrease by $$1$$ in the flipped line, the combined entries all have the same value.

So we have $$n$$ entries all of value $$n+1$$, and can simply multiply to get the total.

## $$\sum k^2$$ using three triangles

$$
12200 \\[3ex]
$$

<small>_Triangle arrangement of $$1^2+2^2+3^2+4^2$$_</small>
{: style="text-align:center;"}

I recently encountered[^triangle-source] a similar trick for the sum of squares $$1^2+2^2+\dots+n^2$$, but this time using three triangles instead of two lines!

[^triangle-source]: I learned about the $$\sum k^2$$ triangle trick from a popular (by math standards) [2020 tweet](https://twitter.com/shukudai_sujaku/status/1296886201819906048), though it has certainly been [discovered before](https://twitter.com/EricESeverson/status/1473033720751742977).

$$
\begin{aligned}
\sum_{k=1}^n k^2
&= 12201 \\[4ex]
&= \frac{1}{3} \Bigg( 12201+12202+12203 \Bigg) \\[4ex]
&= \frac{1}{3} \Bigg( 12204 \Bigg) \\[3ex]
&= \frac{1}{3}(2n+1)\frac{n(n+1)}{2} \\[2ex]
&= \frac{1}{6}n(n+1)(2n+1)
\end{aligned}
$$

In other words, we arrange the sum as a triangle—one one ($$1^2$$), followed by two twos ($$2^2$$), and so on, to the last row of $$n$$ $$n$$'s ($$n^2$$).

We then add two rotated copies of the triangle so we have all three orientations (i.e. the $$1$$ gets to be at each of the three corners), multiplying by $$\frac{1}{3}$$ to keep the total the same.

Every entry in the resulting triangle has the same value of $$2n+1$$[^triangle-symmetry], and there are $$1+2+\dots+n=\frac{n(n+1)}{2}$$ (as derived above!) entries, so we simply multiply to get the total.

[^triangle-symmetry]:
    We want to show that the three rotated triangles always combine as a triangle with all entries equal to $$2n+1$$. We'll visualize this for $$n=4$$, but the reasoning works for all $$n$$:

    $$
    12291 + 12292 + 12293 = \\[4ex]
    12294 \\[4ex]
    $$

    **_Base case_** First we notice that the <span class="tan">top</span> will always be a <span class="tan">1</span> in one triangle and an $$\htmlClass{tan}{n}$$ in the other two, so the top always adds up to $$\htmlClass{tan}{2n+1}$$.

    **_Inductive case_** Next we notice that moving from an <span class="orange">arbitrary entry</span> to a <span class="magenta">neighboring entry</span> in any direction, we will always have:

    - In one triangle, we move away from the $$1$$ corner, so the value changes by $$+1$$
    - In another triangle, we move parallel to the $$1$$ corner, so the value doesn't change
    - In the other triangle, we move towards the $$1$$ corner, so the value changes by $$-1$$

    Thus the combined change in value from an <span class="orange">entry</span> to its <span class="magenta">neighbor</span> is always $$1+0-1=0$$, i.e. the combined value is unchanged from one entry to the next.

    And since we can move neighbor-to-neighbor from the <span class="tan">top</span> to every entry in the triangle, the combined values must all be the same $$2n+1$$.

## $$\sum k^3$$ using four tetrahedra

Since this trick worked for $$\sum k$$ using lines and $$\sum k^2$$ using triangles, I wanted to see if any shape would work for the sum of cubes $$1^3+2^3+\dots+n^3$$.

### Pyramids?

The simplest way to arrange $$\sum k^3$$ is as a pyramid, where the top layer is one one ($$1^3$$), the second layer is two-by-two twos ($$2^3$$), and so on, to the last layer of $$n$$-by-$$n$$ $$n$$'s ($$n^3$$). For example, for $$n=3$$:

$$
1222200 \\[4ex]
$$

<small>_Pyramid arrangement of $$1^3+2^3+3^3$$_</small>
{: style="text-align:center;"}

But pyramids aren't very symmetrical—the sides are triangles but the base is a square, so every symmetry leaves the $$1$$ at the top and doesn't actually change the entries at all, meaning we can't combine copies in a helpful way.

### Octahedra?

If you double the pyramid, you get a much more symmetrical object—the octahedron. It represents $$2\sum_{k=1}^n k^3 - n^3$$ (two pyramids, minus one $$n$$th layer since it isn't doubled). For example, for $$n=3$$:

$$
12222101 \\[4ex]
$$

<small>_Octahedron arrangement of $$2\cdot(1^3+2^3+3^3)-3^3$$_</small>
{: style="text-align:center;"}

This looks promising, since we can combine rotated copies of it as we did with lines and triangles. But this only helps if the combined entries all have the same value, and it turns out they don't. For $$n=3$$, for example:

$$
\htmlClass{tan}{12222101} + \htmlClass{orange}{12222102} + \htmlClass{magenta}{12222103} \\[4ex]
= \\
12222104
$$

<small>_Combining the three unique rotations of the octahedron_</small>
{: style="text-align:center;"}

The combined entries aren't all equal—for example, the top is $$\htmlClass{tan}{1}+\htmlClass{orange}{3}+\htmlClass{magenta}{3}=7$$ but the center is $$\htmlClass{tan}{3}+\htmlClass{orange}{3}+\htmlClass{magenta}{3}=9$$.

### Tetrahedra!

Doubling the pyramid didn't work, so maybe we can cut it in half instead!

It turns out the entries of our pyramid are equivalent to the entries of two tetrahedra, minus the shared central triangle. We can visualize this for $$n=3$$ for example:

$$
\begin{aligned}
1222200
&= 1222201 - 1222202 + 1222203 \\[5ex]
&= 2\bigg(122200\bigg) - 12299 \\[4ex]
\end{aligned}
$$
{: style="margin-top:2em;"}

And the pattern holds for all $$n$$:

$$
1222299 = 2\Bigg(122201\Bigg) - 12201 \\[6ex]
$$

We already know the formula for the triangle—it's just $$\sum k^2$$ from above!—and tetrahedra are much more symmetrical than pyramids, so we can try the rotated copies trick again:

$$
\begin{aligned}
\sum_{k=1}^n k^3
&= 1222299 \\[6ex]
&= 2\Bigg(122201\Bigg) - 12201 \\[6ex]
&= 2\cdot\frac{1}{4}\Bigg(122201+122202+122203+122204\Bigg) - 12201 \\[6ex]
&= \frac{1}{2}\Bigg(122205\Bigg) - 12201 \\[4ex]
&= \frac{1}{2}(3n+1)\frac{n(n+1)(n+2)}{6} - \frac{n(n+1)(2n+1)}{6} \\[3ex]
&= \frac{1}{4}n^2(n+1)^2
\end{aligned}
$$
{: style="margin-top:2em;"}

In other words, we add three rotated copies of the tetrahedron so we have all four orientations (i.e. the $$1$$ gets to be at each of the four corners), multiplying by $$\frac{1}{4}$$ to keep the total the same.

Every entry in the resulting tetrahedron has the same value of $$3n+1$$[^tetrahedron-symmetry], and there are $$\frac{n(n+1)(n+2)}{6}$$ entries[^tetrahedral-number], so we simply multiply to get the total.

[^tetrahedron-symmetry]:
    We want to show that the four rotated tetrahedra always combine as a tetrahedron with all entries equal to $$3n+1$$. We'll use the same argument we used for triangles, so see above[^triangle-symmetry] for more details.

    $$
    122291 + 122292 + 122293 + 122294 = \\[4ex]
    122295 \\[4ex]
    $$

    The <span class="tan">top</span> will always be a <span class="tan">1</span> in one tetrahedron and an $$\htmlClass{tan}{n}$$ in the other three, so the top always adds up to $$\htmlClass{tan}{3n+1}$$.

    Moving from an <span class="orange">arbitrary entry</span> to a <span class="magenta">neighboring entry</span> in any direction, we will always have the new value in one tetrahedron differ by $$+1$$ (moving away from the $$1$$ corner), two values stay the same (moving parallel to the $$1$$ corner), and one value differ by $$-1$$ (moving towards the $$1$$ corner).

    Thus the combined change in value from an <span class="orange">entry</span> to its <span class="magenta">neighbor</span> is always $$1+0+0-1=0$$, i.e. the combined value is unchanged from one entry to the next, so they are all $$3n+1$$.

[^tetrahedral-number]:
    The number of entries in the tetrahedron is called a [_tetrahedral number_](https://en.wikipedia.org/wiki/Tetrahedral_number).

    We can calculate it using our formulas for $$\sum k$$ and $$\sum k^2$$, by noticing that the $$j$$th layer of the tetrahedron is just a triangle with $$\sum_{k=1}^j k$$ entries and summing all $$n$$ layers:

    $$
    \begin{aligned}
    \sum_{j=1}^n \sum_{k=1}^j k
    &= \sum_{j=1}^n \frac{j(j+1)}{2} \\
    &= \frac{1}{2}\left(\sum_{j=1}^n j^2 + \sum_{j=1}^n j \right) \\
    &= \frac{1}{2}\left(\frac{n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2}\right) \\
    &= \frac{n(n+1)(n+2)}{6}
    \end{aligned}
    $$

And lastly we just substitute the formula for the $$\sum k^2$$ triangle (derived above!) and simplify the polynomial.

## Summary

So there we have it, all the ‘visual’ sums of powers before you need more than three dimensions, which isn't very visual for humans.

$$
\begin{aligned}
\sum_{k=1}^n k &= \frac{1}{2} \Bigg( 1201+1202 \Bigg) \\[5ex]
\sum_{k=1}^n k^2 &= \frac{1}{3} \Bigg( 12201+12202+12203 \Bigg) \\[5ex]
\sum_{k=1}^n k^3 &= \frac{1}{2}\Bigg(122201+122202+122203+122204\Bigg) - 12201
\end{aligned}
$$

In the context of [_simplices_](https://en.wikipedia.org/wiki/Simplex), going from 2 line segments to 3 triangles to 4 tetrahedra is a nice pattern—line segments are 1-simplices, triangles are 2-simplices, and tetrahedra are 3-simplices.

The pattern can continue, using 5 four-dimensional 4-simplices to derive the formula for $$1^4+2^4+\dots+n^4$$, and so on in increasingly high dimensions. But that might defeat the point of it being a ‘visual’ derivation.

### …but also

If we write the formula for $$\sum k^3$$ in terms of the formula for $$\sum k$$, an interesting identity emerges, known as Nicomachus's Theorem:

$$
\sum_{k=1}^n k^3 = \frac{1}{4}n^2(n+1)^2 = \left(\frac{1}{2}n(n+1)\right)^2 = \left(\sum_{k=1}^n k\right)^2
$$

We can express this visually, as in this image by Wikipedia user cmglee:

<picture>
  <source srcset="/assets/Nicomachus_theorem_3D_dark.svg" media="(prefers-color-scheme: dark)">
  <img src="/assets/Nicomachus_theorem_3D.svg" width="50%" style="margin:auto;">
</picture>
<small>*Visual proof that $$1^3+2^3+\dots+5^3=(1+2+\dots+5)^2$$ <small>[[source](https://en.wikipedia.org/wiki/Squared_triangular_number)]</small>*</small>
{: style="text-align:center;"}

This is a much easier way to visually derive the formula for $$\sum k^3$$, but don't worry I still had fun figuring out the tetrahedron way—the more, the merrier!

_**Addendum** If you're curious how I made the spinning diagrams in this article, I've since written [an explanation]({% post_url 2023-04-20-spinning-diagrams-with-css %})._
