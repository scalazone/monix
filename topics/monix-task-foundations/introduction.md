## Welcome

Welcome to the Monix course!

[Monix](https://monix.io/) is a high-performance Scala / Scala.js library for composing asynchronous, event-based programs.
The library provides several modules with different functionality:

- [monix-execution](https://monix.io/api/current/monix/execution/index.html) with low-level concurrency abstractions that is a companion to `scala.concurrent`,
- [monix-catnap](https://monix.io/api/current/monix/catnap/index.html) with purely-functional, [Cats-Effect friendly](https://github.com/typelevel/cats-effect) abstractions,
- [monix-eval](https://monix.io/api/current/monix/eval/index.html) with `Task` and `Coeval` data types,
- [monix-reactive](https://monix.io/api/current/monix/reactive/index.html) with `Observable`, a Monix take on RxObservable with stronger functional influence,
- [monix-connect](https://connect.monix.io/) that is a set of connectors to use with Monix, similar in spirit to [Alpakka](https://doc.akka.io/docs/alpakka/current/),
- [monix-bio](https://bio.monix.io/docs/introduction) with `IO` that has typed errors,
- and others!

## Why Monix?

Many other well-developed libraries work in a similar space to Monix. For example,
- `Task` is competition to [cats.effect.IO](https://github.com/typelevel/cats-effect), [Future](https://docs.scala-lang.org/overviews/core/futures.html), and [zio.ZIO](https://zio.dev/), and,
- `Observable` serves a similar purpose to [Akka Streams](https://doc.akka.io/docs/akka/current/stream/index.html), [fs2.Stream](https://fs2.io/#/) and [ZIO Stream](https://zio.dev/docs/datatypes/datatypes_stream).

What makes Monix unique is that despite a _preference_ for purely-functional programming, this preference is not _enforced_. And it supports impure libraries, such as Akka, or anything Future-based, as well as those from the FP ecosystem.
A good example is the `monix-execution` module which offers many utilities that can be used with `Future`, such as [Local integration with Akka HTTP](https://monix.io/docs/current/execution/local.html#example-repository).

Furthermore, even if not using Monix, this course contains a wealth of transferrable knowledge that can apply to other libraries, too.

## What we will learn

The course is intended for Functional Programming beginners who have had little or no exposure to effect types like `Task`. Basic Scala knowledge is required, but not much beyond that.

During the beginner level of the course, we will start from nothing and learn how to use a `Task` and how it can be used in real-life applications.

The first topic introduces Monix Task.

The second topic revolves around a more significant coding exercise that is meant to combine our newly-acquired knowledge to solve a more complete use case that will give us a better idea of how different concepts fit together and can be used in real projects.

## Exercises

At the end of each lesson, there are exercises that we can work on to improve our understanding. These come in two forms:
- Coding exercises in separate repository
- Quiz questions at the end of each lesson on ScalaZONE

### Coding exercises

Coding exercises are a planned future feature of ScalaZONE, but in the meantime we will need to fork the [`monix-exercises` repository](https://github.com/scalazone/monix-exercises)

Click on the "Fork" button next to the "Star" to create a fork of the exercises in a personal GitHub account. We can then clone this fork with,
```sh
git clone git@github.com:github-username/monix-exercises.git
```

The repository includes all the exercises, their solutions, and unit tests that our answer must pass. The exercises are self-paced, and can be followed alongside this course.

### Quiz questions

We have two kinds of question on ScalaZONE.

?---?
# Some of these require us to select just one answer. Let's try this with an easy question now!

Choose the name of the library we are learning.

- [ ] Monaco
- [ ] Monad
- [X] Monix
- [ ] Monday
- [ ] Monster
- [ ] Monkey

# Other questions may have multiple correct answers. These are usually harder since every option must be considered as a potential answer.

Try this one now: select every programming language containing the letter `a` in its name.

- [ ] F#
- [X] Haskell
- [X] Scala
- [X] Java
- [ ] Kotlin
- [ ] C#

## Contributions

All contributions and feedback are very welcome!

The full source of the course is available in the [scalazone/monix](https://github.com/scalazone/monix) repository.

Exercises can be found at [scalazone/monix-exercises](https://github.com/scalazone/monix-exercises).

Sometimes there might be easy issues to pick up by anyone, so don't hesitate to point them out to us.

Any other ideas for improvement are welcome, and we encourage anyone to open an [issue](https://github.com/scalazone/monix/issues) or a [pull request](https://github.com/scalazone/monix/pulls) to make a proposal.