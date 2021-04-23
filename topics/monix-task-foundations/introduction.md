## Welcome

Welcome to the Monix course!

[Monix](https://monix.io/) is a high-performance Scala / Scala.js library for composing asynchronous, event-based programs.
The library provides several modules that provide different functionality:

- [monix-execution](https://monix.io/api/current/monix/execution/index.html) provides low-level concurrency abstractions that are a companion to `scala.concurrent`
- [monix-catnap](https://monix.io/api/current/monix/catnap/index.html) offers purely-functional, [Cats-Effect friendly](https://github.com/typelevel/cats-effect) abstractions
- [monix-eval](https://monix.io/api/current/monix/eval/index.html) provides `Task` and `Coeval` data types
- [monix-reactive](https://monix.io/api/current/monix/reactive/index.html) provides `Observable`, a Monix take on RxObservable, with a stronger functional influence
- [monix-connect](https://connect.monix.io/) is a set of connectors to use with Monix, similar in spirit to [Alpakka](https://doc.akka.io/docs/alpakka/current/)
- [monix-bio](https://bio.monix.io/docs/introduction) provides an `IO` type for handling concurrency with typed errors
- and more!

## Why Monix?

Many other well-developed libraries work in a similar space to Monix. For example:
- Monix `Task` competes with [cats.effect.IO](https://github.com/typelevel/cats-effect), [Future](https://docs.scala-lang.org/overviews/core/futures.html), and [zio.ZIO](https://zio.dev/)
- Monix `Observable` serves a similar purpose to [Akka Streams](https://doc.akka.io/docs/akka/current/stream/index.html), [fs2.Stream](https://fs2.io/#/), and [ZIO Stream](https://zio.dev/docs/datatypes/datatypes_stream)

What makes Monix unique is that despite a _preference_ for pure functional programming (FP), this preference is not _enforced_; it supports impure libraries, such as Akka, or anything `Future`-based, as well as libraries from the FP ecosystem.
A good example is the `monix-execution` module, which offers many utilities that can be used with `Future`, such as [Local integration with Akka HTTP](https://monix.io/docs/current/execution/local.html#example-repository).

Furthermore, even if you don’t end up using Monix, this course contains a wealth of transferrable knowledge that applies to other FP libraries as well.

## What we will learn

The course is intended for functional programming beginners who have had little or no exposure to effect types like `Task`. Basic Scala knowledge is required, but not much beyond that.

During the beginner level of the course, we will start from nothing and learn how to use a `Task`, and how it can be used in real-life applications. Therefore, the first topic introduces Monix Task.

The second topic revolves around a more significant coding exercise. It is meant to combine our newly-acquired FP knowledge to solve a more complete use case. This gives us a better idea of how different concepts fit together, and can be used in real projects.

## Contributions

All contributions and feedback are very welcome!

The full source of the course is available in the [scalazone/monix](https://github.com/scalazone/monix) repository.

Exercises can be found at [scalazone/monix-exercises](https://github.com/scalazone/monix-exercises).

If you find an issue in any of the lessons, don't hesitate to point them out to us.

Any other ideas for improvement are welcome, and we encourage anyone to open an [issue](https://github.com/scalazone/monix/issues) or a [pull request](https://github.com/scalazone/monix/pulls) to make a proposal.

## Exercises

At the end of each lesson, there are exercises that we can work on to improve our understanding. These come in two forms:
- Coding exercises in a separate repository
- Quiz questions at the end of each lesson on ScalaZONE

### Coding exercises

In the future we plan for ScalaZONE to have integrated coding exercises, but in the meantime, to use the exercises, we will need to fork the [`monix-exercises` repository](https://github.com/scalazone/monix-exercises).

To do this, click on the "Fork" button next to the "Star" button to create a fork of the exercises in your own personal GitHub account. We can then clone this fork with this command:
```sh
git clone git@github.com:github-username/monix-exercises.git
```

This repository includes all the exercises, their solutions, and unit tests that our answer must pass. The exercises are self-paced, and can be followed alongside this course.

### Quiz questions

We have two kinds of question on ScalaZONE, and examples of these are shown below.

?---?

# The first type of question requires us to select just one answer. Let's try this with an easy question now!

Choose the name of the library we are learning:

- [ ] Monaco
- [ ] Monad
- [X] Monix
- [ ] Monday
- [ ] Monster
- [ ] Monkey

# Other questions allow you to choose multiple answers.

These are usually harder because, in order to get the question right, you must consider every possible
answer. For example, for this question, select every programming language containing the letter `a` in its name:

* [ ] F#
* [X] Haskell
* [X] Scala
* [X] Java
* [ ] Kotlin
* [ ] C#