---
layout: post
title: Non-Empty Recursion in Elm
---

Elm requires functions to be *total*, one consequence of which is that functions on lists must handle the empty list. For example, since the empty list has no head element, `List.head` has the type:

```elm
List.head : List a -> Maybe a
```

Haskell, on the other hand, allows *partial* functions, so you can write a function on lists which doesn't handle the empty list. So Haskell's `head` just crashes if you give it an empty list, and has the type:

```haskell
head :: [a] -> a
```

I like Elm's approach since it eliminates an entire class of bugs, but it can be annoying if you *know* that your list is non-empty.

Fortunately, you can just use a non-empty list type such as [Cons](http://package.elm-lang.org/packages/hrldcpr/elm-cons/latest/Cons) to avoid both bugs and the hassle of `Maybe`. For example, since non-empty lists always have a head element, `Cons.head` has the type:

```elm
Cons.head : Cons a -> a
```

But things can get tricky if you want to recurse on non-empty lists, since the tail of a non-empty list isn't necessarily non-empty. This writeup shows how to define non-empty lists in a recursion-friendly way.


## Lists

The classic definition of lists in languages like Elm is that they are either the empty list `Nil` or they are a `Cons` of a head element and a tail list:

```elm
type List a = Nil
            | Cons a (List a)
```

So the list `[1, 2, 3]` would be `Cons 1 (Cons 2 (Cons 3 Nil))`.

And since Elm functions are total and must handle all cases, the head of a list is:

```elm
head : List a -> Maybe a
head list =
  case list of
    Nil -> Nothing
    Cons first rest -> Just first
```


## Non-Empty Lists

To define a non-empty list type, which we'll call `Cons`, we can just take the definition of `List` from above and remove `Nil`:

```elm
type Cons a = Cons a (List a)
```

So now we always have a head, and no longer need Maybe:

```elm
head : Cons a -> a
head (Cons first rest) = first
```

But if we want to implement something recursive, such as the maximum element of a Cons, we run into trouble:

```elm
maximum : Cons a -> a
maximum (Cons first rest) =
  case rest of
    Nil -> first
    _ -> max first (maximum ???)  -- rest is a List,
                                  -- not a Cons,
                                  -- so we can't recurse
```

Since Cons is defined in terms of List, we can't easily recurse on it.


## Recursive Non-Empty Lists

But there is a way to define a non-empty list recursively—as a head element, *maybe* followed by a tail non-empty list:[^1]

```elm
Cons a = Cons a (Maybe (Cons a))
```

Now we can recurse easily:[^2]

```elm
maximum : Cons a -> a
maximum (Cons first rest) =
  case rest of
    Nothing -> first
    Just rest -> max first (maximum rest)
```


## Yeah!

If you're using a language with a powerful type system, and you know that a list is going to be non-empty, then you may as well let the compiler know this too by using a non-empty list type.

For example:

- In Elm you can use [Cons](http://package.elm-lang.org/packages/hrldcpr/elm-cons/latest/Cons) from my elm-cons package.
- In Haskell you can use [Data.List.NonEmpty](http://hackage.haskell.org/package/semigroups) from the semigroups package.
- In PureScript you can use [Data.NonEmpty](https://github.com/purescript-contrib/purescript-nonempty/blob/master/src/Data/NonEmpty.purs) from the purescript-nonempty package.
- In Scala you can use [scalaz.NonEmptyList](https://oss.sonatype.org/service/local/repositories/releases/archive/org/scalaz/scalaz_2.11/7.2.4/scalaz_2.11-7.2.4-javadoc.jar/!/index.html#scalaz.NonEmptyList).

Yeah!

There was a small [discussion](https://lobste.rs/s/wjuqbj/non_empty_recursion_elm) of this writeup on lobste.rs


[^1]: Notice that `Maybe (Cons a)` is isomorphic to `List a`, if we treat `Nothing` as the empty list. So our two definitions of `Cons` are equivalent; one is just more convenient for recursion. You can read more about this equivalence in the ["List May Be Cons"](http://package.elm-lang.org/packages/hrldcpr/elm-cons/latest/Cons#list-may-be-cons) section of the elm-cons documentation.


[^2]:
    In elm-cons, since Elm discourages exposing type constructors, you use the [uncons'](http://package.elm-lang.org/packages/hrldcpr/elm-cons/latest/Cons#uncons') function to recurse on a Cons:

    ```elm
    maximum : Cons comparable -> comparable
    maximum c =
      case uncons' c of
        (first, Nothing) -> first
        (first, Just rest) -> max first (maximum rest)
    ```

    Of course, `maximum` is already defined by the package, and even if it weren't you could use a [*non-empty fold*](http://package.elm-lang.org/packages/hrldcpr/elm-cons/latest/Cons#convenient-folding) to more easily define it:

    ```elm
    maximum : Cons comparable -> comparable
    maximum = foldl1 max
    ```
