---
layout: post
title: Spinning Diagrams with CSS
description: This article discusses using CSS to make spinning 3D diagrams.
latex: true
postprocess: _scripts/latex3d.py
---

I wrote a little [math thing]({% post_url 2022-08-08-visual-sum-of-cubes %}) a few months ago, which featured diagrams like this:

$$
122201 \\[8ex]
$$

Some people were surprised to learn that these diagrams didn't use any javascript or animated image formats, but just HTML and CSS. So I thought I'd explain how it works!

## A spinning cube

It turns out CSS supports 3-dimensional coordinates—so not just horizontal (x) and vertical (y) positions, but also depth (z)!

So let's build a spinning cube of letters.

<div class="cube1" style="width:4em; height:8em;">
  <div style="transform: translate3d(0em, 0em, 2em)">A</div>
  <div style="transform: translate3d(4em, 0em, 2em)">B</div>
  <div style="transform: translate3d(0em, 4em, 2em)">C</div>
  <div style="transform: translate3d(4em, 4em, 2em)">D</div>
  <div style="transform: translate3d(0em, 0em, -2em)">E</div>
  <div style="transform: translate3d(4em, 0em, -2em)">F</div>
  <div style="transform: translate3d(0em, 4em, -2em)">G</div>
  <div style="transform: translate3d(4em, 4em, -2em)">H</div>
</div>

First let's look at the HTML.

We make a div for each vertex, specifying location with `translate3d(x, y, z)`. The cube is 4em wide and the vertices are centered around x=2em and z=0em, which will make it easy to spin around the center:

```html
<div id="cube" style="width: 4em; height: 8em;">
  <div style="transform: translate3d(0em, 0em, 2em)">A</div>
  <div style="transform: translate3d(4em, 0em, 2em)">B</div>
  <div style="transform: translate3d(0em, 4em, 2em)">C</div>
  <div style="transform: translate3d(4em, 4em, 2em)">D</div>
  <div style="transform: translate3d(0em, 0em, -2em)">E</div>
  <div style="transform: translate3d(4em, 0em, -2em)">F</div>
  <div style="transform: translate3d(0em, 4em, -2em)">G</div>
  <div style="transform: translate3d(4em, 4em, -2em)">H</div>
</div>
```
<small>*(I use `em` units, but `px` or any other unit is fine too.)*</small>

Next we have the CSS.

For the absolute 3d positions to work, we give the parent `preserve-3d` and relative position, and the children absolute positions. For the spinning, we animate the parent's `transform` propery to continually rotate about the Y axis:
```css
#cube {
  position: relative;
  transform-style: preserve-3d;
  animation: spin 20s linear infinite;
}

#cube > div {
  position: absolute;
}

@keyframes spin {
  from {
    transform: rotateX(-0.1turn) rotateY(0turn);
  }
  to {
    transform: rotateX(-0.1turn) rotateY(1turn);
  }
}
```
<small>*(Note that `1turn` is the same as `360deg`, I just think it's a nicer unit. And we add a slight tilt `rotateX(-0.1turn)` about the X axis just to make the 3d geometry easier to see.)*</small>

<style>
.cube1 {
  position: relative;
  transform-style: preserve-3d;
  animation: spin1 20s linear infinite;

  margin: 2em auto 0em;
}

.cube1 > div {
  position: absolute;
}

@keyframes spin1 {
  from {
    transform: rotateX(-0.1turn) rotateY(0turn);
  }
  to {
    transform: rotateX(-0.1turn) rotateY(1turn);
  }
}
</style>

<div class="cube1" style="width:4em; height:8em;">
  <div style="transform: translate3d(0em, 0em, 2em)">A</div>
  <div style="transform: translate3d(4em, 0em, 2em)">B</div>
  <div style="transform: translate3d(0em, 4em, 2em)">C</div>
  <div style="transform: translate3d(4em, 4em, 2em)">D</div>
  <div style="transform: translate3d(0em, 0em, -2em)">E</div>
  <div style="transform: translate3d(4em, 0em, -2em)">F</div>
  <div style="transform: translate3d(0em, 4em, -2em)">G</div>
  <div style="transform: translate3d(4em, 4em, -2em)">H</div>
</div>
