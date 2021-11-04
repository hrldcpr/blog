---
layout: post
title: An Intriguing Triangle
latex: true
date: 2020-08-18 18:18:18 -0400
---

I recently noticed that the triangle with $$n$$th row and $$k$$th column:

$$
\Delta(n, k) = k (n - k)
$$

…is closely related to the binomial coefficients $$n \choose 3$$ and $$n \choose 4$$.

Here are the first several rows of the triangle[^more], along with their sums ∑ and cumulative sums ∑∑:

[^more]:
    Notice that the triangle is just the antidiagonals of a multiplication table:

    ```
    1  2  3  4  5  .  .  .
    2  4  6  8 10
    3  6  9 12 15
    4  8 12 16 20
    5 10 15 20 25
    .              .
    .                 .
    .                    .
    ```

    It's also known as [OEIS A003991](https://oeis.org/A003991).


```
n              𝚫               ∑    ∑∑
2              1               1     1
3            2   2             4     5
4          3   4   3          10    15
5        4   6   6   4        20    35
6      5   8   9   8   5      35    70
              ...
```

(We omit all the zero entries, at $$k=0$$, $$k=n$$, and $$n<2$$.)


## Theorem 1

Note that the binomial coefficients $${3 \choose 3} = 1$$, $${4 \choose 3} = 4$$, $${5 \choose 3} = 10$$, $${6 \choose 3} = 20$$, … look a lot like the ∑ column of the sums of the rows. Sure enough:

$$
\sum_{k=1}^n k (n - k) = {n+1 \choose 3}
$$

### Proof

Using the facts[^sums] that $$\sum_{k=1}^n k = \frac{n(n+1)}{2}$$ and $$\sum_{k=1}^n k^2 = \frac{n(n+1)(2n+1)}{6}$$, we have:

[^sums]:
    $$\sum_{k=1}^n k$$ has many derivations, including this [clever visual one](https://jeremykun.com/2011/10/02/n-choose-2/).

    $$\sum_{k=1}^n k^2$$ can be derived by expanding $$(k-1)^3$$ as illustrated [here](https://brilliant.org/wiki/sum-of-n-n2-or-n3/#sum-of-the-squares-of-the-first-n-positive-integers).

$$
\begin{aligned}
\sum_{k=1}^n k (n - k)
&= n \sum_{k=1}^n k - \sum_{k=1}^n k^2 \\[3ex]
&= n \frac{n(n+1)}{2} - \frac{n(n+1)(2n+1)}{6} \\[3ex]
&= n(n+1) \left( \frac{n}{2} - \frac{2n+1}{6} \right) \\[3ex]
&= n(n+1) \frac{3n - (2n+1)}{6} \\[3ex]
&= \frac{n(n+1)(n-1)}{6} = {n + 1 \choose 3}
\end{aligned}
$$

$$
\tag*{$\blacksquare$}
$$

<br/>


## Theorem 2

Note that the binomial coefficients $${4 \choose 4} = 1$$, $${5 \choose 4} = 5$$, $${6 \choose 4} = 15$$, $${7 \choose 4} = 35$$, … look a lot like the ∑∑ column of the cumulative sums of the rows. Sure enough:

$$
\sum_{m=1}^n \sum_{k=1}^m k(m-k) = \sum_{m=1}^n {m+1 \choose 3} = {n+2 \choose 4}
$$

And in fact, more generally for any $$k$$:

$$
\sum_{m=0}^n {m \choose k} = {n+1 \choose k+1}
$$

### Proof

*(Also proved in the Lean theorem proving language, for fun.[^lean2])*

[^lean2]:
    ```
    theorem two {n k : ℕ} : ∑ m in range n, m.choose k = n.choose (k+1) :=
    begin
      induction n with n hn,
      { refl, },
      { rw [finset.sum_range_succ_comm, hn],
        refl, },
    end
    ```
    (Note that `range n` only goes up to $$n-1$$, so the formula is slightly different. You can [interact with this code](https://leanprover-community.github.io/lean-web-editor/#code=import%20algebra.big_operators.basic%0A%0Aopen_locale%20big_operators%0Aopen%20finset%20%28range%29%0A%0Atheorem%20two%20%7Bn%20k%20%3A%20%E2%84%95%7D%20%3A%20%E2%88%91%20m%20in%20range%20n%2C%20m.choose%20k%20%3D%20n.choose%20%28k%2B1%29%20%3A%3D%0Abegin%0A%20%20induction%20n%20with%20n%20hn%2C%0A%20%20%7B%20refl%2C%20%7D%2C%0A%20%20%7B%20rw%20%5Bfinset.sum_range_succ_comm%2C%20hn%5D%2C%0A%20%20%20%20refl%2C%20%7D%2C%0Aend%0A) in the Lean web editor.)

#### (n = 0)

If $$k=0$$, $$\sum_{m=0}^0 {m \choose 0} = {0 \choose 0} = 1 = {1 \choose 1}$$

Otherwise, $$k>0$$ so $$\sum_{m=0}^0 {m \choose k} = {0 \choose k} = 0 = {1 \choose k+1}$$

#### (n > 0)

Supposing by induction that $$\sum_{m=0}^{n-1} {m \choose k} = {n \choose k+1}$$, we have:

$$
\sum_{m=0}^n {m \choose k} = {n \choose k} + \sum_{m=0}^{n-1} {m \choose k} = {n \choose k} + {n \choose k+1}
$$

But from Pascal's triangle we know $${n \choose k} + {n \choose k + 1} = {n+1 \choose k+1}$$

$$
\tag*{$\blacksquare$}
$$

<br/>

### Visual Interpretation

In the context of Pascal's triangle, $$\sum_{m=0}^n {m \choose k} = {n+1 \choose k+1}$$ says that you can sum a diagonal to find the value of the entry below and to the right.

For $$n=3$$, $$k=1$$ for example, $$\sum_{m=0}^3 {m \choose 1} = 0 + 1 + 2 + 3 = 6 = {4 \choose 2}$$ is illustrated by marking the relevant entries of Pascal's triangle:

```
        1  +0
      1  +1   0
    1  +2   1   0
  1  +3   3   1   0
1   4  =6   4   1   0
```
