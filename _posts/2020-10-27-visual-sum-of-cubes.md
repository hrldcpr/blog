---
layout: post
title: Visual Sum of Cubes
latex: true
date: 2020-10-27 20:10:27 -0400
---

## $$\sum k$$ using two lines

There's a famous visual proof of the formula for the sum of the integers $$1$$ to $$n$$.
Leaving out a bunch of $$+$$ symbols, it looks like this:

$$
\begin{aligned}
\sum_{k=1}^n k
&= \begin{array}{c}1&2&3&\dots&n-2&n-1&n\end{array} \\
&= \frac{1}{2} \left( \begin{array}{c}1&2&3&\dots&n-2&n-1&n \\ n&n-1&n-2&\dots&3&2&1\end{array} \right) \\[1ex]
&= \frac{1}{2} \left(\begin{array}{c}n+1&n+1&n+1&\dots&n+1&n+1&n+1\end{array}\right) \\[1ex]
&= \frac{1}{2}n(n+1)
\end{aligned}
$$

In other words, we arrange the sum as a line, then make a copy of the line and flip it, and then combine them.

Thanks to their symmetry, this leads to a line of $$n$$ entries all with the same value $$n+1$$, so we can simply multiply to get the sum.


## $$\sum k^2$$ using three triangles

It turns out we can use a similar trick for the sum of squares $$1^2$$ to $$n^2$$, but this time we use three triangles instead of two lines!

I learned this from a tweet by @shukudai_sujaku:

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">自然数の２乗の和の公式を、視覚的に理解できる方法を発見しました！ <a href="https://t.co/T38kgPQJOM">pic.twitter.com/T38kgPQJOM</a></p>&mdash; 3月の宿題で(1)のみ正解の数弱 (@shukudai_sujaku) <a href="https://twitter.com/shukudai_sujaku/status/1296886201819906048?ref_src=twsrc%5Etfw">August 21, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<small>*Google's translations: "I found a way to visually understand the formula of the sum of squares of natural numbers!" and "(Represents the sum of the numbers in a row. The same applies below.)"*</small>

In other words, we arrange the sum as a triangle—one one ($$1^2$$), followed by two twos ($$2^2$$), and so on, up to the last row of $$n$$ $$n$$'s ($$n^2$$).

We then rotate two copies of the triangle so we have all three orientations (i.e. the 1 gets to start in each of the three corners), and combine them. Thanks to symmetry of the triangles, each combined entry adds up to $$2n+1$$.[^trisymmetry]

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

This made me want to try continuing this pattern, for the sum of cubes $$1^3$$ to $$n^3$$.

Unfortunately, tetrahedra don't sum as cleanly as lines and triangles so we have to rearrange things a bit:

$$
\begin{array}{c}
1 \\
2~~~~~~~2 \\
⋰~~~~~~~~~~~~~⋱ \\
\ddots \\
n-1~\cdots\cdots~n-1 \\
n~~~n~\cdots\cdots\cdots\cdots~n~~~n
\end{array}
= \sum_{k=1}^n \frac{k(k+1)}{2}k
= \frac{1}{2}\left(\sum_{k=1}^n k^3 + \sum_{k=1}^n k^2\right)
$$

$$
\begin{aligned}
\sum_{k=1}^n k^3
&=
&= \frac{1}{2} \left( \begin{array}{c}1&2&3&\dots&n-2&n-1&n \\ n&n-1&n-2&\dots&3&2&1\end{array} \right) \\[1ex]
&= \frac{1}{2} \left(\begin{array}{c}n+1&n+1&n+1&\dots&n+1&n+1&n+1\end{array}\right) \\[1ex]
&= \frac{1}{2}n(n+1)
\end{aligned}
$$

In the context of [simplices](https://en.wikipedia.org/wiki/Simplex), going from 2 line segments to 3 triangles to 4 tetrahedra is a nice pattern—line segments are 1-simplices, triangles are 2-simplices, and tetrahedra are 3-simplices.

I *think* the pattern can continue, using 5 four-dimensional 4-simplices to derive the formula for sum of $$1^4$$ to $$n^4$$, and so on.
