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

Several people were surprised to learn that these diagrams don't use any JavaScript or animated image formats, just HTML and CSS. So I thought I'd explain how it works!

## A spinning cube

It turns out CSS supports 3d coordinates—so not just horizontal (x) and vertical (y) positions, but also depth (z)!

So let's build a spinning cube, with a letter at each vertex.

<style>
.cube1 {
  position: relative;
  transform-style: preserve-3d;
  animation: spin 20s linear infinite;

  margin: 2em auto 0em;
}

.cube1 > div {
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

Put it all together and we get:

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

Notice that the letters themselves are rotating, which is kind of cool, but for my diagrams I wanted the symbols to always remain legible.

## Un-spinning the letters

To keep the letters facing forwards, we can 'un-spin' them in the opposite direction, in sync with the spinning parent.

<style>
.cube2 {
  position: relative;
  transform-style: preserve-3d;
  animation: spin 20s linear infinite;

  margin: 2em auto 0em;
}

.cube2 > div {
  position: absolute;
  transform-style: preserve-3d;
}

.cube2 > div > div {
  animation: un-spin 20s linear infinite;
}

@keyframes un-spin {
  from {
    transform: rotateY(0turn);
  }
  to {
    transform: rotateY(-1turn);
  }
}
</style>
<div class="cube2" style="width:4em; height:8em;">
  <div style="transform: translate3d(0em, 0em, 2em)"><div>A</div></div>
  <div style="transform: translate3d(4em, 0em, 2em)"><div>B</div></div>
  <div style="transform: translate3d(0em, 4em, 2em)"><div>C</div></div>
  <div style="transform: translate3d(4em, 4em, 2em)"><div>D</div></div>
  <div style="transform: translate3d(0em, 0em, -2em)"><div>E</div></div>
  <div style="transform: translate3d(4em, 0em, -2em)"><div>F</div></div>
  <div style="transform: translate3d(0em, 4em, -2em)"><div>G</div></div>
  <div style="transform: translate3d(4em, 4em, -2em)"><div>H</div></div>
</div>

To accomplish this we need to add an extra wrapper around each letter, otherwise our new 'un-spinning' `transform: rotateY(...)` will interfere with the divs' `transform: translate3d(...)`.

So the HTML now has an extra div around each letter:

```html
<div id="cube" style="width:4em; height:8em;">
  <div style="transform: translate3d(0em, 0em, 2em)"><div>A</div></div>
  <div style="transform: translate3d(4em, 0em, 2em)"><div>B</div></div>
  <div style="transform: translate3d(0em, 4em, 2em)"><div>C</div></div>
  <div style="transform: translate3d(4em, 4em, 2em)"><div>D</div></div>
  <div style="transform: translate3d(0em, 0em, -2em)"><div>E</div></div>
  <div style="transform: translate3d(4em, 0em, -2em)"><div>F</div></div>
  <div style="transform: translate3d(0em, 4em, -2em)"><div>G</div></div>
  <div style="transform: translate3d(4em, 4em, -2em)"><div>H</div></div>
</div>
```

And the CSS adds an un-spinning animation to these new inner divs:

```css
#cube {
  position: relative;
  transform-style: preserve-3d;
  animation: spin 20s linear infinite;
}

#cube > div {
  position: absolute;
  transform-style: preserve-3d;
}

#cube > div > div {
  animation: un-spin 20s linear infinite;
}

@keyframes spin {
  from {
    transform: rotateX(-0.1turn) rotateY(0turn);
  }
  to {
    transform: rotateX(-0.1turn) rotateY(1turn);
  }
}

@keyframes un-spin {
  from {
    transform: rotateY(0turn);
  }
  to {
    transform: rotateY(-1turn);
  }
}
```

All together this looks like:

<div class="cube2" style="width:4em; height:8em;">
  <div style="transform: translate3d(0em, 0em, 2em)"><div>A</div></div>
  <div style="transform: translate3d(4em, 0em, 2em)"><div>B</div></div>
  <div style="transform: translate3d(0em, 4em, 2em)"><div>C</div></div>
  <div style="transform: translate3d(4em, 4em, 2em)"><div>D</div></div>
  <div style="transform: translate3d(0em, 0em, -2em)"><div>E</div></div>
  <div style="transform: translate3d(4em, 0em, -2em)"><div>F</div></div>
  <div style="transform: translate3d(0em, 4em, -2em)"><div>G</div></div>
  <div style="transform: translate3d(4em, 4em, -2em)"><div>H</div></div>
</div>

I was pleasantly surprised that all this spinning and un-spinning seems to perform fine even on mobile browsers.

You can even select the rotating text and your selection will rotate as well, pretty impressive work by the browser developers.
