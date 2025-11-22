---
layout: post
title: Annulus Is More
description: xxx
excerpt: xxx
image: xxx
latex: true
---

## Annulus

<picture>
  <source srcset="/assets/annulus_dark.svg" media="(prefers-color-scheme: dark)">
  <img src="/assets/annulus.svg" style="margin:auto;">
</picture>

For an annulus of inner radius $$r$$ and width $$d$$, its area is just the area $$\pi(r+d)^2$$ of the outer circle minus the area $$\pi r^2$$ of the inner circle:

$$
\begin{align*}
A & = \pi(r+d)^2-\pi r^2 \\
& = \pi r^2 + 2\pi rd + \pi d^2 - \pi d^2 \\
& = 2\pi rd + \pi d^2
\end{align*}
$$

Interestingly, this is equal to the outer surface area of a cylinder, plus the area of a circle:

<picture>
  <source srcset="/assets/annulus-cylinder-circle_dark.svg" media="(prefers-color-scheme: dark)">
  <img src="/assets/annulus-cylinder-circle.svg" style="margin:auto;">
</picture>

I was wondering if there's a geometric "proof" of this, and here's what I came up with:

TODIAGRAM:
ring + circle
= flat square ring + 4-segment circle
= flat octagon ring + 8-segment circle
= flat 16-gon ring + 16-segment circle
= ...
= annulus
