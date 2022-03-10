---
layout: post
title: Continued Fraction Streams
latex: true
date: 2016-08-17 17:17:17 -0400
---

Every real number can be represented as a potentially infinite stream of digits and also as a potentially infinite stream of continued fraction coefficients, for example:

$$
1.433127... = 1 + \frac{1}{2 + \frac{1}{3 + \frac{1}{4 + \frac{1}{5 + \ddots}}}} = [1; 2, 3, 4, 5, \dots]
$$

(The final expression uses a less cool-looking but probably more practical notation for continued fractions.)

I wrote [some Python code](https://github.com/hrldcpr/continued) which converts streams of digits to streams of continued fraction coefficients, and vice-versa.

This writeup shows some example uses of the software, and discusses some of the nuances of converting between these infinite streams.

## For Example

Next time you forget the digits of the golden ratio, just remember that its continued fraction coefficients are all ones:

$$
\varphi = 1 + \frac{1}{\varphi} = 1 + \frac{1}{1 + \frac{1}{1 + \frac{1}{1 + \ddots}}}
$$

…then grab an endless stream of ones from the unexpectedly useful `yes` command:

``` bash
> yes 1
1
1
1
1
1
…
```

…and pipe them into the coefficients-to-digits script:

``` bash
> yes 1 | python3 as_digits.py
1.6180339887498948482045868343656381177203091798057628621354
486227052604628189024497072072041893911374847540880753868917
521266338622235369317931800607667263544333890865959395829056
383226613199282902678806752087668925017116962070322210432162
695486262963136144381497587012203408058879544547492461856953
…
```

This will output a never-ending stream of the digits of $$\varphi$$.

To check that things are working, you can even pipe the digits back into the digits-to-coefficients script:

``` bash
> yes 1 | python3 as_digits.py | python3 continued_digits.py
1
1
1
1
1
…
```

Cool it works!


## Lochs' Theorem

One of the countless interesting things about the golden ratio is that it's the "most irrational" number.

One way to glimpse this is while converting its stream of continued fraction coefficients to digits---it takes many coefficients to get each digit:

$$
\begin{array}{r|l}
\text{coefficients in} & \text{digits out} \\
\hline
1 \\
1 \\
1 & 1 \\
  & . \\
1 & 6 \\
1 \\
1 \\
1 & 1 \\
1 \\
1 \\
1 \\
1 \\
1 & 8 \\
\vdots & \vdots
\end{array}
$$

[Lochs' theorem](https://en.wikipedia.org/wiki/Lochs%27_theorem) says that for almost all numbers, it takes 0.97 continued fraction coefficients on average to determine each decimal digit. But for the golden ratio it takes 2.39 coefficients to determine each decimal digit, the worst case[^khinchin] possible.


[^khinchin]: $$\varphi$$ is also the "worst case" regarding [Khinchin's constant](https://en.wikipedia.org/wiki/Khinchin%27s_constant), since the geometric mean of its coefficients is always 1, the smallest possible.


We can see both of these behaviors by comparing $$\varphi$$ to a few random streams of digits. It takes about 970 coefficients to get 1,000 digits for random numbers, but it takes 2,395 coefficients to get 1,000 digits of $$\varphi$$:

![Number of coefficients versus number of decimals, for phi and three random numbers]({{ site.baseurl }}/assets/lochs-phi.svg)


## A Problem

Let's say we've received the digits $$1.43...$$ from our input stream of digits. If we just truncate and compute[^compute] the continued fraction we get:

$$
1.43 = [1; 2, 3, 14]
$$


[^compute]:
    Here's how to compute the continued fraction $$1.43 = [1; 2, 3, 14]$$:

    $$
    \begin{array}{cc}
    x_0 = 1.43 = 1\frac{43}{100} & a_0 = 1 \\[1.2ex]
    x_1 = \frac{100}{43} = 2\frac{14}{43} & a_1 = 2 \\[1.2ex]
    x_2 = \frac{43}{14} = 3\frac{1}{14} & a_2 = 3 \\[1.2ex]
    x_3 = \frac{14}{1} = 14 & a_3 = 14
    \end{array}
    $$


So maybe we can safely emit these coefficients into our output stream and then keep emitting whatever coefficients come next?

$$
\begin{array}{r|l}
\text{digits in} & \text{coefficients out} \\
\hline
1 \\
. \\
4 \\
3 & 1 \\
& 2 \\
& 3 \\
& 14 \\
\vdots & \vdots
\end{array}
$$

Let's say we receive the digit $$3$$ next, so far giving us $$1.433...$$

$$
1.433 = [1; 2, 3, {\bf 4}, 3, 10]
$$

The first three coefficients are the same as what we've already outputted, but the fourth coefficient has changed from $$14$$ to $$4$$!

In most streaming situations there's no way to undo or change something we've already outputted---and we can't wait until the stream ends, because it might be infinite---so we're doomed.


## A Solution

We should emit a coefficient only once we're sure it will never change.

We can do this by seeing what would happen if we receive the smallest or largest digits from the stream in the future, giving us bounds on what could possibly happen.

For example, if we've so far received $$1.43...$$ then the smallest number it could possibly be is if we receive *zeroes forever*, $$1.43000...$$, and the largest number it could be is if we receive *nines forever*, $$1.43999...$$ So we can bound the true number with:

$$
1.43000... \le 1.43... \le 1.43999...
$$

Of course, $$1.43000... = 1.43$$ (equivalent to the stream simply ending) and $$1.43999... = 1.44$$, both of which have finite continued fractions that we can compute:

$$
[{\bf 1}; {\bf 2}, {\bf 3}, 14] = 1.43 \le 1.43... \le 1.44 = [{\bf 1}; {\bf 2}, {\bf 3}, 1, 2]
$$

Both bounds have $$[{\bf 1}; {\bf 2}, {\bf 3}, \dots]$$ in common, so across the entire range of possible values, no matter what the future digits in the stream are, these coefficients will remain the same, and we can safely output them:

$$
\begin{array}{r|l}
1 \\
. \\
4 \\
3 & 1 \\
& 2 \\
& 3 \\
\vdots & \vdots
\end{array}
$$

Here's a more thorough example of what a program would do, processing one digit at a time, and outputting coefficients as soon as they're certain:

$$
[1] = 1 \le 1.\dotso \le 2 = [2]
\\{} % https://github.com/KaTeX/KaTeX/issues/910
[{\bf 1}; {\bf 2}, 2] = 1.4 \le 1.4... \le 1.5 = [{\bf 1}; {\bf 2}]
\\{}
[1; 2, {\bf 3}, 14] = 1.43 \le 1.43... \le 1.44 = [1; 2, {\bf 3}, 1, 2]
$$

$$
\begin{array}{r|l}
1 \\
. \\
4 & 1 \\
  & 2 \\
3 & 3 \\
\vdots & \vdots
\end{array}
$$

### In the other direction

What if we want to go in the other direction, from streams of continued fraction coefficients to streams of digits?

The two biggest changes that can happen to the number are if there are *no more coefficients*, or if there is *one more coefficient and it is a $$1$$*.

If that sounds confusing, remember that all coefficients must be positive integers, and ponder some examples:

$$
1 \le 1 + \ddots \le 1 + \frac{1}{1}
\\[1.5ex]
1 + \frac{1}{2} \ge 1 + \frac{1}{2 + \ddots} \ge 1 + \frac{1}{2 + \frac{1}{1}}
\\[1.5ex]
1 + \frac{1}{2 + \frac{1}{3}} \le 1 + \frac{1}{2 + \frac{1}{3 + \ddots}} \le 1 + \frac{1}{2 + \frac{1}{3 + \frac{1}{1}}}
$$

(Notice that the inequalities alternate back-and-forth. Continued fractions oscillate around their limit---unlike digit representations, which increase toward their limit.)


Using these bounds, we can convert the stream of coefficients to a stream of digits, emitting whatever digits remain unchanged across both bounds:

$$
1 = [1] \le [1; \dots] \le [1; 1] = 2
\\
{\bf 1}.5 = [1; 2] \ge [1; 2, \dots] \ge [1; 2, 1] = {\bf 1}.333...
\\
1.{\bf 4}28571... = [1; 2, 3] \le [1; 2, 3, \dots] \le [1; 2, 3, 1] = 1.{\bf 4}44...
$$

$$
\begin{array}{r|l}
\text{coefficients in} & \text{digits out} \\
\hline
1 \\
2 & 1 \\
  & . \\
3 & 4 \\
\vdots & \vdots
\end{array}
$$

### Yeah!

Generalizing the previous examples, we can always bound a stream of continued fraction coefficients[^infinite] as:

$$
(-1)^n [a_0; a_1, \dots, a_n] \le (-1)^n [a_0; a_1, \dots, a_n, \dots] \le (-1)^n [a_0; a_1, \dots, a_n + 1]
$$


[^infinite]:
    What happens to the bounds if we *know* the stream of continued fraction coefficients is infinite? (This is equivalent to knowing that the number is irrational.)

    We can get arbitrarily close to the stream "ending" if the next coefficient is arbitrarily large. And for the other bound, we can get a $$1$$ followed by an arbitrarily large coefficient.

    So all that happens is that the inequality becomes strict, i.e. it is no longer possible to actually reach the bounds:

    $$
    (-1)^n [a_0; a_1, \dots, a_n] < (-1)^n [a_0; a_1, \dots, a_n, \dots] < (-1)^n [a_0; a_1, \dots, a_n + 1]
    $$

    (Another way to notice this is that the bounds are rational, so of course our irrational number can't equal them.)

    With digits, on the other hand, nothing changes even if we know the stream is infinite. We can still reach both bounds, with an endless stream of zeroes or an endless stream of nines.


And we get an almost identical inequality for digit streams:

$$
d_0.d_1d_2...d_n \le d_0.d_1d_2...d_n... \le d_0.d_1d_2...(d_n + 1)
$$
