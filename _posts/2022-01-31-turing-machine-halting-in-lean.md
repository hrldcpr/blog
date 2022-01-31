---
layout: post
title: Turing Machine Halting in Lean
date: 2022-01-31 12:12:12 -0400
---

I recently learned the theorem-proving language [Lean](https://leanprover-community.github.io/), and proved whether some very simple Turing machines halt or not. These are my notes on how I did that.

The code is also [on github](https://github.com/hrldcpr/lean-halting) and can be run in the [web-based Lean editor](https://leanprover-community.github.io/lean-web-editor/#url=https%3A%2F%2Fraw.githubusercontent.com%2Fhrldcpr%2Flean-halting%2Fmain%2Fsrc%2Fhalting.lean).


## Basic definitions

There's some existing Turing machinery in the Lean community's amazing library mathlib, so first we import that:
```
import computability.turing_machine
```

Then we define our set of machine states Λ and set of tape symbols Γ[^symbols] and mark both types as `inhabited` by specifying their default elements, because the imported code uses such types:

[^symbols]:
    Lean makes it easy to type Greek letters and math symbols in your code!

    E.g. \Lambda → Λ, \ex → ∃, …

```
inductive Λ -- states
| A
| B
| C

inductive Γ -- symbols
| zero
| one

instance Λ.inhabited : inhabited Λ := ⟨Λ.A⟩
instance Γ.inhabited : inhabited Γ := ⟨Γ.zero⟩
```

And for convenience we define an initial machine configuration, of the initial state (A) and an empty tape:
```
def cfg₀ : turing.TM0.cfg Γ Λ := turing.TM0.init []
```

We want to be able to repeatedly run a Turing machine one step at a time, but the existing `turing.TM0.step` function is inconvenient for this, because it takes a configuration `turing.TM0.cfg Γ Λ` as input but outputs a different type `option (turing.TM0.cfg Γ Λ)`. So we use `option.bind` to define a more convenient function whose input and output are the same type:
```
def step'
  (M : turing.TM0.machine Γ Λ)
  (x : option (turing.TM0.cfg Γ Λ)) :
  option (turing.TM0.cfg Γ Λ) :=
x.bind (turing.TM0.step M)
```

Now we can easily use Lean's `f^[n]` iteration shorthand to define a function which steps a given number of times:
```
def multistep
  (M : turing.TM0.machine Γ Λ)
  (n : ℕ)
  (cfg : turing.TM0.cfg Γ Λ) :
  option (turing.TM0.cfg Γ Λ) :=
step' M^[n] (some cfg)
```


## Some little proofs

Now for fun we can prove some theorems about `multistep`.

If `multistep M n cfg = none` then `multistep M (n + m) cfg = none` for any m, i.e. once the machine has halted it stays halted. We prove this by induction on m:
```
theorem multistep_none_add
  {cfg M n m}
  (hn : multistep M n cfg = none) :
  multistep M (n + m) cfg = none :=
begin
  induction m with m hm,
  { exact hn, },
  { rw [multistep, nat.add_succ, function.iterate_succ_apply',
        ← multistep, hm],
    refl, },
end
```

And we can prove the same thing but for m≥n instead of m+n:
```
theorem multistep_none_ge
  {cfg M n}
  {m ≥ n}
  (hn : multistep M n cfg = none) :
  multistep M m cfg = none :=
begin
  rw ← nat.add_sub_of_le H,
  exact multistep_none_add hn,
end
```
<small>*(Reading these proofs non-interactively isn't very illuminating—you can try clicking through them [in the Lean web editor](https://leanprover-community.github.io/lean-web-editor/#url=https%3A%2F%2Fraw.githubusercontent.com%2Fhrldcpr%2Flean-halting%2Fmain%2Fsrc%2Fhalting.lean), though it might not make much sense if you haven't used a proof assistant before.)*</small>



## Defining halting

With `multistep` defined, we can easily define halting. A machine M halts if there is some n such that it halts after n steps:
```
def halts (M : turing.TM0.machine Γ Λ) : Prop :=
∃ n, multistep M n cfg₀ = none
```

Now we can try using this definition of halting, for a few specific simple Turing machines.


## A machine that halts immediately

First we'll define the simplest possible machine, which just halts (i.e. returns `none`) no matter what its current state and tape symbol are:
```
def M₁ : turing.TM0.machine Γ Λ
| _ _ := none
```

To prove this halts, we basically just run it for one step and see that it has halted.

Specifically, we use Lean's ⟨⟩ implicit constructor syntax to construct a proof of `∃ n, multistep M₁ n cfg₀ = none` (aka `halts M₁`), by specifying n=1 and using `rfl` to prove the trivial `multistep M₁ 1 cfg₀ = none`:
```
theorem M₁_halts : halts M₁ :=
⟨1, rfl⟩
```


## A machine that goes A → B → halt

In state A, this machine goes to state B, and writes the current symbol back to the tape (i.e. basically ignores the tape). And for any other state (including B) it halts:
```
def M₂ : turing.TM0.machine Γ Λ
| Λ.A symbol := some ⟨Λ.B, turing.TM0.stmt.write symbol⟩
| _ _ := none
```

So again we can easily prove that it halts, by simply running it for two steps:
```
theorem M₂_halts : halts M₂ :=
⟨2, rfl⟩
```


## A machine that loops A → B → A → B → ⋯

Proving that a machine halts isn't very interesting since you just run it until it halts. Proving that a machine *doesn't* halt is trickier and potentially more useful (e.g. for helping to determine the values of the [Busy Beaver function](https://en.wikipedia.org/wiki/Busy_beaver)).

This machine loops forever between A and B, while leaving the tape unchanged:
```
def M₃ : turing.TM0.machine Γ Λ
| Λ.A symbol := some ⟨Λ.B, turing.TM0.stmt.write symbol⟩
| Λ.B symbol := some ⟨Λ.A, turing.TM0.stmt.write symbol⟩
| _ _ := none
```
<small>*(We have to specify the final `_ _ := none` because Λ.C is a possible state as far as the type system is concerned.)*</small>

Proving that this machine doesn't halt is more work than the previous trivial halting proofs. First we prove that for any number of steps, the machine always ends up in either state A or state B:
```
lemma M₃_AB_only {n} : ∃ tape,
  multistep M₃ n cfg₀ = some ⟨Λ.A, tape⟩
  ∨ multistep M₃ n cfg₀ = some ⟨Λ.B, tape⟩ :=
begin
  induction n with n hn,
  { existsi _,
    left,
    refl, },
  { cases hn with tape_n hn,
    cases hn; existsi _,
    {
      right,
      rw [multistep, function.iterate_succ_apply', ← multistep,
          hn, step', option.bind, turing.TM0.step],
      simp,
      existsi _,
      existsi _,
      split; refl, },
    {
      left,
      rw [multistep, function.iterate_succ_apply', ← multistep,
          hn, step', option.bind, turing.TM0.step],
      simp,
      existsi _,
      existsi _,
      split; refl, },
  },
end
```
<small>*(Again, reading these proofs non-interactively is probably pointless, try [the Lean web editor](https://leanprover-community.github.io/lean-web-editor/#url=https%3A%2F%2Fraw.githubusercontent.com%2Fhrldcpr%2Flean-halting%2Fmain%2Fsrc%2Fhalting.lean).)*</small>

Now that we know that the machine is always in state A or state B, it's easy to prove that it doesn't halt, by showing that `some A` and `some B` aren't `none` (which comes from a theorem called `option.no_confusion`):
```
theorem M₃_not_halts : ¬ halts M₃ :=
begin
  intro h,
  cases h with n hn,
  cases M₃_AB_only with tape h_tape,
  cases h_tape; {
    rw h_tape at hn,
    exact option.no_confusion hn,
  },
end
```

So there we have it, a Turing machine which clearly loops forever …doesn't halt!

This is pretty obvious, but maybe someday proofs like these could be automatically derived for more complicated machines. But mostly it was a fun way for me to learn Lean!
