---
layout: post
title: Spinning Diagrams with CSS
description: This article discusses using CSS to make spinning 3D diagrams.
latex: true
postprocess: _scripts/latex3d.py
---

I wrote a little [math thing]({% post_url 2022-08-08-visual-sum-of-cubes %}) last year, which featured equations like this:

$$
\sum_{k=1}^n k^3 = 2\Bigg(122201\Bigg) - 12201 \\[6ex]
$$

Several people expressed surprise that the spinning diagrams don't use any JavaScript or animated image formats, just HTML and CSS. So I thought I'd explain how it works before I forget.

## A spinning cube

We can build a spinning cube, with a letter at each vertex.

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
  from { transform: rotateX(-0.1turn) rotateY(0turn); }
  to { transform: rotateX(-0.1turn) rotateY(1turn); }
}
</style>
<div class="cube1" style="width: 4em; height: 8em;">
  <div style="transform: translate3d(0em, 0em, 2em)">A</div>
  <div style="transform: translate3d(4em, 0em, 2em)">B</div>
  <div style="transform: translate3d(0em, 4em, 2em)">C</div>
  <div style="transform: translate3d(4em, 4em, 2em)">D</div>
  <div style="transform: translate3d(0em, 0em, -2em)">E</div>
  <div style="transform: translate3d(4em, 0em, -2em)">F</div>
  <div style="transform: translate3d(0em, 4em, -2em)">G</div>
  <div style="transform: translate3d(4em, 4em, -2em)">H</div>
</div>

For the HTML, we make a div for each letter and position it with `translate3d`:

```html
<div id="cube" style="width: 4em; height: 8em;">
  <div style="transform: translate3d(0em, 0em, 2em)">A</div>
  <div style="transform: translate3d(4em, 0em, 2em)">B</div>
  …
  <div style="transform: translate3d(0em, 4em, -2em)">G</div>
  <div style="transform: translate3d(4em, 4em, -2em)">H</div>
</div>
```
<small>*(I use `em` units, but `px` or any other unit is fine too. The cube is 4em wide and the vertices are centered around x=2em and z=0em, making it easy to spin about the center.)*</small>

For the CSS, we set an `animation` on the parent from `rotateY(0turn)` to `rotateY(1turn)`:

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

@keyframes spin {
  from { transform: rotateX(-0.1turn) rotateY(0turn); }
  to { transform: rotateX(-0.1turn) rotateY(1turn); }
}
```
<small>*(Note that `1turn` equals `360deg`. And we add a slight tilt `rotateX(-0.1turn)` to make things look better. Finally, for the 3d positions to work, we need `preserve-3d` and `position: relative` on the parent, and `position: absolute` on the children.)*</small>

Put it all together and we get:

<div class="cube1" style="width: 4em; height: 8em;">
  <div style="transform: translate3d(0em, 0em, 2em)">A</div>
  <div style="transform: translate3d(4em, 0em, 2em)">B</div>
  <div style="transform: translate3d(0em, 4em, 2em)">C</div>
  <div style="transform: translate3d(4em, 4em, 2em)">D</div>
  <div style="transform: translate3d(0em, 0em, -2em)">E</div>
  <div style="transform: translate3d(4em, 0em, -2em)">F</div>
  <div style="transform: translate3d(0em, 4em, -2em)">G</div>
  <div style="transform: translate3d(4em, 4em, -2em)">H</div>
</div>

Notice that the letter glyphs themselves are rotating, which is neat, but could make the diagram hard to read.

## Un-spinning the letters

To keep the letters facing forwards, we can 'un-spin' them in sync with the spinning parent, but in the opposite direction.

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
  from { transform: rotateY(0turn); }
  to { transform: rotateY(-1turn); }
}
</style>
<div class="cube2" style="width: 4em; height: 8em;">
  <div style="transform: translate3d(0em, 0em, 2em)"><div>A</div></div>
  <div style="transform: translate3d(4em, 0em, 2em)"><div>B</div></div>
  <div style="transform: translate3d(0em, 4em, 2em)"><div>C</div></div>
  <div style="transform: translate3d(4em, 4em, 2em)"><div>D</div></div>
  <div style="transform: translate3d(0em, 0em, -2em)"><div>E</div></div>
  <div style="transform: translate3d(4em, 0em, -2em)"><div>F</div></div>
  <div style="transform: translate3d(0em, 4em, -2em)"><div>G</div></div>
  <div style="transform: translate3d(4em, 4em, -2em)"><div>H</div></div>
</div>

To accomplish this we add another div around each letter, where we can perform the un-spinning without interfering with the existing `transform`:

```html
<div id="cube" style="width: 4em; height: 8em;">
  <div style="transform: translate3d(0em, 0em, 2em)"><div>A</div></div>
  <div style="transform: translate3d(4em, 0em, 2em)"><div>B</div></div>
  …
  <div style="transform: translate3d(0em, 4em, -2em)"><div>G</div></div>
  <div style="transform: translate3d(4em, 4em, -2em)"><div>H</div></div>
</div>
```

We keep the CSS from before, but give the new inner divs an un-spinning `animation` from `rotateY(0turn)` to `rotateY(-1turn)`:

```css
#cube > div > div {
  animation: un-spin 20s linear infinite;
}

@keyframes un-spin {
  from { transform: rotateY(0turn); }
  to { transform: rotateY(-1turn); }
}
```

All together this looks like:

<div class="cube2" style="width: 4em; height: 8em;">
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

You can even select the rotating text and your selection will rotate as well—impressive work by the browser builders.

$$
\begin{aligned}
\sum_{k=1}^n k^3
&= 1222299 \\[6ex]
\end{aligned}
$$
{: style="margin-top:2em;"}

*The original [math thing]({% post_url 2022-08-08-visual-sum-of-cubes %}) involved a few other tricks—to embed the diagrams in LaTeX and generate their geometries—which for completeness I'll describe as a footnote.[^et-cetera]*

[^et-cetera]:
    The source of the original math thing is a [Markdown/LaTeX file](https://github.com/hrldcpr/poole/blob/master/_posts/2022-08-08-visual-sum-of-cubes.md?plain=1).

    Each diagram is embedded in the LaTeX as a numeric ID, which is then replaced with generated HTML by a [Python script](https://github.com/hrldcpr/poole/blob/master/_scripts/latex3d.py). (The IDs are all at the bottom of the script, after a long mess of typesetting hacks and NumPy geometry.)

    The Python script is run after the Markdown and LaTeX have been rendered because it's specified with `postprocess` in the Markdown front matter, which triggers a `post_convert` Jekyll hook thanks to a [bespoke Jekyll plugin](https://github.com/hrldcpr/poole/blob/master/_plugins/postprocess.rb).

    Lastly, the [relevant CSS](https://github.com/hrldcpr/poole/blob/master/_sass/_latex3d.scss) will look familiar if you've read this far.
